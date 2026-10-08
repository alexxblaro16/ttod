from __future__ import annotations

import json

from fastapi import Cookie, Header, HTTPException


def _session_value(authorization: str | None, ttod_session: str | None) -> str | None:
    raw = ttod_session.strip() if ttod_session and ttod_session.strip() else None
    if raw is None and authorization and authorization.startswith('Bearer '):
        raw = authorization.removeprefix('Bearer ').strip()
    return raw


def require_session_user(
    authorization: str | None = Header(default=None),
    ttod_session: str | None = Cookie(default=None),
) -> str:
    raw = _session_value(authorization, ttod_session)
    if raw:
        try:
            claims = json.loads(raw)
            user_id = claims.get('userId')
            if isinstance(user_id, str) and user_id.strip():
                return user_id.strip()
        except json.JSONDecodeError:
            return raw
    raise HTTPException(status_code=401, detail='Authentication required')


def require_reviewer_session(
    authorization: str | None = Header(default=None),
    ttod_session: str | None = Cookie(default=None),
) -> str:
    user_id = require_session_user(authorization, ttod_session)
    raw = _session_value(authorization, ttod_session)
    try:
        roles = json.loads(raw or '').get('roles', [])
    except json.JSONDecodeError:
        roles = []
    if not isinstance(roles, list) or not {'reviewer', 'instructor'}.intersection(roles):
        raise HTTPException(status_code=403, detail='Reviewer role required')
    return user_id

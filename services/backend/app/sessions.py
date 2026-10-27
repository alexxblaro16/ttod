"""Shore server-side sessions — Redis or process memory with TTL."""

from __future__ import annotations

import json
import time
from threading import RLock
from typing import Any, Protocol

from .auth import SESSION_ROLES, SessionClaims
from .redis_client import create_redis_client


class SessionStore(Protocol):
    def put(self, sid: str, claims: SessionClaims, *, ttl_seconds: int) -> None: ...
    def get(self, sid: str) -> SessionClaims | None: ...
    def delete(self, sid: str) -> bool: ...


def _claims_to_json(claims: SessionClaims) -> str:
    return json.dumps({
        "user_id": claims.user_id,
        "email": claims.email,
        "roles": list(claims.roles),
    })


def _claims_from_json(raw: str) -> SessionClaims | None:
    try:
        data = json.loads(raw)
    except (TypeError, json.JSONDecodeError):
        return None
    if not isinstance(data, dict):
        return None
    user_id = data.get("user_id")
    email = data.get("email")
    roles = data.get("roles")
    if not isinstance(user_id, str) or not user_id.strip():
        return None
    if not isinstance(email, str) or not email.strip():
        return None
    if not isinstance(roles, list) or any(role not in SESSION_ROLES for role in roles):
        return None
    return SessionClaims(user_id=user_id, email=email, roles=tuple(roles))


class MemorySessionStore:
    def __init__(self) -> None:
        self._entries: dict[str, tuple[str, float]] = {}
        self._lock = RLock()

    def put(self, sid: str, claims: SessionClaims, *, ttl_seconds: int) -> None:
        expires = time.monotonic() + max(ttl_seconds, 1)
        with self._lock:
            self._entries[sid] = (_claims_to_json(claims), expires)

    def get(self, sid: str) -> SessionClaims | None:
        with self._lock:
            entry = self._entries.get(sid)
            if entry is None:
                return None
            raw, expires = entry
            if time.monotonic() > expires:
                del self._entries[sid]
                return None
            return _claims_from_json(raw)

    def delete(self, sid: str) -> bool:
        with self._lock:
            return self._entries.pop(sid, None) is not None


class RedisSessionStore:
    def __init__(self, redis_url: str = "", *, client: Any | None = None):
        self.client = create_redis_client(redis_url, client=client)

    @staticmethod
    def _key(sid: str) -> str:
        return f"ttod:session:{sid}"

    def put(self, sid: str, claims: SessionClaims, *, ttl_seconds: int) -> None:
        self.client.set(self._key(sid), _claims_to_json(claims), ex=max(ttl_seconds, 1))

    def get(self, sid: str) -> SessionClaims | None:
        raw = self.client.get(self._key(sid))
        return _claims_from_json(raw) if raw else None

    def delete(self, sid: str) -> bool:
        return bool(self.client.delete(self._key(sid)))

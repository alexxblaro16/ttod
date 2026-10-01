from __future__ import annotations

from fastapi import HTTPException


SESSION_USERS = {
    "seeded-user-token": "usr-001",
}

VALID_USER_IDS = {
    "usr-001",
    "usr-002",
}


def resolve_session_user(session_token: str | None, bearer_token: str | None) -> str:
    """Resolve a known session or bearer identity, rejecting forged identifiers."""
    if session_token and session_token.strip():
        user_id = SESSION_USERS.get(session_token.strip())
        if user_id is None:
            raise HTTPException(status_code=403, detail="Invalid session")
        return user_id

    if bearer_token and bearer_token.startswith("Bearer "):
        user_id = bearer_token.removeprefix("Bearer ").strip()
        if user_id in VALID_USER_IDS:
            return user_id
        if user_id:
            raise HTTPException(status_code=403, detail="Invalid bearer credential")

    raise HTTPException(status_code=401, detail="Authentication required")
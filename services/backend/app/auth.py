from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from fastapi import Header, HTTPException
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer


@dataclass(frozen=True)
class AccessTokenClaims:
    user_id: str
    role: str


class AuthService:
    def __init__(self, pat_secret: str, pat_ttl_seconds: int = 3600):
        if not pat_secret:
            raise ValueError("PAT secret must not be empty")
        self.pat_ttl_seconds = pat_ttl_seconds
        self._serializer = URLSafeTimedSerializer(pat_secret, salt="ttod-api-pat-v1")

    def issue_pat(self, user_id: str, role: str = "student") -> str:
        if not user_id.strip():
            raise ValueError("user_id must not be empty")
        return self._serializer.dumps({"sub": user_id, "role": role, "typ": "pat"})

    def read_pat(self, token: str) -> AccessTokenClaims | None:
        try:
            payload: Any = self._serializer.loads(token, max_age=self.pat_ttl_seconds)
        except (BadSignature, SignatureExpired):
            return None
        if not isinstance(payload, dict) or payload.get("typ") != "pat":
            return None
        user_id = payload.get("sub")
        role = payload.get("role")
        if not isinstance(user_id, str) or not user_id.strip():
            return None
        if not isinstance(role, str) or not role.strip():
            return None
        return AccessTokenClaims(user_id=user_id, role=role)


class RequireAccessToken:
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service

    def __call__(self, authorization: str | None = Header(default=None)) -> AccessTokenClaims:
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Bearer access token required")
        token = authorization.removeprefix("Bearer ").strip()
        claims = self.auth_service.read_pat(token) if token else None
        if claims is None:
            raise HTTPException(status_code=401, detail="Invalid or expired access token")
        return claims

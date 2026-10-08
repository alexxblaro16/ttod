from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from fastapi import Header, HTTPException
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from passlib.context import CryptContext
from passlib.exc import UnknownHashError


@dataclass(frozen=True)
class AccessTokenClaims:
    user_id: str
    role: str
    email: str = ""


class AuthService:
    def __init__(
        self,
        pat_secret: str,
        pat_ttl_seconds: int = 3600,
        admin_email: str = "admin@ttod.local",
        admin_password_hash: str = "",
    ):
        if len(pat_secret.encode("utf-8")) < 32:
            raise ValueError("PAT secret must contain at least 32 bytes")
        self.pat_ttl_seconds = pat_ttl_seconds
        self.admin_email = admin_email.strip()
        self.admin_password_hash = admin_password_hash.strip()
        self._password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self._dummy_password_hash = self._password_context.hash("not-a-valid-account-password")
        self._serializer = URLSafeTimedSerializer(pat_secret, salt="ttod-api-pat-v1")

    def authenticate_admin(self, email: str, password: str) -> AccessTokenClaims | None:
        password_hash = self.admin_password_hash or self._dummy_password_hash
        try:
            password_is_valid = self._password_context.verify(password, password_hash)
        except (TypeError, ValueError, UnknownHashError):
            password_is_valid = False

        if (
            not self.admin_password_hash
            or email.strip().casefold() != self.admin_email.casefold()
            or not password_is_valid
        ):
            return None
        return AccessTokenClaims(user_id="usr-001", role="admin", email=self.admin_email)

    def issue_pat(self, user_id: str, role: str = "student", email: str = "") -> str:
        if not user_id.strip():
            raise ValueError("user_id must not be empty")
        return self._serializer.dumps({"sub": user_id, "role": role, "email": email, "typ": "pat"})

    def read_pat(self, token: str) -> AccessTokenClaims | None:
        try:
            payload: Any = self._serializer.loads(token, max_age=self.pat_ttl_seconds)
        except (BadSignature, SignatureExpired):
            return None
        if not isinstance(payload, dict) or payload.get("typ") != "pat":
            return None
        user_id = payload.get("sub")
        role = payload.get("role")
        email = payload.get("email", "")
        if not isinstance(user_id, str) or not user_id.strip():
            return None
        if not isinstance(role, str) or not role.strip():
            return None
        if not isinstance(email, str):
            return None
        return AccessTokenClaims(user_id=user_id, role=role, email=email)


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

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from fastapi import Cookie, Header, HTTPException
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from passlib.context import CryptContext
from passlib.exc import UnknownHashError


SESSION_ROLES = frozenset({"student", "reviewer", "instructor"})


@dataclass(frozen=True)
class AccessTokenClaims:
    user_id: str
    role: str
    email: str = ""
    roles: tuple[str, ...] = ()


class AuthService:
    def __init__(
        self,
        pat_secret: str,
        pat_ttl_seconds: int = 3600,
        admin_email: str = "admin@ttod.local",
        admin_password_hash: str = "",
        session_ttl_seconds: int = 3600,
    ):
        if len(pat_secret.encode("utf-8")) < 32:
            raise ValueError("PAT secret must contain at least 32 bytes")
        self.pat_ttl_seconds = pat_ttl_seconds
        self.session_ttl_seconds = session_ttl_seconds
        self.admin_email = admin_email.strip()
        self.admin_password_hash = admin_password_hash.strip()
        self._password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self._dummy_password_hash = self._password_context.hash("not-a-valid-account-password")
        self._session_serializer = URLSafeTimedSerializer(pat_secret, salt="ttod-web-session-v1")
        self._pat_serializer = URLSafeTimedSerializer(pat_secret, salt="ttod-api-pat-v1")

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
        return AccessTokenClaims(
            user_id="usr-001",
            role="admin",
            email=self.admin_email,
            roles=("reviewer", "instructor"),
        )

    def issue_session(
        self,
        user_id: str,
        role: str,
        email: str,
        roles: tuple[str, ...] = (),
    ) -> str:
        if (
            not user_id.strip()
            or role not in {"admin", "user"}
            or not email.strip()
        ):
            raise ValueError("Session identity fields must not be empty")
        if any(not isinstance(session_role, str) or session_role not in SESSION_ROLES for session_role in roles):
            raise ValueError("Session contains an invalid role")
        return self._session_serializer.dumps({
            "sub": user_id,
            "role": role,
            "email": email,
            "roles": list(roles),
            "typ": "session",
        })

    def read_session(self, token: str) -> AccessTokenClaims | None:
        payload = self._read_signed_payload(
            self._session_serializer,
            token,
            self.session_ttl_seconds,
        )
        if payload is None or payload.get("typ") != "session":
            return None
        user_id = payload.get("sub")
        role = payload.get("role")
        email = payload.get("email")
        roles = payload.get("roles", [])
        if (
            not isinstance(user_id, str) or not user_id.strip()
            or not isinstance(role, str) or role not in {"admin", "user"}
            or not isinstance(email, str) or not email.strip()
            or not isinstance(roles, list)
            or any(
                not isinstance(session_role, str) or session_role not in SESSION_ROLES
                for session_role in roles
            )
        ):
            return None
        return AccessTokenClaims(user_id, role, email, tuple(roles))

    def issue_pat(self, user_id: str, role: str = "student", email: str = "") -> str:
        if not user_id.strip():
            raise ValueError("user_id must not be empty")
        return self._pat_serializer.dumps({"sub": user_id, "role": role, "email": email, "typ": "pat"})

    def read_pat(self, token: str) -> AccessTokenClaims | None:
        payload = self._read_signed_payload(
            self._pat_serializer,
            token,
            self.pat_ttl_seconds,
        )
        if payload is None or payload.get("typ") != "pat":
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

    def _read_signed_payload(
        self,
        serializer: URLSafeTimedSerializer,
        token: str,
        max_age: int,
    ) -> dict[str, Any] | None:
        try:
            payload: Any = serializer.loads(token, max_age=max_age)
        except (BadSignature, SignatureExpired):
            return None
        return payload if isinstance(payload, dict) else None


class RequireSession:
    def __init__(self, auth_service: AuthService, *, cookie_only: bool = False):
        self.auth_service = auth_service
        self.cookie_only = cookie_only

    def __call__(
        self,
        authorization: str | None = Header(default=None),
        ttod_session: str | None = Cookie(default=None),
    ) -> AccessTokenClaims:
        token = ttod_session.strip() if ttod_session and ttod_session.strip() else None
        if token is None and not self.cookie_only and authorization and authorization.startswith("Bearer "):
            token = authorization.removeprefix("Bearer ").strip()
        claims = self.auth_service.read_session(token) if token else None
        if claims is None:
            raise HTTPException(status_code=401, detail="Authentication required")
        return claims


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

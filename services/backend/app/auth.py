from __future__ import annotations

import secrets
from dataclasses import dataclass
from typing import Any, Protocol

from fastapi import Cookie, Header, HTTPException
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from passlib.context import CryptContext
from passlib.exc import UnknownHashError


SESSION_COOKIE_NAME = "ttod_session"
SESSION_ROLES = frozenset({"student", "reviewer", "instructor"})


@dataclass(frozen=True)
class SessionClaims:
    user_id: str
    email: str
    roles: tuple[str, ...]


@dataclass(frozen=True)
class AccessTokenClaims:
    user_id: str


class _UserStore(Protocol):
    def get_by_email(self, email: str) -> Any: ...
    def ensure_admin(self, email: str, password_hash: str, *, user_id: str = "usr-001") -> None: ...


class _SessionStore(Protocol):
    def put(self, sid: str, claims: SessionClaims, *, ttl_seconds: int) -> None: ...
    def get(self, sid: str) -> SessionClaims | None: ...
    def delete(self, sid: str) -> bool: ...


class AuthService:
    def __init__(
        self,
        session_secret: str,
        session_ttl_seconds: int,
        admin_email: str,
        admin_password_hash: str,
        pat_secret: str,
        pat_ttl_seconds: int,
        *,
        users: _UserStore | None = None,
        sessions: _SessionStore | None = None,
    ):
        if len(session_secret.encode("utf-8")) < 32:
            raise ValueError("Session secret must contain at least 32 bytes")
        if session_ttl_seconds <= 0:
            raise ValueError("Session TTL must be greater than zero")
        if len(pat_secret.encode("utf-8")) < 32:
            raise ValueError("PAT secret must contain at least 32 bytes")
        if pat_secret == session_secret:
            raise ValueError("PAT secret must differ from the session secret")
        if pat_ttl_seconds <= 0:
            raise ValueError("PAT TTL must be greater than zero")
        self.session_ttl_seconds = session_ttl_seconds
        self.pat_ttl_seconds = pat_ttl_seconds
        # Secreto y sal propios: una cookie de sesión robada no se puede presentar como PAT,
        # ni un PAT filtrado abre una sesión de navegador.
        self._pat_serializer = URLSafeTimedSerializer(pat_secret, salt="ttod-api-pat-v1")
        self.admin_email = admin_email.strip()
        self.admin_password_hash = admin_password_hash.strip()
        self._password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        # Se verifica siempre contra algún hash para que el tiempo de respuesta
        # no revele si la cuenta existe o si el login está deshabilitado.
        self._dummy_password_hash = self._password_context.hash("not-a-valid-account-password")
        self._session_serializer = URLSafeTimedSerializer(session_secret, salt="ttod-web-session-v1")
        self._users = users
        self._sessions = sessions
        if self._users is not None:
            self._users.ensure_admin(self.admin_email, self.admin_password_hash)

    def authenticate(self, email: str, password: str) -> SessionClaims | None:
        if self._users is not None:
            return self._authenticate_user_store(email, password)
        return self._authenticate_env_admin(email, password)

    def _authenticate_env_admin(self, email: str, password: str) -> SessionClaims | None:
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
        return SessionClaims(
            user_id="usr-001",
            email=self.admin_email,
            roles=("reviewer", "instructor"),
        )

    def _authenticate_user_store(self, email: str, password: str) -> SessionClaims | None:
        assert self._users is not None
        user = self._users.get_by_email(email)
        password_hash = (user.password_hash if user is not None else "") or self._dummy_password_hash
        try:
            password_is_valid = self._password_context.verify(password, password_hash)
        except (TypeError, ValueError, UnknownHashError):
            password_is_valid = False
        if user is None or not password_is_valid:
            return None
        return SessionClaims(user_id=user.user_id, email=user.email, roles=tuple(user.roles))

    def issue_session(self, claims: SessionClaims) -> str:
        if not claims.user_id.strip() or not claims.email.strip():
            raise ValueError("Session identity fields must not be empty")
        if any(role not in SESSION_ROLES for role in claims.roles):
            raise ValueError("Session contains an unknown role")
        if self._sessions is not None:
            sid = secrets.token_urlsafe(32)
            self._sessions.put(sid, claims, ttl_seconds=self.session_ttl_seconds)
            return sid
        return self._session_serializer.dumps({
            "sub": claims.user_id,
            "email": claims.email,
            "roles": list(claims.roles),
            "typ": "session",
        })

    def read_session(self, token: str) -> SessionClaims | None:
        if self._sessions is not None:
            stored = self._sessions.get(token)
            if stored is not None:
                return stored
            # Compat: tests / older cookies still use signed blobs without a store entry.
        return self._read_signed_session(token)

    def _read_signed_session(self, token: str) -> SessionClaims | None:
        try:
            payload: Any = self._session_serializer.loads(token, max_age=self.session_ttl_seconds)
        except (BadSignature, SignatureExpired):
            return None
        if not isinstance(payload, dict) or payload.get("typ") != "session":
            return None
        user_id = payload.get("sub")
        email = payload.get("email")
        roles = payload.get("roles")
        if not isinstance(user_id, str) or not user_id.strip():
            return None
        if not isinstance(email, str) or not email.strip():
            return None
        if not isinstance(roles, list) or any(role not in SESSION_ROLES for role in roles):
            return None
        return SessionClaims(user_id=user_id, email=email, roles=tuple(roles))

    def revoke_session(self, token: str) -> bool:
        if self._sessions is None or not token:
            return False
        return self._sessions.delete(token)

    def issue_pat(self, user_id: str) -> str:
        if not user_id.strip():
            raise ValueError("user_id must not be empty")
        return self._pat_serializer.dumps({"sub": user_id, "typ": "pat"})

    def read_pat(self, token: str) -> AccessTokenClaims | None:
        try:
            payload: Any = self._pat_serializer.loads(token, max_age=self.pat_ttl_seconds)
        except (BadSignature, SignatureExpired):
            return None
        if not isinstance(payload, dict) or payload.get("typ") != "pat":
            return None
        user_id = payload.get("sub")
        if not isinstance(user_id, str) or not user_id.strip():
            return None
        return AccessTokenClaims(user_id=user_id)


class RequireSession:
    """Dependencia FastAPI: la sesión web solo se acepta desde la cookie, nunca como Bearer."""

    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service

    def __call__(
        self,
        session_token: str | None = Cookie(default=None, alias=SESSION_COOKIE_NAME),
    ) -> SessionClaims:
        claims = self.auth_service.read_session(session_token) if session_token else None
        if claims is None:
            raise HTTPException(status_code=401, detail="Authentication required")
        return claims


class RequireAccessToken:
    """Dependencia FastAPI para la API pública: solo acepta un PAT en `Authorization: Bearer`."""

    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service

    def __call__(self, authorization: str | None = Header(default=None)) -> AccessTokenClaims:
        scheme, _, token = (authorization or "").partition(" ")
        if scheme.lower() != "bearer" or not token.strip():
            raise HTTPException(
                status_code=401,
                detail="Bearer access token required",
                headers={"WWW-Authenticate": "Bearer"},
            )
        claims = self.auth_service.read_pat(token.strip())
        if claims is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid or expired access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return claims

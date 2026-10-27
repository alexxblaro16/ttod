"""Shore user profiles — Redis or process memory. Never writes ttod.yml."""

from __future__ import annotations

import json
from dataclasses import dataclass
from threading import RLock
from typing import Any, Protocol

from .redis_client import create_redis_client


@dataclass(frozen=True)
class UserRecord:
    user_id: str
    email: str
    password_hash: str
    roles: tuple[str, ...]
    display_name: str = ""

    def to_hash(self) -> dict[str, str]:
        return {
            "user_id": self.user_id,
            "email": self.email,
            "password_hash": self.password_hash,
            "roles": json.dumps(list(self.roles)),
            "display_name": self.display_name,
        }

    @classmethod
    def from_hash(cls, data: dict[str, str]) -> "UserRecord":
        roles_raw = data.get("roles") or "[]"
        roles = tuple(json.loads(roles_raw))
        return cls(
            user_id=data["user_id"],
            email=data["email"],
            password_hash=data["password_hash"],
            roles=roles,
            display_name=data.get("display_name") or "",
        )


class UserStore(Protocol):
    def get_by_id(self, user_id: str) -> UserRecord | None: ...
    def get_by_email(self, email: str) -> UserRecord | None: ...
    def upsert(self, user: UserRecord) -> None: ...
    def ensure_admin(self, email: str, password_hash: str, *, user_id: str = "usr-001") -> None: ...


class MemoryUserStore:
    def __init__(self) -> None:
        self._by_id: dict[str, UserRecord] = {}
        self._email_index: dict[str, str] = {}
        self._lock = RLock()

    def get_by_id(self, user_id: str) -> UserRecord | None:
        with self._lock:
            return self._by_id.get(user_id)

    def get_by_email(self, email: str) -> UserRecord | None:
        with self._lock:
            user_id = self._email_index.get(email.strip().casefold())
            return self._by_id.get(user_id) if user_id else None

    def upsert(self, user: UserRecord) -> None:
        with self._lock:
            self._by_id[user.user_id] = user
            self._email_index[user.email.strip().casefold()] = user.user_id

    def ensure_admin(self, email: str, password_hash: str, *, user_id: str = "usr-001") -> None:
        if not email.strip() or not password_hash.strip():
            return
        if self.get_by_email(email) is not None:
            return
        self.upsert(
            UserRecord(
                user_id=user_id,
                email=email.strip(),
                password_hash=password_hash.strip(),
                roles=("reviewer", "instructor"),
            )
        )


class RedisUserStore:
    def __init__(self, redis_url: str = "", *, client: Any | None = None):
        self.client = create_redis_client(redis_url, client=client)

    @staticmethod
    def _user_key(user_id: str) -> str:
        return f"ttod:user:{user_id}"

    @staticmethod
    def _email_key(email: str) -> str:
        return f"ttod:user:email:{email.strip().casefold()}"

    def get_by_id(self, user_id: str) -> UserRecord | None:
        data = self.client.hgetall(self._user_key(user_id))
        return UserRecord.from_hash(data) if data else None

    def get_by_email(self, email: str) -> UserRecord | None:
        user_id = self.client.get(self._email_key(email))
        return self.get_by_id(user_id) if user_id else None

    def upsert(self, user: UserRecord) -> None:
        pipe = self.client.pipeline()
        pipe.hset(self._user_key(user.user_id), mapping=user.to_hash())
        pipe.set(self._email_key(user.email), user.user_id)
        pipe.execute()

    def ensure_admin(self, email: str, password_hash: str, *, user_id: str = "usr-001") -> None:
        if not email.strip() or not password_hash.strip():
            return
        if self.get_by_email(email) is not None:
            return
        self.upsert(
            UserRecord(
                user_id=user_id,
                email=email.strip(),
                password_hash=password_hash.strip(),
                roles=("reviewer", "instructor"),
            )
        )

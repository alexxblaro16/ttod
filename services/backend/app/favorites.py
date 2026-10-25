from __future__ import annotations

from datetime import datetime, timezone
from threading import RLock
from typing import Any, Protocol

import redis


_favorites: dict[str, dict[str, dict[str, str]]] = {}
_lock = RLock()


def add_favorite(user_id: str, quote_id: str) -> dict[str, str]:
    """Save a favorite without modifying the canonical TTOD corpus."""
    with _lock:
        user_favorites = _favorites.setdefault(user_id, {})
        favorite = user_favorites.get(quote_id)
        if favorite is None:
            favorite = {
                "userId": user_id,
                "quoteId": quote_id,
                "savedAt": datetime.now(timezone.utc).isoformat(),
            }
            user_favorites[quote_id] = favorite
        return dict(favorite)


def get_favorites(user_id: str) -> list[dict[str, str]]:
    with _lock:
        return [dict(favorite) for favorite in _favorites.get(user_id, {}).values()]


def remove_favorite(user_id: str, quote_id: str) -> bool:
    with _lock:
        user_favorites = _favorites.get(user_id)
        if not user_favorites or quote_id not in user_favorites:
            return False
        del user_favorites[quote_id]
        if not user_favorites:
            del _favorites[user_id]
        return True


class FavoriteStore(Protocol):
    def save(self, user_id: str, quote_id: str) -> dict[str, str]: ...
    def list(self, user_id: str) -> list[dict[str, str]]: ...
    def remove(self, user_id: str, quote_id: str) -> bool: ...


class MemoryFavoriteStore:
    """Process-local store: favorites are lost when the backend restarts."""

    def save(self, user_id: str, quote_id: str) -> dict[str, str]:
        return add_favorite(user_id, quote_id)

    def list(self, user_id: str) -> list[dict[str, str]]:
        return get_favorites(user_id)

    def remove(self, user_id: str, quote_id: str) -> bool:
        return remove_favorite(user_id, quote_id)


class RedisFavoriteStore:
    """Persists user preferences without duplicating the governed corpus."""

    def __init__(self, redis_url: str, *, client: Any | None = None):
        self.client = client or redis.Redis.from_url(redis_url, decode_responses=True)

    @staticmethod
    def _key(user_id: str) -> str:
        return f"ttod:favorites:{user_id}"

    def save(self, user_id: str, quote_id: str) -> dict[str, str]:
        # HSETNX keeps the original savedAt when the same quote is saved twice.
        self.client.hsetnx(self._key(user_id), quote_id, datetime.now(timezone.utc).isoformat())
        saved_at = self.client.hget(self._key(user_id), quote_id)
        return {"userId": user_id, "quoteId": quote_id, "savedAt": saved_at}

    def list(self, user_id: str) -> list[dict[str, str]]:
        values = self.client.hgetall(self._key(user_id))
        return [
            {"userId": user_id, "quoteId": quote_id, "savedAt": saved_at}
            for quote_id, saved_at in sorted(values.items(), key=lambda item: item[1], reverse=True)
        ]

    def remove(self, user_id: str, quote_id: str) -> bool:
        return bool(self.client.hdel(self._key(user_id), quote_id))

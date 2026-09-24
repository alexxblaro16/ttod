from __future__ import annotations

from datetime import datetime, timezone
from threading import RLock


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
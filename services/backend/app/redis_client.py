"""Shared Redis client for shore stores (users, sessions, favorites, proposals)."""

from __future__ import annotations

from typing import Any

import redis


def create_redis_client(redis_url: str, *, client: Any | None = None) -> Any:
    """Return a decode_responses client, or an injected test double."""
    if client is not None:
        return client
    if not redis_url.strip():
        raise ValueError("REDIS_URL is empty")
    return redis.Redis.from_url(redis_url, decode_responses=True)


def redis_ping(client: Any) -> bool:
    try:
        return bool(client.ping())
    except redis.RedisError:
        return False

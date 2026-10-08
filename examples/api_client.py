#!/usr/bin/env python3
"""Minimal external client for the TTOD API bearer-token flow."""

from __future__ import annotations

import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def request_json(
    base_url: str,
    path: str,
    *,
    method: str = "GET",
    payload: dict[str, str] | None = None,
    headers: dict[str, str] | None = None,
) -> dict:
    request_headers = {"Accept": "application/json", **(headers or {})}
    body = None
    if payload is not None:
        request_headers["Content-Type"] = "application/json"
        body = json.dumps(payload).encode("utf-8")

    request = Request(
        f"{base_url.rstrip('/')}{path}",
        data=body,
        headers=request_headers,
        method=method,
    )
    try:
        with urlopen(request, timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
        if isinstance(exc, HTTPError):
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"{method} {path} failed ({exc.code}): {detail}") from exc
        raise RuntimeError(f"{method} {path} failed: {exc}") from exc


def main() -> int:
    base_url = os.getenv("TTOD_BASE_URL", "http://localhost:8000")
    email = os.getenv("TTOD_EMAIL", "admin@ttod.local")
    password = os.getenv("TTOD_PASSWORD")
    if not password:
        print("Set TTOD_PASSWORD to the configured admin password.", file=sys.stderr)
        return 2

    try:
        login = request_json(
            base_url,
            "/api/v1/auth/login",
            method="POST",
            payload={"email": email, "password": password},
        )
        session_token = login.get("session_token")
        if not isinstance(session_token, str) or not session_token:
            raise RuntimeError("Login response did not contain session_token")

        token_response = request_json(
            base_url,
            "/api/v1/auth/token",
            method="POST",
            headers={"Cookie": f"ttod_session={session_token}"},
        )
        access_token = token_response.get("access_token")
        if not isinstance(access_token, str) or not access_token:
            raise RuntimeError("Token response did not contain access_token")

        wisdom = request_json(
            base_url,
            "/api/v1/wisdom/random",
            headers={"Authorization": f"Bearer {access_token}"},
        )
    except RuntimeError as exc:
        print(f"TTOD API client error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(wisdom, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

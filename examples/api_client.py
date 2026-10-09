#!/usr/bin/env python3
"""Minimal external client for the TTOD public API.

It is not a second application: it is the smallest script that proves the two
credentials of the API are really two, by walking both flows in order.

    1. POST /api/v1/auth/login   -> a session cookie, for browser-shaped clients
    2. GET  /api/v1/auth/session -> the AuthUser behind that cookie
    3. POST /api/v1/auth/token   -> a bearer token (PAT), which needs the session
    4. GET  /api/v1/wisdom/random-> a quote, and it accepts the PAT *only*

Step 5 is the part worth reading: it sends the session cookie to the bearer-only
route and the PAT to a session-only route, and expects 401 from both. A client
that cannot tell the two apart would pass steps 1-4 and still be wrong.

Usage:

    python examples/api_client.py \
        --base-url http://localhost:8080 \
        --email admin@ttod.local \
        --password "$TTOD_ADMIN_PASSWORD"

Exits non-zero and prints what broke if the API does not honour the contract.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request


SESSION_COOKIE_NAME = "ttod_session"


class ContractError(RuntimeError):
    """The API answered, but not the way the documented contract says it should."""


def call(
    base_url: str,
    method: str,
    path: str,
    *,
    body: dict | None = None,
    session: str | None = None,
    bearer: str | None = None,
) -> tuple[int, dict | list | None]:
    """One HTTP call. Returns (status, parsed body) and never raises on 4xx."""
    data = json.dumps(body).encode("utf-8") if body is not None else None
    request = urllib.request.Request(f"{base_url}{path}", data=data, method=method)
    request.add_header("accept", "application/json")
    if data is not None:
        request.add_header("content-type", "application/json")
    if session is not None:
        request.add_header("cookie", f"{SESSION_COOKIE_NAME}={session}")
    if bearer is not None:
        request.add_header("authorization", f"Bearer {bearer}")

    try:
        with urllib.request.urlopen(request) as response:
            raw = response.read()
            return response.status, json.loads(raw) if raw else None
    except urllib.error.HTTPError as error:
        raw = error.read()
        return error.code, json.loads(raw) if raw else None
    except urllib.error.URLError as error:
        raise ContractError(f"No TTOD instance answered at {base_url}: {error.reason}") from error


def expect(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--base-url", default="http://localhost:8080", help="where TTOD is served")
    parser.add_argument("--email", default="admin@ttod.local")
    parser.add_argument("--password", required=True)
    args = parser.parse_args()
    base = args.base_url.rstrip("/")

    # 1. The session credential.
    status, login = call(base, "POST", "/api/v1/auth/login",
                         body={"email": args.email, "password": args.password})
    expect(status == 200, f"login answered {status}, expected 200 — check the credentials")
    expect(login["token_type"] == "Session", f"login returned token_type {login['token_type']!r}")
    session = login["session_token"]
    print(f"1. logged in as {login['user']['email']} with roles {login['user']['roles']}")

    # 2. The session identifies a real AuthUser (id, email, roles).
    status, user = call(base, "GET", "/api/v1/auth/session", session=session)
    expect(status == 200, f"/auth/session answered {status} to a valid cookie")
    expect(set(user) == {"id", "email", "roles"}, f"AuthUser has unexpected keys: {sorted(user)}")
    print(f"2. the cookie resolves to AuthUser {user['id']}")

    # 3. The bearer credential is minted from the session, not from the password.
    status, issued = call(base, "POST", "/api/v1/auth/token", session=session)
    expect(status == 200, f"/auth/token answered {status} to a valid session")
    expect(issued["token_type"] == "Bearer", f"token_type was {issued['token_type']!r}")
    pat = issued["access_token"]
    print(f"3. minted a bearer token valid for {issued['expires_in']}s")

    # 4. The public API call an external, non-browser client would actually make.
    status, quote = call(base, "GET", "/api/v1/wisdom/random", bearer=pat)
    expect(status == 200, f"/wisdom/random answered {status} to a valid bearer token")
    print(f"4. {quote['id']} ({quote['section']}): {quote['text'][:72]}...")

    # 5. The two credentials are not interchangeable. This is the real assertion.
    checks = (
        ("the session cookie on the bearer-only route",
         call(base, "GET", "/api/v1/wisdom/random", session=session)[0]),
        ("the session value presented as a bearer token",
         call(base, "GET", "/api/v1/wisdom/random", bearer=session)[0]),
        ("the bearer token on a session-only route",
         call(base, "POST", "/api/v1/auth/token", bearer=pat)[0]),
        ("no credential at all",
         call(base, "GET", "/api/v1/wisdom/random")[0]),
    )
    for description, status in checks:
        expect(status == 401, f"{description} answered {status}, expected 401")
    print("5. all four cross-credential attempts were refused with 401")

    print("\nThe API honours the documented contract.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except ContractError as error:
        print(f"\nCONTRACT BROKEN: {error}", file=sys.stderr)
        sys.exit(1)

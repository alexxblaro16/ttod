from __future__ import annotations

from dataclasses import replace

from fastapi.testclient import TestClient

from services.backend.app.main import create_app
from services.backend.tests.support import BackendTestCase


class AuthIntegrationTests(BackendTestCase):
    def issue_token(self, client=None):
        client = client or self.client
        response = client.post(
            "/api/v1/auth/token",
            cookies={"ttod_session": self.session_cookie},
        )
        self.assertEqual(response.status_code, 200)
        return response.json()["access_token"]

    def test_issued_bearer_token_is_distinct_from_session_cookie(self):
        response = self.client.post(
            "/api/v1/auth/token",
            cookies={"ttod_session": self.session_cookie},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["token_type"], "Bearer")
        self.assertNotEqual(response.json()["access_token"], self.session_cookie)

    def test_token_issuance_requires_a_session_cookie(self):
        response = self.client.post(
            "/api/v1/auth/token",
            headers={"Authorization": "Bearer student-1"},
        )
        self.assertEqual(response.status_code, 401)

    def test_token_issuance_rejects_a_forged_json_cookie(self):
        response = self.client.post(
            "/api/v1/auth/token",
            cookies={"ttod_session": '{"userId":"attacker","roles":["instructor"]}'},
        )
        self.assertEqual(response.status_code, 401)

    def test_bearer_token_allows_public_random_wisdom_request(self):
        response = self.client.get(
            "/api/v1/wisdom/random",
            headers={"Authorization": f"Bearer {self.issue_token()}"},
        )
        self.assertEqual(response.status_code, 200)
        quote = response.json()
        self.assertTrue(quote["id"])
        self.assertTrue(quote["text"])
        self.assertIn("rights", quote)

    def test_random_wisdom_rejects_missing_bearer_token(self):
        self.assertEqual(self.client.get("/api/v1/wisdom/random").status_code, 401)

    def test_random_wisdom_rejects_invalid_bearer_token(self):
        response = self.client.get(
            "/api/v1/wisdom/random",
            headers={"Authorization": "Bearer invalid-token"},
        )
        self.assertEqual(response.status_code, 401)

    def test_random_wisdom_rejects_session_cookie_as_bearer_token(self):
        response = self.client.get(
            "/api/v1/wisdom/random",
            headers={"Authorization": f"Bearer {self.session_cookie}"},
        )
        self.assertEqual(response.status_code, 401)

    def test_random_wisdom_rejects_session_cookie_without_bearer_header(self):
        response = self.client.get(
            "/api/v1/wisdom/random",
            cookies={"ttod_session": self.session_cookie},
        )
        self.assertEqual(response.status_code, 401)

    def test_public_api_token_cannot_be_used_as_a_web_session(self):
        pat = self.issue_token()
        response = self.client.get(
            "/api/v1/favorites",
            headers={"Authorization": f"Bearer {pat}"},
        )
        self.assertEqual(response.status_code, 401)

    def test_random_wisdom_rejects_expired_bearer_token(self):
        expired_settings = replace(self.settings, pat_ttl_seconds=-1)
        expired_client = TestClient(create_app(expired_settings, self.oracle))
        token = self.issue_token(expired_client)
        response = expired_client.get(
            "/api/v1/wisdom/random",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code, 401)

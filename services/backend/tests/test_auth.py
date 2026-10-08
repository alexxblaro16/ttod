from __future__ import annotations

from fastapi.testclient import TestClient

from services.backend.app.auth import SESSION_COOKIE_NAME
from services.backend.app.config import REPOSITORY_ROOT, Settings
from services.backend.app.main import create_app

from .support import SEEDED_EMAIL, SEEDED_PASSWORD, AccountsTestCase


class LoginTests(AccountsTestCase):
    def test_wrong_password_is_rejected_without_issuing_a_session(self):
        response = self.client.post(
            "/api/v1/auth/login",
            json={"email": SEEDED_EMAIL, "password": "wrong-password"},
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"detail": "Invalid email or password"})
        self.assertNotIn("session_token", response.json())

    def test_unknown_email_gets_the_same_answer_as_a_wrong_password(self):
        response = self.client.post(
            "/api/v1/auth/login",
            json={"email": "nobody@ttod.local", "password": SEEDED_PASSWORD},
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"detail": "Invalid email or password"})

    def test_seeded_credentials_issue_a_session_the_backend_recognises(self):
        login = self.client.post(
            "/api/v1/auth/login",
            json={"email": SEEDED_EMAIL, "password": SEEDED_PASSWORD},
        )

        self.assertEqual(login.status_code, 200)
        self.assertEqual(login.json()["token_type"], "Session")
        self.assertEqual(login.json()["user"], {
            "id": "usr-001", "email": SEEDED_EMAIL, "roles": ["reviewer", "instructor"],
        })
        session = self.client.get(
            "/api/v1/auth/session",
            cookies={SESSION_COOKIE_NAME: login.json()["session_token"]},
        )
        self.assertEqual(session.status_code, 200)
        self.assertEqual(session.json(), login.json()["user"])

    def test_login_is_disabled_when_no_password_hash_is_configured(self):
        settings = Settings(
            ttod_path=REPOSITORY_ROOT / "ttod.yml",
            schema_dir=REPOSITORY_ROOT / "schema",
            proposal_dir=self.proposal_dir,
            admin_password_hash="",
        )
        client = TestClient(create_app(settings))

        response = client.post(
            "/api/v1/auth/login",
            json={"email": SEEDED_EMAIL, "password": "any-password"},
        )

        self.assertEqual(response.status_code, 401)

    def test_the_stored_credential_is_a_bcrypt_hash_not_the_password(self):
        self.assertTrue(self.settings.admin_password_hash.startswith("$2"))
        self.assertNotIn(SEEDED_PASSWORD, self.settings.admin_password_hash)


class SessionGuardTests(AccountsTestCase):
    def test_request_without_a_session_is_rejected_and_reveals_no_account_data(self):
        response = self.client.get("/api/v1/auth/session")

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"detail": "Authentication required"})
        self.assertNotIn(SEEDED_EMAIL, response.text)

    def test_forged_and_tampered_session_cookies_are_rejected(self):
        session_token = self.login()
        self.client.cookies.clear()

        for cookie_value in ("not-a-signed-token", session_token[:-2] + "xx", "usr-001"):
            with self.subTest(cookie_value=cookie_value[:12]):
                response = self.client.get(
                    "/api/v1/auth/session",
                    cookies={SESSION_COOKIE_NAME: cookie_value},
                )
                self.assertEqual(response.status_code, 401)

    def test_session_value_is_not_accepted_in_the_authorization_header(self):
        session_token = self.login()
        self.client.cookies.clear()

        response = self.client.get(
            "/api/v1/auth/session",
            headers={"Authorization": f"Bearer {session_token}"},
        )

        self.assertEqual(response.status_code, 401)


class ReviewerRoleTests(AccountsTestCase):
    def test_anonymous_request_to_the_review_queue_is_rejected(self):
        self.assertEqual(self.client.get("/api/v1/proposals").status_code, 401)

    def test_student_session_gets_403_and_no_proposals(self):
        author = self.session_for("student-1", "student")
        self.client.post("/api/v1/proposals", json={"text": "A draft", "section": "wisdom"}, cookies=author)

        response = self.client.get("/api/v1/proposals", cookies=author)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {"detail": "Reviewer role required"})

    def test_reviewer_and_instructor_sessions_see_the_queue(self):
        author = self.session_for("student-1", "student")
        self.client.post("/api/v1/proposals", json={"text": "A draft", "section": "wisdom"}, cookies=author)

        for role in ("reviewer", "instructor"):
            with self.subTest(role=role):
                response = self.client.get("/api/v1/proposals", cookies=self.session_for("staff-1", role))
                self.assertEqual(response.status_code, 200)
                self.assertEqual([item["candidate_content"]["text"] for item in response.json()], ["A draft"])

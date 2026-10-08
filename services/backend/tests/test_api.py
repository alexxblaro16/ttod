from __future__ import annotations

import hashlib
import json
import time
from unittest.mock import patch

from ttod_core.proposals import create_proposal

from services.backend.app.auth import SESSION_COOKIE_NAME

from .support import AccountsTestCase


class ProposalEndpointTests(AccountsTestCase):
    def stored_proposals(self) -> list:
        return list(self.proposal_dir.glob("*.json"))

    def test_anonymous_request_is_rejected_and_nothing_is_stored(self):
        response = self.client.post("/api/v1/proposals", json={"text": "A useful quote", "section": "wisdom"})

        self.assertEqual(response.status_code, 401)
        self.assertEqual(self.stored_proposals(), [])

    def test_invalid_or_client_owned_fields_are_rejected(self):
        student = self.session_for("student-1", "student")

        empty_text = self.client.post("/api/v1/proposals", json={"text": "", "section": "wisdom"}, cookies=student)
        forged_origin = self.client.post(
            "/api/v1/proposals",
            json={"text": "A useful quote", "section": "wisdom", "origin": "blackbox"},
            cookies=student,
        )

        self.assertEqual(empty_text.status_code, 422)
        self.assertEqual(forged_origin.status_code, 422)
        self.assertEqual(self.stored_proposals(), [])

    def test_signed_in_student_gets_the_id_of_a_stored_draft_and_the_corpus_is_untouched(self):
        payload = {
            "text": "A useful quote",
            "section": "wisdom",
            "source": "student observation",
            "level": "advanced",
            "tags": ["simplicity"],
            "teaches": "Prefer the smallest useful change.",
            "lang": "en",
        }
        corpus_before = hashlib.sha256(self.settings.ttod_path.read_bytes()).digest()

        response = self.client.post(
            "/api/v1/proposals",
            json=payload,
            cookies=self.session_for("student-1", "student"),
        )

        self.assertEqual(response.status_code, 201)
        created = response.json()
        self.assertEqual(set(created), {"proposal_id", "status"})
        self.assertEqual(created["status"], "proposed")
        stored = json.loads((self.proposal_dir / f"{created['proposal_id']}.json").read_text(encoding="utf-8"))
        self.assertEqual(stored["status"], "proposed")
        self.assertEqual(stored["proposer_id"], "student-1")
        self.assertEqual(stored["candidate_content"], {**payload, "origin": "human"})
        self.assertNotIn("accepted_quote_id", stored)
        self.assertEqual(hashlib.sha256(self.settings.ttod_path.read_bytes()).digest(), corpus_before)

    def test_endpoint_delegates_to_the_shared_create_proposal_primitive(self):
        with patch("services.backend.app.main.create_proposal", wraps=create_proposal) as primitive:
            response = self.client.post(
                "/api/v1/proposals",
                json={"text": "A useful quote", "section": "wisdom"},
                cookies=self.session_for("student-1", "student"),
            )

        self.assertEqual(response.status_code, 201)
        primitive.assert_called_once_with(
            candidate_content={
                "text": "A useful quote", "section": "wisdom", "level": "intermediate",
                "origin": "human", "lang": "en",
            },
            proposer_kind="human",
            proposer_id="student-1",
            generation_method="api-proposal-create",
        )

    def test_storage_failure_is_reported_without_leaking_the_path(self):
        with patch("services.backend.app.main.ProposalStore.save", side_effect=OSError("disk full")):
            response = self.client.post(
                "/api/v1/proposals",
                json={"text": "A useful quote", "section": "wisdom"},
                cookies=self.session_for("student-1", "student"),
            )

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"detail": "Unable to save proposal"})


class PublicApiTokenTests(AccountsTestCase):
    def test_token_endpoint_requires_a_session(self):
        self.assertEqual(self.client.post("/api/v1/auth/token").status_code, 401)

    def test_issued_token_is_not_the_session_value_and_does_not_open_a_session(self):
        session_token, pat = self.issue_pat()

        self.assertNotEqual(pat, session_token)
        as_session = self.client.get("/api/v1/auth/session", cookies={SESSION_COOKIE_NAME: pat})
        self.assertEqual(as_session.status_code, 401)

    def test_valid_bearer_token_gets_a_quote_from_the_corpus(self):
        _session_token, pat = self.issue_pat()

        response = self.client.get("/api/v1/wisdom/random", headers={"Authorization": f"Bearer {pat}"})

        self.assertEqual(response.status_code, 200)
        quote = response.json()
        for field in ("id", "section", "level", "text", "tags", "origin"):
            self.assertIn(field, quote)
        self.assertIn(quote["id"], {entry["id"] for entry in self.snapshots.wisdom()})

    def test_missing_token_is_rejected(self):
        response = self.client.get("/api/v1/wisdom/random")

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.headers["www-authenticate"], "Bearer")
        self.assertEqual(response.json(), {"detail": "Bearer access token required"})

    def test_invalid_token_is_rejected(self):
        response = self.client.get(
            "/api/v1/wisdom/random",
            headers={"Authorization": "Bearer not-a-signed-token"},
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"detail": "Invalid or expired access token"})

    def test_session_cookie_on_its_own_is_rejected(self):
        session_token, _pat = self.issue_pat()

        response = self.client.get("/api/v1/wisdom/random", cookies={SESSION_COOKIE_NAME: session_token})

        self.assertEqual(response.status_code, 401)
        self.assertNotIn("text", response.json())

    def test_session_value_presented_as_bearer_is_rejected(self):
        session_token, _pat = self.issue_pat()

        response = self.client.get(
            "/api/v1/wisdom/random",
            headers={"Authorization": f"Bearer {session_token}"},
        )

        self.assertEqual(response.status_code, 401)

    def test_expired_token_is_rejected(self):
        _session_token, pat = self.issue_pat()

        later = time.time() + self.settings.pat_ttl_seconds + 60
        with patch("itsdangerous.timed.time.time", return_value=later):
            response = self.client.get("/api/v1/wisdom/random", headers={"Authorization": f"Bearer {pat}"})

        self.assertEqual(response.status_code, 401)

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

from services.backend.app.main import create_app
from services.backend.tests.support import BackendTestCase
from ttod_core.repository import ProposalStore


class ProposalApiIntegrationTests(BackendTestCase):
    student_headers = {"Authorization": 'Bearer {"userId":"student-1","roles":["student"]}'}
    proposal_payload = {
        "text": "A useful quote",
        "section": "wisdom",
        "source": "student observation",
        "level": "advanced",
        "tags": ["simplicity"],
        "teaches": "Prefer the smallest useful change.",
        "lang": "en",
    }

    def test_logged_out_student_cannot_submit_proposal(self):
        response = self.client.post(
            "/api/v1/oracle/propose",
            json={
                "query": "What should this teach?",
                "creativeAnswer": "A candidate answer.",
                "locale": "en",
            },
        )
        self.assertEqual(response.status_code, 401)

    def test_logged_in_student_submits_proposal_not_accepted_quote(self):
        before = hashlib.sha256(self.settings.ttod_path.read_bytes()).digest()
        response = self.client.post(
            "/api/v1/oracle/propose",
            headers=self.student_headers,
            json={
                "query": "What should this teach?",
                "creativeAnswer": "A candidate answer.",
                "locale": "en",
            },
        )
        self.assertEqual(response.status_code, 201)
        proposal = response.json()
        self.assertEqual(proposal["status"], "proposed")
        self.assertEqual(proposal["candidate_content"]["origin"], "blackbox")
        self.assertEqual(proposal["candidate_content"]["lang"], "en")
        self.assertNotIn("id", proposal["candidate_content"])

        stored = json.loads(next(Path(self.temp.name).glob("*.json")).read_text())
        self.assertEqual(stored["status"], "proposed")
        self.assertNotIn("accepted_quote_id", stored)
        self.assertEqual(hashlib.sha256(self.settings.ttod_path.read_bytes()).digest(), before)

    def test_student_cannot_read_reviewer_queue_but_reviewer_can(self):
        self.assertEqual(self.client.get("/api/v1/proposals").status_code, 401)
        self.assertEqual(
            self.client.get("/api/v1/proposals", headers=self.student_headers).status_code,
            403,
        )
        reviewer_headers = {"Authorization": 'Bearer {"userId":"reviewer-1","roles":["reviewer"]}'}
        instructor_headers = {"Authorization": 'Bearer {"userId":"instructor-1","roles":["instructor"]}'}
        self.assertEqual(self.client.get("/api/v1/proposals", headers=reviewer_headers).status_code, 200)
        self.assertEqual(self.client.get("/api/v1/proposals", headers=instructor_headers).status_code, 200)

    def test_proposal_endpoint_requires_authentication(self):
        response = self.client.post(
            "/api/v1/proposals",
            json={"text": "A useful quote", "section": "wisdom"},
        )
        self.assertEqual(response.status_code, 401)

    def test_proposal_endpoint_rejects_invalid_payload(self):
        response = self.client.post(
            "/api/v1/proposals",
            headers=self.student_headers,
            json={"text": "", "section": "wisdom"},
        )
        self.assertEqual(response.status_code, 422)

    def test_proposal_endpoint_creates_and_persists_proposal(self):
        response = self.client.post(
            "/api/v1/proposals",
            headers=self.student_headers,
            json=self.proposal_payload,
        )
        self.assertEqual(response.status_code, 201)
        proposal = response.json()
        self.assertTrue(proposal["proposal_id"])
        self.assertEqual(proposal["status"], "proposed")
        self.assertEqual(proposal["proposer_id"], "student-1")
        self.assertEqual(proposal["candidate_content"]["text"], self.proposal_payload["text"])
        self.assertEqual(proposal["candidate_content"]["source"], self.proposal_payload["source"])
        self.assertTrue(Path(proposal["stored_at"]).exists())

    def test_proposal_endpoint_reports_storage_failure(self):
        client = TestClient(create_app(self.settings, self.oracle), raise_server_exceptions=False)
        with patch.object(ProposalStore, "save", side_effect=OSError("disk full")):
            response = client.post(
                "/api/v1/proposals",
                headers=self.student_headers,
                json={"text": "A useful quote", "section": "wisdom"},
            )
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()["detail"], "Unable to save proposal")

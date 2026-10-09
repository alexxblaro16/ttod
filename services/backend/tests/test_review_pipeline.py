from __future__ import annotations

import inspect
import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from services.backend.app.auth import SESSION_COOKIE_NAME, AuthService, SessionClaims
from services.backend.app.config import REPOSITORY_ROOT, Settings
from services.backend.app.main import create_app
from services.backend.app.oracle import OracleService
from services.backend.app.storage import SnapshotService


class FakeOllama:
    async def generate(self, prompt, system):
        yield "answer"


class FakeRetrieval:
    async def semantic_retrieval(self, query, *, top_k, context_tag, section):
        return {"results": [], "indexDigest": "test", "indexedQuotes": 0}


def auth_service_for(settings: Settings) -> AuthService:
    """`AuthService` recibe los parámetros del PAT a partir de la Tarea 5.

    Se le pasa solo lo que acepta su firma actual para que este test siga
    valiendo tanto aquí como más arriba en la pila del equipo.
    """
    candidates = {
        "session_secret": settings.session_secret,
        "session_ttl_seconds": settings.session_ttl_seconds,
        "admin_email": settings.admin_email,
        "admin_password_hash": settings.admin_password_hash,
        "pat_secret": getattr(settings, "pat_secret", None),
        "pat_ttl_seconds": getattr(settings, "pat_ttl_seconds", None),
    }
    accepted = inspect.signature(AuthService.__init__).parameters
    return AuthService(**{name: value for name, value in candidates.items() if name in accepted})


class ReviewPipelineTestCase(unittest.TestCase):
    """Aplicación real con un directorio de propuestas temporal y vacío."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.settings = Settings(
            ttod_path=REPOSITORY_ROOT / "ttod.yml",
            schema_dir=REPOSITORY_ROOT / "schema",
            proposal_dir=Path(self.temp.name),
            ollama_model="test-model",
        )
        snapshots = SnapshotService(self.settings.ttod_path, self.settings.schema_dir)
        oracle = OracleService(self.settings, snapshots, FakeOllama(), FakeRetrieval())
        self.client = TestClient(create_app(self.settings, oracle))
        self.auth_service = auth_service_for(self.settings)

    def session_for(self, user_id: str, *roles: str) -> dict[str, str]:
        """Cookie de sesión firmada para un usuario con los roles indicados."""
        token = self.auth_service.issue_session(
            SessionClaims(user_id=user_id, email=f"{user_id}@ttod.local", roles=tuple(roles))
        )
        return {SESSION_COOKIE_NAME: token}

    def submit_proposal(self, text: str) -> str:
        created = self.client.post(
            "/api/v1/proposals",
            json={"text": text, "section": "wisdom", "level": "intermediate", "lang": "en"},
            cookies=self.session_for("student-1", "student"),
        )
        self.assertEqual(created.status_code, 201)
        self.client.cookies.clear()
        return created.json()["proposal_id"]


class ReviewerQueueGateTests(ReviewPipelineTestCase):
    def test_anonymous_requests_never_see_the_queue(self):
        self.submit_proposal("An anonymous caller must not read the queue.")

        queue = self.client.get("/api/v1/proposals")

        self.assertEqual(queue.status_code, 401)
        self.assertNotIn("proposal_id", queue.text)

    def test_a_signed_in_student_is_refused_with_403_and_sees_no_rows(self):
        """El bloqueo es del servidor: no basta con esconder el botón en la interfaz."""
        self.submit_proposal("A student must not read the reviewer queue.")

        queue = self.client.get("/api/v1/proposals", cookies=self.session_for("student-1", "student"))

        self.assertEqual(queue.status_code, 403)
        self.assertEqual(queue.json(), {"detail": "Reviewer role required"})
        self.assertNotIn("proposal_id", queue.text)

    def test_a_reviewer_sees_the_submitted_proposal_in_the_queue(self):
        proposal_id = self.submit_proposal("A reviewer reads the queue and finds this draft.")

        queue = self.client.get("/api/v1/proposals", cookies=self.session_for("rev-1", "reviewer"))

        self.assertEqual(queue.status_code, 200)
        self.assertEqual([row["proposal_id"] for row in queue.json()], [proposal_id])
        self.assertEqual(queue.json()[0]["status"], "proposed")

    def test_an_instructor_is_allowed_through_the_same_gate(self):
        self.submit_proposal("An instructor reviews too.")

        queue = self.client.get("/api/v1/proposals", cookies=self.session_for("ins-1", "instructor"))

        self.assertEqual(queue.status_code, 200)
        self.assertEqual(len(queue.json()), 1)

    def test_the_queue_is_empty_when_nothing_has_been_proposed(self):
        queue = self.client.get("/api/v1/proposals", cookies=self.session_for("rev-1", "reviewer"))

        self.assertEqual(queue.status_code, 200)
        self.assertEqual(queue.json(), [])


class CanonicalMutationPathTests(ReviewPipelineTestCase):
    def test_submitting_and_reviewing_never_writes_to_the_canonical_corpus(self):
        """`cli.py proposal accept` es la única escritura admitida en ttod.yml."""
        before = self.settings.ttod_path.read_bytes()

        self.submit_proposal("Proposing and listing must not publish anything.")
        self.client.get("/api/v1/proposals", cookies=self.session_for("rev-1", "reviewer"))

        self.assertEqual(self.settings.ttod_path.read_bytes(), before)

    def test_a_submitted_proposal_is_stored_as_a_draft_outside_the_corpus(self):
        proposal_id = self.submit_proposal("Drafts live in the proposal directory.")

        draft = Path(self.temp.name) / f"{proposal_id}.json"

        self.assertTrue(draft.exists())
        self.assertNotIn(proposal_id, self.settings.ttod_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import inspect
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

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


class FavoritesTestCase(unittest.TestCase):
    """Aplicación real con almacén temporal; cada test arranca sin favoritos previos."""

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
        # El almacén es un diccionario de módulo: se aísla para que los tests no se contaminen.
        store = patch("services.backend.app.favorites._favorites", {})
        store.start()
        self.addCleanup(store.stop)

    def session_for(self, user_id: str, *roles: str) -> dict[str, str]:
        """Cookie de sesión firmada para un usuario con los roles indicados."""
        token = self.auth_service.issue_session(
            SessionClaims(user_id=user_id, email=f"{user_id}@ttod.local", roles=tuple(roles))
        )
        return {SESSION_COOKIE_NAME: token}


class FavoritesApiTests(FavoritesTestCase):
    def test_anonymous_requests_are_rejected_and_return_no_rows(self):
        self.client.post(
            "/api/v1/favorites",
            json={"quoteId": "wis-001"},
            cookies=self.session_for("student-1", "student"),
        )
        self.client.cookies.clear()

        listing = self.client.get("/api/v1/favorites")
        saving = self.client.post("/api/v1/favorites", json={"quoteId": "wis-002"})
        removing = self.client.delete("/api/v1/favorites/wis-001")

        for response in (listing, saving, removing):
            self.assertEqual(response.status_code, 401)
        self.assertNotIn("wis-001", listing.text)

    def test_student_saves_a_favorite_and_sees_it_in_the_library(self):
        student = self.session_for("student-1", "student")

        saved = self.client.post("/api/v1/favorites", json={"quoteId": "wis-001"}, cookies=student)

        self.assertEqual(saved.status_code, 201)
        entry = saved.json()
        self.assertEqual(set(entry), {"userId", "quoteId", "savedAt"})
        self.assertEqual((entry["userId"], entry["quoteId"]), ("student-1", "wis-001"))
        self.assertIsNotNone(datetime.fromisoformat(entry["savedAt"]).tzinfo)
        self.assertEqual(self.client.get("/api/v1/favorites", cookies=student).json(), [entry])

    def test_saving_the_same_quote_twice_keeps_a_single_entry(self):
        student = self.session_for("student-1", "student")

        first = self.client.post("/api/v1/favorites", json={"quoteId": "wis-001"}, cookies=student)
        second = self.client.post("/api/v1/favorites", json={"quoteId": "wis-001"}, cookies=student)

        self.assertEqual(second.json(), first.json())
        self.assertEqual(len(self.client.get("/api/v1/favorites", cookies=student).json()), 1)

    def test_removing_a_favorite_takes_it_out_of_the_library(self):
        student = self.session_for("student-1", "student")
        self.client.post("/api/v1/favorites", json={"quoteId": "wis-001"}, cookies=student)

        removed = self.client.delete("/api/v1/favorites/wis-001", cookies=student)
        again = self.client.delete("/api/v1/favorites/wis-001", cookies=student)

        self.assertEqual(removed.status_code, 204)
        self.assertEqual(again.status_code, 404)
        self.assertEqual(self.client.get("/api/v1/favorites", cookies=student).json(), [])

    def test_one_user_cannot_read_or_remove_another_users_favorites(self):
        owner = self.session_for("student-1", "student")
        other = self.session_for("student-2", "student")
        self.client.post("/api/v1/favorites", json={"quoteId": "wis-001"}, cookies=owner)

        self.assertEqual(self.client.get("/api/v1/favorites", cookies=other).json(), [])
        self.assertEqual(self.client.delete("/api/v1/favorites/wis-001", cookies=other).status_code, 404)
        self.assertEqual(len(self.client.get("/api/v1/favorites", cookies=owner).json()), 1)

    def test_the_user_id_comes_from_the_session_not_from_the_request_body(self):
        student = self.session_for("student-1", "student")

        saved = self.client.post(
            "/api/v1/favorites",
            json={"quoteId": "wis-001", "userId": "student-2"},
            cookies=student,
        )

        self.assertEqual(saved.json()["userId"], "student-1")
        self.assertEqual(
            self.client.get("/api/v1/favorites", cookies=self.session_for("student-2", "student")).json(),
            [],
        )

    def test_the_favorites_store_never_touches_the_canonical_corpus(self):
        """La frontera de la ficha: ttod.yml no cambia al guardar un favorito."""
        before = self.settings.ttod_path.read_bytes()

        self.client.post(
            "/api/v1/favorites",
            json={"quoteId": "wis-001"},
            cookies=self.session_for("student-1", "student"),
        )

        self.assertEqual(self.settings.ttod_path.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()

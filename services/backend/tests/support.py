from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient
from passlib.context import CryptContext

from services.backend.app.auth import SESSION_COOKIE_NAME, AuthService, SessionClaims
from services.backend.app.config import REPOSITORY_ROOT, Settings
from services.backend.app.main import create_app
from services.backend.app.oracle import OracleService
from services.backend.app.storage import SnapshotService


SEEDED_EMAIL = "admin@ttod.local"
SEEDED_PASSWORD = "seeded-user-token"
# bcrypt es lento a propósito: el hash se calcula una vez para toda la suite.
SEEDED_PASSWORD_HASH = CryptContext(schemes=["bcrypt"]).hash(SEEDED_PASSWORD)


class AccountsTestCase(unittest.TestCase):
    """Aplicación real con almacenamiento temporal; cada test parte de un estado limpio."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.proposal_dir = Path(self.temp.name)
        self.settings = Settings(
            ttod_path=REPOSITORY_ROOT / "ttod.yml",
            schema_dir=REPOSITORY_ROOT / "schema",
            proposal_dir=self.proposal_dir,
            ollama_model="test-model",
            admin_password_hash=SEEDED_PASSWORD_HASH,
        )
        self.snapshots = SnapshotService(self.settings.ttod_path, self.settings.schema_dir)
        oracle = OracleService(self.settings, self.snapshots)
        self.client = TestClient(create_app(self.settings, oracle))
        self.auth_service = AuthService(
            self.settings.session_secret,
            self.settings.session_ttl_seconds,
            self.settings.admin_email,
            self.settings.admin_password_hash,
            self.settings.pat_secret,
            self.settings.pat_ttl_seconds,
        )
        favorites = patch("services.backend.app.favorites._favorites", {})
        favorites.start()
        self.addCleanup(favorites.stop)

    def login(self) -> str:
        response = self.client.post(
            "/api/v1/auth/login",
            json={"email": SEEDED_EMAIL, "password": SEEDED_PASSWORD},
        )
        self.assertEqual(response.status_code, 200)
        return response.json()["session_token"]

    def session_for(self, user_id: str, *roles: str) -> dict[str, str]:
        """Cookie de sesión firmada para un usuario con los roles indicados."""
        token = self.auth_service.issue_session(
            SessionClaims(user_id=user_id, email=f"{user_id}@ttod.local", roles=tuple(roles))
        )
        return {SESSION_COOKIE_NAME: token}

    def issue_pat(self) -> tuple[str, str]:
        """Devuelve (sesión, PAT) sin dejar cookies en el cliente, como un cliente externo."""
        session_token = self.login()
        issued = self.client.post("/api/v1/auth/token", cookies={SESSION_COOKIE_NAME: session_token})
        self.assertEqual(issued.status_code, 200)
        self.client.cookies.clear()
        return session_token, issued.json()["access_token"]

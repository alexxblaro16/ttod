from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient
from itsdangerous import URLSafeTimedSerializer

from services.backend.app.config import REPOSITORY_ROOT, Settings
from services.backend.app.main import create_app
from services.backend.app.oracle import OracleService
from services.backend.app.storage import SnapshotService


class FakeOllama:
    def __init__(self):
        self.prompt = ""
        self.system = ""

    async def generate(self, prompt, system):
        self.prompt = prompt
        self.system = system
        yield "answer"


class FakeRetrieval:
    async def semantic_retrieval(self, query, *, top_k, context_tag, section):
        return {"results": [{
            "id": "wis-001", "text": "Nearest wisdom", "section": "wisdom",
            "tags": ["simplicity"], "origin": "human", "score": 0.1,
        }], "indexDigest": "digest", "indexedQuotes": 1}


def issue_session_token(settings, user_id="student-1", role="user", email="student@ttod.local", roles=("student",)):
    serializer = URLSafeTimedSerializer(settings.pat_secret, salt="ttod-web-session-v1")
    return serializer.dumps({
        "sub": user_id,
        "role": role,
        "email": email,
        "roles": list(roles),
        "typ": "session",
    })


def session_headers(settings, user_id="student-1", role="user", email="student@ttod.local", roles=("student",)):
    token = issue_session_token(settings, user_id, role, email, roles)
    return {"Authorization": f"Bearer {token}"}


def session_cookies(settings, user_id="student-1", role="user", email="student@ttod.local", roles=("student",)):
    return {
        "ttod_session": issue_session_token(settings, user_id, role, email, roles),
    }


class BackendTestCase(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.settings = Settings(
            ttod_path=REPOSITORY_ROOT / "ttod.yml",
            schema_dir=REPOSITORY_ROOT / "schema",
            proposal_dir=Path(self.temp.name),
            ollama_model="test-model",
        )
        snapshots = SnapshotService(self.settings.ttod_path, self.settings.schema_dir)
        self.ollama = FakeOllama()
        self.oracle = OracleService(self.settings, snapshots, self.ollama, FakeRetrieval())
        self.client = TestClient(create_app(self.settings, self.oracle))
        self.session_cookie = session_cookies(self.settings)["ttod_session"]
        self.student_headers = session_headers(self.settings)
        self.favorites_patch = patch("services.backend.app.favorites._favorites", {})
        self.favorites_patch.start()

    def tearDown(self):
        self.favorites_patch.stop()
        self.temp.cleanup()

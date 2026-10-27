"""Z3–Z4 shore store unit checks (memory + dual-write) without live Redis."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock

import redis
from fastapi.testclient import TestClient
from passlib.context import CryptContext

from ttod_core.proposals import create_proposal
from ttod_core.repository import ProposalStore

from services.backend.app.auth import SESSION_COOKIE_NAME, AuthService, SessionClaims
from services.backend.app.config import REPOSITORY_ROOT, Settings
from services.backend.app.main import create_app
from services.backend.app.proposal_drafts import DualWriteProposalDraftStore
from services.backend.app.sessions import MemorySessionStore
from services.backend.app.users import MemoryUserStore


class FakeRedis:
    def __init__(self):
        self.kv: dict[str, str] = {}
        self.sets: dict[str, set[str]] = {}

    def pipeline(self):
        return self

    def set(self, key, value, ex=None):
        self.kv[key] = value
        return self

    def get(self, key):
        return self.kv.get(key)

    def delete(self, key):
        return int(self.kv.pop(key, None) is not None)

    def sadd(self, key, *members):
        self.sets.setdefault(key, set()).update(members)
        return self

    def smembers(self, key):
        return set(self.sets.get(key, set()))

    def hset(self, key, mapping=None, **kwargs):
        # unused in proposal tests
        return self

    def execute(self):
        return []


class ShoreStoreTests(unittest.TestCase):
    def test_memory_user_store_seeds_admin_once(self):
        store = MemoryUserStore()
        store.ensure_admin("admin@ttod.local", "$2b$12$seededhashplaceholderxxxxxxxxxxxx")
        store.ensure_admin("admin@ttod.local", "$2b$12$other")
        user = store.get_by_email("admin@ttod.local")
        self.assertIsNotNone(user)
        self.assertEqual(user.user_id, "usr-001")
        self.assertEqual(user.password_hash, "$2b$12$seededhashplaceholderxxxxxxxxxxxx")

    def test_memory_session_store_revokes(self):
        store = MemorySessionStore()
        claims = SessionClaims("u1", "u1@ttod.local", ("student",))
        store.put("sid-1", claims, ttl_seconds=60)
        self.assertEqual(store.get("sid-1"), claims)
        self.assertTrue(store.delete("sid-1"))
        self.assertIsNone(store.get("sid-1"))

    def test_auth_with_stores_issues_revocable_opaque_session(self):
        from passlib.context import CryptContext

        password_hash = CryptContext(schemes=["bcrypt"]).hash("secret")
        users = MemoryUserStore()
        sessions = MemorySessionStore()
        auth = AuthService(
            "s" * 32,
            3600,
            "admin@ttod.local",
            password_hash,
            "p" * 32,
            3600,
            users=users,
            sessions=sessions,
        )
        claims = auth.authenticate("admin@ttod.local", "secret")
        self.assertIsNotNone(claims)
        token = auth.issue_session(claims)
        self.assertEqual(auth.read_session(token), claims)
        self.assertTrue(auth.revoke_session(token))
        self.assertIsNone(auth.read_session(token))

    def test_dual_write_proposal_leaves_cli_loadable_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            client = FakeRedis()
            store = DualWriteProposalDraftStore(Path(tmp), client=client)
            proposal = create_proposal(
                candidate_content={
                    "text": "Shore draft",
                    "section": "wisdom",
                    "level": "beginner",
                    "origin": "human",
                    "lang": "en",
                },
                proposer_kind="human",
                proposer_id="student-1",
                generation_method="test",
            )
            store.save(proposal)
            loaded = ProposalStore(Path(tmp)).load(proposal.proposal_id)
            self.assertEqual(loaded.proposal_id, proposal.proposal_id)
            self.assertIn(f"ttod:proposal:{proposal.proposal_id}", client.kv)
            self.assertEqual([p.proposal_id for p in store.list()], [proposal.proposal_id])


class ShoreHttp503Tests(unittest.TestCase):
    """Z6 F1 — 503 matrix beyond favorites (login/logout/proposals)."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.password_hash = CryptContext(schemes=["bcrypt"]).hash("secret")
        self.settings = Settings(
            ttod_path=REPOSITORY_ROOT / "ttod.yml",
            schema_dir=REPOSITORY_ROOT / "schema",
            proposal_dir=Path(self.temp.name),
            admin_email="admin@ttod.local",
            admin_password_hash=self.password_hash,
            redis_url="redis://unused",
            ollama_model="test-model",
        )

    def test_login_returns_503_when_session_store_raises(self):
        sessions = MagicMock()
        sessions.put.side_effect = redis.RedisError("down")
        users = MemoryUserStore()
        users.ensure_admin(self.settings.admin_email, self.password_hash)
        client = TestClient(
            create_app(self.settings, users=users, sessions=sessions, redis_client=object())
        )
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "admin@ttod.local", "password": "secret"},
        )
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json()["detail"], "Session store unavailable")

    def test_logout_returns_503_when_session_delete_raises(self):
        sessions = MagicMock()
        sessions.delete.side_effect = redis.RedisError("down")
        client = TestClient(
            create_app(
                self.settings,
                users=MemoryUserStore(),
                sessions=sessions,
                redis_client=object(),
            )
        )
        response = client.post(
            "/api/v1/auth/logout",
            cookies={SESSION_COOKIE_NAME: "any-sid"},
        )
        self.assertEqual(response.status_code, 503)

    def test_proposal_create_returns_503_when_dual_write_redis_fails(self):
        broken = FakeRedis()

        def boom(*_a, **_k):
            raise redis.RedisError("down")

        broken.execute = boom  # type: ignore[method-assign]
        draft = DualWriteProposalDraftStore(Path(self.temp.name), client=broken)
        users = MemoryUserStore()
        users.ensure_admin(self.settings.admin_email, self.password_hash)
        sessions = MemorySessionStore()
        auth = AuthService(
            self.settings.session_secret,
            self.settings.session_ttl_seconds,
            self.settings.admin_email,
            self.password_hash,
            self.settings.pat_secret,
            self.settings.pat_ttl_seconds,
            users=users,
            sessions=sessions,
        )
        app = create_app(
            self.settings,
            users=users,
            sessions=sessions,
            proposals=draft,
            redis_client=object(),
        )
        client = TestClient(app)
        token = auth.issue_session(
            SessionClaims("usr-001", "admin@ttod.local", ("reviewer", "instructor"))
        )
        response = client.post(
            "/api/v1/proposals",
            json={"text": "Draft under Redis outage", "section": "wisdom"},
            cookies={SESSION_COOKIE_NAME: token},
        )
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json()["detail"], "Proposal store unavailable")


if __name__ == "__main__":
    unittest.main()

"""Usuarios de verdad: el alta se guarda en Redis y los favoritos cuelgan de quien tiene la sesión."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import redis
from fastapi.testclient import TestClient

from services.backend.app.auth import SESSION_COOKIE_NAME, AuthService, SessionClaims
from services.backend.app.config import REPOSITORY_ROOT, Settings
from services.backend.app.main import create_app
from services.backend.app.oracle import OracleService
from services.backend.app.storage import SnapshotService


PASSWORD = "una-clave-larga"


class FakeRedis:
    """Lo justo de Redis para estos almacenes; sobrevive a recrear la aplicación."""

    def __init__(self):
        self.strings: dict[str, str] = {}
        self.hashes: dict[str, dict[str, str]] = {}

    def set(self, key, value, ex=None, nx=False):
        if nx and key in self.strings:
            return None
        self.strings[key] = value
        return True

    def get(self, key):
        return self.strings.get(key)

    def delete(self, key):
        existed = key in self.strings or key in self.hashes
        self.strings.pop(key, None)
        self.hashes.pop(key, None)
        return int(existed)

    def hset(self, key, mapping):
        self.hashes.setdefault(key, {}).update(mapping)
        return len(mapping)

    def hsetnx(self, key, field, value):
        fields = self.hashes.setdefault(key, {})
        if field in fields:
            return 0
        fields[field] = value
        return 1

    def hget(self, key, field):
        return self.hashes.get(key, {}).get(field)

    def hgetall(self, key):
        return dict(self.hashes.get(key, {}))

    def hdel(self, key, field):
        return int(self.hashes.get(key, {}).pop(field, None) is not None)

    def pipeline(self):
        return self

    def execute(self):
        return []

    def ping(self):
        return True


class RedisCaido(FakeRedis):
    def hset(self, key, mapping):
        raise redis.RedisError("simulated outage")


class UserPersistenceTestCase(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.settings = Settings(
            ttod_path=REPOSITORY_ROOT / "ttod.yml",
            schema_dir=REPOSITORY_ROOT / "schema",
            proposal_dir=Path(temp.name),
            ollama_model="test-model",
        )
        self.redis = FakeRedis()
        self.client = self.start_backend()

    def start_backend(self, client=None) -> TestClient:
        """Cada llamada es un backend recién arrancado: solo comparte lo que hay en Redis."""
        snapshots = SnapshotService(self.settings.ttod_path, self.settings.schema_dir)
        oracle = OracleService(self.settings, snapshots)
        return TestClient(create_app(self.settings, oracle, redis_client=client or self.redis))

    def register(self, email="ana@ttod.local", password=PASSWORD, http=None, **extra):
        return (http or self.client).post(
            "/api/v1/auth/register", json={"email": email, "password": password, **extra}
        )

    def stored_user(self, user_id: str) -> dict[str, str]:
        return self.redis.hashes[f"ttod:user:{user_id}"]


class RegisterTests(UserPersistenceTestCase):
    def test_registering_stores_the_user_in_redis_and_opens_a_session(self):
        response = self.register()

        self.assertEqual(response.status_code, 201)
        body = response.json()
        self.assertEqual(body["user"]["email"], "ana@ttod.local")
        self.assertEqual(self.redis.get("ttod:user:email:ana@ttod.local"), body["user"]["id"])
        session = self.client.get(
            "/api/v1/auth/session", cookies={SESSION_COOKIE_NAME: body["session_token"]}
        )
        self.assertEqual(session.json(), body["user"])

    def test_the_password_is_stored_only_as_a_bcrypt_hash(self):
        user_id = self.register().json()["user"]["id"]

        stored = self.stored_user(user_id)
        self.assertTrue(stored["password_hash"].startswith("$2b$"))
        self.assertNotIn(PASSWORD, json.dumps(stored))

    def test_a_client_cannot_choose_its_own_roles_or_id(self):
        response = self.register(roles=["instructor"], id="usr-001", user_id="usr-001")

        user = response.json()["user"]
        self.assertEqual(user["roles"], ["student"])
        self.assertNotEqual(user["id"], "usr-001")
        self.assertEqual(json.loads(self.stored_user(user["id"])["roles"]), ["student"])

    def test_an_email_already_registered_is_rejected_whatever_its_case(self):
        first = self.register(email="ana@ttod.local")

        second = self.register(email="ANA@ttod.local", password="otra-clave-distinta")

        self.assertEqual(second.status_code, 409)
        self.assertEqual(
            [key for key in self.redis.hashes if key.startswith("ttod:user:")],
            [f"ttod:user:{first.json()['user']['id']}"],
        )
        stolen = self.client.post(
            "/api/v1/auth/login", json={"email": "ana@ttod.local", "password": "otra-clave-distinta"}
        )
        self.assertEqual(stolen.status_code, 401)

    def test_invalid_data_is_rejected_without_storing_anything(self):
        for email, password in (
            ("ana@ttod.local", "corta"),
            ("ana@ttod.local", "x" * 73),
            ("ana@ttod.local", "ñ" * 40),  # 40 caracteres, pero 80 bytes
            ("sin-arroba", PASSWORD),
            ("con espacio@ttod.local", PASSWORD),
        ):
            with self.subTest(email=email, password=password[:8]):
                self.assertEqual(self.register(email=email, password=password).status_code, 422)
        self.assertEqual(self.redis.strings, {})

    def test_redis_outage_answers_503_and_creates_no_account(self):
        down = self.start_backend(RedisCaido())

        response = self.register(http=down)

        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json()["detail"], "User store unavailable")


class SurvivesRestartTests(UserPersistenceTestCase):
    def test_the_user_session_and_favorites_survive_a_backend_restart(self):
        registered = self.register().json()
        cookie = {SESSION_COOKIE_NAME: registered["session_token"]}
        self.client.post("/api/v1/favorites", json={"quoteId": "wis-001"}, cookies=cookie)

        restarted = self.start_backend()

        self.assertEqual(restarted.get("/api/v1/auth/session", cookies=cookie).json(), registered["user"])
        self.assertEqual(
            [entry["quoteId"] for entry in restarted.get("/api/v1/favorites", cookies=cookie).json()],
            ["wis-001"],
        )
        restarted.cookies.clear()
        login = restarted.post(
            "/api/v1/auth/login", json={"email": "ana@ttod.local", "password": PASSWORD}
        )
        self.assertEqual(login.status_code, 200)
        self.assertEqual(login.json()["user"], registered["user"])


class FavoriteOwnerTests(UserPersistenceTestCase):
    def cookie_of(self, email: str) -> tuple[str, dict[str, str]]:
        body = self.register(email=email).json()
        self.client.cookies.clear()
        return body["user"]["id"], {SESSION_COOKIE_NAME: body["session_token"]}

    def test_a_favorite_belongs_to_the_logged_in_user_not_to_the_request_body(self):
        ana_id, ana = self.cookie_of("ana@ttod.local")
        luis_id, _ = self.cookie_of("luis@ttod.local")

        saved = self.client.post(
            "/api/v1/favorites", json={"quoteId": "wis-001", "userId": luis_id}, cookies=ana
        )

        self.assertEqual(saved.status_code, 201)
        self.assertEqual(saved.json()["userId"], ana_id)
        self.assertIn("wis-001", self.redis.hashes[f"ttod:favorites:{ana_id}"])
        self.assertNotIn(f"ttod:favorites:{luis_id}", self.redis.hashes)

    def test_each_user_only_sees_their_own_favorites(self):
        ana_id, ana = self.cookie_of("ana@ttod.local")
        luis_id, luis = self.cookie_of("luis@ttod.local")

        self.client.post("/api/v1/favorites", json={"quoteId": "wis-001"}, cookies=ana)
        self.client.post("/api/v1/favorites", json={"quoteId": "wis-002"}, cookies=luis)

        listing = self.client.get("/api/v1/favorites", cookies=ana).json()
        self.assertEqual([(e["userId"], e["quoteId"]) for e in listing], [(ana_id, "wis-001")])
        listing = self.client.get("/api/v1/favorites", cookies=luis).json()
        self.assertEqual([(e["userId"], e["quoteId"]) for e in listing], [(luis_id, "wis-002")])

    def test_a_valid_session_of_a_user_that_does_not_exist_cannot_save_favorites(self):
        # Firmada con el secreto correcto, como una cookie antigua, pero sin usuario detrás.
        signer = AuthService(
            self.settings.session_secret,
            self.settings.session_ttl_seconds,
            self.settings.admin_email,
            self.settings.admin_password_hash,
            self.settings.pat_secret,
            self.settings.pat_ttl_seconds,
        )
        ghost = signer.issue_session(SessionClaims("usr-fantasma", "fantasma@ttod.local", ("student",)))

        response = self.client.post(
            "/api/v1/favorites", json={"quoteId": "wis-001"}, cookies={SESSION_COOKIE_NAME: ghost}
        )

        self.assertEqual(response.status_code, 401)
        self.assertNotIn("ttod:favorites:usr-fantasma", self.redis.hashes)


if __name__ == "__main__":
    unittest.main()

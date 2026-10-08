from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from services.backend.app.config import REPOSITORY_ROOT, Settings
from services.backend.app.favorites import add_favorite, get_favorites, remove_favorite
from services.backend.app.main import create_app
from services.backend.app.oracle import OracleService
from services.backend.app.storage import SnapshotService
from services.backend.tests.support import session_headers


class FakeOllama:
    async def generate(self, prompt, system):
        yield "answer"


class FakeRetrieval:
    async def semantic_retrieval(self, query, *, top_k, context_tag, section):
        return {"results": [], "indexDigest": "test", "indexedQuotes": 0}


class FavoriteStorageTests(unittest.TestCase):
    def test_add_get_and_remove_favorite(self):
        user_id = "favorites-storage-test-user"
        quote_id = "wis-storage-test"

        favorite = add_favorite(user_id, quote_id)

        self.assertEqual(favorite["userId"], user_id)
        self.assertEqual(favorite["quoteId"], quote_id)
        self.assertTrue(favorite["savedAt"])
        self.assertEqual(get_favorites(user_id), [favorite])
        self.assertTrue(remove_favorite(user_id, quote_id))
        self.assertEqual(get_favorites(user_id), [])
        self.assertFalse(remove_favorite(user_id, quote_id))

    def test_duplicate_favorite_keeps_one_saved_entry(self):
        user_id = "favorites-duplicate-test-user"
        quote_id = "wis-duplicate-test"

        first = add_favorite(user_id, quote_id)
        second = add_favorite(user_id, quote_id)

        self.assertEqual(second, first)
        self.assertEqual(get_favorites(user_id), [first])

    def test_storage_isolated_between_users(self):
        quote_id = "wis-isolation-test"
        add_favorite("favorites-user-a", quote_id)
        add_favorite("favorites-user-b", quote_id)

        remove_favorite("favorites-user-a", quote_id)

        self.assertEqual(get_favorites("favorites-user-a"), [])
        self.assertEqual(get_favorites("favorites-user-b")[0]["quoteId"], quote_id)


class FavoriteApiTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        settings = Settings(
            ttod_path=REPOSITORY_ROOT / "ttod.yml",
            schema_dir=REPOSITORY_ROOT / "schema",
            proposal_dir=Path(self.temp.name),
            ollama_model="test-model",
        )
        self.settings = settings
        snapshots = SnapshotService(settings.ttod_path, settings.schema_dir)
        oracle = OracleService(settings, snapshots, FakeOllama(), FakeRetrieval())
        self.client = TestClient(create_app(settings, oracle))

    def tearDown(self):
        self.temp.cleanup()

    def test_favorites_endpoints_require_authentication(self):
        self.assertEqual(self.client.get("/api/v1/favorites").status_code, 401)
        self.assertEqual(
            self.client.post("/api/v1/favorites", json={"quoteId": "wis-auth-test"}).status_code,
            401,
        )
        self.assertEqual(
            self.client.delete("/api/v1/favorites/wis-auth-test").status_code,
            401,
        )

    def test_authenticated_user_can_create_list_and_delete_favorite(self):
        headers = session_headers(self.settings, user_id="favorites-api-user")

        created = self.client.post(
            "/api/v1/favorites",
            headers=headers,
            json={"quoteId": "wis-api-test"},
        )

        self.assertEqual(created.status_code, 201)
        self.assertEqual(created.json()["userId"], "favorites-api-user")
        self.assertEqual(created.json()["quoteId"], "wis-api-test")
        self.assertTrue(created.json()["savedAt"])
        self.assertEqual(
            self.client.get("/api/v1/favorites", headers=headers).json(),
            [created.json()],
        )

        deleted = self.client.delete(
            "/api/v1/favorites/wis-api-test",
            headers=headers,
        )

        self.assertEqual(deleted.status_code, 204)
        self.assertEqual(self.client.get("/api/v1/favorites", headers=headers).json(), [])

    def test_api_isolates_users_when_listing_and_deleting(self):
        user_a = session_headers(self.settings, user_id="favorites-api-user-a")
        user_b = session_headers(self.settings, user_id="favorites-api-user-b")
        quote_id = "wis-api-isolation-test"

        created = self.client.post(
            "/api/v1/favorites",
            headers=user_a,
            json={"quoteId": quote_id},
        )

        self.assertEqual(created.status_code, 201)
        self.assertEqual(self.client.get("/api/v1/favorites", headers=user_b).json(), [])
        self.assertEqual(
            self.client.delete(f"/api/v1/favorites/{quote_id}", headers=user_b).status_code,
            404,
        )
        self.assertEqual(
            self.client.get("/api/v1/favorites", headers=user_a).json(),
            [created.json()],
        )

from __future__ import annotations

from datetime import datetime

from services.backend.tests.support import BackendTestCase, session_headers


class FavoritesLibraryIntegrationTests(BackendTestCase):
    def setUp(self):
        super().setUp()
        self.student_headers = session_headers(self.settings)

    def test_anonymous_library_request_is_rejected_without_favorite_rows(self):
        response = self.client.get("/api/v1/favorites")
        self.assertEqual(response.status_code, 401)
        self.assertNotIn("wis-001", response.text)

    def test_student_can_save_view_and_remove_favorite_entry(self):
        created = self.client.post(
            "/api/v1/favorites",
            headers=self.student_headers,
            json={"quoteId": "wis-001"},
        )
        self.assertEqual(created.status_code, 201)
        entry = created.json()
        self.assertEqual(set(entry), {"userId", "quoteId", "savedAt"})
        self.assertEqual(entry["userId"], "student-1")
        self.assertEqual(entry["quoteId"], "wis-001")
        self.assertIsNotNone(datetime.fromisoformat(entry["savedAt"]))

        listed = self.client.get("/api/v1/favorites", headers=self.student_headers)
        self.assertEqual(listed.status_code, 200)
        self.assertEqual(listed.json(), [entry])

        removed = self.client.delete(
            "/api/v1/favorites/wis-001",
            headers=self.student_headers,
        )
        self.assertEqual(removed.status_code, 204)
        self.assertEqual(self.client.get("/api/v1/favorites", headers=self.student_headers).json(), [])

    def test_favorite_library_is_isolated_between_users(self):
        other_student = session_headers(self.settings, user_id="student-2", roles=("student",))
        created = self.client.post(
            "/api/v1/favorites",
            headers=self.student_headers,
            json={"quoteId": "wis-001"},
        )
        self.assertEqual(created.status_code, 201)
        self.assertEqual(self.client.get("/api/v1/favorites", headers=other_student).json(), [])
        self.assertEqual(
            self.client.delete("/api/v1/favorites/wis-001", headers=other_student).status_code,
            404,
        )

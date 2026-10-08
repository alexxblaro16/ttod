from __future__ import annotations

from datetime import datetime

from .support import AccountsTestCase


class FavoritesLibraryTests(AccountsTestCase):
    def test_anonymous_requests_are_rejected_on_every_route_and_return_no_rows(self):
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

    def test_student_saves_a_favorite_entry_and_sees_it_in_the_library(self):
        student = self.session_for("student-1", "student")

        saved = self.client.post("/api/v1/favorites", json={"quoteId": "wis-001"}, cookies=student)

        self.assertEqual(saved.status_code, 201)
        entry = saved.json()
        self.assertEqual(set(entry), {"userId", "quoteId", "savedAt"})
        self.assertEqual((entry["userId"], entry["quoteId"]), ("student-1", "wis-001"))
        self.assertIsNotNone(datetime.fromisoformat(entry["savedAt"]).tzinfo)
        library = self.client.get("/api/v1/favorites", cookies=student)
        self.assertEqual(library.json(), [entry])

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

"""Exercise the public API using a disposable SQLite database."""

import importlib
import os
from pathlib import Path
import tempfile
import unittest

from fastapi.testclient import TestClient


class DashboardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temp_dir = tempfile.TemporaryDirectory()
        cls.previous_path = os.environ.get("ANDROMEDA_DB_PATH")
        os.environ["ANDROMEDA_DB_PATH"] = str(Path(cls.temp_dir.name) / "insights.db")
        cls.module = importlib.import_module("app")
        cls.client = TestClient(cls.module.app)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.client.close()
        if cls.previous_path is None:
            os.environ.pop("ANDROMEDA_DB_PATH", None)
        else:
            os.environ["ANDROMEDA_DB_PATH"] = cls.previous_path
        cls.temp_dir.cleanup()

    def setUp(self) -> None:
        with self.module.sqlite3.connect(str(self.module.DB_PATH)) as conn:
            conn.execute("DELETE FROM insights")

    def test_health(self) -> None:
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"ok": True, "service": "andromeda-dashboard"})

    def test_round_trip_and_newest_first(self) -> None:
        for item_id, timestamp in [("old", 1), ("new", 2)]:
            response = self.client.post("/api/insights", json={
                "id": item_id, "ts": timestamp,
                "title": "Local signal", "evidence": {"host": "pi"},
                "recommended_actions": [{"label": "Review"}],
            })
            self.assertEqual(response.status_code, 200)
        items = self.client.get("/api/insights?limit=1").json()["items"]
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["id"], "new")
        self.assertEqual(items[0]["evidence"], {"host": "pi"})

    def test_sql_text_is_stored_as_data(self) -> None:
        title = "'); DROP TABLE insights; --"
        self.client.post("/api/insights", json={"id": "sql", "title": title})
        items = self.client.get("/api/insights").json()["items"]
        self.assertEqual(items[0]["title"], title)

    def test_limit_rejects_invalid_and_unbounded_values(self) -> None:
        for limit in ["-1", "0", "101", "abc"]:
            with self.subTest(limit=limit):
                self.assertEqual(self.client.get(f"/api/insights?limit={limit}").status_code, 422)

    def test_replacing_an_id_preserves_a_single_record(self) -> None:
        for title in ["first", "updated"]:
            self.client.post("/api/insights", json={"id": "same", "title": title})
        items = self.client.get("/api/insights").json()["items"]
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["title"], "updated")

    def test_insights_page_is_served(self) -> None:
        response = self.client.get("/insights")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/html", response.headers["content-type"])


if __name__ == "__main__":
    unittest.main()

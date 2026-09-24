from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from services.backend.app.config import REPOSITORY_ROOT, Settings
from services.backend.app.main import create_app
from services.backend.app.oracle import OracleService
from services.backend.app.storage import SnapshotService
from ttod_core.repository import TTODRepository


FIXTURES = REPOSITORY_ROOT / "tests" / "fixtures"


class _Ollama:
    async def generate(self, prompt, system):
        yield "test segment"


class _Retrieval:
    def __init__(self, score=0.1): self.score = score
    async def semantic_retrieval(self, query, *, top_k, context_tag, section):
        return {"results": [{"id": "wis-001", "text": "Wisdom", "section": "wisdom", "tags": ["simplicity"], "origin": "human", "score": self.score}], "indexDigest": "fixture", "indexedQuotes": 1}


class R7PlatformContracts(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.settings = Settings(ttod_path=REPOSITORY_ROOT / "ttod.yml", schema_dir=REPOSITORY_ROOT / "schema", proposal_dir=Path(self.temp.name), ollama_model="fixture")
        snapshots = SnapshotService(self.settings.ttod_path, self.settings.schema_dir)
        self.client = TestClient(create_app(self.settings, OracleService(self.settings, snapshots, _Ollama(), _Retrieval())))

    def tearDown(self): self.temp.cleanup()

    def test_read_endpoint_shapes_rights_and_determinism(self):
        health = self.client.get("/health"); self.assertEqual(health.status_code, 200); self.assertIsInstance(health.json()["status"], str)
        definitions = self.client.get("/api/v1/schema/definitions").json(); self.assertTrue(all(isinstance(definitions[k], dict) for k in ("quote", "ttod", "proposal")))
        wisdom = self.client.get("/api/v1/wisdom/sample").json()
        required = {"id", "section", "level", "text", "teaches", "tags", "related", "origin", "lang", "rights"}
        self.assertTrue(wisdom and all(required <= entry.keys() for entry in wisdom))
        self.assertTrue(all(isinstance(entry["tags"], list) and isinstance(entry["rights"]["license"], str) for entry in wisdom))
        first = self.client.get("/api/v1/graph"); second = self.client.get("/api/v1/graph")
        self.assertEqual(first.content, second.content)
        graph = first.json(); self.assertTrue(all({"id", "section", "origin", "status", "text", "lang"} <= node.keys() for node in graph["nodes"]))
        self.assertTrue(all(node["status"] == "active" for node in graph["nodes"]))
        emitted = {entry["id"] for entry in wisdom}
        root = TTODRepository(REPOSITORY_ROOT / "ttod.yml", schema_dir=REPOSITORY_ROOT / "schema").load()
        forbidden = {q["id"] for q in root["quotes"] if q.get("status", "active") != "active" or q.get("rights", {}).get("access") != "public"}
        self.assertTrue(emitted.isdisjoint(forbidden))

    def test_named_threshold_calibration(self):
        fixture = json.loads((FIXTURES / "r_oracle_threshold_calibration.json").read_text())
        threshold = fixture["threshold"]
        for case in fixture["cases"]:
            with self.subTest(case=case["name"]):
                verdict = "grounded" if case["top_score"] >= threshold else "creative"
                self.assertEqual(verdict, case["expected"])

    def test_oracle_proposal_fixture_can_never_activate(self):
        fixture = json.loads((FIXTURES / "r_negative_oracle_propose_no_active.json").read_text())
        response = self.client.post(
            "/api/v1/oracle/propose",
            headers={"Authorization": "Bearer student-fixture"},
            json=fixture["request"],
        )
        self.assertEqual(response.status_code, 201)
        proposal = response.json(); expected = fixture["required"]
        self.assertEqual(proposal["status"], expected["status"])
        self.assertEqual(proposal["candidate_content"]["origin"], expected["origin"])
        self.assertNotIn("id", proposal["candidate_content"])
        self.assertNotIn("accepted_quote_id", proposal)

    def test_creative_envelope_has_no_citations(self):
        creative = self.client.post("/api/v1/oracle/stream", json={"query": "unmatched", "sessionHistory": []}).text
        envelope = json.loads(creative.removeprefix("data: ").strip())
        self.assertEqual(envelope["mode"], "creative"); self.assertNotIn("citedQuoteIds", envelope)


if __name__ == "__main__": unittest.main()

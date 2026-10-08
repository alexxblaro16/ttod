from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from services.backend.app.config import REPOSITORY_ROOT, Settings
from services.backend.app.main import create_app
from services.backend.app.oracle import (
    CREATIVE_PROMPT,
    FastMCPRetrievalClient,
    OracleService,
    build_user_prompt,
    detect_language,
    normalize_retrieval_envelope,
    thematic_frame,
)
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


class BackendTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.settings = Settings(
            ttod_path=REPOSITORY_ROOT / "ttod.yml", schema_dir=REPOSITORY_ROOT / "schema",
            proposal_dir=Path(self.temp.name), ollama_model="test-model",
        )
        self.snapshots = SnapshotService(self.settings.ttod_path, self.settings.schema_dir)
        self.ollama = FakeOllama()
        self.oracle = OracleService(self.settings, self.snapshots, self.ollama, FakeRetrieval())
        self.client = TestClient(create_app(self.settings, self.oracle))

    def tearDown(self):
        self.temp.cleanup()

    def test_health_schema_and_public_projections(self):
        self.assertEqual(self.client.get("/health").status_code, 200)
        self.assertIn("properties", self.client.get("/api/v1/schema/definitions").json()["quote"])
        wisdom = self.client.get("/api/v1/wisdom/sample").json()
        self.assertTrue(wisdom)
        self.assertTrue(all(q["rights"]["license"] and "validation" not in q for q in wisdom))
        graph = self.client.get("/api/v1/graph").json()
        self.assertTrue(graph["nodes"])
        self.assertTrue(all(n["status"] == "active" for n in graph["nodes"]))

    def test_graph_is_byte_deterministic(self):
        self.assertEqual(self.client.get("/api/v1/graph").content, self.client.get("/api/v1/graph").content)

    def test_creative_stream_discloses_mode_without_citations(self):
        response = self.client.post(
            "/api/v1/oracle/stream",
            json={"query": "unmatched", "sessionHistory": [], "locale": "en"},
        )
        envelope = json.loads(response.text.removeprefix("data: ").strip())
        self.assertEqual(envelope["mode"], "creative")
        self.assertNotIn("citedQuoteIds", envelope)
        self.assertEqual(envelope["themes"], ["wisdom"])
        self.assertEqual(envelope["tags"], ["simplicity"])
        self.assertIn("MUST NOT", self.ollama.system)
        self.assertIn("koan", self.ollama.system.lower())
        self.assertIn("Thematic anchors — knowledge areas: wisdom", self.ollama.prompt)
        self.assertIn("Thematic anchors — tags: simplicity", self.ollama.prompt)
        self.assertIn("Respond in en.", self.ollama.system)

    def test_locale_overrides_heuristic_language(self):
        self.assertEqual(detect_language("The router hangs", "es"), "es")
        self.assertEqual(detect_language("¿Cómo simplifico?", "en"), "en")

    def test_thematic_frame_and_creative_prompt_forbid_debugging(self):
        ranked = [{
            "id": "ops-001", "text": "x", "section": "ops", "tags": ["observability", "ops"],
            "origin": "human", "score": 0.4,
        }]
        frame = thematic_frame(ranked)
        self.assertEqual(frame, {"themes": ["ops"], "tags": ["observability", "ops"]})
        prompt = build_user_prompt(
            query="router hangs", session_history=[], ranked=ranked, frame=frame, grounded=False,
        )
        self.assertIn("below threshold", prompt)
        self.assertIn("MUST NOT", CREATIVE_PROMPT)

    def test_oracle_propose_cannot_activate_or_allocate_canonical_id(self):
        response = self.client.post("/api/v1/oracle/propose", json={
            "query": "What should this teach?", "creativeAnswer": "A new candidate answer.",
            "locale": "en",
        })
        self.assertEqual(response.status_code, 201)
        proposal = response.json()
        self.assertEqual(proposal["status"], "proposed")
        self.assertEqual(proposal["candidate_content"]["origin"], "blackbox")
        self.assertEqual(proposal["candidate_content"]["lang"], "en")
        self.assertEqual(proposal["candidate_content"]["tags"], ["simplicity"])
        self.assertNotIn("id", proposal["candidate_content"])
        persisted = json.loads(next(Path(self.temp.name).glob("*.json")).read_text())
        self.assertEqual(persisted["status"], "proposed")
        self.assertNotEqual(persisted.get("status"), "active")
        self.assertNotIn("accepted_quote_id", persisted)

    def test_r2_envelope_normalization(self):
        payload = {"results": [{
            "id": "wis-001", "text": "x", "section": "wisdom", "tags": [],
            "origin": "human", "score": 0.8,
        }], "indexDigest": "abc", "indexedQuotes": 1, "ignored": True}
        self.assertEqual(set(normalize_retrieval_envelope(payload)), {"results", "indexDigest", "indexedQuotes"})

    def test_mcp_unavailable_fails_closed(self):
        import asyncio
        client = FastMCPRetrievalClient("http://127.0.0.1:1")
        with self.assertRaisesRegex(RuntimeError, "MCP semantic retrieval unavailable"):
            asyncio.run(client.semantic_retrieval("query", top_k=5, context_tag=None, section=None))


if __name__ == "__main__":
    unittest.main()

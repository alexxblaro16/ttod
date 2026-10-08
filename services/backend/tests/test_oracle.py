from __future__ import annotations

import asyncio
import json

from services.backend.app.oracle import (
    CREATIVE_PROMPT,
    FastMCPRetrievalClient,
    build_user_prompt,
    detect_language,
    normalize_retrieval_envelope,
    thematic_frame,
)
from services.backend.tests.support import BackendTestCase


class OracleIntegrationTests(BackendTestCase):
    def test_health_schema_and_public_projections(self):
        self.assertEqual(self.client.get("/health").status_code, 200)
        definitions = self.client.get("/api/v1/schema/definitions").json()
        self.assertIn("properties", definitions["quote"])
        wisdom = self.client.get("/api/v1/wisdom/sample").json()
        self.assertTrue(wisdom)
        self.assertTrue(all(quote["rights"]["license"] and "validation" not in quote for quote in wisdom))
        graph = self.client.get("/api/v1/graph").json()
        self.assertTrue(graph["nodes"])
        self.assertTrue(all(node["status"] == "active" for node in graph["nodes"]))

    def test_graph_response_is_byte_deterministic(self):
        first = self.client.get("/api/v1/graph").content
        second = self.client.get("/api/v1/graph").content
        self.assertEqual(first, second)

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

    def test_explicit_locale_overrides_language_heuristic(self):
        self.assertEqual(detect_language("The router hangs", "es"), "es")
        self.assertEqual(detect_language("¿Cómo simplifico?", "en"), "en")

    def test_thematic_frame_and_prompt_forbid_debugging(self):
        ranked = [{
            "id": "ops-001", "text": "x", "section": "ops", "tags": ["observability", "ops"],
            "origin": "human", "score": 0.4,
        }]
        frame = thematic_frame(ranked)
        self.assertEqual(frame, {"themes": ["ops"], "tags": ["observability", "ops"]})
        prompt = build_user_prompt(
            query="router hangs",
            session_history=[],
            ranked=ranked,
            frame=frame,
            grounded=False,
        )
        self.assertIn("below threshold", prompt)
        self.assertIn("MUST NOT", CREATIVE_PROMPT)

    def test_retrieval_envelope_discards_unknown_fields(self):
        payload = {"results": [{
            "id": "wis-001", "text": "x", "section": "wisdom", "tags": [],
            "origin": "human", "score": 0.8,
        }], "indexDigest": "abc", "indexedQuotes": 1, "ignored": True}
        self.assertEqual(
            set(normalize_retrieval_envelope(payload)),
            {"results", "indexDigest", "indexedQuotes"},
        )

    def test_mcp_retrieval_fails_closed_when_service_is_unavailable(self):
        client = FastMCPRetrievalClient("http://127.0.0.1:1")
        with self.assertRaisesRegex(RuntimeError, "MCP semantic retrieval unavailable"):
            asyncio.run(client.semantic_retrieval("query", top_k=5, context_tag=None, section=None))

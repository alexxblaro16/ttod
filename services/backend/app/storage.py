from __future__ import annotations

import hashlib
import json
import tempfile
import threading
from pathlib import Path
from typing import Any

from ttod_core.canonical import ExportPolicy
from ttod_core.exporter import Exporter
from ttod_core.repository import TTODRepository


PUBLIC_ACTIVE_POLICY = ExportPolicy(
    include_deprecated=False,
    include_erased=False,
    include_restricted=False,
    public_export=True,
)


def is_public_active(quote: dict[str, Any]) -> bool:
    rights = quote.get("rights")
    return (
        quote.get("status", "active") == "active"
        and isinstance(rights, dict)
        and rights.get("access") == "public"
        and isinstance(rights.get("license"), str)
        and bool(rights["license"].strip())
    )


class SnapshotService:
    """Read-only cached projections, invalidated by source mtime and digest."""

    def __init__(self, ttod_path: Path, schema_dir: Path):
        self.ttod_path = Path(ttod_path)
        self.schema_dir = Path(schema_dir)
        self.repository = TTODRepository(self.ttod_path, schema_dir=self.schema_dir)
        self.exporter = Exporter()
        self._lock = threading.RLock()
        self._cache_key: tuple[int, str] | None = None
        self._wisdom: list[dict[str, Any]] = []
        self._graph_bytes = b""

    def health(self) -> dict[str, Any]:
        root = self.repository.load()
        return {"status": "ok", "ttod_version": root.get("meta", {}).get("version")}

    def definitions(self) -> dict[str, Any]:
        names = {
            "quote": "quote.schema.json",
            "ttod": "ttod.schema.json",
            "proposal": "proposal.schema.json",
        }
        return {key: json.loads((self.schema_dir / filename).read_text(encoding="utf-8")) for key, filename in names.items()}

    def _source_key(self) -> tuple[int, str]:
        raw = self.repository.read_bytes()
        return (self.ttod_path.stat().st_mtime_ns, hashlib.sha256(raw).hexdigest())

    def _refresh(self) -> None:
        # La clave (mtime + sha256 de los bytes) cuesta ~1 ms; cargar y validar el YAML
        # de 450 KB, ~1 s. Solo se carga si el fichero cambió desde la última vez.
        key = self._source_key()
        with self._lock:
            if key == self._cache_key:
                return
            root = self.repository.load()
            public_root = {**root, "quotes": [q for q in root.get("quotes", []) if is_public_active(q)]}
            self._wisdom = [self._wisdom_projection(q) for q in public_root["quotes"]]
            with tempfile.TemporaryDirectory(prefix="ttod-backend-graph-") as directory:
                target = Path(directory) / "graph.json"
                self.exporter.export_graph(public_root, target, export_policy=PUBLIC_ACTIVE_POLICY)
                self._graph_bytes = target.read_bytes()
            self._cache_key = key

    @staticmethod
    def _wisdom_projection(quote: dict[str, Any]) -> dict[str, Any]:
        rights = quote["rights"]
        projected = {
            "id": quote["id"], "section": quote["section"], "level": quote["level"],
            "text": quote["text"], "teaches": quote.get("teaches", ""),
            "tags": quote.get("tags", []), "related": quote.get("related", []),
            "origin": quote["origin"], "lang": quote["lang"],
            "rights": {"license": rights["license"]},
        }
        if quote.get("subsection"):
            projected["subsection"] = quote["subsection"]
        if rights.get("holder"):
            projected["rights"]["holder"] = rights["holder"]
        return projected

    def wisdom(self) -> list[dict[str, Any]]:
        self._refresh()
        return self._wisdom

    def graph_bytes(self) -> bytes:
        self._refresh()
        return self._graph_bytes


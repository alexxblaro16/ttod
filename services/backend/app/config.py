from __future__ import annotations

import os
import secrets
from dataclasses import dataclass, field
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]


@dataclass(frozen=True)
class Settings:
    ttod_path: Path = REPOSITORY_ROOT / "ttod.yml"
    schema_dir: Path = REPOSITORY_ROOT / "schema"
    proposal_dir: Path = REPOSITORY_ROOT / "services/backend/data/proposals"
    session_secret: str = field(default_factory=lambda: secrets.token_urlsafe(32))
    session_ttl_seconds: int = 3600
    admin_email: str = "admin@ttod.local"
    admin_password_hash: str = ""
    ollama_mode: str = "host"
    ollama_model: str = ""
    ollama_embed_model: str = "nomic-embed-text"
    ollama_base_url: str = "http://host.containers.internal:11434"
    mcp_server_url: str = "http://mcp:3001"
    retrieval_threshold: float = 0.575
    retrieval_top_k: int = 5

    @classmethod
    def from_env(cls) -> "Settings":
        mode = os.getenv("OLLAMA_MODE", "host")
        if mode not in {"host", "container"}:
            raise ValueError("OLLAMA_MODE must be 'host' or 'container'")
        return cls(
            ttod_path=Path(os.getenv("TTOD_PATH", str(REPOSITORY_ROOT / "ttod.yml"))),
            schema_dir=Path(os.getenv("TTOD_SCHEMA_DIR", str(REPOSITORY_ROOT / "schema"))),
            proposal_dir=Path(os.getenv("TTOD_PROPOSAL_DIR", str(REPOSITORY_ROOT / "services/backend/data/proposals"))),
            session_secret=os.getenv("TTOD_SESSION_SECRET") or secrets.token_urlsafe(32),
            session_ttl_seconds=int(os.getenv("TTOD_SESSION_TTL_SECONDS", "3600")),
            admin_email=os.getenv("TTOD_ADMIN_EMAIL", "admin@ttod.local"),
            admin_password_hash=os.getenv("TTOD_ADMIN_PASSWORD_HASH", ""),
            ollama_mode=mode,
            ollama_model=os.getenv("OLLAMA_MODEL", ""),
            ollama_embed_model=os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text"),
            ollama_base_url=os.getenv("OLLAMA_BASE_URL", "http://host.containers.internal:11434").rstrip("/"),
            mcp_server_url=os.getenv("MCP_SERVER_URL", "http://mcp:3001").rstrip("/"),
            retrieval_threshold=float(os.getenv("ORACLE_RETRIEVAL_THRESHOLD", "0.575")),
            retrieval_top_k=int(os.getenv("ORACLE_RETRIEVAL_TOP_K", "5")),
        )

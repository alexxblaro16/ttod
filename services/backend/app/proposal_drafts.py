"""API proposal drafts — Redis indexes + dual-write to filesystem for CLI accept."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Protocol

import redis

from ttod_core.proposals import Proposal
from ttod_core.repository import ProposalStore, _proposal_from_dict

from .redis_client import create_redis_client


class ProposalDraftStore(Protocol):
    def save(self, proposal: Proposal) -> None: ...
    def list(self) -> list[Proposal]: ...


class FilesystemProposalDraftStore:
    """Filesystem-only (unit tests / empty REDIS_URL)."""

    def __init__(self, proposal_dir: Path):
        self._files = ProposalStore(proposal_dir)

    def save(self, proposal: Proposal) -> None:
        self._files.save(proposal)

    def list(self) -> list[Proposal]:
        return self._files.list()


class DualWriteProposalDraftStore:
    """Redis runtime queue + filesystem accept substrate (ttod_core stays redis-free)."""

    def __init__(self, proposal_dir: Path, redis_url: str = "", *, client: Any | None = None):
        self._files = ProposalStore(proposal_dir)
        self.client = create_redis_client(redis_url, client=client)

    @staticmethod
    def _key(proposal_id: str) -> str:
        return f"ttod:proposal:{proposal_id}"

    @staticmethod
    def _status_key(status: str) -> str:
        return f"ttod:proposals:status:{status}"

    @staticmethod
    def _user_key(user_id: str) -> str:
        return f"ttod:proposals:user:{user_id}"

    def save(self, proposal: Proposal) -> None:
        # Disk first: CLI accept substrate must exist even if Redis fails mid-write.
        self._files.save(proposal)
        payload = json.dumps(proposal.to_dict(), ensure_ascii=False)
        try:
            pipe = self.client.pipeline()
            pipe.set(self._key(proposal.proposal_id), payload)
            pipe.sadd(self._status_key(proposal.status.value), proposal.proposal_id)
            if proposal.proposer_id:
                pipe.sadd(self._user_key(proposal.proposer_id), proposal.proposal_id)
            pipe.execute()
        except redis.RedisError:
            # Filesystem write already succeeded; surface Redis failure to the caller.
            raise

    def list(self) -> list[Proposal]:
        try:
            ids = self.client.smembers(self._status_key("proposed"))
            # Include other non-terminal statuses the review queue may show.
            for status in ("needs_revision",):
                ids |= self.client.smembers(self._status_key(status))
        except redis.RedisError:
            raise
        if not ids:
            # Fallback if Redis was empty but files exist (partial dual-write recovery).
            return self._files.list()
        proposals: list[Proposal] = []
        for proposal_id in sorted(ids):
            raw = self.client.get(self._key(proposal_id))
            if raw:
                proposals.append(_proposal_from_dict(json.loads(raw)))
            else:
                try:
                    proposals.append(self._files.load(proposal_id))
                except Exception:
                    continue
        return proposals

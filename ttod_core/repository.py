"""
TTOD Atomic Repository (Q3)

Exclusive-lock write transactions for ttod.yml.

Binding sequence (no shortcuts):
  parse → in-memory candidate → validate (strict) → lock → re-read & rebase →
  allocate ID (accept only) → temp write → fsync → atomic rename →
  validate persisted bytes → release lock

On failure at any step the target file must remain byte-identical to its
pre-transaction state.
"""

from __future__ import annotations

import fcntl
import os
import tempfile
import uuid
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, Iterator, List, Optional, Set

import yaml

from ttod_core.canonical import Canonicalizer
from ttod_core.proposals import Proposal, ProposalStatus, create_proposal
from ttod_core.validation import DiagnosticCode, TTODValidator, ValidationResult


class RepositoryError(Exception):
    """Raised when a repository transaction fails."""


@dataclass
class TransactionHooks:
    """Test-only injection points; never set in production CLI paths."""

    fail_after_lock: bool = False
    fail_after_temp_write: bool = False
    fail_before_rename: bool = False
    fail_post_validate: bool = False


@dataclass
class DerivedMetadata:
    """Metadata recomputed from the canonical quote snapshot."""

    total_quotes: int
    last_id_by_section: Dict[str, int]
    origin_counts: Dict[str, int]
    section_counts: Dict[str, int]
    language_counts: Dict[str, int]
    languages: List[str]


@dataclass
class StatsDrift:
    """Single drift item between stored meta and recomputed values."""

    field: str
    stored: Any
    computed: Any


@dataclass
class StatsCheckResult:
    """Result of stats --check (read-only; never mutates meta)."""

    derived: DerivedMetadata
    drifts: List[StatsDrift] = field(default_factory=list)
    contract_blockers: List[str] = field(default_factory=list)

    @property
    def is_clean(self) -> bool:
        return not self.drifts and not self.contract_blockers


@dataclass
class AcceptResult:
    """Outcome of a successful accept transaction."""

    quote_id: str
    proposal_id: Optional[str] = None


class FileLock:
    """Process-wide exclusive lock via fcntl on a sibling .lock file."""

    def __init__(self, target: Path):
        self.lock_path = target.with_suffix(target.suffix + ".lock")
        self._fd: Optional[int] = None
        self._file = None

    def acquire(self) -> None:
        self.lock_path.parent.mkdir(parents=True, exist_ok=True)
        self._file = open(self.lock_path, "w")
        fcntl.flock(self._file.fileno(), fcntl.LOCK_EX)

    def release(self) -> None:
        if self._file is not None:
            fcntl.flock(self._file.fileno(), fcntl.LOCK_UN)
            self._file.close()
            self._file = None


def flatten_tag_taxonomy(tag_taxonomy: Dict[str, Any]) -> Set[str]:
    """Collect all declared tag strings from the taxonomy tree."""
    declared: Set[str] = set()
    for _category, tags in tag_taxonomy.items():
        if isinstance(tags, list):
            declared.update(tags)
        elif isinstance(tags, dict):
            declared.update(tags.keys())
    return declared


def compute_last_id_by_prefix(quotes: List[Dict[str, Any]]) -> Dict[str, int]:
    """
    Recompute meta.last_id_by_section keyed by section *prefix* (live file convention).

    Example: arch-059 → last_id_by_section['arch'] = 59
    """
    max_by_prefix: Dict[str, int] = {}
    for quote in quotes:
        quote_id = quote.get("id", "")
        if "-" not in quote_id:
            continue
        prefix, num_str = quote_id.split("-", 1)
        try:
            number = int(num_str)
        except ValueError:
            continue
        max_by_prefix[prefix] = max(max_by_prefix.get(prefix, 0), number)
    return max_by_prefix


def compute_derived_metadata(root: Dict[str, Any]) -> DerivedMetadata:
    """Recompute all derived meta fields from quotes (never hand-patch)."""
    quotes = root.get("quotes", [])
    language_counts = _count_field(quotes, "lang")
    return DerivedMetadata(
        total_quotes=len(quotes),
        last_id_by_section=compute_last_id_by_prefix(quotes),
        origin_counts=_count_field(quotes, "origin"),
        section_counts=_count_field(quotes, "section"),
        language_counts=language_counts,
        languages=sorted(language_counts.keys()),
    )


def _count_field(quotes: List[Dict[str, Any]], field_name: str) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for quote in quotes:
        value = quote.get(field_name)
        if value is None:
            continue
        counts[value] = counts.get(value, 0) + 1
    return counts


class TTODRepository:
    """Atomic read/write access to a TTOD YAML file."""

    SCHEMA_VERSION = "3.1.0"

    def __init__(
        self,
        path: Path,
        schema_dir: Optional[Path] = None,
        hooks: Optional[TransactionHooks] = None,
    ):
        self.path = Path(path)
        self.hooks = hooks or TransactionHooks()
        self.canonicalizer = Canonicalizer()
        self._schema_dir = schema_dir

    def _validator(self, strict: bool) -> TTODValidator:
        return TTODValidator(schema_dir=self._schema_dir, strict=strict)

    def read_bytes(self) -> bytes:
        if not self.path.exists():
            raise RepositoryError(f"TTOD file not found: {self.path}")
        return self.path.read_bytes()

    def load(self) -> Dict[str, Any]:
        return yaml.safe_load(self.read_bytes().decode("utf-8"))

    def validate(self, strict: bool = False) -> ValidationResult:
        root = self.load()
        return self._validator(strict).validate_root(root)

    def stats_check(self) -> StatsCheckResult:
        """Recompute derived metadata and report drift (read-only)."""
        root = self.load()
        derived = compute_derived_metadata(root)
        meta = root.get("meta", {})
        drifts: List[StatsDrift] = []
        blockers: List[str] = []

        stored_total = meta.get("total_quotes")
        if stored_total is not None and stored_total != derived.total_quotes:
            drifts.append(StatsDrift("meta.total_quotes", stored_total, derived.total_quotes))

        stored_languages = meta.get("languages")
        if stored_languages is not None and list(stored_languages) != derived.languages:
            drifts.append(StatsDrift("meta.languages", stored_languages, derived.languages))

        stored_last = meta.get("last_id_by_section", {})
        if not isinstance(stored_last, dict):
            blockers.append("meta.last_id_by_section is missing or not an object — cannot compare")
        else:
            all_prefixes = set(stored_last.keys()) | set(derived.last_id_by_section.keys())
            for prefix in sorted(all_prefixes):
                stored_val = stored_last.get(prefix, 0)
                computed_val = derived.last_id_by_section.get(prefix, 0)
                if stored_val != computed_val:
                    drifts.append(
                        StatsDrift(
                            f"meta.last_id_by_section.{prefix}",
                            stored_val,
                            computed_val,
                        )
                    )

        sections = root.get("sections", [])
        if not sections:
            blockers.append("sections list missing — prefix/section mapping unavailable for audit")

        return StatsCheckResult(derived=derived, drifts=drifts, contract_blockers=blockers)

    def validate_candidate_content(
        self,
        candidate: Dict[str, Any],
        *,
        reject_unknown_tags: bool = True,
    ) -> None:
        """Pre-lock validation of proposal candidate_content (no canonical id yet)."""
        if "id" in candidate:
            raise RepositoryError("candidate_content must not contain a canonical 'id' field")

        required = ("text", "section", "level", "origin", "lang")
        for field_name in required:
            if field_name not in candidate:
                raise RepositoryError(f"candidate missing required field '{field_name}'")

        root = self.load()
        section_ids = {s["id"] for s in root.get("sections", [])}
        if candidate["section"] not in section_ids:
            raise RepositoryError(f"unknown section '{candidate['section']}'")

        if reject_unknown_tags:
            tags = candidate.get("tags") or []
            declared = flatten_tag_taxonomy(root.get("tag_taxonomy", {}))
            unknown = [t for t in tags if t not in declared]
            if unknown:
                raise RepositoryError(
                    f"unknown tags {unknown} — taxonomy extension is a separate reviewed operation"
                )

        origin = candidate["origin"]
        if origin == "blackbox":
            validation = candidate.get("validation") or {}
            if not validation.get("reviewer_id"):
                raise RepositoryError("blackbox origin requires validation.reviewer_id before accept")

    def accept_proposal(
        self,
        proposal: Proposal,
        reviewer_id: str,
        *,
        reject_unknown_tags: bool = True,
    ) -> AcceptResult:
        """
        Accept a proposal into ttod.yml via the full write transaction.

        The proposal object is mutated in memory (status → accepted) but ttod.yml
        is only touched inside _run_transaction.
        """
        if proposal.status == ProposalStatus.ACCEPTED and proposal.accepted_quote_id not in (
            None,
            "PENDING_ATOMIC_ALLOCATION",
        ):
            raise RepositoryError(
                f"proposal {proposal.proposal_id} already accepted as {proposal.accepted_quote_id}"
            )

        # blackbox/mixed-origin candidates must carry a full validation block
        # (schema/quote.schema.json's own conditional: reviewer_id + activity_id
        # required, status constrained to "validated" when present) before
        # validate_candidate_content() and the strict pre-write validator below
        # will admit them. The CLI/API caller already supplies a human
        # reviewer_id as this method's own argument (required, never optional)
        # — thread it in here, along with a freshly generated activity_id
        # representing *this* acceptance event, rather than requiring a
        # separate hand-edit of the proposal JSON. Nothing else in the object
        # model currently tracks an activity_id (ReviewActivity has none), so
        # this is the one place that identifier can honestly originate.
        # Never overwrite an already-present field: if an earlier step already
        # recorded its own reviewer_id/activity_id/status, that attribution is
        # preserved, not silently replaced by this acceptance call's own values.
        if proposal.candidate_content.get("origin") in ("blackbox", "mixed"):
            validation = proposal.candidate_content.setdefault("validation", {})
            validation.setdefault("reviewer_id", reviewer_id)
            validation.setdefault("activity_id", f"accept-{uuid.uuid4()}")
            validation.setdefault("status", "validated")
            validation.setdefault(
                "reviewed_at", datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
            )

        self.validate_candidate_content(
            proposal.candidate_content,
            reject_unknown_tags=reject_unknown_tags,
        )

        allocated_id: Dict[str, str] = {}

        def mutate(root: Dict[str, Any]) -> None:
            quote = self._build_quote_from_candidate(root, proposal.candidate_content)
            self._apply_proposal_provenance(quote, proposal)
            allocated_id["id"] = quote["id"]
            root.setdefault("quotes", []).append(quote)
            self._apply_derived_metadata(root)

        self._run_transaction(mutate, operation="accept")
        quote_id = allocated_id["id"]
        proposal.accept(reviewer_id)
        proposal.accepted_quote_id = quote_id
        return AcceptResult(quote_id=quote_id, proposal_id=proposal.proposal_id)

    def accept_quote_direct(
        self,
        candidate_content: Dict[str, Any],
        reviewer_id: str,
        *,
        reject_unknown_tags: bool = True,
    ) -> AcceptResult:
        """Convenience wrapper: create proposal, accept in one transaction."""
        proposal = create_proposal(
            candidate_content=candidate_content,
            proposer_kind="human",
            proposer_id=reviewer_id,
            generation_method="cli-add",
        )
        return self.accept_proposal(
            proposal,
            reviewer_id,
            reject_unknown_tags=reject_unknown_tags,
        )

    def deprecate_quote(self, quote_id: str, *, deprecated_by: Optional[str] = None) -> None:
        """Mark a quote deprecated (never deletes)."""

        def mutate(root: Dict[str, Any]) -> None:
            quote = self._find_quote(root, quote_id)
            quote["status"] = "deprecated"
            if deprecated_by:
                quote["deprecated_by"] = deprecated_by
            quote["content_digest"] = self.canonicalizer.compute_content_digest(quote)

        self._run_transaction(mutate, operation="deprecate")

    def erase_quote(
        self,
        quote_id: str,
        *,
        authority: str,
        decision_ref: str,
        reason: Optional[str] = None,
    ) -> None:
        """Higher-law erasure tombstone — requires explicit authority and decision reference."""
        if not authority.strip():
            raise RepositoryError("erase requires non-empty --authority")
        if not decision_ref.strip():
            raise RepositoryError("erase requires non-empty --decision-ref")

        def mutate(root: Dict[str, Any]) -> None:
            quote = self._find_quote(root, quote_id)
            quote["status"] = "erased"
            quote["text"] = "[REDACTED - legally erased under higher-law authority]"
            quote["reason"] = reason or f"Erasure under {authority} per {decision_ref}"
            quote["effective_at"] = date.today().isoformat()
            quote["erasure_authority"] = authority
            quote["erasure_decision_ref"] = decision_ref
            quote["content_digest"] = self.canonicalizer.compute_content_digest(quote)

        self._run_transaction(mutate, operation="erase")

    def apply_v3_migration(self):
        """
        Replace ttod.yml with a v3-migrated candidate via atomic bytes write.

        Phase Q6 only — preserves the header comment banner and rolls back on failure.
        """
        from ttod_core.migration import migrate_root, serialize_migrated_document

        original_bytes = self.read_bytes()
        original_text = original_bytes.decode("utf-8")
        root = yaml.safe_load(original_text)
        if root is None:
            raise RepositoryError("empty ttod.yml — cannot migrate")

        migrated, summary = migrate_root(root)
        content = serialize_migrated_document(migrated, original_text).encode("utf-8")

        pre_result = self._validator(strict=True).validate_root(migrated)
        if not pre_result.is_valid:
            codes = [e.code.value for e in pre_result.errors[:5]]
            raise RepositoryError(f"pre-migration strict validation failed: {codes}")

        lock = FileLock(self.path)
        try:
            lock.acquire()
            if self.hooks.fail_after_lock:
                raise RepositoryError("injected failure after lock (migrate-v3)")

            self._write_bytes_atomic(content, original_bytes)

            if self.hooks.fail_post_validate:
                raise RepositoryError("injected failure after successful migration write")

        except RepositoryError:
            self._ensure_bytes_unchanged(original_bytes)
            raise
        except Exception as exc:
            self._ensure_bytes_unchanged(original_bytes)
            raise RepositoryError(f"migration transaction failed: {exc}") from exc
        finally:
            lock.release()

        return summary

    def _build_quote_from_candidate(
        self,
        root: Dict[str, Any],
        candidate: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Build a full quote record with allocated ID and digest (call under lock only)."""
        section = candidate["section"]
        prefix = self._section_prefix(root, section)
        new_id = self._allocate_canonical_id(root, prefix)

        quote: Dict[str, Any] = {
            "id": new_id,
            "schema_version": self.SCHEMA_VERSION,
            "text": candidate["text"],
            "section": section,
            "level": candidate["level"],
            "lang": candidate["lang"],
            "origin": candidate["origin"],
        }

        for optional in (
            "subsection",
            "tags",
            "teaches",
            "show_when",
            "related",
            "relation_edges",
            "lesson",
            "source",
            "validation",
            "rights",
            "created_at",
            "authorship_assertion",
        ):
            if optional in candidate:
                quote[optional] = candidate[optional]

        if "created_at" not in quote:
            quote["created_at"] = date.today().isoformat()

        quote["content_digest"] = self.canonicalizer.compute_content_digest(quote)
        return quote

    def _apply_proposal_provenance(self, quote: Dict[str, Any], proposal: Proposal) -> None:
        """Copy bridge-level provenance from proposal onto the accepted quote."""
        if proposal.proposal_id:
            quote["proposal_id"] = proposal.proposal_id
        if proposal.wpl_record_id:
            quote["wpl_record_id"] = proposal.wpl_record_id
        if proposal.wpl_record_digest:
            quote["wpl_record_digest"] = proposal.wpl_record_digest
        if proposal.evidence_snapshot_digest:
            quote["evidence_snapshot_digest"] = proposal.evidence_snapshot_digest
        quote["content_digest"] = self.canonicalizer.compute_content_digest(quote)

    def _allocate_canonical_id(self, root: Dict[str, Any], prefix: str) -> str:
        """Allocate next canonical ID under lock after re-read."""
        max_num = 0
        for quote in root.get("quotes", []):
            quote_id = quote.get("id", "")
            if quote_id.startswith(prefix + "-"):
                try:
                    max_num = max(max_num, int(quote_id.split("-", 1)[1]))
                except ValueError:
                    continue

        meta_last = root.get("meta", {}).get("last_id_by_section", {})
        if isinstance(meta_last, dict):
            max_num = max(max_num, meta_last.get(prefix, 0))

        new_num = max_num + 1
        return f"{prefix}-{new_num:03d}"

    def _apply_derived_metadata(self, root: Dict[str, Any]) -> None:
        """Recompute and apply all derived meta fields atomically with the quote mutation."""
        derived = compute_derived_metadata(root)
        meta = root.setdefault("meta", {})
        meta["total_quotes"] = derived.total_quotes
        meta["last_id_by_section"] = dict(sorted(derived.last_id_by_section.items()))
        meta["languages"] = list(derived.languages)
        if derived.languages:
            # Deprecated mirror for unmigrated tooling (S0 decision 7).
            meta["language"] = derived.languages[0]

    def _find_quote(self, root: Dict[str, Any], quote_id: str) -> Dict[str, Any]:
        for quote in root.get("quotes", []):
            if quote.get("id") == quote_id:
                return quote
        raise RepositoryError(f"quote not found: {quote_id}")

    def _section_prefix(self, root: Dict[str, Any], section_id: str) -> str:
        for section in root.get("sections", []):
            if section.get("id") == section_id:
                return section["prefix"]
        raise RepositoryError(f"section not found: {section_id}")

    def _run_transaction(
        self,
        mutate: Callable[[Dict[str, Any]], None],
        *,
        operation: str,
    ) -> None:
        """Execute the binding write-transaction sequence."""
        if not self.path.exists():
            raise RepositoryError(f"TTOD file not found: {self.path}")

        original_bytes = self.read_bytes()
        lock = FileLock(self.path)

        try:
            lock.acquire()
            if self.hooks.fail_after_lock:
                raise RepositoryError(f"injected failure after lock ({operation})")

            current_bytes = self.read_bytes()
            root = yaml.safe_load(current_bytes.decode("utf-8"))
            if root is None:
                root = {}

            mutate(root)

            pre_result = self._validator(strict=True).validate_root(root)
            if not pre_result.is_valid:
                codes = [e.code.value for e in pre_result.errors[:5]]
                raise RepositoryError(
                    f"pre-write strict validation failed ({operation}): {codes}"
                )

            self._write_yaml_atomic(root, original_bytes)

            if self.hooks.fail_post_validate:
                raise RepositoryError(f"injected failure after successful write ({operation})")

        except RepositoryError:
            self._ensure_bytes_unchanged(original_bytes)
            raise
        except Exception as exc:
            self._ensure_bytes_unchanged(original_bytes)
            raise RepositoryError(f"transaction failed ({operation}): {exc}") from exc
        finally:
            lock.release()

    def _write_yaml_atomic(self, root: Dict[str, Any], original_bytes: bytes) -> None:
        """Temp write → fsync → rename → validate disk bytes."""
        serialized = yaml.dump(
            root,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
        )
        self._write_bytes_atomic(serialized.encode("utf-8"), original_bytes)

    def _write_bytes_atomic(self, content: bytes, original_bytes: bytes) -> None:
        """Temp write → fsync → rename → validate disk bytes."""
        tmp_path = self.path.with_suffix(self.path.suffix + ".tmp")

        try:
            with open(tmp_path, "wb") as handle:
                handle.write(content)
                handle.flush()
                os.fsync(handle.fileno())

            if self.hooks.fail_after_temp_write:
                raise RepositoryError("injected failure after temp write")

            if self.hooks.fail_before_rename:
                raise RepositoryError("injected failure before rename")

            os.replace(tmp_path, self.path)

            disk_root = yaml.safe_load(self.path.read_bytes().decode("utf-8"))
            post_result = self._validator(strict=True).validate_root(disk_root)
            if not post_result.is_valid:
                self._restore_bytes(original_bytes)
                codes = [e.code.value for e in post_result.errors[:5]]
                raise RepositoryError(f"post-write disk validation failed: {codes}")

        finally:
            if tmp_path.exists():
                tmp_path.unlink(missing_ok=True)

    def _restore_bytes(self, original_bytes: bytes) -> None:
        """Atomically restore pre-transaction bytes."""
        tmp = self.path.with_suffix(self.path.suffix + ".restore")
        with open(tmp, "wb") as handle:
            handle.write(original_bytes)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, self.path)

    def _ensure_bytes_unchanged(self, original_bytes: bytes) -> None:
        """If the file was modified, restore original bytes."""
        try:
            current = self.read_bytes()
        except RepositoryError:
            return
        if current != original_bytes:
            self._restore_bytes(original_bytes)


class ProposalStore:
    """Filesystem store for proposal JSON records (never writes ttod.yml)."""

    def __init__(self, directory: Path):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)

    def save(self, proposal: Proposal) -> Path:
        path = self.directory / f"{proposal.proposal_id}.json"
        import json

        path.write_text(
            json.dumps(proposal.to_dict(), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        return path

    def load(self, proposal_id: str) -> Proposal:
        import json

        path = self.directory / f"{proposal_id}.json"
        if not path.exists():
            raise RepositoryError(f"proposal not found: {proposal_id}")
        data = json.loads(path.read_text(encoding="utf-8"))
        return _proposal_from_dict(data)

    def list(self) -> list[Proposal]:
        return [self.load(path.stem) for path in sorted(self.directory.glob("*.json"))]

    def load_path(self, path: Path) -> Proposal:
        import json

        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return _proposal_from_dict(data)


def _proposal_from_dict(data: Dict[str, Any]) -> Proposal:
    from ttod_core.proposals import ReviewActivity, ReviewActivityType

    activities = []
    for raw in data.get("human_review_activities", []):
        activities.append(
            ReviewActivity(
                activity_type=ReviewActivityType(raw["activity_type"]),
                reviewer_id=raw["reviewer_id"],
                timestamp=raw["timestamp"],
                comment=raw.get("comment"),
                decision_reason=raw.get("decision_reason"),
            )
        )

    proposal = Proposal(
        proposal_id=data["proposal_id"],
        status=ProposalStatus(data["status"]),
        candidate_content=data.get("candidate_content", {}),
        proposer_kind=data.get("proposer_kind", ""),
        proposer_id=data.get("proposer_id", ""),
        generation_method=data.get("generation_method", ""),
        wpl_record_id=data.get("wpl_record_id"),
        wpl_record_digest=data.get("wpl_record_digest"),
        evidence_snapshot_id=data.get("evidence_snapshot_id"),
        evidence_snapshot_digest=data.get("evidence_snapshot_digest"),
        human_review_activities=activities,
        accepted_quote_id=data.get("accepted_quote_id"),
        created_at=data.get("created_at", ""),
    )
    return proposal

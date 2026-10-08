"""Enforce the one-axis `agentic/` tree: every child is a topic pack (Phase Y5).

The rules live in docs/DEV_PLAN/DECISIONS/Y5-2026-09-21-ONE-AXIS-TREE.md. The checks are one pure
function, `check_tree(root)`, so the same code runs on the real tree (must be clean) and on
deliberately broken copies (each must be caught) — the negative controls are a permanent test.

Skipped when `agentic/` is absent: the TS5 skeleton generator copies `tests/` but never `agentic/`.
Local only: `.github/workflows/ci.yml` runs no Python tests, so `make test` is the only enforcer.
"""

from __future__ import annotations

import json
import re
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_KEYS = (
    "name",
    "purpose",
    "surfaces",
    "landings",
    "mirrors",
    "locks",
    "external_readers",
    "status",
)
KIND_NAMES = {"rules", "skills", "agents", "scripts"}
SINGULAR_KINDS = {"rule", "skill", "agent", "script"}
IGNORED = {"__pycache__", ".DS_Store"}
PACK_FILES = {"PACK.md", "README.md"}
CANONICAL = re.compile(r"Canonical:\s*`([^`]+)`")
LANDING_MAX_LINES = 25  # a doorway is a few lines of redirect, never a second copy


def parse_front_matter(text: str) -> dict[str, object]:
    """Tiny parser: `---` fence, `key: value`, inline `[a, b]` lists, `[]` empty, no comments."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("PACK.md does not start with a --- front-matter fence")
    out: dict[str, object] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return out
        key, sep, value = line.partition(":")
        if not sep:
            raise ValueError(f"front-matter line without a colon: {line!r}")
        value = value.strip()
        if value.startswith("[") and value.endswith("]"):
            out[key.strip()] = [item.strip() for item in value[1:-1].split(",") if item.strip()]
        else:
            out[key.strip()] = value
    raise ValueError("front matter is never closed")


def _nonempty(path: Path) -> bool:
    if path.is_dir():
        return any(child.name not in IGNORED for child in path.iterdir())
    return path.is_file() and path.stat().st_size > 0


def check_tree(root: Path) -> list[str]:
    """Return every violation of the one-axis invariant under `root` (empty list = clean)."""
    agentic = root / "agentic"
    errors: list[str] = []
    meta: dict[str, dict[str, object]] = {}

    # 1-2. Every direct child is a pack; no kind folder, stray file, symlink or hidden dir beside one.
    for child in sorted(agentic.iterdir()):
        if child.name in IGNORED:
            continue
        if child.is_symlink():
            errors.append(f"{child.name}: symlinks are not allowed in agentic/")
        elif child.is_file():
            if child.name != "README.md":
                errors.append(f"{child.name}: stray file in agentic/ (only README.md is allowed)")
        elif child.name in KIND_NAMES:
            errors.append(f"{child.name}: a kind folder at top level (exists only inside a pack)")
        elif not (child / "PACK.md").is_file():
            errors.append(f"{child.name}: no PACK.md")
        else:
            try:
                fm = parse_front_matter((child / "PACK.md").read_text(encoding="utf-8"))
            except ValueError as exc:
                errors.append(f"{child.name}: {exc}")
                continue
            missing = sorted(set(REQUIRED_KEYS) - set(fm))
            if missing:
                errors.append(f"{child.name}: missing front-matter keys {missing}")
                continue
            if fm["name"] != child.name:
                errors.append(f"{child.name}: name is {fm['name']!r}")
            if not fm["purpose"]:
                errors.append(f"{child.name}: purpose is empty")
            if fm["status"] not in ("tracked", "local-untracked"):
                errors.append(f"{child.name}: status is {fm['status']!r}")
            meta[child.name] = fm

    for name, fm in meta.items():
        pack = agentic / name
        # 6. Surfaces: non-empty, simple relative names, each resolving to something non-empty in the pack.
        surfaces = list(fm["surfaces"])  # type: ignore[arg-type]
        if not surfaces:
            errors.append(f"{name}: surfaces is empty")
        for item in surfaces:
            if item.startswith(("/", ".")) or ".." in item or "/" in item:
                errors.append(f"{name}: surface {item!r} must be a plain name inside the pack")
            elif not _nonempty(pack / item):
                errors.append(f"{name}: surface {item!r} is missing or empty")
        # Every child of a pack is PACK.md, README.md, or a declared surface; kind names are plural.
        for child in sorted(pack.iterdir()):
            if child.name in IGNORED or child.name in PACK_FILES:
                continue
            if child.name in SINGULAR_KINDS:
                errors.append(f"{name}/{child.name}: singular kind folder (use the plural)")
            elif child.name not in surfaces:
                errors.append(f"{name}/{child.name}: not declared in surfaces")
        # 3. Landings: exist, start with front matter, stay short, carry a Canonical marker into a declared surface.
        for landing in fm["landings"]:  # type: ignore[union-attr]
            path = root / landing
            if not path.is_file():
                errors.append(f"{name}: landing missing: {landing}")
                continue
            text = path.read_text(encoding="utf-8")
            if not text.startswith("---"):
                errors.append(f"{landing}: landing has no front matter")
            if len(text.splitlines()) > LANDING_MAX_LINES:
                errors.append(f"{landing}: over {LANDING_MAX_LINES} lines — a landing is a redirect, not a copy")
            targets = CANONICAL.findall(text)
            if not targets:
                errors.append(f"{landing}: no `Canonical: `path`` marker")
            for target in targets:
                resolved = root / target
                parts = Path(target).parts
                if not resolved.is_file():
                    errors.append(f"{landing}: canonical target missing: {target}")
                elif parts[:2] != ("agentic", name) or len(parts) < 4 or parts[2] not in surfaces:
                    errors.append(f"{landing}: {target} is not inside a declared surface of agentic/{name}/")
        # 4. Mirrors: src>dst, both exist, parsed JSON equal.
        for pair in fm["mirrors"]:  # type: ignore[union-attr]
            src, sep, dst = pair.partition(">")
            a, b = pack / src, root / dst
            if not sep or not (a.is_file() and b.is_file()):
                errors.append(f"{name}: mirror {pair!r} malformed or a file is missing")
                continue
            try:
                if json.loads(a.read_text()) != json.loads(b.read_text()):
                    errors.append(f"{name}: mirror {pair!r} differs")
            except ValueError:
                errors.append(f"{name}: mirror {pair!r} is not valid JSON")
        # 5. Locks: exist, and one line carries both `agentic` and the pack name (a bare mention does not count).
        for lock in fm["locks"]:  # type: ignore[union-attr]
            path = root / lock
            if not path.is_file():
                errors.append(f"{name}: lock file missing: {lock}")
            elif not any(
                "agentic" in line and name in line for line in path.read_text(encoding="utf-8").splitlines()
            ):
                errors.append(f"{name}: {lock} no longer names agentic/{name} on any line")

    # Orphans: a doorway or mirror in .cursor/.claude that no pack declares.
    declared_landings = {landing for fm in meta.values() for landing in fm["landings"]}  # type: ignore[union-attr]
    declared_mirror_dsts = {p.partition(">")[2] for fm in meta.values() for p in fm["mirrors"]}  # type: ignore[union-attr]
    for tool in (".cursor", ".claude"):
        base = root / tool
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*")):
            rel = path.relative_to(root).as_posix()
            if path.suffix in (".md", ".mdc") and path.is_file():
                for target in CANONICAL.findall(path.read_text(encoding="utf-8")):
                    if target.startswith("agentic/") and rel not in declared_landings:
                        errors.append(f"{rel}: points into agentic/ but no pack declares it as a landing")
            elif path.suffix == ".json" and path.is_file() and rel not in declared_mirror_dsts:
                errors.append(f"{rel}: JSON copy that no pack declares under mirrors")
    return errors


def _copy_fixture(dst: Path) -> Path:
    """A minimal copy of everything check_tree reads, so mutations never touch the real repo."""
    for name in ("agentic", ".cursor", ".claude", ".github", "Makefile"):
        src = ROOT / name
        if src.is_dir():
            shutil.copytree(src, dst / name, ignore=shutil.ignore_patterns("__pycache__"))
        elif src.is_file():
            shutil.copy2(src, dst / name)
    (dst / "tests").mkdir()
    shutil.copy2(ROOT / "tests" / "test_public_privacy_watcher.py", dst / "tests")
    return dst


@unittest.skipUnless((ROOT / "agentic").is_dir(), "no agentic/ (skeleton)")
class AgenticTreeTests(unittest.TestCase):
    def test_real_tree_is_clean(self) -> None:
        self.assertEqual(check_tree(ROOT), [])


@unittest.skipUnless((ROOT / "agentic").is_dir(), "no agentic/ (skeleton)")
class AgenticTreeNegativeControls(unittest.TestCase):
    """Each mutation breaks the one-axis contract and must be caught. Written after a cold review
    found fifteen ways to break the tree that an earlier version of this test let through."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = _copy_fixture(Path(self._tmp.name))
        self.assertEqual(check_tree(self.root), [], "fixture must start clean")

    def caught(self, mutate) -> list[str]:
        mutate(self.root)
        return check_tree(self.root)

    def _edit(self, rel: str, old: str, new: str) -> None:
        path = self.root / rel
        text = path.read_text(encoding="utf-8")
        self.assertIn(old, text)
        path.write_text(text.replace(old, new, 1), encoding="utf-8")

    def test_top_level_kind_folder(self) -> None:
        self.assertTrue(self.caught(lambda r: (r / "agentic/rules").mkdir()))

    def test_hidden_and_dunder_dirs_are_not_exempt(self) -> None:
        self.assertTrue(self.caught(lambda r: (r / "agentic/.rules").mkdir()))
        self.assertTrue(self.caught(lambda r: (r / "agentic/__skills").mkdir()))

    def test_stray_file_and_symlink(self) -> None:
        self.assertTrue(self.caught(lambda r: (r / "agentic/notes.txt").write_text("x")))
        self.assertTrue(self.caught(lambda r: (r / "agentic/skills").symlink_to("/nonexistent")))

    def test_singular_kind_folder_inside_a_pack(self) -> None:
        self.assertTrue(self.caught(lambda r: (r / "agentic/report-steward/agent").mkdir()))

    def test_unlisted_surface(self) -> None:
        self.assertTrue(self.caught(lambda r: (r / "agentic/ttod-editing/skills/x").mkdir(parents=True)))

    def test_surface_empty_or_escaping(self) -> None:
        def empty(r: Path) -> None:
            (r / "agentic/ttod-editing/emptydir").mkdir()
            self._edit("agentic/ttod-editing/PACK.md", "surfaces: [rules]", "surfaces: [emptydir]")

        self.assertTrue(self.caught(empty))

    def test_surface_dotdot(self) -> None:
        self.assertTrue(
            self.caught(lambda r: self._edit("agentic/ttod-editing/PACK.md", "surfaces: [rules]", "surfaces: [..]"))
        )

    def test_landing_stripped_of_front_matter(self) -> None:
        self.assertTrue(
            self.caught(
                lambda r: (r / ".cursor/rules/ttod-editing.mdc").write_text(
                    "Canonical: `agentic/ttod-editing/rules/ttod-editing.md`\n"
                )
            )
        )

    def test_landing_that_is_a_full_copy(self) -> None:
        def bloat(r: Path) -> None:
            path = r / ".cursor/rules/ttod-editing.mdc"
            path.write_text(path.read_text() + "\n".join(f"copied line {i}" for i in range(40)))

        self.assertTrue(self.caught(bloat))

    def test_canonical_points_at_pack_md_not_a_surface(self) -> None:
        self.assertTrue(
            self.caught(
                lambda r: self._edit(
                    ".cursor/rules/ttod-editing.mdc",
                    "agentic/ttod-editing/rules/ttod-editing.md",
                    "agentic/ttod-editing/PACK.md",
                )
            )
        )

    def test_stale_canonical_target(self) -> None:
        self.assertTrue(
            self.caught(
                lambda r: self._edit(
                    ".cursor/rules/ttod-editing.mdc",
                    "agentic/ttod-editing/rules/",
                    "agentic/rules/",
                )
            )
        )

    def test_orphan_landing(self) -> None:
        self.assertTrue(
            self.caught(
                lambda r: self._edit(
                    "agentic/ttod-editing/PACK.md",
                    "landings: [.cursor/rules/ttod-editing.mdc]",
                    "landings: []",
                )
            )
        )

    def test_orphan_mirror(self) -> None:
        self.assertTrue(
            self.caught(
                lambda r: self._edit(
                    "agentic/ide-mcp/PACK.md", "mirrors: [mcp.cursor.json>.cursor/mcp.json]", "mirrors: []"
                )
            )
        )

    def test_mirror_drift(self) -> None:
        self.assertTrue(self.caught(lambda r: (r / ".cursor/mcp.json").write_text("{}")))

    def test_lock_that_no_longer_names_the_pack(self) -> None:
        self.assertTrue(
            self.caught(
                lambda r: self._edit(
                    "Makefile", "agentic/report-steward/scripts", "agentic/renamed/scripts"
                )
            )
        )

    def test_pack_md_defects(self) -> None:
        self.assertTrue(
            self.caught(lambda r: self._edit("agentic/ttod-editing/PACK.md", "name: ttod-editing", "name: other"))
        )
        self.assertTrue(
            self.caught(lambda r: (r / "agentic/ttod-editing/PACK.md").write_text("# no front matter\n"))
        )


if __name__ == "__main__":
    unittest.main()

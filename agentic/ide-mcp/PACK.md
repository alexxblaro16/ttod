---
name: ide-mcp
purpose: Student IDE MCP client configuration (official servers only), its vendored llms index and offline/live verify scripts.
surfaces: [mcp.cursor.json, examples, llms, scripts]
landings: []
mirrors: [mcp.cursor.json>.cursor/mcp.json]
locks: []
external_readers: []
status: tracked
---

# Student IDE MCP Pack

Project-level MCP client configuration for the coding agent inside a collaborator's editor —
official, vendor-maintained servers only. Student-facing setup lives in [`README.md`](README.md).

| Surface | Purpose |
| --- | --- |
| `mcp.cursor.json` | edit-home for the committed server list |
| `../../.cursor/mcp.json` | landing Cursor actually reads — an **identical copy**, not a redirect (JSON cannot forward); `verify-ide-mcp.py` enforces semantic equality (parsed JSON, so whitespace or key order alone would not trip it) |
| `examples/github.json` | opt-in-only GitHub server block (credentialed, never in the default) |
| `llms/` | vendored, digest-checked offline docs index |
| `scripts/verify-ide-mcp.py` | offline config + official-servers allowlist gate (CI-safe) |
| `scripts/simulate-student-check.py` | live MCP `initialize` handshake against every committed server |

The pack is source material for one governed method: **a server ships by default only if it is
official, and the claim is checked, not assumed.** Keep the files together so the allowlist, the
config, and the two checks evolve as one.

Not part of this pack: the product's own MCP server (`services/mcp/`) — a runtime protocol, not
an IDE tool. Same initials, unrelated process.

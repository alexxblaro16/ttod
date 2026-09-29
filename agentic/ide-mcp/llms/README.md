# `llms/` — vendored agent-readable docs indexes

Vendored copies of framework-published `llms.txt`-style indexes, so agents have an
offline, digest-verified fallback even when the MCP server for that framework is
unreachable (network policy, campus firewall, first-`npx`-fetch failure).

| File | Source | What it is |
| --- | --- | --- |
| `svelte-prompts-llms.txt` | <https://svelte.dev/docs/ai/prompts/llms.txt> | Svelte's own list of MCP prompts and when to use each |

## When to use the file vs the MCP `get-documentation` tool

- **Prefer the MCP tool call** (`svelte` server's `get-documentation`, or equivalent)
  when the IDE MCP connection is live — it returns current, framework-served content,
  not a point-in-time vendor snapshot.
- **Fall back to this file** only when the MCP server is unreachable (offline, campus
  network blocks `npx` registry fetch, first-run `npx` download failed) or when you
  need to know *which prompt to ask for* before making the call — the file is a prompt
  index, not a docs mirror; it tells you what the server's prompts cover, it does not
  replace calling them.

## Keeping this current

`agentic/ide-mcp/scripts/verify-ide-mcp.sh` checks this file's SHA-256 digest against
the value recorded in the script (offline, no network required in CI). Re-vendor with:

```bash
curl -s -o agentic/ide-mcp/llms/svelte-prompts-llms.txt \
  https://svelte.dev/docs/ai/prompts/llms.txt
shasum -a 256 agentic/ide-mcp/llms/svelte-prompts-llms.txt
```

Update the digest constant in `verify-ide-mcp.sh` after re-vendoring, in the same
commit — a silent content change with a stale recorded digest is exactly the drift
this check exists to catch.

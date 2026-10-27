# PHASE-Z4 Report

| Field | Value |
| --- | --- |
| **status** | DONE |
| **cold_review** | pending |

## Summary

`DualWriteProposalDraftStore`: filesystem write first, then Redis `ttod:proposal:{id}` + status/user sets.
API list uses sets (no `KEYS`). Empty `REDIS_URL` → `FilesystemProposalDraftStore`.
`test_dual_write_proposal_leaves_cli_loadable_file` proves `ProposalStore.load` still works.
Patched storage-failure tests to `proposal_drafts.ProposalStore.save`.

## Acceptance

- [x] Dual-write + CLI loadable file
- [x] No KEYS/FLUSH in app code (only `Redis.from_url` in `redis_client.py`)
- [x] Review/API proposal tests green
- [ ] Cold review — pending

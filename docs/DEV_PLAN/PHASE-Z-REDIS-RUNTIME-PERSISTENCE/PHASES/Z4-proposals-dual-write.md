# PHASE-Z4: Proposal drafts in Redis (dual-write for CLI accept)

> **Track:** backend proposal routes + store adapter; **not** `ttod_core` Redis dependency.
> **Status:** BLOCKED until Z3 DONE

## Goal

API proposal create/list (review queue) uses Redis as the runtime store so drafts survive backend restart and support indexes by status/user. **Simultaneously dual-write** each save to `TTOD_PROPOSAL_DIR` so `cli.py proposal accept` / `ProposalStore.load` keep working without importing `redis` into `ttod_core`.

## Deliverables

- Backend `ProposalDraftStore` Protocol: save/load/list; Redis implementation + filesystem dual-write on save; Memory or filesystem-only when `REDIS_URL` empty.
- Keys: `ttod:proposal:{id}` (JSON); `ttod:proposals:status:{status}` set; `ttod:proposals:user:{user_id}` set. List paths use sets — **no `KEYS *`**.
- Review queue still role-gated; corpus untouched on create.
- Tests: create → present in Redis + file; restart backend (or FakeRedis persistence story) still lists; accept substrate file loadable by `ProposalStore`.
- Cold review + report.

## Scope

**In:** API persistence path.
**Out:** Changing accept to Redis-only; writing accepted quotes into Redis; UI redesign.

## Prompt (Implementation Agent)

```text
Implement PHASE-Z4 per
docs/DEV_PLAN/PHASE-Z-REDIS-RUNTIME-PERSISTENCE/PHASES/Z4-proposals-dual-write.md.

## Deliver
1. Replace bare ProposalStore(...) calls in main.py with an injectable draft store that dual-writes.
2. On save: write Redis record + indexes, then write the same JSON via ttod_core ProposalStore to proposal_dir.
3. On list (API): prefer Redis indexes; if Redis down and REDIS_URL set → 503 (fail closed).
4. Prove with a test that the file under proposal_dir is loadable by ProposalStore.load(proposal_id).
5. Full proposal/review tests green. Hand off for cold review — do NOT mark DONE.

## Constraints
- Do not add redis to ttod_core. Do not commit unless asked.
```

## Acceptance

- [ ] API list uses status/user indexes, not `KEYS`.
- [ ] Dual-write proven: Redis entry and filesystem JSON both exist after POST.
- [ ] `ProposalStore.load` succeeds on the written file (**CLI accept substrate intact**).
- [ ] RedisError on configured stack → 503 for create/list.
- [ ] Cold review filed; blocking Fn closed.

## Risks

- Dual-write partial failure (Redis ok, disk fail) — fail the request; do not leave Redis-only orphans without a documented repair. Prefer disk-first or transactional best-effort with explicit report note.
- Student tips inventing a third store — point them at this Protocol.

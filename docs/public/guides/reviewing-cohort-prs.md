---
title: Reviewing the cohort's PRs
eyebrow: For the instructor, running review and your own work at once
description: A git/gh workflow for triaging student pull requests in parallel with your own backend work, without stashing, blocking, or losing state.
permalink: /guides/reviewing-cohort-prs/
lang: en
alt_lang_missing: true
---

# Review ten PRs without stopping your own work

**Who this is for:** the instructor/maintainer running review across the cohort — not students.
[Contributing]({{ '/guides/contributing/' | relative_url }}) covers what a student does to open a
PR and what the automated bot checks; this page covers what *you* do with the PRs that result,
while your own backend debugging keeps running in parallel.

**The actual problem this solves.** With five teams each landing PRs, checking one out the naive
way (`git checkout <branch>` in your own working copy) forces a choice every time: stash your own
in-progress backend changes, or don't review yet. Neither is acceptable at cohort scale. The fix is
one extra worktree, set up once.

## Two review backends, one active

There are two ways to get the automated first-pass comment (same hybrid rubric, same prompt
builder — `scripts/pr-review/build-prompt.sh`), and only one is actually turned on:

| | Local (active) | Cloud (inactive) |
| --- | --- | --- |
| Backend | Your own Ollama instance | Anthropic API |
| Cost | Free, your own compute | Paid per review |
| Trigger | You run it, on demand | Would auto-fire on every PR push |
| Status | **This is what you use today** | Kept in the repo as working documentation, not deleted — commented-out trigger in `.github/workflows/pr-review.yml` |

**Why local, why now:** at cohort scale — five teams, ~10 PRs a day during the sprint — an
automatic per-PR cloud review adds up in API spend for a check that a free local model handles
adequately. If that trade-off changes later (a sponsored API budget, a smaller cohort, wanting
the *automatic* trigger specifically), reactivating the cloud path is two steps, both in
`.github/workflows/pr-review.yml`'s own header comment: uncomment the `pull_request:` trigger,
then `gh secret set ANTHROPIC_API_KEY`.

## Set up once, before the first PR lands

1. **Use host Metal Ollama for review (Tanit default).** `make review-pr` talks to
   `http://localhost:11434` and model `qwen2.5-coder:32b` unless you override. Confirm the
   model is pulled on the **host** server:
   ```bash
   curl -s http://localhost:11434/api/tags | python3 -c 'import sys,json; print([m["name"] for m in json.load(sys.stdin)["models"]])'
   # if missing:
   ollama pull qwen2.5-coder:32b
   ```
   The Compose Ollama on `:11435` is a small teaching runtime (`llama3.2:1b` + embed) — not
   where the 32B coder lives. To force compose anyway:
   `OLLAMA_BASE_URL=http://localhost:11435 OLLAMA_MODEL=llama3.2:1b make review-pr PR=<n>`.
2. **The review worktree**, covered next.

## One worktree, not a habit of switching branches

From your existing clone's root:

```bash
git worktree add ../ttod-review main
```

Your original clone stays your own workspace — your backend debugging branch, your half-finished
changes, untouched. The new `../ttod-review` directory (a sibling of your clone, not inside it) is
a second, independent checkout of the same repository you use *only* for checking out and running
student PRs. Checking out a PR there never touches your own uncommitted work, because they're
different directories with different working trees over the same `.git`. Tear it down when the
cohort's PR wave is over: `git worktree remove ../ttod-review`.

**Escape hatch: a second review worktree, only when you actually need one.** One reused worktree
is enough for the normal sequential loop below — check one PR out, decide, move to the next. The
exception is when a PR's dev server needs to stay up for interactive testing (you're clicking
through a behavioral acceptance criterion) while another PR is waiting on you at the same time.
Don't make `gh pr checkout` fight the running server for that case — open a second, throwaway
worktree instead:

```bash
git worktree add ../ttod-review-2 main
```

Use it exactly like the first, for that one PR, then remove it (`git worktree remove
../ttod-review-2`) once it's no longer needed — this is a one-off for a specific collision, not a
second standing worktree to maintain alongside the first.

## The core loop

Run every command below from the `ttod-review` worktree, not your main checkout.

1. **See what's waiting.** `make review-queue` (already in the Makefile) lists open PRs, read-only
   — it never approves or merges on your behalf. Or `gh pr list` for the raw list.
2. **Run the local review first.** `make review-pr PR=<N> POST=1` (or
   `scripts/pr-review/review-local.sh <N> --post`) scores the PR against the hybrid rubric (generic
   §5 dimensions + that task's own acceptance criteria, matched from the branch name — see
   [Contributing → Automated review]({{ '/guides/contributing/#automated-review' | relative_url }}))
   using your local Ollama, and posts it as a PR comment. Drop `POST=1` to just print it to your
   terminal first if you want to read it before it goes public. Treat it as a first pass: it tells
   you where to look, not what to conclude. The bot must label each bullet `MUST FIX:` or `NIT:`;
   when you `--request-changes`, elevate **MUST FIX** items only — NITs stay comments or stay off
   the request.
3. **Check it out to actually run it.**
   ```bash
   gh pr checkout <N>
   npm --prefix services/frontend run check && npm --prefix services/frontend run build
   ```
   The bot reads a diff; it does not run the app. If a task's acceptance criterion is behavioral
   ("clicking a node updates the aside"), you still need to see it happen once.
4. **Decide, then say so on GitHub, not just in your head.**
   - Looks right, bot flagged nothing you disagree with → `gh pr review <N> --approve`
   - Small, nameable issue → `gh pr review <N> --comment --body "..."` and let the student push a
     fix, rather than fixing it yourself
   - Wrong direction or missing the task's own acceptance criteria → `gh pr review <N> --request-changes --body "..."`
5. **Merge only what's actually ready.** `gh pr merge <N> --squash` — branch protection already
   requires the `typecheck-and-build` check and one approval, so a merge attempt fails loudly if
   either is missing; you're not relying on memory to enforce that.

## When the local review isn't enough

It's a manual step, not one that fires on every push — you decide when to re-run it, and a smaller
local model won't always catch what a larger one would. Two situations call for you to run a
review yourself, deliberately, on top of it:

- **A PR the local review under-covered** — its branch name didn't match `<seam>-task<N>` *and*
  didn't match a known short alias (e.g. Equipo 5's `task/2-personal-library` → `accounts-task2`
  inside `build-prompt.sh`), so it only got the generic rubric. Check the stderr line
  `pr-review: brief=…` from `make review-pr`. If `brief=none`, rename the branch or run
  `/code-review <N> --comment` with the right task sheet attached — don't treat a generic-only
  bot comment as the full picture.
- **A PR you're about to request changes on** — post your own comment referencing the specific
  acceptance line from that task's own [detail sheet]({{ '/teaching/tasks/' | relative_url }})
  (there is no in-app `ASSIGNMENT.md` — the detail sheet on this site is the canonical source, and
  links to its own GitHub brief at the bottom), not a restatement of the bot's.

## Running this alongside your own backend work

This is the actual point of the separate worktree: your backend debugging session in your main
clone never needs to know review is happening. Concretely:

- Keep your main clone on your own working branch, mid-debug, dirty working tree and all.
- Do all of the loop above from the `ttod-review` worktree, on a clean `main`-tracking checkout
  that only ever holds one student's branch at a time (`gh pr checkout` replaces it each time,
  cleanly).
- If a student's PR changes `services/frontend/src/types/domain.ts` (the shared contract) and your
  own backend work depends on that file, that's the one case worth a manual look before merging —
  a contract change ripples into every module, including whatever you're mid-debugging. Everything
  else is safely isolated by the worktree split.

## Troubleshooting

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `review-pr` fails to connect | Ollama isn't running, or `OLLAMA_BASE_URL`/port doesn't match | Host default is `:11434`; confirm `curl -s http://localhost:11434/api/tags` |
| `HTTP Error 404` / `model '…' not found` | Model missing on the endpoint you hit (classic: 32B coder on host, script pointed at compose `:11435`) | Use host `:11434`, or set `OLLAMA_MODEL` to a name listed on that port's `/api/tags` |
| Review is shallow or misses obvious things | Model is too small for the diff's complexity | Pull and set a stronger `OLLAMA_MODEL`, or fall back to `/code-review <N> --comment` for that one PR |
| Review comment only shows the generic rubric | Branch name didn't match `<seam>-task<N>` | Ask the student to rename the branch, or just run `/code-review <N> --comment` yourself for that one |
| `gh pr checkout <N>` fails or leaves stray files | You ran it from your main clone instead of the review worktree | `cd` into the `ttod-review` worktree first — this is the one command in this whole guide that must run from the right directory |
| Merge blocked despite an approval | `typecheck-and-build` hasn't reported yet, or reports failing | `gh pr checks <N>` to see which; don't override with an admin merge unless you know exactly why it's failing |

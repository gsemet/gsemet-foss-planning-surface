# Change Specification: the eval judge follows a PR whose head was replaced

Short name: `judge-head`. Area: the eval kit (`evals/kit/audit.py`, `evals/kit/dry_run.py`) and its
docs (`evals/README.md`). No change to the CLI, the cards, the hooks or the scenario.

## Goal

In a sandbox campaign the audit's judge must judge the code that was actually reviewed and merged.
Today it judges the head the batch's record holds (the CR's last `ship`/hand-back head). In a stack
batch on GitHub, each bottom merge restacks the PRs above it, replacing their heads; the recorded
heads are then on no ref of the origin, and the judge answers `not run`. The judge must instead
resolve the CR's PR on the forge, judge that PR's head (its head at merge when merged, its current
head otherwise), and say in its row which head it judged and where that head came from.

## Evidence (why)

Run 2 of `real-foreman`, 2026-11-15, stack mode
(`C:/Users/gaeta/Projets/chantier-eval/real-foreman-2026-11-15.audit.md`, finding 5 and
`## The judge`): 4 of the 6 judge rows were `not run`:

| CR | PR | head the record holds | PR's head at merge |
| --- | --- | --- | --- |
| CR-102 edit-item | 6 | 3f60a08 | 93a906c |
| CR-103 status-filter | 7 | 194525b | 59edd1f |
| CR-104 json-api | 9 | 2eb57ae | 1f29cde |
| CR-105 stats-page | 10 | 881a963 | 3900c46 |

Each row read `not run (head <recorded sha> not found on the origin)`; `main` (all 5 CRs) passed.
The PRs' heads at merge are still reachable: `git ls-remote origin refs/pull/6/head` (and 7, 9,
10) on `https://github.com/gsemet/chantier-eval-sandbox.git` returns exactly 93a906c, 59edd1f,
1f29cde, 3900c46, checked on 2026-11-15. `judge.clone` already fetches
`+refs/pull/*/head:refs/remotes/origin/pull/*`, so those heads resolve in its clone. The parallel
run of the same day (`real-direct-2026-11-15.audit.md`) had no restack: recorded heads equalled
the PRs' heads and the judge passed 6 of 6.

## What changes

### 1. `evals/kit/audit.py`, `judge_rows` (feature CR branch, the final `else:`)

Today:

```python
view = views.get(c["id"]) or {}
if view.get("headRefOid") and not same(view["headRefOid"][:12], c["head"]):
    head += f" (the PR's head is {view['headRefOid'][:7]})"
got = judge.feature(origin, c["head"], [slug_of(c)])
```

New behaviour:

- The ref judged is the PR's head read from the forge: `headRefOid` of the `gh pr view` of the PR
  the record holds for the CR (`c["pr"]`). For a merged PR GitHub reports the head it had at
  merge; for an open PR its current head. Make sure the view used is the one of `c["pr"]` itself
  (match by PR number), not merely the last PR viewed for that CR in `sandbox_checks`; adjust what
  `sandbox_checks` returns if needed (for example a view per PR number besides the per-CR one), and
  keep J5's behaviour and messages unchanged.
- `judge.feature(origin, <the PR's headRefOid>, [slug_of(c)])` is called with that SHA.
- The `head judged` cell always says which head was judged and its source:
  - merged PR: `<sha7>, the PR's head at merge`;
  - open PR: `<sha7>, the PR's head`;
  - in both cases, when the record's head differs (`not same(...)`), append
    ` (the record holds <recorded sha7>)`.
  The `sha7` printed is the one `judge.feature` returns (`got["sha"][:7]`), so the cell names what
  was checked out; on `not run` print the forge's head instead.
- When the forge view of `c["pr"]` is missing (`gh pr view` failed; `sandbox_checks` already writes
  a `FAIL [J5]` line with gh's text) or holds no `headRefOid`, the row is
  `not run (the PR's head could not be read from the forge: <gh's text, or "no headRefOid">)`,
  with the recorded head in the `head judged` cell followed by ` (the record's head, not judged)`.
  No judging of the recorded head in its place: the request is to judge the PR's head, and a
  silent switch back would hide exactly the failure this CR fixes.
- The `no head` guard (`elif not c.get("head")`) stops being a reason to skip: a CR with a PR but
  no recorded head is judged at its PR's head like any other. The `no PR`, `cancelled`, `no
  origin`, `fix` and `no hidden test` rows are unchanged, as are the release rows and the `main`
  row.
- Update the module docstring (line 21, "runs the hidden tests of the frozen CRs on each CR's
  recorded head") to say each CR's PR head as the forge reports it (its head at merge once
  merged), and the `judge_rows` docstring if it names the head.

`judge.py` needs no change: its `clone` already fetches the PR refs and its `checkout` accepts a
SHA. Its printed `judge <slugs> at <sha7>` line stays as it is.

### 2. `evals/kit/dry_run.py`, the proof

The staged clean world must reproduce the restack, so that the dry run fails on today's code and
passes on the new one:

- In `Batch.feature`, after `handback <cr> ready` and before the operator's merge, play the forge's
  restack: move the PR's branch on the local origin to a new commit carrying the same change (for
  example the reviewed commit rebased or amended with a new message, made outside any agent, with
  `world.git_origin(...)` or a temporary clone, so no transcript and no rail sees it). The local
  forge (`sandbox_forge.py`, `head()`) then moves the PR's `head_sha` and `refs/pull/<n>/head` to
  the new commit; the merge, through the merge command setup printed, merges that new head (its CI
  runs there and must be green). The record keeps the old head.
- In `case_clean`, beyond today's assertions (audit exit 0, no failed check, judge rows all
  `pass`), assert from the judge table that the feature CR's `head judged` cell starts with the new
  head's seven characters, says `the PR's head at merge`, and names the old head as
  `the record holds <sha7>`. Extend the module's table parser (`judge_rows(text)` in
  `dry_run.py`) to return the `head judged` cell too, or add a second parser; keep the existing
  callers working.
- Caution for the case's power: a clone of a local path may copy unreachable objects, so the old
  head may still resolve in the judge's clone and today's code might pass by judging it. The
  assertion on the `head judged` cell is what proves the fix, not the `pass`.
- If the restack makes another check of the clean world fail (a check reading the PR's head against
  the record), say so in the PR and fix the check only if it is wrong on a restacked PR; do not
  weaken a rail.

### 3. `evals/README.md`

Line 118 ("the judge (the hidden tests on each CR's head, on `main`, and the release judge)"):
say the hidden tests run on each CR's PR head as the forge reports it (its head at merge once
merged, which a stack's restack may have replaced since the CR's hand-back), and that the row names
the head judged and, when it differs, the head the record holds. Line 266 (`kit/judge.py`, "the
hidden tests on a PR's head") already holds. No change to `SCORECARD.md` or the runbooks: the
judge marks no rail, and `copilot/RUNBOOK.md` already says "on the PR's head".

## Decisions carried from `02-answers.md`

1. The request's scope stands as written: the judge resolves the CR's PR and judges its merged (or
   current) head, and says which head it judged. Planned in the next parallel batch, before the
   next release. Implementation detail is the agents': the choices above (the cell's wording, `not
   run` when the forge view is missing, the dry run's restack) are taken within that scope.

## Out of scope

- `sandbox.py merge` and GitHub's asynchronous merge for a native stack (finding 1 of the same
  audit): a separate fix (`chantier/fix-sandbox-stack-merge`).
- `cost` on a paused batch without `--batch` (finding 6), the retro-critic's J1 prompt line, and
  any other finding of the two audits.
- The CLI's recorded head: chantier keeps recording the hand-back head; nothing in `rails.py`,
  `ship` or `handback` changes, and no new CLI command.
- The release judge (`judge.release`, judged by its tag) and the `main` row.
- Rewriting past results in `evals/results/`.

## Evidence that proves it

- `just eval-dry-run` passes, with the clean case's new assertions on the `head judged` cell; run
  on the PR's branch before the change to the audit, the new assertion fails (say so in the PR, with
  the line it printed).
- `just check` passes (lint covers `evals/kit/`).
- By hand, read-only on the forge, from the worktree: the judge on each of the four replaced heads
  of run 2, for example
  `uv run --no-project python evals/kit/judge.py https://github.com/gsemet/chantier-eval-sandbox.git 93a906c edit-item`,
  and likewise `59edd1f status-filter`, `1f29cde json-api`, `3900c46 stats-page`; paste the four
  last lines in the PR (they prove the PR heads resolve through `refs/pull/*`; a `fail` there is a
  finding to report, not this CR's to fix). Run 2's workspace is closed (`4-batch/` is gone), so
  the audit itself cannot be rerun on it.
- What only a live run proves: the next stack run of `real-foreman` on GitHub, whose judge rows
  must name the PRs' heads at merge with no `not run` for a replaced head. The PR's Known gaps names
  this.
- No `just scenario`: per `AGENTS.md`, a change to the eval kit and its docs alone needs none.
  No `just mod`: nothing in `hooks/` or `types/`.

## Open questions for the user

None. The answers leave no behaviour question open.

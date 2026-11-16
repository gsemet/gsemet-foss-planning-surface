# Verify CR-267

Head: 0be062cbfcd01a7b47bf84d72cf22d4d8ddffa24

Result: VERIFIED

Every claim below was judged at 0be062c (`git rev-parse HEAD` in the CR worktree printed
`0be062cbfcd01a7b47bf84d72cf22d4d8ddffa24`; `gh pr view 212 --json headRefOid` printed the same).

## 1. Structure tests, at 0be062c

Command (worktree): `uv run --locked pytest skills/chantier/scripts/cli/tests/test_mode_switch.py -q`

```
......                                                                   [100%]
6 passed in 4.19s
```

Covers: same mode and unknown note refused for each of the three modes with `batch.json` and
`events.jsonl` bytes unchanged; to a stack the ready CRs go first by readiness; `after` chain kept;
`previous` in the `mode` event; leaving a stack clears `stacked`.

## 2. Live check on a temporary batch, at 0be062c

Setup: a throwaway git repo (scratchpad `live`), `chantier open 1-inbox/alpha 1-inbox/beta 1-inbox/gamma
--default-branch main` printed "opened batch-01 on claude: 3 CRs, 4 slots, parallel, steering foreman".
CR-101 set `merged` in `batch.json`. CLI run from the worktree:
`uv run --locked --project <worktree> chantier order mode --note <mode> --batch batch-01` (via env
`CHANTIER_BATCH`). Printed lines, trimmed:

```
> order mode --note parallel            (batch is parallel)
error: batch-01 is already a parallel                                  exit 2
> order mode --note stack               (parallel -> stack)
batch-01 is a stack now (order: CR-102 -> CR-103): the stack driver stacks the open PRs, the CRs to come join on top   exit 0
> order mode --note parallel            (stack -> parallel)
batch-01 is parallel now: each open PR is rebased on the default branch, its long gate and CI run again, and it leaves draft once ready
run `forge-stack unstack` before any rebase                            exit 0
> order mode --note series              (parallel -> series)
batch-01 is a series now (order: CR-102 -> CR-103): each open PR is rebased on the one below, the ones above the bottom go back to draft   exit 0
> order mode --note parallel            (series -> parallel)
batch-01 is parallel now: each open PR is rebased on the default branch, its long gate and CI run again, and it leaves draft once ready   exit 0
> order mode --note fast
error: order mode --note parallel|series|stack (any mode to any other)   exit 1
```

Merged CR untouched: the record read after every switch showed `CR-101 merged order=1` each time
(CR-102 and CR-103 stayed `queued order=2` and `order=3`; `stacked=False` after leaving the stack).
`events.jsonl` (`Select-String '"mode"'`) holds four `kind: mode` events with `previous`:
`stack/parallel`, `parallel/stack`, `series/parallel`, `parallel/series`; none is written for the two
refused calls.

## 3. Before / after against origin/main

`git rev-parse origin/main` = 33fc800e4945fb252a8a09b79d403d2ce969b62b; a detached worktree of it ran the
same CLI on the same parallel batch:

```
> (origin/main) order mode --note series
error: order mode: only a series batch switches, to a stack (`order mode --note stack`)   exit 2
> (origin/main) order mode --note stack
error: order mode: only a series batch switches, to a stack (`order mode --note stack`)   exit 2
```

At 0be062c the same two calls succeed (section 2). The detached worktree was removed afterwards.

## 4. Cards and docs

`git grep -n -i "series to stack\|series to a stack\|series switched\|only a series" -- skills docs README.md scenario`
at 0be062c printed nothing: no leftover "series to stack only" text.

`git grep -n "order mode --note" -- skills/chantier/references docs` shows the new text:
`chief-of-staff.md:887` ("any mode to any other, on the user's word"), `chief-of-staff.md:951`,
`concepts.md:147` ("`order mode --note parallel|series|stack`, on the user's word"), `foreman.md:230`
("A mode switch"), `hosts/claude-code.md:291` (stack row with `forge-stack create|rebuild|show|unstack`),
`docs/batch-modes-texts.md:74` and `docs/batch-modes.svg:101` ("order mode --note parallel|series|stack;
merged CRs never change."), `docs/use-cases-foreman.md:86-87` (the generalised row and "Switch to
parallel.").

## 5. Scenario gate (cited, not rerun)

`work/gates/20261115-022428.log` (head line: `gate CR-267 branch ... head 0be062cbfcd01a7b47bf84d72cf22d4d8ddffa24`);
`Get-Content` of the log shows:

```
         ok  stack (github): 103/103 checks, 269.5 s
         ok  series-deps (github): 67/67 checks, 191.2 s
         ok  gitlab (gitlab): 32/32 checks, 59.7 s
         (and parallel, gates, release, direct, qa-driver, surface-board: ok)
result: pass at 0be062cbfcd01a7b47bf84d72cf22d4d8ddffa24
```

`series-deps` holds the live switches, `stack` the `forge-stack unstack` GitHub case, `gitlab` the
retarget-only case (the diff of `scenario/run_scenario.py` and `scenario/README.md` carries them,
with the budget `series-deps` 190 -> 260, matching the PR's Known gaps).

## 6. PR description (`gh pr view 212 --json body`) against the diff and pr-template.md

- Layout matches: Summary, Deliverables, Blast radius, Autonomous decisions, Known gaps visible; one
  `<details>` with Changes, Human decisions, Impacts, Test plan, Internal references; nothing after
  `</details>`.
- No internal reference outside "Internal references" (CR-267 only there); "stack driver" and
  "specification" are product terms of this repository (the diff changes those cards).
- Changes match `git diff --stat origin/main...HEAD` (18 files): orders_apply, forge_stack(+_gh,
  _gitlab, declare), cards, docs, README, tests, scenario. Minor: `declare/orders.py` (help text, 10
  lines) is not named in Changes; harmless.
- Known gaps (timings not remeasured; `series-deps` budget raised to 260 s; `stack` renumbering tie)
  agree with the diff. Test plan boxes still carry `<sha7>` placeholders: expected before review and
  merge, not a defect of the description.
- Not applicable: no change to the CR board pane, so no screenshot is required.

## Not done

`just check` and the full scenario were not rerun by me (CI green and gate pass cited at this head).

## Description pass

Judged at 0be062cbfcd01a7b47bf84d72cf22d4d8ddffa24 (`git rev-parse HEAD` and `gh pr view 212 --json headRefOid` agree).

- Layout vs pr-template.md: Summary, Deliverables, Blast radius, Autonomous decisions, Known gaps visible in order; one Details block holding Changes, Human decisions, Impacts, Test plan, Internal references; nothing after `</details>`; no Issues References (spec has no `issue:`). Roles named (stack driver) and card paths are project terms of this repository; internal refs only in the last section. OK.
- Changes list vs `git diff --stat origin/main..HEAD` (18 files, at 0be062c): every file named exists in the diff (orders_apply, declare/orders, forge_stack, forge_stack_gh, forge_stack_gitlab, declare/forge_stack, 6 cards, 4 docs, test_mode_switch.py, run_scenario.py, scenario/README.md). OK.
- Known gap "series-deps budget raised to 260 s": `git diff origin/main..HEAD -- scenario/README.md` shows `-| series-deps | 190` / `+| series-deps | 260`; run_scenario.py line 99 reads 260. OK.
- Box "just check (106 passed), just scenario pass at 0be062c": `gh pr checks 212` shows just check macos/ubuntu/windows, just scenario and eval-dry-run all pass; work/gates/20261115-022428.log ends `result: pass at 0be062cbfcd0...`; 106 passed is from work/r1.md (just check). OK.
- Box "Evidence before at 33fc800, after at 0be062c": this file sections 2 and 3 (before at `git rev-parse origin/main` = 33fc800, switch refused; after at 0be062c accepted). OK.
- Box "Review approved at 33fc800, committed as 0be062c": events.jsonl 2026-11-15T01:24:02Z note "r1 inspector approved at 33fc800e4945..."; HEAD parent is 33fc800 (`git show --format=%P HEAD`). OK.
- Box "Verified at 0be062c": sections 1-5 above. "CI green at 0be062c": gh pr checks above. OK.
- No pane change: no screenshot required.

---

# Delta pass at e7eab41 (rebase of the same commit onto CR-263's branch 84f669a)

Head: e7eab41584ccd22dc00ad5ffd87516dade70e355

Result: VERIFIED

Judged at e7eab41 (`git rev-parse HEAD` in the CR worktree and `gh pr view 212 --json headRefOid` print
`e7eab41584ccd22dc00ad5ffd87516dade70e355`; `baseRefName` is `chantier/batch-18/cr-263-change-specification-batch-17-retro-card`).

## Why the move touched only the card hunks

- `git diff --stat 84f669a e7eab41` prints the same 18 files and `581 insertions(+), 170 deletions(-)` as
  `git diff --stat 33fc800 0be062c` did at the previous head.
- The base change (`git diff --name-only 33fc800 84f669a`) overlaps the CR's files in five cards only
  (chief-of-staff, concepts, driver, foreman, hosts/claude-code). I compared the changed lines of those five
  files between the two diffs (`Select-String '^[+-][^+-]'`): 63 lines vs 63 lines, `Compare-Object` printed
  no difference. The CLI, tests, scenario and docs files are not in the overlap.
- Claims carried from 0be062c, reason: patch unchanged, base brought changes only to card context lines:
  CLI refusals/record (section 1-2 above), before/after against the old CLI (section 3), docs and scenario
  gate (section 5; the gate pass is the one at 0be062c, kept by a clean rebase, rule 3 of the Driver card).

## Claims judged again at e7eab41

1. Structure tests: `uv run --locked pytest skills/chantier/scripts/cli/tests/test_mode_switch.py -q`
   printed `6 passed in 3.24s`.
2. Live switches, throwaway repo (scratchpad `live2`, `open 3-ready/alpha beta gamma`, CLI run with
   `uv run --locked --project <worktree> chantier order mode --note <m> --batch batch-01`):
   ```
   > parallel  (parallel)        error: batch-01 is already a parallel                 exit 2
   > stack                       batch-01 is a stack now (order: CR-101 -> CR-102 -> CR-103): the stack driver stacks the open PRs, the CRs to come join on top   exit 0
   > parallel                    batch-01 is parallel now: each open PR is rebased on the default branch, its long gate and CI run again, and it leaves draft once ready
                                 run `forge-stack unstack` before any rebase           exit 0
   > series                      batch-01 is a series now (order: ...): each open PR is rebased on the one below, the ones above the bottom go back to draft   exit 0
   > parallel                    (parallel line, no unstack hint)                       exit 0
   > fast                        error: order mode --note parallel|series|stack (any mode to any other)   exit 1
   ```
   `events.jsonl` holds four `mode` events with `previous` (parallel>stack, stack>parallel, parallel>series,
   series>parallel); none for the refused calls.

## Open items for the Driver (not code failures)

- The posted description still names `0be062c` in the Test plan (Local gates, Evidence, Review, Verified, CI)
  and its base was retargeted: the boxes must be re-stated at e7eab41 (or carried with the reason above).
- `gh pr checks 212` at e7eab41: just check x3 and eval-dry-run pass; `just scenario (ubuntu-latest)` was
  still pending when I looked.
- Not rerun by me: `just check` and `just scenario` (the cited gate pass at 0be062c is kept by the clean rebase).

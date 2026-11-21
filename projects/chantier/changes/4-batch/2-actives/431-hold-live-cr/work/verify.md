# CR-431 verify

Head: c13260272361568a74083699ac0e85e3479b4f3d

Rules read (`$CHANTIER rules`): AGENTS.md, CONTRIBUTING.md and the listed docs; the gates they name are cited below.

## Claims (all judged at c1326027)

1. New and changed tests pass at the head. Command (worktree, code imported from the worktree):
   `python -m pytest test_hold_live.py test_hold_live_modes.py test_hold_live_series.py test_hold_live_shared.py test_hold_live_stack.py test_stack_hold.py test_came_back.py -q`
   Output: `60 passed in 17.84s`. They cover the Evidence section's cases: hold refusals, hold in each mode (blocked, lease ended, slot free, handback refused, pending order, take refusal, unhold, check_slot), shared definition, stack, series, drop, leaving a stack, release refusal, status views, card checks.
2. Whole suite at the head: `python -m pytest -q -n auto --dist worksteal` -> `1540 passed, 20 skipped in 94.52s`.
3. The new tests fail on the previous code (base 3b3eba06, detached worktree, removed after): the five `test_hold_live*.py` files copied onto base, run with base's `src` first on PYTHONPATH -> `ImportError: cannot import name 'apart_owner' from 'chantier.rails'`, `4 errors during collection`.
4. CI at the head (`gh pr checks 399`): just check macos/ubuntu/windows pass, just eval-dry-run (ubuntu) pass, just scenario (ubuntu-latest) pass (job log: `ok stack (github): 210/210 checks`, the unit holding case `hold_live`, listed in `UNITS` at scenario/run_scenario.py:84). Driver's log: `just check` pass and `just eval-dry-run` pass (18 of 18) at c132602 before the push. Local scenario log work/gates/scenario-r3.log: `ok stack (github): 210/210 checks, 556.4 s` (budget 750).
5. Cards: `routing.md` lines 15-16 name `stop hold: <O-n>`, `rebase: <cr> dropped`, `stopped: held; worktree clean|dirty`; `driver.md` lines 53-54 (`stop hold`), 954 (`rebase: <cr> dropped`); `chief-of-staff.md` 1318 "Holding a CR" names a live CR; checked in `test_came_back.py` (passes, claim 1). CLI help (`chantier order --help`): `hold|unhold (a live CR, ...`.
6. Review box: `$CHANTIER log CR-431` has `move bd7543a..c132602 (rebase) inspector approved at c13260272361568a74083699ac0e85e3479b4f3d`: a review note at the head's SHA.
7. PR description (as posted, `gh pr view 399`): renders (sections, tables, details fold), no images; Summary, Deliverables and Changes match the diff (rails, stacks, stack_words, delivery, forge_stack_apart, orders_hold/orders/orders_drop/orders_reorder, driver, status words/views/now_next, cards, scenario, tests: all in `git diff --stat origin/main...HEAD`); Known gaps names the missing pane screenshot (UNVERIFIED bullet matches). Role names appear only as product terms of this change.

## Notes for the Driver (not failures)

- The Test plan boxes still hold `<sha7>` placeholders and are unchecked: fill them with `c132602` and check them at hand-back.
- Known gaps' second bullet says the pipeline job remains: it is now green at the head (claim 4); the Windows run at the top of the stack remains. Reword it.
- Not run by me: a Windows `chantier gate` (owed by AGENTS.md at the top of the stack), and the real-session pane screenshot (named known gap, spec section 7: absence is not a failure).

Verdict: VERIFIED

## Description-only pass (Head: c13260272361568a74083699ac0e85e3479b4f3d)

Judged at c1326027 (`gh pr view 399 --json body,headRefOid`: headRefOid c13260272361568a74083699ac0e85e3479b4f3d; `git diff --stat origin/main...HEAD`: 31 files).

- Clean: Summary, Deliverables (table), Blast radius, Autonomous decisions, Known gaps visible in order; one Details fold holding Changes, Human decisions, Impacts, Test plan, Internal references; no images.
- Consistent with the diff: every file group in Changes (rails, stacks, stack_words, delivery, forge_stack_apart, orders*, driver, status words/views/now_next, cards, scenario, tests) is in the diff stat; no delivered change unmentioned. The Test plan boxes now name c132602 (Local gates, Review, Verified, CI), the head.
- Review box: `$CHANTIER log CR-431`: `move bd7543a..c132602 (rebase) inspector approved at c13260272361568a74083699ac0e85e3479b4f3d`, the SHA the box cites.
- Known gaps: pane screenshot (the one UNVERIFIED claim), Windows `chantier gate` owed on top of the stack, driver.md stop-hold note minor gap (Driver's closing note): all present; the pipeline-green bullet is reworded as asked.
- Internal references: CR name and batch only in the last section. Role names (Driver, Drivers) appear as product terms of this change to the Driver card; "a reviewer" in the third Known gaps bullet names no role of the template as doer (minor wording, not a failure).

Verdict: VERIFIED

## Move c132602 -> db75bff (restack onto CR-430, 6fb2b35)

Head: db75bff64f9645e1bc88d68814dae73e332d8665

Judged at db75bff (`git rev-parse HEAD` in the worktree; `git status --short` clean). The move touched the live hold's code (orders_hold, stacks, park, rails, status, records), so the code claims are judged again.

8. Hold-live tests at db75bff. Command (worktree `tests/`, `uv run --no-sync --project <worktree> python -m pytest test_hold_live.py test_hold_live_modes.py test_hold_live_series.py test_hold_live_shared.py test_hold_live_stack.py test_stack_hold.py test_came_back.py -q`): `61 passed in 39.05s`. They cover the live hold in each mode, shared helpers with the park, held and parked together (test_hold_live_shared, test_stack_hold).
9. Whole suite at db75bff: `python -m pytest -q -n auto --dist worksteal` -> `1584 passed, 20 skipped in 191.76s`.
10. Claims 3 (new tests fail on the old code), 5 (cards and help) and the card checks: carried from c132602 for 3 (the tests' content is unchanged in kind; they still pass at the head, claim 8); 5 is exercised by `test_came_back.py`, passed at db75bff (claim 8).
11. CI at db75bff (`gh pr checks 399`, headRefOid db75bff): `just check (ubuntu)` pass, `just eval-dry-run (ubuntu)` pass; `just check` macos and windows and `just scenario (ubuntu-latest)` still `pending`. Local scenario log work/gates/scenario-r3.log is at an older head and proves nothing at db75bff. No long gate passed at db75bff (`ship` says so).
12. Review box: `$CHANTIER log CR-431` holds no approved note at db75bff; the last approval is `move bd7543a..c132602 (rebase) inspector approved at c1326027...`. The restack with 18 conflict files resolved was not reviewed.
13. PR description (`gh pr view 399 --json body`): the Test plan boxes (lines 60, 62, 63, 64) still say `Local gates`, `Review: approved`, `Verified`, `CI green` at `c132602`, not in db75bff's history (the CLI's `ship` lists the same four). The PR is draft.

Failed: 12 (no review at db75bff), 13 (stale SHAs in the description), 11 (CI pending at the head, no long gate).

Verdict: NOT VERIFIED

## Re-verify at db75bff (after the Driver closed the process gaps)

Head: db75bff64f9645e1bc88d68814dae73e332d8665

14. Code claims 8 and 9 above stand at db75bff (61 passed; 1584 passed, 20 skipped).
15. CI at db75bff: `gh pr checks 399` (headRefOid db75bff): `just check` macos, ubuntu, windows pass; `just eval-dry-run` pass; `just scenario (ubuntu-latest)` pass (4m48s). This is the long gate AGENTS.md names; the local Windows run is owed at the top of the stack.
16. Review: `$CHANTIER log CR-431`: `move c132602..db75bff (restack) inspector approved at db75bff`: the SHA the Review box cites.
17. Description source work/pr-body.md: lines 60, 62, 64 cite db75bff; line 63 (`Verified at`) must read db75bff, set by the Driver now that this verdict is VERIFIED. The description posted on the forge at this moment (`gh pr view 399 --json body`) still shows c132602 on lines 60-64: it must be pushed from pr-body.md before the PR leaves draft. The PR is a draft, as stated.

Verdict: VERIFIED

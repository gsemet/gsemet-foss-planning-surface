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

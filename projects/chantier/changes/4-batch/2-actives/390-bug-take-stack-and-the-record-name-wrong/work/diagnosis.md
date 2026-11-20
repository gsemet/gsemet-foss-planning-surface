# Diagnosis: `stack (github)` scenario, 5 checks red at head 5cb0f31

Reproduction (worktree, 379 s solo, same 172/177 and same 5 checks as CI):
`uv run --locked python scenario/run_scenario.py --unit stack`
Log: work/debugger/stack.log. Unit output: scenario/results/20261120-005621-17260/stack-github.out.
Checks are in `scenario/run_scenario.py`, `stack_batch` (l.5736-5825) and the base-check unit (l.6072).

Cause in one line: `start_base` now returns `stack_start` for every non-fix CR of a stack batch,
so a CR with no recorded `start_on` and a CR below with a PR now reads that CR's branch where it
read the default branch. Four checks assert the old value, which the specification changes on
purpose; one (the fifth) is a bug in the code.

## 1. "independent CRs are all taken at once and start on the default branch; ..." (l.5736) - SCENARIO
Before any PR exists, `take stack` rows 2 and 3 used to say `base <cr-one branch>` / `base <cr-two
branch>` (the chain predecessor, a branch not yet pushed). Spec rule 3 (and "the record never names
a branch that does not exist yet"): no CR below has a PR, no dependency, so the default branch. All
three rows now read `base origin/main`.
Fix: the two assertions `f"base {w.cr(one)['branch']}" in stacked[2]` and `... two ... stacked[3]`
become `"base origin/main" in stacked[2]` and `in stacked[3]`; reword the title to "start on the
default branch; no CR below has a PR, so their place is the default branch too".

## 2. "`order add` joins the open batch, on top of the stack; no batch is opened" (l.5777) - SCENARIO
CR-four is queued, no `after`; CR-three (top of the stack) has a PR. `handoff four` now prints
`base <three's branch>` (rule 2: nearest CR below with a PR), which is what `take` would freeze in
`start_on` (spec section 2: take and record read the same function). Old value `origin/main` was the
old inconsistency (handoff said main, take froze three).
Fix: last conjunct becomes `f"base {w.cr(three)['branch']}" in ln` for a `handoff four` line.

## 3. "a chain through `order after` starts on the ready CR's branch; `--note -` ..." (l.5786) - SCENARIO
`order after four two`: dependency two sits at place 2, below three (place 3, has a PR), so rule 2
returns three's branch, not two's (a dependency wins only when it sits higher than the CR with a PR).
`--note -` removes the `after`; four stays on three's branch (rule 2), no longer on main.
Fix: `chained` tests `base {three branch}`; the final conjunct tests `base {three branch}` too (not
`origin/main`); reword the title: "`order after` on a CR lower in the stack than the top CR with a PR
leaves the base on that CR; `--note -` clears the `after` and the base is unchanged". To keep a
dependency-wins case in the scenario the dependency must sit above the nearest PR CR (unit tests
case B already cover it).

## 4. "the recorded start base falls back to the default branch while the CR that owns it is cancelled..." (l.5818) - SCENARIO
With three cancelled, rule 1 fails (owner ended) and rule 2 walks `chain` (which drops cancelled
CRs): the nearest CR below four with a PR is two. `handoff four` prints `base <two's branch>`, not
main; restoring three brings back three's branch (recorded start_on), as the check wants.
Fix: `on_main` becomes `on_two = any(f"base {w.cr(two)['branch']}" in ln ...)` while cancelled;
reword to "falls back to the nearest CR below with a PR while the CR that owns it is cancelled".
The second half (back with it) is unchanged and still proves recorded, not recomputed.

## 5. "a stacked CR with no PR prints today's line and makes no forge read" (l.6072) - CODE BUG
Batch with three CRs, `stack one two three` placed all three; CR-three (CR-107) has no PR. It
prints `base chantier/batch-04/cr-106-base-two`, expected `base origin/main`. `_base_of`
(`commands/facts.py` l.55) falls to `start_base` when `stacked_read` is None (no PR). `start_base`
(`stacks.py`, new branch `if b_data.mode == "stack" and c.kind != "fix": return stack_start(...)`)
does not test `c.stacked`, though `stack_start`'s own contract (spec section 1) is "not placed by
`stack` (`not c.stacked`)". So a placed CR is now given rule 2 (two has a PR) in the take's
`worktree:` line. No forge read happens (reads() unchanged); only the value moved. The spec text for
`start_base` says "for a CR that is not a release and not a fix" and omits `not c.stacked`: the
spec is imprecise, the code follows it literally and contradicts section 1 and the check's intent
(a placed CR with no PR keeps today's line).
Place to fix: `stacks.py` `start_base`, make the stack branch `b_data.mode == "stack" and
c.kind != "fix" and not c.stacked` (the placed CR then falls through to the old
`after`/`start_on`/default path, today's value). `stack_base` already routes stacked CRs through
the chain, unaffected. Add a unit case: a `stacked=True` CR with no PR and a CR below with a PR:
`start_base` is the default branch.
Decision to confirm with the spec owner: if instead a placed CR's handoff should print its place
(two's branch), the scenario would change to that, but the name "prints today's line" and spec
section 1 argue for the code fix.

## Summary

In a stack batch the forge stack was made late and was refused: CRs started on the default branch even after two PRs were ready, `forge-stack create` never retargeted a PR the stack driver had moved, and the stack as it stands counted working PRs that were not on their place. A real run needed two stack drivers and several extra conflict resolutions for what one take should have done.

This PR makes the stack form once. From the moment two stack CRs are handed back ready with a PR, a CR started from the queue is based on the top of the stack's ready part (recorded at its first take) and its PR is opened on that branch as a draft. A working PR that is not on its place is left out of the stack as it stands until its Driver rebases, and `forge-stack create` retargets the PRs of the plan before it posts the stack.

## Deliverables

Where a CR starts in a stack batch:

| Moment | Start base |
| --- | --- |
| Fewer than two stack CRs ready with a PR | the default branch (as before) |
| Two or more ready with a PR | the top ready CR's branch, recorded at the first take |
| That CR merged or cancelled, or the batch left stack mode | the default branch |

`forge-stack create` on GitHub now prints `#<n> base <old> -> <new>` for each PR it retargets, then the `stack` line. A working CR whose PR is on another base shows `not on its place: its PR is on <pr_base>; to come until its Driver rebases` in `take stack` and `stack`, and is in `to come:` of `show`. The bottom CR in that state refuses with `no PR placed at the bottom of the stack: …` (exit 2).

## Blast radius

Grade: 2. The start base and the stack plan are shared code of the stack mode; parallel, series, releases and fix CRs are unchanged. Reverting the PR restores the previous behaviour; records written with the new optional `start_on` field are still read by the old code.

## Autonomous decisions

- The two open questions of the specification were taken as it chose them: a new CR starts on the top of the ready part, and basing starts at two ready CRs.
- The scenario's stack unit stays one world; at `67b19d4` it runs 137/137 checks in 239 s locally, under its 640 s budget.

## Known gaps

None.

<details>
<summary>Details</summary>

## Changes

- `stacks.py` `start_base()` and `take`: the start base recorded as `start_on` on the CR entry (`core/records.py`).
- `forge_stack.py`: `_plan()` stops at the first working PR off its place; `_create()` retargets before it creates; `facts.py` `stack_lines()` prints the `not on its place` row.
- Cards: `concepts.md`, `foreman.md`, `driver.md`; docs: `README.md`, `docs/batch-modes-texts.md`, `docs/batch-modes.svg`, `docs/use-cases-foreman.md`, `scenario/README.md`.
- Scenario: `scenario/fake_gh.py` answers the stacks endpoint with GitHub's 422 for a PR not based on the previous one; `scenario/run_scenario.py` checks the start base, the recorded base, the retargets and the left-out working PR.

## Test plan

- [ ] New or changed tests: scenario checks of the stack unit
- [ ] Local gates at `67b19d4`: `just check` pass; `run_scenario.py --unit stack` 137/137
- [ ] Evidence: scenario output, `run_scenario.py --unit stack` at `67b19d4`
- [x] Review: approved at `67b19d4` (carried from e8158be: conflict resolution reviewed there; earlier round approved at 842b800)
- [x] Verified at `67b19d4`
- [x] CI green at `67b19d4`: `gh pr checks 242`, all five checks pass

## Internal references

CR-287 stack-forms. Work files: `work/r1.md`.

</details>

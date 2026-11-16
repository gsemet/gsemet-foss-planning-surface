Stacked on #205.

## Summary

A running batch could only switch from a series to a stack. A batch opened in parallel could not become a stack when the user later wanted one ready to merge. This PR lets a running batch switch between any two of its three modes (parallel, series, stack) with `order mode --note <mode>`, on the user's word. Merged work never changes.

## Deliverables

What `order mode` does by target:

| Switch to | Record | What follows |
| --- | --- | --- |
| stack | open CRs reordered: the ones already handed back ready first (in the order they became ready), then the others; chains (`after`) kept | the open PRs are stacked, each on the one below; CRs to come join on top |
| series | same order rule | each open PR is rebased on the one below; those above the bottom go back to draft |
| parallel | `stacked` cleared when leaving a stack | each open PR is rebased on the default branch, its gates run again, it leaves draft once ready |

New action `forge-stack unstack`: dissolves the forge stacks that hold the batch's open PRs (GitHub) and retargets each open PR to the base of the current mode; on GitLab it only retargets.

```text
chantier order mode --note parallel|series|stack
chantier forge-stack unstack
```

Choices: a note equal to the current mode, an unknown note and a closing batch are refused with nothing written; the `mode` event records `previous`; merged, cancelled and fix CRs keep their place, the release CR stays last.

## Blast radius

Grade: 2. The CLI's order command and a new forge-stack action change, with the cards that describe them. A revert restores the series-to-stack-only switch; a batch already switched keeps its recorded order.

## Autonomous decisions

- The five open points of the specification take their stated defaults (chain all open PRs on a switch to a series; PRs above the bottom go back to draft when a stack becomes a series; a running stack driver is told and stops after the branch it is pushing; a started release is taken back with `redo` once the others merge; the user is told which PRs go to draft).
- The forge-stack GitHub code moved to its own module to keep files under the size limit.

## Known gaps

- The scenario unit timings in `scenario/README.md` were not remeasured on a quiet machine; the `series-deps` budget was raised to 260 s.
- The `stack` command renumbers orders from 1 and can tie with a merged CR's order; unchanged, and the scenario switches to a stack last for that reason.

<details>
<summary>Details</summary>

## Changes

- `orders_apply.py`: `_mode` accepts every pair of distinct modes; `_reorder` applies the readiness order with chains kept; leaving a stack clears `stacked`.
- `declare/orders.py`: help text. `forge_stack.py`, new `forge_stack_gh.py`, `forge_stack_gitlab.py`, `declare/forge_stack.py`: the `unstack` action.
- Cards: `concepts.md`, `chief-of-staff.md`, `foreman.md` (a "mode switch" bullet by target), `driver.md` (`note rebase: mode <mode>`), `hosts/claude-code.md`.
- Docs: `README.md`, `docs/batch-modes-texts.md`, `docs/batch-modes.svg`, `docs/use-cases-foreman.md`.
- Tests: `tests/test_mode_switch.py` (refusals, record, order, `previous`, `stacked` cleared); scenario cases in the `series-deps`, `stack` and `gitlab` units, with `scenario/README.md` coverage markers.

## Human decisions

- To a stack: open PRs are stacked, each rebased on the one below, CRs not yet started join on top.
- To parallel: each open PR is rebased on the default branch and its gates run again.
- Order of a stack or series made by a switch: CRs already ready at the bottom in the order they became ready, then the others; chains kept.
- Merged CRs never change.

## Impacts

No visual change; the CLI prints one line per switch naming the new shape and what follows.

## Test plan

- [x] New or changed tests (they fail on the previous code): `tests/test_mode_switch.py`, scenario cases
- [x] Local gates at `e7eab41` (long gate passed at `0be062c`, carried by a clean rebase and green CI): `just check` (106 passed), long gate `just scenario` pass
- [x] Evidence: before at `33fc800` (switch refused), after at `e7eab41` (all pairs accepted)
- [x] Review: approved at `33fc800` for the round, committed as `e7eab41`
- [x] Verified at `e7eab41`
- [x] CI green at `e7eab41`

## Internal references

- CR-267 batch-mode-switch; archive work files under its folder.

</details>


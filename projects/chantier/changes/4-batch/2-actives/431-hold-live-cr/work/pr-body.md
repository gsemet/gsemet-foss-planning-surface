## Summary

`order hold` took only a CR handed back ready, in a stack. A CR waiting on the user (for instance a phone trial) kept a slot and its place in the stack for hours with no Driver at work. `order hold` now also takes a live (`working`) CR, in every batch mode (parallel, series, stack). The CR becomes `blocked` and held, its lease ends, its slot is free at once, and it leaves the stack and the series order together with the CRs that depend on it. Only the user's `order unhold` releases it; it then comes back on top and is taken back before any queued CR.

## Deliverables

What a held live CR does, by step:

| Step | Effect |
| --- | --- |
| `order hold <cr>` on a working CR | `blocked`, reason `held: order <O-n>`, lease ended, slot free, out of the stack and the order |
| CRs that depend on it | wait with it (out of order), keep their status and their base on its branch |
| `order unhold <cr>` | `blocked`, reason `unheld: order <O-m>`, on top (series: after the started CRs), dependents above it |
| `take <cr> --note "unhold: ..."` | taken back before any queued CR, no round counted |
| `take <release>` while a CR is held | refused, naming the held CRs |

Choices: one shared definition of "out of order" (apart or dependent) in `rails.py`, computed on each call and never stored; a series batch now records `start_on` at the take, so a successor already started on the held CR is a dependent; dropping a held CR that has dependents has their Drivers rebase to take its commits out.

**UNVERIFIED:** no screenshot of the pane from a real session (the step, phase, now and next texts of a held CR change what the pane draws).

## Blast radius

Grade: 2. The hold touches shared stack and series ordering code (`stacks.py`, `rails.py`) and the take and drop paths; revert is possible but the two predecessors' readers of `is_held` moved onto the shared helpers.

## Autonomous decisions

- The new status text lives in a new small module `status/now_next.py` to keep `status/views.py` under the file-size limit.
- The series out-of-draft refusal is tested at the command's own "is not a stack" refusal, since the command refuses non-stack batches.

## Known gaps

- No screenshot of the pane from a real session.
- The `hold_live` scenario case ran locally on Linux-style stack unit only; the pipeline job and a Windows run at the top of the stack remain.

<details>
<summary>Details</summary>

## Changes

- `rails.py`: `is_held`, `is_parked`, `apart`, `out_of_order`, `apart_owner`, the dependents' base rule, `series_predecessor` skipping out-of-order CRs, the release refusal while a CR is held.
- `stacks.py`, `stack_words.py`, `commands/delivery.py`, `commands/forge_stack_apart.py`: readers move to `out_of_order` / `apart`; the PR of a dependent is left out of the native stack.
- `commands/orders_hold.py`, `orders.py`, `orders_drop.py`, `orders_reorder.py`, `commands/driver.py`: hold and unhold of a working CR, pending order, drop with dependents, `handback` of a held CR refused, live holds kept when a batch leaves a stack.
- `status/words.py`, `status/views.py`, `status/now_next.py`: `Held` and `Unheld` step, phase and now/next texts.
- Cards (foreman, driver, chief-of-staff, concepts, routing), `scenario/` case `hold_live`, tests.

## Human decisions

- `order hold` is accepted on a live CR, in every mode, and only the user releases it.
- A series successor already started on the held CR waits with it.
- Dropping a held CR that has dependents has their Drivers rebase to take its commits out.

## Impacts

The CR board pane shows `Held` and `Unheld` for a held live CR.

## Test plan

- [ ] New or changed tests (they fail on the previous code): `test_hold_live*.py`, `test_stack_hold.py`, `test_came_back.py`
- [ ] Local gates at `<sha7>`: `just check`, `just eval-dry-run`
- [ ] Evidence: none beyond the tests and the scenario case
- [ ] Review: approved at `<sha7>`
- [ ] Verified at `<sha7>`
- [ ] CI green at `<sha7>`

## Internal references

CR-431 hold-live-cr (batch-30); shares a section with CR-430 park-live-cr.

</details>

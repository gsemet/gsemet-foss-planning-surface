Stacked on #208.

## Summary

Long gates cost hours between finished work and the user's merges: the PR the user waited for queued behind another gate, a rebased PR was pushed only after its gate, and a clean rebase onto a docs-only change ran the full gate again. Three default rules fix this: the next merge goes first in the gate queue, a PR that already exists is pushed early as a draft after a rebase, and a clean rebase carries the gate pass.

## Deliverables

- **Queue order** (stack and series batches): the CR the user merges next (first of the batch's order not merged or cancelled) goes ahead of gates marked `--first`, then arrival order. A running gate is never stopped. A parallel batch keeps the marked-then-arrival order.
- **Push early** (cards): after a rebase that needs a gate, a Driver turns an existing PR to draft, force-pushes with lease, ships `--draft`, then runs the gate and the CI watch side by side; it leaves draft once both pass at the same head.
- **Carry**: at `handback ready` with no gate pass at the head, the CLI proves from git (`git merge-tree --write-tree`, equal tree and commit count) that the head is the last passed head rebased cleanly, and accepts it, recording `gate_from`. A conflict, an added commit or a git older than 2.38 refuses with the reason.
- The eval kit's C7 check accepts a carried pass.

| | Before | After |
| --- | --- | --- |
| Gate queue (stack, series) | arrival order, or marked `--first` | next merge's gate, then marked `--first`, then arrival order |
| Rebased PR that exists | pushed after its gate | pushed at once as a draft, gate and CI side by side, ready when both pass at one head |
| Clean rebase at hand-back | a new long gate | the last pass carries (`gate_from`), CLI-proved by `git merge-tree` |
| Conflicted rebase | a new long gate | a new long gate, refused with "does not carry" otherwise |

## Blast radius

Grade: 2. The gate queue and the hand-back check are shared CLI code; revert is possible, with the cards to revert alongside.

## Autonomous decisions

- The next merge is read from the batch's record at each pass of the waiting loop, read-only; a missing or invalid record means no next merge.
- A gate head unknown to the repository counts as a replay that conflicts, so the gate runs.
- The CLI does not fetch the base: it uses the existing `origin/<base>` ref.
- The `gates` unit's scenario budget goes from 330 s to 400 s for the two added cases, set from one run of 421 s made under load (the measured columns are not refreshed).

## Known gaps

- Rule 2 lives in the cards only (as decided): no CLI refusal enforces it.
- The CLI reads no forge: CI at the new head after a carried pass is still the Driver's to read.

<details>
<summary>Details</summary>

## Changes

- `stacks.py` `next_merge`; `commands/gate_queue.py` three-step order; `commands/crs.py` carry check; `driver_checks.py`, `driver.py` (`gate_from`, printed line); `declare/gate.py` help.
- Cards: `concepts.md`, `driver.md`, `foreman.md`, `chief-of-staff.md`; `docs/gates.md`; `evals/kit/audit.py`, `evals/SCORECARD.md`.
- `gate_lock.py` docstring; `scenario/run_scenario.py` and `scenario/README.md` (the `gates` budget and coverage bullet).
- Tests: two scenario cases in the `gates` unit; `test_gate_queue_order.py`, `test_gate_carry.py`.

## Human decisions

- Rule 4 (the stack's one gate) is a separate change, after this one.
- In a parallel batch no order is automatic: the Foreman moves a gate first on the user's word.

## Impacts

Users see the next merge's gate run first and fewer repeated gates after a clean rebase.

## Test plan

- [x] New or changed tests (they fail on the previous code)
- [x] Local gates at `b9f20b6`: `just check` pass; `just scenario` pass
- [x] Evidence: none, no visible change
- [x] Review: approved at `b9f20b6`
- [x] Verified at `b9f20b6`
- [x] CI green at `b9f20b6`: all five jobs pass

## Internal references

CR-265 gate-rules.

</details>

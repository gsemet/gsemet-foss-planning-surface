## Summary

A pull request that targets the default branch and is out of draft can carry, under its own commits, the commits of another change of the same batch. Merging it then merges that other change too, and dissolves a partial stack. `ship` now refuses to record such a PR, and the cards tell the Driver to put the PR back to draft first, and tell the user which single PR to merge.

## Deliverables

`ship` refuses before recording anything, when the PR is on the default branch, out of draft, and its head carries another change's head that is not recorded merged:

```
ship <cr> <pr>
  read_state(pr) -> base, draft
  base == default branch and draft is False
    -> _foreign_crs(...) non-empty -> refuse (exit: precondition), nothing recorded
  otherwise record as before
```

- A draft PR, a PR on another change's branch, a failed forge read and a change recorded merged are never refused.
- The refusal text names the first step: put the PR back to draft, `ship` again, then rebase if needed.
- The stack-ready-to-merge ask now names the one PR to merge (`merge <cr> <link>`).

## Blast radius

Grade: 1

`ship` gains one refusal for a narrow case; a `git revert` restores the previous behaviour.

## Autonomous decisions

- The refusal text lives in a small helper because `ship` hit the project's function-length cap.

## Known gaps

None

<details>
<summary>Details</summary>

## Changes

- `delivery.py`: `_foreign_crs` (read-only git, reuses the existing ancestor check) and the refusal in `ship`, before the record is written.
- `driver.md`, `foreman.md`, `chief-of-staff.md`: the draft-first step, the `merge <cr> <link>` part of the asks, and what the user is told to merge.
- `test_carry_ship.py`: one parametrized test of four cases.
- `scenario/run_scenario.py`: a series CR's PR is opened or retargeted on the branch of the CR under it (a `base` parameter on `ship` and `driver_round`, `forge_base` in the restack steps), so the steps follow the real flow under the new refusal.

## Impacts

No visual change.

## Test plan

- [x] New or changed tests (they fail on the previous code): parametrized `ship` test, four cases
- [x] Local gates at `76a19a4`: `just check` pass (569 tests), `just eval-dry-run` pass, full local scenario pass
- [x] Evidence: none (CLI refusal covered by the test)
- [x] Review: approved at `76a19a4` (round 1 judged at `4bde985`, scenario change judged at `76a19a4`)
- [x] Verified at `76a19a4`
- [x] CI green at `76a19a4` (all five jobs)

## Internal references

- CR-346 ship-refuses-foreign-commits

</details>

## Summary

A Driver could push a branch whose fast gate or whose project-named pre-push check had not run at the rebased head, and the failure then showed up in CI or in the Verifier, costing a round. The Driver's card now asks for those checks before the first push, and the Coder's prompt carries the specification's file edits as a checklist so that missing edits are visible before review.

## Deliverables

Before and after, for a Driver's path to the first push:

| | Before | After |
| --- | --- | --- |
| Order | rebase, long gate, push | rebase, fast gate again plus the rules' pre-push checks, long gate, push |
| Failure of those checks | found in CI or by the Verifier | a round, before the push |
| Coder's brief | one-line note | one-line note plus a checklist of the specification's file edits, marked `done` or `open: <why>` in `r<n>.md` |

Choices made:

- The card names no project command; the project's `AGENTS.md` says which checks run. chantier's own `AGENTS.md` names `just check`, and `just eval-dry-run` for a change under the CLI's `src/` or the eval kit.
- It is not a third gate: the long gate and `chantier gate` are unchanged, and the checks run as short gates, one command per call.
- The checklist goes in the Coder's prompt only; the `round --note` stays a one-line brief.

## Blast radius

Grade: 1

Documentation and card text only; no code path changes. A plain `git revert` restores the previous behaviour.

## Autonomous decisions

- The new `AGENTS.md` bullet sits beside the existing `just check` bullet rather than replacing it, to keep "before you hand back" and the three-system requirement as they were.

## Known gaps

- The rule is not yet tested in a real batch: a Driver of a CR under the CLI's `src/` should run `just check` and `just eval-dry-run` before its first push, its log should show the note, and a red result should be a round before the push.

<details>
<summary>Details</summary>

## Changes

- `skills/chantier/references/driver.md`: new "Before the first push" bullet in "Your means"; the "CR driver" sequence places the step after the rebase and before the long gate and the push (also in the `ci: beside the long gate` variant); the Coder's checklist rule at the reading rule and at the round step.
- `skills/chantier/references/coder.md`: `r<n>.md` marks each checklist item `done` or `open: <why>`.
- `docs/gates.md` and `skills/chantier/references/init.md`: the fast gate also runs before the first push; a project may name an extra pre-push check.
- `AGENTS.md` and `CONTRIBUTING.md`: `just check` before the first push; `just eval-dry-run` for a change under the CLI's `src/` or `evals/kit/`, not for a cards-only change.

## Human decisions

- The Driver's card names no project command; the project's `AGENTS.md` says which pre-push checks run, and chantier's own names `just check` and `just eval-dry-run`.
- The checklist covers every file edit the specification lists, not only card edits, so it also serves projects with no cards.
- `just eval-dry-run` is owed for a change under the CLI's `src/` or the eval kit, and not for a cards-only change.
- The checks come before the first push only; later pushes are out of scope.

## Impacts

No visual change. Drivers run one more short check before the first push when the project names one.

## Test plan

- [ ] New or changed tests: No behaviour change
- [x] Local gates at `carried from 54cd5a4`: `just check` pass; `just eval-dry-run` 17 of 17 cases as expected
- [ ] Evidence: none, cards and docs only
- [x] Review: approved at `carried from 54cd5a4`
- [x] Verified at `carried from 54cd5a4`
- [x] CI green at `carried from 54cd5a4`

## Internal references

- CR-330 driver-checks-before-first-push

</details>

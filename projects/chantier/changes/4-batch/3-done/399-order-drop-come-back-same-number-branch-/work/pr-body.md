## Summary

A change request (CR) that `order drop` sent out of a batch to the inbox or the backlog leaves a `formerly.json` file in its folder (its number, branch, worktree and PR). It used to come back as a brand-new CR: a new number, a fresh branch, a new PR. Now, when its folder joins a batch again, it gets its own number back, and its Driver picks up its branch and its PR (rebased on the new base). It starts fresh only when its branch no longer exists locally.

## Deliverables

The folder's `formerly.json` (written by `order drop`) is read by the one function every join goes through, so `open`, `order add`, a factory's `triage --ready`, the fix CR and the release CR all behave the same.

| Case | Number | Branch and PR | Join line |
| --- | --- | --- | --- |
| Another batch, branch exists | the former number | the former branch, worktree, PR | `CR-n joins with its branch <b> and PR <link>` (or `and no PR`) |
| Same batch, cancelled entry | same entry reopened, counters reset, notes and cost kept | as above | as above |
| Branch gone | the former number | usual fresh names, PR unset | `CR-n joins fresh: its branch <b> is gone[; its former PR <link> is left as it is]` |

`formerly.json` is deleted once the record holds the CR again; a refusal (malformed file, or a live CR with that number) leaves the folder and the file in place.

## Blast radius

Grade: 2 - the shared join path of every CR changes (moved into `commands/joining.py` and `commands/came_back.py`); a CR with no `formerly.json` takes today's path. Revert restores the previous behaviour.

## Autonomous decisions

- The join code moved out of `opening.py` into `joining.py` and `came_back.py` to stay within the file and function size limits.
- The deletion of `formerly.json` goes through a new `Batch.consume()` run just before `batch.json` is written, so a later refusal keeps the file.

## Known gaps

- A branch left only on the remote counts as gone (no fetch of it).
- The PR-side rules for a closed or merged PR are card rules, not exercised by a real forge in the tests.

<details>
<summary>Details</summary>

## Changes

- `commands/came_back.py`: reads and validates `formerly.json`, the clash and reopen rules, the branch rule.
- `commands/joining.py`: `add_cr`, `join_cr`, `new_entry`; `orders_apply.py` and `orders_release.py` import from it.
- `core/batch.py`: `Batch.consume()`.
- Cards: `driver.md` (use the recorded branch, read the PR, reopen a closed one, never open a second PR), `chief-of-staff.md` (a moved-out CR merged later: `order add` then `order merged`), `concepts.md` (lifecycle line).
- Tests and a scenario step that adds a dropped CR back.
- `driver.md` is tightened (wording only) so the CR Driver's reading stays within its size budget.

## Human decisions

- A dropped CR gets the same number back and is never given to another CR.
- Its branch and PR are picked up and rebased on the new base; it starts fresh only when its branch is gone.
- Rejoining its own batch reopens its cancelled entry, resetting every per-round and stack field.
- A closed PR is reopened before any push to its branch; a second PR is never opened.
- A moved-out CR whose PR the user merges later is recorded with `order add`, then `order merged`.

## Impacts

No visual change. A restored CR keeps its number and PR.

## Test plan

- [x] New or changed tests (they fail on the previous code)
- [x] Local gates: `just check` pass at 783329d; `just eval-dry-run` pass at 524b899 (carried from 75b7a18, patch unchanged by the rebase)
- [x] Evidence: none (no visible change)
- [x] Review: approved at 783329d (code carried from 75b7a18; the card trim committed as 783329d)
- [x] Verified at 783329d
- [x] CI green at 783329d

## Internal references

CR-399 order-drop-come-back-same-number-branch-; depends on CR-397.

</details>

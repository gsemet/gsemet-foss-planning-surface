## Summary

Taking a change request out of a batch used to have one exit, `order drop`, which always sent it to `6-trash/`. A change request that was only postponed ended in the trash, needed a `restore` and a `triage` to reach the backlog, and lost its number on the way. `order drop` now names where the change request goes: the trash (cancelled), the inbox (to look at again) or a backlog priority `P1` to `P4` (postponed or handed off). Whatever the destination, its work (worktree, branch, open PR) is kept, and its PR is closed only for the trash.

## Deliverables

`order drop <cr> --note trash|inbox|P1|P2|P3|P4` is required (no default; the CLI never chooses), and the folder lands in the matching place:

| `--note` | Folder | Work and PR | Number |
| --- | --- | --- | --- |
| `trash` | `6-trash/<date>-<number>-<slug>/` | PR closed | as before |
| `inbox` | `1-inbox/<number>-<slug>/` | kept, PR to draft on the default branch | reserved |
| `P1`..`P4` | `2-backlog/P<n>/<number>-<slug>/` | kept, PR to draft on the default branch | reserved |

- A moved folder carries `formerly.json` (where it came from: change request, batch, branch, worktree, PR, draft state) and a `formerly` line in its intro file, and its number is written to `restored.json` so no other change request is given it.
- A release or fix change request leaves only to the trash.
- `STATUS.md`, `STATUS.json` and the board read `dropped` for the trash and `dropped to 2-backlog/P2` (or `1-inbox`) otherwise; `close` lists trashed work for removal and, on a line of its own, the work moved out and kept.
- The forge stack leaves a moved-out PR out and retargets it to the default branch, apart from trashed PRs, which stay "close it".

Before (base `9ff16d5`) and after (head `a872a66`), in a scratch repository:

| Call | Before | After |
| --- | --- | --- |
| `order drop <cr>` | goes to `6-trash/` | exit 1, nothing recorded (no destination) |
| `order drop <cr> --note P2` | goes to `6-trash/` (`P2` ignored) | `dropped <cr> to 2-backlog/P2: 2-backlog/P2/<number>-<slug>` |
| label in `STATUS.md` | `[dropped]` | `[dropped to 2-backlog/P2]`, `[dropped to 1-inbox]` or `[dropped]` (trash) |

## Blast radius

Grade: 2

`order drop` now refuses a call without a destination, `cancel` follows the recorded destination, and `close`, the batch record, status labels and the forge stack read the new `left_to` field. A cancelled record without it reads as trash, so older batches behave as before. Revert restores the single-exit behaviour; folders already moved would stay where they are.

## Autonomous decisions

- The move-out code lives in `lifecycle/moveout.py` and the drop handler in `commands/orders_drop.py`, because the existing files were at their line limits.
- `cancel` refuses to move a folder twice, since a drop to the inbox or backlog already placed it.
- A drop of a live change request stays a pending order until `order done`, and the batch pause waits for it, as today; the scenario's `cancel` calls therefore go through a helper that drops, marks the order done, then cancels.
- The allow-rule table in `references/hosts/claude-code.md` gained the four close and reopen patterns, because a test ties it to the CLI's sample list.
- `cr-folder-lifecycle.svg` has a wider trash box and `cr-lifecycle-simple.svg` a two-line footer, so the longer label fits.

## Known gaps

- No screenshot of the pane from a real session: the status label the board pane draws changes, and the project asks for one captioned with the head's SHA.
- Coming back under the same number with the branch and the PR is a separate change; until then a moved-out folder that joins a batch gets a new number.

<details>
<summary>Details</summary>

## Changes

- `commands/intake.py`, `commands/opening.py`: `cr_slug`, `folder_taken` and `remember_cr` are shared by the move-out code.
- `core/records.py`: new optional `left_to` field on a change request's record.
- `declare/orders.py`, `commands/orders.py`, `commands/orders_drop.py`, `commands/orders_apply.py`: the destination is parsed, checked (usage refusal, release and fix rule, name clash, held change request, second drop) and recorded; the order line carries the folder and, for a trash drop outside a stack with a PR, `; close its PR <link>`.
- `lifecycle/moveout.py`, `lifecycle/stages.py`, `commands/release.py`: the move to inbox or backlog with `formerly.json`, the `formerly` line and the number reservation; `cancel` follows the recorded destination and refuses with none.
- `commands/closing.py`, `history.py`, `status/write.py`, `status/words.py`, `lifecycle/layout_check.py`: removal and kept lines, `"to"` in the batch record, no final pages in the backlog, the new label, `formerly.json` in the folder layout.
- `commands/forge_stack*.py`: moved-out PRs apart from trashed ones, their retarget on GitHub and GitLab.
- `commands/permissions.py`: `gh pr close`/`reopen`, `glab mr close`/`reopen` allow rules.
- Cards (`chief-of-staff.md`, `foreman.md`, `driver.md`, `concepts.md`), docs, the three lifecycle SVGs, eval texts and the scenario.

## Human decisions

- The destination is asked of the user and never chosen: trash for cancelled work, backlog for postponed or delegated work.
- The work is kept for every destination; the PR is closed only for the trash.
- A moved-out change request keeps its number, and no other is given it.
- A release or fix change request can only be trashed.
- Close and reopen join the recommended allow rules.
- Coming back under the same number is split into its own change.

## Impacts

Users and the steering session now say where a dropped change request goes; backlog items keep their numbers. The status label gains a destination. No other visual change.

## Test plan

- [x] New or changed tests (they fail on the previous code): `test_order_drop_to.py`, `test_forge_moved.py`, plus a conftest fixture that resets the global project between tests
- [x] Local gates at `a872a66`: `just check` (977 passed), `just eval-dry-run` (18 of 18)
- [x] Evidence: before at `9ff16d5`, after at `a872a66`
- [x] Review: approved at `682e37d` plus the test-only round committed as `a872a66`
- [x] Verified at `a872a66`
- [x] CI green at `a872a66`: `gh pr checks 370`, all 5 jobs pass (check on 3 systems, eval-dry-run, scenario)

## Internal references

CR-397 order-drop-asks-where-the-cr-goes-trash (batch-29, stacked on CR-396).

</details>

# Report — stress-alert-dropdown-flake

Status: **done** (2026-11-05, branch `change-requests/259-stress-alert-dropdown-flake`, PR #316, merge commit `e1d15d57`).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | Redo proof, later removed: it hid the bug | `604885eb` |
| T1 | A new preview's group stays out of the last one's unlock | `c70bcec7` |
| T1 | Unlock the groups open when a preview closed (restored previews) | `e1d15d57` |

## Proof of completion

- Cause: the unlock of a closed preview matched by column, and took a new preview's empty group.
- Unit tests in `test/host-vscode/groupFocus.test.ts`; `just check` passed.
- Three heavy runs at `7612009d` on the branch: 41925610108, 41925614481, 41925619047 (60 stress
  rounds, 3 `integration`, all green). The first fix passed stress and failed `integration`.
- Main runs 42031927810, 42038757461 and 42086410139 are green with this fix.
- The link with the focus command rests on the 1 s timing and the code: the command was not logged.
- `just preflight` did not finish on the Mac: the VS Code test window never became active.

## Open items

None.

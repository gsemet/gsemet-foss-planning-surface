# Report — find-and-replace-in-preview

Status: **done** (2026-10-28, branch `change-requests/144-find-and-replace-in-preview`, PR #152, merge commit 2992b50a).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | feat: find and replace in the preview | 2992b50a |

## Proof of completion

- Merged by the user with normal CI green after a rebase on main f7b17518 (okfreq 0.16). Round 3 added a `find` command and a Ctrl/Cmd+F keybinding for the find bar focus.
- Heavy integration not re-run after the last rebase; main's heavy is red on `tableMoves` since CR 143 (hotfix CR 153).

## Open items

- Find-bar focus in a real window is proven only by the round-3 CI run; re-check on main's next green heavy run.

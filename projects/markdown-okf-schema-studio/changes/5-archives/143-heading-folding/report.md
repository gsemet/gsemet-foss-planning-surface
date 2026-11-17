# Report — heading-folding

Status: **done** (2026-10-28, branch `change-requests/143-heading-folding`, PR #151, merge commit f7b17518).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | feat(preview): fold and unfold sections under headings | f7b17518 |

## Proof of completion

- Merged by the user after a rebase on main bc15ce75 (okfreq 0.16), normal CI green.
- Heavy integration had failed `tableMoves` column drop zone on the older bases (runs 40640639724, 40656120188); the user merged it with normal CI green.

## Open items

- Heavy `tableMoves` column drop zone: re-check on main's next heavy run; CR 147 (#155) fails the same assertion (shared 6th toolbar-button hypothesis).

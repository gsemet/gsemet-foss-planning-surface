# Report — 290-label-popover-covers-table

Status: **done** (2026-11-11, branch `change-requests/290-label-popover-covers-table`, PR #358, merge commit `5725fa15`; no GitHub issue). Merged by the owner in one whole-stack merge.

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | The label rename popover opens above a table's anchor icon instead of under the floating toolbar | `5725fa15` |

## Proof of completion

- 2 round(s). Opus Inspector approved each round; a fresh Verifier returned VERIFIED at the final head (restacked on `origin/main` 2eb4a473); `just check` passed; heavy CI (visual, integration, stress) green at the merged head.

## Open items

- The remote branch `change-requests/290-label-popover-covers-table` is left for the owner to delete; its `-assets` branch is kept.
- CI integration logs print no scenario names for the default real-input sequence, so the new real-input scenario rests on a green real-input step, not a named pass.

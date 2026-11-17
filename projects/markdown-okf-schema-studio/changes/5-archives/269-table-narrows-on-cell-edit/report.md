# Report — 269-table-narrows-on-cell-edit

Status: **done** (2026-11-10, branch `change-requests/269-table-narrows-on-cell-edit`, PR #338, merge commit `293366d0`).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | A wide table in Auto width mode keeps its breakout while a table cell is edited (a cell editor is told apart from a source editor in `eligibleWrappers`); approved StRS change with the owner's recorded agreement, SwRS updates, requirements log, CHANGELOG line | `293366d0` |

## Proof of completion

- Three rounds: round 1 FIX-REQUIRED, round 2 APPROVE with two wording fixes, round 3 wording only. Inspector on Opus (blast radius 2).
- PR run green (static, static-windows, visual, checks) at head `8138116c`; heavy run 42824305608: static, static-windows, visual and integration passed; the advisory `stress` job was still running when the owner merged.
- Local `just check` passed per the coder; `just e2e` and `just preflight` not run locally (they need an unlocked screen).

## Open items

- GitHub could not request the owner's review (the owner is the PR author); the PR body says so.
- Known issue kept in SwRS LAYOUT-023: the width mode returning to Auto while a cell editor is open measures the table with the editor in place.

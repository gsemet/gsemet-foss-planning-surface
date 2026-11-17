# Report — highlight-table-row-on-hover

Status: **done** (2026-11-05, branch `change-requests/260-highlight-table-row-on-hover`, PR #317, merge commit `363e56ec`).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | Table headings, even rows and the hovered row are tinted | `363e56ec` |

## Proof of completion

- `test/visual/capture_table_row_colours.py`, with a real pointer; SwRS-MDOKFSTUDIO-CORE-077.
- Main run 42038757461 at `363e56ec`: `checks`, `integration` and `stress` green.
- `just preflight` did not finish on the Mac: the VS Code test window never became active.

## Open items

- README images were not regenerated with the new table colours.

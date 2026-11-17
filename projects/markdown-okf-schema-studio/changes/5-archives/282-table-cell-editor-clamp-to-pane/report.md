# Report — 282-table-cell-editor-clamp-to-pane

Status: **done** (2026-11-11, branch `change-requests/282-table-cell-editor-clamp-to-pane`, PR #351, merge commit `48a81d08`; no GitHub issue).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | The table cell editor is clamped to a narrow pane, so the field and buttons no longer run past the pane's right edge | `48a81d08` |

## Proof of completion

- Heavy CI run 42987003647 at head `ae4bf3ec` concluded success, stress included.
- Light-only before/after screenshots (280 px pane, scenario `table-editing/v29-cell-editor-clamped-light-280`) on branch `change-requests/282-table-cell-editor-clamp-to-pane-assets`.
- The Chantier repository was not touched.

## Open items

- Remote branches `change-requests/282-table-cell-editor-clamp-to-pane` and its `-assets` branch are left for the owner to delete.

# QA-03 — Screenshots are captured but nothing checks them

| Field | Value |
| --- | --- |
| Severity | Medium (process gap) |
| Confidence | Observed in the campaign layout (`test/visual/screenshots/*.png` + `.txt` notes) |
| Area | Visual review |

## Observed

The E2E campaign produces about 100 screenshots, each with a TXT note listing the expected content
and visual checks. Today only a human reads them. Several bugs in this report are visible on a
single screenshot and would be caught by a reviewer that reads the note's checklist:
[UX-14](../02-table-editing/UX-14-table-toolbar-covers-content.md) (toolbar covers a row),
[UX-20](../03-frontmatter-editing/UX-20-row-menu-overlaps-and-clipped-tooltips.md) (menu covers
values, clipped tooltip), [UX-15](../02-table-editing/UX-15-wide-table-layout.md) (wrapped ids),
[UX-26](../05-preview-lifecycle/UX-26-status-page-text-and-stale-naming.md) (glued status text).

## Suggested change

1. Make each TXT note machine-checkable: a short list of yes/no visual assertions
   ("No floating control overlaps text of another row", "All tooltips fully visible",
   "Identifiers are not split across lines").
2. Add an agent review step (multimodal model) that reads each image and its assertions and writes
   `review.json` with pass/fail and a one-line justification per assertion; failures become
   findings with the image attached.
3. Complement with cheap DOM geometry checks in the capture script: overlapping bounding boxes
   between floating menus and text nodes, elements clipped by the viewport, and text nodes whose
   `getClientRects().length > 1` for short identifiers.

## Done when

A screenshot campaign ends with a pass/fail summary, and a human only looks at failures.

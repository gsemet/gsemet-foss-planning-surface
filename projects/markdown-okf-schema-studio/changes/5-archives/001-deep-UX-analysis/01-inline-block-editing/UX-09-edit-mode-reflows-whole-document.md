# UX-09 — Turning edit mode on reflows every paragraph with source line breaks

| Field | Value |
| --- | --- |
| Severity | Low |
| Confidence | Observed |
| Area | Edit mode |
| Evidence | [u05-click-paragraph.jpg](../evidence/u05-click-paragraph.jpg) (paragraphs show hard-wrapped source lines) |

## Use case

An author reads a chapter, toggles edit mode to fix one word, and expects the page to stay as it
was.

## Observed

All paragraphs switch to `white-space: pre-wrap`, so every soft line break of the source becomes
visible. The book wraps source lines at clause boundaries (100-character rule), so paragraphs turn
into ragged short lines ("…the **emerging features** / that these / machines provides…"). The
document grows and the reading position shifts. The rendered page no longer matches any export
format, so edit mode stops being a preview.

## Expected

Rendered paragraphs keep their normal flow in edit mode; only the block being edited shows raw
source.

## Where it comes from

`src/preview/previewStyles.ts` L356-L359:
`html[data-sphinx-preview-edit-mode="on"] … p[data-sphinx-source-line] { white-space: pre-wrap; }`.

## Suggested direction

Drop the rule, or scope it to the edited block. If the intent is to help line-level mapping, keep
it behind a setting.

## Done when

Toggling edit mode does not change the layout of blocks that are not being edited.

# UX-34 — The sticky heading band shows raw `#` markers in the rendered view

| Field | Value |
| --- | --- |
| Severity | Low |
| Confidence | Observed |
| Area | Sticky headings |
| Evidence | [u02-scroll-preview.jpg](../../evidence/u02-scroll-preview.jpg) |

## Observed

The sticky band at the top of the preview reads "# Foundations / ## Definitions / ### LLM": the
rendered preview shows Markdown syntax, which mirrors the editor's sticky scroll but looks like a
rendering bug in a WYSIWYG context. The band also uses three full-size lines (about 75 px) of a 540 px
preview, and the floating toolbar overlaps its right side.

## Suggested direction

Render the band as a breadcrumb ("Foundations › Definitions › LLM") on one line by default, keep the
hash style as an option, and reserve space so the toolbar does not overlap it.

## Done when

The band shows heading text only and takes one line by default.

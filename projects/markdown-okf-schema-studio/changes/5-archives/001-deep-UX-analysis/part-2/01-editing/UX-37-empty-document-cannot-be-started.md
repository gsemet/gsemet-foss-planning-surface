# UX-37 — An empty document cannot be started from the Studio editor

| Field | Value |
| --- | --- |
| Severity | Medium |
| Confidence | Reproduced |
| Area | Authoring in the Open With editor |
| Evidence | [p2-empty-edit.jpg](../evidence/p2-empty-edit.jpg) |
| Related | Extends [UX-10](../../01-inline-block-editing/UX-10-no-way-to-insert-a-block.md) |

## Steps to reproduce

1. Create or open an empty Markdown file (`synth/empty.md`).
2. **Reopen Editor With… → Markdown OKF-Schema Studio**, toggle edit mode, click in the page.

## Observed

The page is completely blank (no title, no placeholder, no hint). With edit mode on, clicking
anywhere does nothing because there is no mapped block. The only way forward is to reopen the file
in the text editor.

## Expected

An empty document shows a placeholder ("Empty document — click to start writing", or a short
template picker: heading, OKF frontmatter from the matching schema) that opens an inline editor
at line 1.

## Done when

A user can create a document from an empty file without leaving the Studio editor.

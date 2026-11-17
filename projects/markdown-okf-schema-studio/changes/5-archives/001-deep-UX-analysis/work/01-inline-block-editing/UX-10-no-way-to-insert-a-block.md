# UX-10 — There is no way to insert a new block or section from the preview

| Field | Value |
| --- | --- |
| Severity | Medium |
| Confidence | Observed (workaround verified) |
| Area | Authoring from the preview / Open With editor |
| Evidence | [r2-ce-section-committed.jpg](../../evidence/r2-ce-section-committed.jpg) |

## Use case

An author working only in the Studio editor wants to write a new section ("## Incident review
checklist" with a paragraph, a list, and a tip) between two existing sections or at the end.

## Observed

Edit mode only edits existing blocks. The only way to add content is to open an existing
neighbouring block and type raw Markdown after it (`\n\n## New section\n\n…`). This works (the
section rendered correctly after blur), but:

- nothing in the UI suggests it;
- the new content is typed into a textarea that still claims to be the previous block;
- there is no "insert paragraph/heading/list/admonition/table/figure below" affordance, no slash
  command, and no empty-document entry point (an empty file has no block to click).

Moving a section (cut/paste between distant blocks) has the same limitation: there is no block
drag handle or move action.

## Expected

At least an "insert below" affordance between blocks (hover `+` or a keyboard command) that opens
an empty inline editor at the right source position, plus a way to start writing in an empty
document.

## Suggested direction

Render insertion points between top-level mapped blocks in edit mode. Clicking one opens an empty
textarea mapped to a zero-length source range at the boundary line; saving inserts the text
surrounded by blank lines. A small template menu (heading, list, admonition, table, figure) is a
natural follow-up.

## Test to add

E2E: in an empty Markdown file opened with the Studio editor, create a heading and a paragraph
using only the preview; assert the source.

## Done when

A document can be written from scratch in the Studio editor without typing into another block.

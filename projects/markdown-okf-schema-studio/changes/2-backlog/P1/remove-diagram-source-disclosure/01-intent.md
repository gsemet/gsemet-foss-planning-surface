# Remove the "Diagram source" disclosure under diagrams

## Intent

A reader no longer sees the collapsed **Diagram source** disclosure under a diagram, in the preview
or in the HTML export: the owner finds it useless, and a reader who wants the source reads the raw
Markdown.

## Decided (owner, 2026-11-27)

- Priority P1.
- The HTML export removes it too (`02-answers.md`).

## To grill

- **Chart source**, still shown (closed) in the HTML export: is it removed too.
- A diagram that fails to render: does its source stay visible.

The code and requirement facts are in `intake/request.md` and `02-answers.md`.

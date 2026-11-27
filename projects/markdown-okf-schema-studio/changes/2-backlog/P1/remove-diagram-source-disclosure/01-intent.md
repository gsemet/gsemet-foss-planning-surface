# Remove the source panels under diagrams and charts

## Intent

A reader no longer sees the collapsed **Diagram source** panel under a diagram, nor the **Chart
source** panel under a chart, in the preview or in the HTML export: the owner finds them useless,
and a reader who wants the source reads the raw Markdown.

## Decided (owner, 2026-11-27)

- Priority P1.
- The HTML export removes **Diagram source** too (`02-answers.md`).
- The HTML export removes **Chart source** too (`02-answers.md`); the preview already hides it.

## To grill

- A diagram or chart that fails to render: does its source stay visible.

The code and requirement facts are in `intake/request.md` and `02-answers.md`; requirement
SwRS DIAG-121, which shows **Chart source** in the export, changes with the others.

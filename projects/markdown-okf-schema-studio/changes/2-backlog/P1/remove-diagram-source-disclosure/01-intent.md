# Remove the source panels under diagrams and charts

## Intent

A reader no longer sees the collapsed **Diagram source** panel under a diagram, nor the **Chart
source** panel under a chart, when the figure renders: the owner finds them useless, and a reader
who wants the source reads the raw Markdown. The panel appears only when the render fails.

## Decided (owner, 2026-11-27)

- Priority P1.
- The HTML export removes **Diagram source** too (`02-answers.md`).
- The HTML export removes **Chart source** too (`02-answers.md`); the preview already hides it.
- A diagram or chart that fails to render keeps its source (`02-answers.md`).
- A failed chart in the preview shows its source too: the same rule in the preview and the export,
  for diagrams and charts (`02-answers.md`).

## To grill

Nothing open.

The code and requirement facts are in `intake/request.md` and `02-answers.md`; requirements
SwRS DIAG-121 (**Chart source** in the export) and DIAG-123 (a failed chart in the preview) change
with the others.

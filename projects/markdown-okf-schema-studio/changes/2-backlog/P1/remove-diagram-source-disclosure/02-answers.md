# Answers

## 2026-11-27: the HTML export too

Open question: which surfaces, the preview only (as for **Chart source** since 1.13.0) or the HTML
export too.

The owner's words, in French:

> « oui pareil en export html. si on veut voir le source on regarde le md en brut. il y en a d
> autres de similaire  de choses comme ca ? »

Decided: **Diagram source** is removed from the HTML export as well as from the preview. Reason: a
reader who wants the source reads the raw Markdown.

## 2026-11-27: **Chart source** leaves the HTML export too

Question: « Retirer aussi « Chart source » de l'export HTML dans ce CR ? » The owner's answer, in
French:

> « Oui, aussi »

Decided: this change also removes **Chart source** from the HTML export, for the same reason. No
generated source panel is left, in the preview or in the export. It supersedes the "not decided"
note on **Chart source** below.

## Similar panels (facts read in the code at `b9b29c5a`, not decisions)

- The extension generates three source panels, all in `normalizeDiagram`
  (`src/core/render/mystNormalize.ts`): **Diagram source** under Mermaid and PlantUML figures, and
  **Chart source** under Vega and Vega-Lite charts.
- **Chart source** is hidden in the preview since 1.13.0 and still shown, closed, in the HTML export
  (SwRS DIAG-121). Whether this change removes it from the export too is not decided.
- **Show the parser error** and **Show the error** show the reason of a rendering failure, not the
  source.
- The closed properties section of the export shows the front matter, not a copy of the source.
  Collapsible sections the document author writes are content.

# UX-36 — Editing a diagram or an equation hides it: no live preview while typing

| Field | Value |
| --- | --- |
| Severity | Medium |
| Confidence | Observed |
| Area | Inline editing of Mermaid, math, and other rendered blocks |
| Evidence | [dg-0-preview-only.jpg](../evidence/dg-0-preview-only.jpg) |

## Use case

An author tweaks a Mermaid flowchart or a display equation from the preview and wants to see the
result as they type, the way the side preview behaves when editing in the source editor.

## Observed

- Click-to-edit maps correctly: a diagram opens its full fence, a `$$` block opens its source, an
  inline equation opens its paragraph.
- While the textarea is open, the rendered diagram/equation is hidden
  (`[data-sphinx-preview-editing="true"] { display: none }`) and nothing is re-rendered until the
  editor closes. Authors edit diagram syntax blind; a syntax error is discovered only after
  leaving the editor.
- In edit mode, clicking the "Diagram source" disclosure opens the inline editor instead of
  expanding the disclosure, so the read-only source view is unreachable in edit mode.

## Suggested direction

For rendered blocks (Mermaid, math, PlantUML, figures), show the editor next to (or above) a live
rendering of the textarea content, re-rendered on a short debounce in the webview (Mermaid and
KaTeX already run there). Exclude `summary` elements from click-to-edit.

## Done when

Editing a diagram shows the updated rendering, or the error, within a second, without leaving the
editor.

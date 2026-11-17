# Backlog (P3): Mermaid labels as SVG text (`htmlLabels: false`)?

## Context

Mermaid sizes an HTML label box from text it measures once. If the webview then draws the text wider
(a font or zoom difference), the end of the label is cut. Drawing labels as SVG text
(`htmlLabels: false`) removes that whole class of clipping. CR 178 tried it; the owner kept the
current behaviour for now (2026-10-29) and shipped only the wait for fonts before the first render.

## Keep HTML labels (current)

Pros:

- Mermaid's default, so diagrams look the same as on GitHub and mermaid.live.
- Raw HTML in labels (`<b>`, `<br>`, `<i>`) and Font Awesome `fa:` icons keep working.
- Long labels wrap automatically inside the node.
- No visible change for existing documents.

Cons:

- Labels can still be cut when the measured and drawn widths differ (fonts not loaded yet, a font
  fallback, the webview zoom).
- The fonts wait reduces the problem but does not remove it.

## Switch to SVG text

Pros:

- The text and its box are measured by the same engine, so labels are never cut.
- Sharper at any zoom.
- PNG/PDF export and screenshots are more reliable.
- No `foreignObject`, which some SVG consumers do not render.

Cons:

- HTML in labels and `fa:` icons show as plain text, which breaks existing documents that use them.
- Poorer wrapping: long labels need an explicit `<br>` or the markdown-string syntax.
- The result looks different from GitHub's rendering of the same diagram.

## Possible middle ground

SVG text only for diagrams with no HTML and no `fa:` in their labels, or a user setting.

## Decision

Owner, later.

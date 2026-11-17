# UX-44 — The floating toolbar overlaps content and the find widget

| Field | Value |
| --- | --- |
| Severity | Low |
| Confidence | Observed in four states |
| Area | Preview chrome |
| Evidence | [p2-smoke.jpg](../evidence/p2-smoke.jpg), [p2-find-next.jpg](../evidence/p2-find-next.jpg), [p2-narrow.jpg](../evidence/p2-narrow.jpg) |

## Observed

- At the top of a document, the toolbar covers the end of the H1 ("Diagrams and math while
  typing": the title wraps under the buttons).
- It covers the properties table header and its error counter at narrow widths
  ([UX-43](UX-43-narrow-preview-layout.md)).
- VS Code's find widget (Cmd+F in the preview, which works and highlights matches) opens on top of
  the toolbar; both stay visible and overlap.
- Scrolling caused by find ("next match") does not move the source editor; scroll sync reacts
  only to user wheel scrolls.

## Suggested direction

Give the toolbar a reserved lane (for example inside the sticky band, which already spans the top)
or auto-hide it on scroll; move it below the find widget when the widget is open; treat find
navigation as a preview-owned scroll for synchronization.

## Done when

No text is ever hidden under the toolbar.

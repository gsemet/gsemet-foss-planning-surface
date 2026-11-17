# UX-45 — The preview's white theme leaves the sticky band and toolbar dark

| Field | Value |
| --- | --- |
| Severity | Low |
| Confidence | Observed |
| Area | Preview theme override |
| Evidence | [p2-theme2-b.jpg](../evidence/p2-theme2-b.jpg) |

## Observed

With VS Code in a dark theme, the toolbar theme button cycles Current → Dark → White. In White
mode the page is white, but the sticky heading band and the floating toolbar keep their dark
backgrounds, which produces a black bar with white headings on top of a white page. The button
tooltip ("White theme (click for current theme)") is clear.

## Suggested direction

Drive the band and toolbar colours from the same preview theme variables as the page, not from the
VS Code theme variables.

## Done when

Each preview theme is visually consistent from the top edge to the bottom.

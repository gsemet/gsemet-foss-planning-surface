# UX-46 — Wide Mermaid diagrams are scaled until their labels are unreadable

| Field | Value |
| --- | --- |
| Severity | Low |
| Confidence | Observed at a 540 px preview |
| Area | Diagram rendering |
| Evidence | [p2-smoke.jpg](../evidence/p2-smoke.jpg) |

## Observed

A five-node `flowchart LR` is scaled down to the content width; node labels ("Manifest",
"Plan legs", "Dispatch") render at about 6 px and the edge labels ("yes", "no") are smaller still.
There is no way to zoom or open the diagram larger. Sequence diagrams, which are taller than wide,
stay readable.

## Suggested direction

Set a minimum scale (render at natural size and let the figure scroll horizontally, like wide
tables), and add click-to-zoom (open the SVG in an overlay or a separate tab).

## Done when

Diagram text is never rendered below about 10 px.

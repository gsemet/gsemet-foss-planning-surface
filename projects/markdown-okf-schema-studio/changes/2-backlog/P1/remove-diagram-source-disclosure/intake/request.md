# Remove the "Diagram source" disclosure under diagrams

Filed on the owner's word of 2026-11-27, in French:

> « Met en P1 d'enlever les "Diagram source" sur les pages, sous les diagrammes, ça sert à rien. »

Request: remove the collapsed **Diagram source** disclosure shown under the diagrams of a page.
Priority given by the owner: P1.

Facts read in the code at `b9b29c5a`, for the grill (not decisions):

- `src/core/render/mystNormalize.ts` (`normalizeDiagram`) adds the disclosure under Mermaid and
  PlantUML figures ("Diagram source") and under Vega figures ("Chart source").
- Since 1.13.0 the preview no longer shows **Chart source** under a chart, and the HTML export keeps
  it (`docs/user/charts.md`, `src/core/export/exportStyles.ts`). The same split is the obvious
  precedent.
- Requirements that name the disclosure: SwRS DIAG-001, DIAG-015, DIAG-023 and BLOCK-014, StRS
  DIAG-001 and DIAG-006.
- A Mermaid render error says "Its source remains available below." (`src/page/modules/mermaidError.ts`).
- A click on the words "Diagram source" has its own behaviour in edit mode (SwRS BLOCK-014).

Open questions for the grill:

- Does the HTML export keep the disclosure, as it does for charts?
- When a diagram fails to render, does the source stay visible?

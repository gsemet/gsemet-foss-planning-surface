# Source panels under diagrams and charts show only on a failed render

## Goal

The owner finds the collapsed **Diagram source** panel under a Mermaid or PlantUML figure, and the
**Chart source** panel under a Vega or Vega-Lite chart, useless: a reader who wants the source reads
the raw Markdown. After this change a figure that renders shows no source panel, in the preview or
in the HTML export. A figure that fails to render keeps its source panel, closed, in both, so a
reader of an exported file without the Markdown does not lose the content.

Facts read at `origin/main` `b9b29c5a`. Automatable; the owner does not review this specification.

## Decisions (from `02-answers.md`)

1. **Diagram source** leaves the HTML export as well as the preview.
2. **Chart source** leaves the HTML export too (the preview already hides it since 1.13.0).
3. A diagram or chart that fails to render keeps its source panel.
4. One rule everywhere, preview and export, diagrams and charts: the source panel appears only when
   the render fails. A failed chart in the preview now shows its **Chart source** (changes SwRS
   DIAG-123).
5. StRS DIAG-001 and DIAG-006 are `approved` and change: the owner re-approves them (see
   "Requirements").

## The rule

- "Fails to render" is the render state the page and the host already set on the diagram element
  (`data-render-state`): `error` (Mermaid `src/page/modules/mermaidPreview.ts`, charts
  `src/page/modules/vegaPreview.ts`, PlantUML `src/page/modules/plantumlDiagram.ts` and the JAR path
  `src/core/render/plantUmlRenderer.ts`) or `unavailable` (PlantUML refusals, a missing engine or
  JAR). `rendered` and no state yet (pending) show no panel.
- The export takes its snapshot from the live page (`src/page/modules/exportSnapshot.ts`, the render
  state attributes are copied), so the same CSS decides in the exported file, with JavaScript off.

## What changes

- `src/core/render/mystNormalize.ts` (`normalizeDiagram`): unchanged; the `details.myst-<kind>-source`
  element stays in the markup, since a failure is only known after the page draws.
- `src/core/preview/styles/contentBlockStyles.ts`: `details.myst-mermaid-source`,
  `details.myst-plantuml-source` and `details.myst-vega-source` get `display: none`, and are shown
  (`display: block`, existing margin and summary styles kept) when the figure's diagram element has
  `data-render-state` `error` or `unavailable`, for example
  `figure.myst-<kind>-figure:has(> .myst-<kind>-diagram[data-render-state="error"]) > details.myst-<kind>-source`
  (a class set on the figure by the page is an acceptable alternative if it also reaches the export).
- `src/core/export/exportStyles.ts` (`exportSheet`): remove the `details.myst-vega-source
  { display: block; }` override and its mention in the JSDoc; the export follows the preview rule.
- `src/page/modules/findIndex.ts`: the find bar searches only text the reader sees. A source panel
  that is hidden (figure rendered or pending) is skipped, for all three kinds (today only
  `.myst-vega-source`); a shown panel (failed figure) is searchable like any folded section.
- Unchanged: `src/page/modules/mermaidError.ts` ("Unable to render Mermaid diagram. Its source
  remains available below." stays true), `src/page/modules/chartError.ts` ("Unable to render the
  chart."), the **Show the parser error** and **Show the error** sections, the edit-mode click on
  the words "Diagram source" (SwRS BLOCK-014, now reachable on a failed figure only), the copy-button
  exclusion of diagram sources (SwRS CODE-017).

## Requirements

Update in place, with markers and `@tests_req` on each test that checks the new text,
`just requirements-update`, and a dated entry in `requirements/tiers/log.md`.

- StRS DIAG-001 (approved): "Reading" bullet and the SwRS DIAG-001 line say the source panel is
  shown only when the diagram fails; "Failure" keeps "the source stays available".
- StRS DIAG-006 (approved): same for the "Reading" bullet; "Failure" unchanged.
- Approval: the project asks for the owner's explicit agreement before an approved requirement
  changes (`requirements/guidelines/project.guidelines.md`, "Approved requirements"); it is **not
  yet recorded** for these two. With it, the coder sets `approved_by` to the owner's email and
  `approved_at` to the time of the change on both, the PR body lists them under "Approved
  requirements changed", and the agent that opens the PR requests the owner's review.
- SwRS DIAG-001 (Mermaid) and DIAG-023 (PlantUML): description and S1 say the collapsed
  "Diagram source" disclosure is hidden unless the render state is `error` or `unavailable`, in the
  preview and the HTML export; DIAG-023 S4 and S7 (rendered picture: no disclosure shown; disclosure
  style applies to a shown one). Add `src/core/preview/styles/contentBlockStyles.ts`,
  `src/core/export/exportStyles.ts` and `src/page/modules/findIndex.ts` to their implementation where
  marked.
- SwRS DIAG-121 (charts): description and S4 become "a collapsed Chart source section shown, in the
  preview and the HTML export, only when the chart fails to render"; the find bar does not match a
  hidden one.
- SwRS DIAG-123 S3: a failed chart shows the message and the reason, and its **Chart source**
  section, closed, under it, in the preview.
- SwRS DIAG-105 S3 ("... the expandable source disclosure is kept"): a rendered diagram keeps the
  disclosure in the markup and does not show it.
- Still true, check only: DIAG-015 S1, DIAG-032 S1, DIAG-089 (missing command row); BLOCK-014 rows
  on "Diagram source" reworded to "of a failed Mermaid or PlantUML figure".
- StRS DIAG-015 (proposed): "chart with its source section" and "a source section kept for the HTML
  export" become the failure-only rule. StRS DIAG-009 "the expandable source": add "when it fails".
- Deprecated, not touched: SwRS DIAG-029, DIAG-083, DIAG-092, DIAG-111, DIAG-112, CODE-022.

## Documentation

- `docs/user/charts.md` "Errors": no **Chart source** section under a drawn chart, in the preview
  or the export; a chart that fails shows its message and its source, closed.
- `CHANGELOG.md` "Unreleased": one line (the panels are gone under drawn diagrams and charts, in the
  preview and the HTML export; a failed figure keeps its source).
- `docs/demo-video/clips/export-html/clip.md` (the "One visible difference: Chart source" note) is
  now false: correct the text; re-recording the clip is out of scope.
- The writing skill `skills/writing-for-markdown-okf-schema-studio/` and the rest of `docs/user/`
  do not describe these panels (checked): no change.

## Evidence

- `test/page/chartCsp.test.ts`: the preview hides **Chart source** of drawn charts (kept); the test
  "the HTML export shows each Chart source section again" becomes: the export hides it for a drawn
  chart and shows it, closed, for the broken chart of the fixture; the broken chart shows its panel
  in the preview.
- `test/page/modules/chartError.test.ts`: the preview sheet hides the three panels and shows them for
  `error`/`unavailable`; `exportSheet` no longer contains a `details.myst-vega-source` rule.
- `test/page/modules/findIndex.test.ts`: a hidden Mermaid, PlantUML or chart source is not searched;
  the source of a failed figure is.
- `test/visual/scenarioAssertions.ts`: on drawn figures (`plantUmlBuiltinAssertions`,
  `plantUmlFileAssertions`, `plantUmlIncludeAssertions`) "the source stays available" becomes the
  disclosure present but not visible; on failures (`MERMAID_ERROR_ASSERTIONS`,
  `PLANTUML_UNSUPPORTED_ASSERTIONS`) it is visible and closed.
- `test/visual/capture_export_html.py`: the exported Mermaid source is present and not displayed.
- `test/page/blockReq.requirements.test.ts` (click on "Diagram source" in edit mode) passes on a
  failed figure.
- `just requirements-lint`, `just check`, `just preflight`.

## Out of scope

- The **Show the parser error** / **Show the error** sections, the export's properties section,
  author-written collapsible sections.
- The wording of the Mermaid and chart error messages.
- Re-recording feature clips (`advanced-renderings-tour` crops around the "Diagram source" lines;
  only a manual `just clip` run would show it).

## Questions for the Chief of Staff

None.

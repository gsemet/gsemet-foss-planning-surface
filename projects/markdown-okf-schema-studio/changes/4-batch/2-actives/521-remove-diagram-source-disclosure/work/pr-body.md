## Summary

Every Mermaid and PlantUML diagram carried a collapsed "Diagram source" section under it, and a chart
carried a "Chart source" section in the HTML export. A reader who wants the source reads the Markdown.
A figure that draws now shows no source section; a figure that fails to render keeps it, closed, so a
reader of an exported file does not lose the content.

## Deliverables

One rule for diagrams and charts, in the preview and in the HTML export:

| Figure state                      | Before                                      | After                  |
| --------------------------------- | ------------------------------------------- | ---------------------- |
| Mermaid or PlantUML, drawn        | "Diagram source" in preview and export      | no source section      |
| Mermaid or PlantUML, failed       | "Diagram source" in preview and export      | unchanged              |
| Chart, drawn                      | "Chart source" in the export only           | no source section      |
| Chart, failed                     | "Chart source" in the export only           | in preview and export  |
| Any figure not yet drawn          | diagrams: source section shown              | no source section      |

The style sheet shared by the preview and the export decides, from the render state already set on the
diagram element:

```css
.myst-mermaid-diagram:is([data-render-state="error"], [data-render-state="unavailable"])
  ~ details.myst-mermaid-source { display: block; }
```

## Changes

- Preview style sheet: the three source sections are hidden, and shown for the `error` and
  `unavailable` render states. The HTML markup is unchanged.
- HTML export: the rule that showed "Chart source" again is removed, so the export follows the preview.
  The exported file needs no JavaScript for this.
- Find bar: it skips a hidden source section of any kind and searches a shown one.
- Built-in PlantUML engine: its syntax-error picture now marks the figure as failed.
- Requirements, the charts page of the user documentation, the changelog and the tests follow.

## Approved requirements changed

The maintainer agreed to these changes before the work started.

- `StRS-MDOKFSTUDIO-DIAG-001`: the source stays available when the diagram fails to render; the goal
  and the use case diagram no longer promise the source under a drawn diagram.
- `StRS-MDOKFSTUDIO-DIAG-006`: the collapsed "Diagram source" section shows only when the diagram
  fails to render.

## Requirements changed

A short name such as "SwRS DIAG-001" stands for `SwRS-MDOKFSTUDIO-DIAG-001`. Test paths are under
`test/`, source paths under `src/`.

| Requirement                     | Source                                                                                      | Tests                                                                                                                  |
| ------------------------------- | ------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| SwRS DIAG-001 (Mermaid)         | `core/preview/styles/contentBlockStyles.ts`, `core/export/exportStyles.ts`, `page/modules/findIndex.ts` | `page/modules/chartError.test.ts`, `page/modules/findIndex.test.ts`, `visual/scenarioAssertions.ts`, `visual/capture_export_html.py` |
| SwRS DIAG-023 (PlantUML)        | the same three files                                                                        | `page/modules/chartError.test.ts`, `page/modules/findIndex.test.ts`, `visual/scenarioAssertions.ts`                   |
| SwRS DIAG-121 (charts)          | the same three files                                                                        | `page/chartCsp.test.ts`, `page/modules/chartError.test.ts`, `page/modules/findIndex.test.ts`                           |
| SwRS DIAG-123 (failed chart)    | `core/preview/styles/contentBlockStyles.ts`                                                 | `page/chartCsp.test.ts`, `page/modules/chartError.test.ts`                                                            |
| SwRS DIAG-105 (PlantUML JAR)    | markup unchanged                                                                            | `visual/scenarioDefinitions1.ts`, `visual/capture_support.py`                                                         |
| SwRS DIAG-068 (PlantUML file)   | markup unchanged                                                                            | `visual/scenarioAssertions.ts`                                                                                         |
| SwRS DIAG-032 (syntax error)    | `page/modules/plantumlDiagram.ts`                                                          | `page/modules/plantumlDiagram.test.ts`, `page/plantumlErrorPicture.test.ts`                                          |
| SwRS BLOCK-014 (edit clicks)    | behaviour unchanged, wording only                                                           | `page/blockReq.requirements.test.ts`                                                                                   |
| StRS DIAG-009, DIAG-015         | proposed requirements, wording only                                                         | none                                                                                                                   |

## Impacts

- A drawn diagram or chart has no source section under it, in the preview and in exported HTML files.
- A failed chart now shows "Chart source", closed, under its message in the preview.
- In edit mode, the click on the words "Diagram source" is available on a failed figure only.

Before and after screenshots: provisional, to be added.

## Blast radius

Grade: 1. Styles, the find bar's text collection and the render state the built-in PlantUML engine's page
module sets; a plain `git revert` restores the previous
behaviour.

## Autonomous decisions

- A PlantUML syntax error that the built-in engine draws as its own error picture counts as a failed
  render: the picture shows as before and the source stays under it, closed.
- The hidden or shown choice is a style sheet rule on the render state, so the export decides the same
  way as the preview.
- The find bar does not search again by itself when a render state changes after a search: a figure
  that fails while the bar is open is matched at the next search.

## Known gaps

- A valid light `@startsalt` diagram whose first text is "Your data does not sound like JSON data" is
  taken for an error picture: it still draws, with its source shown under it.
- Only the light-theme error picture is covered by a committed test.
- The find bar does not search again by itself when a figure's render state changes while it is open.
- The PlantUML engine in Java (JAR) was not run for the syntax-error case; that path was read in code.
- The test with the real built-in engine needs a browser and is skipped by the static CI jobs; a test
  with a stand-in engine runs there.
- On a syntax error the built-in engine shows its error picture without a hint about the JAR engine,
  as before this change, which `StRS-MDOKFSTUDIO-DIAG-006` does not describe.

## Test plan

- [ ] New or changed tests (they fail on the previous code)
- [x] Requirements: SwRS updated, markers in code and tests, `just requirements-update` (table above)
- [x] Changelog: one user-facing line under `## Unreleased` in `CHANGELOG.md`
- [ ] Local gates
- [ ] Review
- [ ] CI green

🤖 Generated with [Claude Code](https://claude.com/claude-code)

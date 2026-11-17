---
title: Change spec - the visual campaign export draws Mermaid diagrams like the real export
cr: 299
date: 2026-11-12
issue: none
priority: P2
source: CR 288 follow-up, release 1.7.0 check (2026-11-11)
blast_radius: 2 (the visual campaign build of export files; possibly the Mermaid label styles of the export)
inspector: Opus
rounds: 3
---

# Change spec: the visual campaign export draws Mermaid diagrams like the real export

> [!NOTE]
> Intent: `01-intent.md`. Answers: `02-answers.md`. Read code and guidelines on `origin/main`
> (`20ccb380` at the time of writing). Rules: `.agents/constitution.md`, `AGENTS.md`,
> `requirements/guidelines/project.guidelines.md` ("During a change").

## Problem

`writeExportFile` in `test/visual/renderFixtures.ts` builds the "Export to HTML" file of scenarios
`toolbar-navigation/v42-export-html-cream-900` and `v43-export-html-dark-900` from the static page
written by `renderPage`. The page script that draws Mermaid (`src/page/modules/mermaidPreview.ts`)
never runs there, so a `mermaid` fence shows as its source text. In real VS Code the export embeds
the drawn diagram as `<img class="myst-mermaid-image" src="data:image/svg+xml...">` with the source
folded in a `<details class="myst-mermaid-source">` ("Diagram source"); see
`test/integration/exportHtml.test.ts`. The campaign pictures therefore do not show what a user gets
and cannot serve as release pictures.

A second defect was seen in a real export (release 1.7.0 check, fixture 87-export-html, Cream): the
labels of the Mermaid flowchart boxes sit at the top of their boxes instead of their middle.

## Target behaviour

1. The export files of v42 and v43 hold each Mermaid diagram of the fixture as the real export
   does: the drawn diagram as an embedded `data:image/svg+xml` image of class
   `myst-mermaid-image`, then the folded "Diagram source" with the fence text. No Mermaid source
   is shown open, and the file still has no `<script>`.
2. The diagram is drawn by the product's own Mermaid path (the page script in a browser, as the
   preview does), not by a test-only re-implementation; the export markup comes from the product's
   export code (`buildHtmlExport` and what it already does with a drawn diagram). The coder chooses
   how the campaign gets the drawn page (for example: build the export from the page after the
   capture browser ran the page script, the same snapshot the webview sends on Export).
3. Box labels: compare the preview and the export of the same diagram (both themes).
   - If the preview centres the labels and only the export puts them at the top, fix the export
     so the labels are centred in their boxes (product change, with its SwRS).
   - If the preview shows the same fault, do not fix it here: record it in the PR's "Autonomous
     decisions" and add a P3 backlog item note to the final report.
4. The v42 and v43 scenario descriptions in `test/visual/scenarioIds.ts` mention the drawn
   diagram with its folded source, and their checks assert it (an image of class
   `myst-mermaid-image` with a `data:image/svg+xml` source, and a closed details element).

## Decisions (Chief of Staff, by judgment)

- The fixture used by v42/v43 must contain a Mermaid flowchart; if it does not, add a short one
  (three boxes) to the export fixture.
- Keep HTML labels (the P3 item `mermaid-svg-text-labels` is out of scope).

## Acceptance checks

- `just ci-visual` (or the campaign subset that builds v42/v43) passes, and the v42 and v43
  export files contain `class="myst-mermaid-image"` with a `data:image/svg+xml` source, a closed
  `myst-mermaid-source` details, and no `<script`.
- Screenshots of v42 (Cream) and v43 (Dark), before and after, show the drawn diagram in place of
  its source text; box labels centred if point 3 applies.
- `just check` and `just requirements-update` pass; a `requirements/tiers/log.md` entry if an SwRS
  changes.
- PR body per the template, with before/after images in light and dark.

# Visual campaign export shows Mermaid diagrams as source text

Found during CR 288 (export to a single HTML file, PR #365). In the exported file written by the
static visual campaign (`renderFixtures.ts`, scenarios v42 and v43), a `mermaid` fence shows as its
source text: the page script that draws Mermaid does not run when the campaign builds the file.

Checked on 2026-11-11 for release 1.7.0: **not a product bug**. In real VS Code the export embeds the
drawn diagram as `<img class="myst-mermaid-image" src="data:image/svg+xml...">`, with the source
in a folded "Diagram source" (`test/integration/exportHtml.test.ts` asserts it, and a run with the
87-export-html fixture confirmed it).

Expected: the campaign's exported file shows the drawn diagram too, so the v42/v43 screenshots
match what a user gets and can serve as release pictures.

Seen in the same check: in the exported file, the labels of the Mermaid flowchart boxes sit at the
top of the boxes instead of their middle. Check whether the preview does the same; fix in the same
change if it is export-only.

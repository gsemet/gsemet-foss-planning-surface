# CR-521 before and after

Before: `6b1dd90d176a9ed4a2139e2cf71e11eb02e9fc03` (origin/main, detached worktree, `src/` unchanged). After:
`0afb09dc2f9712dbbcfd393563e9376e282375c4` (pushed head).

All images come from the real preview page (real `renderPreviewDocument`, `buildPreviewWebviewHtml` and page bundles)
in headless Chromium, and from the file the real `HtmlExportController` wrote, opened with JavaScript off. The same
Markdown on both sides. Each of the 18 images was opened and shows no username and no home folder.

| Pair | Before | After | What it shows |
| --- | --- | --- | --- |
| Preview, light | `before-preview-light.png` | `after-preview-light.png` | Before: "Diagram source" under the drawn and the failed Mermaid figure, no "Chart source" under the failed chart. After: nothing under a drawn figure, "Diagram source" under the failed diagram, "Chart source" under the failed chart, both closed. |
| Preview, dark | `before-preview-dark.png` | `after-preview-dark.png` | The same, dark theme. |
| Export, light | `before-export-light.png` | `after-export-light.png` | Before: four source sections, one under each figure. After: only under the two failed figures. |
| Export, from the dark theme | `before-export-dark.png` | `after-export-dark.png` | The same. The exported page is light with dark node boxes and pale chart labels, identically before and after: not changed here. |
| PlantUML syntax errors, light | `before-plantuml-syntax-error-light.png` | `after-plantuml-syntax-error-light.png` | Identical files: "Diagram source" under three error pictures of the built-in engine. Round 3 gives back what the base showed. |
| PlantUML syntax errors, dark | `before-plantuml-syntax-error-dark.png` | `after-plantuml-syntax-error-dark.png` | The same, dark theme. |
| PlantUML EBNF errors, light (a failed claim, not for Impacts as a success) | `before-plantuml-ebnf-error-light.png` | `after-plantuml-ebnf-error-light.png` | A valid grammar, then two the engine answers with "Syntax error!". Before: "Diagram source" under all three. After: under none, so the two failed figures lost their source. |
| PlantUML EBNF errors, dark (the same failed claim) | `before-plantuml-ebnf-error-dark.png` | `after-plantuml-ebnf-error-dark.png` | The same, dark theme. |
| PlantUML EBNF errors, export (the same failed claim) | `before-plantuml-ebnf-error-export-light.png` | `after-plantuml-ebnf-error-export-light.png` | The same in the exported file. |

Reproduce, from each worktree after `just dev`, `compile` and `bundle`:

```text
fnm exec -- node --import ./scripts/register-myst-patches.mjs <CR folder>/work/verifier/realflow.cjs <worktree> <outdir> shots
fnm exec -- node --import ./scripts/register-myst-patches.mjs <CR folder>/work/verifier/realflow.cjs <worktree> <outdir> syntax
fnm exec -- node --import ./scripts/register-myst-patches.mjs <CR folder>/work/verifier/realflow.cjs <worktree> <outdir> ebnf
```

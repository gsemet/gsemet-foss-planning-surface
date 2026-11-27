# CR-521 before and after

Before: `b9b29c5a34e6d6e24b898513f5fad44c4515b52c` (origin/main, detached worktree, the head's `test/` checked out,
`src/` unchanged). After: `4000024f8220ac13bbdba952af5f6a701994f216` (pushed head).

All images come from the real preview page (real `renderPreviewDocument`, `buildPreviewWebviewHtml` and page bundles)
in headless Chromium, and from the file the real `HtmlExportController` wrote, opened with JavaScript off. The same
Markdown on both sides: a drawn and a failed Mermaid diagram, a drawn and a failed Vega-Lite chart. Each image was
opened and shows no username and no home folder.

| Pair | Before | After | What it shows |
| --- | --- | --- | --- |
| Preview, light | `before-preview-light.png` | `after-preview-light.png` | Before: "Diagram source" under the drawn and the failed Mermaid figure, no "Chart source" under the failed chart. After: nothing under a drawn figure, "Diagram source" under the failed diagram, "Chart source" under the failed chart, both closed. |
| Preview, dark | `before-preview-dark.png` | `after-preview-dark.png` | The same, dark theme. |
| Export, light | `before-export-light.png` | `after-export-light.png` | Before: four source sections, one under each figure. After: only under the two failed figures. |
| Export, from the dark theme | `before-export-dark.png` | `after-export-dark.png` | The same. The exported page is light with dark node boxes and pale chart labels, identically before and after: not changed here. |
| PlantUML syntax errors, built-in engine (a failed claim, not for Impacts as a success) | `before-plantuml-syntax-error-light.png` | `after-plantuml-syntax-error-light.png` | Before: "Diagram source" under three engine error pictures. After: no source section under any of them. |

Reproduce, from each worktree after `just dev`, `compile` and `bundle`:

```text
fnm exec -- node --import ./scripts/register-myst-patches.mjs <CR folder>/work/verifier/realflow.cjs <worktree> <outdir> shots
fnm exec -- node --import ./scripts/register-myst-patches.mjs <CR folder>/work/verifier/realflow.cjs <worktree> <outdir> syntax
```

# 165 — Refresh the README screenshots — report

Landed 2026-10-28. Decision (user): option A, two parts.

- Part 1: PR #177 (headless README pictures, `--visual-only`), merged earlier.
- Part 2: PR https://github.com/gsemet/markdown-okf-schema-studio/pull/184 (6 real-window pictures:
  myst-admonitions, myst-diagrams-and-figure, inline-editing, open-with-editor,
  open-preview-to-side, preview-beside-editor), merged 2026-10-28.

## Part 2 outcome

- Source: real-input artifact of the green 1.0.0 heavy gate on main cad03b4d, run 40762299560
  ("Suite: passed").
- New `--real-only` flag in `scripts/generate-readme-images.py`; crop boxes fixed for
  myst-admonitions and inline-editing (was cutting Done/Cancel) in `test/shared/captureRegistry.ts`;
  new crop test in `test/site/captureRegistry.test.ts`.
- Opus Inspector APPROVE after opening all six PNGs (review `reviews/T1-r3.md`). Normal CI green:
  run 40766289670. Before/after pairs on `change-requests/165-refresh-readme-screenshots-assets`.

## Known limit

- myst-diagrams-and-figure shows clipped Mermaid labels from the source capture; tracked by backlog
  P2 `mermaid-labels-clipped-in-webview` (regenerate this picture once fixed).

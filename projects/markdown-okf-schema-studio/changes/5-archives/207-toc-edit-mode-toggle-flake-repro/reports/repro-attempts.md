# CR 207 - toc edit-mode toggle flake: reproduction attempts (2026-10-31)

Result: NOT reproduced. 280 clean rounds, 0 failed.

Method: scenario `toc-loop` (STUDIO_TOC_LOOP=40 rounds in one real VS Code window under xvfb) on scratch
branch proof/207-toc-toggle (deleted afterwards), with random pauses 0..N ms around the toggle click and
the host theme change; the #205 toggle state is recorded on failure plus a focus dump.

| Run | Delay max | Result |
|---|---|---|
| https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/41145936663 | 0 ms | 40 clean |
| https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/41147013837 | 0 ms | 40 clean |
| https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/41145939358 | 300 ms | 40 clean |
| https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/41147016249 | 500 ms | 40 clean |
| https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/41145941806 | 1000 ms | 40 clean |
| https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/41147019295 | 2000 ms | 40 clean |
| https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/41147022242 | 2000 ms | 40 clean |

Headless (test/page/runtimeEditToggleRace.test.ts): rapid clicks, patches between clicks, saved state vs
host initialEditMode all behave; no product race found. Open suspect (real window only): webview reload
(theme change) booting from stale saved state right after a click.
A round takes about 5 s, so 40 rounds fit well within 5 minutes; the cap could be raised.
Diagnostics PR worth it: modest (a ready repro tool for when the flake recurs). Local commit handed to Foreman.

# Report: CR 248

Status: **done** (2026-11-03, branch `change-requests/248-syntax-coverage-audit`, PR [#302](https://github.com/gsemet/markdown-okf-schema-studio/pull/302), merged as 628fc69f).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | Syntax coverage audit (`matrix.md`): every rendered syntax checked against the slash menu and palette. New slash entries "Content tabs" and "PlantUML". Guard test `test/page/modules/slashSyntaxCoverage.test.ts` with 7 documented exceptions. | 9b4764e7 |
| T1 (round 2) | Docs link the slash coverage rule to its registry and name Content tabs; `@implements_req` marker for PALETTE-275. | 628fc69f |

Requirements: new SwRS PALETTE-273, PALETTE-274, PALETTE-275 (`proposed`), markers, dated log entry. One CHANGELOG line.

## Proof of completion

- 2 rounds of 3. CI green on the rebased head e06c33a9 (static, static-windows, visual, report). Real-window jobs not run.

## Open items

- The README presentation HTML has no insert form (M).
- `{uml} file.puml` has no insert; it needs a .puml picker (M).
- `<sub>` and `<sup>` exist only as MyST roles (S-M).
- Empty `{list-table}` and `{toctree}` can only be written by hand (S, low).
- Nits: plantuml reuses the mermaid icon; guard test 3 uses a loose substring match.

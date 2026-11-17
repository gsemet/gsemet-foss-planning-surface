# Report: CR 249

Status: **done** (2026-11-03, branch `change-requests/249-myst-block-break-in-directive-crashes-render`, PR [#291](https://github.com/gsemet/markdown-okf-schema-studio/pull/291), merged by the owner as 4b52da06, middle of stack #292).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | A `+++` line inside any container (directive, quote, list item, alert) renders as text and no longer throws; a root-level `+++` stays a block break. New tree pass `src/core/render/mystNestedBlockBreaks.ts`, registered in `mystRenderer.ts`. | 4b52da06 |

Requirements: new SwRS MYST-101 (`proposed`), generated myst index and StRS link, dated log entry, one CHANGELOG line.

## Proof of completion

- `test/core/render/blockBreakInContainer.test.ts`: 7 tests (the 6 inputs of the intent plus a root-level guard); the 6 container cases throw `TypeError` without the pass.
- `just check` passed (3560 unit, 73 security); simulated group `myst` 45 scenarios. CI run 41648198893 green. One round, reviewer APPROVE.

## Open items

- A second `+++` inside a card footer fragment renders as text under the rule, with no test.
- The comparison with GitHub's rendering of the quote and list cases was not done (needs network).

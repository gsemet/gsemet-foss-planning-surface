# Report: CR 246

Status: **done** (2026-11-03, branch `change-requests/246-myst-code-block-editor`, PR [#300](https://github.com/gsemet/markdown-okf-schema-studio/pull/300), merged as 71bdc0fa).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | A "Code-block (MyST)" palette form (language, line numbers, emphasized lines, caption, name) that edits an existing `{code-block}` or inserts a new one. New files `src/page/modules/codeBlockDirective.ts` and `src/page/modules/codeBlockPanel.ts`. | 71bdc0fa |

Requirements: new SwRS PALETTE-272 (`proposed`; it was PALETTE-268 in the branch and was renumbered when it was stacked), markers, dated log entry. Writing skill: the Code row now lists `:emphasize-lines:` and `:name:`. One CHANGELOG line.

## Proof of completion

- 14 new tests (9 unit, 5 page); the 5 page tests failed on the unchanged code, and the 9 unit tests could not load before the module existed.
- `just check` passed (3567 unit, 73 security); simulated `palette-slash` group passed; `just requirements-update` ran. One round (1 of 3), inspector APPROVE. CI green on the rebased head (all four checks plus the Windows static job). Real-window jobs not run.

## Open items

- An existing block whose language contains a space blocks Apply until the language is edited, even if the writer changed nothing.
- A body line indented less than the fence is re-indented on write.
- The `palette-slash` scope text in `e2eGroups` still says "figure form".
- No visual scenario or screenshot covers the code-block form.

# Report: CR 236

Status: **done** (2026-11-03, branch `change-requests/236-ctrl-a-in-search`, PR [#281](https://github.com/gsemet/markdown-okf-schema-studio/pull/281), merge commit d9fb242c).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | The find and replace fields keep the native text-editing keys (Cmd/Ctrl+A, C, X, V, Z, Y, arrows, Home, End, Backspace, Delete, word and line moves): they stop at the bar and the browser acts on the field. The bar's own keys are unchanged. | 3f3ee131 (rebased as d9fb242c) |

New requirement SwRS-MDOKFSTUDIO-TOOLBAR-132 (`proposed`), with `@implements_req` and `@tests_req` markers, a dated entry in `requirements/tiers/log.md`, and the regenerated index and StRS-003 files.

## Proof of completion

- New test in `test/page/modules/findBar.test.ts`; it failed on the old code (`{"key":"a","ctrlKey":true}`: stopped 0, expected 1) and passes after (20 of 20 tests of the file).
- `just check`: unit 3517 pass, security 73 pass.
- Standard CI run 41620792036 green; heavy run 41623150162 green (real VS Code window jobs included).
- The Ctrl+A symptom could not be reproduced without a real window, so the fix is a generic guard (listed under "Autonomous decisions" in the PR). Review: APPROVE in round 1 of 3.

## Open items

- None.

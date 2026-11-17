# Report — empty-document-keyboard-start

Status: **done** (2026-10-28, branch `change-requests/156-empty-document-keyboard-start`,
PR [#171](https://github.com/gsemet/markdown-okf-schema-studio/pull/171) merged into `fix/tab-item-edit-source`, landed on main with
PR [#166](https://github.com/gsemet/markdown-okf-schema-studio/pull/166) as `c6c96731`).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | In edit mode on an empty document the Start writing button is the keyboard selection (ring); Enter and Down open the new-block editor; hint "Enter to create a new block" under it. New SwRS-MDOKFSTUDIO-BLOCK-253 (`proposed`); editing guide. | `c6c96731` |

## Proof of completion

- Tests: test/page/runtimeEmptyDocumentStart.test.ts, visual scenarios `layout-width/v86` (light)
  and `v87` (dark) at 700 px.
- Local gate on the restacked branch (`12f8db62`): `just check` green, `okfreq validate
  --check-links` 1058 requirements, 0 errors; at the stack top the webview tests of 156 and 157
  ran together: 25/25 pass.
- CI: normal run [40695096753](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40695096753) green (pre-stack); heavy [40695110033](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40695110033)
  failed only on the known tableMoves regression (fixed by [#167](https://github.com/gsemet/markdown-okf-schema-studio/pull/167)). Main after merge:
  [40700143893](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40700143893).
- Screenshots: branch `change-requests/156-empty-document-keyboard-start-assets`.
- Rounds: 1/3.

## Open items

- Missing `@implements_req SwRS-MDOKFSTUDIO-BLOCK-253` marker in createInsertPoint and a
  verification note citing a test without marker:
  [02-backlog/P3/keyboard-nav-followups](../../2-backlog/P3/keyboard-nav-followups/01-intent.md).

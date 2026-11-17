# Report — edit-toolbar-cover-figure-button

Status: **done** (2026-10-28, branch `change-requests/161-edit-toolbar-cover-figure-button`,
PR [#174](https://github.com/gsemet/markdown-okf-schema-studio/pull/174), head `620c640a`, merged as
`117c026c`).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | Edit figure button clamped inside a short figure sat under the five-row toolbar (at 421 px: button 290..363 x 119..138, toolbar 304..406 x 12..178). `figurePanel.ts` gets an optional `obstacle()` and moves the button left of the toolbar on overlap; `runtime.ts` wires the live toolbar rect. SwRS-MDOKFSTUDIO-PALETTE-153 (proposed) + log entry. No change to the integration test. | `620c640a` |

## Proof of completion

- One round (reviewer APPROVE). Unit test and visual scenario v29, both failing on the old code.
  `just check` and `okfreq validate --check-links` clean.
- CI: normal [40719994631](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40719994631) pass.
  Heavy: [40722041491](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40722041491)
  infra (VS Code version request timeout); [40723163115](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40723163115)
  failed earlier in `checkboxToggle` (webview start timeout, before `editToolbarCover`);
  [40723757734](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40723757734)
  integration still running at landing. The user merged on normal CI + unit/visual proofs.
- Screenshots: before/after on `change-requests/161-edit-toolbar-cover-figure-button-assets` (`cr161/`).

## Open items

- Heavy proof of `editToolbarCover` on the fix: run 40723757734 (Foreman tick follows it). If it
  fails in `editToolbarCover`, reopen as a hotfix; if `checkboxToggle` times out again, file a P2
  flaky-test backlog item.
- Not removed yet: worktree `../markdown-okf-schema-studio-wt-161` and its branch.

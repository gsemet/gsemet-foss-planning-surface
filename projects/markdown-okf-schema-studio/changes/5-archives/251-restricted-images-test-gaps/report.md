# Report: CR 251

Status: **done** (2026-11-03, branch `change-requests/251-restricted-images-test-gaps`, PR [#290](https://github.com/gsemet/markdown-okf-schema-studio/pull/290), merged by the owner as 6949fdb6, bottom of stack #292).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | A test for the workspace-root change of the baseline diff in a read-only preview (`test/session/baselineDiff.test.ts`, marker `@tests_req SwRS-MDOKFSTUDIO-TRUST-002`), and the doubled phrase in the TRUST-002 verification notes fixed. | 6949fdb6 |

## Proof of completion

- The coder showed the new test fails (2 pass, 1 fail) when `pagePolicyRoot(preview)` is reverted to `preview.workspaceRoot`, then restored the source. No `src` change, no CHANGELOG line (test-only).
- `just check` and the simulated `trust-security` group (4 scenarios) passed. CI run 41646341333 green. One round (1 of 3), reviewer APPROVE.

## Open items

- None.

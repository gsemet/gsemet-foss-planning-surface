# Report: CR 238

Status: **done** (2026-11-03, branch `change-requests/238-bug-display-relative-image-untrusted`, PR [#283](https://github.com/gsemet/markdown-okf-schema-studio/pull/283), merged by auto-merge as 5bd80b63).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | In Restricted Mode, images (png, jpg, jpeg, gif, webp, svg) are served from the document folder and the workspace folder; the extension is checked again after the symlink is resolved. Includes, other file types, dot-segment paths and symlink escapes stay refused; a broad workspace folder stays refused. Fixes two cases: an image in the workspace folder but outside the document's folder, and a document in the home folder or above that had every resource refused. | 5bd80b63 |

Requirements: SwRS TRUST-002 and TRUST-007 changed (both `proposed`, so no approval fields), StRS TRUST-004 one-line rationale edit, dated entry in `requirements/tiers/log.md`.

## Proof of completion

- Round 1: FIX-REQUIRED (two tests did not fail when the fix was reverted). Round 2: tests fixed, APPROVE. 2 of 3 rounds used.
- `just check`: unit 3524, security 73 pass; the trust-security e2e group passed 4 of 4 in simulation; okfreq validate 0 errors.
- Changed assertion: `test/session/readOnlyLocalRoots.test.ts` expected `[]` for `previewLocalResourceRoots(home, true)` and `(root, true)`; it now expects `[home]` and `[root]`, following the owner's own-folder exception.
- Rebased twice (after PR 282 and PR 284 merged); final CI run 41632457548 green (static, visual, report, checks). Real-window jobs not run (manual).
- Owner decision: auto-merge left on; the owner accepted the wider image roots by letting it merge.

## Open items

- `baselineDiff.ts` has no test of its own for the workspace-root change.
- The Verification notes sentence in `SwRS-MDOKFSTUDIO-TRUST-002.md` says "cover the images" twice (cosmetic).

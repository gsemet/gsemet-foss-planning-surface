# Report — 050-preview-warning-and-pasted-image

Status: **done** (2026-10-23, branch `changes-requests/050-preview-warning-and-pasted-image`,
[PR #46](https://github.com/gsemet/markdown-okf-schema-studio/pull/46), rebase-merged by the user;
main at 469b0fe).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 r1 | conf.py MyST warning banner (role=status, Open Problems button, close per document per session, reappears when the warning set changes, theme colours, no toolbar overlap, scroll anchor unchanged); pasted image inserted as its own paragraph; inline images vertically centred on the text line | 64a2424 (469b0fe on main) |

## Proof of completion

- 1/3 rounds, reviewer APPROVE (4 minor findings).
- Tests added: `test/webview/warningBanner.test.ts` (11), `test/webview/pasteImage.test.ts` (5),
  +1 previewMessages, +1 scrollSync; visual scenarios myst v29-v33.
- Local: tsc clean, unit 2009/2009, `just check` exit 0, `just visual` 320 scenarios pass.
- CI: [run 40001157752](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40001157752)
  pass (static, visual, report, checks); heavy
  [run 40001163360](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40001163360)
  integration pass (real-window image paste), stress advisory.
- Screenshots on `changes-requests/050-preview-warning-and-pasted-image-assets` (85d023a).
- Autonomous decisions (in the PR body): banner not sticky; set change compares messages, not
  lines; dismissal kept in host memory; no Open Problems button in Restricted Mode (tooltip
  lists warnings); a pasted image ends a list item / blockquote.

## Open items

- Questions: sticky banner (recommended no); banner text cut at ≤360px panes (recommended accept).
- Follow-ups: comments say "fixed" for an absolutely positioned banner; banner z-index above the
  sticky heading band; Restricted Mode flag only read at page load.

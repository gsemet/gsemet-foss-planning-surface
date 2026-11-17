# Report — comment-editor-behaviour

Status: **done** (2026-11-06, branch `change-requests/265-comment-editor-behaviour`, PR #329, merge commit `30239846`).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | The comment editors stay in the window and follow their text on scroll (SwRS REVIEW-217); Escape and a press outside dismiss them, with a question when a draft would be lost (SwRS REVIEW-218) | `30239846` |

## Proof of completion

- `test/page/modules/commentEditorBehaviour.test.ts` added; each bug failed on the old code.
- `just check` exit 0 (unit 3627 of 3627); PR CI green; heavy run 42184807228 green on the stack top. Approved in round 2.

## Open items

- SwRS REVIEW-217 and 218 were renumbered by hand on restack, against the constitution; the owner accepted it on 2026-11-06.
- Inspector findings left: a press on the scrollbar, and Cmd+Alt+M drops a reply draft silently.
- No screenshots. No changelog line in `## Unreleased`: to add before the next release.

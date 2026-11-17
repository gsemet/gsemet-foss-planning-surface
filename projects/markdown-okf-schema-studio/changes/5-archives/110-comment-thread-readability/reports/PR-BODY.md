## Summary

Review comment threads were hard to read: the popover text came out as pale grey on the cream page.
The forced Dark, White and Cream modes did not define the popover text colour, so it fell back to
the host theme's colour, and the date, quote and meta lines were additionally faded with `opacity`.
This change defines the colour per mode, removes the fading, and makes the comment author name
setting overridable per user, workspace or folder.

## Deliverables

- Comment popover, orphan and compose text reach WCAG AA (4.5:1) on Dark, White and Cream; the dark
  placeholder colour was lightened from 4.07:1 to 4.65:1.
- `comments.authorName` now has `scope: resource`; a workspace or folder value wins over the user
  value. Default source is unchanged (Git `user.name`, then the OS user). Documented in
  `docs/user/settings.md` and `docs/user/review-comments.md`.
- Tests: a contrast test over 11 text/surface pairs in three modes, a no-opacity test, a resource
  read test, a package contract test, three visual scenarios, and a Workspace-override step in the
  real-window comment test.
- Requirements: new `SwRS-MDOKFSTUDIO-REVIEW-002`, updated `SwRS-MDOKFSTUDIO-REVIEW-065`.

Before / after, in a real VS Code window (dark host theme, Cream preview), attached by the stack
driver from `before-real-cream-dark.png` and `after-real-cream-dark.png` (plus White, Dark, host and
light-host variants). Before: author and body 1.51:1, date 1.33:1; after: all at least 4.5:1.

A real-window contrast scenario measures author, date, body, placeholder, Resolve, Delete and Reply
as painted, under dark and light hosts across host, Dark, White and Cream previews; it fails on the
previous style files (17 of 56 pairs below 4.5:1).

## Autonomous decisions

- Contrast target is WCAG AA (4.5:1) for all comment text on every forced theme.
- Author setting uses `scope: resource`, keeping the current default source.
- Text under a non-forced (host) theme follows the user's VS Code theme and is not audited.

## Internal references

- CR 110, backlog item `bug-comment-thread-readability`.
- Screenshots: `.agents/changes/03-requests/110-comment-thread-readability/reports/shots/`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

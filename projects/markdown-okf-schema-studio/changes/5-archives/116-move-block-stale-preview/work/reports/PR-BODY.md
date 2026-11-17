## Summary

Clicking "move block up" or "move block down" next to a list did nothing and showed "The preview is
out of date. Refresh it and try again.", although the preview was in sync. Moving a block now works
and the message no longer appears in that case.

## Deliverables

The renderer maps a list up to the blank line that follows it. The editor refused any range ending
on a blank line as stale. Two changes:

```text
before: page range (list + trailing blank) -> planBlockMoveEdit -> refused "out of date"
after:  page range -> trailing blank lines dropped -> move planned -> block moves by one
        host still refused as stale -> resend once after the next render -> message only if refused again
```

- `planBlockMoveEdit` (`src/core/edits/sourceEdits.ts`) drops trailing blank lines from both ranges.
- `src/page/features/blockMoves.ts` resends a single-block move refused as stale once after the next
  render; the message appears only if that retry is refused too, or no render arrives within 5 s.
- Tests: a unit test for the planner, a page test for the retry, and an integration test using the
  ranges produced by the real renderer on a document with front matter, headings and lists.
- No visible UI change besides the removed error, so no screenshots.

## Autonomous decisions

- Fixed the range check at its cause (trailing blank lines) and added a single automatic retry for a
  genuinely stale preview, instead of showing the message at once.
- Selection moves are not retried.
- Copy and cut probably refuse such list ranges too; left out of scope, to go to the backlog.
- The new integration test could not be shown failing on the old code (the reverted run stopped
  earlier in an unrelated real-input stage); the unit and page tests were verified to fail before the fix.

## Internal references

- CR 116, backlog item bug-move-block.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

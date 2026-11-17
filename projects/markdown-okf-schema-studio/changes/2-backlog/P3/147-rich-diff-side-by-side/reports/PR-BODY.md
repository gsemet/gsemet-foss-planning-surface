## Summary

Blocks changed since the last commit still get the green bar on the left by default. A new
**Side-by-side** button in the floating toolbar (read mode only, disabled in edit mode) turns each
changed block into a small two-column card: the block as in the last commit on the left, as it is
now on the right, both rendered, with removed and added words marked. Added blocks have an empty
left side; deleted blocks reappear with an empty right side. Unchanged blocks are untouched, and the
source file is never rewritten.

## Deliverables

- Host computes line hunks against HEAD and posts the rendered HEAD content (cached per HEAD text).
- Page module `sideBySide` builds the cards; word-level marking comes from a new `wordDiff`.
- Docs: toolbar, settings, comparison, README, CHANGELOG.
- Screenshots (cream + dark, before/after): not yet attached; the real-window run could not be
  done on the authoring machine (locked macOS session). To be added before merge.

```ts
// host -> page
{ type: "previewBaselineDiff", html: string /* rendered HEAD */, hunks: LineHunk[] }
```

## Requirements traceability

- SwRS-MDOKFSTUDIO-REVIEW-003, -005, -006, -007, -008, -009 (new), TOOLBAR-001 and TRUST-001
  (button count 13 to 14), StRS REVIEW-017.
- Sources: `src/core/mapping/lineDiff.ts`, `src/core/mapping/wordDiff.ts`,
  `src/session/features/baselineDiff.ts`, `src/page/modules/sideBySide.ts`,
  `src/core/preview/previewToolbar.ts`, `src/page/features/editMode.ts`.
- Tests: `test/core/mapping/lineHunks.test.ts`, `test/core/mapping/wordDiff.test.ts`,
  `test/session/baselineDiff.test.ts`, `test/page/sideBySideCards.test.ts`,
  `test/page/runtimePageControls.test.ts`, `test/core/preview/previewStyles.test.ts`,
  `test/core/protocol/*.test.ts`.

## Autonomous decisions

- Read mode only (the user's answer was cut off); to confirm.
- A list or table with one changed item shows as one card; a moved block may show as "changed".
- Cards briefly disappear (~300 ms) after a content patch until the new baseline arrives.
- `requirements-coverage` drift on three unrelated requirements (MYST-005, DIAG-097, LIFE-039)
  is pre-existing and left out of this PR.

## Internal references

CR 147, review rounds 1 and 2 approved.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

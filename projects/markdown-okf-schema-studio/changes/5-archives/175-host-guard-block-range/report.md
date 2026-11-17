# 175 — Host-side guard on block ranges — report

Landed 2026-10-28. PR https://github.com/gsemet/markdown-okf-schema-studio/pull/187 merged as
68c213b6 (normal CI green, run 40780919021; heavy left to the stack top).

- `checkBlockLines` (src/core/mapping/blockRange.ts), called from `currentSourceEdit`
  (src/session/features/blockEdits.ts): edit open and Done/autosave refuse a range whose first line
  is blank, a reversed or non-integer range, or one past the end of the document, with "The preview
  and the document disagree about this block's lines. Refresh the preview and try again." No write.
- Copy, cut, paste, move already refused such ranges.
- Checked against ~60 real rendered block kinds (headings, lists, alerts, fences, directives,
  tables, frontmatter, CRLF, no final newline): no false refusal.
- A range ENDING on a blank line is accepted (list ranges end on a separator line), so a block
  shifted onto its own trailing blank line is not caught.
- 4 new tests fail on the old code; Opus Inspector APPROVE (round 1). New SwRS BLOCK-256 (proposed),
  parent StRS BLOCK-006 (proposed); no locked StRS touched.
- Follow-ups: P3 blank-line-check-unicode-spaces; optional page sends block tag.

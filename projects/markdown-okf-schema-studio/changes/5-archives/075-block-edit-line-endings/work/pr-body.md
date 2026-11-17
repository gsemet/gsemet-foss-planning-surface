## Summary

Editing a multi-line block in a document with CRLF or lone-CR line endings wrote LF line breaks
into the block (mixed endings, which matters on Windows) and the next autosave could be refused as
"The source block changed while it was being edited." Inserting a new block in a lone-CR document
landed at the end of the text or was refused as stale. Both now keep the document's line ending.

## Deliverable showcase

```text
CRLF document, block "- a\r\n- b", user adds a line in the text box (the text box returns LF)

before: - a\r\n- b\n- c     (mixed endings)
after:  - a\r\n- b\r\n- c
```

```mermaid
flowchart LR
  T[text box: LF] --> W[withLineEndingOf block] --> P[planBlockTextEdit] --> D[document]
```

## Changes

- `withLineEndingOf` turns the line breaks of the edited text into the one ending of the last
  written block text (a one-line block takes the document's ending; mixed endings are left as is); the host applies it
  before each write.
- `planInsertion` finds lines with the same LF / CR LF / CR splitter as the other edit planners
  and uses CR as the inserted ending in a lone-CR document.
- Requirements: two "Known issue" lines removed, scenarios added.

## Impacts

No visual change. Documents with CRLF or CR endings stay consistent after block edits and inserts.

## Blast radius

Grade: 1. Pure text planning in two core modules plus one call in the block-edit controller;
`git revert` restores the previous behaviour.

## Test plan

- [x] New tests: the lone-CR insertion tests and the controller tests (CR LF / CR documents, a block
      without a final line break) fail on the previous code; the LF, mixed-ending and unit helper
      tests pin behaviour that already held or is new
- [x] Requirements: SwRS updated, markers in code and tests, coverage and indexes regenerated
- [x] Local gates: `just check` (2614, 44 and 2 in the other suites, 31 Python tests,
      okfreq validate, lint and update-coverage clean)
- [ ] Review
- [ ] CI green

## Internal references

CR 075 (block-edit-line-endings); SwRS BLOCK-234 and BLOCK-094.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

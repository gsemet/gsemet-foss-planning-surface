## Summary

Pasting a large document copied from a code editor into an empty Markdown file no longer wraps it in a
code fence. A multi-line copy from a VS Code editor arrives on the clipboard as monospace HTML; the
HTML-to-Markdown conversion fenced it, and when the text itself held fences the wrapper became four
backticks. Such a copy is now inserted as copied, blank lines kept. Plain-text and block pastes were
already fence-free.

## Deliverables

- `htmlToMarkdown` returns an editor copy as the copied text, with no fence.
- Unit test (one expectation that encoded the bug corrected, one case added) and a real-window
  integration assertion that pastes a document containing fenced code blocks.
- Requirement SwRS-MDOKFSTUDIO-PALETTE-217 updated.

No screenshots: the behaviour is the inserted text, asserted by the real-window test. The bug was not
reproduced with a physical clipboard paste; the clipboard HTML was posted by the test.

## Changes

- `htmlToMarkdown` returns a code-editor copy as plain text; unit and integration tests; one requirement and the changelog.

## Impacts

Pasting rich HTML other than an editor copy is unchanged.

## Blast radius

1 of 3: one conversion branch in the paste path.

## Autonomous decisions

- Fixed the editor-HTML conversion rather than the plain-text path, which was not at fault; rich HTML
  paste conversion is otherwise unchanged.

## Test plan

- Unit: 2766 pass, 0 fail. Real-window integration suite exits 0.
- `requirements-lint` fails on `okfreq` rejecting `--check-links`; it fails the same way on main.

## Internal references

CR 127.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

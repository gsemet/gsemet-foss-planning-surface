## Summary

When another tool (an AI agent, a formatter, a script) edits the document you have open, the preview
now plays its update glow on the changed blocks. Before, VS Code gave no sign of who made a change,
so such an edit was treated like typing and never glowed.

## Deliverables

A change is treated as foreign, and glows, unless a keystroke reached the text editor within the
last 500 ms and the change touches a cursor or selection (with one line of margin). Typing in the
preview already reaches the document as the editor's own edit and never glows. The host reports
keystrokes through the host port (new `src/host-vscode/keystrokes.ts`), and the session decides
when it builds the update patch.

| | Cream | Dark |
| --- | --- | --- |
| Before | ![before cream](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/e10239cabb1b1c35e10be967ca503e5894503d8b/before-cream.png) | ![before dark](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/e10239cabb1b1c35e10be967ca503e5894503d8b/before-dark.png) |
| After | ![after cream](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/e10239cabb1b1c35e10be967ca503e5894503d8b/after-cream.png) | ![after dark](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/e10239cabb1b1c35e10be967ca503e5894503d8b/after-dark.png) |

## Changes

- Foreign-edit rule in the update-range computation and the host port.
- New unit tests and a real-window step that fails on the old code.
- Requirement LIFE-094, user guide and changelog updated.

## Impacts

Preview glow only. Known limit: VS Code sends no key event for Backspace, Delete or a paste, so one
of them pressed first after a pause can still glow once.

## Blast radius

2 (session and host event wiring).

## Test plan

Unit tests (2834 pass) and the real-window update-glow scenario.

## Autonomous decisions

- The foreign-change rule above (keystroke window of 500 ms, range touching a cursor or selection).
- A keyboard selection change stands in for a key event, as VS Code exposes none.
- The old known-issue line in the requirement was narrowed to the Backspace/Delete/paste limit instead of removed.

## Internal references

CR 139, requirement LIFE-094.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

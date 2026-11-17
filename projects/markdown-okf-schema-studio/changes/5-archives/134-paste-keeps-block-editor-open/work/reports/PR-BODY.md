fix(edit-mode): keep the page still after a paste in a block editor

## Summary

Pasting a long text into the open editor of a tall block made the page jump away from the caret:
the autosave applied the paste, VS Code scrolled the text editor to the edit, and the preview
followed that scroll. The preview now ignores the text editor's scroll while its own edit is being
applied and for 750 ms after it settles, so the caret stays in view and the editor stays open.

Only the scroll jump was reproduced. The reported "editor closes after a paste" did not happen in
a real window (the document version stays the same, so no re-render occurs).

## Deliverables

Before (page jumped back up, end of the paste out of view) and after (page where it was, end of the
paste in view, editor open), cream and dark themes:

| | Cream | Dark |
| --- | --- | --- |
| Before | ![before-window-tall-pasted-cream](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/5fd74b1002978c4c823c7cefc92b7be1fa091ded/before-window-tall-pasted-cream.png) | ![before-window-tall-pasted-dark](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/5fd74b1002978c4c823c7cefc92b7be1fa091ded/before-window-tall-pasted-dark.png) |
| After | ![after-window-tall-pasted-cream](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/5fd74b1002978c4c823c7cefc92b7be1fa091ded/after-window-tall-pasted-cream.png) | ![after-window-tall-pasted-dark](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/5fd74b1002978c4c823c7cefc92b7be1fa091ded/after-window-tall-pasted-dark.png) |

- `src/session/features/scrollSync.ts`, `blockEdits.ts`: own-edit window for text-editor scroll.
- New unit test and a real-window paste case (cream and dark) in `tallBlockScroll.test.ts`; both
  fail on the old code. The tall block test now fails when the editor closes.
- SwRS PALETTE-021: new row for the paste case, wording fix; stale comment in `caretRect.ts` fixed.

## Changes

Scroll-sync and block-edit modules of the session layer, one requirement row, tests.

## Impacts

The preview no longer follows the text editor's scroll for a short window after its own edit.

Blast radius: 2.

## Autonomous decisions

- Fixed the three small points listed in the item together with the bug.
- Kept the editor-closes symptom out of scope since it could not be reproduced; an intermittent
  close of the editor in the click-opened tall block case (about 3 of 8 runs, before and after the
  change) is a separate, unexplained issue to file as a backlog item.
- `just check` stops at `okfreq update-coverage --check` because the okfreq in use reorders file
  lists (also on main); unrelated reordering was reverted.

## Test plan

- New unit test and real-window paste case (cream and dark); both fail on the previous code.
- `just check` passes except the requirements coverage step, which fails identically on the unchanged base because of file-list ordering in the local okfreq build; CI confirms it.

## Internal references

CR 134, backlog item paste-rerender-closes-editor.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## Summary

After pasting or picking an image, its alt text is selected. Pressing Enter replaced that text
with a line break, which surprised users who expected Enter to confirm. In the block source
editor, Enter inside the alt text of a Markdown image (`![alt](path)`) now keeps the text and
moves the caret just after the closing parenthesis, like a "validate and continue".

## Deliverables

Before: Enter on the selected alt text replaced it. After: the alt text is kept and the caret
sits after the image.

| | Cream theme | Dark theme |
| --- | --- | --- |
| Before | ![before cream](shots/before-enter-cream.png) | ![before dark](shots/before-enter-dark.png) |
| After | ![after cream](shots/after-enter-cream.png) | ![after dark](shots/after-enter-dark.png) |

(Screenshots are in `reports/shots/`; the stack driver publishes them to the assets branch.)

- New `imageAltExit` edit action in `src/page/modules/linkEditActions.ts`, used by the Enter
  handler in `src/page/features/blockSourceEditor.ts` before list continuation.
- Unit, runtime and Playwright visual tests (cream and dark); requirement BLOCK-069 and the
  user docs updated.

## Autonomous decisions

- The alt field is single-line, so Enter always validates and moves after the image, whether
  or not the text was modified; the same after paste and after edit.
- Shift+Enter stays native, Cmd/Ctrl+Enter still finishes the block, Enter elsewhere is unchanged.
- Scope is the Markdown image alt only; the `:alt:` option of a `{figure}` directive is untouched.

## Test plan

- `just check` passes (2686 unit tests). New unit, runtime and visual scenarios fail on the old code.
- Real-window tests not run locally; use the on-demand heavy CI.

## Internal references

CR 118, requirement SwRS-MDOKFSTUDIO-BLOCK-069, visual scenarios palette-slash v22 to v24.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

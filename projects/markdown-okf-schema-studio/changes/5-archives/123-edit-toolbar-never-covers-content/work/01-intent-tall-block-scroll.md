# Editing a block taller than the viewport: scrolling jumps back to the top of the page

Type: fix · Priority: P1 · Reported 2026-10-27 after the demo tour of the P1 stack (regression)

## Intent (user)

After pasting a very large text into a block (empty file, edit mode), the block is taller than the
viewport. Scrolling down jumps back to the top of the page again: the old problem is back.

Expected: the viewport goes down with the scroll, and the block edit toolbar floats over the text.
This is probably a conflict with the rule "the toolbar never covers the edited text" (CR 123). For a
block taller than the viewport, we accept that the floating toolbar covers the first lines of the
text.

## Expected

- While a block editor taller than the viewport is open, scrolling (wheel, trackpad, scrollbar,
  caret moves) never moves the page back to the top.
- The edit toolbar stays sticky at the top of the viewport and may cover the text under it.
- The "toolbar never covers the content" rule of CR 123 keeps applying to blocks that fit in the
  viewport (and at opening time only).

## Before starting the CR

Suspected cause: CR 123 (`change-requests/123-edit-toolbar-never-covers-content`, PR #128) added a
tall-block clearance and a layout anchor in `src/page/features/editorChrome.ts`. Reproduce it in a
real VS Code window on the stack top and on main to confirm which change brings it back. The e2e
scrolls a block editor taller than the viewport down step by step and must fail on the current code.

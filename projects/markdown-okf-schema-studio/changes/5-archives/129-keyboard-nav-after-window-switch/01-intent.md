# Keyboard block navigation lost after leaving the window

Type: fix · Priority: P1 · Reported 2026-10-27 during the demo tour of CR 120 (keyboard-only editing)

## Intent (user)

Keyboard-only editing works, but at one point the whole page was selected (focus ring around the
entire preview, see the screenshot) and I could no longer switch the active element: Up/Down only
scrolled the viewport.

It seems to happen when I leave the window completely and come back: by default the active element is
then the whole page and keyboard navigation does not work. Opening an edit box and leaving it brings
back the block-by-block selection.

![Whole page focused](evidence/image.png)

## Expected

- After the window (or the preview) regains focus in edit mode, Up/Down move the block selection
  again, starting from the last selected block or the block nearest the top of the viewport.
- The whole page never takes the block focus ring.

## Before starting the CR

Reproduce it first, in a real VS Code window (light and dark preview themes): edit mode on, move the
block selection with the keyboard, switch to another application (and also to another VS Code
editor tab), come back, press Down. Record which focus path shows the bug and capture a before
screenshot that matches the one above. The e2e must fail on the current code.

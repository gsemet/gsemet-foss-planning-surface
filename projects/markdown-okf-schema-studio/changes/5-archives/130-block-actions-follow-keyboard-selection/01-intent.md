# Block actions (+ / up / down) stay on a stale block after the keyboard selection moves

Type: fix · Priority: P2 · Reported 2026-10-27 during the demo tour of CR 120 (keyboard-only editing)

## Intent (user)

Moving the focus a bit, the + / up / down icons stay on the previous block: in the screenshot the
keyboard focus ring is on the paragraph of section 3, while the block actions are still shown on
"Premier paragraphe" in section 5.

![Block actions on a stale block](image.png)

## Expected

- The block actions show on one block only: the block of the keyboard selection when it moves, the
  hovered block when the mouse moves. Whichever moved last wins; the other indicator goes away.
- Up / down from those icons act on the block they are shown on.

## Before starting the CR

Reproduce it in a real VS Code window (hover a block, then move the selection with the keyboard and
the reverse) and capture a before screenshot matching the one above. The e2e must fail on the current
code.

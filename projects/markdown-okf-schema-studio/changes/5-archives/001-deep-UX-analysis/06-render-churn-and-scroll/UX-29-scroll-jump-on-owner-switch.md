# UX-29 — The preview jumps when scroll ownership changes

| Field | Value |
| --- | --- |
| Severity | Low |
| Confidence | Observed (case 1 reproduced; case 2 seen once, not reproduced) |
| Area | Scroll synchronisation |
| Evidence | [u02-scroll-preview.jpg](../evidence/u02-scroll-preview.jpg) → [u03-typing-after.jpg](../evidence/u03-typing-after.jpg) |

## Observed

1. After scrolling the **preview** with the wheel (the preview owns the anchor, the editor follows
   with its first visible line), the first keystroke in the source editor makes the editor the
   owner. The preview then jumps about four source lines (about 90 px) to align its reading line
   with the editor's first visible line. The jump is small, but it happens exactly when the user
   starts typing and is reading the preview.
2. Once, the first click on a table cell after a wheel scroll in the preview moved the preview by
   about 178 px before the cell editor opened. A second identical click did not move it.

## Expected

Switching ownership should not move the pane the user is looking at: the new owner should adopt the
other pane's current anchor instead of re-deriving it from its own first visible line.

## Suggested direction

When the editor becomes the owner after a preview-owned period, initialise the anchor from the
preview's last reported anchor (rule R4/R6 in `docs/scroll-anchoring.md`). Add an E2E step that
types after a preview scroll and asserts the preview `scrollY` change stays under a few pixels.

## Done when

Typing after scrolling the preview does not move the preview.

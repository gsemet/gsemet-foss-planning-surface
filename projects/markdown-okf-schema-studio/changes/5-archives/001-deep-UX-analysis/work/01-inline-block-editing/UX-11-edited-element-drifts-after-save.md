# UX-11 — The edited block drifts on screen after commit

| Field | Value |
| --- | --- |
| Severity | Low |
| Confidence | Observed once per scenario (two scenarios) |
| Area | Scroll anchoring rule R7 ("inline edits keep the edited element fixed") |
| Evidence | [u16-list-add-item.jpg](../../evidence/u16-list-add-item.jpg) → [u17-tab-in-block.jpg](../../evidence/u17-tab-in-block.jpg) |

## Observed

- After committing the list edit of [UX-04](UX-04-enter-breaks-list-structure.md), the "Dry goods"
  item moved from y≈458 to y≈363 (about 95 px) in the preview viewport, and the source editor
  scrolled to follow.
- After pressing Escape on an unchanged block in `02-admonition-gallery.md`, the next measurement
  showed the page at a different scroll offset (the target heading went from the viewport to
  y=-1229). This second case was not reproduced in a later attempt.

## Expected

Per `docs/scroll-anchoring.md` R7, the edited element keeps its viewport top while editing and
after Save.

## Suggested direction

Add an E2E measurement around commit and cancel: record the edited element's `getBoundingClientRect().top`
before and after the re-render and assert a small tolerance. Investigate whether the full-document
replacement ([UX-28](../06-render-churn-and-scroll/UX-28-full-webview-reload-per-keystroke.md))
applies the anchor before or after images and fonts settle.

## Done when

Commit and cancel keep the edited element within a few pixels of its position.

# TOC rail polish

Follow-up of CR 239 ([report](../../../4-archives/239-bug-toc-column-not-displayed-on-narrow/report.md)),
filed by the owner on 2026-11-03.

- Rename the e2e scenario ids v28 and v29, which still say "hidden-narrow".
- `capture_layout_checks.py` is at 1499 of 1500 lines: split it before it breaks the size ratchet.
- At 460 px the TOC overlay touches the toolbar tooltip.
- The content is not padded for the 16 px rail.
- The window-level Escape handler can swallow another handler's Escape: scope it to the overlay.

# 033 — comment-chips

From backlog `P3/bug-comment-rendering` (files copied here as `backlog-*` / images).

## Problem

With comments in the document, `<!--` appears as a chip label instead of the comment chip; the chip show/hide button exists only in edit mode; the comment box has rounded corners.

## Decisions (user grill, 2026-10-22 night plan)

1. Fix the parsing/rendering so each HTML comment (TODO, comment, the kinds the extension already supports) renders as its real chip, never as a `<!--` label (backlog screenshot `image.png`: three `<!--` chips around a list). Write the failing fixture first from that pattern (comments before/after a list, consecutive comments).
2. Decision: the chip show/hide button lives in the toolbar in BOTH preview and edit mode; its state is remembered (existing state store), chips visible by default.
3. Decision: the comment box (compose/thread box) loses its rounded corners (square corners; buttons and text inputs may keep a small radius).

Night rules: blocked on a real product decision → apply the driver's recommendation and list it in the PR under "Décisions prises en autonomie" (Autonomous decisions).

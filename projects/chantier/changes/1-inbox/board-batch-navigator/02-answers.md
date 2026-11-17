---
type: cr-answers
description: The user's answers to the grill of board-batch-navigator.
---

# Answers

## Round 1 (2026-11-17)

### scope-Q1: how the board feedback of 2026-11-17 is cut

The user chose the recommended answer: four CRs, in the next batch: board-picker-surface-item,
board-batch-navigator (this one), board-kanban-priority-colours (with board-pastel-colours folded
in) and board-config-role-descriptions. This CR absorbs the inbox item cost-receipt-batch-chooser
and the batch history navigation (previous / next) of board-batch-view; board-batch-view keeps
its connected cards, their arrowheads and the tooltip on the batch mode.

### nav-Q2: the navigator's form

The user chose the recommended answer: arrows and a "last" button, in the page header next to
the title, on the Costs page and the Batch page: `‹ batch-04 ›` and a pill "Dernier" ("Latest"),
shown only when the page is not on the last batch. `‹` is greyed out on the first batch, `›` on
the last. The batch shown is in the URL (`&b=batch-04`), so a link opens the same batch.

## Round 2 (2026-11-17)

### receipt-Q7: copying the receipt as an image where the browser forbids it

The browser copies an image to the clipboard only on a secure origin (127.0.0.1 or localhost),
not from another machine of the local network over http. The user chose the recommended answer:
there, the button is greyed out and its tooltip says why ("image copy only works on this
machine"); no download or other replacement.
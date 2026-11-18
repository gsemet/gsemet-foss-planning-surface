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
## Spec questions (2026-11-17, after the spec-writer)

### nav-Q9: what the Batch page shows for a closed batch

The user: keep the order of the CRs and the dependencies between them for a past batch. So the
close records each CR's order and dependencies (`after`) in the batch's record, and the Batch
page draws a closed batch's graph from it, with its arrows. For batches closed before this
change, whatever their archived files still give is used; where nothing gives the dependencies,
the page says so rather than inventing arrows.

Settled by the Chief of Staff (the spec-writer's choices): the `b=` batch choice stays between
Costs and Batch and is cleared on any other view or project; an abandoned record that is neither
closed nor the live batch is left out of the navigator; the board's content security policy gains
`img-src blob:` for the image copy, nothing else.
## Spec questions, round 2 (2026-11-17, after the spec critic)

### receipt-Q14: the board's own link is not a secure origin

The board listens on the local network by default and prints the LAN address, plain http, so
the image copy would be greyed out even on the user's machine. The user chose the recommended
answer: the board also prints the `http://127.0.0.1:<port>/?k=...` link next to the LAN one
(same key), and the greyed button's tooltip links to that 127.0.0.1 address.

Settled by the Chief of Staff: the image method and the CSP change (`blob:` or `data:`) are
left to what the Driver proves in Chrome, Edge and Firefox, recorded in the PR.
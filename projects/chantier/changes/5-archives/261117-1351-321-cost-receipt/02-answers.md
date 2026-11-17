---
type: cr-answers
description: The user's answers to the grill of the Cost page as a supermarket receipt.
---

# Answers

## cost-receipt-Q1: the direction

2026-11-17, the user chose the recommended answer after three HTML mock-ups (`prototypes/01-mockups/`): direction 3, the modern ticket (`prototypes/01-mockups/receipt-modern.html`): a sans-serif receipt card on warm paper, a scalloped cut line with a scissors mark before a large total, a perforated tear-off stub holding the per-CR list with small bars and their sum, the stub beside the card on desktop and below it on a narrow screen.

## cost-receipt-Q2: the receipt in the page (after the combined mock-up)

2026-11-17, the user changed the direction after seeing it inside the board: the receipt is one piece, not a card and a stub; the per-CR detail sits under the total (after a dashed rule, ending with the barcode). It stands on the left on a desktop and on top on a phone. Beside it (below it on a phone), the page keeps today's cards: Recompute with the computed age, the four figures, per CR, last merged. "The ticket catches the eye; take it away and the cards still give the information." Reference, to compare at delivery: `prototypes/01-mockups/final-costs.html` and `prototypes/01-mockups/final-costs-phone.html` (copies of the board-visual-refresh ones); the ticket's split uses three shades of the board's one accent, in its font (board-visual-refresh). The user approved these mock-ups as the specification's reference.

Open for the specification: which batch the page shows by default, and how another one is chosen (today's history block); the decorative "thank you · N PRs · 0 reverted" line takes its figures from the record, or goes.

Spec critic: yes, it changes what the user sees on a whole page and its layout on a phone.

## Spec questions (2026-11-17)

- cost-receipt-Q3 (default batch): the running batch, else the last closed one.
- cost-receipt-Q4 (choosing another batch): split off as its own CR, aligned with board-batch-view's previous/next navigation; this CR keeps today's Earlier batches unfold.
- cost-receipt-Q5 (thank-you line): "thank you · N PRs", N the CRs with `result == "merged"` and a `pr`; no "0 reverted".
- cost-receipt-Q6 (recording): `close` writes `cost_receipt` in `batch-NN.json`; no back-fill; older records show "roles not recorded for this batch".
- cost-receipt-Q7 (order): after board-visual-refresh, stacked on it in the same batch (`depends.json` on board-visual-refresh).
- cost-receipt-Q8 (the rest): "the rest, $X: steering and agents outside a CR", with the parts named when there are several.
- cost-receipt-Q9 (outside the budget): two lines in the foot's cell: the grill and the specifications; the Chief of Staff's steering (Foreman batch).
- cost-receipt-Q10 (paused, or running without a live figure): the pill shows the real state (running, paused); the steering, Drivers and split lines read "not computed yet" or the live error, with Recompute; "roles not recorded" stays for old closed records only.

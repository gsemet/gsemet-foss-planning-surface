# Design critique of the combined mock-ups (2026-11-17)

The `final-*.html` files combine every choice of the grill (layout A, comfortable spacing, one teal accent with state icons and the legend in a tooltip, two-tone cards, Inter at two weights). They are the reference for the delivery: the PRs' screenshots are compared with them. The generator is `scratchpad/gen_final.py` on top of `gen.py`; the HTML files are the reference, not the scripts.

## Requested by the user

- Batch: the Merged column's "For information." label goes; so do the earlier batches' CRs (they add nothing to a batch's view).
- Costs: the receipt is one piece, not a card and a stub. The per-CR detail sits under the total, after a dashed rule, and ends with the barcode. It stands on the left on a desktop (sticky) and on top on a phone. Today's cards sit beside it (Recompute, the four figures, per CR, last merged), so the page reads the same without the ticket: the ticket is for the eye, the cards are for the information.

## Found by the critique, and applied

1. Batch: the third level of the graph was clipped by the two PR columns. With the earlier batches gone, one PR column is enough (to review, then merged, under a rule), and the graph gets the width back.
2. Batch: the "Batch" figure card and the counters line under the title repeated the crumbs (batch-12, running) and the mode strip (Stack). Both are gone. The mode strip says "Stack · Foreman", and four figure cards remain.
3. Batch: "PRs to review" said "nothing to review" twice (a paragraph and an empty-state line). One sentence is left.
4. Picker: the subtitle was cut ("planning-surface · batch…"). It now reads "batch-12 running".
5. Costs: the split bar and the dots use three shades of the one teal accent, not violet, green and blue.
6. Configuration › Timing: a card per host is kept (the user's choice), but each setting shows once, with one column per model family. Before, a band per family repeated every setting and its description. The legend sits beside the tabs, where the eye is when it reads a value.
7. Phone: the Costs table drops the bar and state columns, and the Recompute note goes, so a row fits in 390 px.

## Left open

- The Costs mock-up shows the last closed batch (batch-22) while the picker shows a running batch-12. The two mock data sets are from two moments. The spec decides which batch Costs shows by default and how to choose another one (today's history block).
- The receipt's "thank you · 11 PRs · 0 reverted" line is decoration. Its figures must come from the record, or the line goes.

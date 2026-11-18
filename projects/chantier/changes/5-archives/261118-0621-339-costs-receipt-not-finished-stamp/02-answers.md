# Answers

- stamp-Q1 (where): a red stamp, set at an angle on the receipt of a batch that is not closed,
  translated ("PAS FINI" in French, "NOT FINISHED" in English), on the page and on the receipt's
  copied image too.
- The user put this CR in the running batch (batch-24), 2026-11-17.

## Settled by the Chief of Staff

- stamp-S1 (when, 2026-11-17): the receipt carries the stamp exactly when the batch it shows is
  not closed: its record's state is anything other than `closed` (running, paused, closing, or
  any other value). On the page that is the receipt's `stateName !== 'closed'` (`model/receipt.js`,
  `headOf`); a closed record chosen in the navigator never carries it.
- stamp-S2 (words, 2026-11-17): the stamp's text is the user's own, "NOT FINISHED" in English and
  "PAS FINI" in French, one new key in each of the Costs dictionaries; no other wording.

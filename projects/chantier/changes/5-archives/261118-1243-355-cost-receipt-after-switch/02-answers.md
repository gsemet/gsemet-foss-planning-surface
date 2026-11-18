# Answers: cost-receipt-after-switch

No grill question: the request settles the behaviour. Filed by the batch-25 Foreman from
direct-switch-Q8 of CR-353 (2026-11-18); the user put it in batch-26 on 2026-11-18 ("A": grill the
morning's items and run them).

## Settled by the Chief of Staff

- After a batch switches steering (Foreman to direct, or back), the board's cost receipt line
  `chief_outside` shows the same figure as the `cost` command's text, which already counts what the
  Chief of Staff spent steering outside its claim window.
- One source for both: the board reads the figure `cost` computes; no second computation.
- A test covers a switched batch: the receipt's figure equals `cost`'s.

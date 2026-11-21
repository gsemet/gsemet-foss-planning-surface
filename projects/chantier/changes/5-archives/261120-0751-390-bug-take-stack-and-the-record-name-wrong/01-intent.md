# bug: take stack and the record name wrong bases in a stack batch

Seen in batch-28 (2026-11-19), when the stack driver was started (order O-24) on the stack
369 370 373 375 376 377 378 379 380 381 382, then 383 (working), then 384..387 to come.
The Foreman reported two anomalies:

1. `take stack`'s row for CR-383 says "not on its place ... note rebase: stacked on CR-369", while
   the stack order puts CR-383 on CR-382 (and its code needs CR-375). The Foreman did not send that
   note; following it would have rebased CR-383 onto the wrong CR.
2. The record gives CR-387 (working, first take) the base CR-386's branch, which does not exist
   yet, while its `take` gave it CR-383's branch.

Change: in a stack batch, `take stack` names as the "stacked on" CR the one just below in the
stack's order, and the record's base of a CR matches the base its `take` gave it (never a branch
that does not exist yet). A test on a prepared state covers both.

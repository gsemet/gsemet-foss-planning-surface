# Answers

## 2026-11-14: picked for batch-04

Owner, 2026-11-14: « Faisons les 3 CR. Uniquement pose moi les questions impactantes ». The
three open items after v1.9.1 (lost edit-toggle clicks, palette focus bounce, Cursor
compatibility) go into batch-04. Priority P1. The Chief of Staff decides every question without a
user impact; only questions with a user impact go to the owner.

Decided by the Chief of Staff (no user impact):

- Scope: the lost clicks on the edit toggle after a preview opens, on any step (`toc`,
  `myst-blocks`), not only `toc`. Widen `toc-loop` (or a sibling loop) to reproduce it on the step
  after `toc`.
- Fix the root cause (focus or frame state), no retry unless a host cause is proven and
  documented, no test removed or skipped, no timeout raised.
- If the cause is a product behaviour a user can hit (clicks lost in the real editor), stop and
  bring it to the owner before shipping a test-only change.
- Proof: integration green on a branch heavy run, and the reproducing loop green over at least 40
  rounds.

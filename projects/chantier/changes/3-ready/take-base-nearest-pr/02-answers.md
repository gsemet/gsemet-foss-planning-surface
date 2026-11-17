---
type: cr-answers
description: The user's answers to the grill of take-base-nearest-pr.
---

# Answers

## Round 1 (2026-11-17)

### batch-Q8: in which batch

The user: the six retro points of batch-23 join the next batch, with the four board CRs of
2026-11-17.

### stack-Q4: what a Driver bases its branch on

The user chose the recommended answer: `take` bases a CR on the nearest earlier CR of the batch
that already has a PR, else on main; one stack-driver run, at the batch's end, owns the final order
of the stack (one linear stack on the forge).

## Spec questions (2026-11-17, settled by the Chief of Staff from stack-Q4)

- The stack-driver runs during the batch stay, to keep the stack current after a merge or a CR
  that joins; only the run at the batch's end may set the final order.
- That end run starts when every non-release CR has handed back (ready or blocked), before the
  release's take.
- The user may still merge a ready CR on main before it; the restack is done at once, as today.
- The base rule applies to stack batches only, not parallel ones.
## Spec questions, round 2 (2026-11-17, settled by the Chief of Staff after the spec critic)

- A CR handed back ready that sits above drafts is still moved below them during the batch, as
  today (so "deliver by" and the partial ready-to-merge ask keep working); only the end run may
  reorder freely.
- A queued CR that cannot start because its dependency is blocked or cancelled does not hold back
  the final-order take: it stays out of the stack and goes into the ask to the user.
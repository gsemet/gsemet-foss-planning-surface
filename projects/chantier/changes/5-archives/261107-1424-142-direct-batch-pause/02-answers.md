# Answers (grill of 2026-11-07, after batch-08 landed)

- **The pause is the landed state.** A batch that ran `land` but not `close` is paused: the Chief
  of Staff grills the stacked ideas, and `order add` sets the batch running again. No new state.
- **This holds for a direct batch too.** Today (since CR-140) `order add` exits 2 on any direct
  batch, landed or not; it must accept a landed direct batch. While the batch runs, a direct
  batch stays strict.
- **A release CR may join without a pause** (it needs no real grill).
- Context: batch-08 itself was reopened this way on the user's word ("même batch").

- 2026-11-07, the user: grilled enough; joins batch-08 now ("C", "Relance le batch avec toutes ses CR").

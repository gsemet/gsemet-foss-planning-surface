# Intent: a ready CR sent back to its Driver can be handed back again

- **The defect** (batch-09, 2026-11-10): CR-163 was already handed back ready (PR 99). After
  CR-162 merged, it was sent back to its Driver to rebase. The Driver rebased, passed the gates
  and pushed, but `handback` was refused: "CR-163 is ready: no Driver to hand it back". The
  rebase is missing from the batch record.
- **The fix** (`02-answers.md`): `take <cr> --note "<why>"` on a ready CR reopens it.
  - The CR goes back to working, and no round is counted.
  - The Driver passes the two gates again at the new head: a passed long gate and a `VERIFIED`
    verdict (since CR-171).
  - Then it hands back ready again.
- **Runs in the next `real` eval:** the PR opens as a draft, and nobody merges it.

# Stack batch frictions: restack line, bases, carry, dead leases

Short name: `stack-frictions`. Priority P1, next batch (the user, 2026-11-22). Seen in batch-30, a
`stack` batch, and in the markdown-okf-schema-studio batch-09 retro (a stack batch, chantier
0.15.1, 2026-11-24).

## The request, summarised

Four frictions slowed batch-30's stack:

1. A GitHub rebase merge rewrites the merged CR's SHAs. The next stacked PR then showed the merged
   CR's commits again (#421 after #428, #430 after #421). Each time, the Foreman rebased onto
   origin/main without them and the Chief of Staff force-pushed.
2. `take` printed wrong bases for stacked CRs; the stack's shape only showed at `ship`.
3. After a clean restack, `ship` printed `off:` where it should print `carried:`.
4. The leases of Drivers that had ended blocked `ship` until someone reclaimed them by hand.

## Analysis

- Item 1 is mostly covered already. CR-466 pre-authorises the rebase and the
  `--force-with-lease` push on a CR's own branch, and the stack driver's card holds the one-pass
  restack after a partial merge. What is missing is a reminder at the moment the merge is
  recorded: `order merged` says nothing about the restack the stack now owes.
- Item 2: commit `92c7a795` fixed part of it. A base is still wrong after a stack reorder (the
  Studio retro, inbox item `take-prints-the-old-worktree-base-after-`). At main, `take` prints a
  stacked CR's PR base as read from the forge, which keeps the old base until
  `forge-stack rebuild`. For a CR taken but not placed, it prints its recorded `start_on` branch
  even after the reorder put that branch above the CR.
- Item 3 is a defect of the carry proof (`commands/carry.py`, `commands/crs.py`). When the base
  recorded at the gate is lower than the CR's real fork point, the CRs below are counted as the
  CR's own commits. A clean restack then reads as "the rebase changed the patch".
- Item 4: the cards already let the steering session end a lease once the host shows its holder
  ended. The refusals (`ship ... needs --lease <n>`, `take ... --reclaim`) do not name the
  command that does it, so a Driver or the Foreman has to ask. This folds in inbox item
  `foreman-s-stack-lease-goes-stale-with-no` (the Foreman's stack lease went stale three times
  and `take stack` needed `--reclaim`).

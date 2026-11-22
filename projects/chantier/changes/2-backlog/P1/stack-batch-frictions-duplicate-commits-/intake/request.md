# Stack batch frictions: duplicate commits, bases, labels, dead claims

Priority P1, next batch (the user, 2026-11-22). Seen in batch-30, a `stack` batch.

1. A rebase merge on GitHub rewrites SHAs, so the next stacked PR shows the merged CR's commits again (#421 after #428, #430 after #421). The Foreman had to rebase onto origin/main dropping them and the Chief of Staff force-pushed, each time. Intent: the CLI says so at `order merged` and names the rebase to run (`git rebase --onto origin/main <old tip> <branch>`), or the stack driver does it.
2. The stack's shape shows only at `ship`; `take` prints wrong bases for stacked CRs.
3. After a clean restack, `ship` prints `off:` where it should print `carried:`.
4. Dead Drivers' claims block `ship` until reclaimed by hand.

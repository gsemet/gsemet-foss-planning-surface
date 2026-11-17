# Answers

## 2026-11-14: picked, fix everything and release again

Owner, 2026-11-14: « oui je pense qu'il faut tout corriger et retenter une release ». Priority P1,
in batch-04 before the v1.9.1 release CR.

Decided by the Chief of Staff (no user impact):

- First find the exact failing steps and their logs (the runs of the v1.9.0 release in CR-323's
  archive and recent heavy runs on `main`), then the root cause of each.
- Fix the root cause (wait on a real condition rather than a delay, and so on). A retry is
  acceptable only where the cause is the host and is documented next to it; no test is removed or
  skipped.
- Proof: the CR's branch heavy run, and a stress run (`just ci-stress` / `-f heavy=true`) green on
  the steps in question.
- If a step reveals a real product bug, it is filed separately and brought back to the owner.

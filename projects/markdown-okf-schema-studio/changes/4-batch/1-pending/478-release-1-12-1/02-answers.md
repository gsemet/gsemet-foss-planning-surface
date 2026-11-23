Short name: `release-1-12-1`

Grilled with the owner on 2026-11-23 (bug day, batch-09).

1. release-Q1 (version): **1.12.1**, a patch release (owner's word "on release", answer raw-text-Q6).
2. release-Q2 (scope): **everything in 1.12.1** (raw-text-Q9): what is on `main` since v1.12.0
   (CR-474 and the other merged work) plus the stack: `raw-text-opens-studio`, CR-475, CR-476. The
   release waits for all of them.
3. release-Q3 (procedure): the project's own, `.agents/guidelines/release-process.guidelines.md`,
   the version PR on top of the stack; the owner merges the whole stack with it.
4. release-Q4 (approvals after the merge): **all the irreversible steps after the owner's merge of
   the version PR are approved in advance** (owner, 2026-11-23: "Toutes, d'avance"): the tag, the
   GitHub release with its notes and images, the Marketplace and Open VSX publications. Recorded with
   `order approve` at the merge. The announcement thread stays the owner's. The issue comments of step
   8 keep the procedure's one owner approval.
5. release-Q5 (docs diagram in the notes): none (not asked for).

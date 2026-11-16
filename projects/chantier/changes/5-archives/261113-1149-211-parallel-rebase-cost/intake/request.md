In parallel mode each merge forces the other ready CRs to rebase, rerun the long gate and CI and re-verify; batch-11 paid this several times. Measure it and see whether ready CRs can be merged in an order that limits rebases (batch-11 retro).

Also seen in real-direct run 1 (2026-11-12, PR 137): CR-101 delete-item paid three rebases, each with a conflict-resolver ($3.32 of $9.22). The plan could chain CRs that all touch the same files (there the README's Routes table and the item template).

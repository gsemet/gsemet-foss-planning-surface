# ship refuses a main-based PR that carries another CR's commits

From the retro of batch-24 (2026-11-18), kept by the retro critic; the user asked to file all six and run them in batch-24.

The user merged PR 297 (CR-337) right after its force push, whose head carried CR-336 under it, so CR-336 landed through CR-337's PR and the partial stack (#299, PR 295 + 296) dissolved with CR-335 still unmerged. `ship` refuses a PR based on main whose head carries another CR's commits, and the stack-ready-to-merge ask names the one PR to merge.


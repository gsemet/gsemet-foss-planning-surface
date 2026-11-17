Head: cb7a1f53e8b7a696dede6aeec303418aeae6c31d

All claims judged at cb7a1f5.

1. No text shows a batch number between project and `·` (cb7a1f5).
   Grep `(Project|Chantier|project) ?<nn>|Chantier \d\d|Chantier 0\d|Project \d\d` over the worktree: No matches found.
   Grep `·\s*(CoS|Foreman)|<nn> · ` lists only: `Project · CoS (Batch <nn>)`, `Project · Foreman (Batch <nn>)`, `Chantier · Foreman (Batch 17)`, and no-batch titles (`Proj · CoS`, `Chantier · CoS`). None has a number before `·`.

2. session-start.md examples (cb7a1f5): lines 147-149 contain `[Battle] 💬 Chantier · CoS (Batch 17)` and `[Battle] ⚙️ Chantier · Foreman (Batch 17)` (also `[Mac] ⚙️ Chantier · Foreman (Batch 06)`).

3. Titles with no batch unchanged (cb7a1f5): `git diff HEAD~1` touches only batch-bearing lines; `Project · CoS`, `Project · Griller`, `Project · Griller · <subject>` rows are not in the diff (4 files, 11 +/11 -).

4. `just check` at cb7a1f5, clean tree: ruff, mypy, biome, lock check ok; `382 passed in 20.97s`; release-notes ok. CI green per prompt.

5. PR 274 description (head cb7a1f5 per gh): renders, Summary/Deliverables/Changes match the 4-file diff; Known gaps None, no unverified claim.

Review box: placeholders `<sha7>` still unfilled in the Test plan are the Driver's to fill; not judged as a failure.

VERIFIED

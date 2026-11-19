# Conflicts: CR-369 rebased onto CR-374 (4e0de99c)

Commits replayed: 7bf2bb04 (conflicts), e43752ce (no conflict).

## docs/batch-lifecycle-texts.md, line 3 (intro paragraph)
- CR-374 (HEAD) side: direct-mode sentence "A running direct batch takes no grill in its session and no order qa; order add queues a specified CR, and a release CR and its fixes join."
- CR-369 side: added "chantier open with no CR creates the batch paused ..." and the older "strict" direct-batch sentence.
- Choice: CR-374's text kept, plus CR-369's one sentence: "open is refused while a batch is not closed; chantier open with no CR creates the batch paused, with no CR: order add joins CRs and the first take sets it running." CR-369's old direct-batch sentence dropped (CR-374 supersedes it).

## docs/batch-lifecycle.svg, `<desc>` line 4
- Same two sides, same choice, applied identically to the `<desc>` text. The svg is hand-written (no generator found); the rest of the svg (CR-369's added text lines) merged cleanly.

## Gate
Command: `just check` (in the worktree, after the rebase completed). Result: pass (ruff, mypy, uv lock, biome, 647 pytest passed, release-notes ok), exit 0.

# `ship` always reads the PR's base and draft state from the forge

Filed 2026-11-15 by the Chief of Staff from batch-18's retro (kept by the retro critic and by a Fable review), on the user's word "lance le tout dans le batch actuel".

Problem: the record drifted from the forge. `ship` recorded "base main" for PRs stacked by hand on another branch (CR-264, CR-266 in batch-18), and CR-266's record kept a stale base and "PR in draft, waits on cr-265" while the forge had it ready on another branch. It recurs from batch-17. CR-264 reads the forge's base only for a CR of a recorded stack.

Fix (CLI, `delivery.py` `ship`, `forge_base.py`): for any CR with a PR or MR, always read the base and the draft state from the forge (drop the `is_stacked` condition); keep the existing "base ? (not read…)" line, no retry. Both `gh` and `glab` paths; the scenario's fake gh and fake glab serve the draft field (GitLab's field name unproved on a real instance). One line in driver.md: any change of base or draft on the forge is followed by `ship`.

Order in the batch: third, before the early-conflict CR (stacking on a conflict needs true bases).

# Retro — 290-label-popover-covers-table

| What happened | Root cause | Process fix |
| --- | --- | --- |
| Round 1 red: real-input scenario `label-rename-above-table` failed in CI | `topInset()` in `labelRename.ts` counted the toolbar even when it did not overlap the popover horizontally; the spec never named that case | Fixed in round 2 (SwRS MYST-038); None further |
| Whole stack went BEHIND `origin/main` when #357 landed; the owner asked for one rebase of all six PRs, so every head changed and needed new heavy CI and a fresh Verifier | A docs-only merge on main during a long stack run invalidated every green head | None: the Rebase rule worked as intended |

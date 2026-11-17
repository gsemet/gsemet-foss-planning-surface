# Retro — 289-find-scrolls-wide-table-to-hit

| What happened | Root cause | Process fix |
| --- | --- | --- |
| Clean run apart from the restack. | n/a | None |
| Whole stack went BEHIND `origin/main` when #357 landed; the owner asked for one rebase of all six PRs, so every head changed and needed new heavy CI and a fresh Verifier | A docs-only merge on main during a long stack run invalidated every green head | None: the Rebase rule worked as intended |

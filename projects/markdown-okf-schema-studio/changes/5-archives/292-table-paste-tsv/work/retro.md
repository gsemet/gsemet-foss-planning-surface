# Retro — 292-table-paste-tsv

| What happened | Root cause | Process fix |
| --- | --- | --- |
| Red heavy visual run at round 1 | It inherited 293's v30 scenario failure (shared scenario), not its own code | None: held until 293's fix, then restacked |
| Whole stack went BEHIND `origin/main` when #357 landed; the owner asked for one rebase of all six PRs, so every head changed and needed new heavy CI and a fresh Verifier | A docs-only merge on main during a long stack run invalidated every green head | None: the Rebase rule worked as intended |

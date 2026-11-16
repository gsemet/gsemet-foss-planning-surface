# Conflicts: CR-285 rebase onto origin/main (f257647)

One conflict, evals/README.md, the kit table (sandbox.py and dry_run.py rows).
- sandbox.py row: kept this CR's text (refuses a check finished and not green; waits at most 5 minutes for a pending check); main left it unchanged.
- dry_run.py row: kept main's text (the audit's detectors with their planted breaches); this CR left it unchanged.
Both rows kept in their original order. The commit message is unchanged (no leading "#").

Gates (in the worktree, after the rebase): `just check` passed (200 passed); `just eval-dry-run` passed (11 of 11 cases as expected). Not pushed.

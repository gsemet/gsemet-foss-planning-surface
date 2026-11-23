# Forbid merge commits in PR branches (no plain Update branch)

Forbid merge commits in PR branches (owner, batch-08 retro, 2026-11-22).

In batch-07 the GitHub "Update branch" button put merge commits into PR branches twice (#458, #462); the repository merges by rebase only, so each cost a rebase round.

Wanted: the pull-request guideline forbids the plain "Update branch" button (only "Update with rebase", or asking the Driver to rebase), and a static CI check fails a pull request whose commits include a merge commit.

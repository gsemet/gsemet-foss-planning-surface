Short name: `no-merge-commits`

# Answers

Context from the owner (2026-11-23): "toujours penser générique, on va supporter aussi bien GitLab que GitHub": every rule, word and check is forge-neutral (pull request or merge request, GitHub or GitLab).

1. no-merge-commits-Q1: **Where the rule lives.** A: in the project, written forge-neutral (the pull-request guideline: update a branch only by rebase, the forge's rebase action or a local rebase and a protected force-push, never by merge; GitHub's plain "Update branch" named as an example), plus a separate chantier CR so that Drivers and conflict-resolvers never merge the base into a branch.
2. no-merge-commits-Q2: **The check.** A: a git-only script run by the justfile (just check-no-merge-commits <base>, git rev-list --merges <base>..HEAD), in ci-static; it fails naming the merge commits and the rebase command that removes them. CI passes the target branch (GITHUB_BASE_REF on GitHub, CI_MERGE_REQUEST_TARGET_BRANCH_NAME on GitLab); locally the base defaults to origin/main.
3. no-merge-commits-Q3: **Grilled enough.** A: specify, for the running batch.
Spec critic: no (small, low risk).
Destination: running batch batch-09.


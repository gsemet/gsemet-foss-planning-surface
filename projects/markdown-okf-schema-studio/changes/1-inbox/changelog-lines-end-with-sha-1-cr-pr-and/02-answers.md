Short name: `changelog-refs`

# Answers

Context from the owner (2026-11-23): "toujours penser générique, on va supporter aussi bien GitLab que GitHub": every rule, word and script is forge-neutral (pull request or merge request; GitHub, GitLab or Jira issues).

1. changelog-refs-Q1: **When the SHA-1 is added.** A: at release, by a script: for each line of "Unreleased", it finds on main the commit that added it (git blame, forge-neutral) and adds its short SHA-1, e.g. `(commit 1a5b98b, ...)`. No follow-up commit on main.
2. changelog-refs-Q2: **When the PR/MR number is added.** A: by the Driver (or the author) right after opening the pull request, in the same branch, before marking it ready.
3. changelog-refs-Q3: **Format.** A: labelled references in the forge's own notation: on GitHub `(commit 1a5b98b, CR-463 change-bar-tooltip, PR #476, issue #413)`, on GitLab `(..., MR !476, issue #413)`, with Jira `issue PROJ-12`; a piece that does not exist is left out (no CR for a pull request opened directly, no issue).
4. changelog-refs-Q4: **Enforcement.** B: no check: the rule lives in the guideline only (the release script that adds the SHA-1 is not a check).
5. changelog-refs-Q5: **Where the rule lives.** A: in the project only: the pull-request guideline (CHANGELOG part) and the release-process guideline (the SHA-1 step); no chantier CR.

6. changelog-refs-Q6: **Grilled enough.** A: specify, for the running batch.
Spec critic: no.
Destination: running batch batch-09.


# CHANGELOG lines end with SHA-1, CR, PR and issue references

Each CHANGELOG line ends with its references in parentheses (owner, batch-08 retro, 2026-11-22).

Owner's rule, word for word in substance: at the end of every CHANGELOG line, in parentheses: the commit SHA-1, the CR number and slug, the PR number, and the linked issue when there is one (GitHub, GitLab or Jira).

Why: in batch-07, CHANGELOG lines were written without their PR number, which forced follow-up docs(changelog) commits on main (95d34013, 369e8bad) and a round of CR-463.

To settle in the grill: where the rule lives (lifecycle guideline "Code" bullet, release-process guideline, CONTRIBUTING), when each reference is known (the PR number only after `ship`, the final SHA-1 only after the rebase merge: which SHA, and who adds it), the exact format, and whether a check (release-notes-check or a static CI check) enforces it.

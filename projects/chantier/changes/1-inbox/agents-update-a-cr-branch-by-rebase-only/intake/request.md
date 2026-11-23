# Agents update a CR branch by rebase only, never by merging the base

Filed on the owner's word of 2026-11-23, relayed by the Chief of Staff of markdown-okf-schema-studio (grill no-merge-commits-Q1).

Chantier's agents (Drivers, conflict-resolvers, stack-driver) never merge the base into a CR branch. They update a branch by rebase only: a local rebase and a protected force-push, or the forge's rebase action. Never a plain merge, never GitHub's 'Update branch' button. Forge-neutral: GitHub and GitLab alike (the owner's standing word).

Why: in markdown-okf-schema-studio batch-07, merge commits landed twice in PR branches (#458, #462) and each cost a rebase round.

The project side (a guideline and a git-only CI check) is a CR of markdown-okf-schema-studio batch-09; this item is the chantier side: the cards and agent files (both hosts together) say it, and the rails refuse it if they can.
# Agents update a CR branch by rebase only, never by merging the base

Short name: `rebase-only`. Owner's word of 2026-11-23, relayed from markdown-okf-schema-studio.

In the PRs chantier delivers there is never a merge commit, in any project and in a stack too (a CR updated on the CR below). Drivers, conflict-resolvers and the stack-driver update a CR branch by rebase only: a local rebase and a protected force-push of the chantier branch, or the forge's rebase action; never a plain merge, never the forge's "Update branch" merge button. Forge-neutral (GitHub and GitLab). A branch that already holds a merge commit is rebased by the Driver itself. `ship` refuses a branch that holds a merge commit and says to rebase. No project key and no project exception for now. The cards and the agent files of both hosts say it together.

Why: in markdown-okf-schema-studio batch-07, merge commits landed twice in PR branches (#458, #462), each costing a rebase round.

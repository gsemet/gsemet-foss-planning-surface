# Each CR carries a condensed JSON summary

Split from visualization-backend on 2026-11-13, on the user's word ("Oui, ces 5 CRs").

Each CR gets a condensed JSON (title, summary, origin: Jira, GitHub or GitLab issue, or verbal,
labels, group) refreshed by the agent that edits the CR's Markdown, with a checksum of the
Markdown so a late summary shows; a CLI linter and its commands; the cards' rule (the agent that
edits runs the linter, the Chief of Staff at worst). The board shows the late-summary and origin
icons and the labels, as in `1-inbox/visualization-backend/prototype/`.

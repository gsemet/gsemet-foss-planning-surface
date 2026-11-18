# Answers: board-forge-links

## forge-Q1: what a click on a Home "Open PRs" row does
**Answer (A):** the row opens the PR (GitHub) or MR (GitLab) on the forge in a new tab; the CR's
number (e.g. CR-335) stays a link to the CR's side panel.

## Settled by the Chief of Staff
- In a CR's side panel, a URL of a PR/MR, a GitHub issue, a GitLab work item or a Jira issue is a
  link that opens in a new tab, wherever it appears (rendered Markdown, front matter, the CR's
  facts).- One CR, not split: it starts in batch-24 at once and its Driver rebases on CR-338 (which edits
  `markdown.js` and `panel.css`) when CR-338 lands; a shared file is no dependency.
- The side panel's facts row also shows the CR's own PR or MR (and a backlog item's issue when its
  files name one) as links opening in a new tab.
- Any other `http(s)` link in the panel's rendered Markdown opens in a new tab too, not only
  forge and tracker links (the user: "il faut pouvoir naviguer vers").
- A GitLab MR's number shows as `!n` (as `commands/facts.py` writes it), a GitHub PR's as `#n`.
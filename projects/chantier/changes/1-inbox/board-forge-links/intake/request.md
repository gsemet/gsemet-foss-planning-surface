# A PR, a merge request or an issue on the board opens on its forge

The user (2026-11-17), on a screenshot of the Home page's "Open PRs" block:

1. A row of the Home page's "Open PRs" block opens the CR's side panel, though the row is about the
   PR: it should open the PR (GitHub) or the merge request (GitLab) on the forge. The Batch page's
   "To review" cards already link to the PR, which is the expected behaviour.
   (Code: `js/views/home-prs.js:11`, `prRow` uses `opener(crKey(c))`.)
2. In a CR's side panel, a link to a Jira issue, a GitHub issue, a GitLab work item, or a PR or MR,
   must be navigable (clickable, opens on the forge or tracker).

Also seen on the screenshot: CR-335's title shows as "---" (front matter), already fixed by CR-338.
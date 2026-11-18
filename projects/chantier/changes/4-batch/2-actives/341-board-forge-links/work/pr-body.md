## Summary

On the board, a row of Home's "Open PRs" block is about a pull request, yet a click opened the CR's side panel. And a link to a PR, a merge request, an issue or a work item in the side panel could not be followed. A row now opens its PR or MR on the forge in a new tab, and web links in the panel open in a new tab.

## Deliverables

- Home "Open PRs": each row is a link to the PR (GitHub) or MR (GitLab) in a new tab; the CR number inside it still opens the side panel. A PR with no web address stays a plain box.
- Side panel: every `http(s)` Markdown link, autolink and bare URL of the drawn Markdown (inline code and fenced blocks excepted) opens in a new tab; a relative link stays plain underlined text.
- Facts row: the CR's own PR or MR, and a backlog item's issue when its files name one, are links.
- A GitLab MR's number shows as `!n`, a GitHub PR's as `#n`, everywhere the board writes it (the form is read from the link's shape, so a self-hosted GitLab is recognised).

Screenshots at `ade7512`: Home's open PRs with a row hovered (the status-bar address is a drawn overlay of the row's real link), and the side panel with its facts row and a Markdown fixture of links. No before image: the previous behaviour is a row that opens the side panel.

![Home open PRs row hovered at ade7512](../evidence/home-open-prs-row-hovered.png)

![Side panel facts row and links at ade7512](../evidence/side-panel-facts-and-links.png)

## Blast radius

Grade: **1**. Front-end only, in the board's page; a plain `git revert` restores the previous behaviour.

## Autonomous decisions

None.

## Known gaps

- The side panel's front matter (a separate change) is not yet in this PR: a URL in a front matter value is proven by the same link code but not drawn here.
- A link label holding inline code (`[`x`](url)`) is not linked.

<details>
<summary>Details</summary>

## Changes

- `core/format.js`: `isMergeRequest`, `prNumber` writes `!n` for an MR.
- `views/home-prs.js`, `ui/open.js`, `css/views/home.css`: the row as a link, the CR number as the panel's opener, the opener never follows an enclosing link.
- `panel/markdown.js`, `css/panel.css`: link marks in `inline()`, skipping inline code.
- `panel/head.js`: PR/MR and issue facts as links.
- `i18n/en.js`, `i18n/fr.js`: `mr.open`, `issue.open`.
- `docs/web-board.md`: Home and the side panel.

## Human decisions

- A click on a Home "Open PRs" row opens the PR or MR on the forge in a new tab; the CR's number in the row still opens the CR's side panel.
- Every web link and URL of the side panel's Markdown opens in a new tab, any web page included, not only forges and trackers.

## Impacts

Click behaviour on Home's open PRs and links in the side panel change; nothing else.

## Test plan

- [x] No behaviour change in the Python code; the board's page has no JS unit tests (checked by `just lint` and the page's size and style tests)
- [x] Local gates carried from `ade7512`: `just check` pass, `just eval-dry-run` pass (17 of 17)
- [x] Evidence at `ade7512`: real-browser run, 36 checks pass (Home rows for GitHub and GitLab in English and French, CR number opens the panel, box row, panel links, facts row)
- [x] Review: approved carried from `ade7512`
- [x] Verified carried from `ade7512`: browser proof; description pass pending
- [x] CI green at `ade7512`: all five jobs pass

## Internal references

CR-341 (board-forge-links).

</details>

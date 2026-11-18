# Change Specification: a PR, an MR, an issue or a link on the board opens on its site

## Goal

The user (2026-11-17, on a screenshot of Home's "Open PRs" block) asked for two things:

1. A row of Home's "Open PRs" block is about a PR, yet a click on it opens the CR's side panel. It
   must open the PR (GitHub) or the merge request (GitLab) on the forge, as the Batch page's
   "To review" cards already do.
2. In a CR's side panel, a link to a PR or an MR, a GitHub issue, a GitLab work item or a Jira
   issue must be navigable: a click opens it on its forge or tracker.

After this change (`02-answers.md`: forge-Q1, answer A, and the lines settled by the Chief of
Staff):

- A click on a Home "Open PRs" row opens its PR or MR on the forge in a new tab. The CR's number
  in the row (for example `CR-335`) still opens the CR's side panel.
- In the side panel, every `http(s)` link and URL of the rendered Markdown (the front matter
  included) opens in a new tab: a PR or an MR, a GitHub issue, a GitLab work item, a Jira issue,
  and any other web page too ("il faut pouvoir naviguer vers").
- The panel's facts row shows the CR's own PR or MR, and a backlog item's issue when its files name
  one, as links that open in a new tab.
- A GitLab MR's number shows as `!n` (as `commands/facts.py` writes it), a GitHub PR's as `#n`.

One CR, not split. It starts in batch-24 at once; its Driver rebases on CR-338
(`338-board-design-bugs`, which edits `markdown.js` and `panel.css`) when CR-338 lands. A shared
file is no dependency: no `depends.json`.

The CR has no `issue:` line. The paths below are under the board's page,
`skills/chantier/scripts/cli/src/chantier/board/web/` (`<web>`), read at main `a65a8d3d`.

## What changes

### 1. A GitLab MR, told from its link; its number

`<web>/js/core/format.js`:

- New `isMergeRequest(url)`: true when `safeUrl(url)` passes and the URL's path holds
  `/-/merge_requests/<digits>`. The forge is read from the shape of the link, never from its host,
  as `pr_parts` (`commands/forge_stack_gh.py`) and `GITLAB_LINK` (`commands/forge_stack_gitlab.py`)
  do, so a self-hosted GitLab is recognised too.
- `prNumber(url)`: `!<n>` for a merge request (`isMergeRequest`), `#<n>` otherwise, as today. The
  number is the path's digits after `/merge_requests/` or `/pull/`; a query or a fragment after it
  is not part of it. Every place that calls `prNumber` (Home, the Batch cards, the PRs page, the
  activity's `ev.ship`, the panel's facts) then writes `!n` for an MR.

This agrees with `board-prs-filter-sort`'s rule ("MR" when the project's forge is GitLab): the
board reads a project's forge from its links' shape (`board/forge_read.py:210`), and so does this
helper; whichever of the two CRs lands second aligns on the other's helper, with no second GitLab
test.

Constraint of `skills/chantier/scripts/cli/tests/test_code_targets.py`
(`test_the_web_frame_is_self_contained_and_follows_the_style_rules`): no file of `<web>` may hold
the text `http://` or `https://`, comments and regex literals included. Write a scheme test as
`safeUrl` does (`/^https?:\/\//i`, slashes escaped) or reuse `safeUrl`.

### 2. Home's "Open PRs" rows (forge-Q1)

`<web>/js/views/home-prs.js`, `prRow(c)`:

- When `safeUrl(c.pr)` gives an address, the row is an `<a class="x" href="<the PR's URL>"
  target="_blank" rel="noopener" data-key="prl-<CR>" title="<open the PR | open the MR>">` (the
  `data-key` keeps the keyboard focus over a live redraw, as `views/prs-row.js` does). The row no
  longer carries `opener(crKey(c), 'pr-')`.
- The CR's number inside it, today `<b>${c.cr}</b>`, becomes the panel's opener:
  `<b ${opener(crKey(c), 'pr-')} title="${t('pr.folder')}">${c.cr}</b>`. A click, Enter or Space on
  it opens the side panel and never follows the row's link, as the folder icon inside the Batch
  card's link (`views/batch-pr-card.js`).
- `<web>/js/ui/open.js`, `open(event, element)`: `preventDefault()` and `stopPropagation()` move
  before the `if (!target) return`, so a click on an opener inside a link never follows that link,
  even when `targetFor` finds no CR (a record refreshed under the click).
- When the CR's PR has no web address (`safeUrl` gives `null`), the row is a `<div class="x">`,
  not a link, and its CR number opens the panel as above (the Batch card is a plain box then).
- The state tag, the title and the number (`prNumber(c.pr)`: `#41` or `!41`) stay in place.
- `blockedRow` (the blocked CRs under it) is not changed: it still opens the CR's panel.

`<web>/css/views/home.css`:

- `a.x`: colour inherited, no underline, so it looks like today's `div.x` row.
- The row hover: today's `.home .x[data-open]:hover` (home.css:118) no longer matches the row,
  which loses `data-open`; a rule for `.home a.x:hover` gives it the same `var(--row-hover)`
  background.
- The CR number: it gets the pointer cursor from `[data-open] { cursor: pointer }`
  (`css/cards.css:57`), and an underline on hover (`.home .x b[data-open]:hover`) so it shows as a
  second target inside the row.
- The new rules use tokens only (`var(--…)`), even beside the raw values `.home .x` holds today; no
  new colour, no id selector, nesting at most 3 (`test_code_targets.py`).

The block's words: the row's `title` is `t('pr.open')` ("open the PR" / "ouvrir la PR") for a
GitHub PR and a new key `mr.open` ("open the MR" / "ouvrir la MR") when `isMergeRequest(c.pr)`, in
both word files (`<web>/js/i18n/en.js`, `<web>/js/i18n/fr.js`: the test checks they share their
keys). The heading "Open PRs" and the Batch cards' `pr.open` stay as they are.

### 3. The side panel: links in the rendered Markdown and the front matter

`<web>/js/panel/markdown.js`, `inline(text)` (the inline marks, already run on paragraphs, list
items, headings and table cells):

- A Markdown link `[label](url)` whose `url` passes `safeUrl` becomes
  `<a href="<url>" target="_blank" rel="noopener" title="<url>">label</a>`. A link whose target is
  not `http(s)` (a relative path to a file of the folder, an anchor, a `mailto:`) stays as today,
  `<u>label</u>`, not navigable.
- An autolink `<https://…>` (escaped to `&lt;https://…&gt;` by then) becomes the same `<a>`, its
  text the URL, without the angle brackets.
- A bare `http(s)` URL in the text becomes the same `<a>`, its text the URL. It ends at the first
  space, `<`, `>`, `"` or `'` (in the escaped text: `&lt;`, `&gt;`, `&quot;`, `&#39;`), and loses a
  trailing `.`, `,`, `;`, `:`, `!` or `?`, and a trailing `)` that has no `(` in the URL.
- A URL already inside a link, its `href` or its label (`[https://…/pull/1](https://…/pull/1)`), is
  not linked a second time: one `<a>`, never one inside another.
- The link marks skip the text between `<code>` and `</code>`: a URL in inline code stays literal,
  as one in a fenced block does (how, at the Driver's choice: for example by splitting the escaped
  line on the code spans first).
- Every piece of text stays escaped first (`esc`); the `href` is the escaped URL, so the output
  still holds no markup but the tags `markdown.js` writes.
- The file's head comment ("A link shows underlined and does not navigate.") says which links
  navigate.

The front matter: CR-338 (bugs-S5) adds to the same `renderMarkdown` a muted key/value list for a
leading front matter, each value run through `inline()`. This CR does not touch that reader: a URL
in a front matter value becomes a link through `inline()`. The Driver rebases on CR-338 when it
lands and keeps its front matter reader, its `<dl class="fm">` and its CSS as they are; it only
checks that a value's URL is a link.

`<web>/css/panel.css`: `.panel .doc a` looks like today's underlined link text (underlined,
`overflow-wrap: anywhere` so a long URL wraps inside the document's column, the pointer cursor).
Tokens only.

The links open in a new tab and leave the board's page as it is. The board's
`Referrer-Policy: no-referrer` (`board/reply.py`) stays, so no site sees the board's URL and its
key.

### 4. The side panel: the facts row

`<web>/js/panel/head.js`:

- `crFacts` (a CR of the batch) and `doneFacts` (a merged CR): when `safeUrl(row.pr)` gives an
  address, a fact `<a class="lbl" href="<pr>" target="_blank" rel="noopener"
  title="<open the PR | open the MR>">` whose text is `prNumber(row.pr)` (`#n` or `!n`). The batch's
  rows (`board/crs.py`, `"pr": link_of(c.pr)`) and the merged ones (`status/views.py`, `_done_rows`)
  already carry `pr`; no server change.
- `itemFacts` (a backlog item): when the item's `origin` (from its `summary.json`, read by
  `board/backlog.py`'s `summary_fields`) has a `url` that passes `safeUrl`, a fact
  `<a class="lbl" href="<origin.url>" target="_blank" rel="noopener" title="<open the issue>">`
  whose text is `origin.ref` (`#12`, `ABC-12`). A verbal origin, or none, shows no fact. A new key
  `issue.open` ("open the issue" / "ouvrir le ticket") in both word files.
- `gateFact` (the long gate's validating PR) is already such a link: unchanged.

### 5. Docs

`docs/web-board.md`:

- Home's paragraph (line 28): a row of the open PRs opens its PR or MR on the forge; its CR number
  opens the CR's folder.
- The side panel's paragraph (line 100): a web link or URL of the drawn Markdown opens in a new
  tab; the facts row links the CR's PR or MR and a backlog item's issue; an MR's number is `!n`.

No card change, no CLI (Python) change, no `STATUS.json` change. `just docs-screenshots` is not
owed by this CR (by hand, before a release).

## Out of scope

- A link whose target is not `http(s)` (a relative path to another file of the folder, an anchor):
  it stays underlined and not navigable.
- A URL in a fenced code block, in inline code, in a JSON file or in a plain-text file of the panel.
- An issue fact for a CR of the batch or a merged CR (only a backlog item's, as settled).
- The words "Open PRs" and the Batch cards' "open the PR" on a GitLab project; the PRs page's
  wording, filters and sorts (`board-prs-filter-sort`).
- Everything CR-338 does in `markdown.js` and `panel.css` (the front matter's reader and look, the
  file list) and in the titles.

## Evidence

**Checks.** The board's page has no JS unit tests: `just lint` (Biome on `<web>`) and
`skills/chantier/scripts/cli/tests/test_code_targets.py` (script and style sizes, no other origin
named in a file, both word files with the same keys) check the touched JS and CSS. No Python test
changes.

**In a browser** (the Driver's scratch script in `work/scratch/`, as CR-338's `shoot.py`, or
`scripts/docs_screenshots.py`'s browser on `docs/demo/`), on a board serving a batch with a CR
whose PR is a GitHub PR link and, in a scratch copy of the record, one whose PR is a GitLab MR
link; results written in the PR:

1. Home, "Open PRs": the row is `a[href=<the PR's URL>][target=_blank]`; a click on the title or
   the number opens a new tab on that URL (headless: the `popup` event carries it) and does not open
   the side panel; a click on `CR-…` opens the side panel and opens no tab; Tab reaches the row and
   the CR number, and Enter on each does the same. The GitLab row shows `!n` and its `title` says
   "open the MR"; the GitHub row shows `#n` and "open the PR"; in English and in French. The row
   and the CR number have their hover looks.
2. A row whose PR has no web address: a box, no link; its CR number opens the panel. A CR number
   whose CR left the record between the draw and the click opens no tab.
3. The side panel on a Markdown fixture holding, in a paragraph, a list, a table cell and inline
   code: one URL of each kind (GitHub PR, GitHub issue, GitLab MR, GitLab `/-/issues/`, GitLab
   `/-/work_items/`, Jira `/browse/ABC-12`) and a documentation page, as Markdown links, as bare
   URLs and as an autolink `<https://…/pull/1>`; one on a self-hosted host, one with a
   `#fragment`, one followed by a `.`, one in parentheses, one followed by `"`;
   `[https://…/pull/1](https://…/pull/1)`; a relative link `[spec](03-change-spec.md)`. Each
   `http(s)` URL outside code is one `<a target="_blank" rel="noopener">` with the right `href` (no
   trailing dot, bracket or quote, no `<a>` inside another); the relative link and the URLs in code
   are not links. A batch-24 `STATUS.md` shows its `[PR](…)` table cells as links.
4. The facts row: a batch CR with a PR shows its `#n` (or `!n`) as a link to it; a merged CR too;
   a backlog item whose `summary.json` has an origin URL shows its `ref` as a link; a verbal one
   shows none.
5. With CR-338 in: a front matter value holding a URL shows it as a link.

**Screenshots** in the PR's Deliverables, with no username or home folder in view: Home's "Open
PRs" block with a row hovered and its link's address in the browser's status bar (or its tooltip),
and the side panel with its facts row and a `STATUS.md` or the fixture showing its links.

**Gates** (AGENTS.md):

- Before the first push, the Driver runs `just check` in the worktree at the rebased head it
  pushes, and `just eval-dry-run` there (the change is under the CLI's `src/`).
- The long gate: the pipeline's `just scenario (ubuntu-latest)` job, green at the PR's head (a CLI
  change). No scenario step is added: the scenario does not drive the board's page; it must stay
  green.
- Windows coverage: if this CR is on top of batch-24's stack, it also passes `just scenario`
  locally (`chantier gate`) at its head before the user merges; when a CR joins on top, that local
  run moves to it.
- `just mod` is not owed: nothing under `hooks/` or `types/` changes. No screenshot of the CR board
  pane is owed: `hooks/register.tsx` and `STATUS.json` are not touched.

## Open questions

None.

# Change Specification: the PRs page filters by batch and state, sorts, and says MR on GitLab

## Goal

The user (2026-11-17): on the board's PRs page, pick the batch whose PRs are shown, filter them by
state, and order them by date or CR number, the choice kept in the page's address. On a project
whose forge is GitLab, the board says "MR" (merge request) wherever it says "PR" today, in every
language, and writes an MR's number `!n`.

## Decisions carried from the grill (02-answers.md)

- prs-Q1 (A): filter by batch and by state (open, merged, draft); sort by opening date, last
  activity or CR number; the choice is kept in the URL.
- prs-Q2 (C): the forge is read at once on each change of the batch shown; AGENTS.md's PRs-page
  rule widens to "the batch shown" (a change of batch reads at once; the 10 s limit applies to the
  polling of the batch shown). The exact wording is in section 7.
- Settled by the Chief of Staff:
  - The title, labels and tags say "MR" when the project's forge is GitLab, "PR" otherwise, in
    every language (today: English and French).
  - A closed (unmerged) PR shows under "all" only.
  - Today's order is the default sort; dates newest first; CR numbers ascending.
  - A row shows the date it is sorted by.
  - GitLab is also recognised from the `origin` remote's host.
  - "MR" applies wherever the board says PR: the PRs page, Home, the Batch page, the overview, the
    events feed (and every other word that names a PR).
  - One batch at a time (no "all batches" choice).
  - The critic's fixes apply, with `mr.open` as the shared key scheme and `!n` for an MR number,
    as in board-forge-links (CR-341).
  - With no batch running, the page shows the last closed batch's PRs, with the navigator, read
    once on the forge; `pv.none` stays only when there is no history at all. This is a change
    from today.
  - It stays one CR: the user asked for "MR" on GitLab in the same request as the PRs page. The
    risk is named in "Limits the Driver keeps".
- Uniformity with board-design-system (its `02-answers.md`, DS-Q2, DS-Q5, DS-Q6): no side accent
  border, the one chip, the one card.

All paths below are under `skills/chantier/scripts/cli/src/chantier/board/` (`<board>`) and its
`web/` (`<web>`), read at main `f36277c6`, unless named from the repository root.

## Dependency

This CR depends on CR-341 (board-forge-links): it starts once CR-341 is merged (depends.json).

## Today

- `GET /api/projects/<id>/prs` (`<board>/routes.py` `prs_of`) answers `<board>/prs.py`
  `answer(reads, key, state, repo)`, `key` being the project's id: the rows of the batch in
  `4-batch/` (running or paused) only, its CRs with a PR in merge order then batch order
  (`_in_order`). With no batch: "No batch running. The last batch was X." (`pv.none`, `pv.last`).
  Past batches' PRs are never shown.
- `<board>/forge_read.py` `read` asks `gh api graphql` or `glab api graphql` (one call for all the
  links) for `state`, draft, mergeability, base, `mergedAt`, `closedAt` and the checks. No creation
  or update date is read. Links spanning two repositories raise `NOT_ONE_REPOSITORY`; a PR the
  forge does not show raises "the forge does not show #n".
- `prs.py` `ForgeReads.get(key, links, load)` keeps one read per `key` for `TTL_S` (10 s); a
  different set of links calls the forge at once. The feed (`<web>/js/views/prs-feed.js`
  `startFeed`) reads once when the page opens, then every 10 s while the page is visible and a PR
  is not done (`all_done`), and at once when a CR of the running batch gets a new PR.
- The batch navigator (`<web>/js/ui/batch-nav.js` `navigator`, its own `VIEWS`) and the address's
  `b=` serve Costs and Batch only (`<web>/js/core/router.js` `BATCH_VIEWS`, `resolve`, `batchOf`,
  `href`). `<web>/js/model/history.js` gives `batchSequence`, `shownId`, `shownRecord`,
  `recordRows`. The store's `batchId` (`<web>/js/core/store.js`) holds the chosen batch, `null`
  for the latest.
- The project state's `history` (`<board>/state.py` `_history`) lists every
  `5-archives/batches/batch-NN.json` record, newest first, the running batch's included (its
  `state` is `running`). A record's id is its `batch` field (`"batch-22"`); a closed record has
  `state: "closed"` and `crs`, each with `cr`, `title`, `result` (`merged` or not), `pr`, and
  sometimes `order`. It holds no `kind`, `branch`, `to_review` nor CR `state`.
- The web code holds no "MR" word. `prNumber` (`<web>/js/core/format.js`) writes `#n` for any
  link. CR-341 adds `isMergeRequest(url)`, `prNumber`'s `!n` for an MR, and the key `mr.open`
  ("open the MR" / "ouvrir la MR") in `i18n/en.js` and `i18n/fr.js`.
- The forge is told from a PR link's shape: `GITLAB_LINK` (`commands/forge_stack_gitlab.py`)
  against GitHub's `pr_parts` (`commands/forge_stack_gh.py`). `state.py` `origin_of(root)` reads
  the `origin` remote's URL (no network, kept 30 s).
- `prs.css` draws the rows as one bordered list with hairline separators between rows; no side
  accent border.

## What changes

### 1. Filter by batch: the PRs page joins the batch navigator

Browser:

- `router.js`: `BATCH_VIEWS` gains `prs`; the header comment says Costs, Batch and PRs.
  `batch-nav.js`: `VIEWS` gains `prs` (better: import `BATCH_VIEWS` from `router.js` rather than
  keeping a second list). The navigator shows on the PRs page as on Costs and Batch; `batchOf`
  keeps the shown batch when moving between Costs, Batch and PRs of the same project. No `b=`, or
  one that `batchSequence` does not hold, shows the latest batch (`shownId`): the batch in
  `4-batch/` when there is one, else the last closed batch.
- `<web>/js/core/api.js` `prs(id, batch)`: sends `?batch=<id>` when `batch` is given.
- `prs-feed.js` `startFeed(batch)`: the batch it reads is `shownId(state.data, state.batchId)` when
  it starts, sent only when it is not the running/paused batch's id (`state.data.batch?.id`). The
  "a CR got a new PR" subscription stays, for the running/paused batch only. A closed batch is
  read once: the feed does not poll after the first answer whose `closed` is true (a failed read
  is still retried at the next tick).
- `<web>/js/views/prs.js` `mount`: when `state.prs?.batch` is not the shown batch at mount, or
  when the shown batch changes, it stops the feed and sets `prs: null` (the page shows "loading"
  rather than another batch's rows under the shown batch's name), then starts a new feed, which
  reads at once (prs-Q2). It subscribes to the store for the change.
- No batch running (a change from today): the page shows the last closed batch's PRs with the
  navigator (`shownId` gives it), read once on the forge. `pv.none` ("No batch running.") shows
  only when the project has no history at all; `pv.last` goes (its key is removed from both word
  files). The header names the batch (`pv.batch`) and, for a closed batch, a tag
  `pv.closed_batch` ("closed, read once" / "close, lue une fois") in place of the refresh words.

Server:

- `routes.py` `prs_of` reads `req.query.get("batch")` and passes it to `prs.answer(..., batch=...)`.
- `prs.answer`:
  - The id of the batch in `4-batch/`, or no `batch` while there is one: today's answer.
  - The id of a `history` record whose `state` is `closed` (matched on its `batch` field), or no
    `batch` while `4-batch/` holds none: the rows come from that record (the newest closed one
    when no id is given; below); `batch` in the answer is that id and `closed` is true.
  - No batch in `4-batch/` and no closed record: today's "no batch" shape (`batch: null`,
    `rows: []`), no forge call.
  - Any other id: the "no batch" shape with `error: "unknown batch <id>"`, status 200, no forge
    call.
  - The answer gains `closed` (false for the batch in `4-batch/`); `last_batch` is removed.
- A closed batch's rows: the record's CRs that have a `pr`, ordered by `order` when present, else
  as listed (as `history.js` `recordRows` does). Each is mapped to the CR shape `row_of` reads:
  `kind: None`, `branch: None`, `to_review: False`, `state: "merged"` when `result` is `merged`,
  else `result`. Then on each row: `ready_now: False`, `why: None`, `disagrees: None`,
  `merged_into.cr: None` (the record keeps no branch, so `landed_with` is `None`). `paused` is
  false. No line is written to `board-seen.jsonl`: `seen.signal` runs for the batch in `4-batch/`
  only.
- A closed batch whose links span two repositories, or one PR the forge no longer shows, answers
  today's error line with no rows (no new handling).
- The new code goes in a helper (`_closed_rows` or the Driver's name) so `answer` stays under 50
  lines; `prs.py` stays under 400 and imports no `Context` (its docstring's rule).
- The forge reads: `ForgeReads` is unchanged as a class; `answer` calls it with the key
  `"<project id>:<batch id>"` (the batch shown), so each batch shown keeps its own 10 s read and two
  pages on two batches never call the forge in turn on every poll. A change of batch shown reads at
  once (a key read for the first time, or more than 10 s ago). The docstrings of `ForgeReads` and
  of the module say one read per project and batch shown.
- The sidebar count of the PRs entry (`<web>/js/views/registry.js`) is unchanged (the running
  batch's open PRs).

### 2. Filter by state

- A row of chips above the rows: "all" (default, today's view), "open", "draft", "merged". One on
  at a time. "open" is the forge's `state: open` (not a draft); "draft" is `state: draft`; "merged"
  is `state: merged`. A closed (unmerged) PR shows only under "all".
- Applied in the browser on the answer's rows: it never changes what the server reads on the
  forge, nor how often.
- The header (`prs.js` `head`) still counts the whole batch (`pv.progress`). When the filter hides
  every row: one line, `pv.nomatch` ("No PR matches this filter." / "Aucune PR ne correspond à ce
  filtre."; MR forms in section 5).

### 3. Sort

- A second row of chips: "batch order" (default: today's order, merge order then batch order, or
  the record's order for a closed batch), "opened", "last activity", "CR number". One on at a time.
  Dates newest first; CR number by the digits of the CR id (`CR-308` -> 308), ascending. A row with
  no date (the forge gave none) goes last; ties keep the batch order.
- Two new forge fields, in the same single GraphQL call (no extra call):
  - `forge_read.py`: `GITHUB_FIELDS` and `GITLAB_FIELDS` gain `createdAt updatedAt` (the field
    names on GitHub's `PullRequest` and GitLab's `MergeRequest`); `github_state` and
    `gitlab_state` return `opened_at` and `updated_at`.
  - `prs.py` `row_of` copies `opened_at` and `updated_at` into the row. "Last activity" is the
    forge's `updatedAt`.
- A row shows the date it is sorted by, in its facts line (`prs-row.js` `when`): sorted by
  "opened", `pv.opened_ago` ("opened {age} ago" / "ouverte il y a {age}"); by "last activity",
  `pv.active_ago` ("active {age} ago" / "active il y a {age}"). Under the batch order or the CR
  number, the facts are today's (merge or close date). `prRow` takes the sort as a parameter.
- Applied in the browser, like the filter.

### 4. The choice in the URL

- `router.js` stays the only module that writes the address. On `v=prs` the address carries,
  besides `p`, `v` and `b`: `st=<open|draft|merged>` (absent: all) and
  `sort=<opened|activity|cr>` (absent: batch order). `resolve` reads them on `v=prs` only; an
  unknown value reads as absent; `href` writes them on `v=prs` only; `go` takes them in its
  `place` (`undefined` keeps the current ones on the PRs page). Another view drops them; back and
  forward bring them back with the address. A copied address reopens the page on the same batch,
  filter and sort.
- A change of filter or sort replaces the address (`go(..., { replace: true })`), so back leaves
  the page rather than stepping through each chip; a change of batch goes through the navigator
  as today (a new history entry).
- `store.js` gains `prsState` and `prsSort` (or the Driver's names) next to `batchId`, `null` for
  the defaults; `router.js` `apply` sets them from the place and its `reset` clears them with the
  project.
- The chips' module is new (for instance `<web>/js/views/prs-filter.js`), so `prs.js` stays
  small; its clicks call `go`, never `history` directly.

### 5. "MR" on a GitLab project, `!n` for its number

How the board knows the forge (server):

- New small module `<board>/forge_kind.py` (or a function in `state.py` if it stays under 400
  lines): `forge_of(state, origin) -> "gitlab" | "github" | None`:
  1. `gitlab` when a PR link of the record (the batch's CRs, or any `history` record's CRs) matches
     `GITLAB_LINK`, imported from `commands/forge_stack_gitlab.py`, never copied; `github` when
     links are there and none matches.
  2. With no link at all: `gitlab` when the `origin` URL's host holds `gitlab` (`origin_of`, no
     network; `git@gitlab.example.com:...` and `https://gitlab.com/...` both count); `github` when
     it holds `github`; else `None`.
  The link's shape wins over the host (a self-hosted GitLab whose host says nothing is known from
  its first MR).
- `state.py` `project_state` gains `"forge": forge_of(...)`; `project_line` gains `"forge"` from
  it (for the overview).

The words (browser), with the key scheme of CR-341's `mr.open`:

- The MR form of a word lives in the `mr.` key space: the MR form of `pr.<x>` is `mr.<x>`
  (`pr.open` -> `mr.open`, `pr.draft` -> `mr.draft`), the MR form of any other key `<k>` is
  `mr.<k>` (`nav.prs` -> `mr.nav.prs`, `pv.nopr` -> `mr.pv.nopr`, `stats.reviews.one` ->
  `mr.stats.reviews.one`). Only the keys whose text names a PR get an MR form.
- `<web>/js/model/words.js`: `t(key, params)` (and so `tn`) looks up the MR form first when the
  shown project's `forge` (`snapshot().data?.forge`) is `gitlab`, else (or when the MR form is
  missing) the key itself. A new `tf(forge, key, params)` does the same for an explicit forge (the
  overview, where each line is a project).
- The MR forms go in new word files `<web>/js/i18n/en-mr.js` and `fr-mr.js`, merged into `en.js`
  and `fr.js` as `en-prs.js` is (so neither passes 300 lines). `mr.open` moves from
  `en.js`/`fr.js` into `en-mr.js`/`fr-mr.js`, so each language defines it once. Both languages
  hold the same keys (`tests/test_code_targets.py`
  `test_the_web_frame_has_small_scripts_and_both_word_files_share_their_keys`). French keeps its
  grammar and the invariable plural: "la MR", "les MR", "une MR en brouillon".
- The keys that get an MR form (every word naming a PR at `f36277c6`; the Driver adds any later
  one and every new word of this CR that names a PR):
  - PRs page: `nav.prs` (title, sidebar, bottom bar), `pv.nopr`, `pv.nomatch`, `pr.open` (the
    row's title: `mr.open`, CR-341's key, reused), the filter and sort labels that name a PR.
  - Home: `home.open_prs`, `home.review_go`, `home.draft`.
  - Batch page and Kanban: `prs.nothing`, `prs.review`, `prs.drafts`, `prs.click`,
    `prs.hint_stack_ok`, `prs.hint_stack_no`, `state.draft`, `pr.draft`, `gate.open`,
    `kanban.handed_sub`, `mode.stack.text`, `mode.series.text`, `mode.parallel.text`,
    `stats.reviews`, `stats.reviews.one`.
  - Events: `ev.ship` ("MR {pr} pushed").
  - Costs receipt: `costs.receipt_thanks`, `costs.receipt_thanks.one`.
  - Overview: `overview.review`, `overview.card_review`, `overview.note`. A project's card uses
    `tf(line.forge, ...)`; the overview's shared headings say "MR" only when every project listed
    is GitLab, else "PR".
  - The state tags (`pv.state.*`) name no PR and stay.
- The number: `prNumber` writes `!n` for an MR (`isMergeRequest`, CR-341). This CR reuses CR-341's
  `isMergeRequest`, `prNumber` and `mr.open`, never a second GitLab test in the web code.

### 6. The look (board-design-system's rules)

- The state filter and the sort are the one chip: the toggle chip of board-design-system §6
  (filled on, the `off` variant outlined grey), filled with `--accent`; until board-design-system
  lands, `.lab lbtn` without the colour square. No new chip style in `prs.css`.
- No side accent border anywhere on the page: the rows keep today's hairline separators; nothing
  of this CR adds a `border-left`/`border-right` accent, nor marks the shown filter or sort with
  one.
- The one card: this CR adds no card builder and no card style. The PRs page's rows stay list
  rows; if board-design-system has landed and turned them into cards, they come from its
  `ui/card.js` and this CR's changes go through it.
- If board-design-system lands first, its `DESIGN.md` is read first and its test passes; if this
  CR lands first, board-design-system's Driver moves the chips under its sheets. Whichever lands
  second rebases.
- Tokens only (`var(--...)`), no new colour outside `tokens.css`.

### 7. AGENTS.md (repository root), the PRs-page rule (prs-Q2)

In the bullet "The CLI's scope", the sentence on the board's PRs page changes, word for word:

From:

> one named exception, its PRs page: when that page asks, at most once every 10 s per project,
> while a PR of the batch is not done, plus one read when the page opens, it reads the forge,

To:

> one named exception, its PRs page: when that page asks, at most once every 10 s per project
> and batch shown, while a PR of the batch shown is not done, plus one read when the page opens
> and one at once on each change of the batch shown, it reads the forge,

and, in the same sentence, "when its forge read finds a PR merged that the record does not hold"
becomes "when its forge read finds a PR of the batch in `4-batch/` merged that the record does
not hold". The rest of the line is unchanged. The line is re-wrapped at 100 columns as its
neighbours are. This change is on the user's word (prs-Q2 C).

### 8. Docs

- `docs/web-board.md`, the section on the PRs page: one short paragraph: the batch navigator
  (a past batch's PRs, read once on the forge when shown; with no batch running, the last closed
  batch), the state filter, the sort and the date a row shows, the `st=` and `sort=` address
  keys, and "MR" / `!n` on a GitLab project (told from its MR links, or from the `origin` host
  while no MR exists). Its line on the forge read says "the batch shown".

## Limits the Driver keeps

- `tests/test_code_targets.py`: a `.js` at most 300 lines, a `.css` at most 300 lines with nesting
  at most 3 and no colour outside `tokens.css`, a `.py` at most 400 lines and a function at most 50,
  no import cycle, no `innerHTML` outside `dom.js`, no `style=`/`on...=` in markup, no
  `http://`/`https://` text anywhere in `<web>` (comments and regex literals included).
- `prs.py` imports no `Context`.
- The page writes nothing in git, the record or the forge; `board-seen.jsonl` only for the batch
  in `4-batch/`.
- One CR, on the Chief of Staff's settlement (the user asked for "MR" on GitLab in the same
  request as the PRs page). The risk it carries: the MR wording touches words on every page (Home,
  Batch, Kanban, Costs receipt, overview, events), far beyond the PRs page, so the diff is wide,
  a missed key shows "PR" on a GitLab project, and rebases against the other board CRs that edit
  `en.js`/`fr.js` are more likely. The MR forms stay in `en-mr.js`/`fr-mr.js` to narrow those
  conflicts, and each listed key is checked on the prepared GitLab record.

## Out of scope

- Several batches at once ("all batches").
- "closed" as a filter value.
- A change of `ForgeReads`' class or of the 10 s period (only its key changes).
- A forge read anywhere else than the PRs page.
- Any write: the board edits no batch and messages no agent.

## Evidence

- `just check` green (lint, `just test` within its budget, release notes); `just eval-dry-run` in
  the worktree before the first push (a change under the CLI's `src/`).
- `just scenario (ubuntu-latest)` green at the PR's head (a change to the CLI).
- New `tests/test_board_prs_batches.py` (`test_board_prs.py` is at 384 of 400 lines), a few
  parametrized cases on the existing fixture:
  - `?batch=<closed id>` answers that record's CRs with a PR in the record's `order`, `closed`
    true, `ready_now` false, `why` and `disagrees` null, and writes nothing in
    `board-seen.jsonl` even when the forge says merged for a CR whose `result` is not `merged`;
  - no `?batch=` and `?batch=<running id>` give today's answer; no `?batch=` with no batch in
    `4-batch/` answers the newest closed record; with no history either, the "no batch" shape and
    no forge call; an unknown id answers `unknown batch <id>` with no forge call;
  - two batches read in turn each call the forge once within 10 s (the key per batch shown);
  - a row carries `opened_at` and `updated_at`.
- `tests/test_board_forge_read.py`: both queries name `createdAt updatedAt`; `github_state` and
  `gitlab_state` return them.
- The `forge` cases, parametrized, in `tests/test_board.py`, or in a new file next to it if they
  pass 40 lines: `gitlab` with a `/-/merge_requests/` link in the record, `github` with a GitHub
  link, `gitlab` with no link and a `gitlab` origin host, `github` with a GitHub link and a
  `gitlab` origin host (the link wins), `None` with neither.
- `test_code_targets.py` passes (same keys in both word files, sizes, style rules); Biome
  (`just lint`) passes on `<web>`; board-design-system's test too if it has landed.
- By hand, on a served board, recorded in the PR's Deliverables: the PRs page on the running batch
  and on a closed one (navigator; one forge read at the change, none later), each state filter,
  each sort with its date on the rows, a reload of a copied address keeping all three; with no
  batch running, the last closed batch shown with the navigator; the PRs page's GitLab rows on a
  real GitLab project, or, with none, the PRs page's GitLab rows and the GitLab
  `createdAt updatedAt` named in the PR's Known gaps as not exercised; MR wording on the other
  pages from the prepared record (a record with GitLab links: "MR" and `!n` on Home, the Batch
  page, the overview and the events, in English and French). This CR changes no CR board pane
  (`hooks/register.tsx`, `STATUS.json`): no pane screenshot is owed.

## Open questions

None: every point is settled by `02-answers.md` or a working choice above (the per-batch forge-read
key, a closed batch read once whether chosen or shown by default, the closed record's mapping, the
`mr.` key space for keys with no `pr.` prefix, the overview's shared headings, the `origin` host
words `gitlab`/`github`).

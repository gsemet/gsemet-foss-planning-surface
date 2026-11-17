# Change Specification: a live, read-only view of the batch's PRs on the web board

## Goal

The user's words (2026-11-15, batch-18, 11 PRs ready at once and merged in several passes): "a
'monitor PR' that refreshes by itself so that I know which PR is merged." Today the user learns
the state of a PR from the Chief of Staff's lines, which go stale as soon as they merge one (a PR
becomes conflicting, another is still a draft, a merge did not go through). This CR adds a page to
the web board (`chantier board`) that shows each PR of the batch with its CR, its state on the
forge and whether it is ready to merge now. The page refreshes by itself about every 10 s, stops
asking the forge once every PR is done (merged, or closed without a merge), and starts again by
itself when a new PR joins the batch. It only reads: it writes nothing anywhere.

This CR is the first of two (Q11). The merge signal (the board leaving a line that `status`
prints for the Chief of Staff when it sees an unrecorded merge) is the CR `pr-merge-signal`, after
this one; nothing of it is built here.

## Decisions carried from 02-answers.md

| Answer | Decision | Where it lands |
| --- | --- | --- |
| Q1 | A page of the web board, not the terminal or the CR board pane. It shows each PR of the batch: its CR, its state on the forge (open, draft, merged, conflicting, checks running or green) and whether it is ready to merge now. It refreshes by itself about every 10 s, with one forge request for all of the batch's PRs per refresh (about 360 an hour, far under GitHub's 5,000 an hour). | 1, 2 |
| Q2 | A named exception: this view reads the forge, read-only, with `gh` or `glab`, and needs the network. The rest of the CLI does not change. AGENTS.md says so. The CLI already calls `gh`/`glab` when an agent runs `forge-stack` or `ship` (its draft read); the exception is worded as the board's own: it reads the forge when its page asks, with no agent asking. | 2, 4 |
| Q3 | Once every PR is done, the view shows its final table and stops refreshing by itself (Q7 widens "all merged" to "all done"). | 3 |
| Q4, Q5 | The merge signal and who acts on it: carried by `pr-merge-signal` (Q11), not here. | Out of scope |
| Q6 | "Ready to merge now" needs both the record (the CR ready to merge) and the forge (open, not a draft, not conflicting, checks green): the Chief of Staff's own rule for "you can merge it". | 1, 2 |
| Q7 | A PR closed without a merge counts as done. The final table says "all done", with each PR's end (merged or closed). | 3 |
| Q8 | After the final table the page keeps reading the local record, with no forge read. A new PR in the batch starts the forge refresh again by itself. | 3 |
| Picture | The Chief of Staff's decision: no picture of the page in `docs/web-board.md` for now (the demo has no forge; a fake forge read is not worth it). | 4 |
| Q9 | While the forge has not computed a PR's mergeability (GitHub's `UNKNOWN` after a push or a neighbour's merge), or its checks have not started, the row says "being checked by the forge" and the PR is not ready. "No checks" counts as ready only when the forge says the repository has none. | 1, 2 |
| Q10 | When the forge shows a PR merged that the record does not hold, the row says "merged on the forge, not recorded yet: tell the Chief of Staff" (the batch-18 case: nothing runs, no heartbeat reads anything). This row text is the page's and lands here; the docs say it. The signal that Q10 sits beside (Q5 stays) is `pr-merge-signal`'s. | 1, 4 |
| Q11 | Two CRs. This one is the read-only PRs page: route, view, the forge-read exception in AGENTS.md, docs. `pr-merge-signal` (`board-seen.jsonl`, the `status` line, the two cards, the second AGENTS.md exception, Q4, Q5, Q10's signal side) comes after it. | Whole spec |
| Q12 | The page shows the batch the Batch view shows, running or paused. After the batch's close it says "no batch running" and names the last batch. | 1 |

No other decision is made here.

## What changes

### 1. The page (board front end, `skills/chantier/scripts/cli/src/chantier/board/web/`)

- A new view, **PRs** (id `prs`; words `nav.prs` in `js/i18n/en.js` and `fr.js`), registered in
  `js/views/registry.js` after `batch`. It has its own module `js/views/prs.js` (and a CSS file
  `css/views/prs.css` if it needs one). It has no `overview` entry: on "All projects" it opens on
  the last real project, as `registry.js` already does for the views that have none.
- **The sidebar count comes from the record only**, because a view's `count(state)` sees only the
  board's 5 s read of the record (`state.data`), never the forge read: it is the number of the
  batch's CRs that have a PR recorded and that the record does not show merged
  (`crsOf(state.data?.batch).filter((c) => c.pr && c.state !== 'merged').length`), or nothing when
  there is no batch. It never claims a PR is ready or merged on the forge.
- **Which batch (Q12):** the batch the Batch view draws, `state.data.batch` (the batch of
  `4-batch/`, read by `board/state.py`'s `project_state` through `repo.batch_folders()`), whether it
  is running or paused; a paused batch is named "paused" in the header, and the page reads the
  forge as for a running one (the user may still merge). When there is no batch (after its close,
  or before the first), the page says "no batch running", names the last batch from the record's
  history (`state.data.history[0].id`, the newest `batch-*.json` record), when there is one, and
  asks the forge nothing.
- One row per CR of the batch that has a PR recorded (`crs[].pr`). A CR with no PR yet has no
  row. Rows follow the batch's merge order (`batch.merge_order` first, then the other CRs in the
  batch's order). Each row shows:
  - the PR's number (a link to the PR when `safeUrl` accepts it, as `batch-pr-card.js` does) and
    the CR's id and title, with the kind tag of a fix or a release CR;
  - its **forge state**, one of `open`, `draft`, `merged`, `closed` (closed without a merge), with
    `conflicting` added when the forge says the PR cannot merge because of a conflict, and the
    checks as `running`, `green`, `failing` or `none` (`none` only as Q9 says, below);
  - **being checked by the forge (Q9):** while the forge has not computed the PR's mergeability
    (GitHub's `mergeable: UNKNOWN`, GitLab's checking or unchecked merge status), or while the
    PR's checks have not started and the forge does not say the repository has none, the row says
    "being checked by the forge" in place of the conflict and checks words. Such a PR is not
    ready;
  - **for a merged PR, the branch it was merged into** (the forge's base or target branch at the
    merge), named as the CR whose branch it is when it is one (the same mapping as
    `board/crs.py`'s `_on`), else as the branch: "merged into main", or "merged into
    `<cr>`'s branch" for a stacked PR merged into the PR under it. The page states it and judges
    nothing more from it: a merged PR is done (Q3, Q7), whatever its branch;
  - **ready to merge now (Q6):** yes or no. Yes only when the record says the CR is ready to merge
    (`crs[].to_review`, true when `ready_word` gives `ready-to-merge`) and the forge says the PR is
    open, not a draft, not conflicting, not being checked (Q9), and its checks are green or the
    forge says the repository has none. The forge alone never makes a PR ready: the Chief of
    Staff's card says "you can merge" only after the `ready-to-merge` line, never because of a
    green CI or how the PR looks on the forge, and the page follows the same rule;
  - **when the record and the forge disagree,** a few words saying so, for example "ready in the
    record, conflicting on the forge", "ready in the record, draft on the forge", and, for a PR the
    forge shows merged and the record does not, exactly **"merged on the forge, not recorded yet:
    tell the Chief of Staff"** (Q10);
  - the time of the forge read the row shows ("read 4 s ago", with `core/format.js`'s `age`).
- A header line gives the batch's id, mode and, when paused, "paused"; the count of PRs done out
  of the total with their ends ("7 of 11 done: 6 merged, 1 closed"); and the refresh state:
  "refreshing every 10 s", "all done, refresh stopped", or the forge error (below).
- **The forge is unreadable** (`gh`/`glab` missing or not logged in, no network, the forge
  refuses): the page shows the forge's own message on one line and keeps the last good read with
  its time. It never guesses a state and never shows the record's state as if it came from the
  forge (the project's "no fallback" rule). The next refresh tries again.
- The page writes nothing. It has no merge button and no other action on a PR. A click on a row
  opens the PR on the forge, and the folder icon opens the CR's folder, as on the Batch view.
- **The refresh:** the page asks the server for the forge read once when the view opens, then
  about every 10 s, only while it is the view shown, the browser tab is visible (the same
  `visibilityState` rule as `js/core/refresh.js`) and a PR of the batch is not done (section 3).
  The board's existing 5 s read of the record keeps running and does not change.

### 2. Reading the forge (board server, `skills/chantier/scripts/cli/src/chantier/board/`)

- A new read route, `GET /api/projects/<id>/prs`, in a new module `board/prs.py` whose `ROUTES`
  `routes.py` appends, as it does with `write_api.ROUTES` (or in `routes.py` itself if that stays
  short). It sits behind the board's key and the same order of judgement (`_judged`) as every
  other route. It answers `{"batch", "paused", "last_batch", "rows": [...], "read_at", "error",
  "all_done", "now"}`, with one row per CR that has a PR: `cr`, `pr`, `number`, `state`
  (`open`/`draft`/`merged`/`closed`), `conflicting`, `checking` (Q9), `checks`
  (`running`/`green`/`failing`/`none`), `merged_into` (the branch, and the CR whose branch it is,
  or null), `ready_now`, `disagrees` (the few words of section 1, or null), `merged_at` and
  `closed_at` from the forge.
- It reads the record the way `board/state.py` already does (`read_batch_json` on
  `repo.batch_folders()`, `crs.cr_rows`) to know the CRs, their links and `to_review`; it adds
  nothing to `STATUS.json` and nothing to `project_state`. With no batch it answers the last
  batch's id and no rows, and calls no forge.
- **One forge request per refresh for all of the batch's PRs:** a single GraphQL query through
  `gh api graphql` (GitHub) or `glab api graphql` (GitLab) that reads every PR of the batch at once:
  state, draft, mergeability or conflict state, the checks' rollup, the base or target branch,
  merged and closed times, and what the forge gives to tell "this repository has no checks" from
  "the checks have not started" (Q9). The forge is chosen from the shape of the links
  (`pr_parts` and `GITLAB_LINK`, imported from `commands/forge_stack_gh.py` and
  `forge_stack_gitlab.py`, never copied, as `forge_base.py` does). The runners' errors (not on PATH,
  a failed call, output that is not JSON) become the page's one-line error. When the batch's PRs
  are not all in one repository, the route answers as its error the same refusal text as
  `forge-stack` ("the batch's PRs are not all in one repository"), and reads nothing.
- **Q9 on each forge:** "being checked" is GitHub's `mergeable: UNKNOWN`, or a head commit with no
  check run and no status yet in a repository that has checks; GitLab's checking or unchecked
  detailed merge status, or no pipeline yet in a project that has CI. `checks: "none"` only when
  the forge's own answer says the repository has no checks (for example, on GitHub, no workflow
  folder on the default branch and no status context on the head; on GitLab, no CI configuration).
  The exact fields are the Driver's to choose and to prove (section "Evidence"); when the read
  cannot tell, the row is "being checked", never "none".
- **At most one forge request per project every 10 s**, whatever the number of pages open: the
  server keeps the last read per project, with its time, and a call less than 10 s after the last
  read gets that read again without asking the forge. With no page asking, the forge is never
  asked.
- **Read-only:** the route runs only read calls (GraphQL queries; no mutation, no `-X POST`,
  `PATCH`, `PUT` or `DELETE`). It changes nothing in the record, the planning folder, git or the
  forge.
- This is the board's own forge read, when its page asks, with no agent asking (Q2).
  `forge-stack` and `ship`'s draft read in `forge_base.py` are not touched.

### 3. The end of the refresh (Q3, Q7, Q8)

- `all_done` is true when every row's forge state is `merged` or `closed` (a PR closed without a
  merge counts as done, Q7). The page then shows its final table with "all done" in the header and
  each row's end ("merged into main at <time>", "merged into `<cr>`'s branch at <time>" or "closed
  at <time>, not merged"), and stops asking for forge reads by itself.
- **After the final table** (Q8): the page stays on screen and keeps the board's ordinary 5 s read
  of the record, with no forge read. When that read shows a PR in the batch that the final table
  does not hold (a CR of the batch that gets a PR later, for example a fix CR added after), the page
  starts the forge refresh again by itself, with no click; it stops again once every row is done.
  Opening the view again, or reloading the page, reads the forge once (the one read when the page
  opens), after which it stops again if every row is still done.

### 4. AGENTS.md, CONTRIBUTING.md and the docs

- `AGENTS.md`, the board's bullet ("One named exception: `chantier board` …"). Keep what it says
  and add, after "it never edits a batch and never messages an agent;", wording that matches the
  read rule of sections 1 to 3:

  > one named exception, its PRs page: when that page asks, at most once every 10 s per project,
  > while a PR of the batch is not done, plus one read when the page opens, it reads the forge,
  > read-only, with the user's own `gh` or `glab`, on its own (no agent asks it), and needs the
  > network for that;

  The bullet that says "the CLI needs no network once uv's cache holds its packages" gets ",
  except the board's PRs page (below)". The rest of the CLI does not change. (`pr-merge-signal`
  adds its own exception to the same bullet later.)
- `CONTRIBUTING.md`, the same board paragraph (lines 93-98, "never edits a batch and never
  messages an agent"): the same exception, in the same words.
- `docs/web-board.md`: a section "### PRs" under "## The views", after "### Batch": what a row
  shows; "ready to merge now" as both the record and the forge; "being checked by the forge"; the
  branch a merged PR went into; "merged on the forge, not recorded yet: tell the Chief of Staff"
  and what to do about it (tell the Chief of Staff, who records it with `order merged`); the 10 s
  refresh while visible; the stop on "all done" with closed PRs counted as done; the restart when a
  new PR joins the batch; the forge error line; a paused batch; "no batch running" after the
  close. The intro line ("It never touches a batch.") stays and gains "It reads your forge with
  your own `gh` or `glab`, read-only, for its PRs page." "## Starting the board": the board needs
  the user's `gh` or `glab` login, and the network, for the PRs page only.
- Pictures: none for the PRs page (the Chief of Staff's decision). `just docs-screenshots` and
  `docs/demo/` do not change.
- The cards: `chief-of-staff.md`, where the board is offered to the user (the remote "board on my
  phone" line and the Tips), names the PRs page: the live view of the batch's PRs. No other card
  changes; no role's body changes (`agents/` and `com.github.copilot/agents/` untouched).

## Out of scope

- The merge signal: `board-seen.jsonl`, the `board saw merged` line in `status`, the Chief of
  Staff's and the Foreman's card bullets about it, the second AGENTS.md exception (Q4, Q5, Q10's
  signal side). All in `pr-merge-signal`, after this CR (Q11).
- The terminal and the CR board pane (`hooks/register.tsx`, `STATUS.json`): unchanged (Q1).
  `just mod` is therefore not required.
- Any write to the forge (merge, ready, rebase, retarget, comment): the page only reads (Q2).
- Recording a merge: only the Chief of Staff does it, with `order merged`.
- PRs of earlier batches, CRs with no PR, and pages on "All projects".
- Any change to the CLI's other commands and their forge use (`forge-stack`, `ship`'s read of the
  draft state in `forge_base.py`).
- A notification outside the page (sound, system notification).
- A picture of the PRs page in `docs/web-board.md`, and a fake forge read in
  `just docs-screenshots`.

## Evidence

- **Tests** (`skills/chantier/scripts/cli/tests/test_board.py`, in-process, parametrized, no
  network; `gh` and `glab` stubbed on PATH as the scenario's fakes do, or their runners
  monkeypatched):
  - `GET /api/projects/<id>/prs` without the key: 401. With the key and no batch: no forge call,
    no rows, the last batch's id from the history.
  - A paused batch: the rows are read as for a running one, `paused` true (Q12).
  - A batch of four CRs with PRs (one ready in the record and green on the forge; one ready in the
    record and conflicting; one ready in the record with `mergeable: UNKNOWN`; one merged on the
    forge into another CR's branch and not in the record): one forge call; the rows' `state`,
    `conflicting`, `checking`, `checks`, `merged_into`, `ready_now` (true for the first only) and
    `disagrees` (the fourth: "merged on the forge, not recorded yet: tell the Chief of Staff").
  - Q9, parametrized: checks not started in a repository that has checks gives `checking` and not
    ready; a repository the forge says has no checks gives `checks: "none"` and ready when the rest
    holds.
  - A CR not ready in the record whose PR is open, green and mergeable on the forge: `ready_now`
    is false (Q6).
  - Two calls within 10 s: one forge call.
  - Forge failure (`gh` missing; a call that fails): `error` holds the forge's text, no row
    invented, and the last good read is kept with its time.
  - `all_done`, parametrized: every PR merged, true; some merged and one closed without a merge,
    true (Q7); one still open, false.
  - The route's forge argv holds no mutation and no `-X` other than `GET`; the planning folder is
    byte-identical before and after a read (read-only).
  - The sidebar count, if the project tests the front end's models; otherwise the front-end check
    below covers it.
  - `just test` stays within its budget (AGENTS.md: at most 30 s above 18.5 s).
- **Scenario** (`scenario/run_scenario.py`, unit `surface-board`, GitHub forge): extend
  `scenario/fake_gh.py` to answer the batch's GraphQL query from its own PR store. Steps: open the
  board, `GET …/prs` and check the rows against the fake forge; merge one PR in the fake forge
  without `order merged`; `GET …/prs` again and check its row says "merged on the forge, not
  recorded yet: tell the Chief of Staff" and nothing was written in the planning folder; `order
  merged <cr>`; the row no longer says it; close one PR without a merge and merge the rest;
  `all_done` is true; add a CR with a PR to the batch (`order add`, then its PR recorded); `GET
  …/prs` shows the new row and `all_done` false (Q8). The `parallel` unit's check "only the agents
  called the forge" (`run_scenario.py`, around line 1231; `scenario/README.md` line 287) stays as
  it is, since no board runs there. Name the new steps in `scenario/README.md` under
  `surface-board`.
- **Unproved reads, with their trials.** Three reads cannot be proved by the fakes; each gets one
  trial, by hand, on a real forge, before the PR is ready, and its result in the PR's
  Deliverables; a trial not run is a Known gap the PR names (so the ready line quotes it):
  - **The merged-into branch**: a stacked PR merged into the PR under it reads as merged with that
    branch, not as merged into the default branch. Trial: on a real GitHub repository, merge a PR
    whose base is another PR's branch and check the row's `merged_into`.
  - **A native GitHub stack** (a batch in `stack` mode stacked by `forge-stack create`, the
    `repos/…/stacks` endpoint): the GraphQL fields (`mergeable`, the checks' rollup, the base) read
    the same for a PR inside a native stack. Trial: one read of a real native stack's PRs.
  - **GitLab** (`glab api graphql` for a batch's MRs: state, draft, detailed merge status, head
    pipeline, target branch): `scenario/fake_glab.py` answers it if that costs little, which
    proves the shape, not the real fields. Trial: one read on a real GitLab project.
- **The front end:** the page drawn from a real board on a project with a running batch, checked
  by hand once on a real GitHub repository: the rows, "being checked by the forge" right after a
  push, the refresh stopping on "all done" and starting again by itself when a new PR joins the
  batch, and the sidebar count matching the record (a screenshot in the PR's Deliverables, not
  required by the project's rules, which ask for one only for the CR board pane).
- `just check` passes on Linux, macOS and Windows. The PR passes `just scenario (ubuntu-latest)`
  (a CLI, cards and scenario change), and the local Windows run as AGENTS.md says for the CR on top
  of the stack.

## Open questions (for the user)

None. The first run's questions are answered in `02-answers.md` (Q5 to Q8 and the picture), the
critic's in Q9 to Q12.

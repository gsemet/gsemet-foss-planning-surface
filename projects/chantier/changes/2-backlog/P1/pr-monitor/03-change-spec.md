# Change Specification: a live view of the batch's PRs on the web board

## Goal

The user's words (2026-11-15, batch-18, 11 PRs ready at once and merged in several passes): "a
'monitor PR' that refreshes by itself so that I know which PR is merged." Today the user learns
the state of a PR from the Chief of Staff's lines, which go stale as soon as they merge one (a PR
becomes conflicting, another is still a draft, a merge did not go through). This CR adds a page to
the web board (`chantier board`) that shows each PR of the running batch with its CR, its state
on the forge and whether it is ready to merge now. The page refreshes by itself about every 10 s,
stops asking the forge once every PR is done (merged, or closed without a merge), starts again by
itself when a new PR joins the batch, and leaves a line for the Chief of Staff when it sees a
merge that the record does not hold yet.

## Decisions carried from 02-answers.md

| Answer | Decision | Where it lands |
| --- | --- | --- |
| Q1 | A page of the web board, not the terminal or the CR board pane. It shows each PR of the running batch: its CR, its state on the forge (open, draft, merged, conflicting, checks running or green) and whether it is ready to merge now. It refreshes by itself about every 10 s, with one forge request for all of the batch's PRs per refresh (about 360 an hour, far under GitHub's 5,000 an hour). | "The page", "Reading the forge" |
| Q2 | A named exception: this view reads the forge, read-only, with `gh` or `glab`, and needs the network. The rest of the CLI does not change. AGENTS.md says so. The CLI already calls `gh`/`glab` when an agent runs `forge-stack` or `ship` (its draft read); the exception is worded as the board's own: it reads the forge on a timer, with no agent asking. | "Reading the forge", "AGENTS.md" |
| Q3 | Once every PR is done, the view shows its final table and stops refreshing by itself (Q7 widens "all merged" to "all done"). | "The end of the refresh" |
| Q4 | A merge the view sees is signalled, not recorded. The view changes nothing in the batch. It leaves a line that the Chief of Staff reads at its next heartbeat, and the Chief of Staff still records the merge (`order merged`). This is a second named exception for the board, written in AGENTS.md together with the first. | "The merge signal", "AGENTS.md", "Cards" |
| Q5 | In Foreman mode too, the Chief of Staff sees the line and records the merge at its own next `status`. The Foreman does nothing more with it and sends no extra message. | "The merge signal", "Cards" |
| Q6 | "Ready to merge now" needs both the record (the CR ready to merge) and the forge (open, not a draft, not conflicting, checks green): the Chief of Staff's own rule for "you can merge it". | "The page", "Reading the forge" |
| Q7 | A PR closed without a merge counts as done. The final table says "all done", with each PR's end (merged or closed). | "The end of the refresh" |
| Q8 | After the final table the page keeps reading the local record, with no forge read. A new PR in the batch starts the forge refresh again by itself. | "The end of the refresh" |
| Picture | The Chief of Staff's decision: no picture of the page in `docs/web-board.md` for now (the demo has no forge; a fake forge read is not worth it). | "AGENTS.md, CONTRIBUTING.md and the docs" |

No other decision is made here.

## What changes

### 1. The page (board front end, `skills/chantier/scripts/cli/src/chantier/board/web/`)

- A new view, **PRs** (id `prs`; words `nav.prs` in `js/i18n/en.js` and `fr.js`), registered in
  `js/views/registry.js` after `batch`. It has its own module `js/views/prs.js` (and a CSS file
  `css/views/prs.css` if it needs one). On "All projects" it has no `overview` entry: it opens on
  a real project, like the views that have none. The sidebar count is the number of PRs that are
  ready to merge now, or nothing when no batch is running.
- One row per CR of the current batch (`state.data.batch`, the same batch the Batch view draws)
  that has a PR recorded (`crs[].pr`). A CR with no PR yet has no row. Rows follow the batch's
  merge order (`batch.merge_order` first, then the other CRs in the batch's order). Each row
  shows:
  - the PR's number (a link to the PR when `safeUrl` accepts it, as `batch-pr-card.js` does) and
    the CR's id and title, with the kind tag of a fix or a release CR;
  - its **forge state**, one of: `open`, `draft`, `merged`, `closed` (closed without a merge),
    with `conflicting` added when the forge says the PR cannot merge because of a conflict, and
    the checks as `running`, `green` or `failing` (or `none`, when the PR has no checks);
  - **ready to merge now** (Q6): yes or no. Yes only when both the record says the CR is ready to
    merge (`crs[].to_review`, the `ready-to-merge` word that `crs.py` derives from
    `stacks.ready_word`) and the forge says the PR is open, not a draft, not conflicting, and its
    checks are green or it has none. The forge alone never makes a PR ready: the Chief of Staff's
    card says "you can merge" only after the `ready-to-merge` line, never because of a green CI
    or how the PR looks on the forge, and the page follows the same rule. When the record and
    the forge disagree (the record says ready and the forge says conflicting, failing or draft;
    or the forge says merged and the record does not), the row says so in a few words, for
    example "ready in the record, conflicting on the forge" or "merged on the forge, not recorded
    yet";
  - the time of the forge read that the row shows ("read 4 s ago", using `core/format.js`'s
    `age`).
- A header line gives the batch's id and mode, the count of PRs done out of the total with the
  merged ones named ("7 of 11 done: 6 merged, 1 closed"), and the refresh state: "refreshing every
  10 s", "all done, refresh stopped", or the forge error (below).
- **The forge is unreadable** (`gh`/`glab` missing or not logged in, no network, the forge
  refuses): the page shows the forge's own message on one line and keeps the last good read, with
  its time. It never guesses a state and never shows the record's state as if it came from the
  forge (the project's "no fallback" rule). The next refresh tries again.
- **No batch running**: the page says so and asks the forge nothing.
- The page writes nothing. It has no merge button and no other action on a PR. A click on a row
  opens the PR on the forge, and the folder icon opens the CR's folder, as on the Batch view.
- The refresh: the page asks the server for the forge read about every 10 s, only while it is
  the view shown, the browser tab is visible (the same `visibilityState` rule as
  `js/core/refresh.js`) and the batch is not all done (section 3). The board's existing 5 s read
  of the record keeps running and does not change.

### 2. Reading the forge (board server, `skills/chantier/scripts/cli/src/chantier/board/`)

- A new read route, `GET /api/projects/<id>/prs`, in `routes.py` (or a new module `prs.py` whose
  routes `routes.py` appends, as it does with `write_api.ROUTES`). It sits behind the board's key
  and the same order of judgement (`_judged`) as every other route. It answers
  `{"batch", "rows": [...], "read_at", "error", "all_done", "now"}`, with one row per CR that
  has a PR: `cr`, `pr`, `number`, `state` (`open`/`draft`/`merged`/`closed`), `conflicting`,
  `checks` (`running`/`green`/`failing`/`none`), `ready_now`, `disagrees` (the few words above, or
  null), `merged_at` and `closed_at` from the forge.
- **One forge request per refresh for all of the batch's PRs:** a single GraphQL query through
  `gh api graphql` (GitHub) or `glab api graphql` (GitLab) that reads every PR of the batch at once
  (state, draft, mergeable or conflict state, the checks' rollup, merged and closed times). The
  forge is chosen from the shape of the links (`pr_parts` and `GITLAB_LINK`, reused from
  `commands/forge_stack_gh.py` and `forge_stack_gitlab.py`, never copied, as `forge_base.py`
  reuses them). The `gh`/`glab` runners' errors (not on PATH, a failed call, output that is not
  JSON) become the page's one-line error. When the batch's PRs are not all in one repository, the
  route answers the same refusal text as `forge-stack` ("the batch's PRs are not all in one
  repository") as its error, and reads nothing.
- **At most one forge request per project every 10 s**, whatever the number of pages open: the
  server keeps the last read per project, with its time, and a call that comes less than 10 s
  after the last read gets that read again without asking the forge. With no page on the view,
  the forge is never asked.
- **Read-only:** the route runs only read calls (GraphQL queries; no mutation, no `-X POST`,
  `PATCH` or `DELETE`). It changes nothing in the record, the planning folder or git, apart from
  the signal line of section 4.
- It reads the record the way `state.py` already does (`read_batch_json`, `crs.cr_rows`) to know
  the CRs, their links and `to_review`; it adds nothing to `STATUS.json` and nothing to
  `project_state`.
- This is the board's own forge read, on a timer, with no agent asking (Q2). `forge-stack` and
  `ship`'s draft read in `forge_base.py` are not touched.

### 3. The end of the refresh (Q3, Q7, Q8)

- `all_done` is true when every row's forge state is `merged` or `closed` (a PR closed without a
  merge counts as done, Q7). The page then shows its final table with "all done" in the header
  and each row's end ("merged at <time>" or "closed at <time>, not merged"), and stops asking for
  forge reads by itself.
- **After the final table** (Q8): the page stays on screen and keeps the board's ordinary 5 s read
  of the record, with no forge read. When that read shows a PR in the batch that the final table
  does not hold (a CR of the batch that gets a PR later, for example a fix CR added after), the
  page starts the forge refresh again by itself, with no click from the user; it stops again once
  every row is done. Opening the view again, or reloading the page, reads the forge once: one
  read, after which it stops again if every row is still done.

### 4. The merge signal (Q4, Q5)

- When a forge read finds a PR `merged` and the record does not show its CR as merged
  (`crs[].state != "merged"`), the server appends one line, once per CR and per batch, to a new
  local file at the planning folder's root, `board-seen.jsonl`:
  `{"t": <now>, "kind": "merged", "batch": <batch id>, "cr": <cr>, "pr": <link>, "merged_at": <the forge's time>}`.
  It is written under the lifecycle lock (`changes_lock`), as `board/journal.py`'s `_append`
  does, and it is UTF-8. The server writes it once: a later read that sees the same merge writes
  nothing more (it checks the file for that batch and CR first). A PR closed without a merge
  writes no line: only a merge is signalled.
- The file is local and never published: add `board-seen.jsonl` to `IGNORED` in
  `core/files.py` and to `SINGLE` in `board/fingerprint.py`, as `board-journal.jsonl` is. It is
  not part of the board's journal: it does not count in the "Written by the board" tile and the
  rescan does not clear it.
- The board never edits `batch.json`, `events.jsonl` or a STATUS file, never runs `order`, and
  never sends a message to a session. The line is only a file that the Chief of Staff reads.
- **Where the Chief of Staff reads it:** `chantier status`, in every form (the Chief of Staff's
  own `status` and `status --refresh`, and the Foreman's heartbeat `status --refresh --batch
  <batch> --epoch <n>`), prints one line for each entry of `board-seen.jsonl` for the batch whose
  CR the record does not yet show merged, next to the order lines (`commands/batch_status.py`, a
  helper beside `_order_lines` and `_autosync_lines`):
  `board saw merged: <cr> <pr link> at <merged_at>; for the Chief of Staff: order merged <cr>`.
  Once the merge is recorded the line no longer prints, so nothing has to clear the file. A
  `close` of the batch leaves the file alone; entries for another batch never print.
- **Who acts on it (Q5):** in direct mode and in Foreman mode alike, the Chief of Staff, at its
  own next `status` that shows the line. In Foreman mode the Foreman's heartbeat prints the line
  too; the Foreman does nothing with it: no `order merged`, no message to the Chief of Staff, and
  the line is not an undone order for ending its heartbeat.

### 5. Cards (`skills/chantier/references/`)

- `chief-of-staff.md`, in the bullet about a merge the user makes (around "When the user merges a
  PR before its `ready-to-merge` line, record it as any merge"): a `board saw merged: <cr> …` line
  in `status` is a merge the user made. Record it like any merge, at the `status` that shows it:
  `order merged <cr>`, then, in Foreman mode, send its line to the Foreman as for any order (the
  existing row "add, drop, reorder, change a CR; \"I merged #42\"" of the "While it runs" table).
  Add the `board saw merged` line to that row, next to "I merged #42".
- In the same card, where the board is offered to the user (the remote "board on my phone" line
  and the Tips), name the PRs page: the live view of the batch's PRs.
- `foreman.md`, beside the heartbeat bullet (around "Heartbeat: the wake that runs `chantier
  status --refresh --batch <batch> --epoch <n>`"): a `board saw merged` line in `status` is the
  Chief of Staff's; do nothing with it, send no message about it, and it does not count as an
  undone order (Q5).
- The two host files (`agents/` and `com.github.copilot/agents/`) do not change: no role changes
  its body.

### 6. AGENTS.md, CONTRIBUTING.md and the docs

- `AGENTS.md`, the board's bullet ("One named exception: `chantier board` …"). Keep what it says
  and add the two exceptions there, together. Proposed wording, to append after "it never edits a
  batch and never messages an agent;":

  > two named exceptions, both for its PRs page: on its own timer, with no agent asking, it reads
  > the forge, read-only, with `gh` or `glab` (one request for all the running batch's PRs, at
  > most every 10 s and only while the page shows it and a PR is not done), and needs the network
  > for that; and when it sees a PR merged that the record does not hold, it leaves one line in
  > `board-seen.jsonl` (planning folder, never published), which `status` prints for the Chief of
  > Staff to record at its next `status`: the board itself records nothing;

  The bullet that says "the CLI needs no network once uv's cache holds its packages" gets ", except
  the board's PRs page (below)". The rest of the CLI does not change.
- `CONTRIBUTING.md`, the same board paragraph (around lines 93-97, "never edits a batch and never
  messages an agent"): the same two exceptions, in the same words.
- `docs/web-board.md`: a section "### PRs" under "## The views" (what a row shows, "ready to merge
  now" as both the record and the forge, the 10 s refresh while visible, the stop on "all done"
  with closed PRs counted as done, the restart when a new PR joins the batch, the forge error
  line, the signal and who records it). Its intro line ("It never touches a batch") stays true,
  and gains "and it reads your forge with your own `gh` or `glab` for its PRs page". "## Starting
  the board": the board needs the user's `gh` or `glab` login for the PRs page only.
- Pictures: none for the PRs page (the Chief of Staff's decision). `just docs-screenshots` and
  `docs/demo/` do not change.

## Out of scope

- The terminal and the CR board pane (`hooks/register.tsx`, `STATUS.json`): unchanged (Q1).
  `just mod` is therefore not required.
- Any write to the forge (merge, ready, rebase, retarget, comment): the page only reads (Q2).
- Recording a merge: only the Chief of Staff does it, with `order merged` (Q4, Q5). The Foreman
  does not record it and does not relay it.
- PRs of earlier batches, CRs with no PR, and pages on "All projects".
- Any change to the CLI's other commands and their forge use (`forge-stack`, `ship`'s read of
  the draft state in `forge_base.py`): unchanged.
- A notification outside the page (sound, system notification).
- A picture of the PRs page in `docs/web-board.md`, and a fake forge read in
  `just docs-screenshots`.

## Evidence

- **Tests** (`skills/chantier/scripts/cli/tests/test_board.py`, in-process, parametrized, no
  network; `gh` and `glab` stubbed on PATH as the scenario's fakes do, or their runners
  monkeypatched):
  - `GET /api/projects/<id>/prs` without the key: 401. With the key and no running batch: no
    forge call, an empty answer.
  - With a batch of three CRs with PRs (one ready in the record and green on the forge, one
    ready in the record and conflicting, one merged on the forge and not in the record): one
    forge call, the rows' `state`, `conflicting`, `checks`, `ready_now` (true for the first only)
    and `disagrees`; exactly one `board-seen.jsonl` line for the third, and none more after a
    second read.
  - A CR not ready in the record whose PR is open, green and mergeable on the forge: `ready_now`
    is false (Q6).
  - Two calls within 10 s: one forge call.
  - Forge failure (`gh` missing; a call that fails): `error` holds the forge's text, no row
    invented, and the last good read is kept with its time.
  - `all_done`, parametrized: every PR merged, true; some merged and one closed without a merge,
    true, with no `board-seen.jsonl` line for the closed one (Q7); one still open, false.
  - `status` prints `board saw merged: <cr> … for the Chief of Staff: order merged <cr>` for an
    unrecorded merge, in the direct form and in the `--batch <batch> --epoch <n>` form, and stops
    printing it after `order merged <cr>`.
  - The route's forge argv holds no mutation and no `-X` other than `GET` (read-only).
  - `just test` stays within its budget (AGENTS.md: at most 30 s above 18.5 s).
- **Scenario** (`scenario/run_scenario.py`, unit `surface-board`, GitHub forge): extend
  `scenario/fake_gh.py` to answer the batch's GraphQL query from its own PR store. Steps: open the
  board, `GET …/prs` and check the rows against the fake forge; merge one PR in the fake forge
  without `order merged`; `GET …/prs` again and check `board-seen.jsonl` holds one line and
  `status` prints the `board saw merged` line; `order merged <cr>`; `status` no longer prints it;
  close one PR without a merge and merge the rest; `all_done` is true; add a CR with a PR to the
  batch (`order add`, then its PR recorded); `GET …/prs` shows the new row and `all_done` false
  (Q8). The `parallel` unit's check "only the agents called the forge" (`run_scenario.py`, around
  line 1231; `scenario/README.md` line 287) stays as it is, since no board runs there. Name the
  new steps in `scenario/README.md` under `surface-board`. If `fake_glab.py` can answer a GraphQL
  query at a small cost, the same read on GitLab; otherwise that path is a known gap in the PR.
- **The front end:** the page drawn from a real board on a project with a running batch,
  checked by hand once on a real GitHub repository: the refresh stops on "all done" and starts
  again by itself when a new PR joins the batch (a screenshot in the PR's Deliverables, not
  required by the project's rules, which ask for one only for the CR board pane).
- `just check` passes on Linux, macOS and Windows. The PR passes `just scenario
  (ubuntu-latest)` (a CLI, cards and scenario change), and the local Windows run as AGENTS.md says
  for the CR on top of the stack.

## Open questions (for the user)

None: the first run's five questions are answered in `02-answers.md` (Q5 to Q8 and the picture).

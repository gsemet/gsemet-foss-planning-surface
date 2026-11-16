# Feasibility of prototype 6 as a real board

Read-only review, 2026-11-13, against the main checkout at `b3fdfc3` (v0.9.0) and the planning
folder as it stood (batch-16, stack, Foreman, 7 CRs). Paths under `src/` are
`skills/chantier/scripts/cli/src/chantier/`; `proto` is `prototype/index.html`.

## Verdict

The **read side** of the prototype is feasible almost as drawn: about nine elements in ten are
already in `batch.json`, `events.jsonl`, the index's `STATUS.json` view or the CR folders, and
the rest is small derivation that fits `board.py` (a read-only view of the record). What blocks
it is delivery, not data: today's board forbids scripts and images by its own
Content-Security-Policy, serves files only as escaped HTML text, and exposes none of `after`,
`order`, `stacked`, `kind`, `created`. The **write side** has no carrier at all: the board
refuses every method but GET and HEAD, `AGENTS.md` says it writes no file and that "answering an
ask, filing an item" is another CR, no record of a queue from the user to the Chief of Staff
exists, and three things the Triage view lets the user do (groups, rank inside a priority, "the
next batch is ready") are recorded nowhere. **Several projects** needs a board started on the
surface, where today one board serves one planning folder, tied to one seat, on one port.
**Remote** needs the token, which does not exist. Five points of the prototype say something
chantier does not mean (two columns named "Ready", a stack merged bottom-up, the release CR "outside
the stack", `ready` read as "ready to merge" in every mode, a `3-ready` key that never matches).

Classes: **now** (available now), **derivable**, **new record**, **outside** (outside chantier),
**conflict** (conflicts with a rule).

## Sidebar, project picker, "Tous les projets"

| Element | Class | Source or gap | Note |
| --- | --- | --- | --- |
| List of the surface's projects | now | `state.surface_projects(root)` (`src/state.py:235`): folders of `projects/` with `checkout.yml` or `changes/` | The Claude Code pane already does it (`hooks/register.tsx:143-155`). |
| One board that reads several projects | derivable | `board.board()` calls `Repo.find(readonly=True)` (`src/board.py:415`), which raises `SurfaceChoice` on a surface with more than one project (`src/state.py:310`) | New: a surface mode in `board.py`, one `Repo._external()` per project, `collect()` per project. In scope (still a read-only view). See cross-cutting 1. |
| Per project: batch number, state, mode | now | `batch.json`: `id`, `status`, `mode`, `steering`; `status.batch_view()` | Only for a project steered on this machine: `batch.json` and STATUS are local, never pushed (`src/state.py:200`). |
| Per project: working, blocked counts | now | `batch_view()["crs"][].state` | |
| Per project: PRs to review, as links | now / outside | `crs[].pr` of CRs in `ready` | The link is recorded by `ship`; whether the PR is a draft, reviewed or already merged is the forge's. |
| Per project: progress merged / total | now | `batch_view()["crs"]` holds every CR of the batch, merged included | The index's `batches[].crs` holds the active ones only (`src/status.py:413`). |
| Per project: spent of budget | now | `spent_usd`, `budget_usd`, `unpriced` | As of the last `status --refresh`; `spent_usd` is `null` before the first one. |
| Per project: intake and grill counts | now | `dashboard_view()["backlog"][].priority` | |
| Per project: "data's age" | derivable | not the view's `updated` (it is `now()` at each request, `src/status.py:426`) | The honest ages are the cost's (last `cost` event) and the heartbeat's. The prototype's figure is the snapshot's age and has no live meaning. |
| Running-batch dot | now | `batch.json` `status == "running"` | |
| Project colours and initials | derivable | nothing recorded; computed from the name | |
| Picker choice kept per browser | now | browser storage; no record needed | |
| A project steered on another machine | outside | its `batch.json`, STATUS, `seat.json` are on that machine only | The line can show its inbox and backlog as last pulled, no batch, no cost. The board runs no `git pull`. |

## Home

| Element | Class | Source or gap | Note |
| --- | --- | --- | --- |
| Tile "À merger" (CRs handed back `ready`) | now | `crs[].state == "ready"` | Wrong word in a stack or a series: see cross-cutting 5. |
| Tile "T'attendent" (blocked + unread asks) | now | `crs[].blocked`, `asks_unread` | A CR blocked on `waits:` needs no one (`status._waits_on`, `src/status.py:72`): it should not count. The asks are the Foreman's to the Chief of Staff, as the pane already counts them (`docs/boards.md`). |
| Tile "Vers le CoS" (to send, pending) | new record | no queue exists | See cross-cutting 2. |
| Tile "Batch suivant" (declared ready) | new record | the count of `3-ready` is available; the user's "ready" is recorded nowhere | |
| Progress bar by state | now | `crs[].state` | Cancelled CRs are not drawn by the prototype. |
| Spent / budget, slots | now | `spent_usd`, `budget_usd`; index `batches[].slots` (`held()`, `src/status.py:420`) | `budget_usd` may be absent: the prototype divides by it. `unpriced` (a floor, "at least") is not shown. |
| "Dernier signe du Foreman / CoS" | now | `heartbeat`, `heartbeat_stopped`, `steering` | `heartbeat_stopped` must show as "stopped", not as an old age. The amber at 15 minutes is the page's judgment; the CLI states ages and never judges them. |
| "Ouvert il y a" | derivable | `batch.json` `created` (not in `batch_view`) | One field to add to the board's own data. |
| Open PRs | now / outside | `crs[].pr` where state is not merged | "Open" is assumed: a PR merged on the forge and not yet told to chantier still shows. |
| Blocked CRs with their reason | now | `crs[].blocked` | |
| Recent activity | now | `events.jsonl`; the board already serves the last 12 (`src/board.py:40,53`) | The prototype reads fields that do not exist: `handback` carries `result`, not `status`; a merge is an `order` event with `order_kind: "merged"`, there is no `merged` kind; an order's word is `order_kind`, not `note`; an `ask` event has no `cr`. `close` is never seen (the batch's files go at `close`). |
| Pipeline by grill state | derivable | `spec` is in `backlog[]` (`specifying`, `specified`, `null`); "in grill" is the presence of `02-answers.md`, not recorded | One `is_file()` per item in `status._backlog()` or in the board. |
| Last merged CRs | now | `dashboard_view()["merged"]` (50 at most), `merged_total` | |

## Triage

| Element | Class | Source or gap | Note |
| --- | --- | --- | --- |
| Columns Inbox, P1 to P4, `3-ready` | now | `backlog[].priority`: `inbox`, `P1`..`P4`, `3-ready` | The prototype tests `"ready"` (`proto:423,666,669`); the record says `"3-ready"`. `3-ready` was empty at the snapshot, so it did not show: with one item there it would fall in no column. |
| Raw / in grill / specified | derivable | `03-change-spec.md` and `02-answers.md` by presence | A fourth real state is missing: `specifying` (`work/specifying` marker, `status.spec_state`, `src/status.py:340`). |
| Automatable (in `3-ready`, no specification) | now | the folder and the missing file; same rule as `lifecycle.prepared_cr` (`src/lifecycle.py:62`) | Matches concepts.md, "`3-ready`". |
| Counts by state in a column header | derivable | same | |
| Move to P1..P4 or to `3-ready` | conflict today, command exists | `chantier triage <item> --priority P<n>` or `--ready` (`src/cli.py:45`, `src/lifecycle.py:193`) | The command exists; the board may not run it (read only, GET and HEAD, `src/board.py:304`), and 02-answers says the Chief of Staff applies it. |
| Move back to Inbox | new command | `triage` has no way back to `1-inbox`; `restore` works from `6-trash` only | Drop the Inbox target, or a small CLI change. |
| Abandon (in 02-answers, not in the prototype) | command exists | `chantier abandon <item>` | |
| Rank inside a priority ("up is more urgent") | new record | nothing; a lane's items come sorted by folder name (`src/status.py:354`) | The prototype does not keep a rank either: a drop inside a lane changes nothing. |
| Groups (named, moved whole, undone) | new record | no concept of a group in the record, the cards or concepts.md | Kept in the browser, a group is lost on the other device. Recorded, it is a new file in the planning folder that the CLI writes, and a new word for concepts.md. |
| Drag and drop | derivable | page code only | Not fired on most touch browsers; the selection bar is the phone's way. Not verified, as 02-answers says. |
| Drafts list ("N changements à envoyer") | new record | browser storage in the prototype | Two devices hold two lists. Either the drafts live on the server, or a change is sent at once. |
| "Envoyer" to the Chief of Staff, "pending" | new record, conflict today | no queue from the user to the Chief of Staff; `orders` go from the Chief of Staff to the Foreman and exist only inside a batch | See cross-cutting 2. |
| "Le batch suivant est prêt" | new record | nothing records the user's word before `open` | Today the word is said to the Chief of Staff, who runs `open` with a mode, slots and a budget the button does not ask. |
| "Injecter dans batch-N" | command exists | `chantier order add --note <folder>` (`src/commands.py:1120`), one per CR | Through the Chief of Staff. In a ready stack an insertion has its own procedure (concepts.md, "Inserting a change into a ready stack"). |
| Next-batch indicator ("3-ready changed since") | new record | compares the declared list with `3-ready` | Follows the record above. |

## Kanban

| Element | Class | Source or gap | Note |
| --- | --- | --- | --- |
| Column Intake (`1-inbox`) | now | `backlog[]` | |
| Column Grill (`2-backlog`) | now | `backlog[]`, P1 first | The name says more than the folder: a backlog item may be untouched or fully specified. |
| Column Ready (`3-ready`) | now | `backlog[]` | Same `"ready"` key bug. |
| Column In progress (queued, working, blocked) | now | `crs[].state` | |
| Column Ready (handed back `ready`) | now | `crs[].state` | Second column named "Ready": concepts.md forbids the confusion (lines 67-70). |
| Card title, slug, CR number, state tag | now | `crs[].cr`, `title`, `folder`; `backlog[].item`, `title` | Titles carry "Change Specification: "; `board.subject()` strips it (`src/board.py:87`). |
| Card description (first paragraph) | derivable | a file read per card | 13 items and 7 CRs today; better read once with the title in `status._title`. |
| Round bars "r/3" | now | `round`; the limit is `round_limit()` (batch setting or `order rounds`), in `label`, not as a field of `_row` | The prototype hard-codes 3. |
| Files count | now / derivable | `backlog[].files`; for a batch CR, a walk of its folder | |
| Dependencies count | derivable | `batch.json` `crs[].after`, not in `_row` | |
| Cost | now | `crs[].cost_usd`, `cost_unpriced` | |
| Filter chips | derivable | page code | Decorative in the prototype. |
| Merged and cancelled CRs | now | not drawn | The user's five columns leave them out; the count "N mergés" is `merged_total`. |

## Batch

| Element | Class | Source or gap | Note |
| --- | --- | --- | --- |
| Figures: batch, state, mode, steering, slots, spent | now | `batch_view()`, index `slots` | |
| Mode band | now | `mode` | Its three sentences need rewording: cross-cutting 5. `order mode` (series to stack) can change it mid-batch. |
| Dependency graph: nodes by level | derivable | `after` (CR ids) in `batch.json`; `rails.waits_for` (`src/rails.py:104`) | `after` holds only dependencies still open when recorded (a merged one "is met, not recorded"). In a series the predecessor is implicit (`series_predecessor`), not in `after`: the graph would draw a series with no arrow. The release's `after` is every other CR. |
| Arrows, hover highlight | derivable | page code | |
| Dependencies of items not yet in a batch | derivable | `depends.json` in the folder, by slug | Not drawn by the prototype. |
| "PR à revoir": the list | now | CRs in `ready` with a `pr` | See cross-cutting 5 for what "to review" may claim. |
| Stack place (#k) | derivable | `commands._chain()` (`src/commands.py:1613`): open CRs by `order`, the release last; `stacked` says the stack driver placed it | `_chain` is private to `commands.py` and not in any view. The prototype leaves the release out of the chain; chantier puts it on top. |
| Base ("on CR-n", "planned on") | now / derivable | each `ship` event records `base` (`src/commands.py:2347`); `_stack_base(planned=True)` gives the planned one | The prototype takes the CR below in the chain; chantier puts a CR with an open `after` on that dependency's branch (`src/commands.py:1661`). |
| Merge order, series | now | `order` | Only the bottom PR is ready to merge; the others are drafts until it merges. |
| Merge order, parallel ("the order they became ready") | derivable | the time of the last `handback` event with `result: "ready"` | The prototype sorts on `updated`, which any later `note` or `ship` moves. After each merge the other PRs are rebased and may go back to `working`. |
| Draft or ready on the forge, review state, CI | outside | not recorded; the Driver writes "draft on <base>: waits for …" in the hand-back's free text | Reading it needs `gh`/`glab`; `status.py` reads nothing from the forge by design (its docstring). |
| "Stack ready" (the five checks) | outside | `chantier forge-stack show` calls `gh`, GitHub only | Not recorded in `batch.json`. |
| One click opens the PR | now | `crs[].pr` | Link only an `http(s)` URL, as `board._url_link` does: `ship` accepts any text with `://`. |
| Drafts, greyed | now | CRs with a `pr` not `ready` (working, blocked) | |
| "PR mergées" of the batch, latest first | now | `merged_at`; `status._done_rows` (`src/status.py:392`) | The prototype sorts on `updated`. |
| Earlier batches' merged PRs | now | `merged[]`: `cr`, `title`, `batch`, `pr`, `cost_usd`, `when` | |
| Folder button on a PR card | now | `crs[].folder` | |

## Costs

| Element | Class | Source or gap | Note |
| --- | --- | --- | --- |
| Spent, budget, percent | now | `spent_usd`, `budget_usd`, `unpriced`, `priced` | Without a budget there is no percent. |
| Per-CR cost and bars | now | `crs[].cost_usd`, written by `_record_costs` (`src/commands.py:1489`) at each `status --refresh` and at `pause` | |
| "Somme des CRs", "le reste : le steering" | derivable | `spent_usd` minus the CRs' sum | The real split by role is `chantier cost` (read-only) or `cost --summary`. The Chief of Staff's own session is outside the batch's spend. |
| Age of the last computation | derivable | the `t` of the last `cost` event in `events.jsonl` (the board hides that kind from its feed but reads the file) | Backlog item `2-backlog/P3/status-spend-age` asks for this in `status` and STATUS.json. |
| "Recalculer", no agent turn | derivable, conflict if recorded | `commands._cost_rows` + `_cost_groups` in memory (what `chantier cost` does, read-only); or `_refresh(repo, batch, None)`, which records | Recording writes `batch.json`, a `cost` event and the STATUS files under the batch lock: the board "writes no file and takes no lock" (`src/board.py:5`). See cross-cutting 3. |
| Last merged CRs' costs | now | `merged[].cost_usd` | An archived batch's total (with its steering) is not kept after `close`. |
| Copilot batches | outside | pricing runs `uv` with a PyPI package (`costs.copilot_session_costs`) | A recompute there needs the network and a subprocess. |

## CR folder side panel

| Element | Class | Source or gap | Note |
| --- | --- | --- | --- |
| Head: CR, state, round, cost, priority | now | as above; the CR's own `STATUS.json` (`cr_view`) has more (steps, notes, branch, worktree) | |
| The folder as it is, every file | derivable | a recursive walk under the planning folder; `board._inside()` (`src/board.py:221`) already confines a path | Today `/file` lists one level as HTML. Needs a JSON listing. |
| File content on demand | derivable | `/file?p=` returns an HTML page with escaped text, cut at 1 MB | Needs a raw or JSON form. The prototype inlines every file in `data.js` (1.5 MB): the real page loads one file at a click. |
| Markdown rendered, JSON pretty-printed | derivable | page code (the prototype's own small renderer; its links are not clickable) | No dependency needed. |
| Images shown | conflict today | `/file` decodes everything as text; the CSP has no `img-src` | New: bytes with a content type, `img-src 'self'`, `nosniff` kept. SVG and HTML files must not run as documents: serve them as text or as a download. |
| Large or unknown files "served as a download" | derivable | not built | |
| A CR archived or trashed | now | `merged[].path`, `trashed[].path` | |
| The surface's privacy | now | the board serves only the planning folder; ignored local files (`batch.json`, `seat.json`, gate logs) are inside it and readable | With a token and a network bind, decide whether `seat.json` and raw logs stay readable. |

## "+ Intake"

| Element | Class | Source or gap | Note |
| --- | --- | --- | --- |
| Paste an idea | command exists, conflict today | `chantier file "<text>" [--slug]` (`src/commands.py:494`) | `AGENTS.md` names "filing an item" from the board as another CR. Through the queue, the Chief of Staff runs `file`. |
| An issue's URL | outside | fetching it is `gh`/`glab`, an agent's work; the CR keeps an `issue:` line | Fits the queue: the Chief of Staff fetches and files. |

## Cross-cutting

### 1. Several projects

- Layout: `<surface>/projects/<name>/{project.md, checkout.yml, changes/}`; `changes/` is the
  planning folder (`docs/planning-modes.md`, `Repo.changes`, `src/state.py:363`). Each project has
  its own batch, its own `seat.json` and, by the doc, its own Chief of Staff session.
- Today: one board per planning folder. `board()` on a surface with several projects and no
  `--project` fails on `SurfaceChoice`. With `--project`, each Chief of Staff starts its own board
  on the same default port 8765: `serve()` sees another planning folder behind the port, tries to
  bind and stops with "board not started" (`src/board.py:381-394`). The port can differ only
  through each clone's `chantier.yaml`, because `settings()` reads `repo.root / chantier.yaml` and
  `repo.root` is the clone in external mode (`src/board.py:361`).
- What one server for all needs, all inside `board.py`: started on the surface; `collect()` per
  project (each is one `batch.json`, one `events.jsonl`, up to 100 small STATUS files and a walk
  of the backlog: cheap); a project segment in every URL; `Repo` objects built once, since
  `Repo._external` runs `git rev-parse` twice.
- Open decisions, not code: which seat the surface board is tied to (it stops when "its" seat
  leaves, `src/board.py:315,399`), and where its address is configured (the surface has no
  `chantier.yaml` of its own today).
- "Tous les projets" is then a loop over the per-project view. Limit: batch, PRs and cost exist
  only for projects steered on the machine that runs the board.
- Several plain repositories that are not one surface: chantier keeps no list of projects on a
  machine, and a new machine-level configuration would break "AGENTS.md and chantier.yaml are the
  only configuration". Keep to the surface.

### 2. Writes

Every state change in the prototype, and what would carry it:

| Action in the page | Existing command | Gap |
| --- | --- | --- |
| Priority P1..P4 | `triage <item> --priority P<n>` | none |
| To `3-ready` | `triage <item> --ready` | none |
| Back to Inbox | none | a new option, or drop it |
| Abandon | `abandon <item>` | none |
| Rank inside a priority | none | new record |
| Group, join, undo | none | new record and a new concept |
| "Next batch is ready" | none (`open` is the Chief of Staff's, with mode, slots, budget) | new record, or only a message |
| Inject into the batch | `order add --note <folder>` | none |
| Intake (text) | `file "<text>"` | none |
| Intake (issue URL) | `file` after a fetch by the agent | outside the CLI |
| Slots, budget, rounds, drop, note, hold | `order slots|budget|rounds|drop|note` (hold is `order slots --note 0`) | in 02-answers, not in the prototype |
| Recompute costs | `status --refresh` without `--epoch` | see point 3 |

What "the Chief of Staff applies it" (02-answers) implies:

- The server runs none of these commands, though `file` and `triage` are role-free, locked
  (`changes_lock`) and safe to run from any process. The user's rule costs one agent turn per
  batch of changes; in return a surface's commit and push stay with the Chief of Staff, and
  nothing moves that it has not seen.
- A **queue record is needed**: none exists. `orders` are the Chief of Staff's word to the
  Foreman, live only in `batch.json` (no batch, no orders) and take a fixed list of kinds;
  `asks` go the other way. The queue is a new local file of the planning folder (ignored like
  `seat.json`), appended by the board process under the lifecycle lock, by atomic write: the
  board is the CLI, so "the CLI alone writes" holds, but "the board writes no file" and "GET and
  HEAD only" do not. `AGENTS.md` already says this is another CR; that CR must amend the
  sentence.
- A **role-free command** to read the queue and mark an entry handled (as `asks --read` and
  `order done` do), so the page can show "pending" then "done" or "refused: <reason>". The CLI
  must not know the reader is the Chief of Staff; the card (`chief-of-staff.md`) says when to
  read it.
- **Nothing wakes an idle Chief of Staff.** It acts at a turn: when the user writes to it, or,
  in direct mode, at its own wakes. Waking a session from a web page is the host's business, not
  chantier's. In Foreman mode a batch order then needs two turns (Chief of Staff, then Foreman).
- **"With the session closed, the page says so" cannot be met from the record.** The seat keeps
  no date on purpose ("no activity date is ever taken as proof of life", concepts.md lines
  184-187). The page can say who holds the seat, that none does, and how old the oldest pending
  entry is.
- Drafts kept in the browser are per device; the queue is the first place both devices share.

### 3. Liveness and the cost of reading

- State: the board computes its view from `batch.json` and the folders at each request
  (`collect`, `src/board.py:58`), so it is as fresh as the last CLI command. It does not depend on
  the STATUS files. A page that polls a JSON endpoint every 15 to 30 seconds costs little: one
  `batch.json`, one `events.jsonl` (20 KB today), at most 50 archive and 50 trash STATUS files, a
  walk of the backlog. `status` itself answers in 0.4 s here, `uv` start included.
- Costs: `spent_usd` and `cost_usd` move only at `status --refresh` (the steering session's wake)
  and at `pause`. Between two wakes they are stale and nothing in the view says how old (the
  heartbeat was 22 minutes old when measured).
- Pricing reads every steering transcript and each subagent's: 2.6 MB plus 129 files, 19 MB, for
  batch-16 so far. `chantier cost --by cr` took 4.0 s (that includes the Chief of Staff's
  whole-session line, which a refresh skips). It grows with the batch. Too heavy for each page
  load or each poll; fine behind a button, with the result kept in the server's memory with its
  time, and one computation at a time.
- Two ways for the button. In memory (as `chantier cost`): the board stays write-free, but its
  figure is newer than the recorded one the budget reads, and the page must say "computed now,
  not recorded". Recorded (as `status --refresh`): one figure everywhere, but the board writes
  `batch.json`, and a spend recorded from a phone can make the next `take` or `round` refuse on
  the budget sooner than the steering session's own wake would.

### 4. Phone and remote access

- Today: `127.0.0.1:8765` by default; a wider address by `board.host` in `chantier.yaml` or
  `--host` (`src/board.py:359`); no authentication at all, said at start ("no password",
  `src/board.py:396`) and by the Chief of Staff; plain HTTP; POST and the rest answer 405; a CSP
  of `default-src 'none'; style-src 'unsafe-inline'; form-action 'none'`.
- This repository has no `chantier.yaml`, so the board is on loopback: that alone explains
  "works on the PC, not from the phone". On Windows a first listen on `0.0.0.0` also meets the
  system firewall, which is the machine's, not chantier's.
- The prototype assumes: scripts (the whole page is one script), images, `fetch`, a token, a
  write channel. Each needs a change: `script-src 'self'` with the script served as its own file
  (no inline script), `img-src 'self'`, `connect-src 'self'`, the page shipped inside the CLI's
  package as a plain file (standard library only holds; the prototype loads nothing from outside).
- The token: none today. The cheapest form writes no file: generated at start (`secrets`),
  printed in the board's first line, which the Chief of Staff already reads and relays; checked
  with a constant-time compare; exchanged for a cookie at the first visit so it leaves the URL.
  Cost: a new token at each start breaks the phone's bookmark; a kept token is one more local
  ignored file. `serve()`'s own probe of `/api/status` (`src/board.py:338`) needs a path that
  answers without the token. Over a LAN in plain HTTP the token can be read on the wire; over
  Tailscale it cannot.
- The page's language: the prototype is in French; the repository's text is English
  (`AGENTS.md`), and `board.py`'s page is.

### 5. Where the prototype says something chantier does not mean

1. **Two columns named "Ready"** (`proto:423,425`), and `ready` translated "prêt à merger"
   (`proto:399`). concepts.md: `3-ready` "is not ready to merge", and a CR handed back `ready` is
   ready to merge only when its PR's base is the default branch or its stack is verified on the
   forge (lines 9-16). In a stack or a series most `ready` CRs have a draft PR.
2. **Stack: "tu merges de bas en haut", "la #1 d'abord"** (`proto:496,530`). chantier: the user
   merges the whole stack in one action from its top PR, once the five checks hold (GitHub); on
   GitLab the stack stays a chain. The numbered places are right as the stack's order, not as a
   merge order.
3. **The release CR "sur main, hors stack"** (`proto:504,518`). Only a fix CR is outside. The
   release is the top of a stack or a series, on the top CR's branch (`_chain`, `_start_base`);
   it is on the default branch only in a parallel batch, after the merges.
4. **A PR's base taken from the chain's neighbour** (`proto:515`). A CR with an open dependency
   sits on that dependency's branch; before `stack` marks it, on its start base.
5. **`"ready"` for `3-ready`** (`proto:423,666,669,704`): the record's value is `"3-ready"`.
6. **State colours.** The prototype: working blue, ready green, merged violet. chantier's icons
   (`status.icon`, `src/status.py:83`): working yellow, ready blue, merged green check, and orange
   for a queued or blocked CR that only waits. The colours are the user's choice in 02-answers;
   the orange case (waits, nobody has to act) has no place in the prototype and inflates
   "T'attendent".
7. **"Grill" for `2-backlog`**, "à griller" for any item without a specification, and no
   `specifying` state.
8. **Events** read with the wrong fields (Home table above), so hand-backs show no result and
   merges never show.
9. **Rounds "/3"** fixed; the limit is per batch and per CR.
10. **"Données : il y a N"** is the snapshot's age; live, the ages that matter are the spend's and
    the heartbeat's.
11. **"Recalculer : aucun tour d'agent"** is true, but it is not free of effect if it records
    (point 3).

## Gaps that block a first real version, cheapest path for each

For a first version that only reads (the split 02-answers already proposes):

1. **The page cannot run on today's board** (CSP, HTML-only `/file`, no JSON beyond
   `/api/status`). Path: in `board.py`, serve the page and its script as two package files, loosen
   the CSP to `'self'` for scripts, images and fetches, add a JSON folder listing and a raw file
   response (text, images with their type, the rest as a download).
2. **Fields the views need are in `batch.json` but in no view**: `after`, `kind`, `order`,
   `stacked`, `merged_at`, `created`, the round limit, the stack place and base, the cost's age,
   the "in grill" flag. Path: add them to the board's own data in `collect()` (it already reads
   `batch.json` and `events.jsonl`), not to `STATUS.json`: no schema change, and the pane's
   screenshot rule is not touched. Move `_chain` and `_stack_base` where `board.py` may import
   them.
3. **Several projects.** Path: a surface mode of `chantier board` (list, per-project `collect`,
   project in the URL), and one decision from the user: which seat the surface board follows.
4. **The token and the bind.** Path: an in-memory token printed at start, cookie after the first
   visit; `board.host` as today. One decision: whether it guards reads too (the planning folder
   holds requests, grills and raw logs).
5. **The wrong semantics** (point 5, items 1 to 5 and 8): reword and rename before any code; no
   record needed. Page text in English.
6. **Costs on demand.** Path: the in-memory computation behind the button, cached, labelled "not
   recorded"; the recorded age from the last `cost` event. Take `status-spend-age` (P3) with it.

For the version that acts, in this order:

7. **The rule itself**: `AGENTS.md` ("writes no file … another CR") and `board.py`'s read-only
   contract. Path: the acting CR amends the sentence and names what the board may write: the
   queue file only.
8. **The queue**: a local queue file, a POST endpoint behind the token, a role-free command to
   list and close entries, a paragraph in `chief-of-staff.md`. This carries, with commands that
   already exist: priorities, `3-ready`, abandon, intake, inject, slots, budget, rounds.
9. **No wake of the Chief of Staff, no proof it is alive**: accept "handled at its next turn" and
   show the pending entry's age; anything more is the host's.
10. **Groups, rank inside a priority, "the next batch is ready", back to Inbox**: each needs a
    new record or command. Cheapest: leave groups and rank out of the first acting version (or
    keep groups as free text sent in the queue entry), send "the next batch is ready" as a plain
    queue message with the list, and drop the Inbox target.

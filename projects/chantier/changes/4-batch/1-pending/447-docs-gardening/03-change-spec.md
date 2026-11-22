# Garden the docs, the README and the SVGs after batch-30

The user's docs (`docs/`), the `README.md`, CONTRIBUTING.md's "How the project is built" and the
SVG diagrams describe chantier as it was days ago. This CR brings them in line with chantier as
batch-30 leaves it, and with what merged since each page was last reviewed whole. It is the last
CR of batch-30. Its specification names the areas to check and the method; the exact list of
fixes is fixed by its Driver, at its start, against what has landed. It writes no behaviour:
docs, pictures and diagrams only, with one exception, the board's Help texts that batch-30 made
false (docs-garden-Q5, below).

## Goal

In the user's words (2026-11-21): "il faudra que tu lances un gardening de la doc, du readme et
des svg qui sont plus à jour". A reader of the README, of `docs/` and of CONTRIBUTING.md's "How
the project is built", a viewer of the diagrams and a reader of the board's Help page see
chantier as it runs at the end of batch-30: the right commands, states, roles, arrows, folders
and board views, and nothing that has been removed.

## Decisions carried from `02-answers.md`

1. **Scope (docs-garden-Q1, A).** Everything batch-30 delivers, plus what merged since the docs
   were last brought up to date. The CR runs after every other CR of batch-30, on top of the stack.
2. **The SVGs (docs-garden-Q2, A).** Fix the SVGs that are wrong (states, roles, arrows). Draw a new
   SVG only for a role or a view that no diagram shows.
3. **Destination.** batch-30, last ("met doc gardening à la fin du batch en cours").
4. **Restatement.** The Driver fixes the exact list against what has merged when it starts; the
   specification does not pre-write the doc text.
5. **CONTRIBUTING.md (docs-garden-Q3).** Its "How the project is built" section only ("What is
   chantier?" and "Repository layout"), one more inventory page, fixing only what is false: no
   restructuring, no de-duplication. The rest of the file stays with each CR that changes a rule.
   It joins the removed-words search. This goes beyond the user's named list on a Fable advisor's
   answer: the user may strike it.
6. **`docs/batch-pace.svg` (docs-garden-Q4).** Out of scope: on 2026-11-07 the user said it stays
   untouched, a diagram they have not finished (archives 261106-2211-139-docs-svgs and
   261107-1737-150-docs-lifecycle); no page links it. The inventory lists it with that reason.
7. **The board's Help texts (docs-garden-Q5, A, bounded).** The CR corrects a Help text that
   batch-30 made false, in `skills/chantier/scripts/cli/src/chantier/clients/web/js/i18n/en-help.js`
   and `fr-help.js` together (both languages, within their word limits: English at most 150 words
   per body, French at most 175), and a topic's `doc` link in `js/views/help-topics.js` when the
   heading it names changed. It renames a README or docs heading a Help topic links to only when
   the heading itself is false, and fixes the link in the same commit. No other web-client file
   changes. If CR-439 (`board-help-page`) is cancelled or dropped, there is nothing to correct. The
   gates this brings are in "Gates" below.
8. **The batch Kanban (docs-garden-Q6).** No new SVG: `docs/cr-folder-lifecycle.svg` already draws
   a batch CR's three folders (`1-pending`, `2-actives`, `3-done`), so by docs-garden-Q2 nothing is
   missing. The Kanban is shown by its retaken screenshot in `docs/web-board.md` (the Batch page's
   default view, `docs/web-board/batch-pc.png` and `batch-phone.png`), and the inventory records
   the check. The user may strike this answer.

## When the Driver starts, and what it reads

### Order

This CR is taken last in batch-30 (batch-30 runs in stack mode), on top of the stack, so its base
holds every other CR of the batch. This is a real need, not a shared file: the CR reads what the
other CRs wrote. When it is queued in batch-30, its folder carries a `depends.json` whose `after`
lists every other CR of batch-30 by slug:

```json
{"after": ["factory-redefine", "board-exposure", "board-running-batch-lane",
  "drop-to-next-batch", "board-fingerprint-cache", "park-live-cr", "hold-live-cr",
  "permissions-bypass", "board-batch-chip-stale", "board-batch-kanban", "board-batch-compact",
  "sync-blocked-by-others", "sync-lock-wait", "stack-shape-guard", "board-help-page",
  "board-triage-polish", "board-batch-view", "stack-git-chain", "gate-hold-narrowing",
  "board-user-inbox", "board-history", "live-several-boards-and-keys"]}
```

(CR-425 to CR-446, as batch-30 holds them on 2026-11-21.) When another CR joins batch-30 later
(for instance `dashboard-pages` or `board-griller`), the Foreman adds its slug to this list; it
goes below this CR, and the Driver checks its areas as in "A CR below changes". The Driver starts
when every other CR of batch-30 has handed back ready, is merged, or is cancelled or dropped.

### What counts as landed

A CR of batch-30 counts when it is merged on `main`, or handed back ready and present in this CR's
base. A CR cancelled or dropped out of batch-30 counts as not delivered: the docs describe none of
its behaviour, and the Driver removes any text its own PR wrote ahead of time if that text reached
the base.

### The baseline, page by page

A page's baseline is the last commit on `main` that reviewed the whole page: a `docs:` alignment
commit such as `e6d8213c` (2026-11-14, "docs: align the README, use cases, diagrams and
CONTRIBUTING with a merge that may come at any moment"), or a full refresh of the pictures such as
`607c2575` (2026-11-18, "docs(board): refresh the board screenshots..."). Where no such commit
exists for a page, the inventory gives an explicit date for it, with one line of why (the page's
creation, for instance). A batch CR's partial edit of a page (one paragraph, one section) does not
move its baseline: the page's other sections still date from the earlier review.

From the baseline, the Driver lists the commits that change behaviour the page describes: commits
under `skills/chantier/scripts/cli/src/` (the web client included), `skills/chantier/references/`,
`hooks/`, `config/`, `agents/`, `com.github.copilot/agents/`, `scripts/` and the `justfile`, plus
the batch's CR branches below this one. It reads their subjects, and their diffs where the subject
is not enough.

### The batch's CRs, and what they edit themselves

For each CR of batch-30, the Driver reads its `03-change-spec.md` (in the planning surface,
`projects/chantier/changes/4-batch/1-pending/`, `2-actives/` or `3-done/`, or the archive once
closed) and its PR's diff. Many update docs or pictures themselves. This CR checks that those edits
landed and hold together, and does not write them again. It fixes what the CRs left: the other
pages that say the same thing, the diagrams they did not touch, the pictures they did not retake,
and a text made false by a later CR of the batch. The edits known at this specification (from the
CRs' specifications):

| CR | Docs and pictures it edits itself |
| --- | --- |
| CR-425 `factory-redefine` | README "Running batch or next batch" (replaces "Factory mode"); the links in `docs/use-cases.md`, `use-cases-direct.md`, `use-cases-foreman.md`; the `batch-lifecycle` pair; `docs/server-api.md` if it adds a move target |
| CR-426 `board-exposure` | README "The CR board"; `docs/web-board.md`; `docs/boards.md` line 3; CONTRIBUTING.md's board bullet (line 99) |
| CR-427 `board-running-batch-lane` | `docs/web-board.md` "Triage" and its "writes in the backlog only" sentence; the Triage screenshots; `docs/server-api.md`; `docs/planning-folder.md` (`board@1` row); README "Running batch or next batch" (one sentence) |
| CR-428 `drop-to-next-batch` | the `cr-folder-lifecycle`, `cr-lifecycle-simple` and `cr-lifecycle` pairs; `docs/planning-folder.md` (`order drop`) |
| CR-429 `board-fingerprint-cache` | `docs/web-board.md` "Starting the board" and its known limit (network shares, WSL `/mnt`); `docs/server-api.md` "The topics"; `docs/planning-folder.md` (`source`: `hub`); `docs/forge-connectors.md` "The budget"; CONTRIBUTING.md's hub and watcher sentences (lines ~89-91, ~122-134) |
| CR-430 `park-live-cr` | README, `docs/use-cases-foreman.md`, `docs/use-cases-direct.md` (a parked CR); the `batch-lifecycle` pair |
| CR-431 `hold-live-cr` | none (the cards carry it) |
| CR-432 `permissions-bypass` | none in `docs/` or the README |
| CR-433 `board-batch-chip-stale` | `docs/web-board.md` "Batch" (the priority-chip sentence) |
| CR-434 `board-batch-kanban` | `docs/web-board.md` "Batch" (Kanban / Graph); retakes no picture |
| CR-435 `board-batch-compact` | `docs/web-board.md` "Batch"; `docs/web-board/batch-pc.png`, `batch-phone.png`, `batch-gantt-pc.png`, `batch-cards-pc.png`, `panel-pc.png`, `panel-phone.png` |
| CR-436 `sync-blocked-by-others` | `docs/web-board.md` "By hand"; CONTRIBUTING.md's CLI paragraph of the architecture list (in "What is chantier?") and "In this checkout, `$CHANTIER` runs the local code, live" (in "Set up", outside this CR's section) |
| CR-437 `sync-lock-wait` | CONTRIBUTING.md "A CLI" (line ~76) and the "In this checkout" paragraph (outside this CR's section) |
| CR-438 `stack-shape-guard` | `docs/use-cases-foreman.md` only if its Driver judges it needed |
| CR-439 `board-help-page` | `js/i18n/en-help.js`, `fr-help.js`, `js/views/help-topics.js`; no docs page (`docs/web-board.md`'s Help section and picture are this CR's, help-Q11) |
| CR-440 `board-triage-polish` | `docs/web-board.md` "Triage"; `triage-pc.png`, `triage-phone.png`, `triage-selection-phone.png` |
| CR-441 `board-batch-view` | `docs/web-board.md` "Batch"; the new `batch-graph-pc.png`; `docs/demo/`; the batch, Kanban and panel pictures its run changes |
| CR-442 `stack-git-chain` | none in `docs/` (scenario README only) |
| CR-443 `gate-hold-narrowing` | `docs/gates.md`, `docs/planning-folder.md`, `docs/agents-and-models.md`, `docs/tutorial-claude-code.md`, the README's init paragraph, `docs/server-api.md` |
| CR-444 `board-user-inbox` | `docs/web-board.md` "### Inbox"; `inbox-pc.png`, `inbox-phone.png`; `docs/server-api.md` (`board.get`); `docs/demo/` |
| CR-445 `board-history` | `docs/web-board.md` "History" (no picture); `docs/server-api.md` (`history.get`); `docs/planning-folder.md` |
| CR-446 `live-several-boards-and-keys` | `docs/boards.md` "The live terminal view"; `docs/server-api.md` "A terminal client" |

Each row is confirmed against the CR's PR, not assumed.

### The inventory

Before it edits anything, the Driver writes `work/garden-inventory.md` in the CR's folder. It has
one row per page, diagram pair or picture checked: the file, its baseline (commit or date), the
commits and CRs that touch it, and a verdict (`holds`, `fixed`, `new`, `kept`, or
`out of scope`, with one line of why). The inventory is the CR's working list and its evidence. A
page that holds is listed too, so the Verifier sees that it was read.

## What changes, area by area

The lists below are where to look, with the changes known when this specification was written.
They are a starting point, not the fix list: the inventory decides the list.

### 1. The README (`README.md`)

Check every section against what landed: "How Chantier works", "Planning modes", "Batch modes",
"Running batch or next batch" (CR-425, CR-427), "What a batch costs", "Change Requests Lifecycle",
"Detailed lifecycle", "Releases", "The CR board" (its picture `docs/web-board/batch-pc.png` and its
caption, "a batch in stack mode, its CRs by level", against the Batch page that now opens on the
Kanban), "Install" (the allow rules of preflight's P10, from CR-432), "Use" (the table of what you
say and what happens: for instance the `our long gate is npm test` row, against CR-443's
`long_gate.commands` in `chantier.yaml`, and the `drop CR-103` row, against CR-428's destinations)
and "More" (one link per page, a new page included).

### 2. The reference pages (`docs/*.md`)

Each page is read against the behaviour that landed. Known areas:

- `docs/web-board.md` and `docs/boards.md`: the board bound to `127.0.0.1` by default,
  `board.host: network`, `board --new-key` and the 30-day cookie (CR-426); the backlog's last
  column split into running batch and next batch (CR-427); the server reading the planning files
  on OS notifications, watchers subscribing, and the board a watcher starts stopping after its last
  client (CR-429); the Batch page's Kanban / Graph toggle, Kanban by default (CR-434); the mode band
  and the legend line moved into the top rows (CR-435); a batch CR's card showing its batch folder
  (CR-433); the Batch view's later changes (CR-441); the Inbox (CR-444) and History (CR-445) pages;
  the live terminal view with several boards and keys (CR-446).
- **Help in `docs/web-board.md` (help-Q11, docs-garden-Q5).** A section `### Help` under "The
  views", after the Inbox's: what the page shows (the concept cards and the role cards, under two
  headings, a detail on click, a "read more" link to the README or a docs page, those pages in
  English), and its picture `web-board/help-pc.png`; `help-phone.png` joins the phone pictures
  named under "On a phone". Section 4 says how they are taken.
- `docs/server-api.md`: the key and cookie (CR-426), the subscriptions and the file watching
  (CR-429), the running-batch move target (CR-427), `lease hold` (CR-443), `board.get` (CR-444),
  `history.get` (CR-445), the terminal client (CR-446), and any other protocol change the batch
  made (protocol 1 takes additions only).
- `docs/forge-connectors.md` and `docs/planning-folder.md`: the hub, watchers and server lifecycle
  (CR-429); `order drop`'s destinations (CR-428); the configuration keys the batch added
  (`board.host`, `long_gate.commands`).
- `docs/gates.md`: the long gates named in `chantier.yaml`, `gate` refusing a free command, and
  `lease hold` running nothing (CR-443).
- `docs/use-cases.md`, `docs/use-cases-foreman.md`, `docs/use-cases-direct.md`: running batch or
  next batch (CR-425); the Foreman parking a CR stuck on an outside wait (CR-430); `order hold` and
  `unhold` on a live CR in every mode (CR-431); a stack keeping its shape (CR-438) and checked as a
  git chain (CR-442).
- `docs/tutorial-claude-code.md` and `docs/hosts.md`: the P10 allow rules with real paths
  (CR-432); how the board is reached from a phone (CR-426).
- `docs/agents-and-models.md`, `docs/costs.md`, `docs/planning-modes.md`,
  `docs/release-process.md`: read for anything the batch or the earlier merges changed.
- Merged before batch-30 and named by no page at this specification (to confirm, not assumed):
  `chantier wait` (typed waits, 9b55b0a4), `chantier access` (daec1986), leases (`--lease`,
  `lease renew`, e461ffd2) and `order hold` on a ready CR (f9087d67). Each goes where a reader
  would look for it, or the inventory says why it stays in the cards only.

`docs/release-notes/` is history and does not change. `docs/demo/` changes only as far as the
screenshots need (section 5).

### 3. CONTRIBUTING.md, "How the project is built" (docs-garden-Q3)

Only this section (from `## How the project is built` to the line before `## Set up`: "What is
chantier?" and "Repository layout"). Fix only what is false; no restructuring, no de-duplication.
The batch edits it in several places, which this CR checks rather than rewrites: CR-426 (the board
bullet, line ~99), CR-429 (the hub and watcher sentences, lines ~89-91 and ~122-134), CR-436 (the
CLI paragraph of the architecture list) and CR-437 ("A CLI", line ~76). Known areas besides those:
the board, the hub and watchers, `gate`, `lease hold` (CR-443), the web client's pages (CR-439,
CR-444, CR-445), `chantier live` (CR-446), and the repository layout against the files that
landed. The rest of the file (the "In this checkout" paragraph of "Set up" included) is not edited
here: a false sentence found there is reported to the Foreman as a finding.

### 4. The SVG diagrams (`docs/*.svg` and their `*-texts.md`)

Eleven diagrams, each with its `-texts.md` companion: `batch-lifecycle`, `batch-modes`,
`cr-folder-lifecycle`, `cr-lifecycle`, `cr-lifecycle-line`, `cr-lifecycle-simple`,
`how-chantier-works`, `how-chantier-works-simple-direct`, `how-chantier-works-simple-foreman`,
`planning-modes`, `release-driver`. `docs/logo.svg` is not a diagram. `docs/batch-pace.svg` is out
of scope (docs-garden-Q4); its inventory row says why.

- **Fix what is wrong.** States (parked, held), roles, arrows, commands and folders, against what
  landed. Known areas: the factory batch in `batch-lifecycle` (CR-425); `order drop` going to
  `1-inbox/` in `cr-lifecycle`, `cr-lifecycle-simple` and `cr-folder-lifecycle` (CR-428: P1-P4,
  `3-ready`, trash); park and hold in `batch-lifecycle`, `cr-lifecycle` and `batch-modes` (CR-430,
  CR-431); the grilled-enough step's destination choice in the `cr-lifecycle` pairs and
  `how-chantier-works*` (CR-425); the server, hub and watchers wherever a diagram draws them
  (CR-429).
- **One text, two files.** A diagram's `-texts.md` holds its words (the description, the header,
  the legend, the lanes), and the SVG's `<title>`, `<desc>` and visible text say the same. A fix
  goes into both. The Driver also fixes any drift between the two that it finds. For instance, at
  this specification `cr-folder-lifecycle.svg`'s `<desc>` says ".agents/changes/" where its
  `-texts.md` says "the planning folder (.agents/changes/ or an external surface)", and the
  `<desc>` lacks the texts' sentence on the archive in the PR.
- **The batch Kanban (docs-garden-Q6).** No new SVG: the inventory's row for
  `cr-folder-lifecycle` records that it draws `1-pending`, `2-actives` and `3-done`, and the
  Kanban is shown by its screenshot (section 5).
- **A new SVG only for what is missing (docs-garden-Q2).** For a role or a view that no diagram
  shows, found by the inventory. A new SVG follows the existing ones (the same font stack, palette,
  emoji legend and monospace commands), comes with its `-texts.md`, and is linked from the README
  or a page of `docs/`.
- An SVG stays hand-written, as today. No generator is added.
- **The surface server (the user, 2026-11-22).** No diagram draws it today (`how-chantier-works`
  draws the CLI as one box; `planning-modes` names the writer in one line), so a new SVG,
  `docs/surface-server.svg` with its `-texts.md`, draws it, linked from `docs/web-board.md` and from
  CONTRIBUTING.md's "How the project is built"; `how-chantier-works` gains a small server box that
  points to it. It shows: the planning folder as the only truth (plain JSON and Markdown, edited by
  the CLI, the agents, git and the user; no database); one process with its roles: the web board
  and its published API (WebSocket, and HTTP as the same protocol) behind a key, the forge hub
  (read-only forge reads, at most every 20 s, journal lines), the writer (commits, rebases and
  pushes the surface's published paths within 5 minutes); each session's watcher reading only its
  project's journal and waking its session; the clients (web, `chantier live`, any API client);
  how it reads: each project's state in memory behind a fingerprint of the folder (a stat walk, no
  file opened), the OS's change notifications (`watchfiles`), one walk once a project's files are
  quiet 1 s (at most 5 s), only the last folders of the archives and the trash. Its words come from
  the code at the head (`board/fingerprint.py`, `board/watch_files.py`, `hub/`, `writer/`) and
  AGENTS.md, never from this list where they differ.

### 5. The pictures (`docs/web-board/*.png` and the other `docs/*.png`)

Every `docs/web-board/*.png` is an inventory row: `batch-cards-pc`, `batch-gantt-pc`, `batch-pc`,
`batch-phone`, `config-pc`, `config-phone`, `costs-pc`, `costs-phone`, `editor-pc`,
`editor-phone`, `home-pc`, `home-phone`, `kanban-pc`, `kanban-phone`, `new-pc`, `new-phone`,
`panel-pc`, `panel-phone`, `picker-pc`, `picker-phone`, `project-pc`, `project-phone`,
`triage-pc`, `triage-phone`, `triage-selection-phone`, `writer-pc`, `writer-phone`, plus those the
batch adds (`batch-graph-pc` from CR-441, `inbox-pc` and `inbox-phone` from CR-444) and the two
this CR adds (`help-pc`, `help-phone`).

- **Why most change.** Help (CR-439) and Inbox (CR-444) join the sidebar, so every desktop picture
  shows a sidebar a CR before them did not have; `panel-pc.png` shows the Batch page beside the
  panel, so it follows the Batch page's changes (CR-434, CR-435, CR-441).
- **The Help view.** `scripts/docs_screenshots.py` gains, in `views()`, after the Inbox's step:
  `goto(page, url, "help", "shop-api")` and `shot(page, "help", size)`, the page with its cards and
  no detail open. It writes `docs/web-board/help-pc.png` and `help-phone.png`. If the Help route
  takes another view name than `help`, the Driver uses the one CR-439 shipped.
- **One run, at the head.** The Driver runs `just docs-screenshots` (`scripts/docs_screenshots.py`,
  from `docs/demo/`) once at its head, after the last restack. A picture whose view did not change
  (same page, same sidebar, same data) is restored from the base (`git checkout -- <file>`), so the
  PR carries only real changes; each picture the PR carries is looked at, and its inventory row says
  what it now shows. If the script needs other demo data, the Driver adds it in `docs/demo/`.
- If `just docs-screenshots` cannot run on the Driver's machine (no Chromium, no network for
  Playwright), the Driver stops and says so: no picture is made another way.
- **Kept pictures.** `docs/board-mod-batch.png`, `board-mod-batch-done.png`,
  `board-mod-batch-prs-light.png`, `board-mod-merged-light.png` and `board-mod-waiting-light.png`
  (the CR board pane, in `docs/boards.md`) are kept: this CR changes neither `hooks/register.tsx`
  nor `status.py`, so no pane screenshot is owed. `docs/direct-mode-session.png` (README) and
  `docs/status-report-done.png` (`docs/costs.md`, `docs/tutorial-claude-code.md`) are real
  session captures that `just docs-screenshots` does not make: they are kept, and if one shows
  something false, its row says so and the Driver reports it to the Foreman as a finding.

## Out of scope

- Any behaviour change, in the CLI, the cards, the hooks or the web client, except the Help texts
  and `doc` links of docs-garden-Q5 (`en-help.js`, `fr-help.js`, `help-topics.js`). No other
  web-client file changes. A doc that cannot be made true without a behaviour change goes back to
  the Foreman as a finding.
- `AGENTS.md` (the project's rules, kept by each CR that changes a rule), the cards
  (`skills/chantier/references/`), `clients/web/DESIGN.md` (read first when Help changes, not
  edited), `scenario/README.md` and the eval docs (`evals/`).
- CONTRIBUTING.md outside "How the project is built".
- `docs/batch-pace.svg` (docs-garden-Q4).
- A new SVG for the batch Kanban (docs-garden-Q6).
- `docs/release-notes/` (history; pinned to their tags).
- The behaviour of a CR cancelled or dropped out of batch-30.

## Gates

Conditional on a Help edit (docs-garden-Q5):

- **With no Help edit**, the CR is docs-only (a change to `scripts/docs_screenshots.py` or
  `docs/demo/` is neither the CLI's `src/` nor `evals/kit/`): no `just eval-dry-run` and no
  `just scenario (ubuntu-latest)` before its PR.
- **With a Help edit**, it is a change under the CLI's `src/`: the Driver reads
  `skills/chantier/scripts/cli/src/chantier/clients/web/DESIGN.md` first, runs `just check` and
  `just eval-dry-run` in the worktree at the rebased head before its first push, and the
  pipeline's `just scenario (ubuntu-latest)` is green at the PR's head.
- Either way, `just check` passes before the first push, and as the CR on top of batch-30's stack,
  it passes `just scenario` locally (`chantier gate`) at its head before the user merges: the
  batch's Windows coverage. The local run moves to it when it joins on top.

## Evidence

- `work/garden-inventory.md`: every page, diagram pair and picture of sections 1 to 5, each with
  its baseline, the commits and CRs that touch it, and its verdict; `batch-pace.svg` with its
  reason; the Kanban check of docs-garden-Q6.
- `just check` passes at the head. Among its tests, `test_skill_and_references_links_resolve`
  (`skills/chantier/scripts/cli/tests/test_plugin_files.py`) reads the shipped `README.md` and
  `docs/*.md` at the head under test and checks that every relative link's file resolves (it drops
  the `#anchor`). When CR-439 has landed, its test
  `test_the_help_page_is_a_view_with_both_languages_and_real_links`
  (`tests/test_board_design.py`) reads the shipped `help-topics.js`, `en-help.js` and `fr-help.js`
  and checks each topic's `doc` file and `#anchor` against the shipped README and docs headings,
  and the word limits: it is the anchor check for every Help link, and it guards a renamed heading
  a Help topic names.
- **Anchors and new files**, by a short script the Driver keeps in `work/`, run at the head on the
  shipped files, its output in `work/verifier/evidence/`:
  - every `#anchor` link in `README.md`, `docs/*.md` and CONTRIBUTING.md (relative links, and
    links to `https://github.com/gsemet/chantier/blob/main/...`) resolves to a heading of its
    target file (GitHub's slug: lower case, spaces to `-`, punctuation dropped); this covers every
    link to a heading this CR renamed. For each renamed heading, the Driver also searches the whole
    repository for the old slug; a link in a file this CR does not edit (a card, `AGENTS.md`) goes
    to the Foreman as a finding, and the heading keeps its old name until the Foreman answers;
  - each file this CR adds under `docs/` (`git diff --name-only --diff-filter=A <base>...HEAD --
    docs/`) is named in `README.md` or a `docs/*.md` page.
- For each changed or new SVG, at the head, from the shipped files (no copies):
  - it parses as XML (`python -I -c "import xml.etree.ElementTree as E,sys; E.parse(sys.argv[1])"
    <file>`);
  - its `<desc>` equals the description paragraph of its `-texts.md`, compared by a short script
    the Driver keeps in `work/`, whose output goes in `work/verifier/evidence/`;
  - it is rendered to a PNG at its `viewBox` size (Chromium through Playwright, as
    `docs_screenshots.py` uses), saved in `work/verifier/evidence/`, and looked at for overlapping,
    clipped or overflowing text.
- **The removed-words search**, at the head, in `README.md`, `docs/*.md`, `docs/*-texts.md`,
  `docs/*.svg`, CONTRIBUTING.md, and `js/i18n/en-help.js` and `fr-help.js`, for what batch-30
  actually removed: "factory mode" (any case, and its French wording in `fr-help.js`), the command
  `order factory`, `0.0.0.0` named as the board's default address, and `order drop` sending a CR to
  `1-inbox`; plus any word the inventory names. Bare `factory` and bare `0.0.0.0` are not searched
  terms (a sentence may name an address a user chooses). Each hit that remains is listed with why
  it holds; a hit in CONTRIBUTING.md outside "How the project is built" goes to the Foreman.
- Retaken and new pictures: the `just docs-screenshots` run's output, and the PNGs in the PR's
  Deliverables, captioned with the head's SHA (seven characters).
- With a Help edit: the edited texts in both languages in the PR's Deliverables, and the gates of
  "Gates" above.

## A CR below changes

If a CR below this one in the stack gets a new round after this CR started, or a CR joins batch-30
below it, the restack brings its new head. The Driver re-reads that CR's diff, re-checks the rows
of the inventory it touches (pictures included: the screenshot run is then taken again), and fixes
them in a new commit before it hands back.

## Open questions

None.

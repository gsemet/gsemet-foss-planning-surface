# Change Specification: the web board documented, with screenshots taken by a command

## Goal

The user's words (2026-11-13): "rajoute des pages de documentation et de captures automatique pour
remplir des documentation en markdown pour l'instant [...] il faudra 1 screenshot representative
dans le readme".

Once the web board server exists, a reader of `docs/` learns how the web board is launched and how
it works. Screenshots of the real server illustrate each view. One command, run by hand, retakes all
the screenshots from a fixed demo planning folder kept in the repository, at PC width and at phone
width, and they come out the same from one run to the next. The README shows one representative
screenshot: the web board with a batch running, in place of the pane's image. The CR also goes
through `docs/` and fills the gaps it finds, not only those about the web board.

## Where this CR stands

`depends.json`: after `visualization-backend`, `board-read-views`, `board-backlog-edit` and
`surface-autosync` (answer 2: the docs are written once the server exists, with screenshots of the
real server, not of the prototype). None of those four is specified yet. This specification names
what it needs from them (section "What this CR needs from the server") and does not invent their
shape: the Driver reads the server as merged on `main` when it starts. It describes that server, not
the prototype's simulations.

`cr-summaries` is not a dependency. If its display (the origin icon, the late-summary clock, the
labels and their filter) is merged when this CR starts, the demo data and the pages cover it. If it
is not merged, they leave it out, and the PR's Known gaps names what is left out.

The reference for what the views look like is the prototype of `visualization-backend`:
`.agents/changes/2-backlog/P2/visualization-backend/prototype/` (`index.html`, `README.md`) and its
screenshots `.../visualization-backend/evidence/prototype/v6-*`. The folder moves with that CR, so
the Driver looks for it by its slug, possibly under `5-archives/`. The prototype names the views.
The screenshots show what the server actually draws.

## Decisions carried from the grill (`02-answers.md`)

1. **The pages.** New pages in `docs/` explain how the web board's UI is launched and how it
   works. The existing docs stay, and the CR fills their gaps (decision 7).
2. **When.** After the four server CRs. The screenshots are of the real server.
3. **Retaking.** One command run by hand (a `just` recipe over a fixed demo), when the UI changes
   or before a release. It does not run at each release, it is not in CI, and it is not part of
   `just check`.
4. **The README's screenshot.** The web board with a batch running. It replaces
   `docs/board-mod-batch.png` in the README. That file stays in the repository and in
   `docs/boards.md`.
5. **Screens.** Each view is captured at PC width and at phone width, as in the final QA: 1400x860
   and 375x812, the sizes the prototype was checked at.
6. **Data.** A fixed demo planning folder kept in the repository. The screenshots are the same from
   one run to the next.
7. **Gaps in the existing docs.** In this CR too: the CR goes through `docs/` and fills the gaps it
   finds, beyond the web board.

## What changes

### 1. The demo planning folder (new, `docs/demo/`)

A fictional planning folder, checked in, that the server reads to draw every view the pages show.
It is in English and holds no real person, project or PR.

- **Shape.** It is a multi-project planning surface (`projects/<name>/` with `project.md`,
  `checkout.yml` and `changes/`, as `docs/planning-modes.md` describes), so that the project picker
  and "All projects" have something to show. It has two or three projects:
  - one project with a **batch running in stack mode**, whose CRs are in every state the views
    draw: merged, handed back `ready` (PRs to review, and drafts), working (rounds against the
    limit), blocked (with a reason), queued, and queued and waiting on a dependency (`after`). It
    has a cost against a budget, slots, and enough `events.jsonl` lines for the Home activity list;
  - one project with no batch running, an inbox, and last merged CRs in `5-archives/`;
  - optionally a third project, small, to make the "All projects" table worth reading.
- **Backlog content**, in the running project: inbox items, CRs in `2-backlog/P1` to `P4` with one
  priority row left empty (it draws as a thin strip), and `3-ready` holding both a specified CR and
  an automatable one. The CRs cover the grill states raw, in grill, specified and automatable. One
  CR folder has sub-folders (`intake/`, `evidence/` with an image, `work/`), so that the file panel
  shows a tree. Once `cr-summaries` is merged, the folder also has its condensed JSON (titles,
  summaries, origins: a GitHub issue, a Jira ticket, a verbal request; labels; a group; one late
  summary).
- **The record files** (`batch.json`, `events.jsonl`, `STATUS.json`, the STATUS files, and the
  seat if the server reads it) are written in the format that the server merged on `main` reads.
  Every timestamp in them is fixed.
- **PR links** point to a fictional forge URL (for example `https://github.com/example/shop-api/pull/12`).
  The screenshots never follow them.
- A short `docs/demo/README.md` says what the folder is for, says that only the capture command
  reads it, and says it is not a planning folder of this repository.
- chantier's own CLI must never take `docs/demo/` for this repository's planning folder. It sits
  outside `.agents/changes/` and holds no surface marker that the CLI discovers from the
  repository's root. The Driver checks this with `chantier preflight` run from the main checkout,
  read-only.

### 2. The capture command (new, `scripts/docs_screenshots.py` and `just docs-screenshots`)

- A new recipe in `justfile`, `docs-screenshots`, next to `mod`. Its comment says: "Retake the web
  board's screenshots in docs/ from docs/demo/ (by hand: when the UI changes, before a release; not
  in check)".
- The script lives under `scripts/`, like `scripts/version.py` and `scripts/mod.py`. It is a dev
  tool, not the CLI, so it may declare dependencies (a uv inline script). It does the following:
  1. Copies `docs/demo/` to a new temporary folder (initialised as a git repository if the server
     needs one). The board writes to the backlog, so a capture must never change the checked-in
     demo.
  2. Starts the real server with the repository's own CLI (`uv run --script
     skills/chantier/scripts/cli/chantier.py board ...`) on that copy, on loopback. It reads the
     URL that the server prints at start, random part included, and stops the server at the end
     and on any failure.
  3. Opens each view with a headless browser at 1400x860 and at 375x812, at a fixed time and in a
     fixed timezone and locale, with animations off. It waits for the view's data to be drawn
     before the shot.
  4. Writes PNG files to `docs/web-board/`, one per view and width, with fixed names:
     `<view>-pc.png` and `<view>-phone.png`.
  5. Prints the list of files it wrote. It stops with a clear message, and no partial
     substitute, when the browser or the server is missing or fails. This follows the "no
     fallback" rule of `AGENTS.md`.
- The screenshots to take, each at PC and phone width unless noted. The final names follow the
  views that the server ships:
  - **Home**, of the running project (the tiles, the batch's progress, open PRs, blocked CRs, the
    activity list, the pipeline, the last merged CRs, and the "written by the board" tile if the
    server has it);
  - **All projects** (the overview: the table on PC, the cards on the phone);
  - **the project picker**, open;
  - **Triage** (inbox, the P1 to P4 rows, `3-ready`, the grill-state post-its, a group; the label
    filter if it exists), plus one shot with a selection and its bottom bar (phone), the way to
    move a post-it on a phone;
  - **Kanban**;
  - **Batch** (the mode band, the dependency graph, PRs to review and drafts, merged PRs). This
    PC shot is also the README's image;
  - **Costs**;
  - **the CR's file panel**, open on the CR with sub-folders (Markdown rendered, the tree);
  - **"New"** (the dialog that files an idea in the inbox) and **the Markdown editor**, PC only;
  - **the autosync pill and its panel** (PC: the panel open; phone: the dot), if the demo can show
    a fixed autosync state (see "What this CR needs from the server").
- The script does not compare the shots with the prototype's. That comparison is the final QA's,
  ordered by the Chief of Staff (`visualization-backend/02-answers.md`, "Split into CRs").

### 3. The documentation pages

- **`docs/web-board.md`** (new): how the web board is launched and how it works. Its sections:
  - **Launch and access.** Who starts it (the session, as the server CRs decide). The
    `chantier board` command and its options. The URL with its random part, printed by the CLI and
    given in the chat. Reached on the local network only, with no tunnel. Any `chantier.yaml`
    `board:` keys that remain. When it stops.
  - **Projects.** The picker, and "All projects", which hides the project views. In-project
    planning (`.agents/changes/`) shows neither.
  - **One section per view**, each with its PC screenshot and, where the layout differs, its phone
    screenshot: Home, Triage, Kanban, Batch, Costs, the file panel.
  - **Editing the backlog.** What the board writes (files and folder moves in the inbox, P1 to P4
    and `3-ready`, through the CLI's role-free commands), the toast and the journal, and saying
    "rescan" to the Chief of Staff. The board never messages the Chief of Staff and never edits the
    batch. "The next batch is ready" is the user's marker.
  - **Summaries and labels**, if `cr-summaries` is merged: the origin icon and the late-summary
    clock.
  - **Autosync**: the pill, its colours, the panel, approving an incident. Without an autosync the
    board shows nothing about it.
  - **Retaking these pictures**: `just docs-screenshots`, run by hand, over `docs/demo/`.

  Every statement comes from the merged server and its CRs' specifications and answers, in the
  words that `visualization-backend/02-answers.md`, "Semantics fixed", set: the two kinds of
  "ready", "to review", the stack merged in one action from its top PR, the release at the top. If
  that page grows too long, the Driver may split the views into a second page,
  `docs/web-board-views.md`, linked from the first.
- **`docs/boards.md`**: the "Remote board" section describes today's read-only page, which "writes
  no file". If the server CRs have not already rewritten it, it becomes a short pointer to
  `docs/web-board.md`, without the facts that no longer hold. The intro line ("two read-only
  views") is corrected to match. The CR board section (the pane) and its images stay.
- **`README.md`**: the section "The CR board" (around line 162) shows `docs/web-board/batch-pc.png`
  in place of `docs/board-mod-batch.png`, under a caption that says it is the web board with a
  batch running. Its text names the web board beside the pane and links `docs/web-board.md`. The
  "More" list gains `docs/web-board.md`, and its "Boards" line is corrected if it no longer holds.
  This changes the README's image, not the pane, so the `AGENTS.md` rule about a real-session
  screenshot of the pane does not apply.

### 4. The pass over `docs/` (decision 7)

The Driver reads every page of `docs/` and the README against the code on `main` and fixes what
is wrong or missing. Each fix is listed in the PR body. Candidates already seen while writing this
specification, to be checked and not taken on trust:

- `docs/batch-pace.svg` is linked from no page of `docs/`, the README or `CONTRIBUTING.md`.
- `docs/release-process.md` is reached only from `CONTRIBUTING.md`, and the README's "More" list
  does not name it, nor `docs/planning-modes.md` or the use cases.
- Anything in `docs/` that still calls `chantier board` read-only, or says the board writes no
  file (for example `docs/agents-and-models.md` line 28, and `docs/boards.md`), once the server
  CRs have changed that.
- The `*-texts.md` files are the diagrams' text sources. They are not orphans, and are not linked
  on purpose.

The pass changes documentation only. A gap that needs a code or card change becomes an inbox
item that the Driver names in its hand-back, and is not fixed here.

## Out of scope

- Taking the screenshots in CI or at each release (decision 3).
- Any change to the server's views, behaviour or look, beyond what the next section requires to
  run it on the demo.
- A pixel comparison with the prototype (the final QA's job).
- The pane (`hooks/register.tsx`) and its images, other than replacing the README's one.
- The tutorial and the use-case pages get no new screenshots, though the pass may fix their text.
- Another language for the pages: the repository text is English.

## What this CR needs from the server

These are needs, not designs. If the server CRs already meet a need, this CR uses what they built.
If not, the Driver adds the smallest change to `chantier board` that meets it, keeps the CLI
dependency-free and portable, and the CR then passes `just scenario` (it touches the CLI). Each
such change is listed in the PR body.

1. **Run on a given planning folder.** The server can be started on a planning folder (or surface)
   named by path, not only the one found from the current directory. The other way to meet this is
   for the script to make the copy look like a project or surface the server discovers.
2. **A printed URL that can be read.** The server prints its URL, random part included, on start,
   in a form a script can parse. It also gives a way to pick the port (or to print the port it
   picked), so that two runs never clash with a board already running.
3. **A fixed instant.** Every age and clock time that the server computes ("3 min ago", the time
   since the batch opened, the steering session's last sign, the data's age, "you said so at
   HH:MM") is computed against an instant that the capture fixes. Otherwise two runs give
   different pictures. No such hook exists today: `state.now()` in
   `skills/chantier/scripts/cli/src/chantier/state.py` reads the system clock.
4. **Costs without transcripts.** On the demo, the costs view shows the recorded figures. It
   neither fails nor changes them when its 5-minute recompute finds no session transcripts.
5. **No side effect outside the copy.** On the demo copy the server writes nothing outside that
   copy, joins no real autosync group and pushes nothing.
6. **A fixed autosync state**, for the pill's screenshots. The demo must be able to show the pill
   in a given state (for example "waiting for an approval") with no real autosync running.

## Evidence

- `just check` passes on Linux, macOS and Windows. `test_skill_and_references_links_resolve`
  already checks that every link in `README.md` and `docs/*.md` resolves, the new images
  included. No new test is added: tests check structure only, and the capture needs a browser.
- `just docs-screenshots`, run twice in a row on the same machine, writes the same list of files.
  The second run leaves `git status` clean, or any pixel change it shows is explained in the PR.
  The PR body says on which system the pictures were taken.
- After a run, `git status` shows no change under `docs/demo/` and none in the planning folder of
  this repository.
- `chantier preflight` run from the main checkout does not see `docs/demo/`.
- The PR's Deliverables show the README's new image and the PC and phone screenshots of each
  view, with the head's SHA (seven characters). This lets the reviewer judge them beside the
  prototype's `v6-*`.
- If a server change was needed (previous section): `just scenario` passes.
- The PR body lists the gaps fixed by the pass over `docs/`, and any gap turned into an inbox item.
- The PR's Known gaps names any view that has no screenshot, with the reason (for example, no
  autosync state on the demo, or `cr-summaries` not merged).

## Open points (defaults taken; the Chief of Staff takes them to the user)

1. **The headless browser.** Default: Playwright for Python with Chromium, declared in the
   script's inline dependencies. Its first run downloads the browser. Another choice is a
   locally installed Chrome or Edge run with `--headless --screenshot`, with no dependency but a
   browser that must be present.
2. **"The same from one run to the next".** Default: the same pictures on the same machine. The
   platform's UI face (Segoe UI Variable on Windows, the system face elsewhere) makes pictures
   taken on another system differ. The pictures in the repository are taken on the maintainer's
   machine.
3. **Where the demo and the pictures live.** Default: `docs/demo/` and `docs/web-board/` (a
   sub-folder, where today's images sit directly in `docs/`).
4. **The server's needs 1 to 6** are met by this CR when the server CRs have not met them. Default:
   yes, as the smallest change, which makes this CR pass `just scenario`. The other option is to
   send them back to `visualization-backend` before this CR starts.
5. **The autosync pill.** Default: captured only if the demo can show a fixed state (need 6).
   Otherwise its section has no screenshot, and Known gaps says so.
6. **In-project mode** (no picker, no "All projects"). Default: described in the page, not
   captured.
7. **The README's image.** Default: the Batch view at PC width. Another choice is the Home view of
   a project with a batch running.
8. **The UI's language.** The prototype's labels are French ("Tous les projets", "Écrit : …").
   Default: the screenshots show whatever the server ships, and the pages, in English, quote its
   labels as shown.

## Decisions after the specification (they replace the open points they name)

Asked by the Chief of Staff, 2026-11-13 (in French, recorded in English).

- **The page's language: both.** English by default and French, from one word file per language, built so that more translations can be added later. The prototype's French labels are the French file. Where an open point above says English only or French only, this answer replaces it.
- The other open points stay at the specification's defaults.

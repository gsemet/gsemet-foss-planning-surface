# Change Specification: the board's reading views, as in the prototype

## Goal

The user's words (2026-11-13): "je veux la meme chose en fin d'implementation", and "juste assure
toi que le code soit hyper propre avec de beau standard et modularité pour facilite la
maintenance".

The page that `chantier board` serves shows the prototype's reading views, drawn from the live
record of the planning folder instead of a snapshot: Home, Kanban, Batch (the dependency graph,
the batch's mode, the PRs to review or still drafts, the merged PRs), Costs, a CR's file panel,
the project picker with "All projects" (which hides the views tied to one project), and the
phone layout with its bottom bar. These views only read: nothing on them writes a file, moves a
folder or sends anything to an agent.

The page is hand-written HTML, CSS and JavaScript, with no compiler and no bundler, in native ES
modules, one module per view. The code meets measured targets that `just check` enforces, as
the CLI's Python does since `python-inline-deps`.

This CR is CR 2 of the five split from `visualization-backend` (`visualization-backend/02-answers.md`,
"Split into CRs"). It has no `issue:` line.

## Where this CR stands

- **Runs after `visualization-backend`** (`depends.json`). That CR makes `chantier board` the
  server: its read JSON API over the record and the folders, one project or a multi-project
  surface, the URL with a random part on the local network, the live refresh, the costs
  recomputed at worst every 5 minutes. It was not specified when this specification was written.
  The Driver reads the server as merged on `main` when it starts. Section "What the views read"
  lists the facts the views need. Where the merged server lacks one, this CR adds it to the
  server's read data, as the smallest change (open point 2).
- **`python-inline-deps` runs before both.** Its package layout (`board/collect.py`,
  `board/server.py`, …) and its Python targets apply to any Python this CR touches.
- **Later CRs plug into the frame this CR builds:**
  - `board-backlog-edit` adds the Triage view, "+ New", the Markdown editor, the journal and
    the "next batch ready" marker. Its `depends.json` waits for this CR.
  - `cr-summaries` adds the origin icon, the late-summary clock, the labels and their filter.
  - `surface-autosync` adds the autosync pill and its panel.

  This CR leaves each of them one named place in the code ("Extension points") and draws none of
  their elements.
- **`board-docs-screenshots`** documents the result later, with its own capture command. This
  CR's comparison screenshots are PR evidence, not documentation.

## The reference

The prototype of `visualization-backend`:

- `prototype/index.html`, with `prototype/README.md` saying how to serve it and
  `prototype/snapshot.py` making its `data.js`;
- its screenshots `evidence/prototype/v6-*`.

The folder moves with that CR, so the Driver finds it by its slug: in `2-backlog/P2/` today,
under `5-archives/` once that CR is merged, or in git history if the archive was cleaned.

`index.html` as it stands is "the prototype as cleaned" (02-answers, last section of the
prototype work): it is exactly what the five CRs deliver. Where an earlier `v6` screenshot
differs from it, `index.html` wins. Two examples: `v6-15` still shows the "Vers le CoS" tile, and
`v6-04` still shows every view under "All projects".

### Views and screenshots this CR reproduces

| Prototype view (`index.html`) | Screenshots | Reproduced here | Left to |
| --- | --- | --- | --- |
| Project picker, PC (`pmenu`, sidebar `.ws`) | `v6-01-project-picker` | all of it, real projects only | — |
| Picker, phone (`.pbtn` above the title) | `v6-03-picker-phone` | all but the autosync dot beside it | `surface-autosync` (the dot) |
| An example project with no data | `v6-02-example-project` | not reproduced: the real board has no example projects (see "Project picker") | — |
| All projects, PC table and phone cards (`allProjects`) | `v6-16-all-projects-home-only-pc`, `v6-17-all-projects-home-only-phone` (they supersede `v6-04`, `v6-05`) | all of it | — |
| Home (`home`) | `v6-07-polish-home`, `v6-09-impeccable-home`, `v6-15-semantics-home-phone`, `v6-23-home-written-by-board` | all but the tile "Written by the board" and the declared state of "Next batch" | `board-backlog-edit` |
| Kanban (`kanban`, `kcard`) | `v6-10-impeccable-kanban`, `v6-13-semantics-kanban-pc`, `v6-22-kanban-labels-pc` | all but the label filter row, the labels, the origin icon, the late clock and "+ New" | `cr-summaries`, `board-backlog-edit` |
| Kanban on a phone | `v6-11-impeccable-phone` | all of it (one swiped column per screen) | — |
| Batch (`batch`, `modeBar`, `prCols`, `drawEdges`) | `v6-06-polish-batch`, `v6-12-semantics-batch-pc`, `v6-14-semantics-batch-phone` | all of it | — |
| Costs (`costs`) | none at v6 (`v2-04-costs` for the layout) | all of it | — |
| The CR's file panel (`openPanel`, `showFile`, `md`) | `v3-06-this-cr-folder` (layout, still current in v6) | all of it, reading only | `board-backlog-edit` (editing) |
| Phone layout: bottom bar, panel full screen | `v6-08-polish-phone`, `v6-11-impeccable-phone`, `v6-14`, `v6-15` | all of it | — |
| Triage (`triage`, post-its, groups, labels) | `v6-19`, `v6-24` | nothing | `board-backlog-edit` |
| Autosync pill and panel (`asPaint`) | `v6-20`, `v6-21` | nothing | `surface-autosync` |
| Origin icon, late clock (`srcTag`, `lateTag`) | `v6-18` | nothing | `cr-summaries` |

## Decisions carried from the answers

Every decision of `visualization-backend/02-answers.md` that bears on the reading views, and
where this specification carries it. The decisions that belong to the other four CRs are named
under "Out of scope".

| Decision (02-answers) | Where |
| --- | --- |
| Read a CR's Markdown files; a CR is a folder whose files are not known in advance, listed as they are (feedback on prototype 1) | "The file panel" |
| Follow the progress as a kanban (first list of actions) | "Kanban" |
| Costs followed with no extra agent turn; on demand, else the last cost with its age (live costs answer); recomputed at worst every 5 minutes (scope answer 5) | "Costs" |
| The SaaS look: sidebar, header counters, columns with a count and a coloured dot, cards (visual reference) | "The shell", "Visual rules" |
| Sliding right panel; the folder as a tree, the specification first, Markdown rendered, JSON pretty-printed, images shown (prototypes 1 and 2) | "The file panel" |
| The test case for the UI is `visualization-backend`'s own folder; one level of sub-folder headings, a deeper path under its first folder (everything in the CR's folder) | "The file panel", evidence E5 |
| The grill state shown by colour and icon: raw, in grill, specified, automatable (feedback on prototype 2, automatable) | "Home" (the pipeline); the post-its are Triage's |
| Home and its content (prototype 4) | "Home" |
| Batch view: the mode; ready and merged CRs stay in the graph; PRs to review in stack or merge order; merged PRs; one click opens the PR (batch view, prototype 5) | "Batch" |
| Card style: no thick coloured left border; a tinted 1px border and a very light pastel fill; the state colours (card style) | "Visual rules" |
| Several projects: the picker at the top left, each view shows that project only; on a phone above the title (several projects) | "Project picker" |
| All projects: one line per project, a click opens it, a view chosen from there goes back to the last project (all projects) | "All projects" |
| The visual rules and the Impeccable pass (contrast, sizes, no nested cards, edge or shadow, headings, sentence case, drawn icons, platform face, tabular figures, themed browser surfaces) | "Visual rules" |
| Board to Chief of Staff later; nothing queued to it (board to Chief of Staff: later; the prototype as cleaned) | "Out of scope"; no "Vers le CoS" tile |
| Semantics fixed: two kinds of "ready", to review, the stack, a PR's base, waiting, events, rounds | "Semantics", one module |
| The overview hides the project views and "+ New" (the overview hides the project views) | "All projects", "The shell" |
| In-project planning: no project choice and no "All projects" (scope answer 4) | "Project picker" |
| Editing is the backlog only; the board does not edit the batch (editing is the backlog only) | "Bounds": these views write nothing |
| The prototype is the reference; the specification names the views and screenshots; the PR shows each view beside the prototype's; a final QA on PC and on the phone (split into CRs) | "The reference", "Final QA" |
| HTML, CSS and JS with no compiler or bundler, native ES modules, one per view; very clean, standard, modular code (technology) | "Code layout", "Targets" |
| Playwright through a uv script for screenshots (technology) | "Final QA" (the comparison shots; the repository's capture tool is `board-docs-screenshots`'s) |
| The python-inline-deps targets; "the board CRs add the JS and CSS targets with their linter" (its spec, decision 8) | "Targets", "`just check`" |

## Bounds

- **Reading only.** No view of this CR sends a request that changes a file, a folder, the record
  or an agent. The only non-read request is the Costs view's "Recompute", and only if the server
  offers one (see "Costs").
- **No change to `STATUS.json` or `hooks/register.tsx`.** A fact the views need that the server
  lacks is added to the board's own read data, not to the `STATUS.json` schema, so the pane draws
  the same thing and the `AGENTS.md` screenshot rule is not triggered. If the Driver finds that a
  `STATUS.json` field must change, it stops and says so.
- **No card, agent or `AGENTS.md` change.** The server CR already rewrote the board's rules.

## The shell

`static/index.html` holds the page's frame and nothing else: the sidebar, the main column with
its header (the title `h1`, the stats line, an empty actions place), the view container, the
phone's bottom bar, and the panel. It loads the stylesheets with `<link>` tags and one script,
`<script type="module" src="js/main.js">`. It holds no inline script, no inline style, no `on…=`
attribute and nothing loaded from another origin.

The prototype's `.proto` banner ("Prototype 6 : instantané…") and the sidebar's "Prototype :
lecture d'un instantané" line are not reproduced: the real board reads live.

- **Sidebar (PC):**
  - the project block at the top (see "Project picker");
  - "Views", then one button per registered view: Home, Kanban, Batch, Costs, each with its drawn
    icon and its count. The counts are:
    - Kanban: the backlog items plus the batch's CRs not merged;
    - Batch: the batch's id;
    - Costs: the spend.
  - At the foot: "Data: N min ago", the age of the page's last successful read. When the server
    stops answering, the foot says "Board unreachable: data N min ago" (open point 9).
  - Below the foot, the empty place for the autosync pill.
- **Header:** the `h1` is the view's name. The stats line is:
  - for a project: "N intake · N in grill · batch-NN running · N working · N handed back ·
    $spent / $budget";
  - on "All projects": "N projects · N batches running · N PRs to review · N CRs working · N
    intake".
- **Phone (at most 760px wide, as in the prototype):**
  - the sidebar is hidden;
  - the project button sits above the title;
  - a fixed bottom bar holds the same view buttons, with icon and label;
  - the main column keeps room for the bar.
- **Navigation:**
  - The URL carries the project and the view as in the prototype (`?p=<project>&v=<view>`,
    `p=*` for "All projects"), so a reload or a link from the chat opens the same place.
  - Back and forward follow the history.
  - Every URL the page builds is relative to the page's own address, so the random part of the
    board's URL is kept on every request.
  - The project chosen is kept in the browser (`localStorage`), with the last real project, as
    the prototype does.
- **Live refresh:**
  - The page follows the server's live refresh, whatever form `visualization-backend` gave it.
  - On new data it redraws the current view in place. It keeps the open panel, the open file,
    the scroll positions and the keyboard focus.
  - It does not redraw when the data did not change.
- **Keyboard:**
  - Escape closes the panel and any open menu.
  - Every clickable card, row and node is reachable with Tab and opens with Enter.
  - The focus ring is the prototype's.

## Project picker

- **The picker's content:**
  - A surface with several projects: the sidebar's top block is the current project's mark (a
    coloured square with its initial, the colour computed from the name) and its name, with a
    chevron.
  - A click opens the menu:
    - its head is "Planning surface · N projects";
    - then "All projects" ("overview · N PRs to review");
    - then a rule;
    - then one line per project: its mark, its name, a blue dot when its batch runs, and
      "batch-NN · <state> · N in intake" (or "no batch").
  - The current line carries a check mark. A click outside closes the menu.
- **In-project planning** (`.agents/changes/` in the project, or a surface with one project): no
  menu and no "All projects". The top block shows the project's mark and name only.
- **A project steered on another machine:** its `batch.json` and STATUS files are on that
  machine. The board shows its backlog as last pulled, and "no batch" where a batch would show.
  The board pulls nothing.
- **No example projects.** The prototype's `exemple-web` and `exemple-api`, and the screen that
  says the prototype holds no data for them (`v6-02`), are not reproduced. Every project the
  board lists is a real project of the surface.

## All projects

This is the overview home. On it, only Home stays in the sidebar and the bottom bar. Kanban,
Batch and Costs are hidden, and so is the header's actions place (where "+ New" will go).
Choosing a view from there opens it on the last real project. The project counts of the sidebar
are hidden.

- **PC: a table**, one row per project. The columns are:
  - Project: the mark, the name, and the dot when a batch runs;
  - Batch: "batch-NN · <state>", with the mode under it;
  - Working: the count, then in red the number blocked when there are any;
  - PRs to review: one green link per PR to review, "CR-NNN ↗", opening the PR in a new tab;
  - Progress: a meter of the merged CRs out of the batch's, with "N/M merged";
  - Spent: the spend, with "/ budget" under it;
  - "Intake · grill": two counts;
  - Data: an age (open point 7).

  A click on a row opens that project's Home. A click on a PR link opens the PR only.
- **Phone: one card per project.** The card is tinted green when a PR waits for review, blue when
  a batch runs, grey otherwise. It shows the mark, the name, the dot and the batch, then "N PRs
  to review · N working · $spent · N intake".
- Under the table: "One line per project of the surface. A click opens the project; a CR link
  opens the PR to review."

## Home

The grid of the prototype: 12 columns on PC, 2 on a phone. It is drawn by the Home module from
the project's data.

1. **The tiles of what waits** (one row). Each tile is a link to its view.
   - "To review": the count of the PRs to review ("Semantics"). Its line is "PRs ready to merge",
     or "N handed back, no PR to merge". Tinted green when not zero.
   - "Waiting for you": the blocked CRs plus the unread asks. Its line is "N blocked, N
     questions". Tinted red when not zero (open point 5).
   - "Next batch": the count of `3-ready`, with "in preparation (3-ready)".

   The "Written by the board" tile and the declared state of "Next batch" ("declared ready by
   you") are `board-backlog-edit`'s. The tile row is a list that a later module extends. It lays
   out any number of tiles evenly, so the fourth tile lands with no change to Home's layout.
2. **The running batch** (7 columns). Its heading holds:
   - "batch-NN", the state tag, "mode · steering" (direct or Foreman), and "see the batch →".

   Under it:
   - a progress bar by state: merged, handed back, working, blocked, queued, with its legend and
     counts;
   - four figures:
     - Spent / budget, with a meter;
     - Slots taken/total;
     - "Last sign of the Foreman" or "… of the Chief of Staff", from the heartbeat. It is amber
       past 15 minutes, and "stopped" when the heartbeat is stopped (open point 6);
     - "Opened N h ago", from the batch's creation.

   With no batch: "The next batch opens on your go."
3. **Open PRs** (5 columns): the CRs with a PR that are not merged. Each row has its state tag,
   the CR, the title and "#N". A click opens the panel. Under it, when there are any, "Blocked":
   each blocked CR with its reason.
4. **Recent activity** (7 columns): the last 25 events, newest first. Each row has its local
   time `HH:MM`, its icon and its text, as the prototype's `evText` maps them:
   - open, add, take, round;
   - gate passed or failed, with its command;
   - verdict;
   - ship, with "#N";
   - handback, with its `result`;
   - ask;
   - an `order` of kind `merged` shown as "merged";
   - another order, with its kind and note;
   - note.
5. **Pipeline** (5 columns): Inbox, P1, P2, P3, P4 and `3-ready`, one bar each, scaled on the
   whole backlog. Each bar is split by grill state:
   - specified, green;
   - in grill, amber;
   - raw, grey;
   - automatable, violet: a `3-ready` item with no specification.

   It has a legend. The link "sort →" to Triage shows only once a Triage view is registered.
   Under it, "Last merged" (4 rows: CR, title, date) and "N in total".

## Kanban

Five columns, each with a coloured dot, its name, its count, and a line under the name:

| Column | Holds | Line under the name |
| --- | --- | --- |
| Intake (grey) | `1-inbox` items | "1-inbox: filed, not triaged yet" |
| Grill (amber) | `2-backlog` items, P1 first | "2-backlog: prioritised, being grilled" |
| `3-ready` (violet) | `3-ready` items, keyed by the record's own value `3-ready` | "waits for the next batch (not "ready to merge")" |
| In progress (blue) | the batch's queued, working and blocked CRs, blocked first, then working, then queued | "batch-NN: queued, working, blocked" (or "no batch") |
| Handed back (green) | the CRs handed back `ready` | "handback ready: to review when the PR is on <default branch> or the stack verified" |

Above the columns, on the right: "N items · N merged". The left of that row is the empty place
of the label filter. The Intake column has no "+ New" button: that button is
`board-backlog-edit`'s.

The cards:

- **A backlog card:**
  - its priority tag (Inbox, P1…P4, `3-ready`), its slug, and the empty place for the origin and
    late icons;
  - the title, and the empty place for the labels;
  - a two-line description (open point 3);
  - "N files", and "specified" or "to grill".
- **A batch CR's card:**
  - the CR tag, the state tag (with "waits" for a queued CR held by its dependencies), the slug,
    and the place for the origin icon;
  - the title and the description;
  - one bar per round, against the CR's own limit, else the batch's `max_rounds`, filled in the
    state's colour;
  - "round r/limit", "N files", "N deps." when it has open dependencies, and the cost.

A click on a card opens the panel; the open card shows as selected. On a phone the columns are
swiped one per screen (86% wide, snapping).

## Batch

1. **Five figures:**
   - Batch: the id, then "state · mode · steering";
   - Slots: taken/total, then "N queued";
   - Working: the count, then "N blocked";
   - "Handed back ready": the count, then "N to review · N merged";
   - Spent: with its meter, then "of $budget".

   On a phone, two columns, and the fifth figure is hidden, as in the prototype.
2. **The mode band:** the current mode's pill (Stack, Series, Parallel), its sentence, and the
   three modes with the current one lit (hidden on a phone). The sentences say what chantier
   means ("Semantics"):
   - Stack: "each PR sits on the previous one, the release on top; once the stack is verified on
     the forge, you merge it in one action from its top PR."
   - Series: "one CR after the other: the next starts from the previous one's branch, its PR
     stays a draft until the previous one merges; the release last."
   - Parallel: "each PR starts from the default branch, or from its open dependency: you merge
     them in the order they became ready, the release after the others."
3. **The dependency graph** (left):
   - The CRs are set in levels by `after`: "No dependency", then "Level i: after level i−1".
   - In each level they are grouped by state, in the order blocked, working, handed back, waits,
     queued, merged. Each group has a dashed frame, a dot, "<state> · N".
   - Each node shows its CR tag, slug, title, "r<round>/<limit>", its open-dependency count, "PR"
     when it has one, and its cost.
   - Under the graph: a legend ("an arrow goes from a CR to the one that waits for it") and the
     note "Hover a CR to see what it waits for and what waits for it; click to open its folder."
   - The arrows are drawn in an SVG layer, from a dependency to the CR that waits for it, and
     redrawn on resize.
   - Hovering a node lights it, its dependencies, its dependants and their arrows, and dims the
     rest. A click opens the panel.
   - The handed back and merged CRs stay in the graph where they are.
4. **Two PR columns** (right, 560px on PC; first on a phone, the graph under them):
   - **PRs to review:**
     - Its hint depends on the mode and on whether the stack is verified (the prototype's three
       hints, in English), ending "One click opens the PR."
     - Then the PRs to review, in order. A stack reads from its top PR: the numbers are places in
       the stack, "top · N" on the highest, with a dashed rail. A series or a parallel batch shows
       the recommended merge order.
     - Then "Drafts, not to review yet · N", greyed, in the same order. Each says why: "handed
       back, draft PR", or its state.
     - Each PR card shows:
       - "#N", the CR tag, "release" or "fix" when it is one, and its place;
       - the title;
       - its base ("Semantics");
       - its cost;
       - a folder button that opens the panel.

       A click anywhere else on the card opens the PR in a new tab. Only an `http(s)` URL is a
       link.
   - **Merged PRs:**
     - "For information.";
     - this batch's merged PRs, latest first, each "merged N ago";
     - then "Earlier batches": the last 4 merged PRs of earlier batches, with their batch.

With no batch: "No batch running."

## Costs

- **The age line:** "Last computed: N min ago", then a "↻ Recompute" button, then "the server
  reads the transcripts again: no agent turn".
  - The age is the server's last cost computation.
  - The button asks the server to recompute, and shows "recomputing…" disabled until the new
    figure arrives.
  - It is drawn only if the merged server offers an on-demand recompute. Otherwise the line shows
    the age alone, with the server's 5-minute rule (open point 4).
- **Four figures:**
  - Spent (batch-NN), with its meter;
  - Budget, with "N % used";
  - "Sum of the CRs", with "the rest: steering";
  - "Average cost per active CR", with "N CRs with a cost".

  With no budget, the meter and the percentage show "—".
- **"Per CR, batch-NN":** a table with CR and slug, title, state tag and round, cost, and a
  horizontal bar scaled on the highest cost. It is sorted by cost, highest first. A click on a
  row opens the panel.
- **"Last merged CRs":** a table with CR, title, batch, cost, and a green bar.
- **On a phone** the title and bar columns are hidden.

With no batch: "No batch running."

## The file panel

The panel slides in from the right on PC (at most 680px wide, rounded, shadowed). On a phone it
covers the whole screen, with the tree above the file (150px high at most).

- **Head:**
  - A close button.
  - A row of facts:
    - for a batch CR: its CR tag, state tag, "round r/limit", cost, and "after N CRs" when it
      has open dependencies;
    - for a backlog item: its priority tag, its slug, and "specified" or "to grill".
  - The title as `h2`.
  - The folder's path and "N files", in a monospace face.
- **The tree:**
  - the folder's own files first;
  - then one heading per first-level sub-folder ("intake/ · N"), with its files under it;
  - a deeper file sits under its first-level heading, with the rest of its path as its name
    (for example `prototype/v1.html` under `evidence/`);
  - each file has an icon (text, image, other) and its size.

  The listing is the folder as it is: no fixed set of names. An empty folder says "empty
  folder".
- **The file first opened:** `03-change-spec.md`, else `01-intent.md`, else `STATUS.md`, else the
  first Markdown file, else the first file.
- **The file view:**
  - A line "<folder>/<path> · size", with "· cut" when the server cut a long text.
  - Then, by kind:
    - Markdown rendered by the panel's small renderer: headings, paragraphs, lists, tables,
      fenced code, inline code, bold. A link shows underlined and does not navigate, as in the
      prototype.
    - JSON pretty-printed.
    - Images shown, as images the server serves from the folder.
    - Other text in a `pre` block.
    - Any other file listed with its kind and size, and a download link if the server offers one.
  - A file is fetched when it is opened, not with the view.
- **Safety:** every text from a file or a record is escaped before it is drawn, in the panel and
  everywhere else. An SVG or HTML file in a CR's folder is shown as text or offered as a
  download; it never runs as a document. The server's content types and policy carry this; the
  page never builds a `data:` or `blob:` document from a file.

The editing of a file is `board-backlog-edit`'s. The panel's head leaves it one empty actions
place.

## Semantics

All the chantier meanings the views show live in one module, `js/model/semantics.js`. It is
pure: no DOM, no fetch. Every view reads them from there and nothing else. They follow 02-answers,
"Semantics fixed", as `index.html` implements them:

- **Two kinds of "ready".** `3-ready` is the backlog folder that waits for the next batch, keyed
  by the record's value `3-ready`. A CR handed back `ready` is "handed back", and its column is
  "Handed back".
- **To review.** A PR is "to review" only when its CR is handed back `ready` and either:
  - its base is the default branch; or
  - in a stack (a fix apart), the stack is verified on the forge.

  Any other PR is a draft ("handed back, draft PR"). The stack-verified fact is read from the
  server's data. While the server has none, a stack's PRs stay drafts, as the prototype does.
- **The chain:** the batch's open CRs other than a fix, by `order`, with the release on top. A
  stack is merged in one action from its top PR. Its list reads from the top, and its numbers are
  places, not a merge order. The release is the top of the stack or the series; only a fix CR is
  "on <default branch>, outside the stack".
- **A PR's base:**
  - a fix: the default branch;
  - a stacked CR in a stack: the CR under it, else "<default branch>, bottom of the stack";
  - in a series: the previous CR, with "draft until it merges";
  - else its last open dependency in `after`, else the default branch.

  In a stack, a CR not yet stacked adds "· not stacked yet". The default branch comes from the
  batch's settings, else `main`.
- **Merge order:** for a stack or a series, the chain, a fix apart. For a parallel batch, the
  order the CRs were handed back `ready`, with the release last (open point 8).
- **Waits:** a queued CR held by its dependencies (`waits`) shows "waits", in orange.
- **Events:** a hand-back's word is its `result`. A merge is an `order` event whose `order_kind`
  is `merged`.
- **Rounds:** shown against the CR's own limit, else the batch's `max_rounds`, else the round
  alone. Never a fixed "/3".
- **Levels:** a CR's level is one more than the highest level of its dependencies inside the
  batch. A cycle counts as level 0, as in the prototype's `levels()`.
- **Merged time:** `merged_at` when the record has it, else `updated`.

## What the views read

These are the facts the views need, as needs and not as an API design. The Driver maps them onto
the server merged on `main`. Where one is missing, it adds it to the server's read data
(`board/collect.py` or its successor), from the record only: `batch.json`, `events.jsonl`, the
seat, the stage folders, and the CR folders. It does not add it to `STATUS.json`.

- **The planning mode and the projects:**
  - in-project or surface;
  - per project: its name, and whether it is steered on this machine (its `batch.json` is here).
- **Per project, the batch** (or none):
  - id, state, mode, steering;
  - `created`;
  - default branch and `max_rounds` from the settings;
  - slots taken and total;
  - `spent_usd`, `budget_usd`, `unpriced`, `asks_unread`;
  - `heartbeat`, `heartbeat_stopped`;
  - the stack-verified fact, if the server can read it;
  - the time of the last cost computation;
  - the last events, at least 40, with:
    - `t`, `actor`, `kind`, `cr`;
    - `result`, `pr`, `note`, `order_kind`, `reason`, `command`, `round`.
- **Per CR of the batch, merged ones included:**
  - `cr`, `title`, `state`;
  - `round`, and its own round limit;
  - `cost_usd`, `pr`, `waits`;
  - the blocked reason;
  - `kind` (release, fix);
  - `updated`, `merged_at`;
  - the time it was last handed back `ready`;
  - `folder`, `order`, `stacked`, `branch`;
  - `after`, its open dependencies;
  - the number of files in its folder;
  - a description (open point 3).
- **Per backlog item:**
  - priority (`inbox`, `P1`…`P4`, `3-ready`);
  - slug, title, folder;
  - whether it has `03-change-spec.md` and `02-answers.md`;
  - its number of files;
  - its description.
- **Merged CRs:** the last ones, at least 8, with `cr`, `title`, `batch`, `pr`, `cost_usd`,
  `when`, and the total count.
- **A folder:** its listing (path, size, kind: text, image or other, and cut). Then one file's
  content on demand: text, an image with its type, or a download.
- **Costs:** the on-demand recompute, if the server has one.

The titles are shown without the "Change Specification: " or "Intent: " prefix, as `board.py`'s
`subject()` strips it today.

## Code layout

Everything lives under the board's package, in `skills/chantier/scripts/cli/src/chantier/board/static/`,
so it ships with the plugin and the server serves it as files. If `visualization-backend` already
created that folder or a first page, this CR builds on it. If the server still renders an HTML
page of its own (today's `render.py`), `GET /` serves `static/index.html` instead, and the
server-side renderer is removed (open point 11).

```text
static/
├── index.html              the frame only (see "The shell")
├── css/
│   ├── tokens.css          palette, state tints, type, sizes: custom properties only
│   ├── base.css            reset, type, focus, selection, scrollbars, links
│   ├── components.css      tags, dots, buttons, cards, KPIs, meters, tables, empty states
│   ├── shell.css           sidebar, header, picker menu, bottom bar
│   ├── panel.css           the file panel and the rendered document
│   └── views/              home.css, kanban.css, batch.css, costs.css, overview.css
└── js/
    ├── main.js             boot: reads the URL, starts the store, mounts the shell
    ├── core/
    │   ├── api.js          the only module that calls fetch: one function per read
    │   ├── store.js        the current project, view, data; subscribe and notify; live refresh
    │   ├── router.js       the URL ↔ project and view; history
    │   ├── dom.js          the escaping `html` tagged template, query and event delegation helpers
    │   └── format.js       money, sizes, ages, local times, PR numbers, slugs, titles
    ├── model/
    │   ├── semantics.js    the meanings of "Semantics", pure functions
    │   ├── grill.js        a backlog item's grill state
    │   ├── events.js       an event to its icon, tone and text
    │   └── words.js        every word the page shows, in one place
    ├── ui/
    │   ├── icons.js        the drawn SVG icon set
    │   ├── parts.js        shared pieces: tags, state tags, meters, KPI, empty state
    │   ├── sidebar.js
    │   ├── picker.js
    │   ├── bottombar.js
    │   └── header.js
    ├── views/
    │   ├── registry.js     the list of views: id, label, icon, scope (project, overview), module
    │   ├── home.js
    │   ├── overview.js     All projects
    │   ├── kanban.js
    │   ├── batch.js
    │   ├── batch-graph.js  levels, nodes, arrows, hover
    │   ├── batch-prs.js    the two PR columns
    │   └── costs.js
    └── panel/
        ├── panel.js        open, close, head, file view
        ├── tree.js         the folder's listing as a tree
        └── markdown.js     the small renderer, escaping everything
```

The Driver may split a module further to meet the targets, but may not merge two.

- **The views' contract.** A view module exports:
  - `render(state)`, which returns the view's markup from the `html` template;
  - an optional `mount(root, state)`, which binds its events by delegation on `root` and returns
    a cleanup function.

  A view reads facts through `model/` and words through `words.js`. It never fetches; only
  `api.js` does. A view knows no other view; it links to one by its id, through the router.
- **Markup.** All markup goes through `dom.js`'s `html` tag, which escapes every interpolated
  value unless that value is itself the result of `html`. No markup string is concatenated by
  hand. No `style="…"` attribute is written. A computed width or colour (a meter, a bar, a
  project's mark) is set through a CSS custom property with `element.style.setProperty`. No
  `on…=` attribute is written.
- **State.** `store.js` holds the one source of the page's state. The URL and `localStorage` are
  written by `router.js` and `store.js` only.
- **CSS.**
  - Every colour, radius and size that repeats is a custom property of `tokens.css`. The state
    tints (border and fill per state) are defined once and used by cards, nodes and PR cards.
  - A view's rules are in its own file, scoped by the view's root class.
  - The phone rules sit in each file's own `@media (max-width: 760px)` block.
  - No `!important`, and no id selector.
- **Words.** The page's text is in English (open point 1). The prototype's French words become
  these, in `words.js`:

  | Prototype | Page |
  | --- | --- |
  | rendu / Rendus | handed back / Handed back |
  | à revoir / PR à revoir | to review / PRs to review |
  | rendu, PR brouillon | handed back, draft PR |
  | attend, en file, en cours, bloqué, mergé, annulé | waits, queued, working, blocked, merged, cancelled |
  | sur main, hors stack | on main, outside the stack |
  | pas encore empilée | not stacked yet |
  | T'attendent, Batch suivant | Waiting for you, Next batch |
  | Dernier signe du Foreman / CoS, Ouvert | Last sign of the Foreman / Chief of Staff, Opened |
  | Activité récente, Derniers mergés, PR ouvertes, Bloqués | Recent activity, Last merged, Open PRs, Blocked |
  | Tous les projets, vue d'ensemble, Surface de planification | All projects, overview, Planning surface |
  | Coûts, Dernier calcul, Recalculer, Somme des CRs, le reste : le steering | Costs, Last computed, Recompute, Sum of the CRs, the rest: steering |
  | Sans dépendance, Niveau i : après le niveau i−1 | No dependency, Level i: after level i−1 |
  | brut, en grill, spécifié, automatable, à griller | raw, in grill, specified, automatable, to grill |
  | Données : il y a | Data: … ago |

  Labels are in sentence case. No title holds an em dash.

### Extension points

These are the named places the later CRs fill, each one entry and one module:

- `views/registry.js`: a new view (`board-backlog-edit`'s Triage) is one entry. The sidebar, the
  bottom bar, the router, the overview's hiding rule and the links to that view ("sort →")
  follow from the entry.
- The header's actions place: "+ New".
- The panel head's actions place: the editor.
- The sidebar's foot place, and the phone's place beside the picker: the autosync pill and its
  dot.
- On the Kanban cards: the badges place (origin icon, late clock) and the labels place. Above the
  Kanban: the filter place.
- Home's tile list: "Written by the board", and the declared state of "Next batch".

Each place is empty in this CR, and draws nothing.

## Visual rules

They are taken as `index.html` sets them, the tokens copied from its `:root`.

- **Palette:**
  - ink `#16181d`, `#454a58`, `#666b78`;
  - lines `#e6e7ea`, `#eeeff1`;
  - blue `#3b6fe0`, green `#2fa86b`, red `#d6455d`, amber `#d98a1c`, violet `#8b5cf6`, grey
    `#9aa0ab`.
- **Face:** the platform's UI face ("Segoe UI Variable Text", "Segoe UI", system-ui,
  -apple-system, …), with tabular figures.
- **State tints:** a tinted 1px border and a very light pastel fill, never a thick coloured left
  border on a rounded card:
  - working blue;
  - blocked red;
  - handed back green;
  - merged violet;
  - queued grey;
  - waits orange.
- **Contrast:** WCAG AA on white.
- **Sizes:** no interface text under 12px, except the badges at 11px.
- **Surfaces:**
  - no nested cards: the page is the surface, and the sidebar is a column with a rule;
  - a card has an edge or a shadow, never both: hover darkens the edge;
  - popovers have a shadow with a faint ring.
- **Headings:** in order, `h1` then `h2` then `h3`.
- **Icons:** the drawn SVG icons of the prototype's `IC` set, never Unicode glyphs, for
  navigation, files, folder, dependency, external link and chevrons. The activity feed keeps the
  prototype's glyphs.
- **Browser surfaces:** text selection, the focus ring, thin scrollbars and link underlines are
  themed as in the prototype.

## Targets

These apply to every file under `static/`, measured by `just check`. They mirror the Python
targets of `python-inline-deps`.

- **JavaScript:**
  - ES modules only (`type="module"`), no global variable, no dependency, no build step;
  - at most 400 lines per file;
  - at most 50 lines per function;
  - cyclomatic complexity at most 10;
  - at most 5 parameters;
  - nesting at most 3 levels;
  - `eqeqeq`, no unused variable, no undeclared global;
  - formatted by the formatter, with lines of at most 100 characters.
- **CSS:**
  - at most 400 lines per file;
  - nesting at most 3 levels;
  - no `!important`, no id selector;
  - colours through the tokens outside `tokens.css`;
  - formatted.
- **HTML:**
  - no inline script, no inline style, no `on…=` attribute;
  - nothing loaded from another origin.
- **Python:** any Python this CR adds or changes on the server side meets `python-inline-deps`'s
  targets.

## `just check` and the tools

- **The linters.** The `lint` recipe of the `justfile` (added by `python-inline-deps`) gains:
  - the JavaScript linter, with the rules above;
  - the CSS linter;
  - the formatter's check over `static/`.

  Each tool's version is pinned once in a `justfile` variable. Their configuration lives beside
  the static files, or in the CLI folder, and is excluded from the plugin's runtime.
- **The tools themselves.** The default is ESLint (flat config, core rules only), Stylelint and
  Prettier. They are run through Node.js taken from PyPI (`nodejs-wheel-binaries`) under `uvx`,
  so that `uv`, `just` and `git` stay the only tools a contributor installs (open point 10). The
  Driver measures this cold on Windows. If no such tool runs through `uv` on the three systems,
  the Driver stops and says so: no look-alike check and no hand-written substitute (`AGENTS.md`,
  "No fallback").
- **One structure test**, in `tests/test_code_targets.py` (the file `python-inline-deps`
  created), or as one more test beside its two. It checks:
  - every `<link>`, `<script>` and relative `import` of `static/` resolves to a file inside
    `static/`;
  - no static file loads from another origin;
  - `index.html` holds no inline script, inline style or `on…=` attribute;
  - every `static/` file is at most 400 lines.

  A failure names the file.
- **`CONTRIBUTING.md`, "Code standards"** (the section `python-inline-deps` wrote) gains the JS
  and CSS targets, the module layout of "Code layout" (core, model, ui, views, panel), the views'
  contract, the `html` escaping rule, and the lint tools.

## CI

`.github/workflows/ci.yml` does not change. Its `check` job runs `just check`, now with the JS and
CSS lint, on:

- `ubuntu-latest`;
- `macos-15-intel` (named `macos-latest`, `continue-on-error`);
- `windows-latest`.

Each runner has `astral-sh/setup-uv` with an empty cache at each run, the network, and no
`claude`. The runners also ship their own Node.js; the recipe does not use it, so that CI runs
what a contributor runs.

Compared with the local machine, a runner has no warm uv cache, no npm cache, and no lint tools
downloaded. Evidence E9 takes the cold-cache proof before the push. Only the first CI run can
prove:

- the Node.js wheel on Linux x86_64 and macOS Intel;
- the cold fetch of the lint tools on each runner.

## Out of scope

- The server, its API, its URL and its live mechanism: `visualization-backend`. Here, only the
  facts of "What the views read" that it lacks.
- The Triage view, "+ New", editing a Markdown file, moves, groups, labels' writes, the journal
  and its Home tile, the "next batch ready" marker: `board-backlog-edit`.
- The origin icon, the late-summary clock, the labels and their filter, the summaries:
  `cr-summaries`. Until they land, a card shows its description.
- The autosync pill, its panel and its phone dot: `surface-autosync`.
- Any message to the Chief of Staff, the queue, asks and chat, a "refresh summary" button:
  "Board to Chief of Staff: later" and the cleaned prototype.
- Any batch edit (`order` of any kind): "Editing is the backlog only".
- **A batch history view.** `batch-history` makes `5-archives/batches/batch-NN.json` for "the UI
  to show the history (the board CRs)", but:
  - the prototype has no history view;
  - this CR's request is "the prototype's reading views as they are";
  - `batch-history` is not a dependency of this CR.

  The Batch view's "Earlier batches" and the "Last merged" lists read the merged CRs the server
  already gives. A history view is a later CR, after `batch-history` and this one, with its own
  prototype step. The registry makes it one view module and one entry (open point 12).
- The docs' pages and their capture command: `board-docs-screenshots`.
- The pane (`hooks/register.tsx`), `STATUS.json`, the cards, the agents, `AGENTS.md`.
- A version bump.

## Evidence

The Verifier keeps each item in `work/verifier/evidence/`, and the PR body quotes them.

- **E1.** `just check` passes on the Windows machine, then in CI on Linux, macOS and Windows.
  Its output shows 0 findings from the JS and CSS linters and the formatter, and the structure
  test passing.
- **E2.** `just scenario` passes on both forges. This CR touches the CLI's package, and the
  scenario's board step (16c, as `visualization-backend` left it) still holds:
  - `GET /` serves the page;
  - each static module answers 200 with a JavaScript or CSS content type;
  - the policy allows scripts, styles, images and fetches from `'self'` only.

  The Driver adds these three checks to that step if it lacks them.
- **E3. Code shape.** A table of every `static/` file with its line count, and the list of view
  modules: one per view. `rg -n "innerHTML\s*=" static/js` shows only `dom.js`'s one sink, or
  none.
- **E4. Escaping.** On a scratch planning folder, three markups are put in places the views
  show:
  - a CR titled `Board <b>bold</b> <img src=x onerror=alert(1)>`;
  - a backlog item whose `01-intent.md` holds the same markup and a `<script>` line;
  - an `evil.svg` holding a script in its folder.

  Each shows as text. No dialog opens, and the browser's console shows no error and no blocked
  inline script.
- **E5. The test case folder.** `visualization-backend`'s own folder (archived or in the
  backlog) opens in the panel. Its tree shows:
  - the top Markdown files, then `evidence/` with its nested images (shown), `intake/`,
    `prototype/` with `v1/`, and `work/`;
  - `data.js` listed by size, never shown as text.
- **E6. Live refresh.** With the board open on the Batch view and a CR's panel open:
  - a CLI command that changes the record (`note`, `round`, a `triage` in the backlog) appears in
    the view without a reload, within the server's refresh period;
  - the panel stays open on its file.
- **E7. Semantics cases** the live batch does not show: a parallel batch, a series, a stack with
  a CR not yet stacked, an open dependency, a fix CR, a release, a blocked CR with its reason, a
  queued CR that waits. They come from scratch planning folders made with the CLI (as the
  scenario does). One PC screenshot each shows its PR column and its graph, with the words of
  "Semantics".
- **E8. In-project and surface.** The board on this repository's planning folder shows no
  picker. The board on a scratch surface of three projects (one a copy of this repository's
  planning folder, one with no batch, one small) shows the picker and "All projects". The
  overview hides Kanban, Batch and Costs; a view chosen there opens on the last project.
- **E9. A cold machine.** On Windows, with `UV_CACHE_DIR` and `npm_config_cache` set to new empty
  folders outside the repository, `just lint` passes. The tools' versions are printed.
- **E10. The final QA: the views beside the prototype** (below).

## Final QA: the views beside the prototype, on PC and on the phone

This is the last step before the hand-back, and the PR's main deliverable.

1. **The same data on both sides.**
   - Copy the prototype folder (`index.html`, `snapshot.py`) to `work/verifier/prototype/`.
   - Regenerate its `data.js` there with `snapshot.py` from the planning folder the board
     serves. That folder must hold a running batch, because `snapshot.py` reads
     `4-batch/batch.json`. The prototype and the board then show the same CRs.
   - The prototype's `exemple-*` projects stay examples: for "All projects" and the picker, the
     comparison is of layout and words, not data.
   - Serve the copy as `prototype/README.md` says, and start the board on the same folder.
2. **The shots.**
   - A throwaway uv script in `work/verifier/`, with Playwright and Chromium in its inline
     dependencies, not committed, opens each view of each side at:
     - 1400x860;
     - 375x812, as a phone (mobile viewport, touch).
   - Both sides are taken at the same moment, with animations off, after the data is drawn. The
     shots cover:
     - Home;
     - Kanban, PC and one swiped column on the phone;
     - Batch, PC and the phone with the PR columns first;
     - Costs;
     - the panel open on `visualization-backend`'s folder, on a specification and on an image;
     - the picker open, PC and phone;
     - "All projects", the PC table and the phone cards;
     - the phone's bottom bar on a project and on "All projects".
3. **The side-by-side images.**
   - One image per view and width, `compare-<view>-<pc|phone>.png`: the prototype on the left,
     the board on the right.
   - Each is captioned with the view, the width, the prototype's matching `v6-xx` (from the
     table of "The reference"), and the head's short SHA (seven characters).
4. **The checklist.**
   - One table per view: each element of this specification's section for that view, "same",
     or "differs: <why>".
   - A difference is fixed, unless it is one of:
     - an element a later CR owns;
     - the English words;
     - real data instead of the prototype's examples;
     - a fix of the prototype that this specification names (the heartbeat stopped, the absent
       budget).
   - Each listed difference names which of these it is.
   - The browser's console shows no error and no failed request on either width.
   - No request goes to another origin.
5. **The real phone.**
   - The comparison above is an emulated phone. The board's URL opened on a real phone over the
     local network is the user's to try.
   - Until it is done, the PR's Known gaps names it ("not checked on a real phone"), and the
     Chief of Staff asks the user.

The final QA of the five CRs together, after the last one merges, is the Chief of Staff's order
(02-answers, "Split into CRs"). This CR's comparison is its share of it.

## Open points (defaults taken, for the Chief of Staff to confirm with the user)

1. **The page's language.**
   - Default: English, as `AGENTS.md` asks of repository text, with the words of the table in
     "Code layout".
   - The prototype the user approved is in French. The alternative is French labels, or a
     French and an English word list in `words.js`.
2. **Facts the server lacks.**
   - Default: this CR adds them to the board's read data, from the record only, never to
     `STATUS.json`.
   - The alternative is to send them back to `visualization-backend` before this CR starts.
3. **A card's description.**
   - Default: the server gives each item and CR the first paragraph of its
     `03-change-spec.md`, else `01-intent.md`, else its first Markdown file. It skips headings
     and the `issue:` line, as the prototype's `firstPara` does. The server reads that paragraph
     once per refresh, never with one fetch per card.
   - `cr-summaries` replaces it with the summary.
4. **"Recompute" in Costs.**
   - Default: drawn only when the merged server offers an on-demand recompute; otherwise the age
     alone.
   - Whether a recompute is recorded or kept in memory is the server's (feasibility, point 3).
5. **"Waiting for you".**
   - Default, as in the prototype: every blocked CR plus the unread asks.
   - The feasibility study notes that a CR blocked only on `waits:` needs no one, and would
     leave it out.
6. **A stopped heartbeat and an absent budget.**
   - Default: a heartbeat marked stopped shows "stopped", not an age.
   - With no budget, the meters and the percentage show "—".
   - Neither case is drawn by the prototype.
7. **"Data" in "All projects".**
   - Default: the age of the project's last event, "—" with no batch.
   - The prototype's figure was the snapshot's age, which has no live meaning.
8. **The parallel merge order.**
   - Default: the time each CR was last handed back `ready`, else `updated`.
   - The prototype sorts on `updated`, which a later `note` or `ship` moves.
9. **The board unreachable.**
   - Default: the sidebar's foot says "Board unreachable" with the data's age.
   - The page keeps showing the last data and retries at the refresh period.
10. **The JS and CSS lint tools.**
    - Default: ESLint, Stylelint and Prettier, on a Node.js taken from PyPI through `uvx`,
      pinned in the `justfile`.
    - The alternative is Biome, one tool, if it runs through `uv` and covers the targets
      (file and function length, complexity, parameters, nesting).
    - Either way, `uv`, `just` and `git` stay the only tools installed by hand.
11. **The server's own HTML page.**
    - Default: if `visualization-backend` kept today's server-rendered page, this CR removes it
      and `GET /` serves the static shell.
    - The alternative keeps it at another path, as a page with no script.
12. **A batch history view.**
    - Default: not in this CR.
    - It goes to a new inbox item, after `batch-history` and this CR, with a prototype step
      first.
13. **The `specifying` state** (a `work/specifying` marker, `status.spec_state`).
    - Default: not shown, as in the prototype.
    - A backlog item being specified counts as "in grill".

## Decisions after the specification (they replace the open points they name)

Asked by the Chief of Staff, 2026-11-13 (in French, recorded in English).

- **The page's language: both.** English by default and French, from one word file per language, built so that more translations can be added later. The prototype's French labels are the French file. Where an open point above says English only or French only, this answer replaces it.
- **JS and CSS lint: ESLint (and Stylelint, Prettier) through uvx**, on a Node.js taken from PyPI and pinned in the `justfile`, run by `just check`; Biome instead if it covers the targets more simply. `uv`, `just` and `git` stay the only tools installed by hand. The first CR that ships JavaScript (visualization-backend) adds it.
- The other open points stay at the specification's defaults.

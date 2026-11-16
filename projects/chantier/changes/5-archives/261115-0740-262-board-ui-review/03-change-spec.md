# Change Specification: the web board after the user's first page-by-page tour

No issue.

## Goal

On 2026-11-14 the user toured `chantier board` page by page with the Chief of Staff and said what
is wrong (`intake/request.md`). Wanted, in the user's words:

- Kanban: "Je vois bcp d intake (qui devrait s'appeler inbox), plein de grill, et zéro fini dans la
  vue Kanban": the first column is named Inbox, the Grill column holds only what is being grilled,
  and a column shows what is done.
- Kanban: "j'aimerais pouvoir choisir les Priorités affichées (par exemple cacher les P3 et P4)."
- Triage: the page the user missed against the prototype ("je n'ai pas la page backlog") exists in
  code (`views/triage.js`); it shows in both languages. "les cartes n'ont pas le même style, titre,
  etc que dans les autres pages"; "il y a un détourage lors de la sélection en bleu pas beau";
  kept: "l'effet pour prendre une carte est sympa je garde".
- Costs: "la page coût ne me permet pas de voir les coûts des batches précédents."
- Home: "recent activity vide, pas d'info sur les batch fermés et les CR des batches précédents";
  "on a pas mal de grill en cours et pourtant je vois que des 0".
- The counters the Chief of Staff noted the same day agree with the columns they summarise.

There is no `01-intent.md` or `02-answers.md`: the request's notes are the decisions. Batch and All
projects were not toured and do not change.

**Caveat, carried from the request.** The Home notes were taken on a stale build served by uv's
cache (`uvx --refresh --from <checkout>`), with no Triage view. The user then said "Home's notes
stand on the live board". The Driver checks each Home point on the live code first (`uv run
--locked --project <checkout> chantier board` on this repository's planning folder) and records in
the PR, point by point, what the live board showed before the change.

## Rules that bind this CR

- `AGENTS.md`: the board edits the backlog only through the CLI's role-free commands, never a
  batch, and knows no role. This CR adds no write: every change is a reading change, plus a
  filter kept in the page's state.
- `CONTRIBUTING.md`, the page's targets (300 lines a file, 50 lines a function, cognitive
  complexity 10, colours in `css/tokens.css` only, no `!important`, one module per view, the same
  keys in each `js/i18n/` file, a view reads the store and the model, never `fetch` or
  `localStorage`). A view that grows past 300 lines is split into a sibling module, as
  `home-*.js` and `costs-*.js` already are.
- The board's API is fed by `board/state.py`. `status/views.py` also writes `STATUS.json`, which the
  CR board pane reads: this CR does not change `status/views.py` or any `STATUS.json` field, so
  `AGENTS.md`'s pane screenshot rule does not apply. A change that finds it must touch them stops
  and says so.

## What changes

Code under `skills/chantier/scripts/cli/src/chantier/board/` (below, `web/` is
`board/web/`). Three parts, each deliverable alone (see open point Q1).

### Part A. Kanban, the header's figures and the cards' titles

**A1. The columns** (`web/js/views/kanban.js`, `columns()`). The columns become, left to right:

| key | name (en / fr) | holds |
| --- | --- | --- |
| `inbox` | Inbox / Inbox | `1-inbox` items at stage `raw` |
| `backlog` | Backlog / Backlog | `2-backlog` P1 to P4 items at stage `raw` |
| `grill` | Grill / Grill | `1-inbox` and `2-backlog` items at stage `grill` (the record's `grill` or `specifying`) or `spec` (`specified`): being grilled or specified, not yet in `3-ready` |
| `ready` | 3-ready / 3-ready | `3-ready` items, as today |
| `progress` | In progress / En cours | the batch's CRs `queued`, `working`, `blocked`, as today |
| `handed` | Handed back / Rendus | the batch's CRs `ready` (any readiness), as today |
| `done` | Done / Terminé | merged CRs, newest first, from the state's `merged` list (the batch's `3-done` CRs, then `5-archives`) |

- A stage is read with `stageOf()` (`web/js/model/grill.js`); no new stage word.
- The Done column draws at most the 20 newest of `merged` (a `DONE_SHOWN` constant); its count is
  `merged_total`, and when it holds more than it draws, its foot says "{n} more" (en) / "{n} de
  plus" (fr). A Done card shows the CR id, its title, its batch and its merge date, and opens its
  folder like any card (its `path` from the record).
- The Inbox column keeps the **+ New** button (today on `intake`).
- The sub-lines (`kanban.*_sub`) are rewritten for the new columns in `en.js` and `fr.js`, every
  column name and sub-line in French in `fr.js` (today `kanban.progress` reads "In progress" in
  French).
- The keys `kanban.intake*` are renamed `kanban.inbox*`; `stats.intake` in the header becomes
  `stats.inbox` ("inbox" / "inbox").
- The filters row's count (`kanban.count`) still says the items shown and the merged total.
- The sidebar's Kanban count (`views/registry.js`) is unchanged.

**A2. The priority filter.** Beside the label filter (`web/js/labels/filter.js`), the Kanban draws a
row of five toggles: Inbox, P1, P2, P3, P4, all on by default. A toggle off hides the items of that
bucket from every column (Inbox, Backlog, Grill); `3-ready` items, the batch's CRs and the Done
column are never filtered. The choice is the page's state for the session, a new store field
(`priorityFilter`, in `web/js/core/store.js`), written nowhere on disk, like `labelFilter`; the
label filter and the priority filter combine (an item shows when it passes both). A new module
(`web/js/labels/priority.js`, or a name the Driver judges better) holds the row and its binding;
the words go in `en.js` and `fr.js` (`priority.title`: "Priorities" / "Priorités"). Triage does not
draw it.

**A3. The header's figures** (`web/js/ui/header.js`, `of()`). Each figure counts what the Kanban
column of the same name holds:

- inbox: the Inbox column's items (raw `1-inbox` items);
- in grill: the Grill column's items (today it counts every not-specified P1 to P4 item, raw ones
  included);
- in progress: the batch's CRs `queued`, `working` and `blocked` (today `working` only, so a
  blocked CR read "0 in progress"); word `stats.progress` ("in progress" / "en cours");
- handed back: the batch's CRs `ready`, as today.

The header ignores the priority and label filters. The count rules are written once, in
`web/js/model/` (a function per column, used by both `kanban.js` and `header.js`), so they cannot
drift apart again.

**A4. A card's title** (`board/backlog.py`, `backlog_items()`). An item's `title` is its
`summary.json` title when the CR has one (`summary_view(folder).title`, already read by
`summary_fields()`), else today's value (`subject(row["title"])`, the first line of the first of
`03-change-spec.md`, `01-intent.md`, `intake/request.md`). So `cr-folder-self-contained` no longer
reads "Intent". This is the board's own data; `status/views.py` and `STATUS.json` keep their title.

### Part B. Home and Costs read the earlier batches

The state already carries the closed batches: `board/state.py`, `_history()`, sends every
`5-archives/batches/batch-NN.json`, newest first, as `history` (each with `batch`, `opened`,
`closed`, `mode`, `budget_usd`, `cost_usd`, `cost_unpriced` and `crs`, each CR with `cr`, `title`,
`result`, `pr`, `rounds`, `cost_usd`). No view reads it today. Part B reads it; the server changes
only if a field is missing (none is known).

**B1. Costs, the earlier batches** (`web/js/views/costs.js`, `costs-tables.js`, or a new
`costs-history.js`).

- Below today's content, a table **Earlier batches** / **Batches précédents**: one row per record
  of `history`, newest first: the batch id, its closing date, its mode, its CRs (merged / total),
  its cost against its budget, and its unpriced mark when `cost_unpriced` is not empty. A CR title
  in the records starts with "Change Specification:": it is drawn without that lead (as
  `subject()` does on the server; done once, in the model or on the server).
- A click on a row unfolds that batch's CRs below it (CR, title, result, rounds, cost); a second
  click folds it. Which rows are open is the page's state for the session.
- With no batch running, Costs no longer shows only "No batch running": it shows that line, then
  the earlier batches' table and the last merged CRs. The Recompute line and the four figures stay
  for a batch only.
- The sidebar's Costs count (`views/registry.js`) is unchanged: the running batch's spend, else
  nothing.

**B2. Home, the closed batches and the earlier CRs** (`web/js/views/home.js` and its blocks).

- A block **Earlier batches** / **Batches précédents** (a new `home-history.js`): the five newest
  records of `history`, each on one line: id, closing date, merged / total CRs, cost; a "see the
  costs →" link opens Costs (`data-go="costs"`).
- The recent-activity block (`home-feed.js`), with no batch running: instead of "none", it says
  that no batch is running and names the last closed batch (id, closing date, merged / total CRs,
  cost) from `history[0]`; with no record either, "none" as today.
- The last merged CRs (`home-backlog.js`, today the 4 newest, with the total) show each CR's batch
  beside it (the `batch` field the `merged` rows already carry).

**B3. Home, what is being grilled** (`web/js/views/home.js`, `TILES`). A tile **In grill** /
**En grill**: the number of items of the Grill column (A1's rule, the shared model function), its
sub-line "{n} specified" / "{n} spécifié(s)" (the items at stage `spec` among them), its tone `go`
when it is not zero, and `go: 'kanban'`. The pipeline bars keep counting by stage as today. With
the repository's planning folder on 2026-11-14 (fast-scenario, baseline-and-legacy, board-cr-step,
worker-reply-length... carry `02-answers.md` or `03-change-spec.md`), the tile is not zero.

**B4. Home, "Waiting for you"** (`home.js`, `waitingTile`, and `waitingForYou()` in
`web/js/model/semantics.js`). Today it adds the Foreman's unread asks to the Chief of Staff
(`asks_unread`) to the blocked CRs, and read "44 questions" that were not the user's. The tile
counts what waits for the user only (see open point Q3 for the default). `docs/web-board.md`'s
sentence on the tile follows.

**B5. Home's first load.** After a restart, Home stayed on "Loading..." until a second visit. The
Driver reproduces it on the live board (start the server, open the link once); if it reproduces,
the first paint draws Home once the state arrives (`web/js/ui/host.js`, `web/js/core/refresh.js`);
if it does not, the PR says so under Known gaps with the steps tried.

### Part C. Triage's cards

**C1. Same card as the other views** (`web/js/triage/postit.js`, `web/css/views/postit.css`,
`web/css/widgets.css`). A Triage card draws the Kanban item card's markup and style
(`itemCard()` in `web/js/views/kanban-cards.js`: the bucket's priority tag, the slug, the title in
`.ttl`, the labels, the description, the files and the stage word): one function makes the item
card for both views (moved to a shared module, for example `web/js/ui/item-card.js`), with
Triage's extras added to it: the late-summary clock, the origin badge, the open button, the
`modified` and pending marks, and the attributes the drag and the selection need (`draggable`,
`tabindex`, `role`, `aria-*`, `data-slug`, `data-key`). The per-stage post-it fills
(`.pi.grill`, `.pi.specified`...) go; the stage reads in the card's foot as on the Kanban. (Today
`.pi.specified` and `.pi.automatable` never match: `stageOf()` returns `spec` and `auto`.)

**C2. The pick-up effect stays.** The hover tilt and lift (`.pi:hover`: `rotate(-0.6deg)` and
`--shadow-note-hover`), the dragged card's fade (`.drag`) and the drop targets (`.over`) behave as
today on the new card.

**C3. No blue outline on a selected card.** `.pi.sel`'s `outline: 2px solid var(--blue)` goes.
A selected card still reads as selected (the selection bar acts on it) by the mark of open point
Q4's default. The keyboard focus ring of `base.css` (`:focus-visible`, shown on keyboard focus
only, not on a click) stays, for keyboard users.

**C4. The Triage word in both languages.** `nav.triage` exists in `en-write.js` ("Triage") and
`fr-write.js` ("Triage", a French word); the sidebar lists Triage between Home and Kanban
(`views/registry.js`). The Driver checks it on the live board in both languages and keeps the word
unless the user answers Q5 otherwise.

### Docs

`docs/web-board.md`: the Kanban paragraph and its picture's caption name the new columns and the
priority filter; Home's paragraph names the In grill tile, the earlier batches and the new "Waiting
for you"; Triage's paragraph says its cards are the Kanban's; Costs' paragraph names the earlier
batches. `docs/demo/`: one project with no running batch (`mobile-app`) gains a closed batch's
record (`changes/5-archives/batches/batch-01.json` and `.md`, made up, matching its archived CRs),
so the pictures show the earlier batches; `docs/demo/README.md` names it. The pictures are retaken
with `just docs-screenshots` and committed.

## Out of scope

- The Batch view and All projects (not toured).
- Any new write of the board, any change to a batch, to `status/views.py`, `STATUS.json` or the
  CR board pane (`hooks/`).
- The prototype's other differences not named by the user; a later tour files them.
- Storing the filters across reloads (see open point Q2).
- The CLI's `cost` command and how a batch records its costs.

## Evidence

- `just check` passes (Linux, macOS, Windows in CI): Biome on `board/web`, `test_code_targets.py`
  (file and function sizes, the same i18n keys in each language), `test_board.py`.
- `just scenario` passes at the PR's head (`AGENTS.md`: the board is part of the CLI).
- On the live board, run on this repository's planning folder at the PR's head (`uv run --locked
  --project <worktree> chantier board --host 127.0.0.1`), in English and in French, screenshots in
  the PR's Deliverables, each captioned with the head's seven-character SHA:
  - Kanban: the seven columns named as in A1, no English name in French; the Inbox holds
    `1-inbox`'s raw items, the Grill column fast-scenario, baseline-and-legacy and the other items
    with `02-answers.md` or `03-change-spec.md`, Done the newest merged CRs with "{n} more"; P3 and
    P4 toggled off hide their items and nothing else; the header's figures equal the columns'
    counts; `cr-folder-self-contained`'s card shows its `summary.json` title, not "Intent".
  - Triage: the cards look like the Kanban's; hover and drag tilt and lift as before; a selected
    card has no blue outline and still reads as selected; a drag between priorities still moves
    the folder (the board's journal gains the line, as today).
  - Costs with no batch running: the earlier batches batch-17 to batch-01, batch-17 unfolded with
    its CRs and their costs.
  - Home: the In grill tile not zero, the earlier batches block, the activity block naming
    batch-17, the last merged CRs with their batch, "Waiting for you" as Q3 decides.
- The PR records, per Home point, what the live board at the base showed (the caveat) and the B5
  result.
- `just docs-screenshots` run; the changed pictures in the PR.

## Open questions for the user

- **Q1. One CR or three.** Several views change. Default: one CR, delivered in the order A, C, B,
  since A and C share the item card. To split: CR 1 "Kanban, header and cards" (Parts A and C,
  they share the card), CR 2 "Home and Costs read the earlier batches" (Part B), independent of CR
  1 and runnable in parallel (no `depends.json`). Split, or keep one?
- **Q2. The priority filter after a reload.** Default: session state like the label filter, back
  to all on at the next load. Or remembered on this device (like the language and the project)?
- **Q3. "Waiting for you".** Default: the blocked CRs only; the Foreman's unread asks to the Chief
  of Staff leave the tile and stay in the Batch view. Or keep them in the tile, named "questions to
  the Chief of Staff"?
- **Q4. How a selected Triage card shows.** Default: a check mark in its top row and the card
  lifted (the hover's shadow, held), no outline, no blue. Another mark?
- **Q5. The Triage word in French.** It reads "Triage" (a French word) today. Keep it, or another
  word? Same question for "Home", which reads "Home" in French.
- **Q6. The Kanban's columns.** Default as in A1: raw backlog items in a Backlog column, the Grill
  column for items being grilled or specified (from the inbox or the backlog), seven columns in
  all. Or keep the inbox's grilled items in Inbox, with only the backlog split?

# Batch page: a Kanban of the batch's three folders

The board's batch page gets a fourth view, **Kanban**, first in its existing view switch (Kanban,
Graph, Gantt, Time cards) and opened by default: three columns, `1-pending`, `2-actives` and
`3-done`, each holding the batch's CRs whose folder is in that folder of `4-batch/`. The choice of
view is kept on the device. Read-only: the folders move by the CLI's lifecycle only.

Web client only (`skills/chantier/scripts/cli/src/chantier/clients/web/`), plus its doc and two
static tests. No server, CLI, card or record change.

## Goal, in the user's terms

The user (2026-11-21, from the phone, on batch-30's graph): "Dans batch il faut une vue kanban sur
les 3 etats possible dans le batch." In English: the batch page needs a Kanban view of the three
states a CR can be in inside the batch.

## Decisions carried (02-answers.md, and the Chief of Staff's brief)

| Source | Decision | Where it lands |
| --- | --- | --- |
| kanban-Q1 | A Kanban view and the graph on the batch page, through the page's view switch; Kanban by default; the choice kept on the device. | 1, 2 |
| Chief of Staff's message (2026-11-21) | The batch page already has a view switch (Graph, Gantt, Time cards). The Kanban joins it as its first entry. There is no second toggle. | 1, 2 |
| kanban-Q2 | In `1-pending` and `2-actives`, cards are in the batch's order by CR number. In `3-done`, the last merged CR is on top. The order is stable: a card never moves inside its column when a CR changes state, and leaves it only when its folder moves. | 3 |
| kanban-Q3 | Destination: batch-30 at once, with board-batch-chip-stale (same page). | Overlaps |
| Restatement | The column is the CR's real folder in the batch, not a state derived from the record. | 3 |
| Restatement | Read-only: no drag between columns. | 4 |
| kanban-Q5 (Fable advisor, in the user's place) | A closed batch's Kanban tab shows a one-line note, as Gantt and Time cards do: no columns, no cards, no automatic tab switch. Key `batch.kanban_closed`; the static test counts eight keys; one doc sentence. | 2, 5, 6 |

**Read-only kept, and why the code agrees.** The Chief of Staff added "read-only" to the
restatement. The code gives a reason to keep it, and none to drop it. AGENTS.md says the surface
server "never edits a batch": a drag that moved a CR between `1-pending`, `2-actives` and `3-done`
would be the board editing a batch. Those moves belong to `take` (`lifecycle/stages.py`,
`1-pending` to `2-actives`) and to `order merged` / `handback released` (`rails_release.py`, to
`3-done`). Today only the Triage page has a drag (`js/triage/drag.js`); the project Kanban
(`js/views/kanban.js`) has none. The batch Kanban follows the project Kanban.

## What changes

### 1. The view switch: Kanban first, the choice kept on the device

`js/core/router.js`:

- `TABS` becomes `['kanban', 'graph', 'gantt', 'cards']`. The Kanban is the first entry and the
  default.
- The tab kept on the device is the store's preference `batchTab`, read with `pref('batchTab')` and
  written with `setPref` (`js/core/store.js`; the router and the store stay the only writers of
  `localStorage`). `apply()` writes it each time the Batch view settles on a tab, whether from a
  click, a key, a link or back/forward: the tab last shown on the Batch page is the one kept.
- Where the tab comes from, in this order:
  1. the address's `t=`, when it is one of `TABS`;
  2. else, only when the page is on the Batch view now and stays on it in the same project
     (`now.view === 'batch'`, `view === 'batch'`, `project === now.project`: the batch navigator),
     the tab shown now, `now.batchTab`;
  3. else the kept tab, `pref('batchTab')`, when it is one of `TABS`;
  4. else `kanban`.

  Step 2 needs the `now.view === 'batch'` test, which `tabOf()` (`router.js:134-137`) lacks today:
  on any other view `apply()` (`router.js:94`) sets `batchTab` to `TABS[0]`, so without it a move
  from Home to Batch would take `kanban` at step 2 and never reach the kept tab. `resolve()`
  follows steps 1, 3 and 4 (a first load has no tab shown now); `tabOf()` follows all four. One
  helper (for example `keptTab()`: the kept tab when one of `TABS`, else `kanban`) gives steps 3
  and 4 to `resolve()`, `tabOf()` and `settle()`. Every other view still gets `TABS[0]`, and
  `apply()` writes the preference only when the view is `batch`.
- `href()` writes `t=` for every tab of the Batch view, `kanban` included, and for no other view.
  A copied address therefore reopens the same tab on any device. The module's head comment
  ("&t=<tab> (the Batch view's tab, when not the graph)") and `tabOf()`'s comment say so. An address with no `t=` (the
  sidebar, a link from Home or Costs, an old link) opens the device's kept tab.
- `settle()` (`router.js:47-56`): on "All projects" it keeps resetting the tab to `TABS[0]` for
  a view that stays on "All projects". When it moves the place back to a real project
  (`lastOf(ids)`, for a view "All projects" does not show) and that view is `batch`, the tab is
  the kept one, steps 3 and 4 (`keptTab()`), not `TABS[0]`.

`js/core/store.js`: the initial `batchTab` becomes `'kanban'`, and its comment names the four tabs.

`js/views/batch.js`:

- `tabBar` needs no change: it draws `TABS`, so the Kanban chip comes first.
- The arrow keys move through the four tabs (`arrows` already reads `TABS`).
- The legend pill (`legend()`) stays above the switch on every tab, as today.
- `render()` draws the Kanban panel when `state.batchTab === 'kanban'`. The panel is
  synchronous: `batch-kanban.js` is imported statically, like `batch-graph.js`, because it is the
  default and must not show "Loading the view…".
- `tabModule()` returns no module for the Kanban. Opening a card is already wired for the whole
  page by `bindOpen(root)` in `mount`. Leaving the graph for the Kanban unmounts the graph's
  listeners, as any tab change does.

### 2. The words

Every string goes through `t()`, in both language files, `js/i18n/en-batch.js` and
`js/i18n/fr-batch.js`:

| Key | en | fr |
| --- | --- | --- |
| `batch.tab_kanban` | `Kanban` | `Kanban` |
| `batch.kanban_pending` | `1-pending` | `1-pending` |
| `batch.kanban_actives` | `2-actives` | `2-actives` |
| `batch.kanban_done` | `3-done` | `3-done` |
| `batch.kanban_pending_sub` | `joined, not taken yet` | `entrés, pas encore pris` |
| `batch.kanban_actives_sub` | `taken: working, blocked or handed back` | `pris : en cours, bloqués ou rendus` |
| `batch.kanban_done_sub` | `merged, last merged first` | `fusionnés, le dernier en premier` |
| `batch.kanban_closed` | `This batch is closed: its CRs are in 5-archives. The Graph tab shows them.` | `Ce batch est clos : ses CR sont dans 5-archives. L'onglet Graph les montre.` |

The column names are the folder names, the same in both languages, as the project Kanban's
`kanban.ready` is `3-ready`. An empty column reuses `kanban.empty`.

### 3. The Kanban panel: `js/views/batch-kanban.js` (new)

This is a pure module, `kanbanBlock(state, rows)`, which returns the panel's markup. It reuses the
board's parts and builds no card or column of its own (DESIGN.md, "One card, one column, one
chip"):

- **Columns.** Each column is built by `column()` of `js/ui/column.js`, as `js/views/kanban.js`
  builds its columns:
  - key `bcol-pending`, `bcol-actives` and `bcol-done`;
  - the name and sub-line from section 2;
  - count = the column's number of cards;
  - dots `var(--grey)` for `1-pending` (the queued colour), `var(--blue)` for `2-actives` (the
    working colour) and `var(--ink3)` for `3-done` (the project Kanban's Done);
  - no `act`, no `drop`, no `foot`.
- **Cards.** Each card is `crCard(state, c)` of `js/views/kanban-cards.js`, the project Kanban's
  card for a batch CR. That gives the CR number, the next-to-start tag, the slug, the round bars,
  the step, the round, the files, the dependencies, the open waits, the state icon and the cost. A
  click opens the CR's folder (`opener(crKey(c))`), and the open CR carries `sel`.
  - `crCard` is used **unchanged**, with no new option. Its card shows no folder chip: CR-433
    board-batch-chip-stale (its chip-Q3) leaves the Kanban page's batch CR card unchanged, so
    `crCard` gets no `stage` chip, and the column already says the folder.
  - This CR adds no field and no option to the card, and does not edit `kanban-cards.js`.
- **Which column.** The column is the CR's real folder, read from the row's `stage` field.
  board-batch-chip-stale lands before this CR and adds that field in `board/crs.py:_row`, in
  place of `priority`: `1-pending`, `2-actives` or `3-done`, read from the CR's folder on disk.
  - The Kanban reads `c.stage` only. It never derives the folder again: no parsing of `c.folder`
    and no client helper.
  - The column is never derived from `state`. A CR whose row carries no `stage` among the three is
    in no column: a CR cancelled or dropped, whose folder `order drop` moved to the inbox, the
    backlog or the trash, or a CR whose folder is not found. The Graph tab still draws it, as
    today. This assumes chip-stale gives such a row no `stage`, or one outside the three. Either
    way, the Kanban draws it in no column.
- **Order** (kanban-Q2):
  - In `1-pending` and `2-actives`, the CR number ascending: the number part of `c.cr` (`CR-425`
    gives 425), compared as a number.
  - In `3-done`, the row's `c.merged_at` descending, then the CR number ascending on a tie or a
    missing `merged_at`. Not `mergedAt(c)` (`js/model/semantics.js:52`): it falls back to
    `updated`, which moves with any write to the CR and would make cards jump.
  - The order reads nothing else (not `state`, `phase`, `updated` or `next_to_start`). A card
    therefore keeps its place while its CR works, blocks or hands back. A new card appears in its
    place by number, and a new merge enters `3-done` on top.
- **Layout.** The markup is
  `<div class="kanban bkanban" data-key="bkanban"><div class="board">…three columns…</div></div>`.
  Its classes reuse `css/views/kanban.css`:
  - its `.board` flex row and its phone rule (on a phone, one column at a time, scroll-snapped);
  - its `.step` and `.bars` rules, which `crCard`'s step and round bars need and which are
    scoped to `.kanban`.

  `css/views/batch.css` adds only layout rules for the wide screen, scoped `.batch .bkanban`, so
  the three columns share the central column's width beside the PR column:
  - `.batch .bkanban .column`: `flex: 1 1 0` and a `min-width` so a card stays readable;
  - written outside the phone `@media`, or with a selector that does not beat the project
    Kanban's phone rule, so the phone keeps the 86%-wide snapping columns;
  - `.batch .bkanban` resets `.kanban`'s `flex: 1` if it stretches the panel.

  These are a page sheet's placement and size only (DESIGN.md, "Components"). They use no literal
  in a margin, padding, gap, radius or font size, and they restyle no component.

- **The page keeps scrolling.** `css/shell.css:83-91` holds the project Kanban's rule
  `.main:has(.kanban) { overflow-y: hidden; }`. The batch Kanban's `kanban` class would match it
  and stop the batch page scrolling (the PR column below the fold would become unreachable). The
  rule narrows to the project Kanban, a direct child of `.view`: `.main:has(.view > .kanban)`,
  its comment kept. The next rule, `.view:has(> .kanban)`, already matches the direct child only
  and stays as is. The batch Kanban's columns grow with their cards and the page scrolls as today.

### 4. Read-only

`batch-kanban.js` writes no `draggable`, binds no drag, drop or pointer-move event, passes no
`drop` option to `column()` and calls no write op: no `call` of a backlog or config op, no
`data-col`. A card's one action is to open its folder. The word "drop" itself may appear (for
example a comment saying an `order drop` CR is in no column).

### 5. A closed batch's record

A closed batch's CRs are in `5-archives`, no longer in `4-batch/` (`close` refuses while
`1-pending` or `2-actives` holds a CR, and moves `3-done` to `5-archives`). On a closed batch
(`shownRecord`, the batch navigator's past batches), the Kanban tab shows a one-line note
(kanban-Q5), as Gantt and Time cards already do: no columns, no cards, and no automatic switch to
another tab.

`recorded()` in `js/views/batch.js` (line 111) draws, by tab: on `kanban`, `<p class="note">` with
`t('batch.kanban_closed')`; on `graph`, the graph as today; on `gantt` and `cards`,
`batch.times_none` as today. The legend and the tab bar stay as they are. `tabModule()` already
returns no module on a recorded batch.

### 6. Docs: `docs/web-board.md`, section "Batch" (line 36)

- The sentence "three tabs show the same batch three ways: **Graph** …, **Gantt** and **Time
  cards**" becomes four views. **Kanban** comes first and is the default: three columns,
  `1-pending`, `2-actives`, `3-done`, each holding the CRs whose folder is there. A card is the
  project Kanban's CR card, with no folder chip (the column says it), and opens its folder;
  nothing is dragged. In `1-pending` and `2-actives` cards are in CR-number order, and in `3-done`
  the last merged is on top. A CR cancelled or dropped is in no column but stays on the Graph.
- One sentence for a closed batch: on a past batch the Kanban tab shows a one-line note, its CRs
  being in `5-archives`, and the Graph tab shows them.
- The address sentence, "The tab is in the address (`&t=gantt`, `&t=cards`; the graph is the
  default and writes nothing), so a link opens the same tab; it is kept while you stay on the
  Batch page of the project and dropped by any other view or project.", is replaced whole, its
  "kept while you stay … dropped by any other view or project" clause included, by the device
  rule: the tab is in the address for every tab (`&t=kanban`, `&t=graph`, `&t=gantt`, `&t=cards`),
  so a link opens the same tab. With no `t=`, the page opens the tab last shown on this device
  (kept across views, projects and reloads), and the Kanban the first time.
- "The legend pill stays above the tabs" stays.

### 7. DESIGN.md

`clients/web/DESIGN.md` stays true with one change. Its "One card, one column, one chip" rule says
"Every board column (Triage, Kanban) is built by `js/ui/column.js`". It becomes "(Triage, Kanban,
the Batch page's Kanban)". The batch columns' dots are new columns, so the "same dot colour on
both pages" clause binds nothing new. No token, component or class is added. `bkanban` is a page
class laid out in `css/views/batch.css`.

## Out of scope

- Any drag or write from the batch Kanban; any change to the CLI, the server, `board/crs.py` or the
  record.
- The project Kanban (`js/views/kanban.js`) and its seven columns, unchanged.
- Moving the mode band and the legend line (board-batch-compact, after this CR).
- The chip a batch CR's card shows (board-batch-chip-stale).
- Hover lighting of dependencies on the Kanban (the Graph's `bindLight`): not asked.
- Retaking the docs screenshots (`just docs-screenshots`, by hand before a release): the batch page
  now opens on the Kanban, so `docs/board-mod-batch*.png` show the Graph tab of an older default.

## Evidence

- **Static checks on the shipped files** (`skills/chantier/scripts/cli/tests/test_board_design.py`,
  in `just check`). They read the files from the repository as they ship, at the head under test,
  not prepared texts. One parametrized test adds:
  - `js/core/router.js`'s `TABS` begins with `'kanban'`;
  - `js/i18n/en-batch.js` and `js/i18n/fr-batch.js` each define the eight keys of section 2;
  - `js/views/batch.js` uses `batch.kanban_closed`;
  - `css/shell.css` holds `.main:has(.view > .kanban)` and no bare `.main:has(.kanban)`;
  - `js/views/batch-kanban.js` imports `column` from `../ui/column.js` and `crCard` from
    `./kanban-cards.js`;
  - `js/views/batch-kanban.js` contains none of `draggable`, `dragstart`, `'drop'`, `"drop"`,
    `ondrop`, `drop:`, `data-col` or `call(`: the drop event and `column()`'s `drop` option, not
    the bare word "drop", which a comment may use.
  - `js/views/batch-kanban.js` reads `.stage` and never `.folder`.

  The existing tests keep passing on the new files:
  - `test_one_card`: the new module writes no `card` class;
  - `test_components` and `test_sheets`: the `batch.css` additions place and size only.
- **Biome** (`just lint`) passes on the web client.
- **The server field relied on.** The rows' `stage` is board-batch-chip-stale's, and so is its
  in-process check. This CR adds none. If chip-stale landed without such a check, the Driver says
  so in the PR's Known gaps.
- **By hand, in the PR's Deliverables** (DESIGN.md: a pull request's screenshots are the visual
  record), from a board running the PR's head on a real batch (batch-30, or `docs/demo/`):
  - the wide batch page on the Kanban tab, with cards in at least two columns;
  - the same page on a phone width (at most 760px), one column snapped;
  - the Graph tab after a reload, showing the kept choice;
  - an address with `&t=kanban` opened in a private window (no kept tab) and one with no `t=`
    there, both opening on the Kanban;
  - the Kanban tab at 1400x860 on a batch whose PR column is taller than the window, scrolled to
    the end of the PR column (the page still scrolls);
  - pick Graph, go Home, open Batch from the sidebar: the page opens on Graph;
  - with Graph kept, choose "All projects" while on Batch: the page goes back to a real project on
    Graph;
  - a closed batch (a past batch in the batch navigator) on the Kanban tab, showing the one-line
    note.
- **Gates** (AGENTS.md). The change is under the CLI's `src/` (the web client ships in the CLI's
  package):
  - the Driver runs `just check` and `just eval-dry-run` in the worktree at the pushed head;
  - the pipeline's `just scenario (ubuntu-latest)` must be green at the PR's head;
  - `just mod` is not owed: no `hooks/` or `types/` change.
- **No host or default matrix.** The behaviour depends on neither the host nor a configured value.
  The kept tab is the browser's own `localStorage`, the same on every OS.

## Overlaps in batch-30

- **board-batch-chip-stale** (lands before this CR in batch-30; same page, same card):
  - It replaces the batch rows' `priority` with `stage`, read from the CR's folder on disk in
    `board/crs.py:_row`. This CR's columns read that field and nothing else.
  - It changes the chip of a batch CR's card on the Batch page's graph only: its chip-Q3 leaves
    the Kanban page's `crCard` unchanged. This CR uses `crCard` unchanged too, with no folder chip
    and no new option (section 3).
  - Both edit `docs/web-board.md` line 36: chip-stale changes the priority-chip sentence, this CR
    the tabs and address sentences.
  - Both may edit DESIGN.md's "One card, one column, one chip" paragraph: chip-stale the chip,
    this CR the column list.
  - Rebase onto it with care: same files, different sentences.
- **CR-427 board-running-batch-lane**: Triage only (`js/triage/*`). It touches the same DESIGN.md
  paragraph ("One card, one column, one chip" gains a lane sentence) and the comment of
  `js/ui/column.js` (line 9). This CR edits that paragraph's column list, a different sentence,
  and does not touch `column.js`. No code overlap.
- **CR-429 board-fingerprint-cache**: it changes how the server reads the planning files and pushes
  them, not the rows' fields. This CR relies only on `batch.crs[*].stage` (chip-stale's). No web
  client file of this CR is expected in 429's change. Rebase on it, and recheck that `stage` still
  follows a folder move (429's notification path must republish a CR's move from `1-pending` to
  `2-actives`).
- **board-batch-compact** (lands after this CR, in batch-30): it moves the mode band and the legend
  line into the page's top rows, in `js/views/batch.js` (`render`, `legend`, `modeBand`) and
  `css/views/batch.css`, the two files this CR also edits. Its restatement already says the Kanban
  joins the existing view switch. This CR changes `TABS`, the panel and the Kanban's layout rules,
  and does not move the mode band or the legend. Compact rebases on this CR. Its doc change to
  line 36's "The legend pill stays above the tabs" follows this CR's rewrite of the same paragraph.

## Open questions

None. kanban-Q5 settled v1's one question (a closed batch's Kanban tab, section 5).

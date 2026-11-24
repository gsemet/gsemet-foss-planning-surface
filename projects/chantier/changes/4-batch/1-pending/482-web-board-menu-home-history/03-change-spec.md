# Web board: menu, detail overlay, multi-project home, History

The web board loses its Kanban page. Its menu renames "Inbox" to "Notifications" and puts Help
last. The detail panel hides its Grill button and dims the page behind it. The All-projects home
gains a feed of recent events and a list of open PRs, and the History page also opens on All
projects.

## Goal

From the user, 2026-11-24, looking at the web board: make the board's menu match what the user
actually uses, and make the multi-project home a place to follow every project at once:

1. Remove the Kanban page: it is of no use.
2. Rename the menu's "Inbox" to "Notifications": "Inbox" gets confused with the `1-inbox` folder.
3. Move "Help" to the very bottom of the menu, after "Configuration".
4. Hide the detail panel's Grill button for now: it does not work. It is hidden, not removed: the
   board's Griller stays in the server.
5. While a detail panel is open, grey out the rest of the page. A click on the greyed part closes
   the panel.
6. On the multi-project home ("All projects"), show an activity feed across all projects and a
   list of the open PRs (to review and to merge).
7. A History page at the root ("All projects"), to follow every project.

Destination: running batch batch-31.

## Rules that bind this CR

- `AGENTS.md`: a change under `skills/chantier/scripts/cli/src/chantier/clients/web/` reads its
  `DESIGN.md` first and keeps it true. Every section of `DESIGN.md` named below is edited in the
  same PR, so that the file still describes the board as it ships.
- `DESIGN.md` rules apply to every new markup and sheet: tokens only, no side accent border, the
  shared card, column and chip components, one-line titles, every word an i18n key in both
  `en-*.js` and `fr-*.js`, and `js/core/transport.js` as the only transport.
- No new forge read (web-board-Q1). The board keeps its existing reads of the forge (the forge
  hub, and the `prs` topic of a project's PRs page) and adds none.
- No CLI command, card or agent file changes. The server changes only what the new All-projects
  views read (below).

## What changes

### 1. The Kanban page is removed (recorded default)

- `js/views/registry.js`: the `kanban` entry goes, with its menu entry in the sidebar
  (`js/ui/sidebar.js`) and in the phone's bottom bar (`js/ui/bottombar.js`), which both read the
  registry.
- Removed: `js/views/kanban.js`, `css/views/kanban.css` and its `<link>` in `index.html`, the
  `.main:has(.view > .kanban)` and `.view:has(> .kanban)` rules of `css/shell.css`, the `nav.kanban`
  word in `en.js` and `fr.js`, and anything else that only the Kanban page used. The Driver finds
  these by the imports: for example the Kanban-only priority filter (`js/labels/priority.js`,
  `store.js`'s `priorityFilter`) if nothing else uses it, the `kanban` icon if nothing else draws
  it, and the `kanban.*` words that nothing else shows.
- Kept, because other pages use them: the Batch page's Kanban tab (`js/views/batch-kanban.js`, the
  `batch.tab_kanban` and `batch.kanban_*` words, `router.js`'s `TABS`), `js/views/kanban-cards.js`
  (the Batch tab's CR cards), `js/model/columns.js` (the header's figures and Home's tiles), the
  `kanban.*` words that Triage or the header show (for example `kanban.ready_sub`), `js/ui/column.js`
  and `js/ui/item-card.js`.
- The server's reads stay (recorded default): no op, topic or field of the server is removed.
- Home's "In grill" and "Next batch" tiles (`js/views/home.js`, `go: 'kanban'`) now go to Triage,
  where the items being grilled and `3-ready` are shown.
- An old address with `v=kanban` is an unknown view, and the router already handles one: it opens
  what it opens today for an unknown view. No special case is added.
- Comments that name the Kanban page as one of their users are corrected (`css/components/column.css`,
  `css/components/chip.css`, `css/dialog.css`, `js/labels/*.js`, `js/ui/column.js`,
  `js/ui/item-card.js`, `js/ui/parts.js`, `js/ui/header.js`, `js/model/columns.js`,
  `js/triage/postit.js`).
- `DESIGN.md`: "One card, one column, one chip" and "Waits on a card" stop naming the project's
  Kanban page. The Batch page's Kanban tab stays named.

### 2. "Inbox" becomes "Notifications" (recorded default)

- The view's word `nav.inbox` reads "Notifications" in `en.js` and in `fr.js`. The sidebar, the
  phone's bottom bar and the page's title (`js/ui/header.js` draws it from the same word) all
  show it.
- Unchanged: the view's id and address (`v=inbox`), its place (second, after Home), its count and
  badge, its page and its words (`en-inbox.js`, `fr-inbox.js`), and every word that names the
  `1-inbox` folder or Triage's Inbox column.
- `DESIGN.md`, "The Inbox page": the section says that the view is shown as "Notifications".
  Its "Notifications" bullet (browser notifications) is reworded so that the two meanings stay
  distinct.

### 3. Help goes last (recorded default)

- `js/views/registry.js`: the order becomes Home, Notifications (`inbox`), Triage, Batch, PRs,
  History, Costs, Dashboard, Configuration, Help. On All projects, which shows only the views with
  an overview, the order is Home, Notifications, History, Help. The phone's bottom bar follows the
  same order and keeps its sideways scroll, so Help, now its last item, stays reachable.
- `DESIGN.md`, "The Help page": "after Home (and the Inbox)" becomes "last, after Configuration
  (after History on All projects)".

### 4. The Grill button is hidden (recorded default, web-board-Q6)

- A single named constant in the web client, off as shipped (web-board-Q6: turning it back on
  takes an edit and a release; no `chantier.yaml` key), hides the detail panel's Grill button
  (`js/panel/griller.js`'s `grillAction`). With the button hidden, the discussion cannot be opened
  from the panel. Turning the constant on brings back today's behaviour unchanged.
- Nothing else changes: the server's Griller (`board/griller.py`, the `griller.*` ops, the
  `griller` topic, the host checks), `js/api/griller.js`, `js/panel/griller-view.js`,
  `css/griller.css` and the words stay as they are, and so do the existing griller tests
  (`test_board_griller*.py`).
- `DESIGN.md`, "The board's Griller", "The button": the button is hidden behind that constant, off as
  shipped. The section names the constant.
- `docs/web-board.md`, "The board's Griller": says that the button is hidden for now.

### 5. The page dims behind an open detail panel (web-board-Q3)

- While the file panel is open (`#panel.open`, `js/main.js`), the rest of the page (sidebar, header
  and view) is covered by a dimmed layer under the panel. The page behind can be seen but not
  used. On a phone, where the panel already fills the screen, nothing changes.
- A click or a tap on the dimmed layer closes the panel. It goes through the same path as Escape
  (`closeInnermost` / `confirmLeave()` of `js/edit/markdown-editor.js`):
  - with no edit, or an edit with no change (`dirty()` false), the panel closes at once;
  - with an unsaved edit, the existing leave dialog asks first (`edit.leave_title`, `edit.leave`,
    `edit.discard`). Confirm closes the panel and drops the edit; cancel keeps the panel and the
    edit.
- The layer's colour is a new colour token in `css/tokens.css`, with its row added to `DESIGN.md`'s
  token table, where the existing test (`tests/test_board_design.py`) compares the two. No literal
  colour goes in a sheet.
- The layer is ignored by assistive technology, as the page behind already is. The focus stays where
  the panel puts it today, and comes back to the opener when the panel closes.
- `DESIGN.md`: a short section, "The file panel's backdrop", states these rules.

### 6. The All-projects home: open PRs and recent activity (web-board-Q1, Q2, Q5)

The All-projects home is `js/views/overview.js`, fed by the `board` topic (`board/reads.py`'s
`board_data`, `board/state.py`'s `project_line`). It keeps its table and cards, and gains two
blocks, laid out with the existing `block` sections as the project home lays them out
(`home-prs.js`, `home-feed.js`):

- **Open PRs** (web-board-Q1, answer A): the PRs of the batches of every project. One row per CR of
  a project's batch that has an open PR (the record's view: a PR that is recorded, not merged, on a
  CR that is not merged or cancelled, the same test as `model/semantics.js`'s `openPr`). Each row
  shows:
  - the project's mark, the CR, its one-line title, and the PR number, a link to the PR (or the MR)
    when its address is a web one;
  - its state, one of three: **ready to merge** (the record's `to_review`), **red CI** (a CR ready to
    merge for which the forge hub has journaled a `checks-red@1` line in the project's
    `forge-journal.jsonl` since the CR's last hand-back), or **working** (every other open PR),
    shown with the existing state chip's variants and words only.
  
  Ready to merge and red CI come first, in the record's merge order. The block's head counts the
  rows. The rows come from the record and the journal lines the hub already writes: no new forge
  read, and no subscription to any project's `prs` topic from this page. Red CI is only known while
  the hub runs; the block shows no red CI when the hub has not journaled one.
- **Recent activity** (web-board-Q2 and Q5, answer A): the last 20 events of all projects, newest
  first. Only the CRs' life and the releases (web-board-Q5): no round, hand-back, board, writer or
  sync line.
  Each line shows the time, the project's mark, the event's kind (the History page's kinds and
  their chip variants: opened, merged, dropped, release), the CR and its one-line title. The events
  come from the same source as the History page below (the project's index of dated events,
  `board/history_page.py`'s `index_of`), so a line on the feed is always a line of the History.
  "No events" is shown when no project has any. A link under the block goes to the All-projects
  History.
- A row's CR opens its project, as the All-projects Inbox's Open does (`data-project`). Its PR
  number is a link that opens the PR only. The click does not reach the project's line.
- What the server adds: the data these two blocks need, read from the record, the hub's journal and
  the History index, with nothing written. Whether it goes into the `board` topic's project lines
  or into a topic of its own is the Driver's choice. It must not let the public read-only key
  (`READ_TOPICS` of `board/api/topics.py`) read anything that key cannot read today: an event's
  cost and rounds are the History's, which is private. `board/api/protocol.json` follows any new
  op, topic or field.
- The project's own home (`js/views/home.js`) is unchanged.

### 7. History on All projects (web-board-Q2, Q5, Q7)

- `js/views/registry.js`: the `history` entry gains an overview, so History shows on All projects,
  between Notifications and Help.
- On All projects, the page is the project's History page (`js/views/history.js`) widened to every
  project, paged in the same way (web-board-Q7): the same head (day, week or month, previous, next,
  Today), the same five figures summed
  over the projects shown, and the same day groups. Each row also shows its project's mark. The
  figures and rows cover every event of the period, with nothing cut: "complete" means every
  event of each period (web-board-Q7), not one unpaged list. The events are the CRs' life and the
  releases from each project's history (web-board-Q5).
- Two filters, both made of the existing filter-toggle chips (filled when on, outlined grey when
  off, `DESIGN.md`'s chip rule):
  - **project**: one chip per project of the surface, shown on All projects only;
  - **type**: one chip per kind (opened, merged, dropped, releases), on both the All-projects page
    and a project's page.
  
  Every chip is on at the start. The five figures count only what the filters show. If the filters
  ride in the address, they follow the `hp=`/`hd=` rule (only when not the default).
- The server's `history` topic (`board/api/topics.py`'s `_history`, `board/history_page.py`'s
  `answer`) also answers for all projects at once. Each event carries its `project`, and the answer
  merges every project's index (`index_of`, kept per project as today), so it reads no more files
  than the project pages do. The topic stays on the private key. `history-feed.js` subscribes for
  all projects when the page shows All projects.
- A row on All projects opens its CR's project, as in section 6. Its batch name goes to that
  project's Batch view, and its PR number is a link.
- `DESIGN.md`, "History": the page also shows on All projects, with the two filters and the
  project's mark. There is still no chart, and no new token, component or colour.

### Docs

- `docs/web-board.md`:
  - the Kanban section and its two pictures go (`docs/web-board/kanban-pc.png`,
    `kanban-phone.png`);
  - "Inbox" becomes "Notifications" where the view is named;
  - the All-projects home describes its two new blocks;
  - History says it also shows on All projects, with its filters;
  - Help says it is last;
  - the Griller's section says the button is hidden for now.
- `scripts/docs_screenshots.py`: the `kanban` shot goes, and the editor shot opens its item from
  Triage instead of from the Kanban. Retaking the screenshots (`just docs-screenshots`, by hand) is
  done if the Driver's machine can run it. If it cannot, the PR's Known gaps says the pictures
  still show the old menu.
- The `help` topics (`js/i18n/en-help.js`, `fr-help.js`) that name the Kanban page or the "Inbox"
  view are reworded. Topics that name the `1-inbox` folder stay.

## Out of scope

- The server's Griller and its fixes (it "does not work": that is another CR). Here the button is
  only hidden.
- Any new forge read, and any change to the forge hub, its interests or its journal lines.
- The project home's own feed and PR block, the PRs page, and the Batch page's Kanban tab.
- Renaming the `inbox` view's id or address, the `1-inbox` folder, or Triage's Inbox column.
- Keeping events beyond what the History index already reads (closed records, archived CRs' steps,
  the running batch). No new journal or store is written.
- The `live` terminal client (`clients/tui/`).

## Evidence

Every check below reads the shipped files of the web client and the server at the head under test,
as `tests/test_board_*.py` already do (`_read`/`_web` of the package's files), never a prepared copy.

- `tests/test_board_help.py`: Help is the last view of the registry. On All projects it is last
  among the views with an overview. (Today the test asserts that Help follows the Inbox; it is
  rewritten.)
- `tests/test_board_inbox_design.py`: `inbox` is still the second view; `nav.inbox` is
  "Notifications" in `en.js`, and has its French word in `fr.js`.
- `tests/test_board_history_client.py`: the `history` entry has an overview (the assertion
  `"overview" not in entry` is reversed); the filter words exist in both languages.
- A test that the registry has no `kanban` view, that `js/views/kanban.js` and
  `css/views/kanban.css` are gone and not linked from `index.html`, that no `go: 'kanban'` or
  `data-go="kanban"` remains, and that `batch-kanban.js` and `kanban-cards.js` are still there.
- `tests/test_board_griller_client.py`: the constant exists in the shipped `js/panel/griller.js` and is
  off. With it off, `grillAction` draws no `data-grill` button. The server's Griller tests are
  unchanged and pass.
- `tests/test_board_design.py` passes with the new colour token in both `tokens.css` and
  `DESIGN.md`'s table. No literal colour is added to a sheet.
- The panel backdrop: a test reads `js/main.js` (or the module that draws the layer) and checks that
  a click on the backdrop goes through `confirmLeave()` before `closePanel()`.
- `tests/test_board_history.py`: on a prepared surface of two projects, the all-projects `history`
  answer holds the events of both, each with its `project`. Its totals are the sum of the two
  projects' answers for the same period, and a project's answer is unchanged.
- The open-PR rows: on a prepared surface of two projects, each with a batch, the rows hold every
  open PR of both batches, each with one of the three states. A CR ready to merge with a
  `checks-red@1` line after its last hand-back reads red CI, and the same CR with no such line
  reads ready to merge. A test with no `gh` or `glab` on the path (the existing fake forge
  fixtures) shows that building the rows calls no forge.
- The feed: on the same surface, the feed holds the 20 newest events of the two projects' History
  indexes, newest first.
- Public key: `tests/test_board_read_key.py` or `test_board_exposure.py` shows that the public key
  still reads no cost or round of an event, through whatever topic or field carries the new data.
- `just check` passes on Linux, macOS and Windows; `just eval-dry-run` is owed for a change under
  the CLI's `src/` (`AGENTS.md`).
- `just scenario`: the long gate is owed for a change to the CLI's code (`AGENTS.md`); no scenario
  step is added (the scenario has no browser).
- The PR's Deliverables hold screenshots of a real board at the PR's head. Each is captioned with
  the head's SHA (seven characters):
  - the All-projects home with its two new blocks;
  - the All-projects History with its filters;
  - the menu on a project, ending with Configuration and then Help;
  - an open panel over the dimmed page;
  - the leave dialog after a click on the dimmed page with an unsaved edit.
  
  This CR does not change the CR board pane of `hooks/register.tsx`, so no session-pane screenshot
  is owed.

### Matrix: the Grill constant

- Constant off (as shipped): no Grill button in any panel; the server's Griller is untouched.
- Constant on (edited in the client, then released): the button and the discussion behave exactly as today.

No other part of this CR depends on the host or on a configured value.

## Open questions

None: web-board-Q5, Q6 and Q7 answered the three this spec first raised.

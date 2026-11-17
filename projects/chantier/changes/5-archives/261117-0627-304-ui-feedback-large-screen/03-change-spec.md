# Change Specification: the web board on a large screen

No issue.

## Goal

The user looked at `chantier board` on a large screen (about 2900 CSS pixels wide) and filed five
screenshots, kept in this CR's folder. Their reading, confirmed by the user on 2026-11-16
(`intake/request.md`, `02-answers.md` Q2, Q3), gives this CR four points and a fifth fix:

1. The side panel of a CR stays open when the user switches view (Kanban to Home)
   (`sidepanel-not-closing-when-switching-view.png`).
2. Hovering a card in a Triage lane (P1 in the screenshot) makes a horizontal scroll bar appear at
   the bottom of the lane (`triage-hovering-create-scrollbar.png`).
3. In Triage the backlog cards take the whole width of the screen, far wider than the cards of the
   other pages (`triage-cell-very-large-compared-to-other-pages.png`). The user chose (Q6) to cap
   the Triage cards and to lay the backlog out as a grid of several capped cards per row, as the
   inbox item `board-triage-polish` asked ("the items in the middle column are too wide: give them
   the same width as in the Inbox column, several per row (a grid)"); that item no longer owns it.
3b. A card's text shows the raw frontmatter (`--- type: cr-intent id: ...`) instead of the text
   (same screenshot).
4. The side panel is too narrow on a large screen: its content (a table in a round's file) is
   compressed and overflows (`compressed-sidepanel.png`).

The fifth screenshot's point, the surface in the selector and each project's paths
(`home-multiproject.png`, Q1, Q4, Q5), is its own CR, `2-backlog/P1/board-surface-selector`
(Q7): nothing of it is done here.

Apart from points 1, 3 and 3b, the board stays as it is on a laptop (the docs' 1400 x 860 size) and
on a phone (375 x 812).

## Where the code is

The board's server and front-end are in the CLI package,
`skills/chantier/scripts/cli/src/chantier/board/` (below: `board/`); the front-end is
`board/web/` (plain ES modules and CSS, no build step). Tests: `skills/chantier/scripts/cli/tests/test_board.py`
and the others under `skills/chantier/scripts/cli/tests/`. Docs: `docs/web-board.md`, its pictures
`docs/web-board/*.png`, taken by `just docs-screenshots` (`scripts/docs_screenshots.py`, Playwright,
on the made-up surface `docs/demo/`, at 1400 x 860 and 375 x 812).

## What changes

### 1. The side panel closes when the view changes

Today `board/web/js/core/router.js` resets the page's state (`reset`, which holds `panel: null`)
only when the project changes (`apply`, `moved`); a change of view keeps `panel`, `panelTree`,
`panelFile` and `editing`, so the panel stays open over the new view.

After the change, any change of view closes the panel, whatever started it: the left bar
(`[data-view]`), the phone's bottom bar, a link to a view (`[data-go]`, e.g. Home's "see the batch"),
and the browser's back and forward buttons (`listen`, `popstate`). Closing is what `closePanel()`
in `board/web/js/panel/panel.js` does (panel, tree, file and editor emptied). A change that stays on
the same view (a live refresh, a click on another card of the same view) does not close it.

Unsaved edits keep their protection: the view change already asks `confirmLeave()` first
(`guarded` in `board/web/js/main.js`, `guardLeave` for back/forward); a refused leave keeps both
the view and the open panel. The focus rule of `afterPanel` (the focus goes back to what opened
the panel) does not throw or move the page when that element is not in the new view.

### 2. Hovering a Triage card makes no scroll bar appear

A Triage card (`.pi`, `board/web/css/views/postit.css`) tilts and lifts under the pointer
(`.pi:hover { transform: rotate(-0.6deg); box-shadow: ... }`). The user kept this effect on
2026-11-14 ("l'effet pour prendre une carte est sympa je garde", CR 262): it stays. Today the
rotated card overflows its scrolling container (`.tbody`, `.lanes` in
`board/web/css/views/triage.css`, both `overflow: auto`), which then shows a horizontal scroll bar.

After the change, hovering, focusing, selecting or dragging a card shows no horizontal scroll bar
in the inbox column, in any backlog lane (P1 to P4), in 3-ready, or in the lanes' column, at any
window width, with one card or several per row (point 3); the tilt and the shadow are still seen,
not clipped visibly. The vertical scrolling of a column or of the lanes is unchanged. The phone's
horizontal swipe between the three columns (`.tri` under 760 px) is not a hover scroll bar and
stays.

### 3. Triage cards are capped, and the backlog is a grid

Today `.tri` lays the three columns out as `minmax(0, 1fr) minmax(0, 1.6fr) minmax(0, 1fr)`, and
each column's body (`.tbody`) is a single flex column of cards, so a card is as wide as its column:
on a 2900-pixel window a backlog card is well over 1000 pixels wide, while a Kanban card sits in a
290-pixel column (`.kanban .col { flex: 0 0 290px }`, `board/web/css/views/kanban.css`). The markup
is drawn by `column`, `body` and `lanes` in `board/web/js/triage/columns.js`.

After the change (answer Q6):

- **One card width.** Every Triage card (inbox, P1 to P4, 3-ready) has the same width, a fixed cap
  of the same order as a Kanban card (the Driver picks it, no narrower than a Kanban card and no
  wider than about one and a half Kanban columns, and says it in the PR). This is "the same width
  as in the Inbox column": the inbox column and 3-ready hold one card per row, the width of that
  card. Where a column is narrower than the cap (a narrow window, a phone), a card takes the
  column's width, as today.
- **The backlog is a grid.** In each backlog lane (P1 to P4) the cards are laid out side by side,
  as many capped cards per row as the lane's width holds, then on the next row; the order of the
  cards is the order of today, read left to right then top to bottom. The backlog column takes the
  width the window has beyond the inbox and 3-ready columns, so a large screen shows several cards
  per row and the space is used, not left empty; on a laptop (1400 pixels) a lane shows as many
  capped cards as fit (one or two), which is the user's request, not a regression.
- **Groups and the drop zone.** A group's frame (`.grpf`, `frame` in `columns.js`) keeps its
  members together under its handle, inside the lane's grid (its members capped like any card); the
  Driver chooses whether the frame spans a full row or sits as one cell, and says it in the PR. A
  lane's drop zone (`.dropzone`) and an empty lane's thin strip stay where they are today, never a
  single narrow cell that is hard to hit.
- **Unchanged behaviour.** Dragging a card or a group onto a lane, a card or a group's frame
  (`board/web/js/triage/drag.js`), selecting cards and the selection bar, the labels' filter and
  the lanes' vertical scrolling work as today, whatever the number of cards per row.
- **Phone.** Under 760 pixels the three columns keep their 86% swipe and a lane shows one card per
  row.

`docs/web-board.md`'s Triage section gains one sentence: on a wide screen each priority shows its
post-its side by side, as many per row as fit, each the width of an inbox post-it.

### 3b. A card's text never shows a frontmatter

A card's text is the item's `description`, computed by the server in `board/backlog.py`
(`description`, `_first_paragraph`): the first paragraph of `03-change-spec.md`, else
`01-intent.md`, else another Markdown file of the folder or `intake/`. A file that starts with a
YAML frontmatter (`---` on the first line, up to the next `---` line) gives today its frontmatter as
the "first paragraph", hence `--- type: cr-intent id: ... description: ...` on the card.

After the change, a frontmatter at the very start of a file is skipped before the first paragraph
is looked for; the paragraph after it is the description, cut at 300 characters as today. A file
with only a frontmatter and headings gives no paragraph, and the next candidate file is read, as for
an empty file today. A `---` further down a file (a Markdown rule) is not a frontmatter and is
handled as today. A byte-order mark or CRLF line ends before or in the frontmatter do not stop it
being skipped. This is the same `description` that the Kanban cards, Home's backlog and the CR rows
(`board/crs.py`) show: they are fixed with it.

### 4. The side panel is wide enough on a large screen

Today the panel's width is `min(var(--panel-width), calc(100% - 28px))` with `--panel-width:
680px` (`board/web/css/components.css`, `board/web/css/tokens.css`), and its body is a 210-pixel
tree plus the file (`.panel .pbody`, `board/web/css/panel.css`). On a 2900-pixel window the file
column is about 450 pixels; a round file's table is squeezed and runs out of its column.

After the change:

- On a wide window the panel grows with the window (a share of its width), so that the file column
  reads a round's file without squeezing; it keeps its 680 pixels as a floor and keeps the 14-pixel
  margin on the left of the page. On a laptop (1400 pixels) it is not narrower than today; on a
  phone it stays full screen.
- A table, a code block or a long line in the file never runs out of the file column: the file
  column, or the table itself, scrolls sideways when its content is wider than the column, and the
  page behind never does. Table cells are not squeezed to a word per line while the panel has room.
- The tree keeps its width.

The panel stays an overlay above the view, as today; a panel the user resizes by dragging is not
part of this CR.

### Docs pictures

`just docs-screenshots` is run again and its changed pictures committed: at least `triage-pc.png`
(capped cards, the grid) and those whose cards show a description from a file with a frontmatter,
if the demo has one. `picker-*.png` and `home-*.png` are not this CR's (they change with
`board-surface-selector`); a picture this CR does not change is not committed.

The pane drawn by `hooks/register.tsx` and `STATUS.json` do not change: no pane screenshot is due.

## Out of scope

- The surface in the picker, the overview's title and each project's two paths, with their
  `/api/board` fields, docs and pictures: the CR `board-surface-selector`.
- The other points of the inbox item `board-triage-polish` (a collapse per priority, the "writes
  since your last 'rescan'" explanation, the sticky header's border and shadow); its card width and
  grid are done here.
- Any other change to the board's look (the visual refresh is its own inbox item,
  `board-visual-refresh`).
- A resizable side panel, a panel docked beside the view instead of over it.
- More Triage columns, or a change to the order or meaning of the lanes.
- A new screenshot size in `scripts/docs_screenshots.py` (the large-screen checks below are the
  Driver's evidence, not docs pictures).
- The Kanban, Batch, Costs and Home views, apart from points 1 and 3b as they reach them.
- Any write by the board, any change to the autosync or the key.

## Evidence

Checks, before the PR:

- `just check` passes (Linux, macOS, Windows, as `AGENTS.md` asks).
- A parametrized test in `skills/chantier/scripts/cli/tests/` on `description()` (`board/backlog.py`)
  over a prepared folder: a file with a frontmatter then a paragraph gives the paragraph; the same
  with a byte-order mark and with CRLF line ends; a file with only a frontmatter falls through to
  the next candidate; a `---` rule lower in a file is not skipped as a frontmatter; a file with no
  frontmatter gives what it gives today. The test fails on today's code for the frontmatter cases.
  Kept within `just test`'s time budget (`AGENTS.md`).
- `just scenario` passes, and the pipeline's `just scenario (ubuntu-latest)` job is green at the
  PR's head (the board is part of the CLI package).
- `just docs-screenshots` run and its changed pictures committed.

Browser checks, by the Driver or the QA, on the live board (`uv run --no-sync --project <checkout>
chantier board` over a copy of `docs/demo/` with at least six items in one priority, one group of
two in a lane, one item whose `01-intent.md` starts with a frontmatter, and one CR folder whose
round file holds a wide table), at 2560 x 1440, at 2940 x 1280, at 1400 x 860 and at 375 x 812,
each with a screenshot in the PR's evidence:

1. Open a CR's panel on Kanban, then go to Home by the left bar: the panel is closed. Again with
   Home's "see the batch" link and with the browser's back button. Open a file for edit, change it,
   then click another view: the board asks; on "stay", the view and the panel with the edit are
   still there.
2. On Triage, hover each card of a lane holding several cards per row, then of the inbox and of
   3-ready: no horizontal scroll bar appears; the card still tilts.
3. On Triage at 2940 pixels: every card, inbox, backlog and 3-ready, is the width the PR names;
   the priority with six items shows several cards per row, in today's order; the group's members
   stay together in their frame. At 1400 pixels a backlog card is the inbox card's width. On a
   phone the swipe and one card per row remain.
4. On Triage at 2940 pixels: drag a card from the inbox to the middle of a full P1 row, onto
   another card (a group is made), and a group by its handle to P2: each lands as on `main`.
5. The item with a frontmatter shows its first paragraph on Triage, Kanban and Home, never `---`.
6. The wide table's round file in the panel at 2560 and 2940 pixels: the table is readable, its
   cells are not one word per line, and nothing runs past the panel's edge; at 1400 pixels the panel
   is not narrower than on `main`; on a phone it is full screen.

## Open questions

None: Q6 and Q7 of `02-answers.md` are carried above; the first run's Q4 and Q5 belong to
`board-surface-selector`.

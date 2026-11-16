# Change Specification: the web board on a large screen

No issue.

## Goal

The user looked at `chantier board` on a large screen (about 2900 CSS pixels wide) and filed five
screenshots, kept in this CR's folder. Their reading, confirmed by the user on 2026-11-16
(`intake/request.md`, `02-answers.md`), is the whole request:

1. The side panel of a CR stays open when the user switches view (Kanban to Home)
   (`sidepanel-not-closing-when-switching-view.png`).
2. Hovering a card in a Triage lane (P1 in the screenshot) makes a horizontal scroll bar appear at
   the bottom of the lane (`triage-hovering-create-scrollbar.png`).
3. In Triage the backlog cards take the whole width of the screen, far wider than the cards of the
   other pages; and a card's text shows the raw frontmatter (`--- type: cr-intent id: ...`)
   instead of the text (`triage-cell-very-large-compared-to-other-pages.png`).
4. The side panel is too narrow on a large screen: its content (a table in a round's file) is
   compressed and overflows (`compressed-sidepanel.png`).
5. On a multi-project planning surface, the selector at the top left shows the surface (its name and
   its path) instead of "All projects", and each project's line shows where the project is
   declared, its path (`home-multiproject.png`; the user's note: "Missing: where the project has
   been stated (path); model in project (no need to display 'all project') /
   multi-project-surface").

The board stays as it is on a laptop (the docs' 1400 x 860 size) and on a phone (375 x 812), apart
from point 5, which shows on every size.

## Where the code is

The board's server and front-end are in the CLI package,
`skills/chantier/scripts/cli/src/chantier/board/` (below: `board/`); the front-end is
`board/web/` (plain ES modules and CSS, no build step). Tests: `skills/chantier/scripts/cli/tests/test_board.py`
and the others under `skills/chantier/scripts/cli/tests/`. Docs: `docs/web-board.md`, its pictures
`docs/web-board/*.png`, taken by `just docs-screenshots` (`scripts/docs_screenshots.py`, Playwright,
on the made-up surface `docs/demo/`).

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
window width; the tilt and the shadow are still seen, not clipped visibly. The vertical scrolling
of a column or of the lanes is unchanged. The phone's horizontal swipe between the three columns
(`.tri` under 760 px) is not a hover scroll bar and stays.

### 3a. Triage cards keep the width of the other pages' cards

Today `.tri` lays the three columns out as `minmax(0, 1fr) minmax(0, 1.6fr) minmax(0, 1fr)`, so on
a 2900-pixel window a backlog card is well over 1000 pixels wide, while a Kanban card sits in a
290-pixel column (`.kanban .col { flex: 0 0 290px }`, `board/web/css/views/kanban.css`).

After the change, on a wide window a Triage card is no wider than a fixed cap of the same order as
a Kanban card (the Driver picks the cap, no wider than about one and a half Kanban columns, and
says it in the PR); the space the columns no longer take stays empty on the right of the view,
the three columns keep their order and their left alignment. On a laptop (1400 pixels) the view
does not change in a visible way: a card there is already under the cap, or close to it. On a
phone the columns keep their 86% swipe.

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

### 5. The multi-project surface in the selector, and each project's paths

This applies when the board serves a planning surface with several projects (`Projects.surface_mode`
in `board/projects.py` and more than one project; that is when the picker has an "All projects"
entry today, `canPick` in `board/web/js/ui/picker.js`). A single project, in-project or on a surface,
shows no change.

Today the picker's button (`trigger`) and its menu's first line (`menu`) say "All projects" with
"overview · N PRs to review" (`project.all`, `project.all_sub` in `board/web/js/i18n/en.js` and
`fr.js`), and the view's title says "All projects" too (`title` in `board/web/js/ui/header.js`,
`nav.overview`). The menu opens with the caption "Planning surface · N projects" (`project.head`).
The project lines (the menu's `row`, the overview table's `row` and the phone's `card` in
`board/web/js/views/overview.js`) show the project's name, batch and counts, but not where the
project is.

After the change:

- The surface takes the place of "All projects". The picker's button, when the overview is shown,
  shows the surface's name (the name of the surface's root folder) in bold, the surface's path under
  it, and under those the line "Planning surface · N projects" (`project.head`, N the number of
  projects), on the button itself, without opening the menu (answer Q5). This line takes the place
  of "overview · N PRs to review". The menu's first line shows the surface's name in bold and its
  path under it; the menu's caption "Planning surface · N projects" stays at the top of the menu, as
  today. The view's title on the overview is the surface's name. The words "All projects" and
  "overview · N PRs to review" no longer show anywhere in the board (button, menu, title). The
  number of PRs to review stays in the overview's stats line (`overall` in `header.js`), where it
  already is.
- Each project's line shows where the project is declared, by two paths (answer Q4):
  - its folder in the surface, `projects/<name>/`, relative to the surface the selector shows;
  - its code repository as the project's `checkout.yml` names it: the `repo:` value as written
    there (e.g. `../../../chantier/`); with no `repo:` line, the value the CLI takes by default,
    `.repo` (`Repo._external` in `skills/chantier/scripts/cli/src/chantier/core/repo.py`).
  The folder comes first, the repository after it, each labelled so the user tells them apart
  (e.g. "folder" and "repo", in both languages). The menu's lines, the overview table's lines (under
  the project's name, in the Project column) and the phone's cards show both.
- A path too long for its place is cut with an ellipsis and shown whole on hover (a `title`); it
  never widens the left bar or the table's first column beyond what they take today.
- The surface's mark (the overview icon, `.mark.all`) stays as it is.
- Both languages: the French board says the same things (`fr.js`); the words removed from `en.js`
  are removed from `fr.js` too.

The server gives what the page needs to draw this, in `GET /api/board` (`board()` in
`board/routes.py`): it already gives the surface's root as `served` (on a surface,
`Projects.served` is the surface's root); each project's line (`project_line` in `board/state.py`,
or `board()` around it) gains the two paths: the folder relative to the surface (from
`Repo.project_dir` and `Repo.surface`), and the `repo:` value of `checkout.yml` as written. `Repo`
keeps only the resolved repository (`root`), so the server reads the written value with
`read_keyed` (`core/repo.py`), read-only. Nothing else is added to the payload; the per-project
`state` endpoint does not change. The board still reads only and writes nothing new.

`docs/web-board.md` says "A planning surface with several projects adds an **All projects** entry to
the picker" and "Home is the table of **All projects**": these sentences, and every other
mention of All projects there, say instead that the picker's first entry is the surface, by its name
and path with "Planning surface · N projects" under them, and that each project's line shows its
folder in the surface and its code repository as `checkout.yml` names it.

### Docs pictures

`just docs-screenshots` is run again and its new pictures committed: at least `picker-pc.png`,
`picker-phone.png`, `home-pc.png`, `home-phone.png`, `triage-pc.png`, `panel-pc.png` change. The
script copies `docs/demo/` to a temporary folder; with point 5 the pictures would show that
folder's path, which differs on each run and on each machine. The pictures show a stable surface
name and path that reveal nothing of the machine that took them (the Driver chooses how, in
`scripts/docs_screenshots.py`, and says it in the PR); taking the pictures twice gives the same
surface name and path in them. The projects' paths are relative or as written in `checkout.yml`,
so they are the same on every run already; if a demo project has a `checkout.yml`, its `repo:`
value names nothing of the machine.

The pane drawn by `hooks/register.tsx` and `STATUS.json` do not change: no pane screenshot is due.

## Out of scope

- Any other change to the board's look (the visual refresh is its own inbox item,
  `board-visual-refresh`; the Triage polish is `board-triage-polish`).
- A resizable side panel, a panel docked beside the view instead of over it.
- Using the extra width of a large screen to show several Triage cards per row, or more columns.
- A new screenshot size in `scripts/docs_screenshots.py` (the large-screen checks below are the
  Driver's evidence, not docs pictures).
- The Kanban, Batch, Costs and Home views, apart from points 1, 3b and 5 as they reach them.
- Showing the repository's resolved or absolute path, or checking that it exists.
- Any write by the board, any change to the autosync or the key.

## Evidence

Checks, before the PR:

- `just check` passes (Linux, macOS, Windows, as `AGENTS.md` asks).
- A parametrized test in `skills/chantier/scripts/cli/tests/` on `description()` (`board/backlog.py`)
  over a prepared folder: a file with a frontmatter then a paragraph gives the paragraph; the same
  with a byte-order mark and with CRLF line ends; a file with only a frontmatter falls through to
  the next candidate; a `---` rule lower in a file is not skipped as a frontmatter; a file with no
  frontmatter gives what it gives today. The test fails on today's code for the frontmatter cases.
- A test that `GET /api/board` on a prepared surface of two projects gives the surface's root and,
  for each project, its folder (`projects/<name>/`) and its `repo:` value as written, one project
  with a `repo:` line and one without (which gives `.repo`); and on a single in-project folder gives
  what it gives today. Kept within `just test`'s time budget (`AGENTS.md`).
- `just scenario` passes, and the pipeline's `just scenario (ubuntu-latest)` job is green at the
  PR's head (the board is part of the CLI package).
- `just docs-screenshots` run, its pictures committed, and run a second time with no change in the
  surface name or path, or the projects' paths, they show.

Browser checks, by the Driver or the QA, on the live board (`uv run --no-sync --project <checkout>
chantier board` over a surface of several projects, such as a copy of `docs/demo/`, with one item
whose `01-intent.md` starts with a frontmatter and one CR folder whose round file holds a wide
table), at 2560 x 1440, at 2940 x 1280, at 1400 x 860 and at 375 x 812, each with a screenshot in the
PR's evidence:

1. Open a CR's panel on Kanban, then go to Home by the left bar: the panel is closed. Again with
   Home's "see the batch" link and with the browser's back button. Open a file for edit, change it,
   then click another view: the board asks; on "stay", the view and the panel with the edit are
   still there.
2. On Triage, hover each card of a lane holding several cards, then of the inbox and of 3-ready: no
   horizontal scroll bar appears; the card still tilts.
3. On Triage at 2940 pixels, a backlog card is no wider than the cap the PR names; at 1400 pixels,
   the view looks as on `main` (side by side screenshots).
4. The item with a frontmatter shows its first paragraph on Triage, Kanban and Home, never `---`.
5. The wide table's round file in the panel at 2560 and 2940 pixels: the table is readable, its
   cells are not one word per line, and nothing runs past the panel's edge; at 1400 pixels the panel
   is not narrower than on `main`; on a phone it is full screen.
6. The picker's button, menu closed, shows the surface's name, its path and "Planning surface · N
   projects", never "All projects", in English and in French; the menu's first line shows the
   surface's name and path; the overview's title is the surface's name; each project's line, in the
   menu, in the table and on the phone's cards, shows its folder in the surface and its repository
   as `checkout.yml` names it; a long path is cut and shown whole on hover.
7. A board on a single project (in-project) shows no picker change and no path.

## Open questions

None: the first run's two questions are answered in `02-answers.md` (Q4, Q5) and carried above.

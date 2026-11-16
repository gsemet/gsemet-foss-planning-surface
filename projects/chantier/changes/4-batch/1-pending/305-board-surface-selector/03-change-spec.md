# Change Specification: the web board's selector shows the surface, and each project its paths

No issue.

## Goal

Split from `ui-feedback-large-screen` on 2026-11-16 (its `02-answers.md`, Q7, the user's choice).
This CR's grill is that CR's `02-answers.md`: Q1, Q4 and Q5
(`2-backlog/P1/ui-feedback-large-screen/02-answers.md`); its screenshot is `home-multiproject.png`
in that CR's folder, with the user's note: "Missing: where the project has been stated (path); model
in project (no need to display 'all project') / multi-project-surface".

On a planning surface with several projects, the selector at the top left of `chantier board` shows
the surface (its name and its path) instead of "All projects" (Q1), with "Planning surface · N
projects" under them without opening the menu (Q5); and each project's line shows where the project
is declared, by two paths: its folder in the surface and its code repository as `checkout.yml`
names it (Q4). This shows on every window size.

## Where the code is

The board's server and front-end are in the CLI package,
`skills/chantier/scripts/cli/src/chantier/board/` (below: `board/`); the front-end is
`board/web/` (plain ES modules and CSS, no build step). Tests: `skills/chantier/scripts/cli/tests/test_board.py`
and the others under `skills/chantier/scripts/cli/tests/`. Docs: `docs/web-board.md`, its pictures
`docs/web-board/*.png`, taken by `just docs-screenshots` (`scripts/docs_screenshots.py`, Playwright,
on the made-up surface `docs/demo/`, three projects `docs-portal`, `mobile-app`, `shop-api`, each
with a `checkout.yml` of `repo: .repo`).

## When it applies

When the board serves a planning surface with several projects (`Projects.surface_mode` in
`board/projects.py` and more than one project; that is when the picker has an "All projects" entry
today, `canPick` in `board/web/js/ui/picker.js`). A single project, in-project or on a surface,
shows no change.

## What changes

### The surface takes the place of "All projects"

Today the picker's button (`trigger`) and its menu's first line (`menu`) say "All projects" with
"overview · N PRs to review" (`project.all`, `project.all_sub` in `board/web/js/i18n/en.js` and
`fr.js`), and the view's title says "All projects" too (`title` in `board/web/js/ui/header.js`,
`nav.overview`). The menu opens with the caption "Planning surface · N projects" (`project.head`).

After the change:

- The picker's button, when the overview is shown, shows the surface's name (the name of the
  surface's root folder) in bold, the surface's path under it, and under those the line "Planning
  surface · N projects" (`project.head`, N the number of projects), on the button itself, without
  opening the menu (Q5). This line takes the place of "overview · N PRs to review".
- The menu's first line shows the surface's name in bold and its path under it; the menu's caption
  "Planning surface · N projects" stays at the top of the menu, as today.
- The view's title on the overview is the surface's name.
- The words "All projects" and "overview · N PRs to review" no longer show anywhere in the board
  (button, menu, title). The number of PRs to review stays in the overview's stats line (`overall`
  in `header.js`), where it already is.
- The surface's mark (the overview icon, `.mark.all`) stays as it is.

### Each project's line shows its two paths

The project lines (the menu's `row` in `picker.js`, the overview table's `row` and the phone's
`card` in `board/web/js/views/overview.js`) show today the project's name, batch and counts, but not
where the project is. After the change each shows where the project is declared, by two paths (Q4):

- its folder in the surface, `projects/<name>/`, relative to the surface the selector shows;
- its code repository as the project's `checkout.yml` names it: the `repo:` value as written there
  (e.g. `../../../chantier/`); with no `repo:` line, the value the CLI takes by default, `.repo`
  (`Repo._external` in `skills/chantier/scripts/cli/src/chantier/core/repo.py`).

The folder comes first, the repository after it, each labelled so the user tells them apart (e.g.
"folder" and "repo", in both languages). The menu's lines, the overview table's lines (under the
project's name, in the Project column) and the phone's cards show both.

A path too long for its place is cut with an ellipsis and shown whole on hover (a `title`); it
never widens the left bar or the table's first column beyond what they take today.

### Both languages

The French board says the same things (`fr.js`); the words removed from `en.js` are removed from
`fr.js` too.

### The server

The server gives what the page needs, in `GET /api/board` (`board()` in `board/routes.py`): it
already gives the surface's root as `served` (on a surface, `Projects.served` is the surface's
root); each project's line (`project_line` in `board/state.py`, or `board()` around it) gains the
two paths: the folder relative to the surface (from `Repo.project_dir` and `Repo.surface`), and the
`repo:` value of `checkout.yml` as written. `Repo` keeps only the resolved repository (`root`), so
the server reads the written value with `read_keyed` (`core/repo.py`), read-only. Nothing else is
added to the payload; the per-project `state` endpoint does not change. The board still reads only
and writes nothing new.

### Docs

`docs/web-board.md` says "A planning surface with several projects adds an **All projects** entry to
the picker", has a section titled "Home: all projects", and says "Home is the table of **All
projects**", "All projects is read-only", "never in All projects" (the editor) and "All projects and
a running batch's CRs are never written" (Triage), and once more near its end. Each mention says
instead that the picker's first entry is the surface, by its name and path with "Planning surface ·
N projects" under them, and, where it describes the overview, that each project's line shows its
folder in the surface and its code repository as `checkout.yml` names it. The pictures' alt texts
that say "All projects" follow.

### Docs pictures

`just docs-screenshots` is run again and its changed pictures committed: at least `picker-pc.png`,
`picker-phone.png`, `home-pc.png`, `home-phone.png`. The script copies `docs/demo/` to a temporary
folder; with this change the pictures would show that folder's path, which differs on each run and
on each machine. The pictures show a stable surface name and path that reveal nothing of the machine
that took them (the Driver chooses how, in `scripts/docs_screenshots.py`, and says it in the PR);
taking the pictures twice gives the same surface name and path in them. The projects' paths are
relative or as written in `checkout.yml` (`.repo` in the demo), so they are the same on every run
already.

The pane drawn by `hooks/register.tsx` and `STATUS.json` do not change: no pane screenshot is due.

## Out of scope

- The large-screen fixes and the raw frontmatter in a card's preview: the CR
  `ui-feedback-large-screen`.
- Showing the repository's resolved or absolute path, or checking that it exists.
- The worktrees' path (`worktrees:` of `checkout.yml`).
- A change to a single-project board, in-project or on a surface.
- Any other change to the board's look, any write by the board, any change to the autosync or the
  key.

## Evidence

Checks, before the PR:

- `just check` passes (Linux, macOS, Windows, as `AGENTS.md` asks).
- A test that `GET /api/board` on a prepared surface of two projects gives the surface's root and,
  for each project, its folder (`projects/<name>/`) and its `repo:` value as written, one project
  with a `repo:` line and one without (which gives `.repo`); and on a single in-project folder gives
  what it gives today. Kept within `just test`'s time budget (`AGENTS.md`).
- `just scenario` passes, and the pipeline's `just scenario (ubuntu-latest)` job is green at the
  PR's head (the board is part of the CLI package).
- `just docs-screenshots` run, its pictures committed, and run a second time with no change in the
  surface name or path, or the projects' paths, they show.

Browser checks, by the Driver or the QA, on the live board (`uv run --no-sync --project <checkout>
chantier board` over a surface of several projects, such as a copy of `docs/demo/` with one
project's `checkout.yml` given a long `repo:` value and another's `repo:` line removed), at 1400 x 860
and at 375 x 812, each with a screenshot in the PR's evidence:

1. The picker's button, menu closed, shows the surface's name, its path and "Planning surface · N
   projects", never "All projects", in English and in French.
2. The menu's first line shows the surface's name and path; the overview's title is the surface's
   name.
3. Each project's line, in the menu, in the table and on the phone's cards, shows its folder in the
   surface and its repository as `checkout.yml` names it (`.repo` for the project with no `repo:`
   line); the long path is cut and shown whole on hover, and the left bar and the table's first
   column are no wider than on `main`.
4. A board on a single project (in-project) shows no picker change and no path.

## Open questions

None: Q1, Q4 and Q5 of `ui-feedback-large-screen/02-answers.md` are carried above.

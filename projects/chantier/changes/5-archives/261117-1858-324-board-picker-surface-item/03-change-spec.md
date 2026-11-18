---
type: cr-change-spec
description: Change Specification of board-picker-surface-item.
---

# Change Specification: the picker's planning-surface item

Origin: verbal (the user, 2026-11-17, with a screenshot). No issue.

## Goal

This CR changes the web board's project picker, shown when one planning surface holds several
projects:

1. **Bug.** A click on the planning surface's item opens the surface's overview ("All projects")
   from any page. Today it does nothing unless the board already shows Home. The user saw it on
   markdown-okf-schema-studio's Costs page.
2. **Look.** The surface item is the umbrella of the projects and must read as such. It becomes
   the menu's clickable header, set apart from the project items listed under it.

## The bug's cause

`js/main.js` handles a click on `[data-project]` with `go({ project: el.dataset.project })`.
`go` in `js/core/router.js` keeps the current view (`place.view ?? now.view`). Then `settle`
moves "All projects" (`ALL`, `'*'`) back to the last real project when the view has no overview.
Every view but `home` lacks one (see `overviewIds()` in `views/registry.js`). On Costs, Triage,
Kanban, Batch, PRs or Configuration, the click therefore lands where the page already is, and
nothing moves.

## What changes

### Routing: the picker's click only, in `js/main.js`

The switch to Home belongs to the click only. `go` is also called at boot
(`go(resolve(got.data.projects), { replace: true })` in `main.js`), so a rule inside `go` would
turn a typed `?p=*&v=costs`, or a saved `project` pref of `*`, into `?p=*&v=home`. The switch
therefore does not go in `go`.

`main.js`'s `[data-project]` handler changes. It still closes the menu (`update({ menu: false })`)
and calls `go` once. When `el.dataset.project === ALL` and the current view
(`snapshot().view`) is not in `overviewIds()` (already imported from `views/registry.js`), it
calls `go({ project: ALL, view: overviewIds()[0] })` (`home` today). Otherwise it calls
`go({ project: el.dataset.project })` as today. `ALL` is imported from `core/router.js` if
`main.js` does not import it already. The address then reads `?p=*&v=home` and the overview is
drawn.

What does not change:
- `js/core/router.js`: `go`, `settle` and `resolve` stay as they are. An address typed, restored
  at boot from the saved pref, or reached by back/forward (`?p=*&v=costs`) still opens the last
  real project on that view, as today.
- A project row (`data-project` set to a real project, in the menu or on the overview page), a
  sidebar view or a `data-go` link behaves as today. That includes a non-overview view asked while
  on "All projects": it moves to the last real project.
- The surface item keeps `data-project="*"` and gets no `data-view` or `data-go`. Those have their
  own click handlers in `main.js`, and one click must make one `go`.

Back after the jump returns to the page left (the `pushState` of `go` is kept).

### The menu: `js/ui/picker.js`, `menu(state)`

The menu draws, in this order:

1. **The surface header:** a `<button class="row sfc">` (with ` on` while "All projects" is
   shown), `type="button"`, `data-project="${ALL}"`, `role="menuitem"`. It holds:
   - the grid icon: the existing `<span class="mark all">${icon('overview')}</span>`;
   - its name, `surfaceName(state)`, in bold;
   - under the name, a grey line: `overview · <n> projects`, where `n` is the number of projects
     (`projectsOf(state).length`). This line uses a new word key (see Words below);
   - the check mark (`ok()`) at the right while "All projects" is shown, as today.
2. **A separator** below the header: a `<div class="sep" role="separator"></div>`, or the
   header's bottom border. It is one 1px line in `var(--line)`, with a few pixels of space on
   each side.
3. **The projects:** one `row(project, state)` each, drawn as today (mark, name, the batch's
   percent while one runs, the check mark on the current one). They are slightly indented: a left
   inset about one `var(--space-2)` larger than the header's, so the projects sit under it.

The caption `<div class="cap">` ("Planning surface · N projects") is removed. The header now names
the surface, and its grey line carries the count. Remove the `.menu .cap` rule in
`css/picker.css` too, since nothing else uses it today.

The sidebar (`ui/sidebar.js`, `projectSide`) and the phone's top bar (`main.js`,
`#project-phone`) share this menu, so both get the change. A single project draws no menu, as
today (`canPick`).

### The style: `css/picker.css`

- `.menu .sfc` is the header row. Its name (`.who > b`) is in the board's bold: weight 500, the
  heaviest weight the board ships (`css/fonts.css` has 400 and 500 only). Add no new font file
  and no faux bold. To keep the contrast, the project rows' names
  (`.menu .row:not(.sfc) .who > b`) go to weight 400. The header's grey line uses the existing
  `.menu small` rule (`var(--ink3)`, `var(--text-small)`).
- The separator is `border-top: 1px solid var(--line)` (or the header's `border-bottom`), with a
  small vertical margin.
- The project rows' indent is a larger `padding-left` on `.menu .row:not(.sfc)`.
- Both kinds of row keep the existing `.menu .row` rules for hover, `.on` and the check mark.
- Use tokens from `css/tokens.css` only; add no new colour.

### Words: `js/i18n/en.js` and `js/i18n/fr.js`

Add one new key to both files. The test
`test_the_web_frame_has_small_scripts_and_both_word_files_share_their_keys` requires both files to
hold the same keys.

- `en.js`: `'project.overview': 'overview · {n} projects'`
- `fr.js`: `'project.overview': "vue d'ensemble · {n} projets"`

`project.head` stays, because the trigger button (`trigger`) still uses it on "All projects".

### Docs: `docs/web-board.md`

Line 12 describes the picker's first entry ("by its name and its path, with 'Planning surface ·
N projects' under them"). Rewrite that sentence to say:
- the picker's menu opens with the planning surface as its header: the grid icon, its name in
  bold, and "overview · N projects" under it;
- a click on that header opens the overview from any page;
- a line follows, then the projects, slightly indented;
- a single project has no such header.

## Decisions carried from `02-answers.md`

- **scope-Q1:** the board feedback of 2026-11-17 is cut into four CRs, all in the next batch:
  board-picker-surface-item, board-batch-navigator, board-kanban-priority-colours (with
  board-pastel-colours folded in) and board-config-role-descriptions. This CR holds only the
  picker's surface item.
- **picker-Q5:** the surface becomes the menu's clickable header (grid icon, name in bold, grey
  line "overview · <n> projects"), above a separator. The projects are listed under it, slightly
  indented. The bug stays in scope: a click on the surface item opens the surface's overview from
  any page, not only from Home.

## Out of scope

- The picker's trigger button (`trigger`): its face, name and lines stay as they are, both on
  "All projects" and on a project.
- The overview page itself (`views/overview.js`) and the sidebar's views.
- The batch navigator, the Kanban colours and the Configuration's role descriptions: the other
  three CRs of scope-Q1.
- `core/router.js`, and what an address typed by hand, restored at boot or reached by
  back/forward resolves to.
- Retaking `docs/web-board/picker-pc.png` and `picker-phone.png`. The recipe says
  `just docs-screenshots` runs by hand before a release.
- Any change to the CLI's Python, the cards or the record.

## Evidence

- `just check` passes. It covers Biome on the web frame, the word files' shared keys, the
  300-line limit per script, ruff, mypy and the tests.
- The `just scenario (ubuntu-latest)` CI job is green at the PR's head, as the project's rules
  ask, because the web frame ships in the CLI package.
- A manual check in a browser. Record it in the PR's Deliverables with two screenshots of the open
  menu, one at PC width and one at phone width. Run `chantier board` on a planning surface with at
  least two projects, then check:
  1. On a project's Costs page, open the picker and click the surface header. The address becomes
     `?p=*&v=home` and the overview shows. Repeat from Triage, Kanban, Batch, PRs, Configuration
     and the project's Home, with the same result.
  2. Browser back returns to the page left (after step 1 on Costs, the project's Costs page).
  3. On the overview, the header carries the check mark and the `on` background. Picking a project
     opens it on Home and moves the check mark to that project.
  4. The menu reads, in order: the header (grid icon, the surface's name in bold, "overview · N
     projects" in grey), a line, then the projects, indented, with regular-weight names. In
     French, the grey line reads "vue d'ensemble · N projets".
  5. Unchanged behaviour: the address `?p=*&v=costs` typed by hand, or a reload of it, still opens
     the last real project's Costs. Choose the surface from Home, then open the board's bare
     address (`?` with no `p`, so the saved pref of `*` applies): it opens the overview on Home,
     as before.
  6. Unchanged behaviour: a surface with one project shows no menu.

## Open questions

None.

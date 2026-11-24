# Web board: Dashboard on All projects, chart hover band fixed

The Dashboard page also shows on "All projects". It draws the same graphs as a project's Dashboard,
summed over every project of the surface, one curve per graph. Hovering or focusing a point on any
Dashboard chart no longer hides the lines or bars under an opaque band.

## Goal

From the user, 2026-11-24, as the follow-up of CR-482 (`web-board-menu-home-history`, the
multi-project home, its feed and History):

1. Put "Dashboard" graphs at the root ("All projects"), for every project at once, built from the
   same graphs as a project's Dashboard. A project's own Dashboard keeps working.
2. Fix the bug the user saw when the mouse hovers a graph: a pale vertical band covers the chart
   and the curve disappears behind it.

Destination: running batch batch-31, after CR-482 (web-dashboard-Q2). The root pages (the
All-projects menu and its views) are CR-482's, so this CR is built on top of CR-482's result.

## Rules that bind this CR

- `AGENTS.md`: a change under `skills/chantier/scripts/cli/src/chantier/clients/web/` reads its
  `DESIGN.md` first and keeps it true. The `DESIGN.md` sections named below are edited in the same
  PR, so the file still describes the board as it ships.
- `DESIGN.md` rules apply to every new markup and sheet: tokens only (no literal colour in a sheet),
  no side accent border, the shared card, chip and chart components, one-line titles, every word an
  i18n key in both `en-*.js` and `fr-*.js`, and `js/core/transport.js` as the only transport.
- `DESIGN.md`, "Dashboard": the figures come from the server, computed from the closed batch
  records. The views compute no figure. One point per batch, never per day. A figure no record
  holds is no point, never a zero.
- No new forge read, and no write: the root Dashboard reads the closed batch records the server
  already reads for each project's Dashboard.
- No CLI command, card or agent file changes.

## What changes

### 1. The chart hover band (the bug)

**Reproduced from the code.** In `js/ui/chart.js`, `chart()` builds the plot as
`<div class="chart-plot"><svg class="chart-svg">…</svg><div class="chart-cols">…</div></div>`. In
`css/components/chart.css`, `.chart-svg` and `.chart-cols` are both `position: absolute; inset: 0`
with no `z-index`. So the columns, which come after the SVG in the markup, are painted **above**
the drawing. `.chart-col:hover, .chart-col:focus { background: var(--accent-tint); }` fills the
hovered or focused column with `--accent-tint` (`#e9f1f1` in `css/tokens.css`), a solid colour. The
result is an opaque band over the lines, the marks and the bars of that slot: what the user saw at
batch 24 of "CRs pris en charge et mergés". The band also stays after a click or a tap, because
`bindCharts` (`js/ui/chart-read.js`) focuses the clicked column and `:focus` keeps the fill.

This is the shared chart component, so every Dashboard chart has the bug. That covers the four
Productivity tiles (`js/views/dashboard-tiles.js`: CRs held and merged, rounds, duration as lines;
calls by part as stacked `chart-bar` rects) and the Spending tiles (`js/views/dashboard-spend.js`:
lines and stacked bars). In a stacked bar chart, the band hides the bar of the slot.

**The fix.** The highlight band is drawn **behind** the series: the drawing (`.chart-svg`) is
stacked above the columns. The columns keep catching the pointer, focus and taps, which they can
because `.chart-svg` already has `pointer-events: none`. With the band behind them, the lines, the
marks and the bars stay fully visible on the hovered or focused slot. The band keeps today's colour
token (`--accent-tint`), so no new token or colour is needed. The Driver chooses between reordering
the markup and giving the plot's two layers a stacking order in `chart.css`. Either way it is one
fix in the component, not a per-view override. The readout line (`.chart-read`), keyboard walking
(Left, Right, Home, End), the single tab stop and the `:focus-visible` outline keep working as
today.

- `DESIGN.md`, "Dashboard": the bullet "A value is read on hover, on focus and on a tap" gains that
  the read slot's band is drawn behind the series and never hides a line, a mark or a bar.

### 2. Dashboard on All projects (web-dashboard-Q1, answer A)

**The menu.** In `js/views/registry.js`, the `dashboard` entry gains an `overview`, so Dashboard
shows on All projects. With CR-482's order, the All-projects menu becomes Home, Notifications,
History, Dashboard, Help (the project's order, History … Dashboard … Help, kept). The phone's bottom
bar follows the registry. A project's menu does not change.

**What the page shows.** On All projects the page is the project's Dashboard page
(`js/views/dashboard.js`) with the same head: the Productivity and Spending tabs and the range
(last 10, last 20, all) in the address (`dt=`, `dr=`). It has the same tiles, the same chart
component, the same headlines and coverage lines. Each graph draws **one curve (or one stack) per
graph**, with the same series as a project's graph, whose value at each point is **the sum of the
projects for that batch** (web-dashboard-Q1). The page's words (`en-dashboard.js`,
`fr-dashboard.js`) gain only what the root page adds (below).

How each figure is summed, recorded defaults (each reads "the sum of the projects per batch"):

- **Points.** A point is a batch number. Its value sums the closed records of that number across
  every project of the surface. A project with no closed record of that number adds nothing. A point
  with no figure in any project is no point (a cut line, an empty bar slot), as today. The range
  keeps the newest batch numbers held by any project (the last 10, the last 20, or all), oldest
  first.
- **Counts and costs are summed**: CRs held and merged, model calls by part, spend by part and by
  model, the cost outside the batches, and the headline totals.
- **Ratios are pooled** so that they stay true ratios: rounds per merged CR is the mean over the
  merged CRs of every project at that batch number, and cost per merged CR is the summed cost over
  the summed merged CRs. Headlines are computed the same way over the range.
- **Duration** (a batch's minutes): see open question Q1, with its recorded default.
- **Models.** The Spending tab's model series are ranked by their summed cost over all the closed
  records of all projects (`board/dashboard_spend.py`'s `rank`, over the union). It keeps the
  `--m1` to `--m8` palette and "other models" beyond eight.
- **Most expensive CRs**: the ten most expensive CRs of the range across all projects. Each row also
  shows its project's mark (as CR-482's All-projects rows do). A row opens its CR's project, as
  CR-482's All-projects rows do (`data-project`).
- **The readout** of a point names its batch number and how many projects that point sums (for
  example "Batch 24, 3 projects: held 41, merged 38"), so a point that only one project holds is not
  read as a total of all. When the summed records were closed on different days, the readout shows
  no single day. The Driver may show the range of days.
- **Coverage** ("covers n of total") counts the batch numbers that hold the figure.
- **Unpriced** marks a point when any summed record is unpriced, as today for one record.

**The running batches.** On a project, the page's live line says the running or paused batch has no
point and links to Costs. On All projects, the line names each project with a running or paused
batch, each with a link to that project's Costs. There is no line when none has one.

**The per-project detail stays one click away** (web-dashboard-Q1). Under the head, one link per
project of the surface opens that project's Dashboard with the same tab and range. These are plain
links or the existing filter-toggle chips' look, with no new component.

**Empty and error states** are the project page's: the loading line, the error with the last good
answer kept, and "no closed batch" when no project has one.

**The server.** `dashboard.get` (`board/api/ops.py`'s `_dashboard`, `board/dashboard_page.py`'s
`answer`) also answers for all projects at once, by the same all-projects convention CR-482 sets for
the `history` topic. The Driver chooses between the same op with the all-projects value and a
sibling op. The answer has the same shape as a project's, plus the per-point project count and the
top rows' `project`. It is built from each project's closed records as `_dashboard` reads them
today (`reads.state_of(…)["history"]`), with nothing written and no forge call. `dashboard.get` is
in `READ_OPS` today (the public read-only key reads a project's Dashboard). The all-projects answer
stays on the same key and carries nothing a project's answer does not already carry.
`board/api/protocol.py` and `board/api/protocol.json` follow any new argument value, op or field.

**The feed.** `js/views/dashboard-feed.js` asks again on All projects when the range changes or any
project's closed records change (a batch closing, a record corrected afterwards). The Driver takes
the signal from what the All-projects state already carries, and adds a field to the `board`
topic's project line only if needed, without widening what the public key reads.

**A project's Dashboard** is unchanged, apart from the hover fix.

- `DESIGN.md`, "Dashboard": the page also shows on All projects, with one curve per graph summed
  over the projects per batch, counts summed and ratios pooled, the readout's project count, the
  per-project links and the project mark on the ranking's rows. There is no new token, component or
  colour.

### Docs

- `docs/web-board.md`: the Dashboard section says that the page also shows on All projects and how
  its figures are summed.
- `js/i18n/en-help.js` and `fr-help.js`: a Help topic that describes the Dashboard says it also
  shows on All projects.

## Out of scope

- Aligning the projects' batches by date (a time axis) instead of by batch number.
- One curve per project, or a choice of projects to sum (web-dashboard-Q1 chose one summed curve).
- Any change to a project's Dashboard figures, its tiles or its words, other than the hover fix.
- The Costs page and its protected features, the History page, and CR-482's home blocks.
- Any new forge read, and any change to the forge hub or its journal.
- The `live` terminal client (`clients/tui/`).

## Evidence

Every check below reads the shipped files of the web client and the server at the head under test,
as `tests/test_board_*.py` already do (the package's files read in place), never a prepared copy.

- **The hover band.** A test reads the shipped `css/components/chart.css` and `js/ui/chart.js` and
  checks that the drawing (`.chart-svg`) is stacked above the columns (`.chart-cols`), either by its
  place in the plot's markup or by an explicit stacking order in the sheet. It also checks that
  `.chart-svg` keeps `pointer-events: none`, and that the band's fill on `:hover` and `:focus` is a
  token (no literal colour). One test covers both chart kinds, since lines and bars share the plot.
- `tests/test_board_design.py` passes: no new token, and no literal colour in a sheet.
- `tests/test_board_dashboard.py`, on a prepared surface of two projects with closed records:
  - batch numbers held by both projects sum their counts and costs;
  - a batch number held by one project only is that project's value, with a project count of 1;
  - rounds per merged CR and cost per merged CR are pooled ratios, not sums of ratios;
  - the model rank is over both projects' records;
  - the top ten rows carry their `project`;
  - each project's own answer is unchanged;
  - an unknown range is still refused.
- A test with no `gh` or `glab` on the path (the existing fake forge fixtures) shows that the
  all-projects answer calls no forge.
- Public key: `tests/test_board_read_key.py` or `test_board_exposure.py` shows that the public key
  reads the all-projects Dashboard as it reads a project's, and no field a project's answer does not
  carry.
- A client test (beside `tests/test_board_history_client.py`): the `dashboard` registry entry has an
  `overview`, it sits between History and Help on All projects, and the new words exist in both
  `en-dashboard.js` and `fr-dashboard.js`.
- `just check` passes on Linux, macOS and Windows. `just eval-dry-run` is owed for a change under the
  CLI's `src/` (`AGENTS.md`).
- `just scenario`: the long gate is owed for a change to the CLI's code (`AGENTS.md`). No scenario
  step is added (the scenario has no browser).
- The PR's Deliverables hold screenshots of a real board at the PR's head, each captioned with the
  head's SHA (seven characters):
  - a project's "CRs pris en charge et mergés" chart hovered on a point, the line and its mark
    visible through the band;
  - a stacked bar chart ("Appels de modèle par partie") hovered, its bar visible;
  - the All-projects Dashboard on each tab, with the per-project links.
  
  This CR does not change the CR board pane of `hooks/register.tsx`, so no session-pane screenshot is
  owed.

No part of this CR depends on the host or on a configured value.

## Open questions

- **Q1. The duration graph on All projects.** A batch's duration (its minutes) does not add up
  across projects: two projects' batch 24 running side by side do not last the sum of the two. What
  should the root graph show at each batch number? Recorded default: the mean of the projects'
  durations at that batch number, with a headline median over all the projects' batches in the
  range. Other choices: the longest, or drop the duration tile on All projects.
- **Q2. Points by batch number (risk).** Batch numbers are each project's own. Batch 24 of chantier
  and batch 24 of another project may be weeks apart, so the summed point mixes different periods,
  and a young project only adds to the first points. The spec carries web-dashboard-Q1 as answered
  ("the sum of the projects per batch") and only names this. Confirm that alignment by batch number
  is wanted. A time axis, if wanted, is another CR.

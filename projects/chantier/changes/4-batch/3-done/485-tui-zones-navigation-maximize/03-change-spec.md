# TUI: Tab zones, per-panel scroll, newest first, narrow Ago, maximize

`chantier live` gets an active panel: Tab moves it from one box to the next, the arrows and Page
Up/Down scroll the active box, a key maximizes it and restores it. The Flow (the central box) shows
the newest line at the top, and its `Ago` column is narrow and right-aligned. It starts on the
Flow.

## Goal (the user's six rules, 2026-11-24)

1. Tab changes the active zone.
2. Up, Down, Page Up and Page Down navigate inside the active panel.
3. The main (central) zone, the Flow, is sorted newest first.
4. The relative time form exists to save space: the `Ago` column must be narrow, its width
   recomputed, the time right-aligned.
5. A shortcut maximizes the active panel, and the same shortcut restores it.
6. At start, the central panel (the Flow) is the active one.

Destination: the running batch batch-31, with no grill (`02-answers.md`, tui-Q1). The Chief of
Staff left two things to the agents: the maximize key (one not already bound) and the exact
time-column width.

## What exists today (read at main `3c29dd7c`)

All under `skills/chantier/scripts/cli/src/chantier/clients/tui/`:

- `view.py`: `View` holds the Flow's scroll (`anchor`, `gap`, `new`, `moves`), the filter
  (`text`, `typing`), `help`, `ago`, `keys`; `press(name, page)` maps key names; `window(lines,
  rows)` returns the lines to draw, **oldest first, the live end at the bottom**, and the title
  (`Flow` or `Flow  paused, <n> new`). `HELP` lists the keys. Only the Flow scrolls.
- `screen.py`: `render()` lays out the header, the body (left column `Projects` above `Agents`
  from `NARROW = 100` columns; `flow()` in the centre; `Ready` above `Tasks` on the right,
  `RIGHT_W = 44`), the footer (`KEYS_FOOTER = "? keys  / filter  t time  q quit"`). `flow()`
  uses one `TIME_W = 14` for both the clock form (`MM-DD HH:MM:SS`, 14 characters) and the `Ago`
  form. `key_name()` maps a `blessed` keystroke through `KEY_NAMES`; Tab (`"\t"`, `KEY_TAB`) maps
  to `""` today (unbound). `run()` passes `body_rows(models, height)` as the page of every move.
- `times.py`: `since(ts, now)` gives `<n> s`, `<n> min`, `<n> h`, `1 day`, `<n> days` (tested in
  `tests/test_live_ready.py::test_since_rounds_down_and_never_runs_backwards`).
- `ready.py`: the Ready box; `parts.py`: `panel()` (rounded box with a left title), `table()`,
  `grid()`, the widths `LEFT_W = 28`, `RIGHT_W = 44`.
- Tests: `skills/chantier/scripts/cli/tests/test_live_model.py` (keys, scroll, pause, filter,
  help, footer, `key_name`), `test_live_ready.py` (`since`, Ready, render).
- Doc: `docs/boards.md`, the `chantier live` section (the Flow "newest at the bottom", the Keys
  table, "Only the Flow scrolls").

## What changes

### 1. The active panel and Tab (rules 1 and 6)

- `View` gains the active panel, one of `projects`, `agents`, `flow`, `ready`, `tasks`; it starts
  on `flow`.
- Tab moves to the next drawn panel in reading order, wrapping: Projects, Agents, Flow, Ready,
  Tasks, then Projects again. Default added: Shift-Tab (`KEY_BTAB`) moves to the previous one. A
  panel not drawn is skipped: under 100 columns the left column is not drawn, so Tab cycles Flow,
  Ready, Tasks. When a resize hides the active panel, the active panel becomes the Flow.
- `key_name()` maps Tab to `tab` and Shift-Tab to `btab` (or names of the agent's choice); `press`
  takes them. While typing a filter, Tab and Shift-Tab do nothing (the filter takes single
  printable characters only, as today). With the help shown, any key closes it, Tab included, and
  does nothing else (as today).
- The active box is marked so that it reads without colour (the TUI's rule: no colour carries a
  meaning alone): a marker in its title readable in plain text (for instance `▸ Flow`, or the
  title in brackets), plus a different border style if the agent wants. The marker shows in the
  `--once` print too (the Flow active).

### 2. Scrolling the active panel (rule 2)

- Up, Down, PgUp, PgDn, Home and End move the active panel. The page is the active panel's own
  visible rows (the Flow's, Ready's or Tasks' body under its header row, or the maximized box's),
  not always the Flow's: `run()` passes the right page, or `View` computes it at the drawing.
- The Flow keeps its pause semantics (below). Ready, Tasks, Projects and Agents scroll by line
  within their content: an offset clamped between the first line and the last full page; a box
  whose content fits does not move. Each box keeps its own offset when the active panel changes.
  These boxes have no pause title and no new-line count.
- A row that spans two lines (a working task, a project) may be split by a scroll; keeping the two
  lines together is the agent's choice.
- The filter's change resets every box's offset to the start (today it resets the Flow to the
  live end).

### 3. The Flow newest first (rule 3)

- `window()` and `flow()` draw the newest line at the top, the older ones below. The live end is
  the top.
- The key directions follow the screen: Up and PgUp move toward the top (newer), Down and PgDn
  toward the bottom (older). Home goes to the top, the live end, and follows live again; End goes
  to the bottom, the oldest kept line of the merged Flow. (Default chosen: Home and End keep their
  meaning on screen, top and bottom, so their target swaps from today's.)
- The pause is unchanged in meaning: scrolled away from the live end, the window stays on the
  lines it shows while lines arrive, its title reads `Flow  paused, <n> new`, until Home, or Up or
  PgUp reaching the newest line, follows live again. The anchor logic of `window()` stays (the
  line shown that fell out of its board's 2000 lines: the window goes to the oldest kept, as
  today).
- `--once` prints the newest first too.

### 4. A narrow, right-aligned `Ago` column (rule 4)

- The clock form keeps its 14 columns (`MM-DD HH:MM:SS`).
- The `Ago` form (`t`) has its own narrow width, right-aligned, computed rather than `TIME_W`:
  default, the width of the widest `since()` text of the lines drawn, at least the header's 3
  (`Ago`) and at most 8 (`100 days`); a text that would not fit is cut with `…`, as every cell.
  The agent may pick a fixed width instead if it holds every form up to `99 days` and is at most 8.
  `since()`'s words do not change (`docs/boards.md` names them).
- The freed columns go to the `Event` column.

### 5. Maximize (rule 5)

- One key, chosen by the agent among those not bound (bound today: arrows, PgUp, PgDn, Home, End,
  Enter, Esc, Backspace, `t`, `/`, `?`, `q`, Ctrl-C, and Tab and Shift-Tab after this CR),
  maximizes the active panel: it takes the whole body, full width and height; the header and the
  footer stay. The same key restores the layout.
- While maximized, Tab and Shift-Tab move the active panel among the panels that the normal
  layout at this width draws, and the newly active one is shown maximized (default chosen: the
  screen stays maximized). The scroll keys scroll it with its maximized page.
- Ready's fixed `RIGHT_W`, and Tasks', widen to the body's width when maximized (the `Title` and
  `Task` columns take the rest); the forge error title of Ready is cut at the box's width.
- The help (`?`) opens over a maximized screen as over the normal one; closing it returns to the
  maximized panel. Esc keeps its meaning (clear the filter; leave the help): it does not restore.
- `--once` prints the normal layout (no key is read).

### 6. Help, footer and doc

- `HELP` gains Tab (and Shift-Tab), the maximize key, and the scroll rows say "the active panel"
  with the Flow's directions (Up: newer, Home: the newest, follows live; End: the oldest kept).
- The footer names the new keys, for instance `? keys  / filter  Tab panel  <key> max  t time
  q quit`; the agent may shorten it, as long as Tab and the maximize key are in it.
- The module docstrings of `screen.py` ("newest at the bottom") and `view.py` ("Only the Flow
  scrolls" in substance) say the new behaviour.
- `docs/boards.md`, the `chantier live` section: the Flow is newest first; the `Ago` column is
  narrow and right-aligned; the active panel, Tab, the per-panel scroll, the maximize key; the Keys
  table and the bullet "Only the Flow scrolls" rewritten to match.

## Out of scope

- Anything outside `clients/tui/`, its tests and `docs/boards.md`: no server, API, web client or
  `commands/live.py` change (the TUI reads the published API and writes nothing; `--once`,
  `--url`, `--only`, `--transport` unchanged).
- `since()`'s and `age()`'s words, Ready's `Age` column, the clock form, the header, the counts.
- Mouse support, a selected row or cursor inside a panel, opening a row, horizontal scroll.
- A persisted choice of active panel or maximized state between runs.

## Evidence

Tests in `skills/chantier/scripts/cli/tests/test_live_model.py` and `test_live_ready.py`, in
process, through `screen.plain()` and `View.press()` as the existing ones do; parametrized, few,
within `just test`'s time budget (AGENTS.md):

- The start state: the Flow is active, its title carries the marker, the screen is not maximized.
- Tab and Shift-Tab: the cycle at a wide width (5 panels) and under 100 columns (3 panels, the
  left column skipped); Tab while typing a filter adds nothing and changes no panel; Tab with the
  help open only closes it.
- The Flow newest first: with 31 lines, the first data row under `Time` is the newest line; Down
  pauses (`Flow  paused, <n> new` after lines arrive, the shown lines unchanged); Up back to the
  top follows live; Home follows live; End shows the oldest kept line. The existing parametrized
  case table of `test_keys_scroll_pause_filter_and_help_change_what_the_screen_prints` is updated
  to the new directions, not dropped. The merged-boards test (`..._home_shows_the_oldest_...`)
  moves to End.
- Per-panel scroll: with more Ready rows (or tasks) than the box holds, Tab to it, Down and PgDn
  show the later rows, Home the first; the Flow does not move meanwhile; a panel whose content fits
  does not move.
- Maximize: the key shows the active panel alone in the body (the other boxes' titles absent),
  the same key restores; Tab while maximized shows the next panel maximized; a maximized Ready row
  shows a title cut later than at `RIGHT_W`.
- The `Ago` column: with `t`, the column is no wider than the computed width (a row's text shows
  more of the event than with the clock form at the same width), and the times are right-aligned
  (for instance ` 2 min` and `46 min` end at the same column).
- `key_name`: Tab and Shift-Tab keystrokes built by hand map to the new names (the existing
  parametrized test gains two rows).
- `HELP` and the footer: the existing tests read the shipped `HELP` and the shipped footer text
  from the module at the head under test; they are updated to the new keys.
- `test_since_rounds_down_and_never_runs_backwards` stays unchanged.

Gates (AGENTS.md): a change under the CLI's `src/`: `just check` and `just eval-dry-run` in the
worktree before the first push; the long gate `just scenario (ubuntu-latest)` green at the PR's
head; the Windows run of the long gate as the batch's shape asks. No host or default matrix: the
behaviour depends on neither the host nor the configuration. No screenshot of the CR board pane is
owed (the pane is not touched). A manual check in a real terminal (`chantier live` on a running
board: Tab, the scroll, maximize, `t`) is noted in the PR's Deliverables or its Known gaps.

## Open questions

None blocking. Defaults stated above that the Chief of Staff may confirm with the user:
Shift-Tab goes back; Home and End are top (newest, live) and bottom (oldest) of the newest-first
Flow; the screen stays maximized when Tab moves the active panel.

# TUI: resize live's main columns with the mouse and keep the widths

## Goal, in the owner's words

In `chantier live`, the owner wants to resize the screen's main columns with the mouse and keep
the sizes (`intake/request.md`; the owner's words, verbatim in French, are in
`tui-resize-columns/intake/request.md`): « pouvoir redimensionner les 3 colonnes principale avec
la souris et de garder la taille dans un json (utilise la lib platformdirs pour connaitre le
dossier user config) ».

The main columns are the left column (Projects and Agents), the central column (the Flow) and the
right column (Ready and Tasks). The user grabs either of the two panel borders already drawn where
two columns meet and drags it; the columns inside the Flow (Project, Who and the others) are not
resized with the mouse (answer 4). The widths are kept in one JSON file in the user's chantier
configuration folder, computed with `platformdirs` (answers 2 and 6).

This change request sits on top of `tui-resize-columns` in a stack batch (answers 1 and 3; its
`depends.json`: `{"after": ["tui-resize-columns"]}`). It builds on that CR's wider defaults (the
left column 42) and its narrow-terminal rule (its answer 5: the Event column keeps at least 20
columns; the left column shrinks first, down to 28, then Who and Project down to 10, and the left
column is not drawn only when even that does not fit). The code and doc names below are those of
`main` today; where `tui-resize-columns` renames or adds one (its single width function used by
`_plan` and `render`, its threshold replacing `NARROW`), this CR builds on its version.

## What changes

All paths below are under `skills/chantier/scripts/cli/src/chantier/` unless they start at the
repository root.

### 1. Mouse tracking (`clients/tui/screen.py`, `run`)

- When `live` runs with a keyboard (`term` is a `blessed.Terminal`, or the stand-in `run`
  accepts) and the terminal says it does drag reporting
  (`term.does_mouse(clicks=True, report_drag=True)`, asked once at start), `run` turns on
  `blessed`'s mouse tracking, `term.mouse_enabled(clicks=True, report_drag=True)`, in the same
  `with` as `term.cbreak()`, so the terminal is given back, tracking off, on every way out that
  `docs/boards.md` lists today (`q`, Ctrl-C, a refused key, an error, SIGTERM on POSIX).
- Where `does_mouse` says no, or with no keyboard (`term is None`), tracking stays off: no border
  drags, the footer carries no mouse words (section 4), the keys and the terminal's own mouse
  (selection, wheel, links) work as today. This is the absence of a feature the terminal lacks,
  not a substitute; Windows Terminal is required to say yes (section 7: if it does not, the CR
  stops).
- The loop reads mouse events from the same `term.inkey(...)` call as the keys. A key still goes
  through `key_name` and `View.press` exactly as today; a mouse event goes to the new handling of
  sections 2 and 3. Each mouse event that changes the screen redraws at once, as a key does.

### 2. Dragging a border (`clients/tui/screen.py`, `clients/tui/view.py`)

- The draggable borders are the two pairs of panel borders already drawn between main columns,
  on any row of the body (between the header and the footer):
  - between the left and the central column: the left column's right border and the Flow's left
    border, side by side; dragging either sets the left column's width;
  - between the central and the right column: the Flow's right border and the right column's left
    border (Ready's and Tasks'); dragging either sets the right column's width.
  Nothing new is drawn. The central column takes the rest of the width, as today (it has no
  stored width of its own).
- A left-button press on one of these borders starts a drag; each drag event moves that border to
  the pointer's column; the release ends it. A press anywhere else, a right or middle button, a
  release with no drag started, or a drag that did not start on a border does nothing (no panel
  becomes active, nothing scrolls).
- No drag while the help is open, while a panel is maximized (`m`: no column borders are drawn),
  or on a border not drawn (a terminal too narrow for the left column has only the
  central/right pair).
- `View` keeps the two widths (`left`, `right`); `render`, `_plan` and the width function of
  `tui-resize-columns` read them from the `View`, not from `LEFT_W` and `RIGHT_W`, which stay the
  defaults (42 after `tui-resize-columns`, and 44). The hit test of a press is computed from the
  same plan `render` draws, so the borders the user sees are the borders that move. How close a
  press must be to count, and how the code is split, are the Coder's.
- A drag is bounded: no column narrower than its minimum (question Q1), and a drag that would
  leave the central column narrower than its minimum under the narrow-terminal rule of
  `tui-resize-columns` (Time, Project and Who at 10, Event at 20) stops there. Within those
  bounds, when the central column holds less than its defaults, Who and Project close up as that
  rule says.
- On a terminal narrower than the kept widths need, the drawing gives way as
  `tui-resize-columns` says, starting from the kept left width instead of the default (question
  Q2 for the right column); the kept widths are not changed by it. A drag starts from the width
  drawn.

### 3. The wheel (`clients/tui/screen.py`)

With tracking on, the terminal no longer scrolls on its own: a wheel event up is the `up` key
and a wheel event down the `down` key, given to `View.press` for the active panel (the Flow at
the start), with no modifier, so scrolling the main part keeps working directly (answer 5). A
wheel event is one line.

### 4. What the status bar says (`clients/tui/screen.py`, `clients/tui/view.py`)

Answer 5 accepts that, with tracking on, a plain drag no longer selects text and a link may need
a modifier, on condition that the status bar says what to do:

- While tracking is on, the footer (`footer`, after `KEYS_FOOTER`, before the filter and the
  "more projects not watched" text, so it is cut last) adds the mouse words: how to resize (drag
  a border), how to select text, and how to open a PR link in Ready. The exact words for text
  selection and links are the ones the Windows Terminal run of section 7 proves (Shift-drag is
  the usual way to select; the link's modifier is what the run shows); the PR records them.
- The help (`HELP`, `?`) gains the same lines: dragging a border between two columns resizes them
  (kept for the next start), the wheel scrolls the active panel, and the selection and link
  modifiers.
- With tracking off, the footer and the help are as today.

### 5. The kept widths: `live.json` (a new module, `clients/tui/widths.py`)

- One file, `live.json`, in the user's chantier configuration folder (`config_dir()` of section
  6, beside `profiles.json`). Its content is one object, `{"left": <int>, "right": <int>}`, the
  two widths last dragged. A key that is absent takes its default.
- `live` (not `--once`) reads it once at start, before it connects to any board. A file that
  cannot be read, is not JSON, is not an object, or holds a value that is not an integer within
  the bounds of Q1 makes `live` refuse to start with one line naming the file and the fault, in
  the form of `clients/profiles.py`'s `_bad`, with `EXIT_PRECONDITION`: `live: <path>: <fault>:
  fix or delete it`. No default is drawn in its place (no fallback; the Chief of Staff's call).
  A key other than `left` and `right`: question Q3.
- `--once` reads no file and draws the default widths, so a test, a script and a bug report print
  the same for every user (the Chief of Staff's call).
- `live` writes the file on a drag's release when a width changed, and at no other moment: never
  on a redraw, a key, a wheel event, a resize of the terminal or a quit. The write is atomic (a
  temporary file in the same folder, then a replace), as `clients/profiles.py` writes
  `profiles.json`; the folder is created when missing; the mode is the user's default (it holds no
  secret). A write that fails ends `live` with one line naming the file and the error, the
  terminal given back.
- With no file, nothing is written until the first drag. Deleting the file resets the widths.

### 6. The configuration folder, with `platformdirs` (`clients/profiles.py`, root `pyproject.toml`, `uv.lock`)

- `platformdirs` is added to `[project].dependencies` in the root `pyproject.toml`, pinned with
  `==` like the others, and `uv.lock` is regenerated (`uv lock`). It ships a pure-Python wheel, so
  the Linux, macOS and Windows rule of `AGENTS.md` holds. It is imported inside the function that
  uses it, like the other heavy imports (adding it to `banned-module-level-imports` is allowed).
- One folder (answer 6): `config_dir()` keeps `$CHANTIER_CONFIG_HOME` first, as it is, and takes
  the rest from `platformdirs.user_config_dir("chantier", appauthor=False, roaming=True)`,
  replacing its hand-written branches, as `AGENTS.md` asks of a dependency ("replaces
  hand-written code"). Both `profiles.json` and `live.json` live there.
- What that gives: Windows `%APPDATA%\chantier` and Linux `$XDG_CONFIG_HOME/chantier` or
  `~/.config/chantier`, as today; macOS `~/Library/Application Support/chantier` instead of
  `~/.config/chantier`. On macOS only, `profiles.json` is no longer found where it was: the user
  runs `chantier login` again (answer 6). The CR moves no file. Nothing changes on Windows.
- `config_dir()`'s `platform` and `environ` parameters, used by `test_the_config_folder`, keep a
  way to test each platform's rule; how, with `platformdirs`, is the Coder's.

### 7. The rules and docs that change

- Root `AGENTS.md`, the `live` bullet ("it reads the server only ... writes nothing and messages
  no agent"): `live` writes one file, `live.json` in the user's chantier configuration folder,
  the two column widths the user dragged, on a drag's release, and nothing else; `--once` reads
  and writes no file.
- Root `AGENTS.md`, the first rule's list of where chantier writes: add `live.json`, beside
  `profiles.json`, written by `live` only. Its folder rule ("`$CHANTIER_CONFIG_HOME`, else
  `%APPDATA%` on Windows, else `$XDG_CONFIG_HOME` or `~/.config`") becomes the `platformdirs`
  rule (`$CHANTIER_CONFIG_HOME`, else `platformdirs`' user configuration folder: `%APPDATA%` on
  Windows, `~/Library/Application Support` on macOS, `$XDG_CONFIG_HOME` or `~/.config`
  elsewhere). The "no setup" claim holds: `live.json` is the terminal's own view state, not
  configuration, absent until the first drag.
- `clients/profiles.py`: `config_dir()`'s docstring states the new rule; the module docstring
  says the folder also holds `live.json` (written by `clients/tui/widths.py`).
- `docs/boards.md`, "The live terminal view": "writes nothing" becomes "writes nothing but its
  column widths"; a paragraph says the two borders that drag, which columns they size, the wheel,
  the footer's mouse words, where `live.json` lives, when it is written, the refusal on a bad
  file, that a narrow terminal draws narrower without changing the file, that `--once` reads no
  file, and that on a terminal without mouse reporting nothing of this applies. The keys table
  gains the mouse lines of the help. The `--once` capture does not change (`--once` draws the
  defaults; `tui-resize-columns` regenerates it).
- No doc under `docs/` names `profiles.json`'s folder today; `docs/boards.md`'s paragraph above
  names it for `live.json`, with the macOS folder.
- The `screen.py` and `view.py` module docstrings say the border drags, the wheel and the kept
  widths.

## Decisions of `02-answers.md`

- Answer 1: the batch is a stack batch. This CR is the upper of the two stacked CRs; as the CR on
  top, it owes the local Windows run of the long gate `scenario` (`AGENTS.md`).
- Answer 2: the owner's words are the source: resizing with the mouse and sizes kept in a JSON
  file in the user's configuration folder found with `platformdirs`: sections 2, 5 and 6.
- Answer 3: split from `tui-resize-columns` and stacked on it: its wider defaults and its
  narrow-terminal rule are its own; this CR builds on them (section 2) and changes neither.
- Answer 4: the mouse resizes the main columns (left, central, right), grabbed by either of the
  two existing panel borders where two columns meet; nothing new is drawn; the columns inside the
  central one are not resized with the mouse: section 2. Where `work/spec-before-split.md`
  differs (the Flow's Project and Who edges), this answer wins.
- Answer 5: tracking on is accepted (a plain drag no longer selects, a link may need a modifier),
  on two conditions: the status bar says what to do (section 4), and the main part's scrolling
  keeps working directly with the wheel (section 3).
- Answer 6: one configuration folder, computed by `platformdirs`, `$CHANTIER_CONFIG_HOME` still
  first; on macOS only `profiles.json` moves and `chantier login` is run again; nothing changes
  on Windows: section 6.
- Header: spec critic yes (what the user sees, a new dependency, a rule of `AGENTS.md`).
- The Chief of Staff's calls (in the brief): a bad `live.json` refuses the start with one line
  (section 5); `--once` reads no file and draws the defaults (section 5); the Windows Terminal run
  must prove mouse support, else the CR stops and reports (section "Evidence").

## Out of scope

- Resizing the columns inside the Flow (Time, Ago, Project, Who, CR, Event), Ready's or Tasks'
  columns, or the boxes' heights (answer 4).
- The wider defaults and the narrow-terminal rule: `tui-resize-columns`.
- A keyboard way to resize, a reset key or a reset command (deleting `live.json` resets).
- Moving `profiles.json` for macOS users (answer 6: they log in again).
- The web board's columns.
- The CR board pane (`hooks/register.tsx`): untouched, so its screenshot rule does not apply.
- `2-backlog/P1/tui-live-batch-kanban`, a later item on the same layout: whichever lands second
  rebases on the other.

## Evidence

- Tests, in `skills/chantier/scripts/cli/tests/` (`test_live_panels.py`, `test_live_model.py`, or
  one new parametrized file; few, within `just test`'s budget), with the configuration folder the
  test fixture already points `CHANTIER_CONFIG_HOME` at (`conftest.py`), never the user's:
  - with no `live.json`, the screen draws the default widths, read from the drawn text of
    `screen.plain`, not from the constants;
  - the widths a `View` holds are the widths drawn;
  - parametrized over the four borders (each of the two pairs, either border): a simulated
    press-drag-release through the stand-in terminal's mouse events moves that column's width by
    the drag's distance, redraws, and writes `live.json` once, on release, with both keys; a key,
    a wheel event and a click elsewhere write nothing and change no width;
  - a drag is stopped at each bound (Q1, and the central column's minimum);
  - with the help open or a panel maximized, a press on a border's position resizes nothing;
  - a wheel event up and down moves the active panel as `up` and `down` do;
  - the footer and the help carry the mouse words with tracking on and not with it off (a
    stand-in whose `does_mouse` says no: no tracking turned on, footer as today);
  - read: a file with both keys gives those widths; a missing key gives its default; a file that
    is not JSON, not an object, or holds a value out of bounds or not an integer makes `live`
    exit with `EXIT_PRECONDITION` and the one line naming the file and the fault, before any
    connection;
  - `--once` with a `live.json` holding other widths draws the defaults and leaves the file
    unchanged;
  - a terminal narrower than the kept widths draws narrower and leaves the file unchanged;
  - the existing panel tests (keys, Tab order, settle) pass unchanged.
- `test_the_config_folder` (`test_remote_cli.py`) covers the new rule: `$CHANTIER_CONFIG_HOME`
  first; Windows and Linux (with and without `XDG_CONFIG_HOME`) give today's folders; macOS gives
  `~/Library/Application Support/chantier`.
- `just check` and `just eval-dry-run` (a change under the CLI's `src/`); the pipeline's long gate
  `scenario (ubuntu-latest)` green at the PR's head; and, as the stack's top CR, the long gate
  `scenario` run locally on Windows (`chantier gate <cr> scenario`) at its head.
- Mouse support in Windows Terminal, proved by hand, the Chief of Staff's condition: `chantier
  live` in Windows Terminal (PowerShell) on a running board; `does_mouse` says yes there (the
  footer shows the mouse words); a drag of each of the two borders (either side), the wheel
  scrolling the Flow, `q`, a second start showing the widths kept; then the terminal is given back
  (typing, selecting text and the wheel work as before after `q`); and the words the footer gives
  for selecting text and opening a Ready PR link are tried and work. The PR's Deliverables carry
  one screenshot of the real terminal after the drags, showing no username and no home folder
  (floor rule 8; `live.json`'s path is not on it). If mouse support does not work there (no
  tracking, no drag events, the terminal not given back), the CR stops and reports, with no other
  gate or substitute. The same run on Linux or macOS is named in the PR as done or not done.

## Questions for the Chief of Staff

- **Q1, a column's minimum width.** A drag stops at a minimum, and `live.json` is refused below
  it. Which? Suggested: today's widths, the left column 28 (the floor of `tui-resize-columns`'
  narrow rule) and the right column 44 (`RIGHT_W`), so no column the user drags is narrower than
  today; the maximum is where the central column reaches its minimum. Alternative: a smaller floor
  (the boxes' titles and table headers plus one).
- **Q2, the right column on a narrow terminal.** `tui-resize-columns` never shrinks the right
  column (it was fixed at 44). A right column the user dragged wider may not fit on a smaller
  terminal later. Suggested: it gives way first, down to 44, before the left column, then the rule
  of `tui-resize-columns` as it is. Alternative: after the left column and before Who and Project.
- **Q3, an unknown key in `live.json`.** A key other than `left` and `right` (a typo, a later
  version's key): a wrong value, refused like the others, or ignored? Suggested: refused (no
  fallback; a later version that adds a key changes this rule with it).

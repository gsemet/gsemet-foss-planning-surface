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
configuration folder, computed with `platformdirs` (answers 2 and 6). A drag stops at 20 columns
for the left column and 30 for the right one (answer 7). `live` shows its content first and turns
the mouse on after, when the terminal handles it (answer 8), waiting at most 1 second per mouse
query (answer 9).

This change request sits on top of `tui-resize-columns` in a stack batch (answers 1 and 3; its
`depends.json`: `{"after": ["tui-resize-columns"]}`). It builds on that CR's wider defaults (the
left column 42) and extends its narrow-terminal rule (its answer 5: the Event column keeps at least
20 columns; the left column shrinks first, down to 28, then Who and Project down to 10, and the
left column is not drawn only when even that does not fit) for kept widths, with three additions
(section 3, answers 10 and 14); with the default widths that rule's behaviour and order are
unchanged. The code and doc names below are those of
`main` today; where `tui-resize-columns` renames or adds one (its single width function used by
`_plan` and `render`, its threshold replacing `NARROW`), this CR builds on its version.

## What changes

All paths below are under `skills/chantier/scripts/cli/src/chantier/` unless they start at the
repository root.

### 1. Mouse tracking, turned on after the first draw (`clients/tui/screen.py`, `run`)

- **Content first (answer 8).** `run` draws the first screen (today `Live(frame(), ...)`, entered
  inside `with term.cbreak()`) before it asks the terminal anything about the mouse. Only then, in
  the loop, before its first `term.inkey(...)`, does it ask and turn tracking on. No mouse question
  is sent before the first screen is on the terminal.
- **What asks, and when, in the pinned blessed 1.53.0** (read in its sources; the Coder re-reads
  them at the pinned version):
  - POSIX (`blessed/terminal.py`): `does_mouse(clicks=True, report_drag=True)` sends one DECRQM
    query per mode it needs (1006, SGR, then 1002, drag), each through `get_dec_mode` and
    `_query_with_boundary`: the query and a cursor position request (CPR) are written, and the
    call blocks until the CPR comes back or the timeout ends. A terminal that answers the CPR but
    not the mode gives a fast negative (one round trip). The first DECRQM may be preceded by an
    XTVERSION query (`get_dec_mode` calls `_is_apple_terminal(timeout)`, which calls
    `get_software_version(timeout=timeout)`) unless `TERM_PROGRAM` is `Apple_Terminal`. The
    answers are cached: `mouse_enabled(clicks=True, report_drag=True)` then reads the cache
    (`dec_modes_enabled`) and only writes the DECSET sequence, asking nothing more.
  - Windows (`blessed/win_terminal.py`): `WinTerminal.does_mouse` asks nothing (true on any tty
    with styling). The asking is in `mouse_enabled`: it runs the POSIX `does_mouse` probe (the same
    DECRQM and CPR queries, blocking the same way, with the `timeout` it was given), uses the DEC
    modes when they are answered, and otherwise turns on the console's own mouse input
    (`ENABLE_MOUSE_INPUT`, QuickEdit off), converting its events into the same mouse keystrokes.
    So on Windows the moment that waits is entering `mouse_enabled`, and it too comes after the
    first draw.
- **A 1 second timeout per mouse query (answer 9), passed as a parameter.** In blessed 1.53.0 a
  caller sets a query's timeout in two ways: the keyword parameter `timeout` (seconds) of
  `does_mouse` and `mouse_enabled` (both `Terminal` and `WinTerminal`), which they pass on to every
  `get_dec_mode` call, and from there to the XTVERSION query and to the DECRQM-with-CPR query; or
  the environment variable `BLESSED_QUERY_TIMEOUT_SECONDS`, which blessed reads once, when
  `blessed.keyboard` is imported, into the module constant `TERMINAL_QUERY_TIMEOUT_SECONDS` (5 s
  when unset), the default of every query. The specification takes the parameter: `run` calls
  `term.does_mouse(clicks=True, report_drag=True, timeout=1.0)` and
  `term.mouse_enabled(clicks=True, report_drag=True, timeout=1.0)`, the 1.0 named once in the
  code. The environment variable is not used: it is read only at import, it would change every
  query of the process (the XTGETTCAP query of `Terminal()` included) rather than the mouse
  queries, and setting it would override the user's own value. Consequences:
  - each mouse query waits at most 1 second; after a first DECRQM that times out, blessed sends no
    other DECRQM (`NOT_QUERIED`, a false `does_mouse`), so a terminal that answers nothing, not
    even the CPR (a pexpect script, some `ssh -t` relays), holds the loop once, for at most about
    2 seconds (one XTVERSION and one DECRQM), and tracking stays off;
  - the user's `BLESSED_QUERY_TIMEOUT_SECONDS` no longer sets the mouse queries' timeout (it still
    sets blessed's other queries, as today); a terminal on a link slower than 1 second per round
    trip gets no mouse, which answer 9 accepts.
- **Keys typed meanwhile are not lost.** While a query waits, `_read_until` reads all the input
  that arrives; it removes the terminal's answers (the CPR, the DECRQM reply) and puts the rest
  back with `ungetch`, in order, for the next `inkey` (on Windows, `_read_available` reads the
  key-down events the same way). The query runs in the loop's own thread, between two `inkey`
  calls, never in another thread: blessed reads the keyboard itself during it, and two readers
  would split the keys. While it waits, no key is handled and the screen is not redrawn; the keys
  are handled, in order, once it returns. What the code cannot prove, and the Coder checks by
  hand (Evidence): that the keys typed during the wait arrive whole and in order on a real
  terminal, on Windows Terminal and on a POSIX terminal; that the wait is not felt on a terminal
  that answers (one round trip); and on Windows which of blessed's two paths ran.
- When the question says yes (POSIX: `does_mouse` true; Windows: `does_mouse` true, then whichever
  path `mouse_enabled` takes), `run` enters `term.mouse_enabled(clicks=True, report_drag=True,
  timeout=1.0)` so that it is left on every way out that `docs/boards.md` lists today (`q`,
  Ctrl-C, a refused key, an error, SIGTERM on POSIX), before the alternate screen is left and
  `cbreak` ends: the terminal is given back, tracking off. How the code nests it once the loop has
  started (for instance an exit stack held by the `with`) is the Coder's. The footer's mouse words
  (section 5) appear at the first redraw after tracking is on, not on the first screen.
- Where `does_mouse` is false, or with no keyboard (`term is None`), tracking stays off: no border
  drags, the footer carries no mouse words (section 5), the keys and the terminal's own mouse
  (selection, wheel, links) work as today. This is the absence of a feature the terminal lacks,
  not a substitute. On Windows a true `does_mouse`, and the footer's mouse words it brings, prove
  nothing about the terminal: only the hand run of the Evidence does, and its PR records which of
  blessed's two paths ran (the DEC modes or the console's mouse input). How the run tells the two
  apart is the Coder's. Windows Terminal must deliver the drags in the hand run (Evidence, answer
  18: if it does not, the CR stops).
- The loop reads mouse events from the same `term.inkey(...)` call as the keys. A key still goes
  through `key_name` and `View.press` exactly as today; a mouse event goes to the new handling of
  sections 2 and 4. Each mouse event that changes the screen redraws at once, as a key does.
- `blessed.Terminal()` itself, built in `run` before the first draw, already sends an XTGETTCAP
  query at its creation today (`Terminal.__init__xtgettcap`), with blessed's default timeout. It
  is not about the mouse and this CR does not change it.

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
- **Bounds (answer 7).** A drag stops at 20 columns for the left column and 30 for the right one
  (the defaults stay 42 and 44); these are the two minimums, named once in the code. A drag that
  would leave the central column narrower than its minimum stops there. The central column's
  minimum is the one `tui-resize-columns` draws, computed by its one width function (used by
  `_plan` and `render`), which this CR reads and does not restate. There is no other maximum: the
  largest width a drag reaches depends on the terminal. Within those bounds, when the central
  column holds less than its defaults, Who and Project close up as that CR's rule says.
- **A drag while the terminal draws narrower than kept (answer 11).** A drag starts from the
  widths drawn (section 3 may draw a column narrower than kept). During the drag, the column on
  the other side keeps the width drawn when the drag started (the narrow rule does not shrink it
  or widen it while the drag lasts), and the dragged border follows the pointer, down to the
  dragged column's minimum (20 or 30) and up to where the central column reaches its minimum. The
  release keeps the width drawn at that moment for the dragged column: that is the value written
  for it (section 6). The other column was not dragged, so its key in `live.json` keeps its kept
  value (section 6: the file holds the widths last dragged); after the release, the screen is
  drawn by section 3's rule with the new kept widths.

### 3. A narrow terminal, with kept widths (`clients/tui/screen.py`)

This CR extends `tui-resize-columns`' narrow-terminal rule for the kept widths `L` (left) and `R`
(right), read in place of the defaults, with three additions:

- the right column gives way first, from `R` down to 44 (answer 14);
- the threshold under which the left column is not drawn uses `min(L, 28)` and `min(R, 44)`;
- without the left column, the right column takes spare columns back toward `R` (answer 10).

With the default widths (42 and 44), `tui-resize-columns`' behaviour and order are unchanged: the
first step is empty (`R` is 44) and the threshold is that CR's.

The automatic shrinking stops at 28 for the left column and 44 for the right one; a
column the user set below that floor (`L` from 20 to 27, `R` from 30 to 43) is drawn at its kept
width, never widened to the floor and never narrowed by the terminal. When the terminal is
narrower than the kept widths need, the drawing gives way in this order, so that the Event column
keeps at least 20 columns:

1. the right column, from `R` down to 44 (not at all when `R` is 44 or less) (answer 14);
2. the left column, from `L` down to 28 (not at all when `L` is 28 or less);
3. Who, down to 10, then Project, down to 10, as `tui-resize-columns` says;
4. only when even that does not fit is the left column not drawn.

Consequences, which the Coder keeps:

- The threshold under which the left column is not drawn is `tui-resize-columns`' sum with
  `min(L, 28)` for the left column and `min(R, 44)` for the right one. With the defaults it is
  that CR's 122 columns (one project watched, the `Time` column); with `L` 22 and `R` 30 it is 102
  (22 + 50 + 30, the Flow's minimum of 50 being that CR's 4 + 14 + 1 + 10 + 1 + 20). The tests
  measure the drawn text, not these sums. As in that CR, the threshold uses the `Time` column's
  width in both modes.
- A right column kept at or under 44 never gives way; a left column kept at or under 28 never
  shrinks; neither is ever drawn wider than kept. A column kept narrower than its floor only
  frees columns for the central one.
- **Without the left column (answer 10).** The Flow and the right column share the width under
  the same floors: Project and Who first take back their defaults as Event's 20 allows (that CR's
  rule); then the right column takes the spare columns back toward `R`, up to `R`, the reverse of
  the order in which they gave way. The right column is drawn at no more than `R` and, when `R` is
  over 44, at no less than 44, so the kept width shows wherever it fits.
- The kept widths are not changed by any of this: only a drag's release writes them (section 6).
  A drag starts from the width drawn (section 2).

### 4. The wheel (`clients/tui/screen.py`)

With tracking on, the terminal no longer scrolls on its own: a wheel event up is the `up` key
and a wheel event down the `down` key, given to `View.press` for the active panel (the Flow at
the start), with no modifier, so scrolling the main part keeps working directly (answer 5). A
wheel event is one line. A wheel event does nothing while the help is open or while a filter is
being typed (`/`) (answer 15).

### 5. What the status bar says (`clients/tui/screen.py`, `clients/tui/view.py`)

Answer 5 accepts that, with tracking on, a plain drag no longer selects text and a link may need
a modifier, on condition that the status bar says what to do:

- While tracking is on, the footer (`footer`) adds the mouse words: how to resize (drag a
  border), how to select text, and how to open a PR link in Ready. When the footer lacks room,
  the mouse words give way first: the typed filter (`/<text>`) and `filter: <text>` stay visible,
  as `docs/boards.md` promises (answer 16). Where they go in the line
  so that they are cut first is the Coder's. The exact words for text selection and links are the
  ones the Windows Terminal run of the Evidence proves (Shift-drag is the usual way to select; the
  link's modifier is what the run shows); the PR records them.
- The help (`HELP`, `?`) gains the same lines: dragging a border between two columns resizes them
  (kept for the next start), the wheel scrolls the active panel, and the selection and link
  modifiers.
- With tracking off, and on the first screen before tracking is turned on (section 1), the footer
  and the help are as today.

### 6. The kept widths: `live.json` (a new module, `clients/tui/widths.py`)

- One file, `live.json`, in the user's chantier configuration folder (`config_dir()` of section
  7, beside `profiles.json`). Its content is one object, `{"left": <int>, "right": <int>}`, the
  two widths last dragged. A key that is absent takes its default.
- **The path comes from outside `clients/tui/` (answer 19).** `clients/tui/` imports nothing of
  chantier but itself, `chantier.__version__` and `chantier.core.errors`: the check
  `test_the_terminal_client_imports_only_itself_the_version_and_the_errors` in
  `tests/test_live_link.py` (its `ALLOWED`, and the assertion that reads it) and the package
  docstring of `clients/tui/__init__.py` say so, and neither is widened. So `widths.py` does not
  import `chantier.clients.profiles`: the configuration folder (or `live.json`'s path) reaches it
  from outside `clients/tui/`, for instance from `commands/live.py`, which calls
  `profiles.config_dir()` and passes the path in. `widths.py` builds its refusal itself, with
  `ChantierError` and `EXIT_PRECONDITION` from `chantier.core.errors`, in the same form as
  `profiles.py`'s `_bad`, without importing it. The check then covers `widths.py` as it is.
- `live` (not `--once`) reads it once at start, before it connects to any board. A file that
  cannot be read, is not JSON, is not an object, or holds a value that is not an integer, or a
  `left` under 20 or a `right` under 30 (answer 7), makes `live` refuse to start with one line
  naming the file and the fault, in the form of `clients/profiles.py`'s `_bad`, with
  `EXIT_PRECONDITION`: `live: <path>: <fault>: fix or delete it`. No default is drawn in its place
  (no fallback; answer 17). A key other than `left` and `right` is refused like any other wrong
  value, in the same form (answer 17). A large value is not refused: the narrow rule of section 3
  draws it narrower.
- `--once` reads no `live.json` and writes nothing, and draws the default widths, so a test, a
  script and a bug report print the same for every user (answer 17).
- `live` writes the file on a drag's release when a width changed, and at no other moment: never
  on a redraw, a key, a wheel event, a resize of the terminal or a quit. It writes both keys: the
  dragged column's width drawn at the release, and the other column's kept width unchanged (with
  no file, its default) (section 2, answer 12). The write is atomic (a temporary file in the
  same folder, then a replace), as `clients/profiles.py` writes `profiles.json`; the folder is created when
  missing; the mode is the user's default (it holds no secret). A write that fails ends `live`
  with one line naming the file and the error, the terminal given back.
- With no file, nothing is written until the first drag. Deleting the file resets the widths.

### 7. The configuration folder, with `platformdirs` (`clients/profiles.py`, root `pyproject.toml`, `uv.lock`)

- `platformdirs` is added to `[project].dependencies` in the root `pyproject.toml`, pinned with
  `==` like the others, and `uv.lock` is regenerated (`uv lock`). Nothing in the repository shows
  what wheel it ships: the Coder checks, on the pinned version, that it ships a wheel for Linux,
  macOS and Windows (a pure-Python one would do), as `AGENTS.md` asks of a dependency, and the PR
  records what it found; if it does not, the CR stops and reports. It is imported inside the
  function that uses it, like the other heavy imports (adding it to `banned-module-level-imports`
  is allowed).
- One folder (answer 6): `config_dir()` keeps `$CHANTIER_CONFIG_HOME` first, as it is, and takes
  the rest from `platformdirs.user_config_dir("chantier", appauthor=False, roaming=True)`,
  replacing its hand-written branches, as `AGENTS.md` asks of a dependency ("replaces
  hand-written code"). Both `profiles.json` and `live.json` live there.
- How `platformdirs` resolves the Windows folder (the `APPDATA` environment variable, the
  Windows known-folder API, or another way) is not shown by anything in the repository: the Coder
  checks it on the pinned version and the PR records the result. If the folder it gives on the
  user's Windows is not today's `%APPDATA%\chantier`, the CR stops and reports (answer 6: nothing
  changes on Windows).
- What that gives: Windows `%APPDATA%\chantier` (to check, above) and Linux
  `$XDG_CONFIG_HOME/chantier` or `~/.config/chantier`, as today; macOS
  `~/Library/Application Support/chantier` instead of `~/.config/chantier`. On macOS only,
  `profiles.json` is no longer found where it was: the user runs `chantier login` again (answer
  6). The CR moves no file. Nothing changes on Windows.
- `config_dir()`'s `platform` and `environ` parameters, used by `test_the_config_folder`, keep a
  way to test each platform's rule; how, with `platformdirs`, is the Coder's. The test's Windows
  case follows the way `platformdirs` really resolves the folder (found above): it sets `APPDATA`
  only if that is what `platformdirs` reads, else it stands in for what it does read.

### 8. The rules and docs that change

- Root `AGENTS.md`, the `live` bullet ("it reads the server only ... writes nothing and messages
  no agent"): `live` writes one file, `live.json` in the user's chantier configuration folder,
  the two column widths the user dragged, on a drag's release, and nothing else; `--once` reads
  no `live.json` and writes nothing (it still reads `profiles.json` and `server.json`, as today).
- Root `AGENTS.md`, the first rule's list of where chantier writes: "in one file outside any
  project, `chantier/profiles.json` ... mode 0600" becomes two files outside any project, in the
  user's config folder: `chantier/profiles.json` (mode 0600) and `chantier/live.json` (the user's
  default mode, written by `live` only). Its folder rule ("`$CHANTIER_CONFIG_HOME`, else
  `%APPDATA%` on Windows, else `$XDG_CONFIG_HOME` or `~/.config`") becomes the `platformdirs`
  rule (`$CHANTIER_CONFIG_HOME`, else `platformdirs`' user configuration folder: `%APPDATA%` on
  Windows, `~/Library/Application Support` on macOS, `$XDG_CONFIG_HOME` or `~/.config`
  elsewhere). The "no setup" claim holds: `live.json` is the terminal's own view state, not
  configuration, absent until the first drag.
- Every place that calls `live` read-only states the new truth: read-only toward the server;
  it writes only `live.json`, on a drag's release. Checked at the code on `main`:
  - `clients/tui/__init__.py`, line 1, the package docstring ("a read-only client of the surface
    server's published API"); its paragraph on imports stays as it is (section 6, answer 19);
  - `commands/live.py`, line 1, the module docstring ("watched live in the terminal, read-only");
  - `declare/live.py`, the `HELP` text (line 8, "watch a running board live in the terminal,
    read-only: ..."), which `chantier live --help` prints;
  - `docs/server-api.md`, "A terminal client" (line 296, "a read-only terminal view of one to four
    running boards");
  - root `AGENTS.md`, the `live` bullet's clause "it reads the server only (the recorded one, or
    the active profile's) (never the planning folder, the forge or git)": still true of what it
    reads; the bullet adds that it writes `live.json` only, on a drag's release (the next bullet);
  - `docs/boards.md`, "The live terminal view" (line 79, "in the terminal, read-only", and line 80,
    "writes nothing"; below).
  The wording of each is the Coder's.
- `clients/profiles.py`: `config_dir()`'s docstring states the new rule. The module docstring
  ("One file, `profiles.json`, ... nothing else is read or written here") stays true of the module
  itself, which reads and writes `profiles.json` only; it adds that the same folder also holds
  `live.json`, which `clients/tui/widths.py` reads and writes with the path `commands/live.py`
  passes it (section 6).
- `docs/surface-server.svg` (answer 13): in the `chantier live` box, "terminal, reads only" (line
  20) becomes "terminal, reads the server only". Its `<desc>` names `live` only as one of the
  clients and stays true; no other line of the diagram says what `live` reads or writes. The
  diagram's text file, `docs/surface-server-texts.md`, which carries the same box's lines
  ("terminal, reads only", line 22), changes with it, so the two stay identical. Any other line or
  description of the diagram this change makes false changes with it.
- `docs/boards.md`, "The live terminal view": "writes nothing" becomes "writes nothing but its
  column widths"; a paragraph says the two borders that drag, which columns they size, their
  minimums (20 and 30), the wheel, the footer's mouse words, that the mouse is turned on just
  after the first screen (keys typed meanwhile are kept; a terminal that does not answer within
  1 second per query gets no mouse), where `live.json` lives, when it is written, the refusal on
  a bad file, that a narrow terminal draws narrower without changing the file and never touches a
  column kept under 28 (left) or 44 (right), that `--once` reads no `live.json` and writes
  nothing, and that on a terminal without mouse reporting nothing of this applies. The keys table
  gains the mouse lines of the help. The `--once` capture does not change (`--once` draws the
  defaults; `tui-resize-columns` regenerates it).
- No doc under `docs/` names `profiles.json`'s folder today; `docs/boards.md`'s paragraph above
  names it for `live.json`, with the macOS folder.
- The `screen.py` and `view.py` module docstrings say the border drags, the wheel, the kept
  widths and when the mouse is turned on.

## Decisions of `02-answers.md`

- Answer 1: the batch is a stack batch. This CR is the upper of the two stacked CRs; as the CR on
  top, it owes the local Windows run of the long gate `scenario` (`AGENTS.md`).
- Answer 2: the owner's words are the source: resizing with the mouse and sizes kept in a JSON
  file in the user's configuration folder found with `platformdirs`: sections 2, 6 and 7.
- Answer 3: split from `tui-resize-columns` and stacked on it: its wider defaults and its
  narrow-terminal rule are its own. This CR keeps its defaults and extends its narrow-terminal rule
  for kept widths with three additions: the right column gives way first, from `R` down to 44; the
  threshold uses `min(L, 28)` and `min(R, 44)`; without the left column the right column takes
  spare columns back toward `R` (sections 2 and 3). With the default widths, that CR's behaviour
  and order are unchanged.
- Answer 4: the mouse resizes the main columns (left, central, right), grabbed by either of the
  two existing panel borders where two columns meet; nothing new is drawn; the columns inside the
  central one are not resized with the mouse: section 2. Where `work/spec-before-split.md`
  differs (the Flow's Project and Who edges), this answer wins.
- Answer 5: tracking on is accepted (a plain drag no longer selects, a link may need a modifier),
  on two conditions: the status bar says what to do (section 5), and the main part's scrolling
  keeps working directly with the wheel (section 4).
- Answer 6: one configuration folder, computed by `platformdirs`, `$CHANTIER_CONFIG_HOME` still
  first; on macOS only `profiles.json` moves and `chantier login` is run again; nothing changes
  on Windows: section 7.
- Answer 7 (tui-mouse-Q4): a drag stops at 20 columns for the left column and 30 for the right
  one, the defaults staying 42 and 44; `live.json` is refused under them: sections 2, 3 and 6.
- Answer 8 (tui-mouse-Q5): live draws its first screen without waiting for any answer of the
  terminal about the mouse; the mouse question comes after it, and tracking is turned on then if
  the terminal handles it: section 1.
- Answer 9 (the Chief of Staff's call on this specification's question 1): each mouse query has
  its own timeout of 1 second, passed as blessed's `timeout` parameter to `does_mouse` and
  `mouse_enabled`, not through `BLESSED_QUERY_TIMEOUT_SECONDS`: section 1.
- Answer 10 (the Chief of Staff's call on its question 2): without the left column, the right
  column takes spare columns back toward its kept width, after Project and Who: section 3.
- Answer 11 (the Chief of Staff's call on its question 3): during a drag the other side column
  keeps the width drawn, the dragged border follows the pointer down to a minimum, and the release
  keeps the width drawn: sections 2 and 6.
- Answer 12: on a drag's release, `live.json` keeps the dragged column's width as drawn and
  leaves the other column's saved value unchanged: sections 2 and 6.
- Answer 13: `docs/surface-server.svg` changes in this CR: the `chantier live` box's "terminal,
  reads only" becomes "terminal, reads the server only", and any other line or description the
  change makes false changes with it: section 8.
- Answer 14: on a terminal too narrow for the kept widths, a right column kept wider than 44 gives
  way first, down to 44, before the left column; with the default widths nothing differs from
  `tui-resize-columns`: section 3.
- Answer 15: a wheel event does nothing while the help is open or a filter is being typed:
  section 4.
- Answer 16: when the footer lacks room, the mouse words give way first and the typed filter text
  stays visible: section 5.
- Answer 17: a `live.json` that cannot be read or holds a wrong value, an unknown key included,
  refuses the start with one line; `--once` reads no `live.json`, writes nothing and draws the
  defaults: section 6.
- Answer 18: the Windows Terminal hand run must prove mouse support, else the CR stops and
  reports: sections 1 and "Evidence".
- Answer 19: the check that `clients/tui/` imports nothing else of chantier stays as it is; the
  configuration folder reaches the new module from outside `clients/tui/`: sections 6 and 8.
- Header: spec critic yes (what the user sees, a new dependency, a rule of `AGENTS.md`).

## Out of scope

- Resizing the columns inside the Flow (Time, Ago, Project, Who, CR, Event), Ready's or Tasks'
  columns, or the boxes' heights (answer 4).
- The wider defaults and the narrow-terminal rule with the default widths: `tui-resize-columns`
  (this CR adds only section 3's three additions for kept widths).
- Widening the import check of `clients/tui/` or its package docstring's import paragraph
  (answer 19).
- The XTGETTCAP query blessed sends when `Terminal()` is created, before the first draw, with
  blessed's default timeout, as today: not about the mouse.
- `BLESSED_QUERY_TIMEOUT_SECONDS`: `live` neither sets nor reads it.
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
  - content first: through a stand-in terminal that records the order of calls and their
    arguments, the first frame is drawn before `does_mouse` or `mouse_enabled` is called, and both
    are called with `timeout=1.0`; the first frame's footer has no mouse words and the next
    redraw's has them; keys the stand-in holds from before tracking is turned on are handled, in
    order, after it;
  - parametrized over the four borders (each of the two pairs, either border): a simulated
    press-drag-release through the stand-in terminal's mouse events moves that column's width by
    the drag's distance, redraws, and writes `live.json` once, on release, with both keys; a key,
    a wheel event and a click elsewhere write nothing and change no width;
  - a drag is stopped at 20 (left) and 30 (right), and at the central column's minimum;
  - a drag on a terminal drawing a column narrower than kept (answer 11): during the drag the
    other column keeps the width drawn at the start, the dragged border follows the pointer down
    to its minimum and up to the central column's minimum, and the release writes the dragged
    column's width drawn at that moment and the other column's kept width unchanged;
  - with the help open or a panel maximized, a press on a border's position resizes nothing;
  - a wheel event up and down moves the active panel as `up` and `down` do; with the help open or
    a filter being typed, it changes nothing;
  - the footer and the help carry the mouse words with tracking on and not with it off (a
    stand-in whose `does_mouse` is false: no tracking turned on, footer as today); on a footer too
    narrow for both, the typed filter and `filter: <text>` stay visible and the mouse words are
    cut;
  - read: a file with both keys gives those widths; `left` 20 and `right` 30 are accepted; a
    missing key gives its default; a file that is not JSON, not an object, holds a value that is
    not an integer, a `left` of 19 or a `right` of 29, or a key other than `left` and `right` makes
    `live` exit with `EXIT_PRECONDITION` and the one line naming the file and the fault, before
    any connection;
  - `--once` with a `live.json` holding other widths draws the defaults and leaves the file
    unchanged;
  - narrow terminal, parametrized over kept widths and terminal widths: a terminal narrower than
    the kept widths draws narrower and leaves the file unchanged; with a kept right column wider
    than 44, the right column gives way first, down to 44, before the left column; with `left` 22
    and `right` 30 kept, both are drawn at 22 and 30 at every width where the left column is
    drawn (never widened to 28 or 44, never narrowed), Who and Project close up before the left
    column goes, and the left column is drawn down to the lower threshold `min(L, 28)` and
    `min(R, 44)` give (102 columns with one project; 101 does not draw it);
  - without the left column and a kept right column over 44 (answer 10): as the terminal widens,
    Project and Who reach their defaults first, then the right column widens toward `R` and stops
    at `R`;
  - the existing panel tests (keys, Tab order, settle) pass unchanged.
- The import check `test_the_terminal_client_imports_only_itself_the_version_and_the_errors`
  (`tests/test_live_link.py`) passes unchanged with `widths.py` in `clients/tui/` (answer 19).
- `test_the_config_folder` (`test_remote_cli.py`) covers the new rule: `$CHANTIER_CONFIG_HOME`
  first; Windows and Linux (with and without `XDG_CONFIG_HOME`) give today's folders, the Windows
  case built on the way `platformdirs` really resolves the folder (section 7); macOS gives
  `~/Library/Application Support/chantier`. The PR records what `platformdirs` reads on Windows
  and what wheel the pinned version ships.
- `just check` and `just eval-dry-run` (a change under the CLI's `src/`); the pipeline's long gate
  `scenario (ubuntu-latest)` green at the PR's head; and, as the stack's top CR, the long gate
  `scenario` run locally on Windows (`chantier gate <cr> scenario`) at its head.
- Mouse support in Windows Terminal, proved by hand (answer 18): `chantier
  live` in Windows Terminal (PowerShell) on a running board (the footer's mouse words prove
  nothing there: `does_mouse` is true on any styled Windows tty, section 1); the PR records which
  of blessed's two paths ran, the DEC private modes or the console's own mouse input; the first
  screen shows with no wait felt before it; keys typed at once on start (for instance `?` then a
  key, or Tab) are all handled, in order; a drag of each of the two borders (either side), the
  wheel scrolling the Flow, `q`, a second start showing the widths kept; then the terminal is
  given back (typing, selecting text and the wheel work as before after `q`); and the words the
  footer gives for selecting text and opening a Ready PR link are tried and work. The PR's
  Deliverables carry one screenshot of the real terminal after the drags, showing no username and
  no home folder (floor rule 8; `live.json`'s path is not on it). If mouse support does not work
  there (no tracking, no drag events, the terminal not given back), the CR stops and reports,
  with no other gate or substitute. The same run on Linux or macOS (the first screen, the keys
  typed at start, the drags, the terminal given back) is named in the PR as done or not done.

## Questions for the Chief of Staff

None.

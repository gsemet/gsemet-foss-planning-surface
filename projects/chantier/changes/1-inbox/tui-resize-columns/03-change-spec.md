# TUI: resize three columns with the mouse and keep the widths

## Goal, in the owner's words

In `chantier live`, three columns cut their text today: the left column (the Projects and Agents
boxes), and the Flow table's Project and Who columns. The owner wants (`intake/request.md`,
2026-11-27, verbatim in French there):

1. wider defaults: the left column 50 % wider, Project twice as wide, Who 1.5 times as wide;
2. the three columns resized with the mouse;
3. the sizes kept in a JSON file in the user's configuration folder, found with the
   `platformdirs` library.

The batch that carries it is a stack batch (answer 1); this CR is one CR of it, destined for
`3-ready` (answers header).

## What changes

### 1. The default widths (`clients/tui/parts.py`, `clients/tui/screen.py`)

All paths below are under `skills/chantier/scripts/cli/src/chantier/`.

| Column | Today | New default |
|---|---|---|
| Left column (`LEFT_W`, `parts.py`) | 28 | 42 (x1.5) |
| Flow's Project (`PROJECT_W`, `screen.py`) | 10, 12 with several boards | 20, 22 with several boards |
| Flow's Who (`WHO_W`, `screen.py`) | 10 | 15 (x1.5) |

The two extra columns of Project with several boards hold the board's label (`a/`); they stay
added on top of the doubled width. `RIGHT_W = 44` (Ready and Tasks), `CR_W`, `TIME_W` and the
`Ago` column's rule do not change. The Event column keeps taking the rest (`ratio=1`).

### 2. Resizing with the mouse (`clients/tui/screen.py`, `clients/tui/view.py`)

- While `live` runs with a keyboard (the `blessed` terminal `run` already opens), it turns on
  `blessed`'s mouse tracking (`Terminal.mouse_enabled(clicks=True, report_drag=True)`, inside the
  same `with` as `cbreak()`), so the terminal is given back, mouse tracking off, on every way out
  that `docs/boards.md` lists today (`q`, Ctrl-C, a refused key, an error, SIGTERM on POSIX).
- The user presses on a column's right edge and drags it: the left column's right border, the
  border between the Flow's Project and Who columns, and the one between Who and Event (in a
  single-board, single-project Flow there is no Project column, so only Who's edge). On release,
  the column has the new width. The redraw follows the drag (each mouse event redraws at once,
  as a key does today).
- `View` keeps the three widths, and the drawing reads them from it, not from the module
  constants (the constants become the defaults). Hit-testing a press against the drawn edges
  is computed from the same plan `_plan`/`render` use, so the edges the user sees are the edges
  that move. How the edge is found and how close a press must be are left to the Coder.
- Every key works exactly as today (`HELP` and the keys table of `docs/boards.md` unchanged in
  effect). A mouse event that is not a press, a drag or a release on an edge does nothing (a
  click elsewhere changes no panel, scrolls nothing).
- Where `does_mouse` is false or no keyboard is attached (`term is None`), there is no resize:
  the screen draws with the kept widths and the keys work as today. There is no keyboard
  substitute for the mouse (no fallback, and none was asked).
- A drag has bounds, so that it cannot make the screen unusable: a column is never narrower
  than its header text plus one (the left column: its boxes' titles), and a drag that would
  leave the Event column narrower than its minimum (section 4) stops there.
- The help (`HELP`, `?`) gains one line: "drag a column's edge: resize it (kept for the next
  start)". The footer `KEYS_FOOTER` is unchanged.

### 3. The kept widths (a JSON file in the user's configuration folder)

- A new module, `clients/tui/widths.py`, reads and writes one file, `live.json`, in the user's
  chantier configuration folder (which folder: question Q1). Its content is one object:
  `{"left": 42, "project": 20, "who": 15}` (the Project width without the several-boards label
  columns). A key that is absent takes its default.
- `live` reads it once at start. It writes it on a drag's release, when a width changed, and at
  no other moment: never on a redraw, a key, a resize of the terminal or a quit. The write is
  atomic (a temporary file in the same folder, then a replace), as `clients/profiles.py`'s
  write of `profiles.json` is; the folder is created when missing.
- A width the terminal could not draw (section 4) is not written back: the file keeps the
  user's chosen width, and the screen draws what fits.
- A file that cannot be read or parsed, or that holds a value that is not a positive integer:
  question Q3.
- `--once` and the file: question Q4.

### 4. A narrow terminal: what gives way

Today the left column shows from `NARROW = 100` columns, and the Flow takes what `LEFT_W` and
`RIGHT_W` leave. At 100 columns with a 42-column left column and a 44-column right column, the
Flow would have 14 columns, less than its Time column. What gives way is question Q2; the
spec's drawing must, whatever the answer, never draw an Event column narrower than a fixed
minimum, and never change the file because of a narrow terminal.

### 5. The new dependency (`pyproject.toml`, `uv.lock`)

- `platformdirs` is added to `[project].dependencies`, pinned with `==` like the others, and
  `uv.lock` is regenerated (`uv lock`). It ships a pure-Python wheel (`py3-none-any`), so the
  Linux, macOS and Windows rule of `AGENTS.md` holds. It is not in `uv.lock` today.
- It is imported where it is used, inside the function, like the other heavy imports (it need
  not join `banned-module-level-imports`; adding it there is allowed).
- `AGENTS.md` says "A dependency ... replaces hand-written code": the answer to Q1 decides
  whether it replaces `config_dir()`'s hand-written folder rule in `clients/profiles.py`.

### 6. The rules and docs that change

- `AGENTS.md`, the `live` bullet ("reads the server only ... writes nothing and messages no
  agent"): `live` writes one file, `live.json` in the user's chantier configuration folder,
  the three column widths the user dragged, and nothing else.
- `AGENTS.md`, the first rule's list of where chantier writes ("... the user's profiles
  (`chantier login`, `logout`), in one file outside any project, `chantier/profiles.json` in the
  user's config folder (...), mode 0600 ..."): add `live.json`, its folder and its writer, with
  the same folder rule as decided in Q1. Its mode is the user's default (it holds no secret).
- `AGENTS.md`, the "no setup" claim: `live.json` is not configuration of a project; it is the
  terminal's own view state, absent until the first drag.
- `docs/boards.md`, "The live terminal view": "writes nothing" becomes "writes nothing but its
  column widths"; a paragraph says which three columns drag, where the file lives, when it is
  written, and what a narrow terminal does (Q2); the `--once` capture is regenerated with the
  new widths (120 columns); the `?` help line is added to the keys table.
- The `screen.py` and `view.py` module docstrings say the mouse resize and the kept widths.

## Decisions of `02-answers.md`

- Answer 1: the batch is a stack batch. This CR carries no stacking constraint of its own.
- Answer 2: the request's words are the source: wider defaults (left +50 %, Project x2, Who
  x1.5), resizing with the mouse, widths kept in a JSON file in the user's configuration folder
  found with `platformdirs`. All three are in sections 1 to 3 and 5.
- Header: spec critic yes (what the user sees, a new dependency, a rule of `AGENTS.md`).

## Out of scope

- Resizing any other column (Time, Ago, CR, Event, Ready's or Tasks' columns, `RIGHT_W`) or
  the boxes' heights.
- A keyboard way to resize, a reset key or a reset command (deleting `live.json` resets).
- The web board's columns.
- Moving `profiles.json`, unless Q1's answer says one folder computed by `platformdirs`.
- The CR board pane (`hooks/register.tsx`): untouched, so its screenshot rule does not apply.

## Evidence

- Tests, in `skills/chantier/scripts/cli/tests/` (in `test_live_panels.py` and
  `test_live_model.py`, or one new file, few and parametrized, within `just test`'s budget):
  - with no `live.json`, `--once`-style plain renders (`screen.plain`) at `WIDE` (140) show the
    left column at 42, Project at 20 (22 with two boards) and Who at 15, read from the drawn
    text, not from the constants;
  - the widths a `View` holds are the widths drawn;
  - a simulated press-drag-release on each of the three edges changes that width by the drag's
    distance, writes `live.json` once on release with the three keys, and a key press writes
    nothing; the file's folder comes from a temporary configuration folder, never the user's;
  - read: a file with the three keys gives those widths; a missing key gives its default; a
    bad file behaves as Q3 decides;
  - a narrow width behaves as Q2 decides, and the file is unchanged after it;
  - every key of `HELP` still does what it did (the existing panel tests pass unchanged).
- The folder: `test_the_config_folder` in `test_remote_cli.py` (or its successor) covers the
  folder rule Q1 decides, on `win32`, `linux` and `darwin`.
- `just check` and `just eval-dry-run` (a change under the CLI's `src/`), and the long gate
  `scenario` (a CLI change), green.
- Mouse on Windows, proved by hand: `chantier live` in Windows Terminal (PowerShell) on a
  running board, a drag of each of the three edges, `q`, a second start showing the widths kept;
  then the terminal is checked to be given back (typing and selecting text work after `q`).
  The PR's Deliverables carry one screenshot of the real terminal after the drags, showing no
  username and no home folder (floor rule 8; `live.json`'s path is not on it). The same run on
  Linux or macOS is named in the PR as done or not done.
- The Ready box's PR links (OSC 8, opened on a click): checked in the same Windows Terminal run
  with mouse tracking on; the PR says whether a click (or Ctrl-click) still opens the PR (see
  Q5).

## Questions for the Chief of Staff

- **Q1, the folder.** `platformdirs.user_config_dir("chantier", appauthor=False, roaming=True)`
  gives `%APPDATA%\chantier` on Windows and `$XDG_CONFIG_HOME/chantier` or
  `~/.config/chantier` on Linux, the same as `config_dir()` today, but
  `~/Library/Application Support/chantier` on macOS, where `config_dir()` gives
  `~/.config/chantier`. Which one?
  (a) One folder: `config_dir()` keeps `$CHANTIER_CONFIG_HOME` first and takes the rest from
  `platformdirs` (it replaces the hand-written branches, as `AGENTS.md` asks of a dependency);
  `profiles.json` moves on macOS (a macOS user logs in again, or the CR moves the file once).
  (b) One folder: `config_dir()` unchanged, `live.json` beside `profiles.json`; `platformdirs`
  is then not used, against the owner's words.
  (c) Two folders: `live.json` in `platformdirs`' folder, `profiles.json` where it is;
  `$CHANTIER_CONFIG_HOME` applies to both (tests need it) or to `profiles.json` only.
  Suggested: (a), with `$CHANTIER_CONFIG_HOME` still first.
- **Q2, a narrow terminal.** What gives way when the widths do not fit? Suggested: the Event
  column keeps at least 20 columns; to give it that, the left column shrinks first, down to 28
  (today's width), then the Flow's Who and Project down to 10, then, as today, the left column
  is not drawn under the width where even that does not fit (so `NARROW` grows from 100 to the
  width that fits a 28-column left column, the Flow at its minimum and `RIGHT_W`). Or: keep
  `NARROW = 100` and let the Event column be as narrow as it falls.
- **Q3, a bad `live.json`.** A file that cannot be read or parsed, or a width that is not a
  positive integer: `live` refuses to start with one line naming the file and the fault (the
  user deletes or fixes it), or starts on the defaults with a line in the footer and rewrites
  the file at the next drag? Suggested: the refusal (no fallback).
- **Q4, `--once`.** Does `--once` read `live.json`? Suggested: no, `--once` draws the defaults
  and reads no file, so a test, a script and a bug report print the same for every user.
- **Q5, mouse tracking and the terminal's own mouse.** With mouse tracking on, most terminals
  stop selecting text on a plain drag (Shift-drag still selects) and may need a modifier to
  open an OSC 8 link, so the Ready box's PR number may no longer open on a plain click. Is that
  acceptable as long as the docs say it? (Tracking cannot be limited to the edges: a terminal
  turns it on or off for the whole screen.) Suggested: accept it and say it in `docs/boards.md` (Shift-drag selects text;
  the link's modifier as the Windows run shows).

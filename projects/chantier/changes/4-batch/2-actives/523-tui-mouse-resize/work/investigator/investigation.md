# CR-523 investigation, before round 1

Base: 3412cd90 (CR-522). `SRC` = `skills/chantier/scripts/cli/src/chantier/`, `T` =
`skills/chantier/scripts/cli/tests/`. The worktree is untouched. Sources read: blessed 1.53.0 and
Rich 15.0.0 in the main checkout's `.venv`; platformdirs 4.14.8 wheel from PyPI, read as a zip in
`work/scratch/` (not published, not executed).

## Specification statements that are false or inexact at this base

1. s6 "a new module, `clients/tui/widths.py`": it exists (CR-522): `column_widths`, `Widths(left,
   project, who)`, the minima, no Rich, no I/O. Extend it (below); do not replace it.
2. s1 "a terminal that answers nothing ... holds the loop ... and tracking stays off": POSIX only.
   On Windows, after the failed probe `WinTerminal.mouse_enabled` turns on the console's own mouse
   input, so tracking goes on (as s1's own Windows bullet says). The footer words then show.
3. s1 "XTVERSION ... unless `TERM_PROGRAM` is `Apple_Terminal`": any non-empty `TERM_PROGRAM`
   answers from the environment, with no query (`_software_version_from_env`). XTVERSION is sent
   only when it is empty or unset; a failed one is not cached and may precede the 1002 query too.
   With Apple Terminal no DECRQM is sent either (`get_dec_mode` returns `NOT_QUERIED`): the mouse
   is never on there.
4. s7 and s8 "macOS `~/Library/Application Support/chantier`": `MacOS(XDGMixin, ...)`: an absolute
   `XDG_CONFIG_HOME` wins on macOS, giving `$XDG_CONFIG_HOME/chantier` (such a user's profiles do
   not move). The docs, the AGENTS.md folder rule and the macOS test case must say "unset".
5. s7 "Linux ... as today" and "nothing changes on Windows": true in the usual case only.
   - Linux: a relative `XDG_CONFIG_HOME` is ignored (today it is used).
   - Windows: platformdirs does not read `APPDATA` (see below).
6. s6 "the mode is the user's default" with "atomic ... as `profiles.py` writes": `profiles.save`
   uses `mkstemp`, which creates mode 0600. Copying it breaks the mode; create the temporary file
   so that the umask applies.

None of these triggers a stop.

## Section 1 facts confirmed in blessed 1.53.0

- `does_mouse(clicks, report_drag, timeout)` asks 1006 then 1002 and stops at the first
  unsupported one. Each DECRQM goes with a CPR (`_query_with_boundary`); answers are cached, so
  POSIX `mouse_enabled` only writes the DECSET. A first DECRQM with no mode reply sets a sticky
  failure (no further DECRQM).
- Other input read during a query is `ungetch`ed in order.
- `WinTerminal.does_mouse` asks nothing (tty with styling). `WinTerminal.mouse_enabled` probes,
  then DEC modes or native console input (`_native_mouse`; it also reports bare motion and ignores
  `report_drag`). It restores the console mode on exit, so it must exit before `cbreak` ends.
- `BLESSED_QUERY_TIMEOUT_SECONDS` is read at import (5 s default). `Terminal()` sends XTGETTCAP.
- Keystrokes: `MOUSE_LEFT`, `MOUSE_LEFT_MOTION`, `MOUSE_LEFT_RELEASED`, `MOUSE_SCROLL_UP/DOWN`,
  `MOUSE_MOTION`; modified ones are prefixed (`MOUSE_SHIFT_SCROLL_UP`). `mouse_xy` is 0-based.
  Decoded only while mode 1006 is cached as set. Probed with `ungetch` + `inkey`.
- Rich: entering `Live(frame(), ...)` draws the first frame, so asking in the loop before the first
  `inkey` is content-first. blessed writes to `sys.__stdout__`, outside Rich's redirect.

## platformdirs (section 7)

- Pin proposed: `platformdirs==4.14.8` (latest on PyPI, 2026-11-20). One wheel,
  `platformdirs-4.14.8-py3-none-any.whl`, pure Python (Linux, macOS, Windows), no dependency,
  Python >=3.11, MIT, `py.typed`. sha256 `1e34af59...b331392`.
- Windows, `user_config_dir("chantier", appauthor=False, roaming=True)`: `<RoamingAppData>\chantier`.
  `<RoamingAppData>` is `WIN_PD_OVERRIDE_APPDATA` if it is a fully qualified path, else the
  known-folder API (`SHGetKnownFolderPath` through ctypes; registry, then `APPDATA`, only when
  ctypes or winreg cannot be imported). The `APPDATA` variable is normally not read.
- On this machine the known folder (read through .NET, not through platformdirs) equals
  `%APPDATA%`; neither override variable is set: no stop. The Coder re-checks with the installed
  package (print a boolean, never the path). A process with a redirected `APPDATA` would now differ.
  In the repository only `T/test_remote_cli.py` sets `APPDATA`; scenario, eval kit and conftest
  isolate with `CHANTIER_CONFIG_HOME`.
- Linux: absolute `XDG_CONFIG_HOME`/chantier, else `~/.config/chantier`. Nothing is created
  (`ensure_exists` False).
- Test: platformdirs reads `os.environ`, not an injected mapping. Pick the class by `platform`
  (`windows.Windows`, `macos.MacOS`, `unix.Unix`) and monkeypatch the variables. The Windows case
  on Linux stands in for `platformdirs.windows.get_win_folder` (the API raises there; an override
  such as `/a` is not "fully qualified" and is ignored).

## Files, entry points, smallest change

- `SRC/clients/tui/widths.py`: `column_widths` takes the kept `L`, `R` (defaults `LEFT_W`,
  `RIGHT_W`) and returns `right` too; takes a frozen drawn pair during a drag; exposes the central
  minimum (the local `least`: 50 one project, 61 several projects, 63 several boards); minima
  20/30; `live.json` load and save (path passed in, `ChantierError`/`EXIT_PRECONDITION`). The
  existing import check covers it. A formula equal to today's at 42/44, with `lf=min(L,28)`,
  `rf=min(R,44)`, `spare=width-least` (checked by reading, not run):
  if `spare >= lf+rf`: `right=clamp(spare-grows-L, rf, R)`, `left=clamp(spare-grows-right, lf, L)`;
  else `left=0`, `right=clamp(spare-grows, rf, R)`. The rest (`spare-left-right`) goes to Project,
  then Who. Rewrite the module docstring.
- `SRC/clients/tui/view.py`: kept widths, file path, tracking flag, drag state; a separate mouse
  help tuple, shown only with tracking.
- `SRC/clients/tui/screen.py`: `run` (355-400) asks in the loop before the first `inkey` and holds
  `mouse_enabled` in an `ExitStack` as the last `with` item
  (`with keyed, Live(...) as live, ExitStack() as stack`); mouse events handled beside `key_name`;
  hit test on columns `left-1`/`left` and `width-right-1`/`width-right`, rows `header_height` to
  `height-2`; `render` (286-293) draws `widths.right`; `footer` appends the words last;
  `_help_panel`; docstring (14-20).
- `SRC/commands/live.py`: when not `--once`, load before `_boards`/`_start`, passing
  `profiles.config_dir() / "live.json"`; docstring. `SRC/declare/live.py:8`.
- `SRC/clients/profiles.py` (`config_dir` 44-56, docstrings), `pyproject.toml` (optionally the
  banned-import list), `uv.lock`.
- Docs: `AGENTS.md` (first rule, `live` bullet), `docs/boards.md` (79-80, line 90 "42 columns
  wide" becomes the default, keys table), `docs/server-api.md:296`, `docs/surface-server.svg:20`,
  `docs/surface-server-texts.md:22`, `tui/__init__.py:1`.
- Tests that must change: `T/test_live_model.py` `Term` (only `cbreak`, `inkey`: add `does_mouse`,
  `mouse_enabled`; no `hasattr` guard in the product); `T/test_remote_cli.py`
  `test_the_config_folder`. `T/test_live_panels.py` width cases pass unchanged.

## Risks

- Values derived from the old fixed widths: `parts.py:9`; `widths.py:13,43-44`; `screen.py:39,288,
  290`; `ready.py:10,77` (default `width`, title cut `width - 4`); docstrings and `boards.md:90`
  above; the 122/121 thresholds in the panel tests (default only). `_maximized` passes the full
  width already.
- `config_dir()` runs for every command (`_choose` loads the profiles unless `--profile local`).
  The batch's CLI is `uv run --no-sync` on the main checkout: after the merge, commands fail on the
  missing `platformdirs` until the locked sync runs. Sync at once; a held sync is a CLI stop.
- Drag: ignore a press-release that leaves the drawn width unchanged (a narrow terminal must not
  overwrite a kept value). Where the central column is already under its minimum (several boards
  under 107 columns), `width - minimum - other` is under the drawn width, and under 93 columns
  under 30 itself: decide the clamp (the minimum wins, or no move).
  A left drag must not drop the left column. Drop a drag when `?` or
  `m` arrives mid-drag.
- Redraw only when widths or offsets change: native Windows sends bare motion.
- A DEC reply later than 1 s reaches the loop as separate keys (`?` opens the help, the next
  character closes it; `y` and the digits do nothing). A late CPR or XTVERSION reply does nothing.
- Help is 15 rows today in an 18-row body in the tests: more than 3 added rows cut "any key closes
  this help" there and on small terminals.
- `right` at 30 squeezes Ready's fitted columns: look at it in the tests and the hand run.
- `live.json`: reject booleans as integers; only a missing file means defaults.
- In-process refusal tests must fake the tty: the "no terminal" refusal comes first.

## Questions only the user can answer

None. One action needs the user: the Windows Terminal hand run (typing and dragging in a real
terminal; an agent's screen control may not type or drag in terminals, and scripting around that
is not allowed). Item 4 above is a wording correction under answer 6, for the round.

## Evidence plan

Kind: interactive terminal behaviour, a new user file, a new dependency, docs.

- Before/after by command: `--once` output the same at base and head, and at head with a
  non-default `live.json` (file unchanged). `--once` needs a running board.
- Tests, as listed in the specification's Evidence (stand-in terminal for order, `timeout=1.0`,
  drags, wheel, footer, help; file read, refusal, write; narrow cases; config folder). The import
  check passes unchanged.
- Gates at the PR's head: `just check`; `just eval-dry-run`; pipeline `just scenario
  (ubuntu-latest)`; local Windows `chantier gate CR-523 scenario` (stack top); Verifier verdict.
- PR records: the wheel; what Windows reads and the equality boolean.
- Hand run, Windows Terminal + PowerShell, the head's build, a running board, as the specification
  lists it. Set `CHANTIER_CONFIG_HOME` to a neutral folder so no profile or home path shows; show
  `live.json`'s content as text, never its path. Which blessed path ran: a throwaway script outside
  the worktree enters `mouse_enabled` there and prints `_native_mouse`. Record the terminal's
  version and the proved selection and link modifiers. One screenshot after the drags, checked for
  username and home folder. Mouse not working: stop.
- Linux/macOS hand run: stated done or not done.
- No CR board pane screenshot and no `just mod` (neither `hooks/` nor `types/` changes).
- Cannot be shown by tests: real drag and wheel events, whole keys typed during a real query, the
  absence of a felt wait, terminal restoration on a real console, the Windows path taken, selection
  and link modifiers; the macOS folder and the POSIX run on a real machine unless done.

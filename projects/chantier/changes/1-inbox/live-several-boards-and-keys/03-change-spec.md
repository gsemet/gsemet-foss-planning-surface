# live: keys to scroll and filter, and up to 4 boards in one screen

`chantier live` keeps its Rich screen and gains keys: scroll the Flow over its last 2000 lines
(it pauses while scrolled back and counts the new lines), filter the Flow and the Tasks by one
text, a help of the keys, and quit, with the terminal always given back. `--url` becomes
repeatable: up to 4 boards in one screen, one key and one connection each. No server change, no
protocol change, still read-only.

Spec v2 (2026-11-21): live-Q22 to Q25 decided (the former open questions, each as built); the
spec critic's findings applied (overlaps with CR-429 and CR-443, the refusal's suffix, a test of
the loop's exits, one rule for the 2000 lines, Windows key decoding, `just test`'s time).

## Goal

The user wants a working terminal UI (2026-11-21, ui-night). Today `chantier live` watches one
board per run and reads no key (`intake/request.md`, `01-intent.md`). After this CR, in a terminal:

- the user scrolls back in the Flow and comes back to the live end, filters what is shown by a
  text (a project, a CR), shows the keys, and quits with `q` or Ctrl-C;
- the user watches up to 4 boards in one screen, each named by the link it printed.

A key changes what this screen shows and nothing else: `live` still reads the server only,
writes nothing and messages no agent (`01-intent.md`, live-Q19). It works on Linux, macOS and
Windows.

## Where it stands (read-only survey, `main` at 99fa847f)

- `skills/chantier/scripts/cli/src/chantier/declare/live.py`: the parser (`--url LINK` once,
  `--only` repeatable, `--transport auto|ws|http`, `--once`).
- `skills/chantier/scripts/cli/src/chantier/commands/live.py`: `from_link`, `recorded`,
  `_check_only`, `height_for`, `once` (one link read in the calling thread, 10 s deadline),
  `_read` (feeds the model and calls `_check_only` under the lock), `watch` (one reader thread,
  any `ChantierError` of the reader kept in `failed` and raised after `screen.run`, Ctrl-C caught
  as `KeyboardInterrupt`), `live` (refuses a stdout that is not a terminal without `--once`:
  `NO_TERMINAL`).
- `skills/chantier/scripts/cli/src/chantier/clients/tui/model.py`: `Model` (one board), `Line`
  (`t`, `project`, `who`, `text`), `FLOW = 200`, `WATCHED = 15`.
- `skills/chantier/scripts/cli/src/chantier/clients/tui/screen.py`: `header`, `left`, `flow`
  (the last `rows` lines), `tasks`, `footer` (`Ctrl-C to quit` and the not-watched projects),
  `render`, `plain` (for `--once`), `run(m, lock, alive)` (`rich.live.Live(screen=True)`,
  redrawn every `REDRAW_S = 1.0` with `time.sleep`).
- `skills/chantier/scripts/cli/src/chantier/clients/tui/link.py`: `Link` (one board), `refused`
  (`live: <the server's sentence>`, a plain `ChantierError`, exit 4).
- `skills/chantier/scripts/cli/tests/test_live_model.py` (prepared events, no network) and
  `test_live_link.py` (one real server in a thread, module fixture `live`; the import check of
  `clients/tui/`); `tests/test_board.py`'s `LAZY` tuple with the `banned-module-level-imports`
  list of the root `pyproject.toml`.
- `docs/boards.md`, "The live terminal view"; `docs/server-api.md`, "A terminal client".

## The key reader: `blessed`, pinned

Keys are read through one dependency, **`blessed==1.53.0`** (the release of 2026-11-20, the one
`uv lock` resolves on 2026-11-21), added to the root `pyproject.toml`'s `dependencies` and locked
in `uv.lock` (`uv lock` from the root). There is no second way to read keys beside it (live-Q3):
no `termios`, `tty`, `msvcrt` or `select` code of chantier's own.

Why `blessed` (live-Q3, AGENTS.md: "a dependency ships wheels for Linux, macOS and Windows and
replaces hand-written code"; CONTRIBUTING.md: `no-build = true`):

- Wheels: `blessed-1.53.0-py3-none-any.whl`, and its dependencies `wcwidth>=0.9.4` (abi3 wheels
  for Linux x86_64/aarch64, macOS x86_64/arm64, Windows, and a `py3-none-any` wheel),
  `jinxed>=2.1.1,<3` (`py2.py3-none-any`; the terminal capabilities on Windows) and, on Windows
  only, `ansicon` (`py2.py3-none-any`). Nothing builds from source.
- It replaces the code a key reader needs on two systems: the terminal's mode
  (`Terminal.cbreak()`, a context manager that restores echo and line mode on every way out of
  its block, an exception included) and a read with a timeout (`Terminal.inkey(timeout=...)`)
  that decodes the escape sequences into named keys (`KEY_UP`, `KEY_DOWN`, `KEY_PGUP`,
  `KEY_PGDOWN`, `KEY_HOME`, `KEY_END`, `KEY_ESCAPE`, `KEY_ENTER`, `KEY_BACKSPACE`), on POSIX and
  on the Windows console.
- Windows key decoding (the console's key events into these names, through `jinxed` and
  `ansicon`) is **documented by `blessed`, unproved here**: no test of this CR opens a Windows
  console. Evidence item 8 proves it on Windows in a real terminal; when it was not tried there,
  the PR's Known gaps names it (live-Q20).
- The read with a timeout runs in the screen's own loop (the main thread), in place of today's
  `time.sleep(REDRAW_S)`: no reader thread is left blocked in a raw terminal at exit.

Rejected: `readchar` (one blocking read, no timeout: it needs a thread of its own, which a
process ending in Ctrl-C kills inside its raw-mode read, leaving the terminal without echo; the
restore would then be hand-written, a second way); Textual and `prompt_toolkit` (application
frameworks; live-Q2 keeps the Rich screen); `keyboard`, `pynput` (root on Linux, a display
server).

`blessed` loads lazily, like Rich: add `"blessed"` to the root `pyproject.toml`'s
`[tool.ruff.lint.flake8-tidy-imports] banned-module-level-imports` and to `tests/test_board.py`'s
`LAZY`; it is imported inside `screen.py`'s functions only.

## What changes

### 1. The command line (`declare/live.py`, `commands/live.py`)

- `--url LINK` becomes repeatable (`action="append"`, default `[]`): one board per link, each with
  the key of its own `?k=` (live-Q11). Its help: "a board's link (http(s)://host:port/[prefix/]
  ?k=<key>), repeatable, at most 4; omitted: the board recorded as running for this surface or
  project". With no `--url`, the one board `recorded()` finds, as today; the recorded board joins
  others only by giving its link too (no implicit addition).
- A fifth `--url` is refused at start, before any connection: `--url: at most 4 boards in one
  screen` (exit 2, `EXIT_USAGE`) (live-Q11).
- The same board twice is refused at start: `--url <base>: given twice` (exit 2) (live-Q23). The
  comparison is on the base address as `from_link` returns it, with no name resolution: two
  spellings of one host (`localhost`, `127.0.0.1`) are not detected, and that is accepted.
- `--transport` applies to every board (live-Q13). Each `--url` link keeps `proxies=True`, the
  recorded board `proxies=False`, as today.
- `--only <project>` (live-Q13): each board's `Model` keeps the ids it serves; an id is refused,
  with `--only <id>: no board serves it; served: <a/x, b/y, ...>` (exit 2), once every board's
  `board` value is known and none serves it. With one board the sentence stays today's
  (`--only <id>: the board serves <ids>`). `_check_only` becomes this check over all the
  boards' models. These `--only` sentences are usage errors, not a board's refusal: they carry
  no board address (section 2).
- `live` builds one `Link` and one `Model` per board, in `--url` order, each board with a label
  `a`, `b`, `c`, `d` (live-Q22), mapped to its base address on its header line.

### 2. Several boards (`commands/live.py`, `clients/tui/screen.py`)

- One reader thread per board (`_read`, unchanged in body), all under the one lock of `watch`;
  each board has its own connection, its own subscriptions and its own 15 watched projects
  (`WATCHED`, per `Model`) (live-Q13).
- A board not reachable at start, or lost later, is retried every 5 s by its own `Link`, as
  today, while the others go on (live-Q14): nothing changes in `link.py` for that.
- A refused key or protocol on any board ends the run (live-Q14): `watch` (or `once`) raises it
  as `<the server's sentence> (board <base address>)`, with its exit code (4). The base address
  is the one `from_link` returns, with no query: the key is never printed. This holds with one
  board too (one rule).
- The suffix goes on the link's key or protocol refusal only, never on `_check_only`'s `--only`
  errors (exit 2), which the same reader thread raises. It is added in `commands/live.py` where
  the link's refusal is caught, around the reading of `link.items()` only, not around
  `_check_only`: with CR-429 merged, `except Refusal` (its `Refusal(ChantierError)` in
  `clients/tui/link.py`, with `.sentence` and `.kind`); until then, around the `ChantierError`
  that `link.py:refused()` builds, caught where `link.items()` raises it. This CR does not
  change `link.py` (see "Overlaps").
- The screen with one board is today's, plus the keys (live-Q12): same header, same columns, no
  label.
- With several boards (live-Q12):
  - the header: its first line `chantier live  <n> boards  <HH:MM:SS> UTC` (board `a`'s server
    time), then one line per board, `<label>  <base address>  <served>  v<version>  <transport>
    <link state>` (link state `connecting`, `live`, or `reconnecting since HH:MM:SS`, from that
    board's `Model.link_word`), then the four counts, summed over the boards. The header's
    height is 2 with one board and `2 + n` with `n` boards (`screen.HEADER_H` becomes a function
    of the models; `commands/live.py:height_for` uses it);
  - every place that names a project names it `<label>/<project>`: the Flow's project column
    (shown whenever more than one project is watched in all), the left column's projects and
    agents;
  - a task line's CR cell reads `<label> <CR>` (its column widened to hold it), so two boards
    serving a project of the same name stay apart;
  - each lease's time left is computed from its own board's server time (`Model.now`), as today;
  - the footer's not-watched projects are named `<label>/<project>`.
- The Flow merges the boards' lines by time (stable: lines of one time keep their order).

### 3. `--once` (`commands/live.py`)

Unchanged in form and reads no key (live-Q15). With several boards it waits for every board's
first values (every board's `Model.missing()` empty) within `ONCE_S = 10` s, each `Link` with the
same `deadline`, then prints one screen through `screen.plain`; past the deadline it exits 4 with
`live: no first answer within 10 s for <missing>`, each missing item named with its board
(`a board`, `b project demo`, `b events demo`). With one board the sentence stays today's (`live:
the board gave no first answer within 10 s for <missing>`). One path for one board or several (a
thread per board) is the Driver's choice, as long as one board prints what it prints today.

### 4. The view under keys (new `clients/tui/view.py`)

A plain object, no Rich, no `blessed`, no network: what the keys change. It is fed key names
(strings: `up`, `down`, `pgup`, `pgdn`, `home`, `end`, `enter`, `esc`, `backspace`, `ctrl-c`, or
one printable character) by a method such as `press(name, page)` and says whether to quit, so the
tests feed keys with no terminal (live-Q20). It holds the Flow's scroll, the new-line count while
paused, the filter (the text being typed and the text applied), and whether the help is shown.
`screen.py` maps a `blessed` keystroke to these names (one small function, tested with
`blessed.keyboard.Keystroke` objects built by hand, no terminal). It imports nothing of chantier
but `chantier.clients.tui` (the import check of `test_live_link.py` holds).

The keys (live-Q4, live-Q17), outside the filter's typing:

| Key | Effect |
|---|---|
| Up / Down | the Flow one line older / newer |
| PgUp / PgDn | the Flow one page (the Flow's visible rows) older / newer |
| Home | the oldest kept line of the merged Flow (section 5) |
| End | back to the live end (follows again) |
| `/` | starts typing a filter |
| `?` | shows the keys over the screen |
| Esc | clears the filter; leaves the help |
| `q`, Ctrl-C | quit, exit 0 |
| any other key | nothing |

While typing a filter: printable characters are added, Backspace removes the last one, Enter
applies the text (an empty text clears the filter), Esc cancels the typing and clears the
filter; the other keys do nothing; Ctrl-C still quits. The footer shows the text being typed,
`/<text>`.

While the help is shown (`?`), the full list of the keys is drawn over the screen (a Rich
panel over the body), until a key is pressed; that key closes the help and does nothing else,
except Ctrl-C, which quits (live-Q17).

### 5. Scrolling the Flow (`model.py`, `view.py`, `screen.py`)

- Only the Flow scrolls (live-Q5). One rule for how far back (live-Q6): `model.FLOW` becomes
  2000, the cap of each board's `Model` (its last 2000 lines, in memory, as `FLOW = 200` caps it
  today); the Flow on screen is the merged view over the boards' models (section 2), so with `n`
  boards it holds up to `n × 2000` lines. Home goes to the oldest kept line of that merged view.
  Nothing older is asked of the server (no replay of the journal's history). The module
  docstring's "the last 200 lines" says 2000 per board.
- At the live end the Flow shows the newest lines that fit, as today. Scrolled back, it does not
  move when lines arrive: the lines on screen stay on screen, and the Flow's panel title reads
  `Flow  paused, <n> new`, `<n>` the lines arrived since it left the live end (those the filter
  keeps). End, or Down or PgDn reaching the newest line, follows live again and the title is
  `Flow` (live-Q5). A line that falls out of its board's 2000 while scrolled back moves the view
  to the oldest kept line of the merged view, no further.
- `screen.flow(...)` draws the window the view gives (an offset from the newest line of the
  filtered merged Flow), not always `m.flow[-rows:]`.

### 6. The filter (`model.py`, `view.py`, `screen.py`)

- One text, matched without case (`casefold`) against a Flow line's board label and project, its
  CR, its who and its text (live-Q7). `Line` gains a `cr` field (empty when none): a record
  event's `cr`, a journal line's `cr` when it has one.
- It narrows the Flow (scroll over the kept lines that match) and the Tasks (a task row is kept
  when its board label and project, its CR, its title or its phase hold the text; the sections'
  titles `to review` and `blocked` are drawn only when a row of theirs is kept, and `no running
  batch` reads `no task matches <text>` when rows exist but none matches). The left column
  (projects, agents) is not filtered.
- The header's counts stay those of everything watched (live-Q7). The footer says
  `filter: <text>` while one is applied.
- It is local (live-Q8): no subscription is added or dropped, nothing more is sent to the server
  (`Link.want` gets the same `wanted()` with or without a filter); clearing it shows everything at
  once. `--only` stays the way to watch fewer projects.

### 7. The footer and no keyboard (`screen.py`)

- With keys: the footer reads `? keys  / filter  q quit`, then `filter: <text>` when one is
  applied (or `/<text>` while typing), then the not-watched projects as today (live-Q17).
- When the input is not a terminal (`sys.stdin.isatty()` false) and the output is: no
  `blessed`, no keys, the screen runs as today (the loop sleeps `REDRAW_S`) and the footer reads
  `Ctrl-C to quit` only; no refusal (live-Q16). A stdout that is not a terminal without `--once`
  stays refused (`NO_TERMINAL`).

### 8. The loop and leaving (`screen.py:run`, `commands/live.py:watch`)

- `run` takes the models, the view, the lock, an `alive` callable (false as soon as any reader
  thread ended), and the terminal (a `blessed.Terminal` by default; a test passes a stand-in with
  the same `cbreak()` and `inkey(timeout)`), and the Rich console as today. With keys it is, in
  this order, `with term.cbreak():` around `with Live(..., screen=True):`; inside,
  `term.inkey(timeout=...)` waits at most until the next second's redraw; a key is given to the
  view and the screen is redrawn at once; without a key, the redraw comes once a second as today
  (the lease times count down). `watch` passes the terminal through to `run` (a parameter with
  the same default), so a test can drive `watch` with no terminal.
- Leaving (live-Q18): `q` and Ctrl-C exit 0. Ctrl-C quits whether it comes as an interrupt
  (`KeyboardInterrupt`, caught by `watch` as today) or as the key `\x03`. On every way out (`q`,
  Ctrl-C, a refused key or protocol on any board, an exception in the drawing, the end of the
  input) both context managers unwind: Rich leaves the alternate screen and shows the cursor,
  `blessed` gives back echo and line mode; then the error, if any, is printed by the CLI as
  today.
- SIGTERM on POSIX (live-Q24): the same way out as Ctrl-C, terminal given back, exit 0: a
  handler, set in `watch` for the run's length and put back after, raises `KeyboardInterrupt` in
  the main thread. Nothing is added on Windows. A killed process (SIGKILL, a closed terminal
  window) cannot give the terminal back: named in the docs as such.
- The three systems: the restore is `blessed`'s and Rich's on Linux, macOS and Windows; the PR
  says where it was tried (see Evidence).

### 9. Read-only and the server (live-Q19, live-Q25)

No server change, protocol 1 unchanged. The client still sends `hello`, `sub`, `unsub` and the
poll, and nothing else; `clients/tui/` still imports nothing of chantier but itself,
`chantier.__version__` and `chantier.core.errors`. This CR does not change `link.py`.

AGENTS.md's `live` sentence, checked word by word: "a read-only terminal client of the surface
server's published API, shipped in `clients/tui/`; it reads the server only (never the planning
folder, the forge or git), writes nothing and messages no agent". With up to 4 boards each is a
surface server read through the same published API; `live` still reads only servers (and, with
no `--url`, `server.json` as today), writes nothing and messages no agent. The sentence stays
true and AGENTS.md is not changed (live-Q25); the count, "one to four boards", is said in
`docs/boards.md` and `docs/server-api.md`.

### 10. Docs

- `docs/boards.md`, "The live terminal view":
  - "How to start it": `--url <link>` repeatable, one to four boards, one key and one connection
    each; a fifth or the same board twice refused (exit 2; two spellings of one host are not
    detected); the recorded board joins others only by its link; `--only` and `--transport`
    apply to every board; a lost board is retried every 5 s while the others go on; a refused
    key on any board exits 4 with the server's sentence and that board's address (never its
    key).
  - "What it shows": the Flow keeps the last 2000 lines of each board, merged by time; several
    boards: the labels `a`..`d`, the header's line per board, `<label>/<project>`.
  - A new list "Keys": the table of section 4, the filter's typing, the help, the pause
    (`paused, <n> new`), the filter's scope (the Flow and the Tasks, counts unchanged, local);
    with no keyboard (input not a terminal), no keys and `Ctrl-C to quit`; the terminal given
    back on every way out (SIGTERM on POSIX included) but a killed process.
  - "Ctrl-C leaves the screen." becomes "`q` or Ctrl-C leaves the screen."; the `--once`
    capture's last line stays `Ctrl-C to quit` (`--once` reads no key and its footer says so):
    `screen.plain` draws the footer of no keys.
- `docs/server-api.md`, "A terminal client": "a read-only terminal view of a running board"
  becomes "of one to four running boards", nothing else.
- No card, agent, hook or web-client change (live-Q21). No `CHANGELOG`-style file beyond what
  the project's release flow writes.

## Decisions carried (02-answers.md)

- ui-night, ui-night scope: this CR is the live TUI item of the UI night, goal a working UI.
  ui-night act concerns the web board's Inbox, not this CR.
- live-Q1: keys (scroll, filter, help, quit) and several boards: sections 1 to 8.
- live-Q2: no Textual, the Rich screen stays: "The key reader", section 8.
- live-Q3: one pinned dependency, `blessed==1.53.0`, no second way: "The key reader".
- live-Q4: the keys: section 4.
- live-Q5: only the Flow scrolls, paused with `paused, <n> new`, End follows: section 5.
- live-Q6: 2000 lines (per board's `Model`), nothing fetched: section 5.
- live-Q7: one text, case-free, Flow and Tasks, counts unchanged, `filter: <text>`: section 6.
- live-Q8: local filter, `--only` unchanged: section 6.
- live-Q9: no opening of a CR's files, no cursor: Out of scope.
- live-Q10: no mouse: Out of scope.
- live-Q11: repeatable `--url`, recorded board by default, at most 4: section 1.
- live-Q12: one board as today; several: labels, header per board: section 2.
- live-Q13: 15 per board, `--only` across boards, `--transport` for all: sections 1, 2.
- live-Q14: a lost board retried, a refused key ends the run with the address: section 2.
- live-Q15: `--once` unchanged in form, waits for every board: section 3.
- live-Q16: no keyboard, no refusal: section 7.
- live-Q17: the footer and the help: sections 4, 7.
- live-Q18: `q` and Ctrl-C exit 0, terminal given back: section 8.
- live-Q19: no server or protocol change, AGENTS.md checked: section 9.
- live-Q20: tests with no terminal, scenario not extended, the PR names the real terminals:
  Evidence.
- live-Q21: `docs/boards.md`, no card change, independent in batch-30: section 10, Overlaps.
- live-Q22: labels `a`..`d` in `--url` order, each mapped to its base address: sections 1, 2.
- live-Q23: the same board twice refused (exit 2), compared on `from_link`'s base, no name
  resolution: section 1.
- live-Q24: SIGTERM on POSIX leaves as Ctrl-C, exit 0, nothing on Windows: section 8.
- live-Q25: AGENTS.md unchanged, "one to four boards" in the docs: sections 9, 10.

## Out of scope

- Opening a CR's files, a cursor to select a CR (live-Q9); the mouse (live-Q10).
- Any server, protocol or API change; a replay of the journal's history older than what the
  subscriptions give (live-Q6).
- A filter sent to the server, or one per board; a filter of the left column.
- Textual or any other application framework; any key reader but `blessed`.
- More than 4 boards; a board started by `live`; detecting two spellings of one host (live-Q23).
- A SIGTERM handler on Windows (live-Q24).
- The `just scenario` workflow (not extended, live-Q20).
- Cards, agents, hooks, the web client, AGENTS.md (live-Q25).

## Overlaps in batch-30 (read 2026-11-21)

Independent of the other batch-30 CRs (live-Q21): no `depends.json`; textual overlaps only,
and whichever lands second rebases.

- CR-429 board-fingerprint-cache (in `4-batch/2-actives/`; its round 2, `work/coder/r2.md`,
  commit c9c0852b on its branch) touches the same files:
  - `skills/chantier/scripts/cli/src/chantier/clients/tui/link.py`: adds `Refusal(ChantierError)`
    with `.sentence` and `.kind` (`key` or `protocol`; message and exit code unchanged for
    `live`), and `Link.client` (the name sent in `hello` and the User-Agent). This CR does not
    edit `link.py`.
  - `skills/chantier/scripts/cli/src/chantier/commands/live.py`: routes `recorded` through
    `hub/state.py:live_server(git_dir)`. This CR edits `commands/live.py` throughout (the
    repeatable `--url`, the boards, `once`, `watch`, the suffix).
  - `skills/chantier/scripts/cli/src/chantier/hub/state.py`: new `live_server`. This CR does not
    edit it.
  - `skills/chantier/scripts/cli/tests/test_live_link.py`: adds a real `Board().link` case
    against the module's server. This CR adds a second server to the module fixture and tests
    over two boards (Evidence 4).
  - the root `pyproject.toml`: adds `watchfiles==1.3.0` to `dependencies` and `"watchfiles"` to
    the same `banned-module-level-imports` line this CR extends with `"blessed"`; and `uv.lock`.
  Whichever lands second: re-runs `uv lock` from the root (never a hand-merged `uv.lock`), keeps
  both dependencies and both banned names, and rebases `recorded` onto `live_server`. The
  board-address suffix (section 2) is added where the link's refusal is caught: CR-429's
  `except Refusal` once it is on `main`, `refused()`'s `ChantierError` caught at
  `link.items()` until then.
- CR-443 gate-hold-narrowing edits `clients/tui/model.py`'s `lease_left` (drops the `held`
  branch and its docstring words), `tests/test_live_model.py` and `docs/server-api.md`. This CR
  does not touch `lease_left`; its `model.py` edits (`FLOW`, the module docstring's count,
  `Line.cr`, the filter's match) are elsewhere in the file; it adds tests to
  `test_live_model.py` and changes one sentence of `docs/server-api.md`'s "A terminal client".
  Whichever lands second rebases.
- CR-439 board-help-page names `chantier live` in the web board's Help and links
  `docs/boards.md`; it does not edit the live section.

## Evidence

Within `just test`'s budget (AGENTS.md: at most 30 s above its 18.5 s of 2026-11-14), few
tests, parametrized, no terminal and no network beyond the module's own servers (live-Q20); the
scenario is not extended.

1. `tests/test_live_model.py` (prepared events, no network), one parametrized test of key
   sequences fed to `view.py` over a model with more lines than a page, each case checking the
   view's state and the text `screen.plain` prints:
   - Up, PgUp, Home move the Flow back (Home shows the oldest kept line); lines arriving while
     scrolled back leave the window unchanged and the title reads `Flow  paused, 3 new`; End,
     and Down to the newest line, follow again (`Flow`);
   - `/`, `C`, `R`, `-`, `2`, Enter: the Flow and the Tasks keep only the lines and rows that
     hold `cr-2` without case, the counts line is unchanged, the footer reads `filter: CR-2`;
     Backspace while typing; Esc clears it; the model's `wanted()` is the same before and after;
   - `?` draws each key of the table; the next key closes it and does nothing else;
   - `q` and `ctrl-c` say quit; an unbound key (`x`) changes nothing.
2. The same file, the cap (section 5): two models each fed 2100 lines keep 2000 each, the merged
   view holds 4000 in time order, and Home shows the oldest kept line of the merged view (the
   oldest of the two boards' kept lines); one more line on a board while scrolled to Home moves
   the view to the new oldest kept line, no further.
3. The same file: the keystroke mapping of `screen.py`, parametrized over
   `blessed.keyboard.Keystroke` objects built by hand (`KEY_UP`, `KEY_PGDOWN`, `KEY_HOME`,
   `KEY_ESCAPE`, `KEY_ENTER`, `KEY_BACKSPACE`, `/`, `q`, `\x03`), no terminal opened.
4. The same file: the footer with no keys reads `Ctrl-C to quit` only; with keys, `? keys  /
   filter  q quit`.
5. The same file (or `test_live_link.py`, the Driver's choice), one parametrized test driving
   `watch` (and through it `screen.run`) with a stand-in terminal and stand-in links, no terminal
   and no network: the stand-in's `cbreak()` is a context manager recording its entry and exit;
   its `inkey(timeout)` returns scripted keystrokes or raises; the Rich console writes to an
   `io.StringIO`. Five exits:
   - `q`: `watch` returns normally (the command's exit 0);
   - `\x03` as a key: returns normally;
   - `inkey` raising `KeyboardInterrupt`: returns normally;
   - a reader refusal (a stand-in link whose `items()` raises the link's refusal, so `alive`
     turns false): `watch` raises it, with `(board <base>)` at its end;
   - an exception in `render` (patched to raise): `watch` raises it.
   Each case asserts that cbreak's exit ran (entry and exit recorded, in that order).
6. `tests/test_live_link.py`: the module fixture starts a second server (port 0, same
   repository, no second `server.json`); `chantier live --once --url <a> --url <b>` prints both
   boards' header lines (their base addresses, `live`), `a/proj` and `b/proj`, the working CR as
   `a CR-...` and `b CR-...`, and no key in the output. One parametrized refusal test: five
   `--url` (exit 2, `at most 4`), the same link twice (exit 2, `given twice`), `--only nope` over
   two boards (exit 2, the exact sentence `--only nope: no board serves it; served: a/<x>,
   b/<y>`, asserted whole, so it carries no board address), `--only nope` over one board (exit
   2, the exact sentence `--only nope: the board serves <ids>`, asserted whole, no board
   address), and a wrong key on the second board (exit 4, the server's sentence and
   `(board http://127.0.0.1:<port>/)`, and the wrong key not in stderr).
7. The existing tests stay green unchanged in intent: the one-board `--once` capture,
   `test_a_wrong_key_exits_4_with_the_servers_sentence` (its sentence still in stderr, now with
   the board's address), the command line's refusals, and the import check of `clients/tui/`
   (which reads the shipped modules from the repository at the head under test, `view.py`
   included).
8. `tests/test_board.py`: `LAZY` holds `blessed`, and the lazy-import check (it reads the shipped
   `src/` and the shipped `pyproject.toml` at the head under test) finds no module-level import
   of it.
9. `just check` (lint refuses a stale `uv.lock`) and `just eval-dry-run` in the worktree before
   the first push (a change under the CLI's `src/`); the pipeline's `just scenario
   (ubuntu-latest)` green at the PR's head (a CLI change).
10. In a real terminal, by the Driver: the keys, the pause, the filter, the help, `q`, Ctrl-C, a
   refused key on a second board, each leaving a usable terminal (echo, cursor, line mode). On
   Windows this is also the proof of `blessed`'s key decoding ("The key reader"). The PR's
   Deliverables name the systems tried, Windows among them; a system not tried is named in the
   Known gaps as "keys not tried in a real terminal on <system>" (live-Q20), and Windows not
   tried leaves Windows key decoding unproved, named there too.

The PR's Deliverables give `just test`'s measured time at the PR's head (the system it ran on)
beside the AGENTS.md budget (at most 30 s above 18.5 s, measured on the user's Windows machine).

Host and default matrix: none; the CR depends on no host and no configured value. The system
matters only for the real-terminal check of item 10, which names each system.

## Decided questions (v1's open questions)

1. **The board's label with several boards** (live-Q22): a letter `a`..`d` in `--url` order, each
   mapped to its base address on its header line.
2. **The same board given twice** (live-Q23): refused at start, `--url <base>: given twice`
   (exit 2), compared on `from_link`'s base with no name resolution.
3. **SIGTERM on POSIX** (live-Q24): the same way out as Ctrl-C, terminal given back, exit 0;
   nothing added on Windows.
4. **AGENTS.md's `live` sentence** (live-Q25): unchanged; `docs/boards.md` and
   `docs/server-api.md` say "one to four boards".

No question is left open.

# Tell a dev session when the surface server runs a foreign build

Spec v2 (2026-11-21). Short name: `foreign-build`. Priority P3. Split out of
`sync-blocked-by-others` (CR-436 of batch-30), its answer sync-lock-Q12. No grill was held: the
user delegated the night's spec questions to a Fable advisor ("plus de question"); its answers,
foreign-build-Q1 to Q6, are in `02-answers.md` and carried below (section "Decisions").

## Goal

In the user's terms: when I work on chantier itself (dev mode) and the board, with its writer and
the forge hub it holds, that serves my surface was started by another project's session (Studio)
from a cached build, I am told so in one line, even when the version string is the same. Nothing
is stopped or restarted for me, and the line gives no advice: it reports the foreign build only.

Measured basis: 2026-11-14, a board with no Triage view, served by an old build at the same
version. With CR-436, another project's session runs `uvx --from "<chantier checkout>"`, a build
that uv caches by version, and it may be the one that starts the surface-wide processes
(sync-lock-Q12, accepted with no notice). Today every check compares the version string only:
`hub/state.py:other_version` (behind `hub/autostart.py:board_clause`, `hub/lines.py:board_lines`
and `hub_line`, `hub/watch.py:Watch.start_line`, `writer/lines.py:older_board`) and
`board/command.py` (`_recorded`, `_answering`).

## Order in batch-30 and overlaps

Destination: batch-30, after CR-436 and CR-429, before CR-447 `docs-gardening` (foreign-build-Q5).
The CR folder holds `depends.json`: `{"after": ["sync-blocked-by-others",
"board-fingerprint-cache"]}`. This CR is written against the code as those two leave it; places
are found by text on that merged head, not by line number.

- **CR-436 `sync-blocked-by-others`**: adds `plugin_files.is_chantier_project(repo)` and makes the
  dev mode `is_dev_checkout() and is_chantier_project(repo)`; this CR uses that same test. CR-436
  also writes the sync-lock-Q12 sentence ("a chantier session sees no notice while the version
  string is equal ... the inbox item `surface-server-foreign-build`") in `AGENTS.md`,
  `CONTRIBUTING.md` and `skills/chantier/references/session-start.md`; this CR rewrites that
  sentence (section 5).
- **CR-429 `board-fingerprint-cache`**: rewrites `hub/watch.py` (the watcher becomes a subscriber
  and starts the board; it is no longer the hub), the start line's board clause (`board is
  chantier <v>: restart it to run this version`), `hub/lines.py:hub_line` (its `a watcher` branch
  goes), `writer/lines.py:START`, and the board's start in `board/command.py`. After it, the hub
  is always the server's process.
- **CR-446 `live-several-boards-and-keys`**: reads `server.json` through
  `hub/state.py:live_server` and does not edit `hub/state.py`; no conflict. `chantier live` keeps
  showing the board's `version` only (out of scope).
- **CR-449 `board-griller`**: quotes `writer/lines.py`'s `writer:` line; this CR does not change
  that text.
- **CR-447 `docs-gardening`** comes after this CR.

## What changes

### 1. A build's identity in `chantier/server.json` (foreign-build-Q1)

- `hub/state.py`: a new `build_source() -> str`, the resolved folder of the loaded `chantier`
  package, POSIX form (`Path(chantier.__file__).resolve().parent.as_posix()`). In the dev mode it
  is `<plugin root>/skills/chantier/scripts/cli/src/chantier` (the project is installed editable
  by `uv sync`); in a `uvx --from` build it is a folder of uv's cache. Two processes run the same
  build when their `source` is equal.
- `write_server(...)` and `hub_record(...)` add `"source": build_source()` to the entry. The
  `hub` entry's `source` is for the record only: no line reads it (the hub is the server's
  process, section 3). The `writer` entry gets no field: the writer is a thread of the server's
  process (same PID, same build).
- The module docstring of `hub/state.py` (the one doc that lists `server.json`'s fields) adds
  `source` to the `server` entry's fields and to the `hub` entry's, with one clause: "the resolved
  folder of the loaded `chantier` package; the `hub` entry's is for the record only".
- A new `other_build(record, version, source) -> str | None`: None when the record is None, when
  its `version` differs (that case stays `other_version`'s, unchanged) or when its `source` equals
  `source`; else the record's `source`, or the module constant `UNKNOWN` when the entry holds no
  `source` (an entry written by a build of the same version from before this
  CR, foreign-build-Q4). `other_version` is unchanged.
- No content hash, no git commit, no launch command is recorded.

### 2. Who is told (foreign-build-Q3)

Only a session in the dev mode: `plugin_files.is_dev_checkout() and
plugin_files.is_chantier_project(repo)` (CR-436's test), with `own = build_source()`. A session in
the plugin mode (Studio, any user's project) runs a cached build itself and is told nothing new.
The version-string lines of today stay for every session.

### 3. Where it is said (foreign-build-Q2, foreign-build-Q6)

The notice clause, one text in one place (a function in `hub/lines.py`, used by the three
callers), `<what>` always `board`, `<v>` the entry's version, `<source>` the entry's:

- recorded source: `board runs another build of chantier <v> (<source>), not this checkout's`
- no source (`UNKNOWN`): `board runs a build of chantier <v> older than this notice (source
  unknown), not this checkout's`

It carries no advice: no stop command, no restart, no "for the Chief of Staff" instruction.

- `status`: `hub/lines.py:board_lines(repo)` prints, when the live `server` entry is of this
  version and `other_build` names it, one `board:` line with the clause (in place of nothing
  today). `hub_line(repo)` is unchanged: it has no foreign-build branch.
- The watcher's start line: `hub/watch.py:Watch.start_line` appends `; ` and the clause where
  today it appends the `board is chantier <v>` clause, and only when that version clause is
  absent.
- `board --seat <id>` (`board/command.py`): when the running board is the one the record names
  (`_recorded`) and its version is this one, and the dev-mode test of section 2 holds for
  `open_projects().home`, the `board already running at <url>` output (`_running_lines`) gains one
  line, the clause. In a surface with several projects and no `--project` (`open_projects()` took
  its `SurfaceChoice` branch, so `home` is only the first project, not the session's), it prints
  no line. It is not a refusal: the seat is registered as today and the exit code is unchanged.
  `_answering` (no record, a board found at the configured address) adds nothing: its probe
  answer carries no `source`, and this CR changes no published API.
- `writer/lines.py:older_board` is unchanged (a version test).

### 4. Never a kill or a restart

No code stops, signals or restarts a process. The Chief of Staff says the line once to the user
and never stops or restarts the board:

- `skills/chantier/references/chief-of-staff.md`, the sentence "The `board:` line of `status` and
  the start line's `board is chantier <v>`: say it once to the user with the restart; never stop
  or restart the board yourself" gains, after it, one sentence: "A `board runs another build` or
  `board runs a build of chantier <v> older than this notice` line (on `status`, the start line or
  `board`): say it once to the user as printed; never stop or restart the board."
- `skills/chantier/references/session-start.md`, its `board already running at` bullet: one
  sentence, "an added `board runs another build` line: say it once to the user as printed, never
  stop or restart the board".

### 5. The sync-lock-Q12 sentence (CR-436)

In the three places CR-436 writes it (`AGENTS.md`'s bullet, `CONTRIBUTING.md`,
`skills/chantier/references/session-start.md`), "a chantier session sees no notice while the
version string is equal" becomes "a chantier session in the dev mode is told, on `status`, the
watcher's start line and `board`, when the board runs another build than its checkout's, even at
the same version string (`server.json` records each entry's `source`)"; the end of the sentence
("refreshed at the next version bump, or when the process is stopped by hand and a chantier session
starts it again") stays; "a notice of a foreign build is out of scope: the inbox item ..." is
removed. The wording is found by text on CR-436's merged head.

## Out of scope

- A kill, a stop or an automatic restart of any process, and any advice on how to get one's own
  build (foreign-build-Q6).
- Which build starts the surface server when several projects' watchers hold seats: the follow-up
  inbox item "which build starts the surface server when several projects' watchers hold seats",
  filed by the Chief of Staff.
- A board started from the same checkout before a local edit (same `source`, older code in
  memory): not a foreign build (foreign-build-Q1).
- A notice in a plugin-mode session (foreign-build-Q3), on the web board, in `chantier live`, or in
  the published API (`hello`/probe answers) (foreign-build-Q2).
- A line reading the `hub` entry's `source`.
- `writer/lines.py`'s refusal texts and `older_board`.
- Any change to how a build is launched or cached (CR-436, sync-lock-Q7 and Q12 stand).

## Host and default matrix

The notice depends on the mode of the install, not on the host:

| Session | Surface processes | Result |
|---|---|---|
| dev mode (chantier, `.git` plugin root) | started by this or another dev session (same `source`) | no new line |
| dev mode | started from a plugin-mode session (uv cache `source`), same version | the clause on `status`, the start line, `board --seat` |
| dev mode | same version, entry with no `source` | the "older than this notice (source unknown)" clause |
| dev mode | another version | today's version lines only |
| dev mode, `board --seat` in a multi-project surface with no `--project` | foreign build | no line on `board`; `status` and the start line as above |
| plugin mode (another project) | any | today's version lines only |

Claude Code and Copilot read the same cards and run the same CLI: no host difference.

## Evidence

Tests (in-process, few, parametrized, in the existing files that cover these lines):

- `tests/test_watcher_autostart.py` (next to
  `test_the_seat_of_another_session_gets_no_line_and_a_status_names_a_board_of_another_version`):
  one parametrized test over the matrix's rows, writing the `server` entry (a live PID, the
  test's own) with `version` = `__version__` and `source` = this build's, a cache-like path, or
  none, and `is_dev_checkout`/`is_chantier_project` patched true or false; it asserts `status`'s
  `board:` line (the recorded-source clause, the unknown-source clause, or absent), and that no
  line holds a stop command or "restart". `other_build`'s outcomes (same, other, missing, other
  version) are covered by these rows, not a test of their own; `write_server` and `hub_record`
  holding `source` is asserted in the same test.
- `tests/test_forge_hub.py` (next to
  `test_the_start_line_names_the_hub_and_a_hub_of_another_version`): the start line with a board
  of another build gets the clause; with another version, only the version clause.
- `board --seat` cases (parametrized): a recorded board answering at this version with another
  `source`, in a single-project folder: the output holds `board already running at` and the
  clause, exit 0, the seat registered; the same in a surface with several projects and no
  `--project`: no clause, exit 0, the seat registered.
- The cards: the structure tests that read `chief-of-staff.md` and `session-start.md` read them
  from the repository at the head under test; the added sentences are checked there, not in a
  prepared text.
- `just check`; `just eval-dry-run` (a change under the CLI's `src/`); `just scenario
  (ubuntu-latest)` green at the PR's head (a CLI and cards change). The scenario needs no new
  step: a scenario run has one build only, so it proves the no-line row; the foreign rows are
  proved by the tests.
- A real-session check, labelled untested until done: from a Studio session (plugin mode), start
  the board; then a chantier dev session's `status` shows the clause.

## Decisions

From `02-answers.md` (2026-11-21, Fable advisor, in the user's place):

1. **foreign-build-Q1, A.** A build is identified by `source`, the resolved folder of the loaded
   package, in the `server` and `hub` entries; no content hash.
2. **foreign-build-Q2, A.** Said on `status`'s `board:` line, the watcher's start line, and one
   added non-refusing line on `board --seat`; the published API is not changed.
3. **foreign-build-Q3, A.** Dev-mode chantier sessions only (CR-436's test).
4. **foreign-build-Q4, A.** A same-version entry with no `source` is told, as a build older than
   this notice of unknown source.
5. **foreign-build-Q5, A.** batch-30, after CR-436 and CR-429, before CR-447; `depends.json`
   `{"after": ["sync-blocked-by-others", "board-fingerprint-cache"]}`.
6. **foreign-build-Q6, C.** The notice reports the foreign build only, with no stop or restart
   advice; the Chief of Staff says it once and never stops or restarts the board; "which build
   starts the surface server when several projects' watchers hold seats" becomes an inbox item.

No open question.

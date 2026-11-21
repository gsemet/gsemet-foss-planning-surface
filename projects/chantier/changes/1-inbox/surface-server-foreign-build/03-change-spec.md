# Tell a dev session when the surface server runs a foreign build

Spec v1 (2026-11-21). Short name: `foreign-build`. Priority P3. Split out of
`sync-blocked-by-others` (CR-436 of batch-30), its answer sync-lock-Q12. No grill was held: the
user delegated the night's spec questions to a Fable advisor ("plus de question"); every open
choice is a numbered question at the end (foreign-build-Q1 to Q5), and the text below is written,
provisionally, on the recommended option of each (marked "provisional, Qn").

## Goal

In the user's terms: when I work on chantier itself (dev mode) and the board, its writer or the
forge hub that serves my surface was started by another project's session (Studio) from a cached
build, I am told so in one line, with how to get my own build, even when the version string is
the same. Nothing is stopped or restarted for me.

Measured basis: 2026-11-14, a board with no Triage view, served by an old build at the same
version. With CR-436, another project's session runs `uvx --from "<chantier checkout>"`, a build
that uv caches by version, and it may be the one that starts the surface-wide processes
(sync-lock-Q12, accepted with no notice). Today every check compares the version string only:
`hub/state.py:other_version` (behind `hub/autostart.py:board_clause`, `hub/lines.py:board_lines`
and `hub_line`, `hub/watch.py:Watch.start_line`, `writer/lines.py:older_board`) and
`board/command.py` (`_recorded`, `_answering`).

## Order in batch-30 and overlaps

This CR is written against the code as batch-30 leaves it. It lands after, and is rebased on:

- **CR-436 `sync-blocked-by-others`** (2-actives): adds `plugin_files.is_chantier_project(repo)`
  and makes the dev mode `is_dev_checkout() and is_chantier_project(repo)`; this CR uses that
  same test. CR-436 also writes the sync-lock-Q12 sentence ("a chantier session sees no notice
  while the version string is equal ... the inbox item `surface-server-foreign-build`") in
  `AGENTS.md`, `CONTRIBUTING.md` and `skills/chantier/references/session-start.md`; this CR
  rewrites that sentence (section 5). `depends.json`: `{"after": ["sync-blocked-by-others"]}`.
- **CR-429 `board-fingerprint-cache`** (2-actives): rewrites `hub/watch.py` (the watcher becomes a
  subscriber and starts the board; it is no longer the hub), the start line's board clause (`board
  is chantier <v>: restart it to run this version`), `hub/lines.py:hub_line` (its `a watcher`
  branch goes), `writer/lines.py:START`, and the board's start in `board/command.py`. This CR edits
  the same lines: `depends.json` also names it (`{"after": ["sync-blocked-by-others",
  "board-fingerprint-cache"]}`). Places are found by text on that merged head, not by line number.
- **CR-446 `live-several-boards-and-keys`** (1-pending): reads `server.json` through
  `hub/state.py:live_server` and does not edit `hub/state.py`; no conflict, but `chantier live`
  shows the board's `version` and this CR does not change it (out of scope, Q2).
- **CR-449 `board-griller`** (1-pending): quotes `writer/lines.py`'s `writer:` line; this CR does
  not change that text.
- **CR-447 `docs-gardening`** (1-pending) comes after every batch-30 CR; this CR, if it joins
  batch-30, goes before it or the docs it touches are gardened later.
- CR-426 `board-exposure` (3-done) touched `_another_version`'s callers; merged, nothing to order.

## What changes

### 1. A build's identity in `chantier/server.json` (provisional, Q1)

- `hub/state.py`: a new `build_source() -> str`, the resolved folder of the loaded `chantier`
  package, POSIX form (`Path(chantier.__file__).resolve().parent.as_posix()`). In the dev mode it
  is `<plugin root>/skills/chantier/scripts/cli/src/chantier` (the project is installed editable
  by `uv sync`); in a `uvx --from` build it is a folder of uv's cache. Two processes run the same
  build when their `source` is equal.
- `write_server(...)` and `hub_record(...)` add `"source": build_source()` to the entry. The
  `writer` entry gets no field: the writer is a thread of the server's process (same PID, same
  build). The module docstring lists `source` among each entry's fields.
- A new `other_build(record, version, source) -> str | None`: None when the record is None or its
  `version` differs (that case stays `other_version`'s, unchanged); else, when its `source` is not
  `source`, the record's `source`, or `unknown` when the entry holds none (an entry written by a
  build of the same version from before this CR). `other_version` is unchanged.
- No content hash, no git commit, no launch command is recorded (Q1, options B and C).

### 2. Who is told (provisional, Q3)

Only a session in the dev mode: `plugin_files.is_dev_checkout() and
plugin_files.is_chantier_project(repo)` (CR-436's test), with `own = build_source()`. A session in
the plugin mode (Studio, any user's project) runs a cached build itself and is told nothing new.
The version-string lines of today stay for every session.

### 3. Where it is said (provisional, Q2)

The notice clause, one text in one place (a constant or function in `hub/lines.py`, used by the
three callers), with `<what>` `board` or `hub` and `<source>` the entry's:

`<what> runs another build of chantier <v> (<source>), not this checkout's: for the Chief of
Staff: tell the user once to stop it (<stop command>), then start it again from this session`

`<stop command>` is `board/running.py:stop_command(<pid>)` of the entry.

- `status`: `hub/lines.py:board_lines(repo)` prints, when the live `server` entry is of this
  version and `other_build` names it, one `board:` line with the clause (in place of nothing
  today). `hub_line(repo)` appends `; hub runs another build (<source>)` when the live `hub`
  entry's PID is not the server's and `other_build` names it (after CR-429 the hub is always the
  server's process, so the `board:` line already says it and the hub line adds nothing; the
  branch stays for an entry whose PIDs differ).
- The watcher's start line: `hub/watch.py:Watch.start_line` appends `; board runs another build
  (<source>): <the clause's advice>` where today it appends the `board is chantier <v>` clause,
  and only when that version clause is absent.
- `board --seat <id>` (`board/command.py`): when the running board is the one the record names
  (`_recorded`) and its version is this one, the `board already running at <url>` output gains
  one line, the clause with `<what>` `board`. It is not a refusal: the seat is registered as today
  and the exit code is unchanged. `_answering` (no record, a board found at the configured
  address) adds nothing: its probe answer carries no `source`, and this CR changes no published
  API (Q2).
- `writer/lines.py:older_board` is unchanged (a version test).

### 4. Never a kill or a restart

No code stops, signals or restarts a process; the clause asks the Chief of Staff to tell the user
once. The cards say so:

- `skills/chantier/references/chief-of-staff.md`, the sentence "The `board:` line of `status` and
  the start line's `board is chantier <v>`: say it once to the user with the restart; never stop
  or restart the board yourself" becomes "... and the start line's `board is chantier <v>` or
  `board runs another build`: say it once to the user with the stop command as printed; never stop
  or restart the board yourself; after the user stops it, start it again on the user's word".
- `skills/chantier/references/session-start.md`, its `board already running at` bullet: one
  sentence for the added `runs another build` line, same handling.

### 5. The sync-lock-Q12 sentence (CR-436)

In the three places CR-436 writes it (`AGENTS.md`'s bullet, `CONTRIBUTING.md`,
`skills/chantier/references/session-start.md`), "a chantier session sees no notice while the
version string is equal" becomes "a chantier session in the dev mode is told, on `status`, the
watcher's start line and `board`, when one of them runs another build than its checkout's, even at
the same version string (`server.json` records each entry's `source`)"; the end of the sentence
("refreshed at the next version bump, or when the process is stopped by hand and a chantier session
starts it again") stays; "a notice of a foreign build is out of scope: the inbox item ..." is
removed. The AGENTS.md wording is found by text on CR-436's merged head.

### 6. Docs

`docs/server-api.md` (or the doc that lists `server.json`'s fields, found by text `served`):
`source` added to the `server` and `hub` entries, one sentence. No change to the published API.

## Out of scope

- A kill, a stop or an automatic restart of any process (the request).
- A board started from the same checkout before a local edit (same `source`, older code in
  memory): not a foreign build (Q1, option B would cover it).
- A notice in a plugin-mode session (Q3), on the web board, in `chantier live`, or in the published
  API (`hello`/probe answers) (Q2).
- `writer/lines.py`'s refusal texts and `older_board`.
- Any change to how a build is launched or cached (CR-436, sync-lock-Q7 and Q12 stand).

## Host and default matrix

The notice depends on the mode of the install, not on the host:

| Session | Surface processes | Result |
|---|---|---|
| dev mode (chantier, `.git` plugin root) | started by this or another dev session (same `source`) | no new line |
| dev mode | started from a plugin-mode session (uv cache `source`), same version | the clause on `status`, the start line, `board` |
| dev mode | same version, entry with no `source` | the clause with `unknown` |
| dev mode | another version | today's version lines only |
| plugin mode (another project) | any | today's version lines only |

Claude Code and Copilot read the same cards and run the same CLI: no host difference.

## Evidence

Tests (in-process, few, parametrized, in the existing files that cover these lines):

- `tests/test_watcher_autostart.py` (next to
  `test_the_seat_of_another_session_gets_no_line_and_a_status_names_a_board_of_another_version`):
  one parametrized test over the matrix's rows, writing the `server` entry (a live PID, the
  test's own) with `version` = `__version__` and `source` = this build's, a cache-like path, or
  none, and `is_dev_checkout`/`is_chantier_project` patched true or false; it asserts `status`'s
  `board:` line (present with the clause and the stop command, or absent).
- `tests/test_forge_hub.py` (next to
  `test_the_start_line_names_the_hub_and_a_hub_of_another_version`): the start line with a board
  of another build gets the clause; with another version, only the version clause.
- A `board --seat` case where a recorded board answers at this version with another `source`:
  the output holds `board already running at` and the clause; exit 0; the seat registered.
- `hub/state.py`: `write_server` and `hub_record` hold `source`; `other_build`'s three outcomes
  (same, other, missing) in the same parametrized test as the status rows, not a test of its own.
- The cards: the structure tests that read `chief-of-staff.md` and `session-start.md` read them
  from the repository at the head under test; the changed sentences are checked there, not in a
  prepared text.
- `just check`; `just eval-dry-run` (a change under the CLI's `src/`); `just scenario
  (ubuntu-latest)` green at the PR's head (a CLI and cards change). The scenario needs no new
  step: a scenario run has one build only, so it proves the no-line row; the foreign rows are
  proved by the tests.
- A real-session check, labelled untested until done: from a Studio session (plugin mode), start
  the board; then a chantier dev session's `status` shows the clause.

## Open questions

1. **foreign-build-Q1: how a build is identified.**
   - **A (recommended).** `source`: the resolved folder of the loaded `chantier` package, in the
     `server` and `hub` entries; different folder = foreign build. Exact for "not this checkout's"
     (a uv cache folder versus the checkout's `src/`), free to compute, no false notice while the
     user edits the checkout.
   - B. A plus a content hash of the package's files at the process's start: also tells a board
     started from this checkout before an edit (stale code in memory). Catches more, but every
     edit of `src/` in a dev session makes the running board "foreign": a notice at almost every
     `status` during a CR's work.
   - C. The launch form (`dev` or `plugin`, from `cli_command`): coarser; a board started by
     hand has no known form, and two plugin installs of different builds look the same.
2. **foreign-build-Q2: where the notice is said.**
   - **A (recommended).** `status`'s `board:` line, the watcher's start line, and one added line
     (not a refusal) on `board --seat` when the recorded board is of another build: the measured
     case is a session running `board` and silently reusing the foreign build.
   - B. `status` and the start line only (the intake's sketch).
   - C. A, plus the published API (`hello`, the probe answer) and the web board / `chantier live`
     showing the build: a protocol change, and other clients' work.
3. **foreign-build-Q3: which sessions are told.**
   - **A (recommended).** Dev-mode chantier sessions only (CR-436's test): the plugin mode runs a
     cached build itself; comparing would only report other plugin installs.
   - B. Every session whose `source` differs from the entry's (a Studio session told of a board
     that a chantier dev session started).
4. **foreign-build-Q4: an entry of the same version with no `source`** (written by a build from
   before this CR, at the same version string).
   - **A (recommended).** Told, as `another build (unknown)`: that build is older than this CR by
     definition.
   - B. Silent: only a recorded, different `source` is told.
5. **foreign-build-Q5: destination.**
   - **A (recommended).** batch-30 (running), last of the server CRs: after CR-436 and CR-429
     (`depends.json` as section "Order"), before CR-447 `docs-gardening`; it is small (one state
     field, three lines, two card sentences).
   - B. The next batch: batch-30 is already full of edits to `hub/watch.py`, `board/command.py`
     and the cards this CR touches.

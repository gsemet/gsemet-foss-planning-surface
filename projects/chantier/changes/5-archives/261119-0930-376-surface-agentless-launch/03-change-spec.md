# Change Specification: a board started by hand serves a planning surface with no agent

## Goal

The user runs chantier's board, and the surface's autosync through it, with no Chief of Staff
and no plugin: `uvx --from git+https://github.com/gsemet/chantier@v<version> chantier board`
from the surface's root. Such a board keeps serving until the user stops it, even when a Chief of
Staff session comes, registers its seat on it, and goes.

Most of the intake already exists at chantier's `main` (3a9afc2c, v0.13.0); `01-intent.md`
lists what and where. What is left in chantier is one rule of the board's lifetime and the docs.

## What changes

### 1. The board's lifetime (`skills/chantier/scripts/cli/src/chantier/board/`)

Today (`seats.py`, `Seats`): "A board with none stops on Ctrl-C only; one that had some stops
when none of them is still named by its project's `seat.json`." A board started by hand gets its
first seat when a session runs `board --seat <id>` against it (`POST /api/seats`), and then stops
when that session's seat moves or is left.

New rule:

- **A board started with `--seat`**: unchanged. It follows every seat that registers on it and
  stops (exit 0) when none of them is still named by its project's `seat.json`, checked at least
  every `SEAT_CHECK_S` (10 s) and at each request; an unreadable seat file counts as held.
- **A board started with no `--seat`** (by hand): it stops only when stopped by hand (Ctrl-C, or
  the stop command a refused `board` prints). A later `board --seat <id>` against it still
  registers its seat (`POST /api/seats` answers `{"seats": <n>, ...}` as today, `board already
  running at <link>` is printed as today) and `/api/board`'s `seats` still counts it; a seat
  that moves or is left never stops it.

Code:

- `seats.py`: `Seats.__init__(self, projects, follows: bool = True)`. With `follows=False`,
  `add()` records the seat and returns as today but starts no watch; `arm()` starts none; `gone()`
  returns `False`. Rewrite the class docstring to the two rules above.
- `command.py`, `board()`: `Seats(projects, follows=bool(args.seat))`. `_run`'s docstring: "Serve
  until Ctrl-C, or, for a board started with `--seat`, until its seats leave."
- `routes.py`: unchanged (`_judged` calls `ctx.seats.gone()`, which stays false).
- `declare/board.py`, `--seat` help: "the Chief of Staff session this board is for: the board
  follows its seats and stops when none of them names its session any more; with none, it serves
  until stopped by hand".
- The existing callers in tests (`Seats(projects)`) keep the default, unchanged.

No message, exit code, route or file format changes.

### 2. Docs (chantier's repository)

- `docs/web-board.md`:
  - "Starting the board" (the paragraph "It stops when its session leaves the seat."): "Started
    by a session, it stops when that session leaves the seat; started by hand, it serves until you
    stop it."
  - "When it stops.": "With Ctrl-C. A board a session started (`--seat`) also stops by itself once
    no session that registered a seat holds it any more; a board started by hand (no `--seat`)
    does not, even when sessions register a seat on it and leave." The rest of the item stays.
  - "By hand.": add one sentence: from the surface's root, with no `--project`, the board serves
    every project of the surface; it runs until you stop it, so a scheduled task or a service may
    start it (the surface's own setup; chantier ships none).
- `docs/planning-modes.md`, "The surface's autosync", the "The board" item: replace "joins the
  group once, at a fresh start (never when it reuses a running board), as `join . ...`" with what
  the code does (`board/autosync_api.py`): starting the board joins nothing; the board's Start
  runs `start . --enable-only`, then joins once as `join . --owner-pid <its pid> --harness generic
  --session-id chantier-board`, so the board's process owns that participant, which leaves when
  the board stops. Keep Stop, Approve, the blocked state and the `board: autosync not joined`
  line as they are.
- `docs/planning-modes.md`, a new short section after "The surface's autosync", "With no agent":
  start the board from the surface's root with
  `uvx --from git+https://github.com/gsemet/chantier@v<version> chantier board` (the version
  the surface's planners use); click Start for the autosync; the board serves and keeps the group
  joined until you stop it. A Chief of Staff session that starts later reuses it (`board already
  running at`), and its leaving does not stop it. A session running another chantier version is
  refused with the board's version, PID and stop command, as today (`docs/web-board.md`, "When it
  stops"): keep the surface's pinned version on the planners' release.

The cards need no change: `session-start.md` already says a second session's `board --seat`
registers its seat and prints `board already running at`; `chief-of-staff.md`'s "Its board stops
by itself when the seat moves" is about a board the Chief of Staff started with `--seat`, still
true.

### 3. The scenario (`scenario/run_scenario.py`, the board unit)

The step after "the board whose seats are gone stops by itself" (today: "a board that had no seat
takes its first over `POST /api/seats`, then stops by itself when that session goes") becomes:

- start `late = board("board", "--host", "127.0.0.1", "--port", 0)` (no `--seat`), as today;
- `board ... --port <its port> --seat s-4`: exit 0, stdout starts with `board already running at`,
  `/api/board` answers `seats == 1`;
- `w.chantier("seat", "take", "s-5", "--over", "s-4")`, then one `GET /api/board` (the board
  checks its seats at each request, the same `gone()` its watch would call; a board started by
  hand starts no watch, so no wait is needed and the scenario's time does not grow); check "a
  board started by hand registers a session's seat and keeps serving when that session goes":
  `late.p.poll() is None` and a second `GET /api/board` answers 200;
- the board is then stopped by the unit's own cleanup (`BoardProc`'s close, as every board of the
  unit); no further check.

Update the matching bullet of `scenario/README.md` (the board unit's list) to the new wording.

## Out of scope

- The planning surface's repository (`gsemet-foss-planning-surface`): `just board`, `just sync`,
  one place for the pinned version (today `CHANTIER_REF` in `scripts/validate-bundles.py`, at
  `v0.11.0`), a bump recipe, an autostart. **Follow-up in the surface**: a `justfile` recipe
  `board` running `uvx --config-file uv.toml --from git+https://github.com/gsemet/chantier@<ref>
  chantier board`, the ref shared with `validate` in one place; `sync` calling the surface's own
  `scripts/ai-autosync-git.py` (or dropped in favour of the board's Start); optionally a scheduled
  task or service starting `just board`; its `README.md` "Git autosync" section updated to the
  board.
- Replacing or porting the surface's autosync script into chantier (CR-227, option A).
- A session's `board --seat` against a hand-started board of another chantier version: refused as
  today; no change.
- Stopping a hand-started board from the page: no new button.

## Host and default matrix

None: the rule depends neither on the host (Claude Code, Copilot) nor on a configured value; it
depends only on whether `--seat` was given.

## Evidence

- `just scenario` (ubuntu-latest in CI; locally on Windows for the batch's top CR, per
  `AGENTS.md`): the board unit's new step above passes, and its earlier checks still pass ("when
  the seat moves the board stops by itself", "the seat moving from s-2 to s-3 keeps the board
  running", "the board whose seats are gone stops by itself"), which prove a `--seat` board keeps
  today's rule.
- `just check` passes (lint, types, `just test` within its time budget). `just eval-dry-run`, as
  the change is under the CLI's `src/`.
- No pytest is added: the behaviour belongs to the scenario (`tests/test_board.py`'s docstring).

## Open questions

- **Q1.** A board started by hand (no `--seat`) keeps serving after a Chief of Staff session that
  registered its seat on it leaves; today it stops then. This follows the intake ("run with no
  session open") and CR-222's specification ("A board started with no `--seat` (by hand) stops
  only on Ctrl-C"), against the reading the code took in CR-222's round 2. Recommended: yes, as
  specified here.

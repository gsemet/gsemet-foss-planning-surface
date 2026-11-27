# TUI: wider default columns in live, narrowed on a small terminal

## Goal, in the owner's words

In `chantier live`, three columns cut their text today: the left column (the Projects and Agents
boxes), and the Flow table's Project and Who columns. The owner wants them wider by default
(`intake/request.md`, 2026-11-27, verbatim in French there): the left column 50 % wider, Project
twice as wide, Who 1.5 times as wide (answers 2 and 6). On a terminal too narrow for these
widths, the columns close up again before anything disappears (answer 5).

The owner split the request (answer 4): this change request holds the wider defaults and what
gives way on a narrow terminal, nothing else. Resizing with the mouse and keeping the widths are
`tui-mouse-resize`, stacked on this one (its `depends.json`: `{"after": ["tui-resize-columns"]}`).
The batch that carries both is a stack batch (answer 1).

## What changes

All paths below are under `skills/chantier/scripts/cli/src/chantier/`.

### 1. The default widths (`clients/tui/parts.py`, `clients/tui/screen.py`)

| Column | Today | New default |
|---|---|---|
| Left column (`LEFT_W`, `parts.py`) | 28 | 42 (x1.5) |
| Flow's Project (`PROJECT_W`, `screen.py`) | 10, 12 with several boards | 20, 22 with several boards |
| Flow's Who (`WHO_W`, `screen.py`) | 10 | 15 (x1.5) |

The two extra columns of Project with several boards hold the board's label (`a/`); they stay
added on top of the doubled width. `RIGHT_W = 44` (Ready and Tasks), `CR_W`, `TIME_W`, the `Ago`
column's rule (`AGO_MIN`, `AGO_MAX`) and the header and footer do not change. The Event column
keeps taking the rest (`ratio=1`).

### 2. A narrow terminal: what gives way (answer 5)

The widths of section 1 are what the screen draws when they fit. When they do not, the screen
gives way in this order, so that the Event column keeps at least 20 columns:

1. the left column shrinks, from 42 down to 28 (today's width);
2. then the Flow's Who and Project columns shrink, down to 10 each (today's width; Project's
   two board-label columns, with several boards, stay on top of it) (the order between the two:
   question Q1);
3. only when even that does not fit (left column at 28, Who and Project at 10, Event at 20,
   `RIGHT_W` at 44) is the left column no longer drawn.

Consequences, which the Coder keeps:

- `NARROW = 100` (`screen.py`) is no longer a fixed width. The left column is drawn when the
  terminal holds the left column at 28, the Flow at its minimum (its borders and padding, the
  time column, Project at 10 when it is drawn, Who at 10, Event at 20, the gaps between them) and
  `RIGHT_W`. With today's drawing (a 4-column box border and padding, one-column gaps), that is
  122 columns with one project watched and the `Time` column (28 + 44 + 4 + 14 + 1 + 10 + 1 +
  20), 133 with several projects, 135 with several boards; the full defaults need 141, 162 and
  164. The tests measure the drawn text, not these sums. (Whether the `Ago` column, narrower and
  changing with the times shown, moves that threshold: question Q2.)
- Without the left column, the same rule applies to the Flow alone: Who and Project take back as
  much of their default as leaves Event 20 columns. The Event column is narrower than 20 only on a
  terminal where even Who and Project at 10, with no left column, leave it less, as today.
- A maximized Flow (`m`) spans the whole body: it draws Who and Project at their defaults when
  they fit, under the same rule.
- One function, used by both `_plan` and `render`, computes the drawn widths (left column, Who,
  Project) from the terminal's width, the Flow's columns and `RIGHT_W`; `flow()` takes the Who
  and Project widths it is given instead of reading the constants, which become the defaults.
  `_plan`'s list of drawn panels, and so Tab's order and the active panel's move when the left
  column goes (`View.settle`), follow the same computation.
- The Ready and Tasks column (`RIGHT_W`) never shrinks.

### 3. The docs and docstrings that change

- `docs/boards.md`, "The live terminal view":
  - "on the left (from 100 columns)" becomes the rule of section 2 in one sentence (the left
    column shrinks from 42 to 28, then Who and Project from their defaults to 10, so that Event
    keeps 20 columns; the left column is drawn only where that fits);
  - the Flow's paragraph names the Who and Project widths and how they close up;
  - the keys table's Tab line ("under 100 columns: Flow, Ready, Tasks") says "without the left
    column" instead of a number;
  - the `--once` capture is regenerated with the new widths, at a terminal width the Coder names
    in the sentence above it (today 120 columns, where, with one project, the left column would no
    longer be drawn: question Q3).
- The `screen.py` module docstring and `flow()`'s docstring say the widths and the order in which
  they give way; `NARROW`'s comment goes with the constant.

## Decisions of `02-answers.md`

- Answer 1: the batch is a stack batch. This CR is the lower of the two stacked CRs;
  `tui-mouse-resize` comes after it.
- Answer 2: the request's words are the source; of them, this CR carries the wider defaults
  (left +50 %, Project x2, Who x1.5): section 1.
- Answer 3: the request's empty last bullet held nothing else ("Rien d'autre").
- Answer 4: the split: this CR keeps the wider defaults and what gives way on a narrow terminal;
  the mouse, the kept widths, `platformdirs` and the `AGENTS.md` writes rule are
  `tui-mouse-resize`'s (out of scope below).
- Answer 5: on a narrow terminal the columns close up, Event keeps at least 20: the left column
  down to 28 first, then Who and Project down to 10, and the left column is dropped only when even
  that does not fit: section 2.
- Answer 6: the columns the mouse will resize are the screen's main columns, a matter of
  `tui-mouse-resize`; this CR keeps the wider defaults, Project x2 and Who x1.5 inside the central
  column: section 1.
- Header: spec critic yes.

## Out of scope

- `tui-mouse-resize`, stacked on this one: resizing columns with the mouse (`blessed`'s mouse
  tracking, its proof in a Windows terminal), keeping the widths in a JSON file in the user's
  configuration folder, the `platformdirs` dependency, and the `AGENTS.md` rule that `live`
  writes nothing (and its list of where chantier writes). This CR adds no dependency, writes no
  file and leaves `AGENTS.md` unchanged: `live` still writes nothing.
- Any other width: Time, Ago, CR, Event's own share, Ready's or Tasks' columns, `RIGHT_W`, the
  boxes' heights.
- The web board's columns.
- The CR board pane (`hooks/register.tsx`): untouched, so its screenshot rule does not apply.
- `2-backlog/P1/tui-live-batch-kanban`, a later item on the same layout (`screen.py`'s
  `_plan`/`render`): whichever of the two lands second rebases on the other's layout.

## Evidence

- Tests, in `skills/chantier/scripts/cli/tests/` (`test_live_panels.py`, `test_live_model.py`,
  with `live_world.py`'s `WIDE` and `NARROW`, or one new parametrized case; few, within
  `just test`'s budget), each reading the drawn text of `screen.plain`, not the constants:
  - at a width where everything fits, with one project and with several projects (and two
    boards), the left column is 42 wide, Project 20 (22 with two boards), Who 15;
  - parametrized over widths: the left column narrows from 42 to 28 before Who or Project
    narrow; Who and Project narrow to 10 and no further; the Event column is never under 20 while
    the left column is drawn; at one column under the threshold of section 2 the left column is
    not drawn and Who and Project widen back as far as Event's 20 allows;
  - the existing panel tests (Tab order, the active panel when a resize hides it, the keys) pass,
    `live_world.py`'s `NARROW` (90) still drawing no left column and `WIDE` (140) still drawing
    it with one project.
- `docs/boards.md`'s `--once` capture is regenerated from the head under test, not edited by hand.
- `just check` and `just eval-dry-run` (a change under the CLI's `src/`), and the long gate
  `scenario` (a CLI change), green. As the stack's lower CR, the local Windows run of `scenario`
  is owed by the CR on top (`AGENTS.md`).
- One screenshot of `chantier live` in a real terminal, on a running board, at a width where the
  left column shows, in the PR's Deliverables, showing no username and no home folder (floor
  rule 8).

## Questions for the Chief of Staff

- **Q1, Who or Project first.** Answer 5 says "then Who and Project down to 10". Which closes
  first? Suggested: Who first, down to 10, then Project, down to 10 (Project's names, `board/
  project`, are the longer text the owner asked to double). Alternative: both by the same share,
  one column at a time.
- **Q2, the `Ago` column and the threshold.** With `t`, the time column is 3 to 8 columns wide
  and changes as times pass, so a threshold computed from it would show and hide the left column
  on `t`, or as a line ages. Suggested: the threshold is computed with the `Time` column's width
  (14) in both modes, so `t` never hides the left column; the columns `Ago` frees still go to
  Event, as today.
- **Q3, 120 columns.** The rule of answer 5 drops the left column on a 120-column terminal with
  one project watched (it needs 122), where today it is drawn at 28 columns with an 18-column
  Event. Is that the owner's intent? Suggested: yes, as answered (Event's 20 columns first), and
  the docs' capture moves to 140 columns.

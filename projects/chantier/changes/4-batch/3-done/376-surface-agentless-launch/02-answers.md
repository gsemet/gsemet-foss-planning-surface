# Answers

## Given by earlier decisions

- **The launch method** (CR-237, 2026-11-14): `uvx --from git+https://github.com/gsemet/chantier@v<version> chantier`,
  the version pinned where that launch lives. Already in `docs/web-board.md`; nothing to add.
- **The sync with no agent** (CR-227, option A, the user, 2026-11-13): chantier owns no autosync
  and never replaces the surface's `scripts/ai-autosync-git.py`; the board's Start, Stop and
  Approve run that script on the user's click. The intake's "`just sync` in place of the script"
  is superseded: a `just sync` in the surface would call the surface's own script, or the board.
- **The scope** (the Chief of Staff's brief, 2026-11-18): changes in the planning surface's
  repository are out of this CR, which is chantier's; they are named as a follow-up.

## Settled by the spec-writer (2026-11-18)

Points with no user-visible behaviour of their own:

- **Where the rule lives.** `Seats` (`board/seats.py`) learns at construction whether the board
  follows its seats (`--seat` given) or not (started by hand). Not following: seats are still
  recorded and counted (`/api/board`'s `seats`, `POST /api/seats` answers as today), but `gone()`
  is never true and no watch thread starts.
- **The proof** is a scenario step (the board's behaviour belongs to `just scenario`,
  `tests/test_board.py` says so), by changing the existing "board with no seat" check; no new
  pytest.
- **The stale paragraph** of `docs/planning-modes.md` ("The board joins the group once, at a
  fresh start") is corrected to what the code does (joining is opt-in, on the board's Start):
  a docs fix, no behaviour change.

## Taken from the intake and CR-222's specification, to confirm

- **A board started by hand stops only when stopped by hand.** The intake asks for a board that
  runs "with no session open"; CR-222's specification (section 5, "Seats") already said "A board
  started with no `--seat` (by hand) stops only on Ctrl-C". The code instead follows the first
  seat that registers on it (a reading made in CR-222's round 2). This CR brings the code back to
  the specification. Open question Q1 in `03-change-spec.md` asks the user to confirm.

## Settled by the Chief of Staff (spec-writer's question, 2026-11-18)
- Q1: yes. A board started by hand (no `--seat`) keeps serving after a session that registered its
  seat on it leaves; it stops only when stopped by hand. A board started with `--seat` keeps
  today's rule. The surface's own recipes stay a follow-up in the surface's repository.

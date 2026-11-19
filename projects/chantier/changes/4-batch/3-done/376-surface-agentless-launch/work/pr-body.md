## Summary

The web board can already run from a planning surface's root with no agent and no plugin (`uvx --from git+https://github.com/gsemet/chantier@v<version> chantier board`). But a board started that way stopped itself as soon as a Chief of Staff session registered its seat on it and then left. This change makes a board started by hand serve until the user stops it, and documents the agent-free launch.

## Deliverables

A board now follows its seats only when it was started with `--seat`:

| Board started | A session registers a seat | The seat moves or is left |
| --- | --- | --- |
| with `--seat` | followed | the board stops once no registered seat is held (as before) |
| by hand, no `--seat` | recorded and counted in `/api/board`'s `seats`, not followed | the board keeps serving until Ctrl-C or the printed stop command |

```python
class Seats:
    def __init__(self, projects: Projects, follows: bool = True) -> None: ...
    # follows=False: add() records the seat, starts no watch; gone() is always False

seats = Seats(projects, follows=bool(args.seat))   # board/command.py
```

No message, exit code, route or file format changes. Docs: `docs/web-board.md` (starting, stopping, running by hand) and `docs/planning-modes.md` (the board's autosync Start as the code does it, and a new "With no agent" section).

## Blast radius

Grade: **1**. One class and its one construction; a `--seat` board behaves as before. Revert with `git revert`.

## Autonomous decisions

None.

## Known gaps

- The planning surface's own repository (a `just board` recipe, one pinned version, an autostart) is not part of this PR; it is a follow-up there.

<details>
<summary>Details</summary>

## Changes

- `board/seats.py`: `Seats(projects, follows=True)`; with `follows=False`, `add()` starts no watch and `gone()` returns `False`.
- `board/command.py`: `Seats(projects, follows=bool(args.seat))`; `_run` docstring.
- `declare/board.py`: `--seat` help says a board with none serves until stopped by hand.
- `docs/web-board.md`, `docs/planning-modes.md`: as above.
- `scenario/run_scenario.py`: the board unit's "no seat" step now checks that a hand-started board registers a seat (`seats == 1`) and keeps serving after the seat moves.

## Human decisions

- A board started by hand (no `--seat`) keeps serving after a session that registered its seat on it leaves; it stops only when stopped by hand. A `--seat` board keeps today's rule.
- The planning surface's own recipes stay a follow-up in the surface's repository.

## Impacts

No visual change. Users who start the board by hand no longer see it stop when a session leaves.

## Test plan

- [x] New or changed tests: the board unit's step in `scenario/run_scenario.py`; no pytest added (the behaviour belongs to the scenario)
- [x] Local gates at `8f751dd` (carried to `71ce268`, which changed only the scenario's stop step, then re-checked by CI): `just check`, `just eval-dry-run` pass; `just scenario` ran in CI (ubuntu) at `71ce268`, green
- [x] Evidence: none beyond the scenario step
- [x] Review: approved at `71ce268` (round 3, inspector approved at `8f751dd`)
- [x] Verified at `71ce268`
- [x] CI green at `71ce268`

## Internal references

CR-376 surface-agentless-launch.

</details>

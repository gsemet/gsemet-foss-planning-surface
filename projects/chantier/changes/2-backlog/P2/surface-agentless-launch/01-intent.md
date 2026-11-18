# Intent: a board started by hand serves a planning surface with no agent

2026-11-18, the spec-writer, from `intake/request.md` (the user, 2026-11-13: "il faudra un moyen
de lancer le backend directement sans nécessairement avoir de chief of staff (fonctionnement
hors agent)") and the code at chantier's `main` (3a9afc2c, v0.13.0).

## What the intake asked, and what already exists

| Asked | At `main` today | Left |
| --- | --- | --- |
| One launch method with no agent: `uvx --from git+https://github.com/gsemet/chantier@v<version> chantier` (CR-237) | Done. `docs/web-board.md`, "By hand", names it; the surface's `scripts/validate-bundles.py` already runs chantier that way (`CHANTIER_REF = "v0.11.0"`). | Nothing in chantier. |
| The board, with no Chief of Staff | `chantier board` with no `--seat` serves the whole surface from its root (`board/projects.py`, `open_projects`), with no plugin and no session (CR-222). | **One gap:** a board started by hand stops as soon as a session that registered a seat on it leaves (`board/seats.py`; `scenario/run_scenario.py`, "a board that had no seat takes its first over `POST /api/seats`, then stops by itself when that session goes"). A board meant to run with no session open is stopped by the first Chief of Staff that comes and goes. CR-222's own specification (section 5, "Seats") said: "A board started with no `--seat` (by hand) stops only on Ctrl-C." |
| The sync with no agent, "in place of `scripts/ai-autosync-git.py`" | The board's Start button runs the surface's own script (`start . --enable-only`, then a join owned by the board's process: `board/autosync_api.py`), on the user's click. Option A (CR-227, the user, 2026-11-13): chantier owns no autosync and never replaces the surface's. | Nothing in chantier; the "replace the script" part is superseded by CR-227. One stale paragraph: `docs/planning-modes.md` still says the board joins the group at a fresh start, which the code no longer does (joining is opt-in, on Start). |
| `just board`, `just sync`, one place for the pinned version, an optional autostart | Not in the surface (its `justfile` has only `validate`). | The surface's repository, not chantier's: a follow-up there. |

## The change

A board started with no `--seat` serves until it is stopped by hand (Ctrl-C, or the stop
command `board` prints), whatever sessions register a seat on it and leave. A board started with
`--seat` keeps today's rule. The docs say how to run the board, and the autosync through it,
with no agent, and drop the stale "joins at a fresh start".

## Out of this CR

The surface's `justfile` recipes, its pinned version and an autostart (a scheduled task, a
service): they belong to the surface's repository (follow-up there). Replacing the surface's
autosync script: CR-227 decided against it.

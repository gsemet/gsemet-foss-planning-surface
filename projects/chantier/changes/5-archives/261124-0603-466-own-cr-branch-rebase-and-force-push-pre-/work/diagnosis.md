# CR-466 scenario failure: surface-board "webui on a running server prints board already running at"

Verdict: environmental and pre-existing; not caused by the CR's diff.

## Cause
Section 16d1 of `scenario/run_scenario.py` (lines ~2779-2812) starts `first = serve --port DEFAULT_PORT (8765)`.
If the port is held by another program, `Link(first.line())` is not ok and the scenario prints
"the default port 8765 is held by another program here: the second-surface step is skipped" (transcript line 28621).
It then still runs the `webui on a running server` check (line 2808-2812), but no server runs, so `webui` starts a
board itself and prints `board on ...` (transcript 28622-28625). The check expects `board already running at`, so it fails.
`running = surface_link(sw)` is built from the board webui just started (port 59692), which confirms it.

## Evidence
- Transcript `scenario/results/scenario-20261123-145641-3740.md` lines 28621-28626.
- `netstat -ano` on this machine now: 127.0.0.1:8765 LISTENING by PID 33908 with 3 established clients,
  that is the user's own live chantier board, held while the scenario ran.
- `git diff origin/main --stat`: 15 files, only cards, `allow_samples.py`, `driver.py`, `permissions.py`,
  `driver_prompt.py`, tests and a 20-line `scenario/run_scenario.py` change; no `serve`/`webui`/hub/server code.
  (The scenario diff was not read hunk by hunk; the failing code path does not depend on it, the failure
  precedes any CR-specific step.)
- I did not rerun the scenario (told not to run it twice); the port-held trace line makes the cause determinate.

## Place to fix
`scenario/run_scenario.py` ~2807-2812: the `webui` check must not run (or must not be a `check`) when the
default-port serve was skipped; better, start `first` with `--port 0`/a free port for the webui check
(the port-8765 requirement only matters for the second-surface-takes-another-port check).
Minimal: move lines 2807-2812 inside the `else:` branch (after `second.stop()`), and keep a skip note otherwise.
Not a CR-466 change; a separate fix, or rerun the gate with port 8765 free (stop the live board, or run it on a machine/CI where it is free:
CI's ubuntu job has no such board, so the gate there is unaffected).

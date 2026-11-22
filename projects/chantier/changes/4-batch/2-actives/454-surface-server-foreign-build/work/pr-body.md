## Summary

When chantier is developed in its own checkout and the board server (with its writer and forge hub) was started by another project's session from a cached build, nothing says so while the version string is equal. The server's record now keeps the folder of the build it runs, and a dev-mode session is told in one line when it differs from its own checkout's. Nothing is stopped or restarted, and the line gives no advice.

## Deliverables

- `server.json`'s `server` and `hub` entries gain `source`, the resolved folder of the loaded `chantier` package. Two processes run the same build when it is equal.
- One clause, in one place (`hub/lines.py`), used by three callers:
  - `status`, as a `board` line when the live server is of this version but another build;
  - the watcher's start line, only when the version clause is absent;
  - `board --seat`, as one added line under `board already running at` (no refusal, same exit code, seat registered; no line in a multi-project surface with no `--project`).
- Texts: `board runs another build of chantier <v> (<source>), not this checkout's`, or, for an entry with no `source`, `board runs a build of chantier <v> older than this notice (source unknown), not this checkout's`.
- Only a session in the dev mode (chantier's checkout, project chantier) is told; plugin-mode sessions see today's version lines only.
- Cards and docs: the Chief of Staff says the line once and never stops or restarts the board; the "no notice while the version is equal" sentence in `AGENTS.md`, `CONTRIBUTING.md` and `session-start.md` is rewritten.

## Blast radius

Grade: 1. Read-only notice lines and two added fields in a JSON record; a `git revert` restores the previous behaviour.

## Autonomous decisions

- The `status` line is the clause itself, with no `board:` prefix, as `board_lines` prints its other lines. This departs from the spec's wording (a `board:` line).

## Known gaps

- **UNVERIFIED:** the real-session check (a plugin-mode session starts the board, then a dev session's `status` shows the clause) has not been done.
- The multi-project `board --seat` case is tested by forcing the surface's choice flag, not on a real two-project surface.

<details>
<summary>Details</summary>

## Changes

- `hub/state.py`: `build_source()`, `source` in `write_server` and `hub_record`, `other_build()`, `UNKNOWN`.
- `hub/lines.py`: the clause; `board_lines` uses it. `hub/watch.py`: start line. `board/command.py`, `board/projects.py`: the `board --seat` line.
- Cards and docs as above; `tests/test_launch_modes.py` follows the new wording.
- Tests: a parametrized matrix (status line, start line) in `tests/test_watcher_autostart.py`, `board --seat` cases in `tests/test_board_running.py`, a record test in `tests/test_forge_hub.py`, and guards on the shipped cards' sentences in `tests/test_launch_modes.py`.

## Impacts

A dev-mode session may see one more line on `status`, the start line and `board --seat`.

## Test plan

- [ ] New or changed tests (they fail on the previous code)
- [ ] Local gates at `<sha7>`: `just check` (1738 passed), `just eval-dry-run` (19 of 19)
- [ ] Evidence: no visual change
- [ ] Review: approved at `<sha7>`
- [ ] Verified at `<sha7>`
- [ ] CI green at `<sha7>`

## Internal references

CR-454 foreign-build (batch-30).

</details>

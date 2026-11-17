# Sub-agent rules

- Work on the CR branch only. Never commit, push, stash or switch branches (driver's job).
- Read `.agents/constitution.md` first; it ranks above this briefing.
- No installs, no network unless `AGENTS.md` allows it.
- Run only the gates `task.md` lists, in the foreground; leave nothing running.
- Touch only the files the task needs. Never change an existing assertion's intent. New tests must
  fail on the unchanged code.
- A behaviour change updates its SwRS and the `@implements_req` / `@tests_req` markers in the same
  task; a refactor moves the markers with the code
  (`requirements/guidelines/requirements.guidelines.md`).
- Report: files changed, tests added and their failure before the change, changed assertions and
  why, gate results with counts, screenshot paths, open points.
- Never run real-window (app-window / integration) tests locally; heavy CI is the proof.
- Never change an `approved` requirement. Never write the name mark_o_down.
- `rm`, `cp`, `mv` may be aliased to `-i`: use `\rm`, `\cp`, `\mv`.

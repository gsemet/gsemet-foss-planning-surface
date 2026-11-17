# Rules for sub-agents (coder, reviewer, investigator, verifier)

- Read `.agents/constitution.md` first; it ranks above this briefing.
- Work on the CR branch only, in the CR worktree. Never commit, push, stash or switch branches
  (driver's job).
- No installs, no network unless `AGENTS.md` allows it.
- Run only the gates `task.md` lists, in the foreground; leave nothing running. Never run app-window
  (real VS Code) tests locally: CI runs them.
- Documents read by the owner follow the writing skill; working files stay plain GFM.
- Touch only the files the task needs. Never change an existing assertion's intent. New tests must
  fail on the unchanged code.
- A behaviour change updates its SwRS and the markers in the same task, following
  `requirements/guidelines/requirements.guidelines.md`: `@implements_req <ID>` next to the
  implementation and `@tests_req <ID>` next to each test that checks it; `just requirements-update`
  run; a dated entry in `requirements/tiers/log.md`; new requirements created `proposed`.
- Everything written to the repository is in English.
- Report: files changed, tests added and their failure before the change, changed assertions and
  why, gate results with counts, screenshot paths, open points.

# Rules for sub-agents of CR 264

- Work on the CR branch only. Never commit, push, stash or switch branches (driver's job).
- Read `.agents/constitution.md` first; it ranks above this briefing.
- No installs, no network unless `AGENTS.md` allows it.
- Run only the gates `task.md` lists, in the foreground; leave nothing running.
- Touch only the files the task needs. Never change an existing assertion's intent, except what the
  owner's decisions in `00-request.md` change: say why for each. New tests must fail on the unchanged code.
- A behaviour change updates its SwRS and the markers in the same task, following
  `requirements/guidelines/requirements.guidelines.md`: `@implements_req <ID>` next to the implementation
  and `@tests_req <ID>` next to each test; `just requirements-update` run; a dated entry in
  `requirements/tiers/log.md`. The report lists the IDs with their source and test files.
- Files and commits in English. Commit trailer: `Assisted-by: Claude:<model>`, per
  `.agents/guidelines/git-commit-message.guidelines.md`, never Co-Authored-By.
- Report: files changed, tests added and their failure before the change, changed assertions and why,
  gate results with counts, screenshot paths, open points.

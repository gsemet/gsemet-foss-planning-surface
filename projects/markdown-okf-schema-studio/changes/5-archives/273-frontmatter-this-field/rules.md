# Rules for sub-agents

- Work on the CR branch only. Never commit, push, stash or switch branches (driver's job).
- Read `.agents/constitution.md` first; it ranks above this briefing.
- No installs, no network unless `AGENTS.md` allows it.
- Run only the gates `task.md` lists, in the foreground; leave nothing running.
- Documents read by the owner follow the writing skill (see
  `.agents/guidelines/owner-review.guidelines.md`); working files stay plain GFM.
- Touch only the files the task needs. Never change an existing assertion's intent. New tests must
  fail on the unchanged code.
- A behaviour change follows `requirements/guidelines/project.guidelines.md` ("During a change"):
  the SwRS, the markers, `just requirements-update` and the log entry. The report lists the IDs
  with their source and test files.
- Report: files changed, tests added and their failure before the change, changed assertions and
  why, gate results with counts, screenshot paths, open points.
- Files and commits in English. Commit trailer: `Assisted-by: Claude:<model>`, never Co-Authored-By.

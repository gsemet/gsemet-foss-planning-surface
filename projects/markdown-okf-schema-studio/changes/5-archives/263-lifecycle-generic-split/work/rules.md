# Rules for sub-agents of CR 263

- Work on the CR branch only. Never commit, push, stash or switch branches (driver's job).
- Read `.agents/constitution.md` first; it ranks above this briefing.
- No installs, no network unless `AGENTS.md` allows it.
- Run only the gates `task.md` lists, in the foreground; leave nothing running.
- Touch only the files the task needs. Never change an existing assertion's intent, except the folder and
  file names this CR renames. New tests must fail on the unchanged code.
- A pure move: text changes only as far as the new vocabulary, the isolation rule and the listed
  inconsistencies require. Report any rule you could not place.
- Files and commits in English. Commit trailer: `Assisted-by: Claude:<model>`, per
  `.agents/guidelines/git-commit-message.guidelines.md`, never Co-Authored-By.
- Report: files changed, tests added and their failure before the change, changed assertions and why,
  gate results with counts, open points.

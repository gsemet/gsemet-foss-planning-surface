# Sub-agent rules

- Work on the CR branch only. Never commit, push, stash or switch branches (driver's job).
- Read `.agents/constitution.md` first; it ranks above this briefing.
- No installs, no network unless `AGENTS.md` allows it.
- Run only the gates `task.md` lists, in the foreground; leave nothing running.
- Touch only the files the task needs. Never change an existing assertion's intent. New tests must
  fail on the unchanged code.
- A behaviour change updates its SwRS and the markers in the same task, following
  `requirements/guidelines/requirements.guidelines.md`: `@implements_req <ID>` next to the
  implementation **and** `@tests_req <ID>` next to **each** test that checks it, for every touched
  leaf requirement; `just requirements-update` run and its generated files committed; a dated entry
  in the bundle's `tiers/log.md`; a refactor moves the markers with the code. Never leave a touched
  requirement without a source or a test link. The report lists the IDs with their source and
  test files.
- Report: files changed, tests added and their failure before the change, changed assertions and
  why, gate results with counts, screenshot paths, open points.

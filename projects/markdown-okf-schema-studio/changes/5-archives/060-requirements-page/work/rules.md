# Rules for sub-agents (CR 060)
- Work only in worktree /Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-060 (branch changes-requests/060-requirements-page). Never commit, push, stash, switch branches.
- Read /Users/az02065/Projects/DevTools/markdown-okf-schema-studio/.agents/constitution.md first, then AGENTS.md and requirements/guidelines/requirements.guidelines.md (in the worktree).
- No installs, no network. Never `git add`. Use `\rm \cp \mv`. Do not touch the main checkout or /Users/az02065/Projects/DevTools/agentic-planning-surface.
- Run okfreq with UV_PROJECT_ENVIRONMENT=/Users/az02065/Projects/DevTools/markdown-okf-schema-studio/.venv (the worktree has no .venv): `UV_PROJECT_ENVIRONMENT=... uv run --no-sync --group requirements okfreq ...`.
- Run only the gates in task.md, in the foreground. Leave nothing running.
- New tests must fail on the unchanged code. Never change an existing assertion's intent.
- Layer rules (no new dependency-cruiser exception) and size ratchet (800 lines src, 1500 test) hold. Keep buildSite.ts growth minimal: put new logic in new files under test/site/.
- Report: files changed, tests added, gate results with counts, open points.

# Run brief (2026-10-27, run 4) — orchestrator

**Becomes `RUN-BRIEF.md`** once run 3 is landed (archive the run-3 brief and `STACK-STATE.md` to
`04-archives/` with a `-run3` suffix first).

The user asked: every remaining point of the audit (proposed CRs 3–28), "plusieurs drivers en
parallèle pour optimiser le dev mais livre qu'une seule PR avec tout". Fully autonomous: no
questions to the user; decisions under "Autonomous decisions" in `00-request.md` and the PR body.

One CR: [135](135-audit-security-performance-pack/00-request.md), 26 tasks in
`135-audit-security-performance-pack/tasks/T1…T26`. Process:
`.agents/guidelines/change-requests-lifecycle.guidelines.md`, adapted as below.

## Shape

- **Task drivers** (Sonnet, one per task, at most 4 live): coder/reviewer rounds for that task
  only (limit 3), one Conventional Commit on the task's local branch, never pushed. Return one line.
  T1–T7 worktrees exist from origin/main (`../markdown-okf-schema-studio-wt-135-tN`, `node_modules`
  symlinked). For T8–T26 the orchestrator creates the worktree when the task starts, from the
  integration branch tip, with a `node_modules` symlink to the main checkout (it has `shiki`).
  Respect the "start after" constraints written in T5, T7, T12, T13, T18, T21, T24, T26.
- **Integrator** (one Sonnet agent, restarted as needed; Opus for a hard conflict): owns
  `change-requests/135-audit-security-performance-pack` in `../markdown-okf-schema-studio-wt-135`.
  Integrates finished tasks strictly in task order T1 → T26 (cherry-pick, or rebase the task
  branch onto the integration tip), resolves conflicts, `just check` after each task so every
  commit is green on its own. A conflict it cannot resolve without changing a task's intent goes
  back to that task's driver as a new round. Blocked tasks are skipped and listed.
- Suggested start order (dependency and conflict risk): T1, T2, T3, T4 → T6, T8, T9, T10 → T5, T7,
  T11, T12, T14, T15, T16, T19, T20, T22, T23 → T13, T17, T21, T25 → T18 → T24 → T26.
- **PR** (integrator, once every task is integrated or blocked): push the integration branch,
  open **one** PR ready (not draft) against main. Body for an external reader: Summary, a table of
  the 26 tasks (subject, commit, proof: test or bench numbers), Deliverables (benches before/after,
  screenshots only where something visible changed, on a `-assets` branch), Autonomous decisions,
  Not included (blocked tasks with reason), Internal references last, ends with
  "🤖 Generated with [Claude Code](https://claude.com/claude-code)". Security items name the class of
  input refused, never a ready-to-use exploit. Then watch CI in ≤5-minute slices; a product failure
  goes to the task that caused it as a new round; finally heavy CI on the branch
  (`gh workflow run ci.yml --ref <branch> -f heavy=true`) and wait for it.

## Run rules

1. **Never merge.** Never `git add -A` / `.`. Never delete branches or worktrees (the user does it).
   No new dependency (T17 may remove one). `\rm \cp \mv` (noclobber). Rebase only;
   `--force-with-lease` only after a rebase.
2. Never touch `/Users/az02065/Projects/DevTools/agentic-planning-surface`, nor the main checkout's
   untracked `.agents/skills/crf/`, `.claude/`, its modified guideline file, its local `main`
   branch, or its `node_modules` (read-only through the symlinks).
3. **Window tests**: one task at a time under `WINDOW-TESTS.lock`; caffeinate per the guideline.
4. **Permission denial**: never work around it; record it in `STATE.md` and in your return.
5. Agents may run `just requirements-update` (user authorization, 2026-10-27), STUDIO_OKFREQ
   pointing at the okf-schema checkout's okfreq (read-only). Index changes go into the task's commit.
6. Keep `135-…/STATE.md` (4-line header: overall step, tasks done/total, PR, run) and a task table
   `135-…/TASKS.md` (task, status, round, commit) current; `ORCHESTRATOR.md` row for 135.

## Cost rules

No wait longer than 5 minutes between turns. Read only `STATE.md` headers and `TASKS.md`.
`head`/`tail`/`grep` on outputs; never dump CI logs. Drivers and integrator return one line.

## Return to the main session

PR link, task table summary (done / blocked with reason and recommended answer), bench headline
numbers, heavy-CI run link. Refresh `ORCHESTRATOR.md` (and its Backlog table) and
`ORCHESTRATOR-STATUS.md` before returning.

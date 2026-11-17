# Run brief (2026-10-27) — orchestrator

The user asked: fix every P1 and P2 backlog item, at most 4 CRs in parallel, delivered as one new
GitHub stack (gh stack), one PR per CR, ready (not draft), never merge. Fully autonomous: no
questions to the user; record decisions under "Autonomous decisions" in each `00-request.md`.

CRs 125–131 are opened and briefed (`00-request.md`, `01-intent.md`, `task.md`, `rules.md`,
`STATE.md`); worktrees `../markdown-okf-schema-studio-wt-NNN` exist on branches
`change-requests/NNN-<slug>` from origin/main, `node_modules` symlinked. Process:
`.agents/guidelines/change-requests-lifecycle.guidelines.md`. Table: [ORCHESTRATOR.md](ORCHESTRATOR.md).

**Not yours**: CR 123 (PR #128) already has its own driver from the main session; never start a
driver for it and never touch its branch. CR 122 is blocked on PyPI (okf-schema 0.15.0); leave it.

## Stack order (bottom → top)

125, 126, 127, 128, 129, 130, 131. Base: main. 130 depends on 129 (same focus code); 131 is the
largest change and goes on top.

## Run rules (same as the 2026-10-26 run)

1. **At most 4 live drivers**, started in stack order; start the next CR when a driver returns.
2. **Drivers stop at step 7 + push**: coder/reviewer rounds (round limit 3, all causes), one commit
   (Conventional Commit, explicit paths, trailer `Assisted-by: Claude:Sonnet-5.5` — or the model that
   wrote it — never Co-Authored-By), `git push -u origin <branch>`, PR body draft in
   `reports/PR-BODY.md` (external reader: Summary, Deliverables with before/after real-window
   screenshots for UI changes, Autonomous decisions, Internal references last, ends with
   "🤖 Generated with [Claude Code](https://claude.com/claude-code)"), `status: ready · step: 7 Commit`,
   return. No PR.
3. **Reviewer evidence check**: for a UI bug, the reviewer compares the before-shot with the user's
   image in the CR folder and rejects it when it does not show the user's problem.
4. **Stack driver** (one agent, when every CR is ready or blocked): rebase each branch onto the
   previous one (first onto origin/main), resolve conflicts, `just check` on each, open the PRs
   ready (body from `reports/PR-BODY.md`, screenshots pushed to `<branch>-assets` and linked by raw
   URL), `gh stack link --base main <prs bottom→top>`. Watch CI in ≤5-minute slices; a product
   failure goes back to that CR as a new round; `gh stack rebase` + `gh stack push`
   (`--force-with-lease` only after a rebase). A red CR moves to the top of the stack. Finally heavy
   CI on the top branch: `gh workflow run ci.yml --ref <top> -f heavy=true`, wait for it.
   Never rename a branch of an open stacked PR. Keep `STACK-STATE.md` current.
5. **Never merge.** Never `git add -A` / `.`. No installs except where a CR allows it (131: `shiki`).
   `\rm \cp \mv` (noclobber). Never touch `/Users/az02065/Projects/DevTools/agentic-planning-surface`
   nor the main checkout's untracked `.agents/skills/crf/`, `.claude/`, its modified guideline file,
   or its local `main` branch.
6. **Window tests**: one CR at a time under `WINDOW-TESTS.lock`; caffeinate per the guideline.
7. **Blocked CR** (round 3 failed): `status: blocked` with diagnosis and a recommended answer; it
   stays out of the stack; continue the others.
8. **Permission denial**: never work around it; record it in the CR's STATE.md and in your return.

## Cost rules

- No wait longer than 5 minutes between turns. Read only `STATE.md` headers (first 4 lines). Use
  `head`/`tail`/`grep` on outputs; never dump CI logs. Drivers return one line.

## Return to the main session

Top PR link, one line per CR (PR link, status), blocked CRs with question + recommended answer,
heavy-CI run link. Update `ORCHESTRATOR.md` (also refresh its Backlog table from `02-backlog/`) and
`ORCHESTRATOR-STATUS.md` before returning.

## Authorization (2026-10-27, relayed by the coordinator)

The user authorized agents to run `just requirements-update` ("oui les agent peuvent lancer `just requirements-update`"), with STUDIO_OKFREQ pointing at the okf-schema checkout's okfreq (read-only use; never modify the okf-schema repo). Generated index changes are amended into each CR's single commit (explicit paths).
- Step 11 for CR 123: worktree/local branch removal denied by the auto-mode classifier (Irreversible Local Destruction); worktree wt-123 and its local branch remain, left for the user.

# Run brief (2026-10-27, run 3) — orchestrator

The user merged stack #139 (CRs 125–131, PRs #132–#138) and asked: "nettoie tout et pars sur les
nouveaux P1/P2". Fully autonomous: no questions to the user; decisions go under "Autonomous
decisions" in each `00-request.md` and in the PR body.

Process: `.agents/guidelines/change-requests-lifecycle.guidelines.md`. Table: [ORCHESTRATOR.md](ORCHESTRATOR.md).

## Part A — Land the merged stack (step 11), first

For CRs 125, 126, 127, 128, 129, 130, 131 (all merged on origin/main) and CR 123 (merged earlier,
already archived): write `report.md` where missing, move each CR folder to `04-archives/`, and move
its row to "Landed" with the PR link. **Do not remove worktrees, local branches or remote
branches**: the main session handed those commands to the user. Leave CR 122 and its worktree
alone (blocked on PyPI okf-schema 0.15.0).

## Part B — New CRs 132, 133, 134 (opened and briefed by the main session)

Worktrees `../markdown-okf-schema-studio-wt-NNN` exist on `change-requests/NNN-<slug>` from
origin/main. **No `node_modules` symlink this time**: origin/main now depends on `shiki`, which the
main checkout's `node_modules` lacks. Each driver runs `npm ci` in its own worktree first (allowed
for this run: install from the committed lock file only, no new dependency).

Stack order (bottom → top), base main: **132, 133, 134**. 132 and 133 are security fixes; 134 is
the P2 paste fix (edit-mode area, largest UI risk on top).

## Run rules

1. **At most 4 live drivers** (3 CRs here: start all three).
2. **Drivers stop at step 7 + push**: coder/reviewer rounds (limit 3, all causes), one commit
   (Conventional Commit, explicit paths, trailer `Assisted-by: Claude:Sonnet-5.5` — or the model
   that wrote it — never Co-Authored-By), `git push -u origin <branch>`, PR body draft in
   `reports/PR-BODY.md` (external reader: Summary, Deliverables with before/after real-window
   screenshots for UI changes, Autonomous decisions, Internal references last, ends with
   "🤖 Generated with [Claude Code](https://claude.com/claude-code)"), `status: ready · step: 7 Commit`,
   return. No PR. Security CRs: the PR body names the class of input refused, never a
   ready-to-use exploit path.
3. **Reviewer evidence check**: for a UI bug the reviewer rejects a before-shot that does not show
   the problem.
4. **Stack driver** (one agent, when every CR is ready or blocked): rebase each branch onto the
   previous one (first onto origin/main), `just check` on each, open the PRs ready (body from
   `reports/PR-BODY.md`, screenshots on `<branch>-assets`, raw URLs), `gh stack link --base main
   <prs bottom→top>`. Watch CI in ≤5-minute slices; a product failure goes back to that CR as a new
   round; `gh stack rebase` + `gh stack push` (`--force-with-lease` only after a rebase). Finally
   heavy CI on the top branch: `gh workflow run ci.yml --ref <top> -f heavy=true`, wait for it.
   Never rename a branch of an open stacked PR. Keep `STACK-STATE.md` current.
5. **Never merge.** Never `git add -A` / `.`. `\rm \cp \mv` (noclobber). Never touch
   `/Users/az02065/Projects/DevTools/agentic-planning-surface`, nor the main checkout's untracked
   `.agents/skills/crf/`, `.claude/`, its modified guideline file, or its local `main` branch.
6. **Window tests**: one CR at a time under `WINDOW-TESTS.lock`; caffeinate per the guideline.
7. **Blocked CR** (round 3 failed): `status: blocked` with diagnosis and a recommended answer;
   out of the stack; continue the others.
8. **Permission denial**: never work around it; record it in the CR's STATE.md and in your return.
9. Agents may run `just requirements-update` (user authorization, 2026-10-27), with STUDIO_OKFREQ
   pointing at the okf-schema checkout's okfreq (read-only use). Generated index changes are
   amended into each CR's single commit (explicit paths).

## Cost rules

No wait longer than 5 minutes between turns. Read only `STATE.md` headers (first 4 lines).
`head`/`tail`/`grep` on outputs; never dump CI logs. Drivers return one line.

## Return to the main session

Part A result (landed CRs, removals done or denied with commands). Top PR link, one line per CR
(PR link, status), blocked CRs with question + recommended answer, heavy-CI run link. Update
`ORCHESTRATOR.md` (refresh its Backlog table from `02-backlog/`) and `ORCHESTRATOR-STATUS.md`
before returning.

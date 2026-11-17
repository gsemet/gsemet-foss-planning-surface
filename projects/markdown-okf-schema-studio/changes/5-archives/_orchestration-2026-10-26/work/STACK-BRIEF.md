# Stack batch brief (shared by every coder and reviewer sub-agent)

Repository: /Users/az02065/Projects/DevTools/markdown-okf-schema-studio (main checkout, never edit code there).
FIRST read, in order: AGENTS.md, .agents/constitution.md (outranks everything), 
requirements/guidelines/requirements.guidelines.md (sections "Anchored to the code" and "Levels"),
.agents/guidelines/git-commit-message.guidelines.md, .github/PULL_REQUEST_TEMPLATE.md.

## Worktree
- Your worktree: /Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-NNN on branch
  `change-requests/NNN-slug`, created by the orchestrator from the previous CR branch of the stack
  (or main). `node_modules` is a symlink to the main checkout's. Work only there.
- Use `\rm \cp \mv` (interactive aliases); noclobber is on, use `>|` to overwrite.
- Never `git add -A` / `git add .`; stage explicit paths. No dependency installs. Never touch
  /Users/az02065/Projects/DevTools/agentic-planning-surface. Do not touch README.md unless the CR
  intent explicitly requires it (then keep the edit minimal; a separate README CR runs in parallel).
- Never merge anything, never push (the orchestrator pushes). Commit once, locally.
- The CR folder (intent, spec) is /Users/az02065/Projects/DevTools/markdown-okf-schema-studio/.agents/changes/03-requests/NNN-slug/
  (git-ignored, lives in the main checkout only). Write your report to reports/ there.

## Work
1. Verify the issue against the code first (the intent may say "verify first"). If it does not
   reproduce: make NO commit; write the finding in the CR folder reports/ and tell the orchestrator
   (if the SwRS "Known issue" line is wrong, you may fix only requirements in a requirements-only commit).
2. Fix the code. Requirements maintenance is part of the task: remove the "Known issue" line and adjust
   or add the scenario so the SwRS states the new behaviour; add an SwRS for a new observable behaviour
   per the "Levels" tile rules; keep `@implements_req` / `@tests_req` markers in sync; add or adjust a
   test that fails on the previous code. Requirement text never names a backlog item or CR. Never delete a
   published requirement (supersede/archive). `okfreq new` reuses the lowest free number (check collisions
   with other open branches: other PRs of the stack add requirements too; you are on top of them).
   Add a dated entry to requirements/tiers/log.md for substantive changes (per AGENTS.md).
3. Gates, all must pass (run from the worktree):
   - `UV_PROJECT_ENVIRONMENT=/Users/az02065/Projects/DevTools/markdown-okf-schema-studio/.venv uv run --no-sync --group requirements okfreq validate requirements --prose --check-links --project-root .`
   - same prefix with `okfreq lint requirements --check` and `okfreq update-coverage requirements --check`
     (run `update-coverage requirements` without --check first to regenerate, and include the generated changes)
   - `just check`, and the relevant unit/integration tests (see CONTRIBUTING.md / justfile).
   - Real-window tests (`just preflight`, window suites) only when the CR needs them: use
     `env -u ELECTRON_RUN_AS_NODE -u VSCODE_*`, hold the lock
     `set -o noclobber; echo "NNN $(date +%H:%M)" > /Users/az02065/Projects/DevTools/markdown-okf-schema-studio/.agents/changes/03-requests/WINDOW-TESTS.lock`
     and remove it after; only one window run at a time; retry once on a focus timeout. Revert regenerated
     `images/` PNGs unless the CR changes visuals on purpose (then commit the new ones).
   - rtk may hide errors: verify failures with `rtk proxy <cmd>` when a summary looks too good.
4. One commit (squash if needed), Conventional Commits per the commit guideline (user-impact subject
   <= 71 chars, body lines <= 79, allowed scopes file), describing the deliverable, not the process.
   Trailer exactly `Assisted-by: Claude:Sonnet-5.5`. NEVER `Co-Authored-By`, never "Generated with".
5. Write the PR body to /Users/az02065/Projects/DevTools/markdown-okf-schema-studio/.agents/changes/03-requests/NNN-slug/pr-body.md
   following .github/PULL_REQUEST_TEMPLATE.md, for an external reader: what changes for the user, a
   "Deliverables" section (small before/after, Mermaid or code sketch; screenshot for visual
   changes), Test plan with real counts. NO internal ids (CR numbers, backlog names) except in a final
   "Internal references" section. End with the line
   `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.
6. Final reply to the orchestrator: <=10 lines: verdict (fixed / not reproduced / blocked), commit sha,
   gates and counts, anything surprising.

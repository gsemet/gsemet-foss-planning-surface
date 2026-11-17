# Foreman brief

Run: export HTML and QA 271 findings. A STACK of six CRs, bottom to top: 290, 289, 293, 292, 291, 288 (stack mode of the process guideline: one stack driver, one driver per CR). Open-PR cap: 7 (the stack, plus PR #357 outside it, run by the Chief of Staff). Main session: the session that started you (Chief of Staff). Started 2026-11-11 at the owner's request ("Export single html et les findings").

| CR | Folder | Worktree | Branch | Inspector |
| --- | --- | --- | --- | --- |
| 290 | 290-label-popover-covers-table | ../markdown-okf-schema-studio.worktrees/290 | change-requests/290-label-popover-covers-table | Sonnet |
| 289 | 289-find-scrolls-wide-table-to-hit | ../markdown-okf-schema-studio.worktrees/289 | change-requests/289-find-scrolls-wide-table-to-hit | Sonnet |
| 293 | 293-table-keyboard-row-add-discoverable | ../markdown-okf-schema-studio.worktrees/293 | change-requests/293-table-keyboard-row-add-discoverable | Opus |
| 292 | 292-table-paste-tsv | ../markdown-okf-schema-studio.worktrees/292 | change-requests/292-table-paste-tsv | Opus |
| 291 | 291-table-in-quote-or-admonition-editing | ../markdown-okf-schema-studio.worktrees/291 | change-requests/291-table-in-quote-or-admonition-editing | Opus |
| 288 | 288-export-single-html | ../markdown-okf-schema-studio.worktrees/288 | change-requests/288-export-single-html | Opus |

All worktrees start at origin/main `33fb65ef`; the stack driver restacks them in the order above.

## Owner's decisions

In `02-answers.md` and `03-change-spec.md` of each CR. CR 288: the IMPORTANT note at the top of its spec (Export button in the main row, no sixth row) overrides the spec text.

## Notes for this run

- Write files under `.agents/changes/` through short shell scripts with absolute paths: this session runs in a worktree and the app refuses Edit/Write there. This holds for every sub-agent too (drivers, coders, Inspectors, Verifiers): `rules.md` says so since 2026-11-11. Run `just orchestrator /Users/az02065/Projects/DevTools/markdown-okf-schema-studio/.agents/changes` from a checkout of current `origin/main` (a CR worktree works). `STATUS.md` status values: working, wait-ci, ready, blocked, landed only.
- Use general-purpose agents for drivers, the stack driver, coders, Inspectors, Verifiers and debuggers (the chantier agent types refuse to run outside a chantier batch).
- No GitHub issue: no `Fixes`, no issue comment. Never touch the Chantier repository.
- Each PR is a draft and turns ready ON ITS OWN when mergeable: CI green at its head, review approved, Verifier `VERIFIED` at that head (step 10). The owner merges the stack; never touch auto-merge.
- PR body: `.github/PULL_REQUEST_TEMPLATE.md` per `pull-request.guidelines.md`, all six sections plus "Autonomous decisions". A visible change has before/after screenshots in Impacts (light and dark), raw blobs on `change-requests/<id>-<slug>-assets` (`git hash-object -w --no-filters`; `${commit}` in braces under zsh). No screenshot = not mergeable.
- Heavy CI run on each branch (`gh workflow run ci.yml --ref <branch> -f heavy=true`). No real VS Code window locally.
- Replays come from local commit `87307e8f` (branch `qa/271-table-campaign-replays`): each CR copies its own files; never push that branch. 289 adds fixture `c5-reading.md`; 293 and 292 reuse it.
- Shared files: `tableCellEditor.ts` (293, 292, 291); pending navigation `pageRuntime.ts`, `blockEditor.ts`, `editMode.ts` (293, 291); all: `run.ts`, `capture.py`, `scenarios.ts`, `scenarioIds.ts`, `requirements/tiers/log.md` and generated requirement files, `CHANGELOG.md`. `capture_edit_checks.py` and `runtimeTableCellEditor.test.ts` are at their line limit: new files instead.
- Autonomy (owner): routine steps go without asking (rebase, amend, squash, `git push --force-with-lease` of a CR branch; landing, archiving, removing worktrees). One commit per PR. Small clear CI failures are fixed, the failing tests rerun locally, amended and pushed, reported in one line. Escalate to the Chief of Staff only a dangerous operation (merge, release, push to main, discarding work) or a blocker (classifier refusal, round limit, product question). A refused action is reported, never retried or handed to another agent.
- Before the first push of any CR, run the local gate (`just check`), even for a text-only change.
- Step 12 Land writes `report.md` and `retro.md` (see "`retro.md` (archive)" in the lifecycle). GitHub deletes the head branch on merge; keep `-assets` branches.
- Foreman heartbeat: ScheduleWakeup 600 s. Report only state changes; open every turn with the counts line.

- CRs 290, 289, 293, 292, 291 landed 2026-11-11 (PRs #358 #359 #362 #363 #364 merged 17:58 by the owner), step 12 done. CR 288 (#365) still open, round 2 in CI.

- CR 288 landed 2026-11-11 (PR #365 merged 19:29 by the owner, merge abc9e650), step 12 done. Run complete: 6 CRs landed.

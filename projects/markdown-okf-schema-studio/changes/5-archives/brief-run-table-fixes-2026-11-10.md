# Foreman brief

Run: table fixes. Now a STACK of six CRs (QA 271 P2 batch), bottom to top: 278, 279, 277, 280, 282, 281 (stack mode of the process guideline: one stack driver, one driver per CR). Open-PR cap: 7 (the whole stack, plus CR 283 outside it). Main session: the session that
started you (Chief of Staff). Started 2026-11-10 at the owner's request.

| CR | Folder | Worktree | Branch |
| --- | --- | --- | --- |

Landed in this run: CR 268 (PR #337), CR 269 (PR #338), CR 270 (PR #339), CR 272 (PR #340), CR 273 (PR #341), release 1.6.0 (CR 275, PR #342, published), CR 274 (PR #343), CR 276 (PR #344).

## Owner's decisions

In `03-change-spec.md` of the CR.

## Notes for this run

- Write files under `.agents/changes/` through short shell scripts with absolute paths. Run
  `just orchestrator /Users/az02065/Projects/DevTools/markdown-okf-schema-studio/.agents/changes`
  from a checkout of current `origin/main` (the main checkout may be stale).
- CR 273 (GitHub issue #334, started by the owner's "enchaine les CR"): blast radius 2 (new rendered syntax, front matter values in the page): the Inspector uses Opus. The PR body says `Fixes #334`; never comment on the issue (the main session does it after the owner approves). If the driver hits the classifier or another tool refusal, it reports it in its return; the Foreman does not retry a refused message. Use a general-purpose agent for the driver.
- Heavy CI run on the branch required (rendering change).
- Only the owner merges; never touch auto-merge. When the PR is green, report `ready` to the main
  session. After the owner merges, do step 11 in full: set the archived `STATUS.md` header to
  `driver: none`, `status: landed`, `step: 11 Land`, run state `pass`, and check that the
  orchestrator lists the CR under Landed.
- A QA campaign on tables runs at the same time in another session with real VS Code windows; this
  CR runs no real VS Code window locally: CI runs those tests (headless unit, visual and check gates are fine).
- Backlog items are not started: only the owner decides.
- Owner rule (2026-11-10): a PR opened before it is mergeable is a draft. The driver opens it with
  `gh pr create --draft` and runs `gh pr ready <n>` only when it reports `ready` (CI green at the
  head, review approved); an already open PR is converted with `gh pr ready --undo <n>`. ci.yml runs
  on drafts.
- CR 276 (process, owner's go 2026-11-10): guidelines text only, blast radius 1, Inspector on
  Sonnet, no heavy CI run. No GitHub issue in this project: no `Fixes`, no issue comment. Never
  touch the Chantier repository (its part is issue gsemet/chantier#101).
- QA 271 P2 stack (owner's go 2026-11-10): order 278, 279, 277, 280, 282, 281 (shared files: 278/279 `markdownTable.ts` parse; 277/280 `hostEvents.ts`; 277/282 `tableCellEditor.ts`; all: `run.ts`, `requirements/tiers/log.md`, generated requirement files, `CHANGELOG.md`). Inspector Opus for 277, 279, 280; Sonnet for 278, 281, 282. Heavy CI run on each branch. No GitHub issue: no `Fixes`, no issue comment.
- Each PR of the stack is a draft and turns ready ON ITS OWN as soon as it is mergeable (owner's rule, now in the process guideline since PR #344). The owner merges the stack.
- Replays come from local branch `qa/271-table-campaign-replays` (87307e8f): each CR copies its own files; never push that branch.
- If `gh pr ready` or another action is refused by the classifier, report it; do not retry or hand it to another agent.
- Foreman heartbeat (owner, 2026-11-10 23:45): ScheduleWakeup 600 s, not 270 s (this nested session uses a 1-hour prompt cache). Report only state changes; never re-report a relayed driver result.
- CR 283 (process, owner's go 2026-11-10 23:50 "Oui corrigé dans une CR"): NOT in the stack; its own branch from origin/main and its own draft PR. Guideline text only, blast radius 1, Inspector on Sonnet, no heavy CI run, no GitHub issue. Never touch the Chantier repository.
- CR 280 round 4 granted by the owner (2026-11-10, "Oui"): docs and commit trailer only (REVIEW-119 scenario row, real model in Assisted-by), no code change.

- State 2026-11-10 23:59: 278/279/277 ready, draft PRs #346/#347/#348 with heavy CI; 280 ready (bc3ce7e4, round 4/4), 282 and 281 ready, not yet pushed (stack driver ade5bb46 working); 283 PR #345 wait-ci.
- PR body (owner, 2026-11-11, after PR #345): every PR, process CRs included, follows `.github/PULL_REQUEST_TEMPLATE.md` and `pull-request.guidelines.md` (Summary, Deliverables, Changes, Impacts, Blast radius, Test plan). Write the body from the template file, never a short ad-hoc body.

- CR 283 landed (PR #345, merge 87a9d7aa), step 11 done 2026-11-11.
- Before `gh pr ready` (owner, 2026-11-11): the driver or stack driver checks the posted body has the six template sections and matches the diff at the pushed head; fix with `gh pr edit --body-file` first.
- CR 280 round 5 granted by the owner (2026-11-11, "Oui" to "Round 5 pour la CR 280, diagnostic d'abord, correction produit permise si prouvée ?"): first a debugger diagnosis of the two failing real-window scenarios (`scenarioUndoRestoresCommentMark`, `tableCommentUndo.ts:92`, and comment-anchors "thread placed again"); a product fix is allowed only if the diagnosis proves it. Then restack 282 and 281 on the fixed 280. Merge order for the owner: #346, #347, #348.
- 2026-11-11 07:36: owner merged #346 (278), #347 (279), #348 (277); all in origin/main (2f58ab11, ee6c3a48, 74f0bc5f). Stack bottom is now 280 on main. Remote branches 277/278/279 kept until the owner says to delete them.

- 2026-11-11: CR 278, 279, 277 landed (PRs #346, #347, #348; 2f58ab11, ee6c3a48, ad7b5636+74f0bc5f), step 11 done; remote branches left for the owner. 280 is the bottom of the stack: rebases on origin/main, PR #350 targets main.
- 2026-11-11 08:24: owner merged #350 (280). #351 (282) now targets main and must be rebased on origin/main; #352 (281) follows.
- Screenshots (owner, 2026-11-11, "je ne vois plus de screenshot dans ces PR"): a CR that changes what the user sees has before/after screenshots in Impacts, per "Screenshots in the PR" of pull-request.guidelines.md (from the e2e/visual run of the final code, light and dark, raw blobs on `change-requests/<id>-<slug>-assets`). No screenshot = not mergeable: do not run `gh pr ready` before they are in the body.

- 2026-11-11: CR 280 landed (PR #350, 99c2a2b4), archived. Its worktree and local branch are kept until the stack driver has rebased 282/281 (they were stacked on it); remove them after.
- CR 284 (process, owner's go 2026-11-11 "Rajoutes juste un vérifier simple qui vérifie la même chose que dans Chantier"): NOT in the stack; worktree `/Users/az02065/Projects/DevTools/markdown-okf-schema-studio.worktrees/284`, branch `change-requests/284-verifier-step` from origin/main, its own draft PR. Guideline text only, blast radius 1, Inspector on Sonnet, no heavy CI run, no GitHub issue. Never touch the Chantier repository. Open-PR cap stays 7.
- #352 (CR 281) screenshots (owner, 2026-11-11, "Add a scenario"): no waiver; a new round adds a small visual scenario (before: click lost, after: click reaches the field), images in Impacts, then heavy CI and ready.
- Owner (2026-11-11): once #352 and #353 are merged, the Chief of Staff checks the heavy pipeline on main and advises whether a release is worth preparing.

- CR 282 landed (PR #351, merge 48a81d08), step 11 done 2026-11-11; CR 280 worktree and local branch removed. #352 (281) now targets main.
- Autonomy (owner, 2026-11-11): routine steps go without asking the owner (land and archive, remove worktrees, relay rules, process judgment calls). Escalate to the Chief of Staff only a dangerous operation (history rewrite such as force-push, reset --hard or rebase of a pushed branch; merge; release; public post; discarding work) or a blocker (classifier refusal, round limit, product question). The Chief of Staff decides the rest and asks the owner only for the dangerous ones.
- PR branch rewrites (owner, 2026-11-11: "Le push with lease sur une PR est normal, je veux pas que tu m alertes à chaque fois, surtout que je veux un minimum de commit par PR"): rebase, amend or squash a CR branch and `git push --force-with-lease` it is a routine step for drivers and the stack driver; aim for one commit per PR. Never on main. If the classifier refuses it, report the exact text to the Chief of Staff (do not retry).

- CR 284 landed (PR #353, merge 0b2d5bcf), step 11 done 2026-11-11. The Verifier step (10) now applies to the next CRs.

- CR 281 landed (PR #352, merge 2e9cf0b9), step 11 done 2026-11-11. The run is complete: no CR left.

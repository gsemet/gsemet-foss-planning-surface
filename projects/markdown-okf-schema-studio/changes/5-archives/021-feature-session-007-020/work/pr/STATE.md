# PR — resumable state (U33, U35)

Priority (U35, 2026-10-22): make the PR mergeable FIRST, then P10. Every step below is idempotent;
on resume, re-check the "check" command of the first unticked step before redoing it.

Decisions:
- D36: remote `dev/gsemet` (d92d23d) is NOT an ancestor of HEAD (earlier PRs were squash-merged);
  pushing it would need a force push (forbidden). PR branch = `dev/gsemet-features` (new, plain push).
- D37 (revised U37): PR content = 3b6e8f4 (T1 parked, resumes after PR). P9 B5/T2/F and P10 continue locally afterwards and go
  in a follow-up PR (not pushed onto this PR unless needed to make CI green).

Steps:
- [x] S1 (revised U37) T1 parked: stash@{0} "P9-T1 WIP" + p9-e2e/parked/T1-wip.patch + T1-wip-untracked.tar. PR = 3b6e8f4. check: `git status --short` empty.
- [x] S2 merge check vs origin/main. check: `git fetch origin && git merge-tree --write-tree origin/main HEAD`
- [~] S3 (D38: local windowless `just check`+`sphinx-check` green on 3b6e8f4, log pr/check-3b6e8f4.log; full preflight delegated to CI so the user can test locally) `just preflight` green locally (screen unlocked). log: pr/preflight-<sha>.log
- [x] S4 `git push -u origin HEAD:dev/gsemet-features`. check: `git ls-remote --heads origin dev/gsemet-features`
- [x] S5 PR created (`gh pr create --base main --head dev/gsemet-features`, body pr/body.md). check: `gh pr list --head dev/gsemet-features`
- [ ] S6 CI green (`gh pr checks <n> --watch`); fixes = new commits + plain push. check: `gh pr checks <n>`
- [ ] S8 (U38) after S7: move P9 rest (T1 stash/patch, B5, T2, F) to backlog/P3/e2e-campaign-rest/, write the final report, then `mv requests/feature-session archives/021-feature-session-007-020`.
- [ ] S7 mergeable confirmed (`gh pr view <n> --json mergeable,mergeStateStatus`), URL reported.

Log:
- 2026-10-22: state created; origin/main 9df67aa, HEAD 3b6e8f4 is 0 behind / 62 ahead, merge-tree clean.
- [x] S3b VSIX: pr/markdown-okf-schema-studio-3b6e8f4.vsix; local build for the user to test (VSIX + install instructions).
- 2026-10-22: pushed dev/gsemet-features (3b6e8f4), PR #11 https://github.com/gsemet/markdown-okf-schema-studio/pull/11. Next: S6 watch CI.
- 2026-10-22: screenshots added to PR body (branch pr-assets/11 @63e56f1, images from visual run 3b6e8f4 + real-input JYSBC4; 014/018 have none). Delete pr-assets/11 after merge.
- 2026-10-22: CI run 1 red (Linux): P4 caret check (caretRectOf bottom bug) + realInput table toolbar moved 8.28px (reveal under P8 controls). Fix fb901fd pushed. Watching run 2.
- 2026-10-22: run 2: P4 fixed; table cell still +8.28 (no controls overlap). Pushed short-page tolerance + diag. Watching run 3.
- 2026-10-22: run 3: diag {menuHeight 86.28, scrollY 92, maxScroll 346, no controls overlap} -> sticky-band reveal hypothesis; pushed. Watching run 4.
- 2026-10-22: pr-assets/11 held LFS pointers (hash-object applied the LFS filter); recreated raw PNGs on pr-assets/11-png @425102c, PR body updated. Delete both pr-assets/11 and pr-assets/11-png after merge.
- 2026-10-22: run 4: menuTop 82 vs band 30.6 -> reading offset; pushed. Visual flake seen: sticky-3 light [read:properties] control under toolbar (passed runs 2-3). Watching run 5.
- 2026-10-22: run 5 (d5ffaff): table OK, visual OK; new fail realInput scenarioListLinkCompletion 'resolved StRS-A link' timeout (first time reached on CI). Rerun of failed job to test flakiness.
- 2026-10-22: run 5 failure root cause: stale stem index (lookup.unavailable) -> fix + unit test (fails on old code). Pushed. Watching run 6.
- 2026-10-22: run 6 (3f658a0): realInput+visual OK; imagePicker 'outside' test broken on Linux (/tmp is a workspace folder). Fixed + clearance observer + capture settle. Watching run 7.
- run 7 (8c55e48): checks GREEN (17m55s). pages/release/tag-release skipped (main-only jobs). PR MERGEABLE, BLOCKED only by REVIEW_REQUIRED.

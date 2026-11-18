# Each feat and fix commit since v0.12.0, and its place in the notes

`git log --no-merges --format="%h %s" v0.12.0..origin/main` at 4bf3f58: 14 commits (N = 14), 12 of them `feat:` or `fix:`. The two `docs(cards):` commits (c597a705, ee80f03a) are named under "For contributors".

| Commit | Subject | Place in the notes |
| --- | --- | --- |
| a7f32370 | feat(watch): one forge hub per surface and machine, and watchers that wake each session | Highlight "A merge on the forge wakes the Chief of Staff" |
| bdd27e0f | feat(batch): switch a Foreman batch to direct mode with CRs in flight | Highlight "Switch a Foreman batch to direct mode" |
| 4bf3f582 | feat(archive): a CR's archive stays out of the PR unless the project says yes | Highlight "The CR archive stays out of the PR" |
| f02fbbf1 | feat(pane): show the batch's shape next to its slots | Smaller changes, "The pane shows the batch's shape" |
| 327b8107 | feat(driver): start a CR Driver in its worktree and stop background tasks when done | Smaller changes, "A Driver starts in its worktree" |
| 179afb7d | feat(cards): a session whose chantier CLI cannot run stops at once | Smaller changes, "A CLI that cannot run stops the session" |
| 1d6b0735 | feat: add a project logo and a t3.json that points T3 Code to it | Smaller changes, "A logo" |
| 3c4bf53f | fix(cost): show the same steering figure in the board receipt and the cost text | All fixes, "The cost receipt after a switch" |
| 5717626d | fix(status): print the forge hub and watch lines after the last closed batch | All fixes, "`status` after a closed batch" |
| 7be9c543 | fix(board): hide a document's front matter in the panel | All fixes, "The board's panel" |
| 4a49d5c7 | fix(planning): ignore work/gates/ at any depth of the planning folder | All fixes, "The planning folder's ignore list" |
| ef3d423d | fix(summary): print a folder path that summary set can read in the lint hint | All fixes, "The summary lint hint" |

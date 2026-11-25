# Verify CR-491, round 1 after rebase

Head: 8d4af3c7a5589e95b4cfa3deeec96461e147c1c9

Claims (worktree batch-09-CR-491):

1. Clip proof (take, GIF/MP4/WebM, check.json, stage, scenario, themes page) - carried from 03becef: the move was a rebase onto the CR-490 branch.
   `git diff --stat 03becef HEAD -- docs/demo-video/clips/theme-switch docs/user/themes-and-motion.md` printed nothing at 8d4af3c7 (files byte-identical).
2. Clip kit tests at 8d4af3c7: `just clip-kit-test` -> `tests 35, pass 35, fail 0` (includes "the shipped theme-switch clip.md reads as the clip the owner reviews" and "the stage of the theme-switch scenario is the shipped stage file, byte for byte"; the merged hunks of check.test.mjs and storyboard.test.mjs keep both sides).
3. Site test at 8d4af3c7: `node scripts/node-test.mjs unit "out/test/site/siteClips.test.js"` -> `tests 14, pass 14, fail 0`, with "the shipped themes page plays the theme switch clip as video" and the slash-menu grid case both passing.
4. `just check` passed at this head (given by the Driver; not rerun).
5. PR #509 (`gh pr view 509`): headRefOid 8d4af3c7a5589e95b4cfa3deeec96461e147c1c9, isDraft true; the posted body equals pr-body.md (diff: one trailing blank line only).
6. PR body links: GIF, MP4, WebM raw URLs at 8d4af3c7 answer 200 (`curl -sIL`: image/gif, application/octet-stream, audio/webm). The body names the head SHA in every link; its "35 tests, after the rebase" matches claim 2.
7. PR body consistency: Changes lists the clip folder, themes-and-motion.md and the three test files; `git diff --stat <CR-490 branch> HEAD` shows exactly these 20 files, none in src/ or the clip kit lib. Known gaps lists the unwatched motion and the screencast rate; no role name outside Internal references; no username image attached (images carried, unchanged).

VERIFIED

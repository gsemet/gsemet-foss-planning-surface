# Verify CR-494

Head: 6b54c6e6cab1481ad1ecf13a77e210afa1ccb564

All claims judged at 6b54c6e6 (`git rev-parse HEAD` in the worktree, equals `gh pr view 514 --json headRefOid`; PR is a draft: isDraft true).

1. check.json (read at the head): passed true; length 12; mp4 1280x720 15 fps h264, webm vp9 1280x720 15 fps; gif 960 px loopCount 0; loopSeamSsim 0.992573; take.verifyPassed true, check "scenario verify passed"; host.platform win32, extensionSource vsix, vscodeVersion 1.147.0. Matches the spec's Evidence list.
2. Clip files exist in the tree (`git ls-files -s`): table-anchors.gif/.mp4/.webm, clip.md, stage, scenario, frames, poster, contact sheet.
3. PR body links resolve: `curl -sIL` of the three raw URLs at 6b54c6e6 end in HTTP 200: gif image/gif 1704493 bytes, mp4 519040, webm 356627, equal to check.json bytes.
4. `just clip-kit-test`: 37 pass, 0 fail (includes "shipped table-anchors clip.md" and "stage" tests).
5. Site test: `npm run compile`, then `node scripts/node-test.mjs unit out/test/site/siteClips.test.js`: 15 pass, 0 fail, including "editing page plays the table handles clip as video".
6. PR body vs diff (`git diff origin/main --stat`, 21 files): Summary, Changes (clip folder, docs/user/editing.md, kit and site tests) match; sections render; gif inline at the head SHA; Known gaps "None" with the owner-judged items stated separately; no username in clip.md, check.json, scenario.mjs (grep count 0).
7. Contact sheet opened as an image: shows the row drag, the column drag, the zoom on the raw text with two orange marks, two captions in turn; no username or home path visible; texts say "handle".

Not re-proved: motion, rhythm, loop as watched, real-window behaviour (the coder's take, CLIP_PORT=9494); I did not film. The GIF/MP4/WebM were checked for existence and size, not played. Review box unchecked in the PR (draft); no Review claim to judge. CI not checked (Driver).

VERIFIED

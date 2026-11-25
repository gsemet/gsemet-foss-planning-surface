# Verify CR-495

Head: d930238cc64eee77fe5dc0ad25c574a7231b7f5a

All claims judged at d930238cc64eee77fe5dc0ad25c574a7231b7f5a. No clip was retaken.

1. Committed clip files exist (`git ls-files -s`, `git lfs ls-files`): mp4, webm, gif, poster, contact-sheet, first-last, 9 frames, check.json, scenario, clip.md, stage (2 files); media are LFS-tracked. PASS.
2. `check.json`: passed true, verifyPassed true, length 12, mp4 1280x720 15/1 12.000 s, webm 1280x720 15/1, gif 960 px 12 fps loop 0, loopSeamSsim 0.990696, playbackRate 0.995, readingMode on, paste false, platform win32, extensionSource vsix, all 20 checks ok. `ffprobe` on the committed files: mp4 h264 1280x720 15/1 duration 12.000000; webm vp9 1280x720 15/1; gif 960x540 12/1. PASS.
3. `just clip-kit-test`: 37 tests, 37 pass, 0 fail (includes the figure-editor clip.md case and the stage case). PASS.
4. Site test alone: `node scripts/node-test.mjs site out/test/site/siteClips.test.js` after `npm run compile`: 15 pass, including "the shipped editing page plays the figure editor clip as video". PASS.
5. Stage and EXPECTED: `stage/harbour-guide.md` is the figure of the expected result with only the `:alt:` option; `EXPECTED` in `scenario.mjs` equals the clip.md block (the kit case that compares them passes). PASS.
6. `docs/user/editing.md` diff carries the GIF line `../demo-video/clips/figure-editor/figure-editor.gif` in the palette bullet. PASS.
7. Frames looked at (contact-sheet, rendered, 04-mark-1): form flow, Edit figure button, directive with three new lines outlined, keycap Ctrl+Enter / Cmd+Enter at the save, figure floating right with caption and orange outline; window title shows "workspace" only, no personal name or path. PASS. Not checked: motion, rhythm, the loop as watched.
8. PR #515 is draft, head d930238; the posted body equals `work/pr-body.md` (one trailing newline difference); the summary, changes and deliverables match the diff (24 files); links point to the head SHA; Known gaps lists the form cut, the scrolled page and Windows only; the Deviation and Autonomous decisions sections are present. CI at d930238 (`gh pr checks 515`): static, static-windows, viewer-graph, visual, report, checks pass. PASS.
9. `just preflight` and `just check`: taken from the Coder's and CI's runs (static and static-windows green at the head); not rerun here.

VERIFIED

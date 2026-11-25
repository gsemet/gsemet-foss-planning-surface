# Verify CR-492

Head: 211f3a59ec3e1a7d0c6589fd3ddfaa081b8d3b66

Claims, all judged at 211f3a59:

- Diff scope: `git diff origin/main...HEAD --name-only` shows only docs/ (clip folder, editing.md), clip-kit tests, test/site/siteClips.test.ts; no src/ or skills/ change.
- `just clip-kit-test`: 37 pass, 0 fail, including "the shipped radio-buttons clip.md reads as the clip the owner reviews" and "the stage of the radio-buttons clip differs from the expected text by the moved x only".
- Docs-page test: `npm run compile`, then `node scripts/node-test.mjs unit out/test/site/siteClips.test.js`: "the shipped editing page plays the radio clip as video" passes, 15 pass 0 fail. (Plain `node --test` fails on all 8 clip page tests alike, a module resolution quirk of the worktree, not the CR.)
- check.json: passed true; mp4 and webm 1280x720 15 fps, mp4 10.533 s vs Length 10.5, gif 960 px 12 fps loop 0, loop seam SSIM 0.99529, verifyPassed true, reading mode off, playback rate 1.003, platform win32, source vsix, 19 checks all ok.
- editing.md shows the GIF right after the radio paragraph "On GitHub and in plain editors ..." (diff checked).
- Frames are this clip's own (radio choice): opened contact-sheet.png, pointed.png, chosen.png, 05-mark-2.png. Reading mode left, raw text right; pointed: first option selected, `(x)` on line 7; chosen: second selected, `(x)` line 8, no focus ring; mark 2 on old `( )` line 7; captions in turn. No username or home path visible; no "gaeta" in clip.md, scenario.mjs, check.json.
- LFS: all clip renders and frames are LFS-tracked (`git lfs ls-files`).
- PR 513: draft, head 211f3a59, body posted equals work/pr-body.md (trailing newline only); links use the head SHA; no internal references; has the Deviation section.

VERIFIED

## Description pass

Head: 211f3a59ec3e1a7d0c6589fd3ddfaa081b8d3b66

- Body read with `gh pr view 513 --json body,headRefOid`: headRefOid is the head above; sections render (Summary, Deliverables, Changes, Deviation, Impacts, Blast radius, Test plan).
- `curl -sL -w %{http_code}` at the head SHA: radio-buttons.gif, .mp4, .webm and clip.md all return 200.
- Changes match `git diff --stat origin/main...HEAD` (19 files: clip folder, docs/user/editing.md, clip-kit and site tests); no extension code change, as Impacts says.
- No role names, CR or batch numbers, username or home folder in the body. No UNVERIFIED claim in verify.md, so no Known gaps needed; the Review box is unchecked, as expected for a draft.
- Verdict: VERIFIED.

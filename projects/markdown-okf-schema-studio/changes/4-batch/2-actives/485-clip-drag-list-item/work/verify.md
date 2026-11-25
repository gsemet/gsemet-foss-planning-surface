# Verify CR-485

Head: 8197e4fd6b49d655dac95b3ef567db25c4f3a795

All claims judged at 8197e4fd (worktree head = PR head, tree clean).

## Claims

1. Kit tests (`checks`, `resolveChecks`, `takeLines`, `keyFrameTimes`, shipped clip.md and scenario cases).
   Command: `just clip-kit-test`. Output: `tests 25, pass 25, fail 0`, including "a key frame name that takes a numbered kit name or is repeated is refused" and "the shipped drag-list-item clip.md reads as the clip the owner reviews". PASS.
2. Clip's own check on the committed clip. Command: `just clip drag-list-item check`. Output: all lines `ok`: mp4 1280x720 15/1, no audio, 10.533 s vs Length 10.5 s, webm vp9, gif 960 px 12 fps, loop seam SSIM 0.99452, "scenario verify passed: true", "Studio in edit mode at the start: on", no paste line, playback rate 1.004. `git status` clean afterwards. PASS.
3. Site test. Command: `npm run compile` then `node scripts/node-test.mjs unit "out/test/site/siteClips.test.js"`. Output: `tests 9 pass 9`, including "the shipped editing page plays the list drag clip as video". PASS.
4. docs/user/editing.md plays the clip: `git diff <base>..HEAD -- docs/user/editing.md` shows the GIF image under the handle paragraph, as specified. PASS.
5. Stage file: `git ls-files --eol` gives `i/lf w/lf`; content is the specified stage. PASS.
6. Diff matches spec: 25 files (kit lib and tests, recipe, clip folder, editing.md, siteClips.test.ts), no change to `src/`. PASS.
7. Key frames, contact sheet viewed (contact-sheet.png, drag.png, 05-mark-2.png): Studio left in edit mode with handles, text editor right, drop line before "Tag the release." in drag.png, new order, mark 1 on the three lines, mark 2 on the numbers, captions in turn, no tooltip, no username or home path visible. PASS.
8. PR description (live body equals work/pr-body.posted.md; PR 503 is a draft on CR-484's branch, head matches): sections render, links name the head SHA 8197e4fd, Summary/Changes match the diff, Deviation section present, Known gaps lists motion/rhythm/loop, raw rate 3.6 fps, Windows only, draft state. No image in the body shows a username or home folder (GIF frames checked via the contact sheet). PASS.
9. Review box: round 1 approved at f42acf7c, committed as 8197e4fd per the Driver's note (given in the prompt).

## Not proved (Known gaps in the body)

Motion, rhythm, the loop as watched, raw screencast rate, non-Windows filming.
The body's "just preflight pending" is a Test plan line not claimed as fact.

VERIFIED

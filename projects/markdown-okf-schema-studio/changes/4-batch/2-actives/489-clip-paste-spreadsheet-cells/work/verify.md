# Verify CR-489 (round 2)

Head: 612623646a0dd0441fadd3425a8bcccb683945db

Verdict: NOT VERIFIED (one claim: PR body Known gaps). All judgments at 612623646a0dd0441fadd3425a8bcccb683945db.

## Claims

1. `just clip-kit-test` passes (at 61262364). Output: `tests 26, pass 26, fail 0`, including "the shipped paste-spreadsheet-cells clip.md reads as the clip the owner reviews", "EXPECTED in scenario.mjs is the Expected paste block of clip.md" and the win32/darwin story validation. PASS.
2. Site test (at 61262364): `npm run compile` then `node scripts/node-test.mjs unit out/test/site/siteClips.test.js` gives 10 pass, 0 fail, including "the shipped editing page plays the spreadsheet paste clip as video". PASS.
3. check.json at 61262364 (read with python): passed true; MP4 and WebM 1280x720, 15 fps, 10.000 s equal to Length; GIF 960 px, 12 fps, loop count 0, 1.69 MB; loop seam SSIM 0.99337 (in [0.98, 1.0)); "Studio in edit mode at the start" ok (on); verify passed true; pasteWidgets 0; playbackRate 1.004; platform win32; extensionSource vsix. All 21 checks ok. PASS (spec Evidence 2 as amended).
4. Key frames and contact sheet looked at, at 61262364: 01-selected shows the five lines selected, values in columns, no whitespace arrows; 02-pasted shows the table with the four task rows and the cell editor open on Task (third column off the pane edge, as its clip.md caption says); 03-zoomed the zoomed table with Task, Owner, Due and four rows, no cell editor; 04-mark-1 outline on column Due; 05-mark-2 outline on the three added rows; Text 1 during copy and paste, Text 2 during the zoom; badges Ctrl+C / Cmd+C and Ctrl+V / Cmd+V. No username or home path shows (title bar reads "workspace"). Note: a tooltip "Exit edit mode" shows in 01-selected and "Convert to list-table" in 02-pasted (spec Evidence 3 said no tooltip): cosmetic, left to the owner's review. The contact sheet at about 4.2 s shows the pointer on Done (the conditional Done click, disclosed). PASS with the note.
5. Diff matches the PR's Changes (at 61262364): `git diff --stat` shows the clip folder (stage, clip.md, scenario.mjs, media, frames, check.json), docs/user/editing.md (+6), check.test.mjs, storyboard.test.mjs, test/site/siteClips.test.ts; no src/ change. PASS.
6. Posted PR body equals work/pr-body.md (diff: only a trailing blank line). Media URLs name the head SHA. PASS.
7. PR body Known gaps: FAILS. The body states in Deliverables that motion, rhythm, the loop as watched, the GIF and WebM played and the docs page rendering were not watched, but Known gaps lists only the draft state, the conditional Done click and Windows only. Those unverified claims need their bullet there.
8. CI at 61262364: `gh pr view 505` reports checks static, static-windows, visual and viewer-graph IN_PROGRESS (not "none reported"), integration, stress, release-check, toc-loop SKIPPED; none finished. Local preflight.log ends `ci-static: passed ... EXIT 0` (not rerun, carried from the Driver's log).
9. UNVERIFIED by this role: motion, rhythm, the loop as watched, the played GIF and WebM, the docs page rendering.

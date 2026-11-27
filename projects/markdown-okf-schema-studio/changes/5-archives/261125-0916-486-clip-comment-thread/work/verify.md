# Verify CR-486 Feature clip: a comment thread on a passage

Head: 7a02a841ed5a119ac951e3e36b4100a4edf9bfc5

No app-window run (as briefed): every claim is read from the committed take at the head.

## Claims, all judged at 7a02a841

1. check.json passes. `docs/demo-video/clips/comment-thread/check.json` (committed, read): `passed: true`;
   MP4 and WebM 1280x720, 15 fps, 11.333 s vs Length 11.3 s; GIF 960 px, 12 fps, loop count 0; loop seam
   SSIM 0.996608; `verifyPassed: true`; `readingMode: off`; `pasteWidgets: 0`; playbackRate 1.005;
   platform win32; extensionSource vsix; vscode 1.147.0 pinned; 20 checks, all `ok: true`. The 11.3 s
   length is the recorded decision (PR body, Autonomous decisions). VERIFIED.
2. The take's verify. `verify.json` is not committed and no `out/` copy exists (`find out -name verify.json`:
   no output). The proof is `scenario.mjs` `verify` (lines 179 to 193: throws unless version 1, one thread,
   quote, `resolved === false`, one comment by `Reviewer`, `proposal.md` unchanged) plus check.json
   `verifyPassed: true`. Accepted; the parsed file itself was not read.
3. Looked at the contact sheet and the five key frames (images opened):
   - `01-selected`: box open with "Can we keep it one more release?" typed, Save and Cancel, Text 1.
   - `02-pasted`: sentence highlighted, box closed, badge `Ctrl` `Enter` / `⌘` `Enter`, Text 1 fading.
   - `03-zoomed`: popover with Reviewer, date, comment, Resolve, Delete, Reply, mark 2 on, Text 2.
   - `04-mark-1`: orange outline on the highlighted sentence. `05-mark-2`: orange outline on Resolve
     and the Reply box.
   - Sheet: selection on the whole sentence and the Comment button at 1.883 s, popover closed at 10.358 s,
     no tooltip. Title bar reads "proposal.md - workspace"; no personal name or path
     (`grep -n "Users\|gaeta"` on clip.md and check.json: no output). Not checked: motion, rhythm, the loop
     as watched. VERIFIED.
4. Open point, the sheet frame at 8.475 s. The tile in `contact-sheet.png` shows the popover with no
   orange outline, although Mark 2 is 7.5 to 8.9 s. I extracted the same instant from the MP4
   (`ffmpeg -ss 8.475 -i comment-thread.mp4 -frames:v 1`): mark 2 is drawn there, around Resolve and
   Reply. At 8.2 s it is on, at 8.8 s it is fading (lighter outline). So the clip is right and the contact
   sheet tile at 8.475 s is the odd one (a sheet sampling that differs from the MP4, not a missing mark in
   the clip). The sheet is a committed output and misleads a reader; reported, not a failure of the clip.
5. Storyboard consistent with the scenario. `clip.md` (read): Length 11.3; Mark 1 6.3 to 7.5, Mark 2 7.5 to 8.9
   match `scenario.mjs` `MARK_1 = [6.3, 7.5]`, `MARK_2 = [7.5, 8.9]`; zoom hold 9.6 s matches
   `until(9.6)` then `unzoom`; close at 10.4 s matches `until(10.4)`; end `until(11.3)`. Sections, `Size`,
   `Frame rate`, `Zoom`, `Text 1`, `Text 2`, `Badge save` rows are present. The Review notes carry the
   settled items. VERIFIED.
6. docs line. `git diff <base>...HEAD -- docs/user/review-comments.md`: one image line added after the
   paragraph "To start a thread ..." (the hunk context ends at the authorName paragraph), alt text as the
   spec, target `../demo-video/clips/comment-thread/comment-thread.gif`. VERIFIED.
7. Scope. `git diff --stat <base>...HEAD`: 16 files, all under `docs/demo-video/clips/comment-thread/` plus
   `docs/user/review-comments.md`; no `src/`, kit, recipe, lock file. Media are Git LFS (`git lfs ls-files`
   lists 13 comment-thread entries; MP4 416650 bytes locally). VERIFIED.
8. PR description. Posted body equals `work/pr-body.md` (`diff`: only a trailing newline). Head
   `gh pr view 504`: `7a02a841ed5a...`, draft true, base the CR-484 branch. The three links name the head
   sha. Summary, Deliverables and Changes match the diff (item 7). Deviation line, Autonomous decisions and
   Known gaps (the `UNVERIFIED` LFS GIF, the empty author, Windows only, the date) present. Sections
   and fold are well formed. No image of a username or home folder (item 3). Role names: none outside
   "Internal references". That GitHub plays the LFS GIF inline is declared UNVERIFIED by the PR and was not
   checked here (no browser): carried as its own known gap. VERIFIED, with the Review box left unchecked
   (draft).
9. CI at the head. `gh pr checks 504 --repo gsemet/markdown-okf-schema-studio`: checks, report, static,
   static-windows, viewer-graph, visual all `pass`; integration, stress and others `skipping` (heavy jobs
   run on push to main only). Local gate logs in `work/scratch/preflight.log` end `ci-static: passed`
   (first lines name the run). VERIFIED.

## Evidence

No before/after pair: a new clip has no before. The captures judged are the committed clip outputs.
Verifier's scratch frames are outside the CR folder (not kept).

VERIFIED

## Description-only pass (posted PR body)

Head: 7a02a841ed5a119ac951e3e36b4100a4edf9bfc5

Judged at 7a02a84: `gh pr view 504` headRefOid equals the head; raw links for GIF, MP4, WebM at that sha exist as blobs (`git cat-file -t`) and the GIF URL returns HTTP 200 (curl -IL). check.json: 11.3 s, 1280x720 at 15 fps, GIF 960 px at 12 fps, SSIM 0.996608, playback 1.005, reading mode off, 0 paste widgets, passed true: all match the text. scenario.mjs holds the quote, the comment, author Reviewer, resolved false, proposal.md unchanged. Changes list matches the diff against the base branch (clip folder plus docs/user/review-comments.md one image line). Known gaps carries the UNVERIFIED GIF playback. CI checks, report, static, static-windows, viewer-graph, visual pass (`gh pr checks 504`). Draft: true. No STALE mark.

VERIFIED

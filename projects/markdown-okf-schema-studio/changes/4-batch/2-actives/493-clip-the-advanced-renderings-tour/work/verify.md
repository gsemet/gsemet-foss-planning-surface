# Verification of CR-493, PR #512

Head: 8c6845a50d411d894d83c7160e52e1306548330d
Base: 17b779d502b9633fd42dd275986067397db5c4aa (origin/main, equal to the merge base)

Verdict: VERIFIED

Second pass, on the posted description (edit of 2026-11-25T23:57:27Z), at the same head. The first
pass failed two description claims (F1: Impacts had neither before/after nor "No visual change";
F2: "which the other clips of the same round build on" did not hold). Both are fixed. Claims 1 to 9,
"Rest of the PR description" and "Notes" below are carried from 8c6845a: the head did not move.

`git rev-parse HEAD`, `git ls-remote origin` (branch) and `gh pr view 512 --json headRefOid`:
`8c6845a50d411d894d83c7160e52e1306548330d`; remote `main` still `17b779d5`;
`git status --porcelain` empty before the verdict. Still a draft.

## Third pass, description only, judged at 8c6845a

The posted description (edit of 2026-11-26T00:00:11Z). The head did not move, so every claim below
is carried from 8c6845a, except what E1 to E3 judge again.

- E1, the one change: unified diff of the `userContentEdits` of 23:57:27Z (judged by the second
  pass) and 00:00:11Z (`gh api graphql`, saved in `verifier/edits.log`), one hunk:
  `+- [x] Verified at `8c6845a``. `gh pr view 512 --json body` equals the latest edit, and equals
  `work/pr-body.md` (CR removed, trailing blanks ignored).
- E2, the new line holds: this note has `Head: 8c6845a5...` with VERIFIED, and `chantier log CR-493`
  shows `2026-11-25T23:59:42Z driver verdict result=VERIFIED head=8c6845a50d41...`, before the edit.
  `git rev-parse HEAD`, `gh api graphql` `headRefOid` and `git ls-remote origin` (branch): 8c6845a5;
  remote `main` 17b779d5, the PR base; `git status --porcelain` empty; `CLEAN`, still a draft.
- E3, the posted whole: `body_html` renders the headings, the fold, the table and 8 checked boxes of
  8, the new one included. No `UNVERIFIED` or `STALE` mark; the only SHAs are 8c6845a and the base
  17b779d. Images downloaded again: GIF 200, sha256 4666703c...86ba (= the committed file); before
  200, 7c8db8da...7212 and after 200, 627ab9db...026e (= `verifier/evidence/`). Both PNGs opened
  again: they show what Impacts says, with no user name, home folder or local path.
  `gh pr checks 512`: checks, report, static, static-windows, visual, viewer-graph pass (run
  45719751938); the others skipping.

## Second pass, judged at 8c6845a

### D1. The changed lines

Unified diff of the two latest `userContentEdits` of PR 512 (`gh api graphql`; 23:37:53Z, the
body the first pass judged, against 23:57:27Z). Three hunks, nothing else:

```text
@@ -3 +3 @@   "...which the other clips of the same round build on." -> "...which other longer clips can use."
@@ -58 +58,5 @@  "No behaviour change in the extension; the editing page gains a clip." ->
                 "No visual change in the extension. The editing page ... paused on the first mark)."
                 plus the table "Before (17b779d) | After (8c6845a)" with two user-attachments images
@@ -67,0 +72 @@  "- [x] Evidence: before at `17b779d`, after at `8c6845a`"
```

`diff` of `gh pr view 512 --json body` against `work/pr-body.md` (CR removed): one trailing blank
line only.

### D2. Summary (former F2): holds

"which this clip needs and which other longer clips can use": the clip is 16 s, past 12, and the
shared bound is 30 for any clip (claim 1: `MAX_LENGTH` 12 at 17b779d, 30 at 8c6845a). No claim
about other pull requests and no backlog word is left.

### D3. Impacts (former F1): holds

- "No visual change in the extension":
  `git diff --stat 17b779d5 8c6845a5 -- src package.json .vscodeignore CHANGELOG.md requirements`
  prints nothing.
- "The editing page of the user docs gains the clip": `git diff 17b779d5 8c6845a5 --
  docs/user/editing.md` adds only the tour GIF image under the "MyST rendering" bullet.
- "drawn from the page's Markdown with a plain stylesheet rather than the published theme":
  `verifier/shot.cjs` renders each commit's `editing.md` with `renderMyst` and `clipVideos` and its
  own inline style.
- "paused on the first mark": the script seeks to 1.5 s; `clip.md` row "Mark 1" is 1.0 to 2.9 s,
  and the picture shows it.
- The project rule (before/after in Impacts, or "No visual change") is met.

### D4. The images load and show their captions

A throwaway script took the `<img>` sources from `body_html`
(`gh api .../pulls/512 -H "Accept: application/vnd.github.full+json"`), downloaded each and hashed
it and the evidence files:

```text
Renderings tour: HTTP 200 image/gif 2044158 bytes 960x540 sha256 4666703c...86ba (= LFS id of the committed GIF)
Editing page before: HTTP 200 image/png 10698 bytes 820x72 sha256 7c8db8da...7212 (= evidence/editing-page-before.png)
Editing page after: HTTP 200 image/png 118032 bytes 820x550 sha256 627ab9db...026e (= evidence/editing-page-after.png)
```

Both downloaded pictures opened. Before: the "MyST rendering" bullet, text only. After: the same
text, then the zoomed clip in Cream, orange outline on the Mermaid flowchart, caption "Mermaid
diagrams, drawn in the page", PlantUML sequence and line chart below, no "week" title and no "Chart
source" line. No user name, home folder or local path in either. SHAs of the captions are those of
`verifier/evidence/before-after.md` (before 17b779d, after 8c6845a), where the capture is recorded.

### D5. Test plan, render and the rest

- "Evidence: before at `17b779d`, after at `8c6845a`": `verifier/evidence/before-after.md` and D4.
- `body_html`: the five visible headings, the `<details>` fold with its Markdown rendered, the
  table with both images, and the seven checked boxes render.
- The new lines hold no internal id and no agent role. No `UNVERIFIED` or `STALE` mark; Known gaps
  needs no new bullet, since F1 and F2 were fixed, not accepted.
- `gh pr checks 512`: checks, report, static, static-windows, visual, viewer-graph pass (run
  45719751938); the others skipping.

## Passed (first pass, carried from 8c6845a: head unchanged)

### 1. The kit accepts 5 to 30 s and refuses 4.9 and 30.1 s

`just clip-kit-test`: `tests 38`, `pass 38`, `fail 0`, exit 0, including "durationLine holds from
5 to 30 s, bounds included...", "prepared refusals: a length outside 5 to 30 s; 30.0 s is
accepted", the shipped tour storyboard and the tour's checks.
`git show <rev>:docs/demo-video/clip-kit/lib/storyboard.mjs`: `MAX_LENGTH = 12` at 17b779d,
`30` at 8c6845a. `check.mjs` imports the same two bounds for `durationLine`.
`git grep -l "5 to 12" 8c6845a -- docs .agents`: only the `check.json` of the eight merged clips.
Glossary and recipe diffs read: all "5 to 30".

### 2. The new tests fail on the previous code

Detached worktree of 17b779d with the head's `check.test.mjs`, `storyboard.test.mjs` and the
tour's `clip.md`, `scenario.mjs`, `stage/` copied in;
`node --test .../storyboard.test.mjs .../check.test.mjs`, exit 1:

```text
SyntaxError: The requested module './check.mjs' does not provide an export named 'durationLine'
x docs\demo-video\clip-kit\lib\check.test.mjs
x prepared refusals: a length outside 5 to 30 s; 30.0 s is accepted
x the shipped advanced-renderings-tour clip.md reads as the clip the owner reviews
  Error: clip.md: Length 16 s is outside 5 to 12 s
tests 23, pass 20, fail 3
```

Site test: the base's `docs/user/editing.md` renders 0 tour video elements, the head's 1
(`verifier/shot.cjs`, see `before-after.md`), which is what the new test asserts. The compiled
test itself was not run against the base. The worktree was removed
(`git worktree list` no longer shows it).

### 3. The tour reads the live chart markup

`git grep -n -E "myst-vega-image|img\.myst-vega" 8c6845a -- docs test src`: no line, exit 1.
`scenario.mjs` lines 37, 38, 54, 55 use `.myst-vega-view > svg`. `src/page/modules/vegaView.ts`
(lines 71-81) builds `div.myst-vega-view` with an `svg` renderer.

### 4. MP4, WebM, GIF, check.json and clip.md agree

`ffprobe -count_frames` on the committed files:

```text
mp4  h264 1280x720 yuv420p 15/1 240 frames 16.000000 s 568679 bytes, 0 audio streams
webm vp9  1280x720 yuv420p 15/1 240 frames 16.000000 s 334630 bytes, 0 audio streams
gif       960x540          12/1 192 frames 16.000000 s 2044158 bytes, 0 audio streams
```

`ffmpeg -lavfi ssim`, `poster.png` against MP4 frame 239: `All:0.995060` (check.json 0.99506).
`psnr`, poster against frame 0: `inf`. GIF NETSCAPE2.0 loop bytes `0301000000`; MP4 boxes
`ftyp,moov,free,mdat`. `git lfs ls-files -l` ids equal the SHA-256 of the working files.
`check.json`: `passed: true`, "mp4 duration within 5 to 30 s" ok, ladder step 0, `verifyPassed`,
reading mode, no paste line, playback 1.003, win32, vsix, VS Code 1.147.0, extension 1.12.1;
clip.md says Length 16.0 s.
Take records left by the recording (`C:/okfclip493/advanced-renderings-tour/take/`, written
22:53 to 22:55 UTC, before the commit at 23:13:52 UTC): `verify.json` `passed: true`,
`scroll: "scrollTo"`, `unchanged: true`; `take.json` all six mark rects inside the zoom rect.
`just clip advanced-renderings-tour check` was not run (it rewrites `check.json`); no take or
render was run.

### 5. The pictures

Opened: contact sheet, first-last, poster, `03-zoomed`, `04` to `09`, tiles of MP4 frames (every
6th, and 7.4 to 9.4 s), of the GIF (every 12th) and of the WebM. Own stage and window
("search-design.md - workspace"), Cream, reading mode; six drawings, each with its mark and
caption; marks 3 and 4 whole above the caption; bar axis 0/20/40 readable; no tooltip, personal
name or path seen. `git grep -n -i -E 'gaeta|c:\\users|c:/users|/home/|/Users/'` on the clip
folder: no line, exit 1. Motion as watched was not judged.
Mark 4: first visible in the 8.267 s frame, the frame of the last scroll step; frame differences
on static crops are about 0 from 8.333 s. In the 915f2bf4 MP4 (read with
`git cat-file --filters`) the same crop still changes up to 8.8 s while mark 4 shows from
8.267 s, so "the fourth mark now appears on a still page" holds. The earlier frames also show the
"Chart source" lines, the "week" title and the overlapping y ticks the body says are gone.

### 6. Captions, times and marks unchanged against 915f2bf4

`diff` of the `Length`, `Time`, `Zoom`, `Mark 1-6` and `Text 1-6` rows of `clip.md` at 915f2bf4
and 8c6845a: identical (20 rows).

### 7. The editing page shows the clip

`just compile`, then
`node scripts/node-test.mjs unit out/test/site/siteClips.test.js`: `tests 15`, `pass 15`,
`fail 0`, including "the shipped editing page plays the renderings tour clip as video".
Pictures: `verifier/evidence/before-after.md`.

### 8. Scope, requirements, changelog

`git diff --numstat 17b779d 8c6845a`: 25 files; kit, recipe, one glossary line, the clip folder,
`docs/user/editing.md`, `test/site/siteClips.test.ts`. `git diff --quiet` on `src`,
`CHANGELOG.md`, `requirements`: unchanged. `just requirements-update`: "0 files updated",
"0 indexes updated", "0 requirement OKF projections updated", exit 0, tree clean.

### 9. Gates

- `just preflight`, Windows static stage: log `work/scratch/preflight-8c6845a.log` (written after
  the commit; first line `rm -rf out .artifacts`, no SHA in it): `ci-static: passed`, test totals
  with `fail 0`. Tied to the head by the CR log: "at 8c6845a: just preflight (Windows static
  stage): pass, tree clean". Not rerun here.
- `gh pr checks 512`: checks, report, static, static-windows, visual, viewer-graph pass (run
  45719751938); the others skipping. The CR log records one re-run after a Git LFS timeout.

## Rest of the PR description (first pass, unchanged lines, carried from 8c6845a)

- Draft, base `main`, head 8c6845a, `CLEAN` at the first pass. The draft state was not judged.
- `body_html`: headings, line breaks, fold and GIF image render. The GIF, MP4 and WebM links at
  8c6845a answer 200 and their SHA-256 equals the committed LFS ids.
- Owner approval of the storyboard and the earlier cut: `02-answers.md`, "Owner approval
  (2026-11-25, evening ...)".
- "Review: passed at 8c6845a": CR log "r3 approved at 43653245..., committed as 8c6845a5".
- "the CDP wheel never moved the webview page": the take's `scroll: "scrollTo"` (picked only when
  the wheel trial moves nothing), and the notes of round 1.
- Known gaps lists the unwatched re-filmed cut, motion not judged, Windows only.
- No agent role as the doer outside "Internal references".

## Notes, not failures

- "every setting at its default": the kit's take profile does set VS Code settings and
  `markdownOkfSchemaStudio.comments.authorName`; no rendering setting. Worth narrowing while the
  body is edited.
- Specification section 8 asks for a link to `clip.md` and a line saying a retake is a follow-up:
  the body names the path only and has no such line.
- The `wheel` branch of the scenario's scroll did not run on this machine (round 2 notes).
- Process: two of the Verifier's early shell calls changed folder into this CR's `work/scratch`,
  against the startup core; nothing was left running or changed by it.
- The Verifier's throwaways (`work/scratch/vf`, the base worktree) are removed.
  `C:/okfclip493` belongs to the recording and was only read.

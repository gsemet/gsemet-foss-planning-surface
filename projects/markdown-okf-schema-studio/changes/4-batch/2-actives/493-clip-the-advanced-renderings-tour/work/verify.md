# Verification of CR-493, PR #512

Head: 8c6845a50d411d894d83c7160e52e1306548330d
Base: 17b779d502b9633fd42dd275986067397db5c4aa (origin/main, equal to the merge base)

Verdict: NOT VERIFIED

The change itself holds (claims 1 to 9). Two statements of the posted PR description fail
(F1, F2). Both are fixed by editing the body; no code or media change is needed.

Every claim below was judged at 8c6845a. `git rev-parse HEAD` and
`git ls-remote origin <branch>` both give that SHA; `git status --porcelain` is empty after the
checks.

## Failed

### F1. Impacts holds neither before/after screenshots nor a "No visual change" line

Rule, `.agents/guidelines/pull-request.guidelines.md`: "Impacts holds the evidence of the change:
the before/after the Verifier produced (screenshots ...), or one line "No visual change" with the
reason. [...] the Verifier fails a body whose Impacts has neither."

`gh pr view 512 --json body` (and the rendered `body_html`), the whole section:

```text
## Impacts

No behaviour change in the extension; the editing page gains a clip.
```

It has no screenshot, and it speaks of behaviour, not of what is visible; the editing page does
change visibly. Fix: attach `work/verifier/evidence/editing-page-before.png` and
`editing-page-after.png` in Impacts (guideline "Screenshots in the PR"), captioned 17b779d and
8c6845a, with a line saying the extension has no visual change.

### F2. "which the other clips of the same round build on" does not hold at this head

Summary says of the 30 s bound: "which this clip needs and which the other clips of the same round
build on." For each other open clip PR (`gh pr view <n> --json headRefOid`, then
`git show <head>:docs/demo-video/clip-kit/lib/storyboard.mjs` and
`git merge-base --is-ancestor e0d723d5 <head>`, e0d723d5 being this PR's earlier kit commit):

| PR | `MAX_LENGTH` | holds this PR's earlier commits | its clip's Length |
| --- | --- | --- | --- |
| #513 | 12 | no | 10.5 s |
| #514 | 12 | no | 12.0 s |
| #515 | 12 | no | 12.0 s |
| #516 | 30 | yes | 18.0 s |
| #517 | 30 | yes | 11.5 s |
| #518 | 12 | no | 12.0 s |
| #519 | 12 | no | 10.6 s |
| #521 | 12 | no | 12 s |
| #522 | 30 | yes | 20.0 s |

Six of the nine do not build on it. Their specifications read for 495, 496, 497, 498 and 499 say
they stay within 12 s or have no `depends.json`; this CR's specification ("Base and stack") says
only the clips longer than 12 s depend on it. "Round" is also a backlog word the outside reader
does not know. Fix: narrow, for instance "which the longer clips (the export and the keyboard
navigation clips) build on".

## Passed

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

## Rest of the PR description

- Posted body equals `work/pr-body.md` (one trailing blank line apart). Draft, base `main`, head
  8c6845a, `CLEAN`. The draft state was not judged.
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

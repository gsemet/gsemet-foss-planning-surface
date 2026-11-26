# Verify CR-500

Head: c7c6a562420e55b83356a366806f57ff67a9c100

Replaces the verdict on b0e6c6d (clip since reworked and filmed again). Every claim below is judged at
c7c6a56 (PR 516, draft, base chantier/batch-09/cr-510-..., base head 7d35be3). No take, render or app
window was run. No before/after captures (brief: no extension UI change; the visual is the committed clip).

## Verdict

NOT VERIFIED: one Known gaps claim of the PR body is contradicted by the take and by the committed MP4
(claim F). Every other claim checked holds.

## F. FAILED, at c7c6a56: "each of the two scrolls shows as one cut ... The filmed window sends no new frame while the exported page scrolls"

- `node -e` over `C:/okfclip-500/export-html/take/frames.json` (seconds from the first frame, frames
  after 9.9 s): `512 frames`; `507@9.956 508@9.960 509@10.000 510@11.014 511@12.054 512@14.135`.
  The browser wheel is sent from 10.8 s (scenario.mjs). Frame 510 arrives during the first scroll.
- Raw frames 509 to 512 tiled and looked at: 509 is the top of the page, 510 (11.014 s) an intermediate
  scroll position, 511 the wide table, 512 the flowchart and the bar chart.
- `ffmpeg -i export-html.mp4 -vf "select=between(n,150,260),crop=1280:480:0:100,tblend=all_mode=difference,signalstats,..."`
  (time base 1/90000), YAVG: `pts 990000 (11.0 s) 3.51`, `pts 1080000 (12.0 s) 7.77`,
  `pts 1272000 (14.13 s) 17.34`; the other values above 1.0 are the zoom (10.4 to 10.7 s, 17.2 to 17.3 s).
  The rendered clip shows a short step at 11.0 s, then the jump at 12.0 s.
- So the first browser scroll shows as two jumps, not one cut, and the window did send a frame while the
  exported page scrolled. The second scroll is one cut.
- The same wording is committed: `clip.md` line 72 and lines 179 to 182 ("only two come after 11 s of
  it, at 12.0 and 14.1 s of the take": three do, 510, 511, 512), and the comment at scenario.mjs lines
  471 to 472.
- Narrowing that the evidence supports: the first browser scroll shows as a short step at about 11 s then
  a cut at 12 s, the second as one cut at 14.1 s; the window sent one frame at the start of the first.

## Claims that hold, all at c7c6a56

1. Head. `git rev-parse HEAD` and `git ls-remote origin refs/heads/chantier/batch-09/cr-500-...`: both
   c7c6a562420e55b83356a366806f57ff67a9c100; `git status --porcelain` empty.
2. Review box "carried from 8ce169f: a clean rebase, the same four commits".
   `git range-diff 5a73b6e..8ce169f 7d35be3..c7c6a56`: `8b759974 = 6ee2da0d`, `8d6b6248 = 2256a6da`,
   `25fe7997 = 7f4f9820`, `8ce169f0 = c7c6a562`; `git patch-id --stable` equal per pair.
   `git diff --name-status 5a73b6e 7d35be3`: only pull-request.guidelines.md,
   scripts/check-no-merge-commits.sh, test/build/test_no_merge_commits.py. `log CR-500`:
   2026-11-26T02:16:56Z "r4 inspector approved at 8d6b6248", 02:17:28Z "committed as 8ce169f",
   04:30:28Z "approval carried to c7c6a56".
3. Local gates. `work/gates/c7c6a56-preflight.log` first line "CR-500
   chantier/batch-09/cr-500-clip-export-a-long-report-page-same-rend head
   c7c6a562420e55b83356a366806f57ff67a9c100"; `== clip-kit-test exit 0` (56 pass), `== check exit 0`
   (5306 tests, 5299 pass, 0 fail; 107/107; 212 passed), `== requirements-update exit 0`,
   `ci-static: passed`, `== preflight exit 0` (Windows static stage; other stages skipped), last line
   "head after c7c6a562...". `handoff CR-500` checklist at PR head c7c6a562...: "[ ] long gate passed
   (gate CR-500 <name> (none in chantier.yaml ...))" and "[ ] verdict VERIFIED"; no long gate exists, none
   was run by me.
4. Run again by me: `just clip-kit-test`: tests 56, pass 56, fail 0. `just requirements-update`:
   "0 indexes updated", "0 requirement OKF projections updated", tree clean.
5. "The storyboard case and the new stage case fail on the previous clip". Scratch copy of the base
   7d35be3 `docs/demo-video` clip-kit/lib and clips (`git cat-file blob`, 83 files) with the head's
   storyboard.test.mjs; `node --test .../clip-kit/lib/storyboard.test.mjs`: exit 1, tests 40, pass 38,
   fail 2: "the shipped export-html clip.md reads as the clip the owner reviews" (assertion on Length 12 s)
   and "the stage of the export-html clip holds the page the clip claims" (ENOENT platform-report.md).
6. CI box. `gh pr checks 516`: checks, report, static, static-windows, viewer-graph, visual pass;
   gallery, tag-release, release, integration, pages, release-check, stress, toc-loop skipping. Run
   45752986397: head_sha c7c6a562, success.
7. Requirements and changelog boxes, Impacts, Blast radius. `git diff --stat 7d35be3 c7c6a56`: 26 files
   (storyboard.test.mjs, the export-html clip folder, one line of docs/user/toolbar.md); no src/, no
   requirements/, no CHANGELOG.
8. Changes list. `git ls-files docs/demo-video/clips/export-html`: 22 files, platform-report.md present,
   no release.png, no team-handbook.md; `git grep -n team-handbook`: empty (exit 1). `frames/` keeps
   01-selected.png and 02-pasted.png.
9. "From the merged clip". Base clip.md: 12.0 s, Dark by the Theme button, a "Release" tab click, two
   marks, two captions. Head: 18 s, Cream, three captions, three marks. toolbar.md keeps the forced-theme
   line and "Tabs and dropdowns work without JavaScript". The new alt text equals the specification's
   (03-change-spec.md line 326).
10. Stage and Summary. Head stage: 0 CR bytes; two card grids, a 16-column Service table, a small 3-column
    Week table, a flowchart and a sequenceDiagram, a vega-lite bar fence and a vega line fence; equal to
    the draft stage modulo CR (the draft has 116 CR).
11. Deliverables figures. `check.json`: passed true, length 18, MP4/WebM 1280x720 15 fps 18.000 s, GIF
    960 px 12 fps 3071217 B (2.93 MB), ladder step 0, 128 colours, loop 0, seam SSIM 0.990385, 20 check
    lines ok, editMode off, paste false, verifyPassed true, win32. ffprobe: h264 270 frames no audio, vp9
    270, GIF 216 frames. Captions, zoom, marks and times match story.json (12.0-13.2, 14.2-15.2,
    15.4-16.6).
12. Links. Raw GIF, MP4 and WebM at c7c6a56: HTTP 200, sha256 equal to the worktree files (gif
    58827e02a17d..., mp4 766df69c8440..., webm a2e8f72558e8...); clip.md blob URL 200.
13. "What the clip proves", Cream / Auto / 887 px / four drawings / no script, no hover box. Take notes:
    verify.json passed, themeMode cream, widthMode auto, Studio wide table 887.0009 px, browser 887.0049 px;
    exported HTML: 0 `<script`/`<link`, two Mermaid image drawings and two inline chart drawings (verify()
    in scenario.mjs). `git diff --stat 7f4f9820 c7c6a562`: only the test file, so the head's scenario is
    the one committed with the outputs. Decoded framemd5 of the take's render master equals that of the
    committed MP4; the take workspace Markdown equals the committed stage.
14. Look. Contact sheet, poster, first-last, key frames, GIF frame tiles and MP4 tiles opened: Cream, wide
    table breaks out in Studio and browser, Studio scrolls past the four drawings, small table and second
    grid, export, palette "Open Integrated Browser", localhost:5170, marks over the wide table, flowchart
    and bar chart, never over a wrong block. No username or home folder seen (save dialog shows
    C:\okfclip-500\...); `grep -a -i -c -E "gaeta|gaetan|Users[\\/]"` over the videos, PNGs, check.json,
    clip.md, scenario.mjs and stage: 0.
15. Known gaps, the others. Owner approval of 2026-11-25 (02-answers.md) predates the 2026-11-26 take.
    "Chart source": exportStyles.ts shows the closed details the preview hides (SwRS-...-DIAG-121,
    docs/user/charts.md), 2 in the exported HTML, partly behind the caption in 06-mark-3.png.
    browser-opened.png shows the palette. Sequence diagram, line chart and small table are in no key frame
    (at most a sliver at an edge). Windows only: check.json platform win32. Transient render:
    work/gates/r2-take1.log "No frame found at position 107968", r2-render1.log passes. Mark times:
    events.json marks at 11.80, 14.007, 15.405 against the committed 12.0, 14.2, 15.4.
16. Autonomous decisions. take.json notes: wheel for both scrolls, pointer parked at x 900 with the charts
    ending at 860, two inline charts and hover-box checks in scenario.mjs; own port 9500
    (DevToolsActivePort; default 9344) and scratch C:/okfclip-500; 887 px in the 720 px column box with a
    1160 px view; GIF step 0 2.93 MB; LF stage; release.png removed.
17. Description form. `gh api .../pulls/516 --jq .body` equals work/pr-body.md; body_html renders every
    section, the GIF and 6 checked boxes; template sections kept; title "docs: rework the export clip on a
    long report page"; base the CR-510 branch, draft, open; no change numbers or role names outside
    Internal references (CR-510 under CR-501 and CR-493 confirmed by `git log`, live charts in
    origin/main 17b779d5); no STALE; Human decisions match export-long-Q1 and Q3.

Not checked, and not claimed: motion, rhythm, scroll speed and the loop as watched; macOS and Linux.

NOT VERIFIED

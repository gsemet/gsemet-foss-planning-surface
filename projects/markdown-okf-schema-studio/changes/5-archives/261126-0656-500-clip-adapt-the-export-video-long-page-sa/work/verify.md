# Verify CR-500

Head: d6ae0d0458ecbadf97c9b17d05b8f6ae2182ddac

Replaces the NOT VERIFIED at c7c6a56 (claim F). The move c7c6a56..d6ae0d0 is one docs commit on the
same base (PR 516, draft, base chantier/batch-09/cr-510-..., base head 7d35be3). No take, render or app
window was run. No before/after captures (brief: no extension UI change; the visual is the committed
clip). Commands run in the CR worktree.

## Verdict

VERIFIED

## The move (judged at d6ae0d0)

- `git diff --name-only c7c6a562 d6ae0d04`: `docs/demo-video/clips/export-html/clip.md`,
  `.../export-html/scenario.mjs`. `git diff --stat c7c6a562 d6ae0d04 -- . ':(exclude)...clip.md'
  ':(exclude)...scenario.mjs'`: empty (no output file, test or other path).
- `git diff c7c6a562 d6ae0d04`: clip.md changes the section 3 "Time" and "Shot (filmed)" rows, the
  "Measured times of the take" note and the "Scrolling" note; scenario.mjs changes one comment only
  (3 `//` lines replace 2). `node --check .../scenario.mjs`: ok. `git diff --check`: ok.
- `git merge-base 7d35be3 d6ae0d04`: 7d35be3430689c4979a58f471d4cd588ecb93fac (base unchanged).

## F. Holds, at d6ae0d0: the browser's two scrolls (PR body, clip.md, scenario comment)

- `node -e` over `C:/okfclip-500/export-html/take/frames.json` (seconds from the first frame):
  `507@9.956 508@9.960 509@10.000 510@11.014 511@12.054 512@14.135`. Three frames after 11 s, of 512;
  the wheel is sent from 10.8 s (scenario.mjs `until(10.8)`), the second from 13.2 s (`until(13.2)`,
  unmark, `scrollBy`).
- Raw frames 509 to 512 tiled and looked at: top of the page; a position partway through the first
  scroll (table header entering at the bottom); the wide table; the flowchart and the bar chart.
- `ffmpeg ... export-html.mp4 -vf "select=between(n,150,262),crop=1280:480:0:100,tblend=all_mode=difference,signalstats,metadata=print..."`,
  YAVG above 0.5: `11.0 s 3.51`, `12.0 s 7.77`, `14.133 s 17.34`; the others are the zoom (10.33 to
  10.67 s, 17.13 to 17.47 s). With the threshold at 0.04 between 10.8 and 17 s, the rest is at most
  0.29 (marks animating). Same three jumps in the GIF (11.0, 12.0, 14.17 s: 3.54, 7.74, 17.23) and
  the WebM (11.0, 12.0, 14.133 s: 3.56, 7.80, 17.37).
- MP4 frames 164, 165, 179, 180, 211, 212 tiled and looked at: top; short step at 11.0 s, still there
  at 11.93 s; wide table at 12.0 s and still at 14.07 s; diagrams at 14.133 s.
- `verify.json` of the take: `"scrollStudio": "wheel"`, `"scrollBrowser": "wheel"`.
- So the PR body's Known gaps bullet ("a short step at about 11 s then a cut at about 12 s, the second
  as one cut at about 14.1 s", "only three new frames"), clip.md (rows and notes above; "11.01, 12.05
  and 14.13 s of the take") and the scenario comment match the take and the committed outputs.
  `grep` for cut/motion/new frame over the export-html folder: no remaining "one cut" for both
  scrolls and no "no new frame". Marks 1 and 2 animate in from 12.07 and 14.27 s, after their cut.

## Judged again at d6ae0d0

1. Head. `git rev-parse HEAD` and `git ls-remote origin` of the CR branch: both
   d6ae0d0458ecbadf97c9b17d05b8f6ae2182ddac; `git status --porcelain` empty (before and after my run).
   `gh pr view 516`: headRefOid d6ae0d04, base the CR-510 branch, draft, OPEN, title "docs: rework the
   export clip on a long report page".
2. Review box "approved at d6ae0d0". `$CHANTIER log CR-500`, 2026-11-26T04:55:09Z: "r5 approved at
   c7c6a562... (uncommitted wording diff over that head), committed as d6ae0d0458ecbadf97c9b17d05b8f6ae2182ddac".
3. Local gates. `work/gates/d6ae0d0-preflight.log` first line "CR-500
   chantier/batch-09/cr-500-clip-export-a-long-report-page-same-rend head
   d6ae0d0458ecbadf97c9b17d05b8f6ae2182ddac"; `== clip-kit-test exit 0` (56/56), `== check exit 0`
   (5306 tests, 5299 pass, 0 fail; 107/107; 212 passed), `== requirements-update exit 0` ("0 indexes
   updated", "0 requirement OKF projections updated"), `ci-static: passed`, `== preflight exit 0`
   (Windows static stage; other stages skipped), "git status after" empty, "head after d6ae0d04...".
   No long gate in chantier.yaml (`handoff CR-500`: "none in chantier.yaml"); none run by me.
4. Run by me: `just clip-kit-test`: tests 56, pass 56, fail 0 (it reads the changed clip.md); `git
   status --porcelain` empty after. Requirements box: the log of claim 3.
5. CI box. `gh pr checks 516`: checks, report, static, static-windows, viewer-graph, visual pass;
   gallery, tag-release, release, integration, pages, release-check, stress, toc-loop skipping. `gh api
   .../actions/runs/45763282708`: head_sha d6ae0d04..., completed, success, attempt 1.
6. Changelog, Requirements, Impacts, Blast radius. `git diff --stat 7d35be3 d6ae0d04`: 26 files
   (storyboard.test.mjs, the export-html clip folder, one line of docs/user/toolbar.md); `git diff
   --name-only ... -- src requirements CHANGELOG.md`: 0 files.
7. Links. Raw GIF, MP4, WebM at d6ae0d04: HTTP 200, sha256 equal to the worktree files (gif
   58827e02a17d..., mp4 766df69c8440..., webm a2e8f72558e8..., the same hashes as at c7c6a56, so the
   attached GIF's look carries); clip.md blob URL 200.
8. Description form. `gh api .../pulls/516 --jq .body` equals work/pr-body.md ("equal true", 7069
   chars). body_html renders the 11 sections, 1 image, 6 checkboxes; none unchecked. SHAs in the body:
   d6ae0d04... and c7c6a56 (named as "carried from", a parent of the head, reason given). No STALE, no
   UNVERIFIED. `userContentEdits`: against the body of 04:30:07Z (the one judged at c7c6a56), with the
   two head SHAs normalised, only lines 37 to 42 (Test plan) and 47 (the scrolls bullet) differ.
9. `grep -a -i -c -E "gaeta|gaetan|Users[\\/]"` over clip.md, scenario.mjs and pr-body.md: 0 each.

## Carried

The proof of each is the move's output above (two text files; `git diff --stat` of every other path
empty; base unchanged; body unchanged outside lines 37 to 42 and 47).

10. "The storyboard case and the new stage case fail on the previous clip". Carried from c7c6a56:
    storyboard.test.mjs and the base clip are unchanged. Then: that test file over a scratch copy of
    base 7d35be3, `node --test .../storyboard.test.mjs`: exit 1, 38 of 40 pass, the export-html clip.md
    case (Length 12 s) and the stage case (ENOENT platform-report.md) fail.
11. Changes list and stage and Summary. Carried from c7c6a56: no file added, removed or staged
    differently. Then: `git ls-files .../export-html` 22 files, no release.png, no team-handbook.md,
    `git grep -n team-handbook` empty; stage with two card grids, a 16-column and a small table, two
    Mermaid diagrams, a vega-lite and a vega fence, LF.
12. "From the merged clip" and the alt text. Carried from c7c6a56: the move leaves clip.md's length,
    theme, caption and mark rows, and toolbar.md, as they were. Then: base 12 s, Dark, tab click, two
    marks and captions; head 18 s, Cream, three and three; alt text equals the specification's.
13. Deliverables figures. Carried from c7c6a56: check.json and the outputs unchanged. Then: passed,
    18.000 s, 1280x720 15 fps, GIF 960 px 12 fps 3071217 B, step 0, 128 colours, captions, one zoom,
    three marks, loop.
14. "What the clip proves" (Cream, Auto, 887 px, four drawings, no script, no hover box). Carried from
    c7c6a56: outputs and the take unchanged, scenario.mjs changed in a comment only. Then: take
    verify.json passed, 887.0009 and 887.0049 px, no `<script`/`<link`, four drawings.
15. Look of the key frames and videos (no username or home folder, marks on the right blocks). Carried
    from c7c6a56: every image and video unchanged (claim 7 and the empty diff).
16. Known gaps, the others (owner approval of 2026-11-25 in 02-answers.md predates the 2026-11-26 take
    and no later one is there; "Chart source"; palette key frame; blocks in no key frame; motion not
    checked; Windows only; transient Remotion error, work/gates/r2-take1.log; mark times never taken).
    Carried from c7c6a56: bullets unchanged (claim 8), mark calls in scenario.mjs unchanged.
17. Autonomous decisions, Human decisions, Deviation and Internal references. Carried from c7c6a56:
    body text unchanged there (claim 8; only link SHAs moved), take and base unchanged.

Not checked, and not claimed: motion, rhythm, scroll speed and the loop as watched; macOS and Linux.

VERIFIED

---

## Description pass at d6ae0d0458ecbadf97c9b17d05b8f6ae2182ddac (posted body only)

The code claims above stand at the same head and were not redone. Verdict of this pass: VERIFIED.

D1. Head and state, at d6ae0d0. `git rev-parse HEAD`: d6ae0d0458ecbadf97c9b17d05b8f6ae2182ddac; `git status
    --porcelain`: empty. `gh pr view 516 --json title,body,isDraft,headRefOid,baseRefName,state`:
    head d6ae0d04..., base chantier/batch-09/cr-510-stack-ci-the-merge-commit-check-accepts-, isDraft
    true, OPEN, title "docs: rework the export clip on a long report page".
D2. Posted body equals work/pr-body.md, at d6ae0d0. `gh api .../pulls/516 --jq .body` saved to scratch,
    compared by `python -I`: 7073 and 7072 bytes, equal after trimming the trailing newlines and
    CRLF: True (7068 characters each); pr-body.md has no byte-order mark.
D3. Renders, at d6ae0d0. `gh api ... -H "Accept: application/vnd.github.full+json" --jq .body_html`: 11
    h2 sections (Summary, Deliverables, Deviation from the feature clip process, Changes, Impacts, Blast
    radius, Test plan, Known gaps, Autonomous decisions, Human decisions, Internal references, then the
    Claude Code line), one image, six task items all checked, lists and code spans rendered.
D4. Project PR rules (.github/PULL_REQUEST_TEMPLATE.md, pull-request.guidelines.md,
    feature-clip-process.guidelines.md section 6), judged at d6ae0d0. Template sections all present and
    filled; Deliverables right after Summary with the GIF; Impacts has "No visual change to the
    extension" with what changes instead (the documentation page's clip); one blast radius grade with
    its explanation; Autonomous decisions and Known gaps filled; Internal references last, before the
    Claude Code line; GIF inline and MP4, WebM, clip.md linked at d6ae0d0; the unchecked parts (motion,
    rhythm, loop) said. No `issue:` line in the CR's .md files (Grep: no match), no Fixes line.
D5. Internal references and marks, at d6ae0d0. `grep -n -i -E "gaeta|Users[\/]|CR-?[0-9]|batch|round|
    driver|inspector|verifier|coder|foreman|chief of staff|griller|STALE|UNVERIFIED|\.agents"` over the
    posted body: one match, line 77, the Internal references line.
D6. Changes against the diff, at d6ae0d0. `git diff --name-status 7d35be3 d6ae0d04`: storyboard.test.mjs
    M; export-html: check.json, clip.md, scenario.mjs, outputs and frames M or A, frames/release.png D,
    stage/platform-report.md A, stage/team-handbook.md D; docs/user/toolbar.md M. Nothing else.
D7. Review box. `$CHANTIER log 500`, 2026-11-26T04:55:09Z: "r5 approved at c7c6a562... (uncommitted
    wording diff over that head), committed as d6ae0d0458ecbadf97c9b17d05b8f6ae2182ddac".
D8. CI box. `gh pr checks 516`: checks, report, static, static-windows, viewer-graph, visual pass;
    gallery, integration, pages, release, release-check, stress, tag-release, toc-loop skipping.
D9. Proof SHAs: d6ae0d0 (the head), and c7c6a56 only as "carried from" with its reason. Claims of
    Summary, Deliverables, Changes and Impacts are proved by claims 6, 11, 13, 14 and F above. Known gaps
    holds the gaps of claims F and 16; no before-after.md (no extension UI change), no UNVERIFIED mark.
D10. Image, at d6ae0d0. The posted GIF link downloaded: HTTP 200, 3071217 B, sha256 58827e02a17d...,
    equal to the worktree file and to the committed LFS pointer's oid. Looked at every 6th frame (ffmpeg
    tiles, 36 frames): no username or home folder (the save box shows C:\okfclip-500\..., the browser
    localhost:5170, the window title "workspace"); three captions, three marks in turn on the wide
    table, the flowchart and the bar chart, as the body says.

VERIFIED

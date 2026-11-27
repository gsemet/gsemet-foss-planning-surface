# Verify CR-496 (okf-frontmatter clip)

Head: d386ff61a3d5a2cda0cb54130a5ffea5600a3793

Move judged: restack, `39d3eb31801f1679b444e52afa9951ca2ec3daef` (base da86d6e8) to d386ff61 (base
cae819b958dff6138d9b5dee1638a487234a5d79, CR-495's branch), with conflicts resolved in two clip kit
test files. Previous report: this file at 39d3eb31. Commands run in the CR's worktree, clean tree.

## The move (judged at d386ff61)

- `git range-diff da86d6e8..39d3eb31 cae819b9..d386ff61 --stat`: `b9adf4d2 = c83e4c8d`;
  `39d3eb31 ! d386ff61` (test commit, conflict resolutions).
- `git diff --stat cae819b9 d386ff61`: the same 20 files, 697 insertions, 2 deletions as
  `git diff --stat da86d6e8 39d3eb31`. The 2 deletions are the check test's title and the
  `existsSync` import line, so the base's tests are kept. `git log --merges cae819b9..d386ff61`:
  nothing; cae819b9 is an ancestor.
- `git diff --quiet 39d3eb31 d386ff61 -- docs/demo-video/clips/okf-frontmatter docs/user/okf.md`:
  exit 0; the clip tree is `e2f7baedc8634c2408445bd6aca12907f92a3` at both.
- The base brought `src/` changes (`git diff da86d6e8 cae819b9 --stat -- src`, 15 files: charts,
  Auto width of code blocks, export sheet). The read diffs of `previewStyles.ts`,
  `contentBlockStyles.ts`, `exportStyles.ts` and `widthMode.ts` touch charts and code blocks; the
  stage has neither, and no frontmatter file is listed. The take is carried.

## Claims

1. Tests, judged at d386ff61. `just check`: exit 0 (log
   `verifier/just-check-d386ff6.log`): clip kit `tests 47 / pass 47 / fail 0`, with the three
   okf-frontmatter storyboard tests and the scenario checks test; unit `tests 5302 / pass 5295 /
   fail 0 / skipped 7`, with `the shipped OKF page plays the frontmatter clip as video`; security
   107/107; release pytest `205 passed`; `1227 requirements, 0 errors, 26 warnings`; `0 files would
   change`; 94 use case diagrams parse; `check-limits: passed (1340 files, 0 on the size
   baseline)`. `git status` clean afterwards.
2. Requirements, judged at d386ff61. `just requirements-update`: exit 0, `0 indexes updated`,
   `0 requirement OKF projections updated`, `git status --porcelain` empty. The only added marker
   in `git diff cae819b9 d386ff61` is `// @tests_req SwRS-MDOKFSTUDIO-CORE-095`.
3. No behaviour change, no changelog line, judged at d386ff61. `git diff --name-only cae819b9
   d386ff61 -- src requirements CHANGELOG.md`: empty. The two commits are `docs:` and `test:`.
4. `check.json`, judged at d386ff61 (printed with node): `passed: true`, `verifyPassed: true`,
   `length: 11.5`, mp4 11.533 s, `loopSeamSsim: 0.995531`, `playbackRate: 1.005`, `rawFps: 3`,
   `platform: win32`, `extensionSource: vsix`, all 20 checks `ok: true`. The values come from the
   take at 39d3eb31's content (carried: clip folder unchanged; no new take).
5. Media, judged at d386ff61. `ffprobe`: mp4 h264 1280x720 15/1 11.533 s; webm vp9 1280x720 15/1
   11.534 s; gif 960x540 12/1 11.5 s. Sizes 331710, 234683, 1224198 equal check.json.
   `git lfs ls-files` lists 12 files of the 16 tracked.
6. Stage, scenario, storyboard and docs page match the specification: carried from 39d3eb31: the
   clip folder and `docs/user/okf.md` are unchanged. `git diff cae819b9 d386ff61 --
   docs/user/okf.md` still adds the one GIF image after the "Studio makes that metadata
   comfortable" paragraph, before "Linked-File Annotations".
7. No personal data. At d386ff61, `git grep -I -i -E "gaeta|C:[/\\]+Users" d386ff61 --` on the clip
   folder and `docs/user/okf.md`: no match (exit 1); same on `pr-body.md`: exit 1. Images looked at
   again (posted contact sheet, tiles of the downloaded GIF, `first-last.png`,
   `frames/editing.png`): window title "release-note.md - workspace - Visual Studio Code", the
   round "M" at top right is the clip's logo; no user name, home folder or path. The six PNGs of
   `evidence/` are byte-identical (`cmp`) to the head's frames; their other frames' looks are
   carried from 39d3eb31.
8. What the images show, judged at d386ff61: Names and Values table with five fields, "Status:
   draft"; text box on `draft` in the status cell with the "Add field / Remove field" menu;
   `published` typed; badge Ctrl Enter / Cmd Enter, row and body read `published`; zoom, mark on
   the status row then on the Status line. `first-last.png` shows the faint residue next to
   "draft"; `editing.png` shows the ripple and no text box yet (both in Known gaps).
9. "A real click ... `verify` compares the whole file", judged at d386ff61: `scenario.mjs` calls
   `t.click()` on the status value, requires a box holding `draft`, presses
   `ControlOrMeta+Enter`; `verify` throws unless `text === EXPECTED + "\n"`, where `EXPECTED` is
   the stage with the one `status` line replaced; check.json "scenario verify passed" ok.
10. Posted description, judged at d386ff61. `diff` of `gh pr view 517 --json body` against
    `work/pr-body.md`: one trailing blank line only. GIF, MP4, WebM raw URLs at d386ff61: HTTP 200,
    sha256 equal to the head's files; `clip.md` blob URL 200; the attached contact sheet
    (user-attachments) 200, 248100 bytes, sha256 `b0310d37...` equal to the head's
    `contact-sheet.png`. Summary, Deliverables, Changes and Impacts match the diff. The only
    other SHA is the "carried from `39d3eb3`" reason; no STALE or UNVERIFIED mark; `CR-496` and
    `batch-09` appear only in "Internal references" (line 71); no chantier role as doer.
11. Autonomous decisions, judged at d386ff61: `readingMode`, Ctrl+A, mark 1 backticks, the menu
    kept, and the event times (1.01, 4.61, 6.22, 7.01-8.71, 8.71-10.41, 10.51, 11.51 s) match
    `scenario.mjs`, `clip.md` review notes, check.json and `coder/r1.md`; port and scratch folder
    match the take note in `$CHANTIER log` and `coder/r1.md`; no kit code in the diff (kit tests
    only).
12. Deviation, approval and twin, judged at d386ff61: the recipe's storyboard-before-take order
    and its render/retake rule are in `feature-clip-process.guidelines.md`; `02-answers.md`
    okf-fm-Q3 records the review moved into the PR, and its "Owner approval (2026-11-25)" line
    approves storyboard and clip. Twin `okf-schema-bundle-frontmatter` exists on PR #521
    (b7518fb3, draft). Its stage differs from this one by `type: note` and a starting
    `status: publshed` instead of `draft` (`diff`), plus its `_schema/` folder; its storyboard
    calls itself "the same page". Observation, not a failure: "the same page" in this PR and "the
    same gesture" in `clip.md` are loose, the twin starts on a typo and picks from a select.
13. Review box, judged at d386ff61: `$CHANTIER log CR-496` has the driver's note
    `move 39d3eb3..d386ff6 (restack) inspector approved at d386ff6`.
14. CI at d386ff61 (`gh api .../commits/d386ff61.../check-runs`): static, static-windows, visual,
    viewer-graph, report, checks: success; integration, stress, release-check, toc-loop, gallery,
    release, pages, tag-release: skipped. PR #517: open, draft, head d386ff61, base CR-495's
    branch, `mergeStateStatus: CLEAN`.
15. Known gaps: the five bullets match claims 4, 8 and the platform in check.json; "Saving
    frontmatter" absent is as in `clip.md` and `coder/r1.md` (key frames looked at; not every video
    frame). Motion and loop as watched are stated in "What the clip proves".

## Gates

No long gate is configured (`ship`'s "no long gate passed" line is expected); none was run.

## Not checked

Motion, rhythm and the loop as watched; no new take; `just ci-static` and `just preflight` not run
here (CI static and static-windows pass at the head).

## Evidence

`verifier/evidence/before-after.md` (base cae819b9, head d386ff61); the six PNGs in the CR's
`evidence/`, identical to the head's frames.

VERIFIED

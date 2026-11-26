# Verify CR-492

Head: 1d55649b51bee924e24186700634cef03413272f

Judgment after a restack with conflict resolution: 4a47151e..211f3a59 moved to 8c6845a5..1d55649b
(base: `chantier/batch-09/cr-493-clip-the-advanced-renderings-tour-and-cl`). Previous judgment:
VERIFIED at 211f3a59. `git range-diff 4a47151e..211f3a59 8c6845a5..1d55649b`: commit 1 identical
(`4acc01c1 = fd5cbb9f`); commit 2 changed (`!`) in the title and body of the checks test of
`check.test.mjs` and in the context of `siteClips.test.ts`. The base brought kit changes
(`check.mjs`, `storyboard.mjs` MAX_LENGTH 12 to 30), `docs/user/editing.md`,
`siteClips.test.ts`, requirements and chart / width-mode sources.

## Code, tests, clip (judged at 1d55649b by the earlier pass at this head; head unmoved)

- Diff scope: `git diff --name-only 8c6845a5...1d55649b` lists 19 files: the radio-buttons clip folder, `docs/user/editing.md`, `check.test.mjs`, `storyboard.test.mjs`, `test/site/siteClips.test.ts`. No `src/`, `skills/`, `requirements/`, README or CHANGELOG file. `git log --merges 8c6845a5..HEAD`: empty. Tree clean. `git ls-remote`: the pushed branch is 1d55649b. PASS.
- Conflict resolution: `git diff 8c6845a5 1d55649b -- check.test.mjs siteClips.test.ts` shows only additions beside the base's (title names "renderings tour and radio"; radio import and `{ editMode: "off", paste: false }` after the tour's; the radio site test, marker `SwRS-MDOKFSTUDIO-CORE-095`, after the tour test). PASS.
- Clip kit tests: `just clip-kit-test`: tests 40, pass 40, fail 0, including "the shipped scenarios declare their checks: ... renderings tour and radio clips ...", "the shipped radio-buttons clip.md reads as the clip the owner reviews", "the stage of the radio-buttons clip differs from the expected text by the moved x only". PASS.
- Docs-page test: `npm run compile`, then `node scripts/node-test.mjs unit out/test/site/siteClips.test.js`: tests 16, pass 16, fail 0, including "the shipped editing page plays the radio clip as video" and the base's "... renderings tour clip as video". PASS.
- Docs page: `git diff 8c6845a5 1d55649b -- docs/user/editing.md`: one added image (the radio GIF, spec alt text) right after "GitHub and in plain editors the `( )` and `(x)` text stays readable."; the base's tour GIF stays. PASS.
- Clip check with the new kit: a probe ran the head's `checkClip` on a copy of the shipped clip folder (so the tracked `check.json` is not rewritten), take and render read from `C:/okfclip492/radio-buttons`: "passed true; 20 checks; failed 0"; MP4 and WebM 1280x720 15 fps, MP4 10.533 s vs Length 10.5, GIF 960 px 12 fps loop 0, SSIM 0.99529, reading mode off, rate 1.003, verify passed. Values length, mp4, webm, gif, loopSeamSsim, take and host equal the committed `check.json`. Only difference: the committed line is named "mp4 duration within 5 to 12 s", the head's kit names it "5 to 30 s" (same value, both ok). The probe was removed afterwards. PASS.
- Requirements: `just requirements-update` ends "0 indexes updated / 0 requirement OKF projections updated"; `git status --short` empty. PASS.
- Fast check: `just check` at 1d55649b: exit 0 (`work/gates/verifier-check-1d55649.log`): clip kit 40/40; unit 5299 tests, 5291 pass, 0 fail, 8 skipped; security 107/107; release pytest 205 passed; boundaries, limits, settings, diagrams passed. Tree clean. PASS.
- LFS: `git lfs ls-files -s -I "docs/demo-video/clips/radio-buttons/**"`: the 11 renders, frames and sheets, each `*` (content present). PASS.
- Username / home path in the clip text files: `git grep -I -i -c -e gaeta -e "C:\\Users" HEAD -- docs/demo-video/clips/radio-buttons`: no match (exit 1). PASS.

## Carried

- carried from 211f3a59: frames show the radio choice (reading mode left, raw text right, selection and `(x)` moved, no focus ring, marks, captions, no username). Reason: `git diff 211f3a59 1d55649b -- docs/demo-video/clips/radio-buttons` is empty.
- carried from 211f3a59: the take proves a real click selects the option and moves the `x` on two lines (`run` checks and `verify`). Reason: clip folder, `radioMarkers.ts`, `radioGroups.ts` and `checkboxes.ts` have an empty diff between the two heads; the base's source changes are charts, code-block width, find index and export snapshot, and the stage holds none of those elements. The take was not refilmed.
- carried from 211f3a59: the first run on the shared scratch folder showed another clip's pictures and was rerun with its own `CLIP_SCRATCH` (history, untouched by the move).

## Description pass (third, description only; replaces the failed one of 00:43Z)

Head: 1d55649b51bee924e24186700634cef03413272f

Body as posted: `gh pr view 513 --json body,headRefOid,updatedAt,isDraft,baseRefName,title`:
head is the SHA above, last updated 2026-11-26T00:43:17Z (re-read at the end of the pass,
unchanged), draft, base is the CR-493 branch (`baseRefOid` 8c6845a5, `mergeStateStatus` CLEAN),
title "docs: add the radio choice feature clip". `diff` with `work/pr-body.md`: one trailing blank
line only. The whole body was judged.

- PASS, renders: `gh api repos/gsemet/markdown-okf-schema-studio/pulls/513 -H "Accept: application/vnd.github.full+json" --jq .body_html`: nine `h2` sections, three lists (one of six checked task items), the GIF as an `img` with `data-animated-image`, the four links.
- PASS, form: the project template's sections are all present in its order (Summary, Deliverables, Changes, Impacts, Blast radius, Test plan), with the added Deviation, What the clip proves and Autonomous decisions; the stack guideline asks nothing of the body.
- PASS, no internal reference, old SHA or username: `gh pr view 513 --json body --jq .body | grep -n -i -E "CR-[0-9]|batch|round|driver|verifier|inspector|coder|foreman|griller|spec|chief of staff|\.agents/|STALE|UNVERIFIED|211f3a|4a47151|gaeta|C:.Users|03-zoomed"`: no output (exit 1). `... | grep -o -E "[0-9a-f]{7,40}" | sort | uniq -c`: only `1d55649` (3) and the full head (5).
- PASS, links: `curl -sL` at `.../1d55649b.../radio-buttons/`: gif 200 image/gif 1265741 bytes, mp4 200 369217, webm 200 256389, clip.md 200. Served GIF sha256 `80ccaa74...cd` equals the head's LFS object (`git lfs ls-files -l`).
- PASS, the attached image's look: the committed GIF (the served object) sampled every 21st frame into one tile and opened: title "plan.md - workspace", reading mode left, raw text right, first option then second selected, marks on `(x)` then `( )`, both captions; no username, home folder or local path.
- PASS, Summary, Deliverables, Changes against the diff: `git diff --stat 8c6845a5...HEAD`: 19 files (clip folder, `docs/user/editing.md`, `check.test.mjs`, `storyboard.test.mjs`, `siteClips.test.ts`), no `src/` file. `check.json`: win32, extension source `vsix`, 1280x720, 15 fps, length 10.5, GIF loop count 0. "Two characters on two lines": the stage test (40/40 above) and its diff (`changed` is `[7, 8]`).
- PASS, "selects it at once" (What the clip proves): `npm run compile`, `node scripts/node-test.mjs unit out/test/page/runtimeRadioGroups.test.js` at 1d55649b: "clicking an unselected radio option selects it at once and asks the host to move the x" ok; tests 12, pass 12, fail 0. In the committed MP4, frame 22 (about 1.47 s, click at 1.33 s), extracted with `ffmpeg` and opened, already shows the second option clicked and `(x)` on line 8. "Moves the `x`": `scenario.mjs` lines 193 to 211 and `verify`, `check.json` `verifyPassed: true`. Tree clean after.
- PASS, Deviation: the take from the draft (spec, radio-Q3); "then approved": `02-answers.md`, owner approval of 2026-11-25 evening, clip folder unchanged since.
- PASS, Autonomous decisions, the failed point on frames: `git grep -n -e "Measured by" -e "Key frames" -e "focus" -e "03-zoomed" HEAD -- .../clip.md`: the focus ring note (line 92), measured times (line 100), key frames (lines 101 to 103) naming `pointed`, `chosen`, `04-mark-1`, `05-mark-2`; `03-zoomed` is no longer claimed.
- PASS, Autonomous decisions, the failed point on backticks: the body now has "The Mark 1 and Mark 2 rows of the storyboard write `(x)` and `( )` without the backticks of the draft"; `git diff --no-index work/storyboard/clip.md docs/demo-video/clips/radio-buttons/clip.md` shows exactly that on the two mark rows; the other differences are the adaptations the specification's section 2 prescribes. `work/coder/r1.md` records no other decision; `conflict-resolver/conflicts.md` keeps both sides only.
- PASS, Autonomous decisions, scratch folder: `work/gates/clip-all.log` (default scratch under the temporary folder): MP4 12.000 s against Length 10.5, loop SSIM 0.71740, failed; `clip-all2.log` (`C:\okfclip492`): passed, SSIM 0.99529; `lib/profile.mjs:26` puts `remotion` under the one scratch root (`lib/platform.mjs:24`); the diff changes no kit code (only two kit test files). What the failed render showed is carried (above).
- PASS, Impacts: one line, no change to the extension and what the reader gets (the clip in the user guide); not the template's comment. Read as the guideline's "no visual change" line with its reason; the visual is the GIF in Deliverables.
- PASS, Blast radius: one grade (1) with its reason; the diff is docs, a clip folder and tests.
- PASS, Test plan: `gh pr checks 513` and `statusCheckRollup` at 1d55649b: static, static-windows, visual, viewer-graph, report, checks SUCCESS; integration, stress, toc-loop, release-check, release, pages, gallery, tag-release skipped. "40 tests", `just check`, unchanged tree after `just requirements-update`: claims above at 1d55649b. "One added `@tests_req`": `git diff 8c6845a5...HEAD | grep -c "^+.*@tests_req"`: 1. "No user-facing change": no `CHANGELOG.md` in the diff. The New tests, Requirements and Changelog items carry no SHA, as the project template writes them.
- PASS, Review box: `$CHANTIER log CR-492`: `2026-11-26T00:40:13Z driver note note=move 211f3a5..1d55649 (restack) inspector approved at 1d55649`.
- PASS, Known gaps: the project template has no such section; no UNVERIFIED claim, no evidence pair declared uncaptured, no failed claim accepted. The notes' limits are stated in the body (judged by watching; filmed on Windows).

## Before / after

No new pair: the previous judgment captured none, the CR changes no extension screen, and the move touched no capture.

## Verdict

Every code, test and clip claim passes at 1d55649b, and the posted description (updated
00:43:17Z) passes as a whole, the two points failed before included.

VERIFIED

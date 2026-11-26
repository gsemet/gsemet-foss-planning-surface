# Verify CR-492

Head: 1d55649b51bee924e24186700634cef03413272f

Judgment after a restack with conflict resolution: 4a47151e..211f3a59 moved to 8c6845a5..1d55649b
(base: `chantier/batch-09/cr-493-clip-the-advanced-renderings-tour-and-cl`). Previous judgment:
VERIFIED at 211f3a59. `git range-diff 4a47151e..211f3a59 8c6845a5..1d55649b`: commit 1 identical
(`4acc01c1 = fd5cbb9f`); commit 2 changed (`!`) in the title and body of the checks test of
`check.test.mjs` and in the context of `siteClips.test.ts`. The base brought kit changes
(`check.mjs`, `storyboard.mjs` MAX_LENGTH 12 to 30), `docs/user/editing.md`,
`siteClips.test.ts`, requirements and chart / width-mode sources.

## Judged again at 1d55649b (code, tests, clip)

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

## Description pass (second, replaces the failed one of 00:38Z)

Head: 1d55649b51bee924e24186700634cef03413272f

Body read with `gh pr view 513 --json body,headRefOid,updatedAt,isDraft,baseRefName`: head is the
SHA above, last updated 2026-11-26T00:40:38Z, draft, base is the CR-493 branch. Re-read at
00:42:32Z, unchanged. It equals `work/pr-body.md` but for one trailing blank line (`diff`).

- PASS, renders: `gh api repos/gsemet/markdown-okf-schema-studio/pulls/513 -H "Accept: application/vnd.github.full+json" --jq .body_html`: eight `h2` sections, lists, six checked task items, the GIF as an `img` with `data-animated-image`, the three links.
- PASS, links name the head: `curl -sL` at `.../1d55649b.../radio-buttons/`: gif 200 image/gif 1265741 bytes, mp4 200 369217, webm 200 256389, clip.md 200. The served GIF's sha256 is `80ccaa74...2bc605`, equal to the LFS object of the head (`git lfs ls-files -l`). No `211f3a5` link is left (rendered body).
- PASS, the attached image's look: the served GIF (126 frames, 960x540) sampled every 21st frame into one tile and opened: title "plan.md - workspace", reading mode left, raw text right, first option then second selected, marks on `(x)` then `( )`, both captions; no username or home folder.
- PASS, Summary, Deliverables, Changes, Impacts: `git diff --stat 8c6845a5...HEAD`: 19 files, the clip folder, `docs/user/editing.md`, three test files, no `src/` file; 2 commits `fd5cbb9f`, `1d55649b`.
- PASS, Test plan: `gh pr checks 513` and `statusCheckRollup` at head 1d55649b: static, static-windows, visual, viewer-graph, report, checks SUCCESS; integration, stress, toc-loop, release-check, release, pages, gallery, tag-release skipped. "40 tests", `just check` and the unchanged tree after `just requirements-update`: the claims above, at 1d55649b.
- PASS, Review box: `$CHANTIER log CR-492`: `2026-11-26T00:40:13Z driver note note=move 211f3a5..1d55649 (restack) inspector approved at 1d55649`.
- PASS, "The storyboard and the clip were then approved": `02-answers.md`, owner approval of 2026-11-25 evening ("the storyboard and the clip of this PR are approved"), also order O-93 in the log; the clip folder is unchanged since (carried above).
- Known gaps: the project template has no such section; no UNVERIFIED claim, no evidence pair declared uncaptured, no failed claim accepted.
- FAIL, Autonomous decisions, a false statement: the body says the key frames "`pointed`, `chosen`, `03-zoomed`, `04-mark-1`, `05-mark-2`" are in the Review notes of `clip.md`. `git grep -n -e "03-zoomed" HEAD -- docs/demo-video/clips/radio-buttons`: no output. `git grep -n -e "frames/" HEAD -- .../clip.md`: the Review notes (lines 93 to 103) name `pointed`, `chosen`, `04-mark-1`, `05-mark-2` only. The file `frames/03-zoomed.png` exists (LFS list) but the notes do not name it.
- FAIL, Autonomous decisions, a decision left out: `git diff --no-index work/storyboard/clip.md <head>/docs/demo-video/clips/radio-buttons/clip.md` shows the backticks of the Mark 1 and Mark 2 rows dropped (`` new `(x)` `` to `new (x)`, `` now `( )` `` to `now ( )`). The specification, section 2, says that when they are dropped "Autonomous decisions" says so (section 7: the section holds the differences from the draft); `work/coder/r1.md` records it under "Autonomous decisions". `gh pr view 513 --json body --jq .body | grep -n -i -e backtick -e "mark row" -e draft`: only the Deviation line (21), nothing on the mark rows. The project's PR guideline also asks that a decision taken without the user be listed there.

Fix (body only, same head): drop `03-zoomed` from that sentence (or say it is in `frames/`), and
add a bullet saying the mark rows of `clip.md` drop the draft's backticks around `(x)` and `( )`.

## Before / after

No new pair: the previous judgment captured none, the CR changes no extension screen, and the move touched no capture.

## Verdict

Every code, test and clip claim passes at 1d55649b. The posted description fixes the stale SHA
links and the Test plan numbers, but its Autonomous decisions section names a key frame in notes
that do not name it and leaves out a decision the specification requires there.

NOT VERIFIED

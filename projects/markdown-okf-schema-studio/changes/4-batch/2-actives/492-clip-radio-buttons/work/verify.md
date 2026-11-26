# Verify CR-492

Head: 1d55649b51bee924e24186700634cef03413272f

Judgment after a restack with conflict resolution: 4a47151e..211f3a59 moved to 8c6845a5..1d55649b
(base: `chantier/batch-09/cr-493-clip-the-advanced-renderings-tour-and-cl`). Previous judgment:
VERIFIED at 211f3a59. `git range-diff 4a47151e..211f3a59 8c6845a5..1d55649b`: commit 1 identical
(`4acc01c1 = fd5cbb9f`); commit 2 changed (`!`) in the title and body of the checks test of
`check.test.mjs` and in the context of `siteClips.test.ts`. The base brought kit changes
(`check.mjs`, `storyboard.mjs` MAX_LENGTH 12 to 30), `docs/user/editing.md`,
`siteClips.test.ts`, requirements and chart / width-mode sources.

## Judged again at 1d55649b

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

## Description pass

Head: 1d55649b51bee924e24186700634cef03413272f

`gh pr view 513 --json body,headRefOid,updatedAt,statusCheckRollup`, read at 2026-11-26T00:38:19Z
(headRefOid is the head above, body last updated 00:28:02Z; draft, base is the CR-493 branch).

- FAIL, proofs name a SHA that is not the head: 6 occurrences of `211f3a5...`, 0 of `1d55649...`. The GIF, MP4, WebM and both `clip.md` links point at 211f3a59, which the restack removed from the branch; no "carried from" reason is given, and a restack with conflicts is not a clean rebase. The files are the same (`curl -sL`: 200 and equal sizes at both SHAs for gif 1265741, mp4 369217, webm 256389, clip.md 6056; empty diff of the clip folder), so moving the links to 1d55649b is enough.
- FAIL, Test plan: "`just clip-kit-test` (37 tests)": at the head it runs 40 tests. "CI green at 211f3a5 (static, static-windows, visual, viewer-graph, report)": names the old head. At 1d55649b: static, static-windows, visual, viewer-graph SUCCESS, report IN_PROGRESS at the read above.
- To update in the same edit (not counted as failed): "stays a draft until the storyboard and the clip are approved" and "Still to judge by watching" predate the owner's approval recorded on 2026-11-25 (`chantier log CR-492`, order O-93).
- PASS: Summary, Deliverables and Changes match the 19-file diff at the head; Impacts ("No change to the extension") holds, no `src/` file in the diff; `just check` and "`just requirements-update` leaves the tree unchanged" are true at the head (above); Review box unchecked; no Known gaps needed (no UNVERIFIED claim, no evidence pair declared uncaptured).
- Attached image: the same GIF blob as judged at 211f3a59 (carried: empty diff of the clip folder).

## Before / after

No new pair: the previous judgment captured none, the CR changes no extension screen, and the move touched no capture.

## Verdict

Every code, test and clip claim passes at 1d55649b. The posted description fails (stale SHA and test
count). A description-only pass is enough after the body is updated.

NOT VERIFIED

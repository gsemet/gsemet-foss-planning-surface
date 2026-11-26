# Verify CR-495

Head: cae819b958dff6138d9b5dee1638a487234a5d79

Restack move d930238cc64eee77fe5dc0ad25c574a7231b7f5a to cae819b958dff6138d9b5dee1638a487234a5d79, onto base c3c3a57ed16874bf56f5834ef6d789443e842fbb (CR-494 branch). No clip was retaken. A claim marked `carried from d930238` keeps the earlier judgment for the stated reason; the others are judged at cae819b.

## 1. The move. PASS (cae819b)

- `git rev-parse HEAD`, `git ls-remote` of the branch and `gh pr view 515 --json headRefOid` give cae819b; PR 515 is draft, MERGEABLE, base = the CR-494 branch at c3c3a57.
- `git merge-base --is-ancestor c3c3a57 HEAD`: yes. `just check-no-merge-commits origin/main`: "passed (10 commits since origin/main, no merge commit)".
- `git diff --stat c3c3a57 HEAD`: 24 files, 822 insertions, 1 deletion; commits 5dfa76e (docs), cae819b (test); no change in `src/`, `requirements/`, `CHANGELOG.md`, `package.json`; no non-test clip-kit change; `git diff --check c3c3a57 HEAD` clean.
- `git range-diff 4a47151..d930238 c3c3a57..HEAD`: only context and conflict resolutions and the check test title, as `work/conflict-resolver/conflicts.md` describes; no conflict marker in `docs/demo-video/clip-kit/lib`.
- `git diff d930238 HEAD -- docs/demo-video/clips/figure-editor`: empty.
- Base `src/` changes (charts, Auto width) touch none of figurePanel, editorChrome, figureDirective, directives/figure, figureSizes.

## 2. Committed clip files. PASS (carried from d930238: clip folder diff empty)

`git lfs ls-files cae819b -I "docs/demo-video/clips/figure-editor/*"`: mp4, webm, gif, poster, contact-sheet, first-last and 9 frames are LFS objects; check.json, scenario.mjs, clip.md and stage are in the tree.

## 3. check.json and media. PASS (carried from d930238: clip folder diff empty; ffprobe rerun at cae819b)

- check.json: passed true, 20 of 20 checks ok, "scenario verify passed" true, length 12, MP4 and WebM 1280x720 15 fps 12 s, GIF 960 px 12 fps loop 0, loopSeamSsim 0.990696, playbackRate 0.995, win32.
- `ffprobe`: mp4 h264 1280x720 15/1 12.000000; webm vp9 1280x720 15/1 12.000000; gif 960x540 12/1 12.000000.
- Shipped take scratch `C:/okfclip495/figure-editor` (take.json: 110 frames, 11.946 s, as check.json): verify.json passed true, alignBy "r", save press at 8.652 s, DevToolsActivePort 9495.

## 4. Gates. PASS (cae819b)

`just check`, exit 0, log `work/gates/verifier-check-cae819b.log`: boundaries passed (406 modules); file limits passed (1340 files, 0 baseline); settings passed; clip kit 44 of 44 (includes the figure-editor storyboard, stage and scenario check cases and the kept table and radio cases); unit 5301 tests, 5294 pass, 0 fail, 7 skipped; security 107 of 107; release pytest 205 passed; requirements 0 errors, 26 warnings; "0 indexes would change", "0 requirement OKF projections would change", "0 files would change". Tree clean after. `just preflight` was not run and the description does not claim it.

## 5. Site test. PASS (cae819b)

`npm run compile`, then `node scripts/node-test.mjs site out/test/site/siteClips.test.js`: 18 tests, 18 pass, 0 fail, includes "the shipped editing page plays the figure editor clip as video" and the base's table and paste clip tests.

## 6. Stage, expected text, docs line. PASS (cae819b)

The kit cases comparing `stage/harbour-guide.md`, `EXPECTED` and the clip.md block pass (claim 4). `docs/user/editing.md` carries the GIF line with the specification's alt text; pair in `work/verifier/evidence/before-after.md`.

## 7. Pictures. FAIL for `frames/03-zoomed.png`

- PASS (carried from d930238: clip unchanged): contact-sheet, rendered, 04-mark-1. Looked at again with sampled GIF frames and form.png: form flow, three new lines outlined, keycaps Ctrl+Enter / ⌘Enter, figure floating right; title bar "workspace", no username or path. Not checked: motion, rhythm, the loop as watched.
- FAIL (cae819b; this frame was not looked at at d930238): `sha256sum frames/03-zoomed.png frames/rendered.png` gives 931dda9a645ec44e... for both. The frame shows the rendered figure after the save, not the directive. `clip.md` line 51 calls it "Zoom on the text box and the paragraph under it after Apply", and Evidence 4 of `03-change-spec.md` expects `03-zoomed` to show the directive with the three new lines. Cause: `clip-kit/lib/encode.mjs` takes 03-zoomed at the zoom midpoint (about 8.9 s), after the 8.6 s save. The directive is shown by 04-mark-1 only.

## 8. PR description (cae819b)

`gh pr view 515 --json body` equals `work/pr-body.md` but for one trailing newline (rechecked, last update 2026-11-26T01:34:06Z).

PASS:
- Layout: project template as written; renders (headings, animated GIF, checked boxes); internal references only in the last section; no agent role as doer; attribution line last.
- Links at cae819b: GIF 200 (1806032 bytes, sha256 equals the LFS oid), MP4 200 (653958), WebM 200 (457577), clip.md 200. The feature clip guideline requires these head-SHA links.
- Summary, Deliverables, Changes, Impacts, Blast radius: match the diff, the scenario and the pictures.
- Test plan: tests and local gates (claims 4, 5); requirements (check run: nothing would change; one added `@tests_req` on SwRS-MDOKFSTUDIO-CORE-095); changelog (commits are docs and test only); check.json figures (claim 3).
- Review box: Driver note in `chantier log CR-495`, 2026-11-26T00:51:43Z, "move d930238..cae819b (restack) inspector approved at cae819b".
- CI box: run 45728437962 at cae819b: static, static-windows, viewer-graph, visual, report, checks success on attempt 2; attempt 1 visual cancelled with "exceeded the maximum execution time of 15m0s"; integration and stress skipped.
- What the clip proves, Deviation (storyboard after take and owner approval in `02-answers.md`), other Autonomous decisions (scenario.mjs, clip.md, take notes), Known gaps (form.png; check.json platform win32).

FAIL:
- Evidence box: "the take passed after one first render that failed with a Remotion "No frame found" error and was run again". No gate log, evidence or take folder shows this failure or rerun (`work/gates/all.log` holds one `all` run with no such error; the shipped take folder holds the last take only). The only source is `work/coder/r2.md`. The sentence is new in this description. Remove it, narrow it, or mark it `**UNVERIFIED:**` with a Known gaps bullet.
- Autonomous decisions: "The clip was filmed two more times for the scroll fix." The logs show an `all` run (11:01) before the shipped take (11:18), but neither the count of two nor the reason; the only source is `work/coder/r2.md`. Same remedy.

Observations, not failing: the Autonomous decisions list omits three items of specification section 7 (GIF place and alt text, site test, stage tests), which Changes covers; `work/gates/all.log` shows an earlier run on the default scratch folder, while the shipped take ran on its own folder and port. "No long gate passed" from ship is expected (no long gate is configured).

## 9. Failures to settle

1. `frames/03-zoomed.png` does not show what clip.md and the specification say: fix the alt text and storyboard in a round, or accept it with a Known gaps bullet.
2. Unproven "No frame found" rerun sentence in the Evidence box.
3. Unproven "two more times" sentence in Autonomous decisions.

NOT VERIFIED

# Verify CR-495

Head: cae819b958dff6138d9b5dee1638a487234a5d79

Description pass on the restack move d930238cc64eee77fe5dc0ad25c574a7231b7f5a to cae819b958dff6138d9b5dee1638a487234a5d79, onto base c3c3a57ed16874bf56f5834ef6d789443e842fbb (CR-494 branch). The branch has not moved since the previous `verify.md` (Head cae819b, NOT VERIFIED); only the PR description was edited. Claims marked `carried (previous verify.md, cae819b)` keep that report's judgment and proof: same head, same base, and the edit does not touch them. Claims marked `carried from d930238` keep the older judgment it cited, for the reason given. The others are judged again here at cae819b.

## 1. Head, base and the edit. PASS (cae819b)

- `git rev-parse HEAD`, `git ls-remote` of the branch and `gh pr view 515 --json headRefOid` give cae819b958dff6138d9b5dee1638a487234a5d79; `git status --short` empty; PR 515 draft, MERGEABLE, base = the CR-494 branch; `git ls-remote` of that branch gives c3c3a57ed16874bf56f5834ef6d789443e842fbb.
- Posted body (`gh pr view 515 --json body`, last edit 2026-11-26T01:54:04Z) equals `work/pr-body.md` exactly (5908 characters, compared in Python: True).
- `git diff --no-index --word-diff` of the previous posted body (forge edit history, 01:34:06Z) against the posted one shows four edits and nothing else: the "No frame found" clause removed from the Evidence line; "The clip was filmed two more times for the scroll fix." removed; one Autonomous decisions bullet added (GIF place); one Known gaps bullet added (03-zoomed).

## 2. The move. PASS (carried, previous verify.md, cae819b)

- `git merge-base --is-ancestor c3c3a57 HEAD`: yes. `just check-no-merge-commits origin/main`: "passed (10 commits since origin/main, no merge commit)".
- `git diff --stat c3c3a57 HEAD`: 24 files, 822 insertions, 1 deletion; commits 5dfa76e (docs), cae819b (test); no change in `src/`, `requirements/`, `CHANGELOG.md`, `package.json`; no non-test clip-kit change; `git diff --check c3c3a57 HEAD` clean.
- `git range-diff 4a47151..d930238 c3c3a57..HEAD`: only context and conflict resolutions and the check test title, as `work/conflict-resolver/conflicts.md` describes; no conflict marker in `docs/demo-video/clip-kit/lib`.
- `git diff d930238 HEAD -- docs/demo-video/clips/figure-editor`: empty.
- Base `src/` changes (charts, Auto width) touch none of figurePanel, editorChrome, figureDirective, directives/figure, figureSizes.

## 3. Committed clip files. PASS (carried from d930238 through the previous verify.md: clip folder diff empty)

`git lfs ls-files cae819b -I "docs/demo-video/clips/figure-editor/*"`: mp4, webm, gif, poster, contact-sheet, first-last and 9 frames are LFS objects; check.json, scenario.mjs, clip.md and stage are in the tree.

## 4. check.json and media. PASS (carried from d930238 through the previous verify.md; check.json read again at cae819b)

- check.json: passed true, every check ok (previous report: 20 of 20), "scenario verify passed" true, length 12, MP4 and WebM 1280x720 15 fps 12 s, GIF 960 px 12 fps loop 0, loopSeamSsim 0.990696, playbackRate 0.995, platform win32.
- `ffprobe` (previous report, at cae819b): mp4 h264 1280x720 15/1 12.000000; webm vp9 1280x720 15/1 12.000000; gif 960x540 12/1 12.000000.
- Shipped take (previous report: take.json 110 frames, 11.946 s; verify.json passed true, alignBy "r", save press at 8.652 s, DevToolsActivePort 9495), under `C:/okfclip495/figure-editor`.

## 5. Gates. PASS (carried, previous verify.md, cae819b)

`just check`, exit 0, log `work/gates/verifier-check-cae819b.log`: boundaries passed (406 modules); file limits passed (1340 files, 0 baseline); settings passed; clip kit 44 of 44 (includes the figure-editor storyboard, stage and scenario check cases and the kept table and radio cases); unit 5301 tests, 5294 pass, 0 fail, 7 skipped; security 107 of 107; release pytest 205 passed; requirements 0 errors, 26 warnings; "0 indexes would change", "0 requirement OKF projections would change", "0 files would change". Tree clean after. `just preflight` was not run at this head and the description does not claim it. The "no long gate passed" line of `ship` is expected (no long gate is configured).

## 6. Site test. PASS (carried, previous verify.md, cae819b)

`npm run compile`, then `node scripts/node-test.mjs site out/test/site/siteClips.test.js`: 18 tests, 18 pass, 0 fail, includes "the shipped editing page plays the figure editor clip as video" and the base's table and paste clip tests.

## 7. Stage, expected text, docs line. PASS (carried, previous verify.md, cae819b)

The kit cases comparing `stage/harbour-guide.md`, `EXPECTED` and the clip.md block pass (claim 5). `docs/user/editing.md` carries the GIF line with the specification's alt text; pair in `work/verifier/evidence/before-after.md`.

## 8. Pictures

- PASS (carried from d930238 through the previous verify.md: clip unchanged): contact-sheet, rendered, 04-mark-1, sampled GIF frames and form.png: form flow, three new lines outlined, keycaps Ctrl+Enter / ⌘Enter, figure floating right; title bar "workspace", no username or path. Not checked: motion, rhythm, the loop as watched.
- `frames/03-zoomed.png`: the previous failure stands as a fact about the file and is now an accepted gap, disclosed in Known gaps (claim 9). Against `clip.md` line 51 ("Zoom on the text box and the paragraph under it after Apply") and Evidence 4 of `03-change-spec.md`, the frame shows the saved figure, not the directive. It is not attached to the description.

## 9. The new Known gaps bullet (03-zoomed). PASS (judged here, cae819b)

- "which clip.md describes as the zoom on the text box and the paragraph after Apply": Grep of `clip.md`, line 51: `![Zoom on the text box and the paragraph under it after Apply](frames/03-zoomed.png)`.
- "shows the saved figure instead": image opened: the rendered figure at the right with caption "Figure 1 Harbour light at dusk, from the north pier.", the paragraph on its left, the keycaps; no text box; no username or path.
- "the same picture as frames/rendered.png": `sha256sum` gives 931dda9a645ec44e9fc14e22ffb1a9fc4c599572863bec2d06d78d620e55bedb for both; `git ls-tree cae819b ... frames/` gives blob 1afc373d for both.
- "the kit takes it at the middle of the zoom, after the save": `clip-kit/lib/encode.mjs` lines 67 to 69: `zoomIn = take.zooms[0].t / story.rate + 0.6`, `at: (zoomIn + story.zoom.holdTo) / 2`. With `C:/okfclip495/figure-editor/take/take.json` (zoom t 6.79, save press t 8.652), rate 0.995 and holdTo 11.0: frame at about 9.21 s, save at about 8.70 s.
- "The rewritten directive shows in frames/04-mark-1.png": image opened: the text box with the `{figure}` directive, `:alt:` kept, the outline on `:width: 40%`, `:align: right`, `:name: fig-harbour-light`, the new caption; no username or path.

## 10. The two removed claims and the new Autonomous decisions bullet. PASS (judged here, cae819b)

- The posted body holds neither "No frame found" nor "two more times" (word diff, claim 1). The Evidence line now reads `check.json` passed: true, "verify" passed, 12.0 s, loop seam SSIM 0.9907, playback rate 0.995: check.json at cae819b gives passed true, verifyPassed true, length 12, loopSeamSsim 0.990696, playbackRate 0.995; "carried from d930238" holds by claim 2 (clip folder diff empty).
- "The GIF sits after the figure form sentence of docs/user/editing.md": `git diff c3c3a57 cae819b -- docs/user/editing.md` adds the GIF line (line 181) and a blank line on each side, after the passage on the figure form that ends "Escape keeps the figure as inserted." and before "Editing a table cell", the place section 6 of the specification gives.

## 11. Rest of the PR description. PASS

- Carried (previous verify.md, cae819b; text unchanged by the edit): layout of the project template; renders (headings, animated GIF, checked boxes); internal references only in the last section; no agent role as doer; attribution line last; Summary, Deliverables, Changes, Impacts, Blast radius match the diff, the scenario and the pictures; Test plan tests, local gates (claims 5, 6), requirements (nothing would change; one added `@tests_req` on SwRS-MDOKFSTUDIO-CORE-095) and changelog (commits are docs and test only); What the clip proves; Deviation (storyboard after take, owner approval in `02-answers.md`); the other Autonomous decisions (scenario.mjs, clip.md, take notes); the other Known gaps (form.png; check.json platform win32).
- Links, checked again with `curl -L` at cae819b: GIF 200 (1806032 bytes; the previous report matched its sha256 to the LFS oid), MP4 200 (653958), WebM 200 (457577), clip.md 200. The feature clip guideline requires these head-SHA links.
- Review box: `chantier log CR-495`, Driver note 2026-11-26T00:51:43Z, "move d930238..cae819b (restack) inspector approved at cae819b".
- CI box: `gh pr checks 515`: checks, report, static, static-windows, viewer-graph, visual pass (run 45728437962); integration and stress skipped. The first visual attempt cancelled at the 15 minute limit: carried (previous verify.md).
- Known gaps: the accepted failed claim (03-zoomed) has its bullet; the two other failed claims were removed, so they need none; no `UNVERIFIED` or `STALE` mark; `before-after.md` names no uncaptured pair.

Observation, not failing: the Autonomous decisions list does not name the site test and the stage tests of specification section 7; Changes covers both.

VERIFIED

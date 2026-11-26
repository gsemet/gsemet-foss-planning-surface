# Verify CR-494

Head: c3c3a57ed16874bf56f5834ef6d789443e842fbb

Move judged: restack, 4a47151e..6b54c6e6 to 1d55649b..c3c3a57e. Base: 1d55649b51bee924e24186700634cef03413272f. Worktree clean, HEAD equals the PR's `headRefOid`. Previous verdict: VERIFIED at 6b54c6e6.

Verdict: NOT VERIFIED. The delivered files and their tests hold at c3c3a57; the PR description as posted does not (F1 to F8). All eight are fixes of the description text; none needs a new commit.

## The move

- c3c3a57. `git range-diff 4a47151e..6b54c6e6 1d55649b..c3c3a57e`: commit 1 `0f0856fd = cc917941`; commit 2 `6b54c6e6 ! c3c3a57e`, differing only in the merged test title and the context of the `check.test.mjs` and `storyboard.test.mjs` hunks.
- c3c3a57. `git diff --stat 1d55649b..c3c3a57e`: 21 files, 748 insertions, 1 deletion: the clip folder, `docs/user/editing.md`, `check.test.mjs`, `storyboard.test.mjs`, `test/site/siteClips.test.ts`. No `src/`, no `CHANGELOG.md`.
- c3c3a57. `git diff --name-only 4a47151e 1d55649b`: the base changed the clip kit (`check.mjs`, `storyboard.mjs` and tests), `editing.md`, `siteClips.test.ts`, `src/`, requirements. Kit tests, site test, requirements and description are judged again.

## Claims that hold

1. c3c3a57. Kit tests: `just clip-kit-test`: tests 42, pass 42, fail 0, including "the shipped table-anchors clip.md reads as the clip the owner reviews", "the shipped table-anchors stage is the padded pipe table the clip films" and "the shipped scenarios declare their checks ... table clips".
2. c3c3a57. Site test: `just compile` (`tsc -p .`, no error), then `fnm exec -- node scripts/node-test.mjs unit out/test/site/siteClips.test.js`: tests 17, pass 17, fail 0, including "the shipped editing page plays the table handles clip as video".
3. c3c3a57. Requirements: `just requirements-update`: "0 files updated", "0 indexes updated", "0 requirement OKF projections updated" (lint warnings only); then `git status --short --branch` lists no change.
4. c3c3a57. Changelog: `git log --format="%h %s" 1d55649b..c3c3a57e`: `cc917941 docs: ...`, `c3c3a57e test: ...`; no `feat` or `fix`.
5. carried from 6b54c6e: clip folder untouched (`git diff --stat 6b54c6e6 c3c3a57e -- docs/demo-video/clips/table-anchors`: no output). `check.json`: passed true, length 12, MP4 and WebM 1280x720 15 fps, MP4 519040 B, WebM 356627 B, GIF 960 px 1704493 B loop 0, loopSeamSsim 0.992573, playbackRate 1.004, editMode on, paste false, verifyPassed true, win32, vsix, VS Code 1.147.0; all 20 checks ok (read again at c3c3a57).
6. c3c3a57. PR: `gh pr view 514`: draft, OPEN, MERGEABLE, CLEAN, base the stack branch at 1d55649b, head c3c3a57. Commit subjects are the specification's. Forge body equals `work/pr-body.md` (only a trailing newline differs).
7. c3c3a57. Body renders: `gh api .../pulls/514` `body_html` shows the sections and the GIF as an animated `<img>`. `curl -sIL` of the three raw URLs at c3c3a57 ends in 200: GIF image/gif 1704493 B, MP4 519040 B, WebM 356627 B, equal to `check.json`.
8. c3c3a57. The attached GIF (first frame) and the contact sheet opened as images: made-up content, title "launch-checklist.md - workspace - Visual Studio Code", no username, no home path; row drag, column drag, zoom with two marks, two captions saying "handle".
9. c3c3a57. Summary, Deliverables (GIF and links) and Changes match the diff. "No change to the extension": no `src/` file in the diff.
10. c3c3a57. Local gates: `just clip-kit-test` 42 tests, claim 1. `just check` and `just preflight` (Windows static stage): `chantier log CR-494`, note 2026-11-26T00:57:33Z "just preflight at c3c3a57: passed (Windows static stage; log in the driver scratch)" and `work/conflict-resolver/conflicts.md` ("just check ... head c3c3a57e: passed"). Not run again, per the brief; the driver's log was not opened. No long gate exists in `chantier.yaml`; `work/gates/preflight.log` is from the old head and is not used.
11. c3c3a57. Review box: `chantier log CR-494`, note 2026-11-26T00:51:47Z "move 6b54c6e..c3c3a57 (restack) inspector approved at c3c3a57".
12. c3c3a57. CI box: `gh pr checks 514`: static, static-windows, visual, viewer-graph, report, checks pass; heavy jobs skipping. `gh run view 45728432524`: headSha c3c3a57, success.
13. "The owner then approved the storyboard and the clip": `02-answers.md`, "Owner approval (2026-11-25, evening ...)".

## Claims that fail (PR description)

- F1, Deviation: "The take was filmed from the drafted storyboard (the trial take was clean and is the take)" is false. The delivered clip is a second take. Trial take, `work/gates/take1.log`: 39 screencast frames, 3.2 raw fps, SSIM 0.99250; `git show 43b126b1:.../check.json`: 39 frames, MP4 524275 B, WebM 358253 B, GIF 1694867 B, SSIM 0.992503. Head `check.json`: 36 frames, 3 raw fps, MP4 519040 B, SSIM 0.992573. `work/coder/r2.md`: "Retook and re-rendered the table-anchors clip"; `chantier log`: "round 1 render discarded". Fix: say the trial take was filmed from the draft and the delivered clip is a retake of the same scenario.
- F2, Test plan, Evidence: (a) names no SHA (it can read "at c3c3a57 (carried from 6b54c6e)"); (b) "`just clip table-anchors all` passed" is not what happened for the delivered clip: `r2.md`: "take passed; the render step failed once with a Remotion compositor error ...; `render` rerun alone passed, then `check` passed"; (c) "SSIM 0.9925" is the discarded take's 0.992503 rounded; the head's 0.992573 rounds to 0.9926.
- F3, Known gaps: "None." while a gap ships: macOS and Linux are not proved (specification, host matrix: "not proved"; `chantier log` driver note: "Windows only"; clip guideline: "says plainly which cell was not proved"). Fix: one bullet, no macOS or Linux take. Motion, rhythm and loop are covered by the owner's approval.
- F4, Autonomous decisions: the specification (section 7) requires the differences from the draft; omitted are the live storyboard's status and opening paragraph, the filled "Filmed on" row, and the plan notes moved into the scenario. Also omitted: the retake on a private scratch folder (F1) and the render rerun after the compositor error (F2).
- F5, Impacts: neither a before/after nor a "No visual change" line with its reason (`.agents/guidelines/pull-request.guidelines.md`: "the Verifier fails a body whose Impacts has neither"). The body says "No change to the extension. The editing page of the user docs shows a new clip." Fix: "No visual change in the extension (no `src/` file changes); the docs editing page gains the clip shown in Deliverables."
- F6, Deliverables: the specification (section 7) says the body links `clip.md` for the storyboard review; it is only a code path (`body_html`: `<code>`, no `<a>`). Fix: link `/blob/c3c3a57ed16874bf56f5834ef6d789443e842fbb/docs/demo-video/clips/table-anchors/clip.md`.
- F7, proofs without a SHA: Test plan "New or changed tests" and "Requirements" (`just requirements-update` leaves nothing to change: true at c3c3a57, claim 3) and "What the clip proves" (cites `check.json`) name none; "Changelog" names none either. Fix: add "at c3c3a57", or "(carried from 6b54c6e)" for the take's.
- F8, Blast radius: "Docs and kit tests only" is inexact: `test/site/siteClips.test.ts`, a site test outside the clip kit, changes too.

## Observations (not counted)

- `clip.md`, review notes (file untouched by the move): "Measured by the trial take, which is the take" repeats F1 beside the retake's figures; its Time row keeps presses 1.26 and 4.56 s against 1.22 and 4.52 s measured (under one frame at 15 fps). Changing it would be a new commit.
- The body still has "Storyboard to review" and "For the owner to judge" beside "The owner then approved".

Not proved here: motion, rhythm, the loop as watched, real-window behaviour (no take filmed by me; `check.json` is the take's record); macOS and Linux.

NOT VERIFIED

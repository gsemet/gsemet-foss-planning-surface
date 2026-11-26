Head: 5a73b6ebcf66ef80b412afcdbfd09c4defc028d8

Judgment of the restack move 3ea161c..5a73b6e (base: CR-499 head b7518fb) and of the rewritten
description of PR 522. All commands run in the CR worktree; every claim below is judged at 5a73b6e
unless it says "carried". Logs: `work/gates/verify-5a73b6e-*.log`.

## Move

- Pushed head. `git rev-parse HEAD`, `gh pr view 522 --json headRefOid,isDraft` and
  `git ls-remote origin "refs/heads/chantier/batch-09/*"` all give 5a73b6e; draft: true; base
  branch is the CR-499 branch; mergeStateStatus CLEAN. `git status --porcelain`: empty (end of pass).
- Patch. `git range-diff da86d6e8..3ea161c b7518fb3..HEAD`: commits 1 and 3 identical (`=`), commit 2
  differs by the conflict resolutions only (test title list, kept sibling tests; the CR's own
  keyboard-navigation lines unchanged). `git rev-list --merges b7518fb3..HEAD`: empty.
- Scope. `git diff --stat b7518fb3 HEAD`: 27 files, 858 insertions, 1 deletion (the clip folder,
  `docs/user/editing.md` +3, `check.test.mjs`, `storyboard.test.mjs`, `test/site/siteClips.test.ts`).
  `git diff --name-only b7518fb3 HEAD -- src CHANGELOG.md requirements`: empty.
- Clip folder. `git diff 3ea161c HEAD --stat -- docs/demo-video/clips/keyboard-navigation`: empty.
- Spec claims on the take and its behaviour: carried from 3ea161c (verdict VERIFIED in
  `chantier log CR-501`): clip folder unchanged; the base's `src/` changes are chart, preview style
  and width files, none exercised by the filmed outputs, and no new take was made.

## Gates at 5a73b6e (run in this pass)

- `just check`: exit 0. Clip kit 55 tests, 55 pass; unit 5306, 5299 pass, 0 fail, 7 skipped;
  security 107/107; release pytest 205 passed; requirements 0 errors, 26 warnings; "0 files would
  change". The log shows the two keyboard-navigation storyboard tests, the scenario check test and
  "the shipped editing page plays the keyboard navigation clip as video" passing.
- `just check-no-merge-commits origin/main`: passed (20 commits, no merge commit), exit 0.
  `just --unstable --fmt --check`: exit 0. `just audit`: found 0 vulnerabilities.
  `just sphinx-check`: 4 passed. `just requirements-report`: exit 0. These with `just check` are the
  `ci-static` recipe, the whole of `just preflight` on Windows; the driver's `just preflight` pass at
  this head is also in the CR log (2026-11-26T01:33Z).
- `just requirements-update`: exit 0, "0 indexes updated, 0 requirement OKF projections updated",
  tree clean afterwards.
- `gh pr checks 522`: checks, report, static, static-windows, visual, viewer-graph pass; the others
  skipping. `gh run list --commit 5a73b6e...`: run 45728482946, headSha 5a73b6e, success.

## PR description (posted text)

- Posted equals `work/pr-body.md`: `diff` of `gh pr view 522 --json body` with the file shows one
  trailing blank line only. Renders: headings, lists, task list, one image, links; no STALE and no
  UNVERIFIED mark. Layout follows `.github/PULL_REQUEST_TEMPLATE.md` (the project template ranks
  above chantier's layout). Internal references only in the last section. OK.
- Links at 5a73b6e. `curl -sSL` of the GIF, MP4, WebM raw URLs: HTTP 200, sizes 1675368, 574147,
  357763; `sha256sum` equals the worktree files and `git lfs ls-files` ids (1b7d3635, b2ed052f,
  644d3c8b). `clip.md` blob URL: HTTP 200. OK.
- Image look. GIF tiled every 6th frame (40 frames, 0.5 s steps), plus `frames/edit-on.png` and
  `contact-sheet.png` full: made-up names only (window title "release-plan.md - workspace"), no
  username, home path or account name. The top-right "M" disc is the clip's logo. OK.
- Summary and alt text, against the frames: 0 s reading mode; E (edit toggle on); Down heading; Down
  admonition; Enter editor "Lines 3-11"; Esc closed, admonition selected; Right sentence; Down list;
  Right first item; Enter admonition editor; caret walks; Ctrl+Backspace badge; "Thursday" typed;
  Ctrl+Enter; item reads Thursday under the orange mark. Pointer fixed bottom right in every
  unzoomed frame (cropped by the zoom otherwise); Grep of `scenario.mjs`: `moveTo`/`click` only in
  `setup` (lines 130-177), none in `run` (from line 182). "The editing guide says..." is the
  "Keyboard only" paragraph of `docs/user/editing.md` (line 109). No `src/` change. OK.
- Changes. `ffprobe`: MP4 and WebM 1280x720, 15 fps, 20.000 s; GIF 960x540, 240 frames in 20 s
  (12 fps); `check.json` gif loopCount 0. Folder listing: stage, `clip.md`, scenario, three videos,
  poster, contact sheet, first-last, key frames, `check.json`. Clip sits under "A list has three
  levels" (`git diff` of editing.md, line 132). Tests as listed. Impacts and Blast radius match. OK.
- Test plan, tests / Requirements / Changelog: gates above; `git diff b7518fb3 HEAD | grep -c
  "^+.*@tests_req"` gives 1 (CORE-095); `git log b7518fb3..HEAD`: docs, test, docs. OK.
- Local gates (55 tests, `just check`, `just preflight` static): gates above. OK.
- Evidence box. `git diff --name-only 66b8478 HEAD -- <clip folder>`: only `clip.md`; its diff is the
  "Changing one word" review note. `check.json`: passed true, "scenario verify passed" true, length
  20, loopSeamSsim 0.989976, playbackRate 1.003. `work/gates/take1..take8.log`: take8 passes; 1 and
  4-7 fail on scenario checks (list text, caret, trailing space), 2-3 on the Enter behaviour. Carried
  proof of the take (3ea161c: media unchanged). OK.
- Review box. Log note: "move 3ea161c..5a73b6e (restack) inspector approved at 5a73b6e...". OK.
- CI box: above. OK.
- What the clip proves. `check.json`: win32, VS Code 1.147.0, verify passed; scenario reads the state
  after each press and compares the file after Esc and at the end; owner approval of storyboard and
  clip in `02-answers.md` (2026-11-25 evening, media unchanged since). OK.
- Deviation. Recipe section "The storyboard first" has review before the take; rule moved after it
  (answer Q3); render/retake rule as in `clip.md` lines 9-11. Enter opens lines 3-11 (frames,
  take2/take3 logs, Q12). Up x5 and Right: scenario lines 288-308. Filed apart: inbox item
  `enter-on-a-list-item-in-an-admonition-op`. OK.
- Autonomous decisions. Q6, Q7, Q11; `git diff 66b8478 HEAD` of `clip.md` (note rewritten); scenario
  `LOOP_FALLBACK = false`; take logs show `C:\okfclip501`, port 9501 in the round note; no kit code
  in the diff (kit tests only). OK.
- Known gaps. Enter behaviour, badge (`isCombinedBadge` wants the command sign in the second group,
  `wrongModifier` refuses Ctrl on darwin, `storyboard.test.mjs` lines 820-823; the kit films on
  Windows and macOS only, `lib/platform.mjs` line 105), Windows only (`check.json` platform). No UNVERIFIED claim,
  no uncaptured pair (`work/verifier/evidence/before-after.md`: no pair applies). OK.

## Wording notes (not failures, nothing contradicts the delivered clip as a whole)

- Autonomous decisions, first bullet, "opens the item with Enter": Enter on the item opens an editor
  holding the item inside the whole admonition, as Summary and Deviation of the same body say.
- Deviation, "Home and End did not move it": `take5.log` shows End moving the caret to the end of the
  whole text, not to the item's end.
- `clip.md` "The loop seam" says the clip ends with "the item selected"; the frames after the save show
  the admonition selected (not a claim of the PR description).

VERIFIED

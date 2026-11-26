# Verify CR-494

Head: c3c3a57ed16874bf56f5834ef6d789443e842fbb

Description-only pass at the same head. Base: 1d55649b51bee924e24186700634cef03413272f. Code, test and clip claims passed at this head in the earlier pass and are not run again; the whole PR description is judged as it now stands on the forge.

Verdict: NOT VERIFIED. Two points of the description fail (D1, D2). Both are text edits; neither needs a commit.

## Description points that fail

### D1. "the clip shows the focus ring on the moved handle" is false (judged at c3c3a57)

Section "What the clip proves", second paragraph. No focus ring or shading shows on the moved handle. After each drop, the handle at the position the drag STARTED from stays shaded: after the row move, the third row's handle ("Build the packages"), not the moved row's (first row); after the column move, the handle above "Team" (third column), not above "Due" (first column).

- `docs/demo-video/clips/table-anchors/frames/row-dropped.png` (opened): grey box left of "Build the packages"; the handle left of "Fix the login bug" is plain. `frames/column-dropped.png` (opened): grey box above "Team"; the handle above "Due" is plain.
- `ffmpeg -i table-anchors.mp4 -vf "fps=15,select='between(n,30,105)',crop=600:300:0:70,scale=300:150,...,tile=5x16"`: shaded third-row handle in frames 39 to 53; shaded third-column handle in frames 88 to 105.
- `ffmpeg ... select='between(n,39,104)',crop=44:40:55:214,scale=132:120,tile=11x6` (the moved row's handle): plain dots in all 66 frames, no outline, no shading.
- `ffmpeg ... select='between(n,87,106)',crop=44:30:145:154,scale=132:90,tile=5x4` (the moved column's handle): plain dots in all 20 frames.
- Enlarged frames 48, 52, 96, 102: the shaded handle has a grey background and no outline. That matches the handle's `:hover` style, not its `:focus-visible` outline (`src/core/preview/styles/frontmatterEditorStyles.ts` lines 328 to 345). The cause was not investigated.
- `work/coder/r1.md` saw the same ("a highlighted handle shows left of 'Build the packages'") and called it the focus ring. The specification (section 7) lists "the focus ring on the moved handle" for the owner to judge; `clip.md` says only that an outline "may show".

Fix: replace "and the clip shows the focus ring on the moved handle" with "after each drop the handle where the drag started stays shaded; no focus outline shows on the moved handle", or delete the clause.

### D2. The carried proof names no source SHA (judged at c3c3a57)

Test plan, "Evidence at `c3c3a57`, carried from before the rebase, ...". `pr-template.md`, "The rules": a carried proof "names the head it now stands at and the SHA it came from" (`at <head7> (carried from <sha7>)`). The project template is silent on this.

Fix: "Evidence at `c3c3a57` (carried from `6b54c6e`: the rebase leaves the clip folder unchanged): ...". `git diff --stat 6b54c6e6 c3c3a57e -- docs/demo-video/clips/table-anchors` gave no output in the earlier pass at this head. The same marker may be added in "What the clip proves"; its citation of `check.json` at the head is accepted as it stands.

## The earlier pass's points (F1 to F8), judged at c3c3a57 on the new body

- F1 fixed: "The trial take was filmed from the drafted storyboard; the delivered clip is a second take of the same scenario." `git diff --stat 43b126b1 6b54c6e6`: 15 files (check.json, clip.md, renders, pictures), no `scenario.mjs`.
- F2 (b) and (c) fixed: the render failure and rerun match `work/coder/r2.md`; `check.json`: loopSeamSsim 0.992573 (0.9926), playbackRate 1.004, passed true. F2 (a) remains: D2.
- F3 fixed: Known gaps holds "macOS and Linux are not proved".
- F4 fixed: Autonomous decisions lists the draft differences, the retake and the render rerun. `diff work/storyboard/clip.md docs/demo-video/clips/table-anchors/clip.md` shows the status, opening paragraph, "Filmed on" row, times and review notes.
- F5 fixed: Impacts reads "No visual change in the extension (no `src/` file changes). ..."
- F6 fixed: `body_html` holds an `<a>` to `/blob/c3c3a57.../clip.md`; `curl -sL`: 200.
- F7 fixed: Test plan items name `c3c3a57`; "What the clip proves" cites `check.json` at `c3c3a57`.
- F8 fixed: "Docs, clip kit tests and one site test only", matching `git diff --stat 1d55649b..c3c3a57e` (21 files, 748 insertions, 1 deletion; no `src/`).

## Description claims that hold

1. c3c3a57. `git rev-parse HEAD` = c3c3a57ed16874bf56f5834ef6d789443e842fbb; `git status --short --branch` lists no change. `gh pr view 514`: draft, OPEN, MERGEABLE, CLEAN, headRefOid c3c3a57, base the stack branch at 1d55649b.
2. c3c3a57. `diff <(gh pr view 514 --json body) work/pr-body.md`: one trailing blank line only.
3. c3c3a57. Renders: `gh api .../pulls/514` (full+json) `body_html`: all sections as headings, lists, task boxes, the GIF as an animated `<img>`. The project template (`.github/PULL_REQUEST_TEMPLATE.md`) has no fold; its six sections are present in order and filled.
4. c3c3a57. `curl -sL` of the raw GIF, MP4, WebM at the head: 200; 1704493, 519040, 356627 bytes, equal to `check.json`.
5. c3c3a57. Summary, Deliverables, Changes, Impacts, Blast radius match the diff: `git diff 1d55649b c3c3a57e -- docs/user/editing.md test/site/siteClips.test.ts docs/demo-video/clip-kit/lib/check.test.mjs` shows the GIF under the table handles paragraph, the site test with the `CORE-095` marker and the added scenario check.
6. c3c3a57. Images: `contact-sheet.png`, `row-dropped.png`, `column-dropped.png` and the MP4 frames opened: made-up content, title "launch-checklist.md - workspace - Visual Studio Code", no username or home path. The dimmed row and column and the drop line show; no floating drag image; the raw text follows each move.
7. c3c3a57. Test plan, tests, requirements, changelog, kit tests (42): carried from the earlier pass at this head (claims run there: `just clip-kit-test` 42/42, site test 17/17, `just requirements-update` 0 files updated, `git log` with a `docs` and a `test` commit only).
8. c3c3a57. `just check` and `just preflight` (static stage): `work/conflict-resolver/conflicts.md` ("check ... head c3c3a57e: passed") and `chantier log CR-494` 2026-11-26T00:57:33Z "just preflight at c3c3a57: passed". Not run again.
9. c3c3a57. Review: `chantier log CR-494` 2026-11-26T00:51:47Z "inspector approved at c3c3a57".
10. c3c3a57. CI: `gh pr checks 514`: static, static-windows, visual, viewer-graph, report, checks pass; heavy jobs skipping.
11. "The owner then approved the storyboard and the clip": `02-answers.md`, "Owner approval (2026-11-25, evening ...)".
12. No chantier role name and no CR or batch id outside "Internal references".

## Observations (not counted)

- Changes names the clip folder's files but not `first-last.png`; the folder entry covers it.
- Per the brief, the `clip.md` review note "Measured by the trial take, which is the take" is not judged as a description point.

Not proved here: motion, rhythm, the loop as watched, real-window behaviour (no take filmed by me); macOS and Linux.

NOT VERIFIED

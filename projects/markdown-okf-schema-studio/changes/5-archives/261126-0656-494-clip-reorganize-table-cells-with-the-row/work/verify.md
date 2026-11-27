# Verify CR-494

Head: c3c3a57ed16874bf56f5834ef6d789443e842fbb

Description-only pass at the same head, after the pass that failed D1 and D2. Base: 1d55649b51bee924e24186700634cef03413272f. Only D1, D2 and "nothing else changed" are judged here; every other claim is carried from the earlier passes at this head. No code, test or clip proof was run again.

Verdict: VERIFIED.

## Judged in this pass (c3c3a57)

### D1. Focus ring clause: fixed

The paragraph now reads "A CDP drag has no floating drag image (the row or column is dimmed and a line shows where it lands). The owner then approved the storyboard and the clip." The clause "and the clip shows the focus ring on the moved handle" is gone, and the rendered `body_html` holds no "focus ring". What remains of the sentence is claim 6 below.

Command and output: the `diff` under "Nothing else changed", hunk `41c41`.

### D2. Carried proof names its source SHA: fixed

The Evidence box reads "Evidence at `c3c3a57` (carried from `6b54c6e`: the rebase leaves the clip folder unchanged): ...", the form of `pr-template.md`, "The rules" (`at <head7> (carried from <sha7>)`).

- `git diff --stat 6b54c6e6cab1481ad1ecf13a77e210afa1ccb564 c3c3a57ed16874bf56f5834ef6d789443e842fbb -- docs/demo-video/clips/table-anchors`: no output, so the stated reason holds.
- The `diff` below, hunk `33c33`: the text after the colon (take, render failure, rerun, `check.json` values) is the same as in the judged body.

### Nothing else changed since the earlier pass

The forge's edit history (`pullRequest.userContentEdits`, 4 entries) holds one edit after the judged body: judged body 2026-11-26T01:08:14Z, then 2026-11-26T01:12:39Z (`lastEditedAt`), after the NOT VERIFIED verdict of 01:12:27Z (`chantier log CR-494`).

`diff <(gh api graphql ... userContentEdits, entry editedAt 2026-11-26T01:08:14Z) <(gh pr view 514 --json body --jq .body)`:

```text
33c33
< - [x] Evidence at `c3c3a57`, carried from before the rebase, which leaves the clip folder unchanged: the take passed, ... playback rate 1.004)
---
> - [x] Evidence at `c3c3a57` (carried from `6b54c6e`: the rebase leaves the clip folder unchanged): the take passed, ... playback rate 1.004)
41c41
< ... A CDP drag has no floating drag image (the row or column is dimmed and a line shows where it lands), and the clip shows the focus ring on the moved handle. The owner then approved the storyboard and the clip.
---
> ... A CDP drag has no floating drag image (the row or column is dimmed and a line shows where it lands). The owner then approved the storyboard and the clip.
```

(Long unchanged parts of the two changed lines are cut here with "..."; there is no other hunk.)

- Latest forge body equals `work/pr-body.md`, trailing newlines ignored (compared by script: True).
- `git rev-parse HEAD` = c3c3a57ed16874bf56f5834ef6d789443e842fbb; `git status --short --branch`: the branch line only. Forge: headRefOid c3c3a57, baseRefOid 1d55649b, the same stack base branch, draft, OPEN, MERGEABLE, CLEAN.
- Renders: `gh api repos/gsemet/markdown-okf-schema-studio/pulls/514` (full+json) `body_html`: eleven headings, lists, seven checked task boxes, the GIF as an animated `<img>`.
- `gh pr checks 514`: static, static-windows, visual, viewer-graph, report, checks pass; the other jobs skipping.
- Known gaps: the one macOS and Linux bullet; no `STALE` mark, no `UNVERIFIED` claim in the body.

## Carried from the earlier passes at c3c3a57

Reason for each: the head and base did not move, and the diff above shows the description lines they judge did not change.

1. Earlier pass's points F1 to F8, fixed. F1: "The trial take was filmed from the drafted storyboard; the delivered clip is a second take of the same scenario" (`git diff --stat 43b126b1 6b54c6e6`: 15 files, no `scenario.mjs`). F2: render failure and rerun match `work/coder/r2.md`; `check.json` loopSeamSsim 0.992573, playbackRate 1.004, passed true; its source SHA part is D2 above. F3: Known gaps holds "macOS and Linux are not proved". F4: Autonomous decisions lists the draft differences, retake and render rerun (`diff work/storyboard/clip.md docs/demo-video/clips/table-anchors/clip.md`). F5: Impacts reads "No visual change in the extension (no `src/` file changes)". F6: the `clip.md` link at the head, `curl -sL`: 200. F7: Test plan items and `check.json` citation name `c3c3a57`. F8: "Docs, clip kit tests and one site test only" (`git diff --stat 1d55649b..c3c3a57e`: 21 files, 748 insertions, 1 deletion, no `src/`).
2. The six sections of `.github/PULL_REQUEST_TEMPLATE.md` are present in order and filled; the template has no fold.
3. `curl -sL` of the raw GIF, MP4, WebM at the head: 200; 1704493, 519040, 356627 bytes, equal to `check.json`.
4. Summary, Deliverables, Changes, Impacts, Blast radius match the diff: `git diff 1d55649b c3c3a57e -- docs/user/editing.md test/site/siteClips.test.ts docs/demo-video/clip-kit/lib/check.test.mjs` shows the GIF under the table handles paragraph, the site test with the `CORE-095` marker and the added scenario check.
5. Images: `contact-sheet.png`, `row-dropped.png`, `column-dropped.png` and the MP4 frames opened: made-up content, title "launch-checklist.md - workspace - Visual Studio Code", no username or home path.
6. The dimmed row and column and the drop line show; no floating drag image; the raw text follows each move.
7. Tests, requirements, changelog: `just clip-kit-test` 42/42, site test 17/17, `just requirements-update` 0 files updated, `git log` with a `docs` and a `test` commit only.
8. `just check` and `just preflight` (static stage): `work/conflict-resolver/conflicts.md` ("check ... head c3c3a57e: passed") and `chantier log CR-494` 2026-11-26T00:57:33Z "just preflight at c3c3a57: passed".
9. Review: `chantier log CR-494` 2026-11-26T00:51:47Z "move 6b54c6e..c3c3a57 (restack) inspector approved at c3c3a57" (read again in this pass).
10. "The owner then approved the storyboard and the clip": `02-answers.md`, "Owner approval (2026-11-25, evening ...)".
11. No chantier role name and no CR or batch id outside "Internal references".

## Observations (not counted)

- Changes names the clip folder's files but not `first-last.png`; the folder entry covers it.
- Per the earlier brief, the `clip.md` review note "Measured by the trial take, which is the take" is not judged as a description point.
- This pass wrote two temporary files (the edit history JSON and a compare script) in the session scratchpad instead of `work/scratch`; both are removed.

Not proved here: motion, rhythm, the loop as watched, real-window behaviour (no take filmed by me); macOS and Linux.

VERIFIED

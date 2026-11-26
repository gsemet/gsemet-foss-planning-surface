## Summary

Studio already lets a reader move a table row or column by dragging its handle in edit mode. This adds a short feature clip that shows it: a row dragged to the top by its handle, then a column dragged to the first place, with the raw Markdown beside the page following each move and every cell keeping its spacing. The extension does not change.

## Deliverables

![Dragging the row "Fix the login bug" by its handle to the top, then the "Due" column to the first place; the raw text follows](https://github.com/gsemet/markdown-okf-schema-studio/raw/c3c3a57ed16874bf56f5834ef6d789443e842fbb/docs/demo-video/clips/table-anchors/table-anchors.gif)

- MP4: https://github.com/gsemet/markdown-okf-schema-studio/raw/c3c3a57ed16874bf56f5834ef6d789443e842fbb/docs/demo-video/clips/table-anchors/table-anchors.mp4
- WebM: https://github.com/gsemet/markdown-okf-schema-studio/raw/c3c3a57ed16874bf56f5834ef6d789443e842fbb/docs/demo-video/clips/table-anchors/table-anchors.webm
- Storyboard to review: `docs/demo-video/clips/table-anchors/clip.md`

## Changes

- `docs/demo-video/clips/table-anchors/`: the live storyboard, the stage (one padded pipe table), the scenario (two mouse drags through CDP in a real VS Code window, then a zoom with two marks), and the rendered MP4, WebM, GIF, poster, contact sheet, key frames and `check.json` (12.0 s, 1280x720, 15 fps).
- `docs/user/editing.md`: the clip under the table handles paragraph.
- Tests: the shipped storyboard and stage, the scenario checks, and the editing page playing the clip.

## Impacts

No change to the extension. The editing page of the user docs shows a new clip.

## Blast radius

Grade: 1. Docs and kit tests only; a plain `git revert` restores the previous state.

## Test plan

- [x] New or changed tests (storyboard, check and site tests)
- [x] Requirements: No behaviour change (`just requirements-update` leaves nothing to change; one added test marker on `SwRS-MDOKFSTUDIO-CORE-095`)
- [x] Changelog: No user-facing change (no `feat` or `fix` commit)
- [x] Local gates: `just clip-kit-test` 37 tests, `just check` pass, `just clip table-anchors all` pass (`check.json` passed: true, loop seam SSIM 0.9925, playback rate 1.004); preflight (static stage) pass
- [ ] Review
- [ ] CI green

## What the clip proves, and what the owner judges

Proved by the take: real drags by the row and column handles in a real VS Code window on Windows move the row, then the column; the file on disk equals the expected text and the raw table keeps each cell's spacing (`check.json`, "scenario verify passed").

For the owner to judge: motion, rhythm, the loop as watched, the absence of a floating drag image (a CDP drag has none: the row or column is dimmed and a line shows where it lands), the focus ring on the moved handle, the texts, and "handle" for the owner's word "anchor".

## Deviation from the feature clip process

The recipe has the maintainer review the storyboard before the take. Under the owner's rule of the first clip stack that review moved after the take, into this pull request. The take was filmed from the drafted storyboard (the trial take was clean and is the take). A review lands as follows: an *(on screen)* row changed is a render (`just clip table-anchors render`, then `check`); a *(filmed)* row is a retake, a follow-up. The owner then approved the storyboard and the clip.

## Autonomous decisions

- Key frame names `row-drag`, `row-dropped`, `column-drag`, `column-dropped`; the second drag waits for the render of the first.
- Times follow the take; Length 12.0 s; the 12 s fallback (drop Mark 1) was not needed.

## Known gaps

None.

## Internal references

Specification and round notes live in the planning surface (CR-494, batch-09).

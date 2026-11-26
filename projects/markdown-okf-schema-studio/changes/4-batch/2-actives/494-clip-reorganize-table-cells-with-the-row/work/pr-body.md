## Summary

Studio already lets a reader move a table row or column by dragging its handle in edit mode. This adds a short feature clip that shows it: a row dragged to the top by its handle, then a column dragged to the first place, with the raw Markdown beside the page following each move and every cell keeping its spacing. The extension does not change.

## Deliverables

![Dragging the row "Fix the login bug" by its handle to the top, then the "Due" column to the first place; the raw text follows](https://github.com/gsemet/markdown-okf-schema-studio/raw/c3c3a57ed16874bf56f5834ef6d789443e842fbb/docs/demo-video/clips/table-anchors/table-anchors.gif)

- MP4: https://github.com/gsemet/markdown-okf-schema-studio/raw/c3c3a57ed16874bf56f5834ef6d789443e842fbb/docs/demo-video/clips/table-anchors/table-anchors.mp4
- WebM: https://github.com/gsemet/markdown-okf-schema-studio/raw/c3c3a57ed16874bf56f5834ef6d789443e842fbb/docs/demo-video/clips/table-anchors/table-anchors.webm
- Storyboard: [clip.md](https://github.com/gsemet/markdown-okf-schema-studio/blob/c3c3a57ed16874bf56f5834ef6d789443e842fbb/docs/demo-video/clips/table-anchors/clip.md)

## Changes

- `docs/demo-video/clips/table-anchors/`: the live storyboard, the stage (one padded pipe table), the scenario (two mouse drags through CDP in a real VS Code window, then a zoom with two marks), and the rendered MP4, WebM, GIF, poster, contact sheet, key frames and `check.json` (12.0 s, 1280x720, 15 fps).
- `docs/user/editing.md`: the clip under the table handles paragraph.
- Tests: the shipped storyboard and stage and the scenario checks in the clip kit, and a site test of the editing page playing the clip.

## Impacts

No visual change in the extension (no `src/` file changes). The editing page of the user docs gains the clip shown in Deliverables.

## Blast radius

Grade: 1. Docs, clip kit tests and one site test only; a plain `git revert` restores the previous state.

## Test plan

- [x] New or changed tests at `c3c3a57` (storyboard, check and site tests)
- [x] Requirements at `c3c3a57`: No behaviour change (`just requirements-update` leaves nothing to change; one added test marker on `SwRS-MDOKFSTUDIO-CORE-095`)
- [x] Changelog at `c3c3a57`: No user-facing change (no `feat` or `fix` commit)
- [x] Local gates at `c3c3a57`: `just clip-kit-test` (42 tests), `just check` and `just preflight` (static stage on Windows) pass
- [x] Evidence at `c3c3a57`, carried from before the rebase, which leaves the clip folder unchanged: the take passed, the render step failed once with a Remotion compositor error, `render` rerun alone and then `check` passed (`check.json` passed: true, loop seam SSIM 0.9926, playback rate 1.004)
- [x] Review: an independent review approved the rebased change at `c3c3a57`
- [x] CI green at `c3c3a57` (static, static-windows, visual, viewer-graph, report)

## What the clip proves

Proved by the take (`check.json` at `c3c3a57`, "scenario verify passed"): real drags by the row and column handles in a real VS Code window on Windows move the row, then the column; the file on disk equals the expected text and the raw table keeps each cell's spacing.

The take does not prove motion, rhythm, the loop as watched, the texts or the word "handle" for the owner's word "anchor": those are judged by watching. A CDP drag has no floating drag image (the row or column is dimmed and a line shows where it lands), and the clip shows the focus ring on the moved handle. The owner then approved the storyboard and the clip.

## Deviation from the feature clip process

The recipe has the maintainer review the storyboard before the take. Under the owner's rule of the first clip stack that review moved after the take, into this pull request. The trial take was filmed from the drafted storyboard; the delivered clip is a second take of the same scenario. A review change lands as follows: an *(on screen)* row changed is a render (`just clip table-anchors render`, then `check`); a *(filmed)* row is a retake, a follow-up.

## Autonomous decisions

- Differences between the draft storyboard and the live one: `status: draft` and the opening paragraph of a live storyboard; the "Filmed on" row filled from the take; the plan notes on the handle selectors and the two drops moved into the scenario; the times follow the take, with the same beats and order.
- The clip was filmed a second time, on its own scratch folder (`CLIP_SCRATCH`), with no kit change. Its first render failed once and passed when run again.
- Key frame names `row-drag`, `row-dropped`, `column-drag`, `column-dropped`; the second drag waits for the render of the first.
- Length 12.0 s; the 12 s fallback (drop Mark 1) was not needed.

## Known gaps

- macOS and Linux are not proved: the clip was filmed and checked on Windows only.

## Internal references

Specification and round notes live in the planning surface (CR-494, batch-09).

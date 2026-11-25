## Summary

A table in Studio takes a block of spreadsheet cells as a spreadsheet does: copy the cells, click a cell of the table, paste. The cells fill from the clicked cell rightwards and downwards, and the columns and rows the table lacks are added. This PR adds a 10 second feature clip of it and plays it on the editing page of the docs. No behaviour of the extension changes.

**Draft until the owner approves the storyboard and the clip here.**

## Deliverables

The clip (GIF inline; MP4 and WebM linked at this head):

![Five tab-separated lines copied from a text editor and pasted into a two-column table](https://github.com/gsemet/markdown-okf-schema-studio/raw/612623646a0dd0441fadd3425a8bcccb683945db/docs/demo-video/clips/paste-spreadsheet-cells/paste-spreadsheet-cells.gif)

- [MP4](https://github.com/gsemet/markdown-okf-schema-studio/raw/612623646a0dd0441fadd3425a8bcccb683945db/docs/demo-video/clips/paste-spreadsheet-cells/paste-spreadsheet-cells.mp4)
- [WebM](https://github.com/gsemet/markdown-okf-schema-studio/raw/612623646a0dd0441fadd3425a8bcccb683945db/docs/demo-video/clips/paste-spreadsheet-cells/paste-spreadsheet-cells.webm)
- [Storyboard (`clip.md`)](https://github.com/gsemet/markdown-okf-schema-studio/blob/612623646a0dd0441fadd3425a8bcccb683945db/docs/demo-video/clips/paste-spreadsheet-cells/clip.md) for the review.

What the clip proves: on Windows, in a real VS Code window, five tab-separated lines copied from a text editor (`tasks.tsv`, standing for a spreadsheet) and pasted into the header cell "Task" of a two-column table fill the table from that cell and add the column "Due" and three rows; the file on disk is exactly the expected text (`check.json`: scenario verify passed, no paste-options widget, playback rate 1.004, loop seam SSIM about 0.993). The clip makes no claim about the cell editor reopening after the paste.

What the owner judges: motion, rhythm, the loop as watched, the texts and their accent, the tab-separated file standing for a spreadsheet. Not watched by the author: the GIF and WebM played, the docs page rendering, the loop by eye; only the contact sheet and the key frames were viewed.

## Blast radius

Grade: **1**. Docs, a clip folder and tests only; `git revert` restores the previous state.

## Autonomous decisions

- Deviation from the recipe: the storyboard review that the recipe puts before the take was moved after it (decision of the Chief of Staff under the owner's overnight autonomy). The take was filmed from the Griller's draft; the owner reviews `clip.md` and the clip here, before this PR leaves draft; a retake after that review is a follow-up.
- The spec was amended mid-way: the cell editor did not reopen after the CDP paste in the first takes (the real-input integration test covers the reopen; filed apart as a possible bug). The scenario therefore checks only the table and the file on disk. The reopening is nondeterministic across takes; when the editor is open it widens the first column and pushes "Due" off the pane, so the scenario clicks "Done" in that case only, before the zoom (Shot row and review notes of `clip.md` say so).
- The scenario's setup polls up to 5 s for the five lines of the text editor (the window sometimes shows none at first); off camera.
- The 02-pasted frame is taken at the paste moment; its caption states only what is visible.
- Marks 1 and 2 touch at one time; the parser accepts it.
- Length 10.0 s (11.0 s proposed), as the take dictates.

## Known gaps

- Draft: the storyboard and the clip await the owner's review.
- The conditional Done click goes beyond the amended spec (above).
- Windows only; macOS and Linux not filmed.

<details><summary>Details</summary>

## Changes

- `docs/demo-video/clips/paste-spreadsheet-cells/`: stage (`release-checklist.md`, `tasks.tsv`), `clip.md`, `scenario.mjs`, the MP4, WebM, GIF, poster, contact sheet, key frames and `check.json`.
- `docs/user/editing.md`: a sentence and the GIF under "Inline editing".
- Tests: a storyboard case and a checks case in the clip kit tests; a site test that the editing page plays the clip.

## Impacts

The editing page of the docs shows the clip as video. No visual change in the extension.

## Test plan

- [x] New or changed tests: storyboard, checks and site cases (they read the shipped files).
- [x] Requirements: no behaviour change (`just requirements-update`: no file changed).
- [x] Changelog: no user-facing change.
- [x] Local gates: `just clip-kit-test` (26 tests), `just check`, `just preflight` (static stage on Windows).
- [ ] Review
- [ ] CI green

## Internal references

CR-489, batch-09, stacked on the drag-a-list-item clip PR.

</details>

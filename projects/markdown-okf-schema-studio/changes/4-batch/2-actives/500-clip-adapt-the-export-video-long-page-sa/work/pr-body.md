## Summary

Reworks the `export-html` feature clip into a stronger story: a long report page, in the default Cream theme and Auto width, with card grids, a very wide table that breaks out of the centred column, two Mermaid diagrams, a Vega-Lite chart and a full Vega chart. The clip scrolls the page in Studio, exports it with Export, opens the file in VS Code's Integrated Browser and shows the same page there: the wide table still breaking out, the diagrams and charts drawn. A reader with no editor gets the page as the writer sees it. No behaviour of the extension changes.

The charts are drawn as live inline views since the base of this change moved, so the clip was filmed and rendered again.

## Deliverables

18 s, 1280x720 at 15 fps, three captions in turn, one zoom with three marks in turn, no card, logo top right, a loop.

![export-html clip](https://github.com/gsemet/markdown-okf-schema-studio/raw/b0e6c6d9c6d69b07d1f95724033b6c1ed9bf1df5/docs/demo-video/clips/export-html/export-html.gif)

[MP4](https://github.com/gsemet/markdown-okf-schema-studio/raw/b0e6c6d9c6d69b07d1f95724033b6c1ed9bf1df5/docs/demo-video/clips/export-html/export-html.mp4), [WebM](https://github.com/gsemet/markdown-okf-schema-studio/raw/b0e6c6d9c6d69b07d1f95724033b6c1ed9bf1df5/docs/demo-video/clips/export-html/export-html.webm). The live storyboard, with the pictures and measured times: [clip.md](https://github.com/gsemet/markdown-okf-schema-studio/blob/b0e6c6d9c6d69b07d1f95724033b6c1ed9bf1df5/docs/demo-video/clips/export-html/clip.md).

What the clip proves: a real export in a real VS Code window keeps Cream, Auto width, the breakout at the same pixel width (887 px in Studio and in the browser, within 2 px) and the four drawings (two Mermaid images and two inline charts), with no script and no chart hover box (the take's `run` checks and `verify`; `check.json` passed). What the owner judges: motion, rhythm, the scroll speed, the loop as watched, the texts and their accent.

## Deviation from the feature clip process

The storyboard review moved from before the take into this PR: the take was filmed from the drafted storyboard. An *(on screen)* row the owner changes is a render (`just clip export-html render`, then `check`); a *(filmed)* row is a retake, a follow-up of this change.

## Changes

- `docs/demo-video/clips/export-html/`: new stage `stage/platform-report.md` (replaces `team-handbook.md`), reworked `scenario.mjs` and `clip.md`, new outputs (MP4, WebM, GIF, poster, contact sheet, key frames, `check.json`); `frames/release.png` removed (the tab click is gone).
- `docs/demo-video/clip-kit/lib/storyboard.test.mjs`: the shipped-clip case rewritten, a new case for the stage.
- `docs/user/toolbar.md`: the GIF's alt text.

From the merged clip: Cream, the default, instead of a forced Dark, so the clip no longer shows that a forced theme is kept; the tab set and its click are gone, so it no longer shows tabs working without JavaScript (both stay true and documented); 12 s to 18 s, two captions to three, two marks to three.

## Impacts

No visual change to the extension. The documentation page for Export plays the new clip.

## Blast radius

Grade: 1. Documentation and demo files only; a plain `git revert` restores the previous clip.

## Test plan

- [x] New or changed tests (the storyboard case and the new stage case fail on the previous clip)
- [x] Requirements: No behaviour change (`just requirements-update` leaves the tree clean)
- [x] Changelog: No user-facing change
- [x] Local gates: `just clip-kit-test` 56 tests pass; `just check` pass; `just preflight` (Windows static stage) pass
- [ ] Review
- [ ] CI green

## Known gaps

- The owner approved the earlier cut of this clip, not this one, which was filmed again.
- In the browser, each of the two scrolls shows as one cut, not as motion. The filmed window sends no new frame while the exported page scrolls; filming the browser's page itself would be a change of the clip kit. The cut of the earlier clip had the same fault.
- The browser shows a closed "Chart source" line under each chart, which Studio does not show. This is how the export works; under the bar chart the line sits partly behind the caption.
- The key frame taken as the browser opens still shows the command palette.
- Motion, rhythm, the scroll speed and the loop as watched are not checked by the author.
- The second card grid, the sequence diagram, the line chart and the small table appear in no key frame.
- The render step can fail once with a transient Remotion "No frame found" error; running `render` again passes.

## Autonomous decisions

- Length stays 18.0 s and the captions are unchanged. Marks 1 and 2 start 0.2 s later (12.0 to 13.2 and 14.2 to 15.2 s; mark 3 stays at 15.4 to 16.6 s), after the browser's picture changes, so no outline is drawn over the wrong block.
- The take's checks read the charts as inline drawings, no longer as images, and fail on a chart hover box in Studio or in the exported file. The pointer rests right of every chart while Studio is filmed.
- Both scrolls used the mouse wheel; the `scrollTo` fallback was not needed.
- The 16-column table kept all its columns: it fits without a sideways scroll (887 px in a 720 px column, view 1160 px).
- GIF at ladder step 0 (12 fps, 960 px, 128 colours), 2.93 MB.
- The stage is committed with LF endings (the drafted file had CRLF).
- Old frames removed: `frames/release.png`; the kit's `01-selected.png` and `02-pasted.png` stay.
- The take used its own scratch folder outside the user profile and its own port.

## Human decisions

Questions 1 to 13 of the grill: Cream, a long page with tables, grids, Mermaid and Vega, one very wide table in Auto width; 18 s in three beats; built from the merged kit; the storyboard reviewed in this PR; the bar chart as a `vega-lite` fence and the line chart as a `vega` fence.

## Internal references

CR-500, batch-09; stacked on CR-501, above CR-493 (the kit change to 30 s). The live chart views come from CR-503.

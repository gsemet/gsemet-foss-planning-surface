## Summary

Reworks the `export-html` feature clip into a stronger story: a long report page, in the default Cream theme and Auto width, with card grids, a very wide table that breaks out of the centred column, two Mermaid diagrams, a Vega-Lite chart and a full Vega chart. The clip scrolls the page in Studio, exports it with Export, opens the file in VS Code's Integrated Browser and shows the same page there: the wide table still breaking out, the diagrams and charts drawn. A reader with no editor gets the page exactly as the writer sees it. No behaviour of the extension changes.

This PR is a draft until the owner approves the storyboard and the clip.

## Deliverables

18 s, 1280x720 at 15 fps, three captions in turn, one zoom with three marks in turn, no card, logo top right, a loop.

![export-html clip](https://github.com/gsemet/markdown-okf-schema-studio/raw/b0e6c6d9c6d69b07d1f95724033b6c1ed9bf1df5/docs/demo-video/clips/export-html/export-html.gif)

[MP4](https://github.com/gsemet/markdown-okf-schema-studio/raw/b0e6c6d9c6d69b07d1f95724033b6c1ed9bf1df5/docs/demo-video/clips/export-html/export-html.mp4), [WebM](https://github.com/gsemet/markdown-okf-schema-studio/raw/b0e6c6d9c6d69b07d1f95724033b6c1ed9bf1df5/docs/demo-video/clips/export-html/export-html.webm). The live storyboard, with the pictures and measured times: [clip.md](https://github.com/gsemet/markdown-okf-schema-studio/blob/b0e6c6d9c6d69b07d1f95724033b6c1ed9bf1df5/docs/demo-video/clips/export-html/clip.md).

What the clip proves: a real export in a real VS Code window keeps Cream, Auto width, the breakout at the same pixel width (887 px in Studio and in the browser, within 2 px) and the four drawings, with no script (the take's `run` checks and `verify`; `check.json` passed). What the owner judges: motion, rhythm, the scroll speed, the loop as watched, the texts and their accent.

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
- [x] Local gates: `just clip-kit-test` 39 tests pass; `just check` pass; `just preflight` (Windows static stage) pass
- [x] Review (Inspector approved at da86d6e)
- [x] CI green (at b0e6c6d)

## Known gaps

- Motion, rhythm, the scroll speed and the loop as watched are not checked by the author.
- The second card grid, the sequence diagram, the line chart and the small table appear in no key frame.
- The render step can fail once with a transient Remotion "No frame found" error; running `render` again passes.

## Autonomous decisions

- The take ran from the drafted storyboard with no change of times (Length 18.0 s; marks at 11.8 to 13.0, 14.0 to 15.2 and 15.4 to 16.6 s).
- Both scrolls used the mouse wheel; the `scrollTo` fallback was not needed.
- The 16-column table kept all its columns: it fits without a sideways scroll (887 px in a 720 px column, view 1160 px).
- GIF at the first ladder step (10 fps, 960 px, 128 colours), 2.98 MB.
- The stage is committed with LF endings (the drafted file had CRLF).
- Old frames removed: `frames/release.png`; the kit's `01-selected.png` and `02-pasted.png` stay.
- The take used its own scratch folder outside the user profile and its own port.

## Human decisions

Questions 1 to 13 of the grill: Cream, a long page with tables, grids, Mermaid and Vega, one very wide table in Auto width; 18 s in three beats; built from the merged kit; the storyboard reviewed in this PR; the bar chart as a `vega-lite` fence and the line chart as a `vega` fence.

## Internal references

CR-500, batch-09; stacked on CR-493 (the kit change to 30 s).

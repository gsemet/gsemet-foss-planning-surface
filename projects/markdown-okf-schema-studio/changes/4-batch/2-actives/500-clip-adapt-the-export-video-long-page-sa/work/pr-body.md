## Summary

Reworks the `export-html` feature clip into a stronger story: a long report page, in the default Cream theme and Auto width, with card grids, a very wide table that breaks out of the centred column, two Mermaid diagrams, a Vega-Lite chart and a full Vega chart. The clip scrolls the page in Studio, exports it with Export, opens the file in VS Code's Integrated Browser and shows the same page there: the wide table still breaking out, the diagrams and charts drawn. A reader with no editor gets the page as the writer sees it. No behaviour of the extension changes.

## Deliverables

18 s, 1280x720 at 15 fps, three captions in turn, one zoom with three marks in turn, no card, logo top right, a loop.

![export-html clip](https://github.com/gsemet/markdown-okf-schema-studio/raw/c7c6a562420e55b83356a366806f57ff67a9c100/docs/demo-video/clips/export-html/export-html.gif)

[MP4](https://github.com/gsemet/markdown-okf-schema-studio/raw/c7c6a562420e55b83356a366806f57ff67a9c100/docs/demo-video/clips/export-html/export-html.mp4), [WebM](https://github.com/gsemet/markdown-okf-schema-studio/raw/c7c6a562420e55b83356a366806f57ff67a9c100/docs/demo-video/clips/export-html/export-html.webm). The live storyboard, with the pictures and measured times: [clip.md](https://github.com/gsemet/markdown-okf-schema-studio/blob/c7c6a562420e55b83356a366806f57ff67a9c100/docs/demo-video/clips/export-html/clip.md).

What the clip proves: a real export in a real VS Code window keeps Cream, Auto width, the breakout at the same pixel width (887 px in Studio and in the browser, within 2 px) and the four drawings (two Mermaid images and two inline charts), with no script and no chart hover box (the take's `run` checks and `verify`; `check.json` passed). What the owner judges: motion, rhythm, the scroll speed, the loop as watched, the texts and their accent.

## Deviation from the feature clip process

The storyboard review moved from before the take into this PR: the take was filmed from the drafted storyboard, kept in [clip.md](https://github.com/gsemet/markdown-okf-schema-studio/blob/c7c6a562420e55b83356a366806f57ff67a9c100/docs/demo-video/clips/export-html/clip.md). An *(on screen)* row the owner changes is a render (`just clip export-html render`, then `check`); a *(filmed)* row is a retake, a follow-up of this change.

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

- [x] New or changed tests at `c7c6a56` (the storyboard case and the new stage case fail on the previous clip)
- [x] Requirements at `c7c6a56`: No behaviour change (`just requirements-update` leaves the tree clean)
- [x] Changelog at `c7c6a56`: No user-facing change
- [x] Local gates at `c7c6a56`: `just clip-kit-test` 56 tests pass; `just check` pass; `just preflight` (Windows static stage) pass
- [x] Review: approved at `c7c6a56` (carried from `8ce169f`: a clean rebase, the same four commits)
- [x] CI green at `c7c6a56`: checks, static, static-windows, visual, viewer-graph and report pass; the heavy and release jobs are skipped, as on any pull request

## Known gaps

- The owner has not approved this cut of the clip; the approval given so far was for an earlier cut.
- In the browser, each of the two scrolls shows as one cut, not as motion. The filmed window sends no new frame while the exported page scrolls; filming the browser's page itself would be a change of the clip kit.
- The browser shows a closed "Chart source" line under each chart, which Studio does not show. This is how the export works; under the bar chart the line sits partly behind the caption.
- The key frame taken as the browser opens still shows the command palette.
- Motion, rhythm, the scroll speed and the loop as watched are not checked by the author.
- The sequence diagram, the line chart and the small table appear in no key frame.
- The clip was filmed on Windows only; no take proves it on macOS or Linux.
- The render step can fail once with a transient Remotion "No frame found" error; running `render` again passes.
- No take ran with the scenario's mark times as committed: marks 1 and 2 were set by a render, which draws them at the storyboard's times, and the scenario then took the same times.

## Autonomous decisions

- 18 s in three beats (the scroll in Studio, the export, the same page in the browser), built from the merged clip kit.
- The bar chart is a `vega-lite` fence and the line chart a `vega` fence.
- Marks run from 12.0 to 13.2, 14.2 to 15.2 and 15.4 to 16.6 s: the first two start after the browser's picture changes, so no outline is drawn over the wrong block.
- The take's checks read the charts as inline drawings, as Studio draws them, and fail on a chart hover box in Studio or in the exported file. The pointer rests right of every chart while Studio is filmed.
- Both scrolls used the mouse wheel; the `scrollTo` fallback was not needed.
- The 16-column table kept all its columns: it fits without a sideways scroll (887 px in a 720 px column, view 1160 px).
- GIF at ladder step 0 (12 fps, 960 px, 128 colours), 2.93 MB.
- The stage is committed with LF endings (the drafted file had CRLF).
- Old frames removed: `frames/release.png`; the kit's `01-selected.png` and `02-pasted.png` stay.
- The take used its own scratch folder outside the user profile and its own port.

## Human decisions

- The Cream theme, on a long page with tables, card grids, Mermaid and Vega diagrams, with one table so wide that it breaks out of the centred column.
- The clip scrolls through the page and exports it, then shows the exported file rendering the same, diagrams and charts drawn.
- The storyboard and the clip are reviewed in this PR, after the take.

## Internal references

CR-500 clip-export-long, batch-09; stacked on CR-510 (the merge-commit check on stacked pull requests), above CR-501 and CR-493 (the kit change to 30 s). The live chart views come from CR-503.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

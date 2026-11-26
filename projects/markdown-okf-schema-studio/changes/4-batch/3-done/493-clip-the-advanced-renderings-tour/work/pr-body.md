## Summary

Studio draws Mermaid, PlantUML, Vega-Lite, Vega, math and inline SVG in its preview, but nothing shows that at a glance. This adds a 16-second feature clip, "the advanced renderings tour": one design note in reading mode, in Cream, with each of the six renderings outlined in turn and named by a caption. It also lets the clip kit accept clips up to 30 seconds (it stopped at 12), which this clip needs and which other longer clips can use.

The owner approved the storyboard (`docs/demo-video/clips/advanced-renderings-tour/clip.md`) and an earlier cut of the clip. Charts on `main` have since become live views with text sized like the page text, so the clip was filmed again; its storyboard texts, times and six marks are the same.

## Deliverables

The clip, taken in a real VS Code window on Windows with the extension built as a VSIX, every setting at its default (PlantUML on the built-in engine, no Java):

![Renderings tour](https://github.com/gsemet/markdown-okf-schema-studio/raw/8c6845a50d411d894d83c7160e52e1306548330d/docs/demo-video/clips/advanced-renderings-tour/advanced-renderings-tour.gif)

MP4: https://github.com/gsemet/markdown-okf-schema-studio/raw/8c6845a50d411d894d83c7160e52e1306548330d/docs/demo-video/clips/advanced-renderings-tour/advanced-renderings-tour.mp4
WebM: https://github.com/gsemet/markdown-okf-schema-studio/raw/8c6845a50d411d894d83c7160e52e1306548330d/docs/demo-video/clips/advanced-renderings-tour/advanced-renderings-tour.webm

Left to judge by watching: motion, rhythm, six captions in 16 s, the scroll under the zoom, the loop. The take's own checks proved the six drawings are rendered (each chart as its live drawing), no PlantUML error is shown, each mark lies inside the zoom, and the file is unchanged on disk.

Against the earlier cut: the "Chart source" lines are gone, chart text is larger, the line chart has no "week" axis title, the bar chart's left axis shows three ticks, and the fourth mark now appears on a still page.

Kit change: the maximum clip length goes from 12 s to 30 s (one shared bound used by the storyboard parser and the MP4 duration check).

## Blast radius

The kit change touches only the demo-video tooling, its recipe and one glossary line; no `src/` change. A plain revert restores the old bound.

Grade: 1

## Autonomous decisions

- The recipe's order moved: the storyboard review happens in this pull request, not before the take; `clip.md` keeps `status: draft for the owner's review`.
- The glossary line "Feature clip" changed to "5 to 30 seconds" with the recipe.
- `durationLine` is exported from the kit's `check.mjs` so the bound can be tested.
- The clip is documented on the editing page, which lists the MyST renderings.
- The page is scrolled once with a smooth `scrollTo` in the preview frame: the CDP wheel never moved the webview page.
- To fit three renderings per view inside the zoom, the stage note's charts and the PlantUML sequence were made smaller than the draft (PlantUML scale 0.75 without footbox, Vega-Lite height 30, Vega height 80, SVG width 300).
- With the larger chart text, the line chart's x axis title was removed so its mark stays above the caption, and the bar chart asks for three y ticks so its labels do not overlap.
- The way to scroll is now tried off camera and the scroll down lasts 0.7 s instead of 0.8 s: tried during the take, it delayed the scroll and the fourth mark came in over a moving page.
- The storyboard's picture of the zoomed page moved from its first section to its fourth, because it shows the second view.

## Known gaps

- The owner approved an earlier cut; this re-filmed cut has not been watched by the owner.
- Motion, rhythm and the loop as watched were not judged by the author: the screencast frames were checked as stills only.
- Only a Windows take; macOS and Linux are not filmed.

<details><summary>Details</summary>

## Changes

- `docs/demo-video/clip-kit/lib/storyboard.mjs`: `MAX_LENGTH` 12 to 30.
- `docs/demo-video/clip-kit/lib/check.mjs`: new `durationLine`, built from the shared bounds.
- The recipe (`feature-clip-process.guidelines.md`) and the glossary say 5 to 30 s.
- New clip folder `docs/demo-video/clips/advanced-renderings-tour/` (storyboard, scenario, stage note, MP4, WebM, GIF, poster, frames, `check.json`).
- `docs/user/editing.md` shows the GIF; tests in the kit and `test/site/siteClips.test.ts`.

## Impacts

No visual change in the extension. The editing page of the user docs gains the clip (below: its "MyST rendering" entry, drawn from the page's Markdown with a plain stylesheet rather than the published theme, the clip paused on the first mark).

| Before (17b779d) | After (8c6845a) |
|---|---|
| ![Editing page before](https://github.com/user-attachments/assets/17c2826b-915c-4ef4-bf6a-fd01ccfb2788) | ![Editing page after](https://github.com/user-attachments/assets/4699ca77-9a6f-4df0-97fc-fb6b82ec8f2a) |

## Test plan

- [x] New or changed tests (they fail on the previous code), passing at 8c6845a: length refusals at 4.9 s and 30.1 s, 30.0 s accepted, `durationLine`, the shipped storyboard, the editing page plays the clip
- [x] Requirements: no behaviour change (`just requirements-update` leaves the tree unchanged)
- [x] Changelog: no user-facing change
- [x] Local gates at 8c6845a: `just preflight` (on Windows, its static stage); the take's `all` step with its `check` passed on the same files before the commit
- [x] Review: passed at 8c6845a
- [x] CI green: `gh pr checks 512` at 8c6845a: static, static-windows, visual, viewer-graph, report pass
- [x] Evidence: before at `17b779d`, after at `8c6845a`
- [x] Verified at `8c6845a`

## Internal references

CR-493, batch-09.

</details>

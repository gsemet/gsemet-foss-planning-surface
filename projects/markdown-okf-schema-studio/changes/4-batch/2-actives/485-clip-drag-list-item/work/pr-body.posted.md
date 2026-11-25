## Summary

Feature clips show the best features of Studio. This one shows the list item move: in edit mode the reader drags a list item by its handle, the item moves with its sub-items, the ordered list keeps its numbers in order, and the raw text of the same file, open beside the page, changes to match. The clip is one continuous shot (1280x720, 15 fps, silent, loops) with two captions in turn and two orange marks in turn, and plays on the editing page of the docs. No behaviour of the extension changes. The clip kit gains two small generic features so that a clip may start in edit mode and have no paste, and may name its own key frames.

## Deliverables

The clip, played from the committed GIF at the head (the MP4 and WebM are linked next to it):

![Drag a list item by its handle](https://github.com/gsemet/markdown-okf-schema-studio/raw/8197e4fd6b49d655dac95b3ef567db25c4f3a795/docs/demo-video/clips/drag-list-item/drag-list-item.gif)

- [MP4](https://github.com/gsemet/markdown-okf-schema-studio/raw/8197e4fd6b49d655dac95b3ef567db25c4f3a795/docs/demo-video/clips/drag-list-item/drag-list-item.mp4)
- [WebM](https://github.com/gsemet/markdown-okf-schema-studio/raw/8197e4fd6b49d655dac95b3ef567db25c4f3a795/docs/demo-video/clips/drag-list-item/drag-list-item.webm)
- Storyboard to review: [`clip.md`](https://github.com/gsemet/markdown-okf-schema-studio/blob/8197e4fd6b49d655dac95b3ef567db25c4f3a795/docs/demo-video/clips/drag-list-item/clip.md)

What the clip proves (the take's own checks): a real drag by the handle in a real VS Code window moves an item with its sub-items, the numbers stay 1 to 4, and `release-steps.md` on disk equals the expected text (`verify`). What the owner judges: motion, rhythm, the loop as watched, the absence of a floating drag image (a drag driven by the browser protocol shows the item faded in place and a line where it lands), the texts.

Kit shape, reusable by the next clips:

```js
// scenario.mjs
export const checks = { editMode: "on", paste: false }; // defaults: "off", true
// run(t)
t.keyFrame("drag"); // writes frames/drag.png at that moment
```

## Deviation from the feature clip process

The recipe has the maintainer review the storyboard before the take. That review is moved after the take, into this pull request, by the maintainer's overnight autonomy decision. The take was filmed from the drafted storyboard. A review lands as follows: an *(on screen)* row changed in `clip.md` is a render (`just clip drag-list-item render`, then `check`); a *(filmed)* row is a retake, a follow-up. This pull request stays a draft until the storyboard and the clip are approved.

## Blast radius

Grade: 1. Documentation tooling and one docs page only (`docs/demo-video/`, `docs/user/editing.md`, one site test); no change to `src/`. A plain `git revert` removes the clip and the two kit options; the raw copy clip is unchanged.

## Autonomous decisions

- The layout steps off camera differ from the first plan: the Command Palette opens with F1 (Ctrl+Shift+P typed into the document), and the scenario clicks the row `Reopen Editor With...` because `Reopen Editor with Text Editor` ranks first.
- Key frame names `drag` and `dropped`; the kit's numbered frames stay for clips with a press, a zoom and marks.
- The kit options `checks` (`editMode`, `paste`) and `t.keyFrame(name)` are generic on purpose: the next clips reuse them.
- The draft's times held (take 10.54 s, `Length` 10.5 s, rate 1.004), so the times stayed as drafted; the `Time` rows are refined.
- The drag clip's `Expected result` block is checked by the new test, not by the storyboard parser (the parser reads the paste clip's `Expected paste` block).
- Mark 1 wording without the comma, as the specification's differences list says.

## Known gaps

- Motion, rhythm and the loop as watched were not checked (stills and measured numbers only).
- The raw screencast runs at about 3.6 frames per second, so the drop line and the page change by steps.
- Only Windows was filmed; macOS and Linux are not proved.
- The pull request stays a draft until the owner approves the storyboard and the clip.

<details><summary>Details</summary>

## Changes

- `docs/demo-video/clip-kit/lib/check.mjs`: `resolveChecks`, `takeLines`; `take.mjs`: `t.keyFrame`, checks written in `verify.json`; `prepare.mjs`: `keyFrames` in `take.json`; `encode.mjs`: `keyFrameTimes`.
- Tests: `check.test.mjs`, `encode.test.mjs`, new cases in `storyboard.test.mjs` (shipped `clip.md` and `scenario.mjs` read from the repository).
- `docs/demo-video/clips/drag-list-item/`: stage, scenario, storyboard, MP4, WebM, GIF, poster, contact sheet, key frames, `check.json`.
- `docs/user/editing.md` plays the clip; `test/site/siteClips.test.ts` tests it; the recipe documents the new scenario exports.

## Impacts

The editing page of the docs shows the new clip. No visual change in the extension.

## Test plan

- [x] New or changed tests (they fail on the previous code): `just clip-kit-test` 25 tests pass, site test 9 pass, at 8197e4f
- [x] Requirements: no behaviour change (`just requirements-update`, 0 files changed; a test marker added to an existing SwRS)
- [x] Changelog: No user-facing change
- [x] Local gates at 8197e4f: `just clip drag-list-item all` pass; `just check` pass; `just preflight` pass (Windows static stage; CI runs the others)
- [x] Review: approved at 8197e4f
- [x] CI green at 8197e4f (`gh pr checks 503`: static, static-windows, viewer-graph, visual, report pass)

## Internal references

CR-485, batch-09, based on CR-484's branch (stacked); specification in the planning surface.

</details>

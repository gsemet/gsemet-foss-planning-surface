## Summary

A feature clip of the figure editor. In edit mode the writer points at a figure, presses **Edit figure** and gets one form for the whole figure (Source, Alt text, Caption, Legend, Width, Align, Name). The clip retypes the caption, sets Width to 40%, Align to Right and Name to `fig-harbour-light`, applies, then saves: the text box holds a clean `{figure}` directive and the smaller figure floats right of the text. Nobody has to remember the option names or the directive layout. The clip shows existing behaviour; no source file of the extension changes.

## Deliverables

Filmed in a real VS Code window on Windows with the clip kit, one continuous shot, two captions in turn, two marks in turn, one badged save chord, 12.0 s, 1280x720 at 15 fps, a loop.

![Edit a figure in one form](https://github.com/gsemet/markdown-okf-schema-studio/raw/d930238cc64eee77fe5dc0ad25c574a7231b7f5a/docs/demo-video/clips/figure-editor/figure-editor.gif)

- MP4: https://github.com/gsemet/markdown-okf-schema-studio/raw/d930238cc64eee77fe5dc0ad25c574a7231b7f5a/docs/demo-video/clips/figure-editor/figure-editor.mp4
- WebM: https://github.com/gsemet/markdown-okf-schema-studio/raw/d930238cc64eee77fe5dc0ad25c574a7231b7f5a/docs/demo-video/clips/figure-editor/figure-editor.webm
- Storyboard: `docs/demo-video/clips/figure-editor/clip.md`

What the clip proves (the take's own checks, `verify` and `check.json`): the Edit figure button opens the form filled from the directive; the keyboard fills it (Caption retyped after Ctrl/Cmd+A, Tab between fields, Align set with the `r` key, its list never opened); Enter in Name applies and keeps the `:alt:` line while adding the width, align and name lines; the save chord renders the figure at 40% floating right with its new caption and id. `harbour-guide.md` holds exactly the expected text.

What the owner judges: motion, rhythm, the loop as watched, the texts and the times.

## Changes

- `docs/demo-video/clips/figure-editor/`: live storyboard `clip.md`, `scenario.mjs`, stage files, rendered outputs (Git LFS), key frames, `check.json`.
- `docs/demo-video/clip-kit/lib/storyboard.test.mjs` and `check.test.mjs`: the shipped clip's storyboard, expected result, stage and checks are tested.
- `docs/user/editing.md`: the clip plays in the figure form paragraph of the editing page.
- `test/site/siteClips.test.ts`: the editing page plays the figure editor clip as video.

## Impacts

No visual change to the extension. The documentation site gains a clip on the editing page.

## Blast radius

Grade: **1**. Documentation, clip files and tests only; a plain `git revert` restores the previous state.

## Test plan

- [x] New or changed tests (kit storyboard and checks cases, site clip test)
- [x] Requirements: no behaviour change; the new site test carries `@tests_req SwRS-MDOKFSTUDIO-CORE-095`; `just requirements-update` leaves the tree clean
- [x] Changelog: no user-facing change
- [x] Local gates: `just clip-kit-test` (37 tests), `just format`, `just check`, `just clip figure-editor all --vsix ...` (`check.json` passed, verify passed, 12.0 s, playback rate 0.995, loop seam SSIM 0.991)
- [x] Review (inspector approved at 31c9d5d, committed as d930238)
- [x] CI green (static, static-windows, viewer-graph, visual at d930238; integration and stress skipped by design on a pull request)

## Known gaps

- The 1169x660 window cuts the form: a wheel move scrolls the page before the `filled` frame so all four new values show, but the `form` frame still cuts the empty Width, Align and Name fields, and the page stays scrolled until the save, so the loop fade is worth a look.
- After the save the focus returns to the figure and its Edit figure button shows; the take moves the pointer out over the scroll bar and back to hide it (a pointer move only, no field is set, hidden by the zoom).
- Only a Windows take; macOS and Linux are not proved.

## Deviation from the feature clip process

The recipe has the storyboard reviewed before the take. Here the storyboard is reviewed after the take, in this pull request: the author filmed a trial take from the draft, put its pictures and measured times in `clip.md`, filmed the take and opened this draft. A change to an *(on screen)* row is a render (`just clip figure-editor render`, then `check`); a change to a *(filmed)* row is a retake, a follow-up. The pull request stays a draft until the owner approves the storyboard and the clip.

## Autonomous decisions

- Click in Caption, then Ctrl/Cmd+A (no badge) selects its text before typing.
- Align was set with the `r` key (no fallback used).
- Key frames: `button`, `form`, `filled`, `03-zoomed`, `04-mark-1`, `05-mark-2`, `rendered`; `01-selected` and `02-pasted` are the kit's fixed names and are not linked.
- Zoom rectangle: the text box and the paragraph under it, padded 24 px; no widening needed.
- The Name step was kept.
- The GIF sits in the palette bullet of `docs/user/editing.md`, after the figure form sentence.
- The page numbers captions, so the scenario reads the caption without its number.

## Internal references

CR-495, batch-09; specification `03-change-spec.md`.

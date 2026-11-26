## Summary

A feature clip of the figure editor. In edit mode the writer points at a figure, presses **Edit figure** and gets one form for the whole figure (Source, Alt text, Caption, Legend, Width, Align, Name). The clip retypes the caption, sets Width to 40%, Align to Right and Name to `fig-harbour-light`, applies, then saves: the text box holds a clean `{figure}` directive and the smaller figure floats right of the text. Nobody has to remember the option names or the directive layout. The extension does not change.

## Deliverables

![In edit mode, Edit figure over a figure opens one form where the caption, Width, Align and Name are set; Apply writes the option lines and the saved figure floats right at 40%](https://github.com/gsemet/markdown-okf-schema-studio/raw/cae819b958dff6138d9b5dee1638a487234a5d79/docs/demo-video/clips/figure-editor/figure-editor.gif)

- MP4: https://github.com/gsemet/markdown-okf-schema-studio/raw/cae819b958dff6138d9b5dee1638a487234a5d79/docs/demo-video/clips/figure-editor/figure-editor.mp4
- WebM: https://github.com/gsemet/markdown-okf-schema-studio/raw/cae819b958dff6138d9b5dee1638a487234a5d79/docs/demo-video/clips/figure-editor/figure-editor.webm
- Storyboard: [clip.md](https://github.com/gsemet/markdown-okf-schema-studio/blob/cae819b958dff6138d9b5dee1638a487234a5d79/docs/demo-video/clips/figure-editor/clip.md)

## Changes

- `docs/demo-video/clips/figure-editor/`: the live storyboard, the stage, the scenario, and the rendered MP4, WebM, GIF, poster, contact sheet, key frames and `check.json` (12.0 s, a loop; MP4 and WebM at 1280x720 and 15 fps, GIF at 960 px and 12 fps).
- `docs/user/editing.md`: the clip after the figure form sentence.
- Tests: the shipped storyboard and stage and the scenario checks in the clip kit, and a site test of the editing page playing the clip.

## Impacts

No visual change in the extension (no `src/` file changes). The editing page of the user docs gains the clip shown in Deliverables.

## Blast radius

Grade: 1. Docs, clip kit tests and one site test only; a plain `git revert` restores the previous state.

## Test plan

- [x] New or changed tests at `cae819b` (storyboard, check and site tests)
- [x] Requirements at `cae819b`: No behaviour change (`just requirements-update` leaves nothing to change; one added test marker on `SwRS-MDOKFSTUDIO-CORE-095`)
- [x] Changelog at `cae819b`: No user-facing change (no `feat` or `fix` commit)
- [x] Local gates at `cae819b`: `just clip-kit-test` (44 tests) and `just check` pass
- [x] Evidence at `cae819b` (carried from `d930238`: the rebase leaves the clip folder unchanged): the take passed after one first render that failed with a Remotion "No frame found" error and was run again; `check.json` passed: true, "verify" passed, 12.0 s, loop seam SSIM 0.9907, playback rate 0.995
- [x] Review: an independent review approved the rebased change at `cae819b`
- [x] CI green at `cae819b` (static, static-windows, visual, viewer-graph, report; the visual job passed on a second run after the first one hit its 15 minute timeout)

## What the clip proves

Proved by the take (`check.json`, "scenario verify passed"): the Edit figure button opens the form filled from the directive; the keyboard fills it (the caption retyped, Tab between fields, Align set with the `r` key without opening its list); Enter in Name applies, keeps the `:alt:` line and adds the width, align and name lines; the save chord renders the figure at 40%, floating right, with its new caption and id, and `harbour-guide.md` holds exactly the expected text.

The take does not prove motion, rhythm, the loop as watched or the texts and their times: those are judged by watching. The owner then approved the storyboard and the clip.

## Deviation from the feature clip process

The recipe has the maintainer review the storyboard before the take. Under the owner's rule for these feature clips that review moved after the take, into this pull request: the pictures and measured times of `clip.md` come from the take. A review change lands as follows: an *(on screen)* row changed is a render (`just clip figure-editor render`, then `check`); a *(filmed)* row is a retake, a follow-up.

## Autonomous decisions

- The scenario clicks in Caption, then selects its text with Ctrl/Cmd+A (no badge) before typing; Align is set with the `r` key, and the fallback was not needed; the Name step is kept.
- After the save the focus returns to the figure and its Edit figure button shows; the take moves the pointer out over the scroll bar and back to hide it (a pointer move only, hidden by the zoom).
- A 300 ms hold comes before the `filled` frame, and a wheel move scrolls the page there so that the four new values show; this wheel move is not in the specification. The clip was filmed two more times for the scroll fix.
- The page numbers captions, so the scenario reads the caption without its number.
- Zoom rectangle: the text box and the paragraph under it, padded 24 px.
- Key frames `button`, `form`, `filled`, `03-zoomed`, `04-mark-1`, `05-mark-2` and `rendered`; `01-selected` and `02-pasted` are the kit's fixed names and are not linked.
- The clip was filmed on its own scratch folder and debugging port, with no kit change.

## Known gaps

- The 1169x660 window cuts the form: the `form` frame still cuts the empty Width, Align and Name fields, and the page stays scrolled until the save, so the loop fade is worth a look.
- macOS and Linux are not proved: the clip was filmed and checked on Windows only.

## Internal references

Specification and round notes live in the planning surface (CR-495, batch-09).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

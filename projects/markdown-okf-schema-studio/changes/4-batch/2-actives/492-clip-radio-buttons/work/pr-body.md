## Summary

A short feature clip of Studio's radio choice lists: a plan asks its reader to pick one of three options; a click on the second option selects it in the page and the `x` moves in the Markdown file, two characters on two lines. A zoom on the raw text then marks the new `(x)` and the old option, now `( )`. The clip is added to the user guide next to the radio list paragraphs.

## Deliverables

Filmed in a real VS Code window on Windows from the built extension: 1280x720, 15 fps, 10.5 s, one continuous shot, a loop.

![Studio reading mode on the left, the raw text on the right: a click on the second option moves the x](https://github.com/gsemet/markdown-okf-schema-studio/raw/211f3a59ec3e1a7d0c6589fd3ddfaa081b8d3b66/docs/demo-video/clips/radio-buttons/radio-buttons.gif)

[MP4](https://github.com/gsemet/markdown-okf-schema-studio/raw/211f3a59ec3e1a7d0c6589fd3ddfaa081b8d3b66/docs/demo-video/clips/radio-buttons/radio-buttons.mp4) and [WebM](https://github.com/gsemet/markdown-okf-schema-studio/raw/211f3a59ec3e1a7d0c6589fd3ddfaa081b8d3b66/docs/demo-video/clips/radio-buttons/radio-buttons.webm). The live storyboard for review: [clip.md](https://github.com/gsemet/markdown-okf-schema-studio/blob/211f3a59ec3e1a7d0c6589fd3ddfaa081b8d3b66/docs/demo-video/clips/radio-buttons/clip.md).

## Changes

- `docs/demo-video/clips/radio-buttons/`: storyboard, scenario, stage, the three renders, key frames and `check.json`.
- `docs/user/editing.md`: the GIF after the radio list paragraphs.
- Tests: the storyboard and checks of the shipped clip, and the docs page playing it as video.

## Deviation from the feature clip process

The storyboard review moved from before the take into this pull request: the take was filmed from the first storyboard draft. A row marked *(on screen)* that is changed is a render (`just clip radio-buttons render`, then `check`); a row marked *(filmed)* is a retake, a follow-up. This pull request stays a draft until the storyboard and the clip are approved.

## What the clip proves

A real click on a radio option in a real VS Code window selects it at once and moves the `x` on two lines of the file (the take's checks and `verify`). Still to judge by watching: motion, rhythm, the loop, the texts and their accent.

## Autonomous decisions

- Measured times, key frames (`pointed`, `chosen`, `03-zoomed`, `04-mark-1`, `05-mark-2`) and the focus ring as seen are in the Review notes of [clip.md](https://github.com/gsemet/markdown-okf-schema-studio/blob/211f3a59ec3e1a7d0c6589fd3ddfaa081b8d3b66/docs/demo-video/clips/radio-buttons/clip.md).
- The first full run on the default scratch folder rendered another clip's pictures (clips filmed in parallel share it); the take was rerun with its own scratch folder (`CLIP_SCRATCH`), with no kit change.

## Impacts

No change to the extension. A new clip in the user guide.

## Blast radius

Grade: 1. Documentation, a clip folder and tests of it; a plain `git revert` restores the previous state.

## Test plan

- [x] New or changed tests (storyboard, stage, checks, docs page)
- [x] Requirements: No behaviour change (one added `@tests_req` on an existing SwRS), `just requirements-update` leaves the tree unchanged
- [x] Changelog: No user-facing change
- [x] Local gates: `just clip-kit-test` (37 tests), `just check` pass
- [ ] Review
- [ ] CI green

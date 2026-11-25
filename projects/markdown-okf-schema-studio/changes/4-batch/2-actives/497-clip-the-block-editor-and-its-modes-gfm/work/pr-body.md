## Summary

A feature clip of the block editor and its palette modes. In edit mode, a click on a paragraph opens its editor with the GFM buttons; Ctrl+Shift+M then Down switches the palette to MyST, which adds the MyST buttons while the GitHub alert and the MyST tip around the paragraph render the same. The writer learns that the mode is a choice of tools, not of what the page can show.

## Deliverables

GIF (inline, 12 s loop, 1280x720 source): see the head's files below. The clip is `docs/demo-video/clips/block-editor-modes/`.

- Storyboard for review: `docs/demo-video/clips/block-editor-modes/clip.md`
- GIF, MP4 and WebM: `docs/demo-video/clips/block-editor-modes/block-editor-modes.{gif,mp4,webm}`

The take is real: a real click and real keys in a real VS Code window on Windows. Its checks show the GFM palette (9 GitHub buttons), then MyST (9 GitHub and 19 MyST buttons), the rendered alert and tip unchanged, and the file untouched. The request expected a render that changes with the mode; the code has none, so the clip films what exists.

## Changes

- New clip folder: stage, live storyboard, scenario, rendered videos, poster, key frames, `check.json`.
- Four test cases (storyboard, stage, checks, site page) and the clip's GIF in `docs/user/editing.md`.
- No change to `src/`, to a requirement text, to the clip kit's code or to the writing skill.

## Impacts

No behaviour change. The editing page plays the clip.

## Blast radius

Grade: 1. Documentation, test cases and media; a plain revert restores the previous state.

## Test plan

- [x] New or changed tests (storyboard, stage, checks, site page)
- [x] Requirements: no behaviour change (`just requirements-update` leaves the tree clean)
- [x] Changelog: no user-facing change
- [x] Local gates: `just clip block-editor-modes all` (12.0 s, loop SSIM 0.9957, verify passed), `just clip-kit-test` (37), `just check`
- [ ] Review
- [ ] CI green

## Deviation from the feature clip process

The storyboard review moved from before the take into this PR: the take was filmed from the draft storyboard. An on-screen row the owner changes is a render (`just clip block-editor-modes render`, then `check`); a filmed row is a retake, a follow-up. Review `clip.md` here.

## Known gaps

- Only 17 of the 19 MyST buttons have a box on screen, so mark 1 covers those 17.
- Motion, rhythm and the loop as watched are not checked by the author.
- The setup's reset of the stored mode was not exercised (the mode was already GFM).

## Summary

A feature clip of the block editor and its palette modes. In edit mode, a click on a paragraph opens its editor with the GFM buttons; Ctrl+Shift+M then Down switches the palette to MyST, which adds the MyST buttons while the GitHub alert and the MyST tip around the paragraph render the same. The writer learns that the mode is a choice of tools, not of what the page can show. The extension does not change.

## Deliverables

![In edit mode, a click on a paragraph opens its editor with the GFM buttons; Ctrl+Shift+M then Down switch the palette to MyST, which adds the MyST buttons, while the GitHub alert and the MyST tip around the paragraph render the same](https://github.com/gsemet/markdown-okf-schema-studio/raw/af4a4aa62da55cd2093d30c7a5763c0b6bdee8ea/docs/demo-video/clips/block-editor-modes/block-editor-modes.gif)

- MP4: https://github.com/gsemet/markdown-okf-schema-studio/raw/af4a4aa62da55cd2093d30c7a5763c0b6bdee8ea/docs/demo-video/clips/block-editor-modes/block-editor-modes.mp4
- WebM: https://github.com/gsemet/markdown-okf-schema-studio/raw/af4a4aa62da55cd2093d30c7a5763c0b6bdee8ea/docs/demo-video/clips/block-editor-modes/block-editor-modes.webm
- Storyboard: [clip.md](https://github.com/gsemet/markdown-okf-schema-studio/blob/af4a4aa62da55cd2093d30c7a5763c0b6bdee8ea/docs/demo-video/clips/block-editor-modes/clip.md)

## Changes

- `docs/demo-video/clips/block-editor-modes/`: the stage, the live storyboard, the scenario, and the rendered MP4, WebM, GIF, poster, contact sheet, key frames and `check.json` (12.0 s, a loop; MP4 and WebM at 1280x720 and 15 fps, GIF at 960 px and 12 fps).
- `docs/user/editing.md`: the clip in the palette modes item.
- Tests: the shipped storyboard and stage and the scenario checks in the clip kit, and a site test of the editing page playing the clip.

## Impacts

No visual change in the extension (no `src/` file changes). The editing page of the user docs gains the clip shown in Deliverables.

## Blast radius

Grade: 1. Docs, clip kit tests and one site test only; a plain `git revert` restores the previous state.

## Test plan

- [x] New or changed tests at `af4a4aa` (storyboard, check and site tests)
- [x] Requirements at `af4a4aa`: No behaviour change (`just requirements-update` leaves nothing to change; one added test marker on `SwRS-MDOKFSTUDIO-CORE-095`)
- [x] Changelog at `af4a4aa`: No user-facing change (no `feat` or `fix` commit)
- [x] Local gates at `af4a4aa`: `just clip-kit-test` (49 tests) and `just check` pass
- [x] Evidence at `af4a4aa` (carried from `1858396`: the rebase leaves the clip folder unchanged): the first run failed at mark 1 (two MyST buttons have no box on screen), the scenario was fixed and the take passed; `render` and `check` were run again after the last `clip.md` edit; `check.json` passed: true, "verify" passed, 12.0 s, loop seam SSIM 0.9957, playback rate 1.004
- [x] Review: an independent review approved the rebased change at `af4a4aa`
- [x] CI green at `af4a4aa` (static, static-windows, visual, viewer-graph, report)

## What the clip proves

Proved by the take (`check.json`, "scenario verify passed"): a real click and real keys in a real VS Code window on Windows open the block editor with the GFM palette (9 GitHub buttons), then switch it to MyST (9 GitHub and 19 MyST buttons); the rendered alert and tip are unchanged and the file is untouched. The request expected a render that changes with the mode; the code has none, so the clip films what exists.

The take does not prove motion, rhythm, the loop as watched or the texts: those are judged by watching. The owner then approved the storyboard and the clip.

## Deviation from the feature clip process

The recipe has the maintainer review the storyboard before the take. Under the owner's rule for these feature clips that review moved after the take, into this pull request: the take was filmed from the drafted storyboard. A review change lands as follows: an *(on screen)* row changed is a render (`just clip block-editor-modes render`, then `check`); a *(filmed)* row is a retake, a follow-up.

## Autonomous decisions

- Differences between the draft storyboard and the live one: the front matter, the opening paragraph, the links to the key frames, the "Filmed on" row (VS Code 1.147.0, extension 1.12.1) and extended notes (the Problems panel, the fixed key frames, the keycap, the measured times); the mark times are kept as drafted (the take measured within 0.06 s).
- The mode is changed with Down; the `m` fallback was not needed. Ctrl+Shift+M shows as the one keycap `Ctrl Shift M / ⇧⌘M`.
- The two admonitions are compared by their outer HTML, which is identical; the fallback comparison was not needed.
- Mark 1 covers the union of the MyST buttons that have a box on screen.
- Key frames `gfm`, `mode-select` and `myst`; `01-selected` and `02-pasted` are the kit's fixed names and are not linked.
- The GIF sits under the "Full mode adds ..." sentence of `docs/user/editing.md`, inside that item.
- At 11 s and in the last frame the faint hover outline and block handle of the paragraph still fade after Escape (no editor is open); kept as filmed.
- The clip was filmed on its own scratch folder (`CLIP_SCRATCH=C:/okfclip497`) and debugging port (`CLIP_PORT=9497`), with no kit change.

## Known gaps

- Only 17 of the 19 MyST buttons have a box on screen, so mark 1 covers those 17.
- The setup's reset of the stored mode was not exercised (the mode was already GFM in the fresh profile).
- macOS and Linux are not proved: the clip was filmed and checked on Windows only.

## Internal references

Specification and round notes live in the planning surface (CR-497, batch-09).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

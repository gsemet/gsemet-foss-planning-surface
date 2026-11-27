## Summary

The editing guide says the whole page can be edited from the keyboard, but nothing shows it. This adds a 20 second feature clip: a release plan opens in reading mode, `E` turns edit mode on, the arrow keys pick the heading then a `note` admonition, Enter opens the admonition and Escape closes it, Right goes inside it and Down reaches its list, Right selects the first item, Enter opens the admonition's editor, the word "Friday" of that item is replaced by "Thursday", and Ctrl+Enter saves. The pointer never moves. The extension does not change.

## Deliverables

![In edit mode, from the keyboard only: E turns edit mode on, Down selects a note admonition, Enter opens it and Escape closes it, Right goes inside it, Down reaches its list, Right selects the first item, Enter opens the admonition editor, one word of the item is changed and Ctrl+Enter saves](https://github.com/gsemet/markdown-okf-schema-studio/raw/5a73b6ebcf66ef80b412afcdbfd09c4defc028d8/docs/demo-video/clips/keyboard-navigation/keyboard-navigation.gif)

- MP4: https://github.com/gsemet/markdown-okf-schema-studio/raw/5a73b6ebcf66ef80b412afcdbfd09c4defc028d8/docs/demo-video/clips/keyboard-navigation/keyboard-navigation.mp4
- WebM: https://github.com/gsemet/markdown-okf-schema-studio/raw/5a73b6ebcf66ef80b412afcdbfd09c4defc028d8/docs/demo-video/clips/keyboard-navigation/keyboard-navigation.webm
- Storyboard: [clip.md](https://github.com/gsemet/markdown-okf-schema-studio/blob/5a73b6ebcf66ef80b412afcdbfd09c4defc028d8/docs/demo-video/clips/keyboard-navigation/clip.md)

## Changes

- `docs/demo-video/clips/keyboard-navigation/`: the stage, the live storyboard, the scenario, and the rendered MP4, WebM, GIF, poster, contact sheet, key frames and `check.json` (20.0 s, a loop; MP4 and WebM at 1280x720 and 15 fps, GIF at 960 px and 12 fps).
- `docs/user/editing.md`: the clip under "A list has three levels".
- Tests: the shipped storyboard and stage and the scenario checks in the clip kit, and a site test of the editing page playing the clip.

## Impacts

No visual change in the extension (no `src/` file changes). The editing page of the user docs gains the clip shown in Deliverables.

## Blast radius

Grade: 1. Docs, clip kit tests and one site test only; a plain `git revert` restores the previous state.

## Test plan

- [x] New or changed tests at `5a73b6e` (storyboard, check and site tests)
- [x] Requirements at `5a73b6e`: No behaviour change (`just requirements-update` leaves nothing to change; one added test marker on `SwRS-MDOKFSTUDIO-CORE-095`)
- [x] Changelog at `5a73b6e`: No user-facing change (no `feat` or `fix` commit)
- [x] Local gates at `5a73b6e`: `just clip-kit-test` (55 tests), `just check` and `just preflight` (static stage on Windows) pass
- [x] Evidence at `5a73b6e` (carried from `3ea161c`: the rebase leaves the clip folder unchanged; after the media were rendered only a review note of `clip.md` changed): the eighth run of the take passed, after runs that failed on bugs of the new scenario and on the Enter behaviour described below; `check.json` passed: true, "verify" passed, 20.0 s, loop seam SSIM 0.98998, playback rate 1.003
- [x] Review: an independent review approved the rebased change at `5a73b6e`
- [x] CI green at `5a73b6e` (static, static-windows, visual, viewer-graph, report)

## What the clip proves

Proved by the take (`check.json`, "scenario verify passed"): real key presses in a real VS Code window on Windows, the pointer never moving, turn edit mode on, move the selection through three levels, and change and save one word; the scenario reads the selection after each press and compares the saved file.

The take does not prove motion, rhythm, the loop as watched, the 20 seconds or the pace of the badges: those are judged by watching. The owner then approved the storyboard and the clip.

## Deviation from the feature clip process

The recipe has the maintainer review the storyboard before the take. Under the owner's rule for these feature clips that review moved after the take, into this pull request: the take was filmed from the drafted storyboard. A review change lands as follows: an *(on screen)* row changed is a render (`just clip keyboard-navigation render`, then `check`); a *(filmed)* row is a retake, a follow-up.

The planned last scene did not work as drafted. In the real window, Enter on the selected first list item inside the admonition opens the whole admonition in its editor (lines 3 to 11), not the item alone. The clip therefore ends where it works: Enter opens the admonition editor, the caret is moved to the item's last word with Up (five times) and Right, shown with no badge because Home and End did not move it in the filmed window, then Ctrl+Backspace deletes "Friday", "Thursday" is typed and Ctrl+Enter saves. The behaviour is filed apart as a possible bug; the clip would be filmed again if it is fixed.

## Autonomous decisions

- The clip presses `E` first to turn edit mode on and opens the item with Enter (the request pressed `e` to open it; in Studio `E` only turns edit mode on).
- The second Right selects the first list item, which is the item edited: Down already selected the list.
- The badge `Ctrl+⌫ / ⌥⌫` is kept with no change to the clip kit.
- The review note "Changing one word" of `clip.md` was rewritten to match what the take does.
- The key frame names, the measured times, the stage and the placement in the docs page were chosen while making the clip; the loop fallback (a last Escape) was not needed.
- The clip was filmed on its own scratch folder (`CLIP_SCRATCH=C:/okfclip501`) and debugging port (`CLIP_PORT=9501`), with no kit change.

## Known gaps

- Enter on a selected list item inside an admonition opens the whole admonition: the clip shows it as it behaves; it is not fixed here.
- The badge `Ctrl+⌫ / ⌥⌫` passes the storyboard check of the kit only for a Windows take.
- macOS and Linux are not proved: the clip was filmed and checked on Windows only.

## Internal references

Specification and round notes live in the planning surface (CR-501, batch-09).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

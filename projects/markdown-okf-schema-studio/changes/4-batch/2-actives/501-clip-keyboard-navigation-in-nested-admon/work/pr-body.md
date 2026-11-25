## Summary

The editing guide says the whole page can be edited from the keyboard, but nothing shows it. This adds a
20-second feature clip: a release plan opens in reading mode, `E` turns edit mode on, the arrow keys pick
the heading then a `note` admonition, Enter opens the admonition and Escape closes it, Right goes inside it
and Down reaches its list, then Enter opens the admonition's editor, the word "Friday" of the first item is
replaced by "Thursday", and Ctrl+Enter saves. The pointer never moves. The clip plays on the editing page.

## Deliverables

Clip (GIF inline; MP4 and WebM linked at the pushed head):

![Keyboard navigation clip](https://github.com/gsemet/markdown-okf-schema-studio/raw/66b84782df697c6ed9b7ec8119c7b1064fae8ee7/docs/demo-video/clips/keyboard-navigation/keyboard-navigation.gif)

- [MP4](https://github.com/gsemet/markdown-okf-schema-studio/raw/66b84782df697c6ed9b7ec8119c7b1064fae8ee7/docs/demo-video/clips/keyboard-navigation/keyboard-navigation.mp4)
- [WebM](https://github.com/gsemet/markdown-okf-schema-studio/raw/66b84782df697c6ed9b7ec8119c7b1064fae8ee7/docs/demo-video/clips/keyboard-navigation/keyboard-navigation.webm)
- Storyboard to review: [clip.md](https://github.com/gsemet/markdown-okf-schema-studio/blob/3ea161ce58f3b53cfc4121a4cd0581f3082561e6/docs/demo-video/clips/keyboard-navigation/clip.md)

## Changes

- `docs/demo-video/clips/keyboard-navigation/`: storyboard, scenario, stage, take outputs and key frames.
- `docs/user/editing.md`: the clip under "A list has three levels".
- Kit tests: storyboard and stage cases, the checks declaration; site test: the page plays the clip.
- No change to `src/`, to the clip kit's code or to any SwRS text.

## Deviation from the feature clip process

- The storyboard review moved from before the take into this pull request: the take was filmed from the
  drafted storyboard. An on-screen row you change is a render (`just clip keyboard-navigation render`, then
  `check`); a filmed row is a retake, a follow-up.
- The planned last scene did not work as drafted. In the real window, Enter on the selected first list item
  inside the admonition opens the whole admonition in its editor (lines 3 to 11), not the item alone. The
  clip therefore ends where it works: Enter opens the admonition editor, the caret is moved by key presses
  to the item's last word, Ctrl+Backspace deletes "Friday", "Thursday" is typed, Ctrl+Enter saves. This is
  filed apart as a possible bug against the structural navigation; the clip would be retaken if it is fixed.
- Home and End did not move the caret in the filmed window, so the caret goes to the item with Up (five
  times) and Right, shown as plain key presses without a badge.

This pull request stays a draft until the owner approves the storyboard and the clip. What the clip proves:
real key presses in a real VS Code window, the pointer never moving, edit mode on, the selection through
three levels, one word changed and saved (the take's checks and the verified file). What the owner judges:
motion, rhythm, the 20 seconds, the badges' pace, the loop as watched.

## Autonomous decisions

- `E` turns edit mode on, then Enter opens the editor (the request pressed `e`): to be confirmed by the owner.
- The second Right selects the first list item, not the list.
- The `Ctrl+⌫ / ⌥⌫` badge passes the kit on Windows only; the kit is unchanged.
- The last scene ends in the admonition editor, with the caret moved by Up (five times) and Right, shown with no badge.
- The key frame names, the measured times, the stage and the docs placement are the author's.
- The take ran on its own debugging port and scratch folder, so that other clips could be filmed in parallel.

## Impacts

A new clip on the editing page. No behaviour change.

## Blast radius

Grade: 1. Docs, a clip folder and tests; a `git revert` restores the previous state.

## Test plan

- [x] New or changed tests: storyboard, stage and checks cases in the kit tests, the site test for the page
- [x] Requirements: no behaviour change (`just requirements-update`: no change)
- [x] Changelog: no user-facing change
- [x] Local gates: `just clip keyboard-navigation all` (take pass, 20.0 s, GIF 1.60 MB, loop seam SSIM 0.98998), `just clip-kit-test` (40 tests) and `just check` at 3ea161c; the take and `just ci-static` at 66b8478 (carried: only the clip.md note changed since)
- [ ] Review
- [ ] CI green

## Known gaps

- Not checked by the author: motion, rhythm and the loop as watched; the owner judges them.
- Filmed on Windows only; the `Ctrl+⌫ / ⌥⌫` badge passes the kit on Windows only.
- Enter on a selected list item inside an admonition opens the whole admonition: shown as it behaves, not fixed here.

## Internal references

CR-501, batch-09; stacked on the tour clip.

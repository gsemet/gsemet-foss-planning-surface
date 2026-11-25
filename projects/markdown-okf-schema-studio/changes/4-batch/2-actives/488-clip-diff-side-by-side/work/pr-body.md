## Summary

A short clip of the review pair of the preview toolbar: **Diff** marks the blocks changed since the last Git commit with a green bar, then **Side-by-side** turns each change into a card, the block at the last commit on the left and as it is now on the right, removed words struck through and added words underlined. One continuous shot, two captions in turn, outlines in turn, 1280x720 at 15 fps (MP4, WebM and GIF). No behaviour of the extension changes.

**This pull request stays a draft until the maintainer approves the storyboard and the clip.** The storyboard review that the feature-clip guideline places before the take is done on this pull request instead: the take was made from the drafted storyboard, its pictures are in [clip.md](https://github.com/gsemet/markdown-okf-schema-studio/blob/<HEAD>/docs/demo-video/clips/diff-side-by-side/clip.md), and a retake after review is a follow-up.

## Deliverables

The clip (GIF inline from this pull request's head; MP4 and WebM at the same head):

![Diff marks the changed blocks, then Side-by-side shows before and after](https://github.com/gsemet/markdown-okf-schema-studio/raw/<HEAD>/docs/demo-video/clips/diff-side-by-side/diff-side-by-side.gif)

- [MP4](https://github.com/gsemet/markdown-okf-schema-studio/raw/<HEAD>/docs/demo-video/clips/diff-side-by-side/diff-side-by-side.mp4)
- [WebM](https://github.com/gsemet/markdown-okf-schema-studio/raw/<HEAD>/docs/demo-video/clips/diff-side-by-side/diff-side-by-side.webm)

What the take proves (real VS Code window on Windows, extension built as a VSIX from this branch; `check.json`, the take's `verify`): the file is a Git work tree with one commit and an uncommitted edit; Diff puts a green bar on the changed paragraph and on the two changed list items and on nothing else; Side-by-side shows two cards (the paragraph, the list) with the words struck or underlined as the storyboard says; the file is never changed by the feature. The reviewer judges motion, rhythm, the loop as watched, the texts and their accent and the times (not checked by the take).

## Changes

- `docs/demo-video/clips/diff-side-by-side/`: live storyboard `clip.md`, `scenario.mjs` (makes the Git repository off camera, films the two clicks, checks bars and cards), `stage/` files, the rendered clip, key frames, `check.json`.
- Kit tests on the shipped files: the storyboard case, the `checks` of the scenario, a new `scenarioRepository.test.mjs` (the repository the scenario makes, and its two refusals).
- `docs/user/toolbar.md` shows the GIF under the Side-by-side toggle; `test/site/siteClips.test.ts` checks the page plays the clip.
- No change to `src/`, the kit, requirements texts or dependencies.

## Impacts

No visual change to the extension; the toolbar page of the user docs gains the clip.

## Blast radius

Grade: 1. Documentation, clip files and tests only; `git revert` restores everything.

## Known gaps

- Motion, rhythm and the loop as watched are not checked by the take; the maintainer judges them.
- Takes on macOS and Linux are not done.

## Autonomous decisions

- **Three bars, not two.** Studio marks the innermost changed block, so a changed ordered list gets one bar per changed item: the clip shows three bars (paragraph, list items 2 and 3). The specification expected two. The stage text is unchanged, the storyboard, the scenario and Mark 1 follow Studio. The list is one card; the words are as drafted.
- Mark 1 starts at 2.05 s so the key frame `diff-on` has no outline; the pointer leaves the Diff button at once so no tooltip is in the frame.
- `git.decorations.enabled` off; the repository is made without touching the working file and kept across takes; the scenario ignores `GIT_DIR` and related variables.
- Key frame names `diff-on` and `side-by-side`; the test cases and the site test; the docs page and alt text.
- Concurrent takes need different `CLIP_PORT` values (a take on another port avoids cross-talk with a clip running on the default one); no kit change.
- The deviation from the recipe's order (take before the storyboard review) is reported above.

## Test plan

- [ ] New or changed tests (they fail on the previous code)
- [ ] Requirements: No behaviour change
- [ ] Changelog: No user-facing change
- [ ] Local gates: `just clip-kit-test`, `just check`, `just preflight`
- [ ] Review
- [ ] CI green

## Internal references

CR-488, batch-09, stacked on CR-485.

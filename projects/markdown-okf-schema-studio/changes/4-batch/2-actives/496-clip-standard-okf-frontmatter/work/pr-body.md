## Summary

A short feature clip of what Studio does with the standard OKF frontmatter of a page when no schema applies. A release note open in edit mode shows `title`, `description`, `status`, `date` and `tags` as a plain Names and Values table above the page. A click on the `draft` value of the `status` row opens a text box, `published` is typed and saved with Ctrl+Enter / ⌘Enter, and the table row and the "Status:" line of the page both read `published`. A zoom then marks the row, then the line. It shows existing behaviour only: no change to `src/`.

## Deliverables

Clip (11.5 s, 1280x720, 15 fps, loop):

![The okf-frontmatter clip](https://github.com/gsemet/markdown-okf-schema-studio/raw/39d3eb31801f1679b444e52afa9951ca2ec3daef/docs/demo-video/clips/okf-frontmatter/okf-frontmatter.gif)

- MP4: https://github.com/gsemet/markdown-okf-schema-studio/raw/39d3eb31801f1679b444e52afa9951ca2ec3daef/docs/demo-video/clips/okf-frontmatter/okf-frontmatter.mp4
- WebM: https://github.com/gsemet/markdown-okf-schema-studio/raw/39d3eb31801f1679b444e52afa9951ca2ec3daef/docs/demo-video/clips/okf-frontmatter/okf-frontmatter.webm
- Storyboard to review: `docs/demo-video/clips/okf-frontmatter/clip.md`

The GIF is also placed on the OKF user page (`docs/user/okf.md`).

## Deviation from the feature clip process

The storyboard review moved from before the take into this pull request: the take was filmed from the drafted storyboard. A row marked *(on screen)* that the owner changes is a render (`just clip okf-frontmatter render`, then `check`); a row marked *(filmed)* is a retake, a follow-up of this change. This clip has a twin, `okf-schema-bundle-frontmatter` (same page inside an OKF Schema bundle), to review side by side. This pull request stays a draft until the owner approves the storyboard and the clip.

## Changes

- `docs/demo-video/clips/okf-frontmatter/`: stage, live storyboard, scenario, the rendered clip, key frames and `check.json`.
- Kit tests (`storyboard.test.mjs`, `check.test.mjs`) and a site test (`siteClips.test.ts`) read the shipped files.
- `docs/user/okf.md`: the GIF.

## Impacts

Docs only: no visual or behaviour change in the extension.

## Blast radius

Grade: 1. Documentation, a clip and tests; a plain `git revert` restores the previous state.

## Test plan

- [ ] New or changed tests (they fail on the previous code)
- [ ] Requirements: No behaviour change (added test of an existing SwRS; `just requirements-update` leaves the tree unchanged)
- [ ] Changelog: No user-facing change
- [ ] Local gates: `just clip-kit-test` (41 tests), `just check`, `just ci-static`
- [ ] Review
- [ ] CI green

## What the clip proves and what the owner judges

Proved by the take (`check.json` `passed: true`): a real click on a frontmatter value in a real VS Code window opens its text box on `draft`; the save writes only the `status` line of the file (`verify` compares the whole file) and updates the table row and the page body to `published`; the mp4 and webm are 1280x720 at 15 fps, 11.533 s, loop seam SSIM 0.99553, playback rate 1.005. The owner judges: motion, rhythm, the loop as watched, the texts and their accent.

## Autonomous decisions

- The scenario records `readingMode` (not `editMode`) in its setup, because the kit's check reads that note; the first take failed only on that and was retaken.
- Mark 1 keeps the backticks around `status` (the storyboard parser reads them).
- The text is selected with Ctrl+A (no `select()` fallback was needed).
- Measured times: click 1.01 s, save 4.61 s, zoom 6.22 s, mark 1 7.01 to 8.71 s, mark 2 8.71 to 10.41 s, unzoom 10.51 s, end 11.51 s.
- After the click a small "Add field / Remove field" menu shows under the text box; it does not cover the `status` row and is kept as filmed.
- The GIF goes after the paragraph "Studio makes that metadata comfortable..." in `docs/user/okf.md`.
- The take ran with its own `CLIP_PORT=9496` and `CLIP_SCRATCH=C:/okfclip496` (parallel clips film on the same machine).

## Known gaps

- The raw screencast ran at 3 fps (retimed to 15 fps), so typing and page changes can look stepwise.
- `first-last.png` shows a faint ghost residue next to "draft" in its last frame; to judge as watched.
- `frames/editing.png` is taken at the click: it shows the ripple, not yet the text box.
- The status text "Saving frontmatter..." does not show in any frame.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

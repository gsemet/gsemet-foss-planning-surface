## Summary

One click on the Theme button of the floating toolbar changes the whole preview, and the Mermaid diagram and the Vega-Lite chart are drawn again in the new colours. This adds a short silent clip (10.9 s, 1280x720, 15 fps, a loop) that shows it, and plays it on the themes page of the user docs. No behaviour of the extension changes.

## Deliverables

The clip (GIF below; MP4 and WebM linked at the same head):

![The Theme button is clicked four times: the page, the admonition, the diagram and the chart go from Cream through the current theme, Dark and White back to Cream](https://github.com/gsemet/markdown-okf-schema-studio/raw/8d4af3c7a5589e95b4cfa3deeec96461e147c1c9/docs/demo-video/clips/theme-switch/theme-switch.gif)

- MP4: https://github.com/gsemet/markdown-okf-schema-studio/raw/8d4af3c7a5589e95b4cfa3deeec96461e147c1c9/docs/demo-video/clips/theme-switch/theme-switch.mp4
- WebM: https://github.com/gsemet/markdown-okf-schema-studio/raw/8d4af3c7a5589e95b4cfa3deeec96461e147c1c9/docs/demo-video/clips/theme-switch/theme-switch.webm
- Storyboard under review: `docs/demo-video/clips/theme-switch/clip.md`

## Impacts

No visual change in the extension; the themes page of the docs gains the clip.

## Blast radius

Grade: 1. Docs, a clip folder and tests only; a plain `git revert` restores the previous state.

## What the clip proves, and what you judge

Proved by the take: real clicks on the Theme button in a real VS Code window switch the theme mode in order, the button's title follows, and the diagram and the chart are drawn again (their image `src` changes) for each mode before the next step; `handbook.md` stays unchanged on disk; the render passes the kit's checks (MP4 and WebM 1280x720 at 15 fps, duration equal to the length, GIF 960 px at 12 fps, loop seam SSIM 0.99409, reading mode at the start, playback rate 1.004).

To judge: motion, the fade, rhythm, the loop as watched, the two texts, and the version rendered.

## Deviation from the feature clip process

The recipe has the maintainer review the storyboard before the take. Here that review moved after the take, into this pull request (decided under the owner's overnight autonomy): the take was filmed from the proposed draft, and this PR stays a draft until the storyboard and the clip are approved. A change to an *(on screen)* row is a render (`just clip theme-switch render`, then `check`); a change to a *(filmed)* row is a retake, a follow-up.

## Autonomous decisions

- The proposed version (Dark, White, Cream, two clicks) was filmed first. It failed only the loop seam line (SSIM 0.97717), so the four-click version was rendered (Cream, current, Dark, White, Cream; SSIM 0.99409). Frame 0 is Cream; the current VS Code theme shows for 0.8 s.
- Key frames are named `dark`, `white` and `cream` (`t.keyFrame`); the kit also writes `frames/03-zoomed.png`.
- "Drawn again" is read as a change of each drawing's `src`, not by decoding colours.
- "The third toolbar row" corrected to "the second toolbar row" on the themes page.
- Times and length follow the take (10.9 s).
- The existing kit test title was reworded to name the theme clip (assertions unchanged, one added), and the shared fixture's paste press time moved from 4.2 s to 4.6 s so the existing and the new cases share one take.
- The takes ran on the kit's default debugging port; the checks and key frames show the right window.

## Known gaps

- The motion, the fade, the rhythm, the loop as watched and the GIF as played were not watched; only the contact sheet and every key frame were looked at.
- The rendering of this page (GIF inline) is checked after the push.
- The raw screencast is 8.4 fps, retimed to 15 fps, so steps may look slightly stepped.

<details>
<summary>Details</summary>

## Changes

- `docs/demo-video/clips/theme-switch/`: the stage (`stage/handbook.md`), the live storyboard `clip.md` (status `draft`), the scenario `scenario.mjs`, the rendered MP4, WebM, GIF, poster, contact sheet, first and last frames, key frames and `check.json`.
- `docs/user/themes-and-motion.md`: plays the GIF under the first paragraph; "the third toolbar row" becomes "the second toolbar row" (the Theme button is on row 2).
- Tests in the clip kit (`storyboard.test.mjs`, `check.test.mjs`) and `test/site/siteClips.test.ts`: the shipped storyboard, the scenario's checks, the scenario's stage against the shipped stage file, and the themes page playing the clip.
- No change to `src/`, to the clip kit or to a requirement text.

## Test plan

- [x] New or changed tests (they fail on the previous code): the storyboard, scenario checks, stage and site test cases.
- [x] Requirements: no behaviour change (an added test of `SwRS-MDOKFSTUDIO-CORE-095`; `just requirements-update` changed nothing).
- [x] Changelog: no user-facing change.
- [x] Local gates: `just clip-kit-test` (35 tests, after the rebase), `just check`, `just preflight` (Windows, static stage), `just clip theme-switch all --vsix ...` (every `check.json` line passes).
- [ ] Review
- [x] CI green at 8d4af3c (static, static-windows, viewer-graph, visual pass)

## Internal references

CR-491, batch-09; stacked on the slash-menu-grid clip branch. Deviation decided by the Chief of Staff; draft filmed from the Griller's proposal.

</details>

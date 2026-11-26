## Summary

A short feature clip of what Studio does with the standard OKF frontmatter of a page when no schema applies. A release note open in edit mode shows `title`, `description`, `status`, `date` and `tags` as a plain Names and Values table above the page. A click on the `draft` value of the `status` row opens a text box, `published` is typed and saved with Ctrl+Enter / ⌘Enter, and the table row and the "Status:" line of the page both read `published`. A zoom then marks the row, then the line. The extension does not change.

## Deliverables

![A release note with no schema: a click on the draft value of the status row opens a text box, published is typed and saved, and the frontmatter table and the Status line of the page both read published](https://github.com/gsemet/markdown-okf-schema-studio/raw/d386ff61a3d5a2cda0cb54130a5ffea5600a3793/docs/demo-video/clips/okf-frontmatter/okf-frontmatter.gif)

- MP4: https://github.com/gsemet/markdown-okf-schema-studio/raw/d386ff61a3d5a2cda0cb54130a5ffea5600a3793/docs/demo-video/clips/okf-frontmatter/okf-frontmatter.mp4
- WebM: https://github.com/gsemet/markdown-okf-schema-studio/raw/d386ff61a3d5a2cda0cb54130a5ffea5600a3793/docs/demo-video/clips/okf-frontmatter/okf-frontmatter.webm
- Storyboard: [clip.md](https://github.com/gsemet/markdown-okf-schema-studio/blob/d386ff61a3d5a2cda0cb54130a5ffea5600a3793/docs/demo-video/clips/okf-frontmatter/clip.md)

Contact sheet of the take:

![contact-sheet](https://github.com/user-attachments/assets/8da13dc7-03c1-411b-a4c7-2fadb4d54daa)

## Changes

- `docs/demo-video/clips/okf-frontmatter/`: the stage, the live storyboard, the scenario, and the rendered MP4, WebM, GIF, poster, contact sheet, key frames and `check.json` (11.5 s, a loop; MP4 and WebM at 1280x720 and 15 fps, GIF at 960 px and 12 fps).
- `docs/user/okf.md`: the clip on the OKF user page.
- Tests: the shipped storyboard and stage and the scenario checks in the clip kit, and a site test of the OKF page playing the clip.

## Impacts

No visual change in the extension (no `src/` file changes). The OKF page of the user docs gains the clip shown in Deliverables.

## Blast radius

Grade: 1. Docs, clip kit tests and one site test only; a plain `git revert` restores the previous state.

## Test plan

- [x] New or changed tests at `d386ff6` (storyboard, check and site tests)
- [x] Requirements at `d386ff6`: No behaviour change (`just requirements-update` leaves nothing to change; one added test marker on `SwRS-MDOKFSTUDIO-CORE-095`)
- [x] Changelog at `d386ff6`: No user-facing change (no `feat` or `fix` commit)
- [x] Local gates at `d386ff6`: `just clip-kit-test` (47 tests) and `just check` pass
- [x] Evidence at `d386ff6` (carried from `39d3eb3`: the rebase leaves the clip folder unchanged): `check.json` passed: true, "verify" passed, 11.5 s, loop seam SSIM 0.9955, playback rate 1.005
- [x] Review: an independent review approved the rebased change at `d386ff6`
- [x] CI green at `d386ff6` (static, static-windows, visual, viewer-graph, report)

## What the clip proves

Proved by the take (`check.json`, "scenario verify passed"): a real click on a frontmatter value in a real VS Code window on Windows opens its text box on `draft`; the save writes only the `status` line of the file (`verify` compares the whole file) and updates the table row and the page body to `published`.

The take does not prove motion, rhythm, the loop as watched or the texts and their accent: those are judged by watching. The owner then approved the storyboard and the clip.

## Deviation from the feature clip process

The recipe has the maintainer review the storyboard before the take. Under the owner's rule for these feature clips that review moved after the take, into this pull request: the take was filmed from the drafted storyboard. A review change lands as follows: an *(on screen)* row changed is a render (`just clip okf-frontmatter render`, then `check`); a *(filmed)* row is a retake, a follow-up. This clip has a twin, `okf-schema-bundle-frontmatter` (the same page inside an OKF Schema bundle), to watch side by side.

## Autonomous decisions

- The scenario records `readingMode` (not `editMode`) in its setup, because the kit's check reads that note.
- Mark 1 keeps the backticks around `status`: the storyboard parser reads them.
- The text is selected with Ctrl+A; the `select()` fallback was not needed.
- Measured times: click 1.01 s, save 4.61 s, zoom 6.22 s, mark 1 7.01 to 8.71 s, mark 2 8.71 to 10.41 s, unzoom 10.51 s, end 11.51 s.
- After the click a small "Add field / Remove field" menu shows under the text box; it does not cover the `status` row and is kept as filmed.
- The GIF sits after the paragraph "Studio makes that metadata comfortable..." in `docs/user/okf.md`.
- The clip was filmed on its own scratch folder (`CLIP_SCRATCH=C:/okfclip496`) and debugging port (`CLIP_PORT=9496`), with no kit change.

## Known gaps

- The raw screencast ran at 3 fps (retimed to 15 fps), so typing and page changes can look stepwise.
- `first-last.png` shows a faint ghost residue next to "draft" in its last frame.
- `frames/editing.png` is taken at the click: it shows the ripple, not yet the text box.
- The status text "Saving frontmatter..." does not show in any frame.
- macOS and Linux are not proved: the clip was filmed and checked on Windows only.

## Internal references

Specification and round notes live in the planning surface (CR-496, batch-09).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

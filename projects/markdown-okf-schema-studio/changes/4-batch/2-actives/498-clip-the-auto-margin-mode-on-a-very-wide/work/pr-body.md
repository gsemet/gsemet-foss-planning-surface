## Summary

A short feature clip of the Width button's Auto mode on a very wide table. A page in Margin (the default) cuts a twelve-month deploys table at the text column; one click on the Width button sets Auto and the table breaks out of the column, centred, with every month and the total, while the heading and the paragraph stay where they were. The clip is draft until the maintainer approves the storyboard and the clip.

## Deliverables

The clip (10.6 s, 1280x720, 15 fps, a loop): [MP4](https://github.com/gsemet/markdown-okf-schema-studio/raw/cb1ccf693f2ad61203981586bd4e4f198ca3c6b0/docs/demo-video/clips/wide-table-auto-width/wide-table-auto-width.mp4) and [WebM](https://github.com/gsemet/markdown-okf-schema-studio/raw/cb1ccf693f2ad61203981586bd4e4f198ca3c6b0/docs/demo-video/clips/wide-table-auto-width/wide-table-auto-width.webm).

![A page in Margin width shows a twelve-month table cut at the text column; one click on the Width button sets Auto and the table breaks out of the column, centred, with every month and the total, while the paragraph keeps its narrow column](https://github.com/gsemet/markdown-okf-schema-studio/raw/cb1ccf693f2ad61203981586bd4e4f198ca3c6b0/docs/demo-video/clips/wide-table-auto-width/wide-table-auto-width.gif)

Live storyboard for review: `docs/demo-video/clips/wide-table-auto-width/clip.md`.

What the clip proves: a real click on the Width button in a real VS Code window switches Margin to Auto; the very wide table breaks out of the column, centred, and no longer scrolls, while the paragraph keeps its column; the file is unchanged (the take's `run` checks and `verify`). What the maintainer judges: motion, rhythm, the jump at the click, the loop as watched, the texts and their accent.

## Blast radius

Grade: 1. Documentation assets, test cases and one docs image; no change to `src/`. A plain `git revert` restores the previous state.

## Autonomous decisions

- One-click version rendered (10.6 s); the loop seam SSIM is 0.99137, so the fallback was not needed.
- Measured widths: page 1147 px, column 804 px, room 1115 px; the table is 1595 px of scroll width in Margin and 940 px in Auto, centred, no overflow. The table is unchanged (Total column kept), so its first 16 columns are the shared table of the export video clip.
- The expanded toolbar's rows end about 20 px above the table in Auto and in the zoom: they cover neither the table nor the Width button's neighbours.
- Key frames `margin` and `auto`; the GIF sits under the existing capture in `docs/user/wide-tables.md`.
- Taken with its own scratch folder and port (`CLIP_SCRATCH=C:/okfclip498`, `CLIP_PORT=9498`) so the frames show no user name.
- Windows only: no macOS or Linux take.

## Known gaps

- Motion, rhythm and the loop as watched are not checked by the author. At 4.2 raw frames per second the jump at the click reads as a cut.
- In the zoom frames the logo overlaps the toolbar's top row and the toolbar's last row is cut by the zoom edge; this is the kit's layout, not changed here.

## Deviation from the feature clip process

The storyboard review moved from before the take into this pull request; the take was filmed from the drafted storyboard, which is `docs/demo-video/clips/wide-table-auto-width/clip.md` (review it there). A row marked *(on screen)* the maintainer changes is a render (`just clip wide-table-auto-width render`, then `check`); a row marked *(filmed)* is a retake, a follow-up.

<details>
<summary>Details</summary>

## Changes

- `docs/demo-video/clips/wide-table-auto-width/`: stage `deploys.md`, `scenario.mjs`, live storyboard `clip.md`, MP4, WebM, GIF, poster, contact sheet, first and last frames, key frames and `check.json`.
- Kit test cases: the storyboard and the stage of the clip, and the declared checks.
- Site test: the wide tables page plays the clip as video.
- `docs/user/wide-tables.md`: the GIF under the existing capture.

## Impacts

No behaviour change; the user docs page on wide tables shows the clip.

## Test plan

- [ ] New or changed tests (they fail on the previous code)
- [ ] Requirements: No behaviour change
- [ ] Changelog: No user-facing change
- [x] Local gates at `cb1ccf6`: `just clip-kit-test`, `just check`, `just preflight` (Windows static stage), `just clip wide-table-auto-width all`
- [x] Evidence: take at `cb1ccf6` (`check.json` passed)
- [x] Review: approved at `cb1ccf6`
- [x] Verified at `cb1ccf6` (VERIFIED, work/verify.md)
- [x] CI green at `cb1ccf6`: `gh pr checks 519` at cb1ccf6: static, static-windows, viewer-graph, visual pass; real VS Code jobs skipped on a PR

## Internal references

CR-498 `clip-the-auto-margin-mode-on-a-very-wide`, batch-09, stacked on the figure editor clip.

</details>

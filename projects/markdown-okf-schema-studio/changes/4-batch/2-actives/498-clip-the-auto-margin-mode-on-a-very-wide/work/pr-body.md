## Summary

A short feature clip of the Width button's Auto mode on a very wide table. A page in Margin (the default) cuts a twelve-month deploys table at the text column; one click on the Width button sets Auto and the table breaks out of the column, centred, with every month and the total, while the heading and the paragraph stay where they were. The extension does not change.

## Deliverables

![A page in Margin width shows a twelve-month table cut at the text column; one click on the Width button sets Auto and the table breaks out of the column, centred, with every month and the total, while the paragraph keeps its narrow column](https://github.com/gsemet/markdown-okf-schema-studio/raw/37ef61b338b3ca56d1cb428983c78ebdb54684f0/docs/demo-video/clips/wide-table-auto-width/wide-table-auto-width.gif)

- MP4: https://github.com/gsemet/markdown-okf-schema-studio/raw/37ef61b338b3ca56d1cb428983c78ebdb54684f0/docs/demo-video/clips/wide-table-auto-width/wide-table-auto-width.mp4
- WebM: https://github.com/gsemet/markdown-okf-schema-studio/raw/37ef61b338b3ca56d1cb428983c78ebdb54684f0/docs/demo-video/clips/wide-table-auto-width/wide-table-auto-width.webm
- Storyboard: [clip.md](https://github.com/gsemet/markdown-okf-schema-studio/blob/37ef61b338b3ca56d1cb428983c78ebdb54684f0/docs/demo-video/clips/wide-table-auto-width/clip.md)

## Changes

- `docs/demo-video/clips/wide-table-auto-width/`: the stage, the live storyboard, the scenario, and the rendered MP4, WebM, GIF, poster, contact sheet, first and last frames, key frames and `check.json` (10.6 s, 1280x720, 15 fps, a loop).
- `docs/user/wide-tables.md`: the clip under the existing capture.
- Tests: the shipped storyboard and stage and the scenario checks in the clip kit, and a site test of the wide tables page playing the clip.

## Impacts

No visual change in the extension (no `src/` file changes). The wide tables page of the user docs gains the clip shown in Deliverables.

## Blast radius

Grade: 1. Docs, clip kit tests and one site test only; a plain `git revert` restores the previous state.

## Test plan

- [x] New or changed tests at `37ef61b` (storyboard, check and site tests)
- [x] Requirements at `37ef61b`: No behaviour change (`just requirements-update` leaves nothing to change; one added test marker on `SwRS-MDOKFSTUDIO-CORE-095`)
- [x] Changelog at `37ef61b`: No user-facing change (no `feat` or `fix` commit)
- [x] Local gates at `37ef61b`: `just clip-kit-test` (51 tests) and `just check` pass
- [x] Evidence at `37ef61b` (carried from `cb1ccf6`: the rebase leaves the clip folder unchanged): one take, no retake; `check.json` passed: true, "verify" passed, 10.6 s, loop seam SSIM 0.9914, playback rate 1.011
- [x] Review: an independent review approved the rebased change at `37ef61b`
- [x] CI green at `37ef61b` (static, static-windows, visual, viewer-graph, report)

## What the clip proves

Proved by the take (`check.json`, "scenario verify passed"): a real click on the Width button in a real VS Code window on Windows switches Margin to Auto; the very wide table breaks out of the column, centred, and no longer scrolls, while the paragraph keeps its column and the file is unchanged.

The take does not prove motion, rhythm, the jump at the click, the loop as watched or the texts and their accent: those are judged by watching. The owner then approved the storyboard and the clip.

## Deviation from the feature clip process

The recipe has the maintainer review the storyboard before the take. Under the owner's rule of the first clip stack that review moved after the take, into this pull request: the take was filmed from the drafted storyboard. A review change lands as follows: an *(on screen)* row changed is a render (`just clip wide-table-auto-width render`, then `check`); a *(filmed)* row is a retake, a follow-up.

## Autonomous decisions

- The one-click version is rendered (10.6 s); its loop seam passes (SSIM 0.99137), so the fallback with a return to Margin was not needed.
- Measured widths: page 1147 px, column 804 px, room 1115 px; the table has 1595 px of scroll width in Margin and is 940 px wide in Auto, centred, with no overflow. The table is unchanged (the Total column is kept).
- The expanded toolbar's rows end about 20 px above the table in Auto and in the zoom: they cover neither the table nor the Width button's neighbours.
- Key frames `margin` and `auto`; the GIF sits under the existing capture in `docs/user/wide-tables.md`.
- The clip was filmed on its own scratch folder (`CLIP_SCRATCH=C:/okfclip498`) and debugging port (`CLIP_PORT=9498`), so that the frames show no user name, with no kit change.

## Known gaps

- At 4.2 raw frames per second the jump at the click falls between two frames and reads as a cut.
- In the zoom frames the logo overlaps the toolbar's top row and the toolbar's last row is cut by the zoom edge; this is the kit's layout, not changed here.
- macOS and Linux are not proved: the clip was filmed and checked on Windows only.

## Internal references

Specification and round notes live in the planning surface (CR-498, batch-09).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

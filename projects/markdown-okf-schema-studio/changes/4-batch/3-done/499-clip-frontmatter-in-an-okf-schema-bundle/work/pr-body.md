## Summary

The OKF documentation page shows the properties table Studio makes from standard frontmatter, but not what an OKF Schema bundle adds to it: the schema's table, the validation and the select. This adds a 12 second silent feature clip of a note in such a bundle: a typed table with a Description column and type icons, an invalid `status` value flagged by the title badge, a pick from a select of the schema's values, a save, and the error gone. It is the sibling of the standard frontmatter clip (the same page, the same `status` field, the same click, save chord and marks). The stage differs in these points: `type: note`, a `_schema/` folder, the note placed in a `notes/` subfolder, and a starting `status` value with a typo (`publshed` where the sibling starts at `draft`). The extension does not change.

## Deliverables

![A note in an OKF Schema bundle: its frontmatter table shows a Description column and type icons, the title badge counts one error for the value "publshed"; a click opens a select with the schema's values, published is picked and saved, and the error is gone](https://github.com/gsemet/markdown-okf-schema-studio/raw/b7518fb3c16b8ac5da27f87c1165837530e5127f/docs/demo-video/clips/okf-schema-bundle-frontmatter/okf-schema-bundle-frontmatter.gif)

- MP4: https://github.com/gsemet/markdown-okf-schema-studio/raw/b7518fb3c16b8ac5da27f87c1165837530e5127f/docs/demo-video/clips/okf-schema-bundle-frontmatter/okf-schema-bundle-frontmatter.mp4
- WebM: https://github.com/gsemet/markdown-okf-schema-studio/raw/b7518fb3c16b8ac5da27f87c1165837530e5127f/docs/demo-video/clips/okf-schema-bundle-frontmatter/okf-schema-bundle-frontmatter.webm
- Storyboard: [clip.md](https://github.com/gsemet/markdown-okf-schema-studio/blob/b7518fb3c16b8ac5da27f87c1165837530e5127f/docs/demo-video/clips/okf-schema-bundle-frontmatter/clip.md)

## Changes

- `docs/demo-video/clips/okf-schema-bundle-frontmatter/`: the stage (`_schema/note.schema.yaml` and `notes/release-note.md`), the live storyboard, the scenario, and the rendered MP4, WebM, GIF, poster, contact sheet, key frames and `check.json` (12.0 s, a loop; MP4 and WebM at 1280x720 and 15 fps, GIF at 960 px and 12 fps).
- `docs/user/okf.md`: the clip on the OKF user page.
- Tests: the shipped storyboard and stage and the scenario checks in the clip kit, and a site test of the OKF page playing the clip.

## Impacts

No visual change in the extension (no `src/` file changes). The OKF page of the user docs gains the clip shown in Deliverables.

## Blast radius

Grade: 1. Docs, clip kit tests and one site test only; a plain `git revert` restores the previous state.

## Test plan

- [x] New or changed tests at `b7518fb` (storyboard, check and site tests)
- [x] Requirements at `b7518fb`: No behaviour change (`just requirements-update` leaves nothing to change; one added test marker on `SwRS-MDOKFSTUDIO-CORE-095`)
- [x] Changelog at `b7518fb`: No user-facing change (no `feat` or `fix` commit)
- [x] Local gates at `b7518fb`: `just clip-kit-test` (53 tests) and `just check` pass
- [x] Evidence at `b7518fb` (carried from `635f1ba`: the rebase leaves the clip folder unchanged): the take passed on its third run, after two runs failed on bugs of the new scenario; `check.json` passed: true, "verify" passed, 12.0 s, loop seam SSIM 0.9960, playback rate 1.007
- [x] Review: an independent review approved the rebased change at `b7518fb`
- [x] CI green at `b7518fb` (static, static-windows, visual, viewer-graph, report)

## What the clip proves

Proved by the take (`check.json`, "scenario verify passed"): in a real VS Code window on Windows, a click on the invalid `status` value opens a select with the schema's values; two ArrowDown keys reach `published`; the save writes it to the file, the schema file is unchanged, the title badge goes away and the body line reads "Status: published".

The take does not prove motion, rhythm, the loop as watched or the texts: those are judged by watching. The owner then approved the storyboard and the clip.

## Deviation from the feature clip process

The recipe has the maintainer review the storyboard before the take. Under the owner's rule for these feature clips that review moved after the take, into this pull request: the take was filmed from the drafted storyboard. A review change lands as follows: an *(on screen)* row changed is a render (`just clip okf-schema-bundle-frontmatter render`, then `check`); a *(filmed)* row is a retake, a follow-up.

The storyboard first said the `status` row is red at frame 0. The trial take showed that Studio paints no colour on a field row in error (the `okf-error` style exists only on the info row), so the only error signal on screen is the title badge reading 1 error. The clip shows what exists: every "red row" wording was changed to the badge, in the storyboard, the scenario comments and the alt text of the OKF page. No `src/` change.

## Autonomous decisions

- The error signal is shown as the title badge only, because the field row has no error colour; the missing row style is filed apart as a possible bug, not fixed here.
- The select is changed with ArrowDown and saved with the save chord; the trial showed no native popup, so no Escape was needed.
- Two scenario fixes came out of the trial: the table header cells are read without their resize handle glyphs, and the cell's stored value is compared in its JSON form.
- The clip was filmed on its own scratch folder (`CLIP_SCRATCH=C:/okfclip499`) and debugging port (`CLIP_PORT=9499`), with no kit change.

## Known gaps

- A field row in error has no colour of its own (existing behaviour, not changed here).
- The captions of the first three pictures in `clip.md` are loose: `frames/01-selected.png` is captioned as frame 0 but shows `published` picked in the status cell, before the save.
- The opening paragraph of `clip.md` says that only `type: note` and the `_schema/` folder are added, and leaves out the typo that its Stage row names.
- The raw screencast ran at 2.1 fps (retimed to 15 fps), so page changes can look stepwise.
- macOS and Linux are not proved: the clip was filmed and checked on Windows only.

## Internal references

Specification and round notes live in the planning surface (CR-499, batch-09).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

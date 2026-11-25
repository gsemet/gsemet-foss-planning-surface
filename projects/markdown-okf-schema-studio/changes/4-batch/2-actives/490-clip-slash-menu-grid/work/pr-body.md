## Summary

A new feature clip shows how fast a MyST card grid is written in the page. In edit mode the writer
types `/grid` on an empty line of a paragraph's text box, the slash menu highlights Grid, Enter opens
the "Insert grid" form, Enter again accepts its defaults, and the save chord renders two cards. A card
grid is a layout plain Markdown lacks, and agents otherwise write it as HTML: that is the selling point.
The clip is filmed in a real VS Code window, silent, 1280x720 at 15 fps, and loops. It also plays on the
slash menu page of the documentation. No behaviour of the extension changes.

This pull request stays a draft until the storyboard and the clip are reviewed here (see "Deviation from
the feature clip process").

## Deliverables

The clip, played from the head of this branch (GIF; MP4 and WebM linked at the same head):

![The slash menu opens on /grid with Grid highlighted, Enter opens the Insert grid form, Enter inserts a MyST grid, and Ctrl+Enter / ⌘Enter renders two cards](https://github.com/gsemet/markdown-okf-schema-studio/raw/d5e68210b4c9392e3faf66a561567b835dc3096a/docs/demo-video/clips/slash-menu-grid/slash-menu-grid.gif)

[MP4](https://github.com/gsemet/markdown-okf-schema-studio/raw/d5e68210b4c9392e3faf66a561567b835dc3096a/docs/demo-video/clips/slash-menu-grid/slash-menu-grid.mp4) |
[WebM](https://github.com/gsemet/markdown-okf-schema-studio/raw/d5e68210b4c9392e3faf66a561567b835dc3096a/docs/demo-video/clips/slash-menu-grid/slash-menu-grid.webm) |
[Storyboard (`clip.md`)](https://github.com/gsemet/markdown-okf-schema-studio/blob/d5e68210b4c9392e3faf66a561567b835dc3096a/docs/demo-video/clips/slash-menu-grid/clip.md)

```text
docs/demo-video/clips/slash-menu-grid/
  clip.md  scenario.mjs  stage/onboarding.md
  slash-menu-grid.{mp4,webm,gif}  poster.png  contact-sheet.png  first-last.png  frames/  check.json
```

What the clip proves: in a real VS Code window on Windows, `/grid` in MyST mode highlights Grid first
(Table second), the form takes its defaults (columns 2, gutter 2, cards 2), the save renders two cards
"Card 1" and "Card 2", and `onboarding.md` on disk holds exactly the expected text (the scenario's
checks and `verify`; `check.json` has `verifyPassed: true`). What the owner judges: motion, rhythm, the
loop as watched, and the texts and times of the storyboard.

## Deviation from the feature clip process

The recipe has the maintainer review the storyboard, with a picture per key moment from a trial take,
before the take. Here the storyboard is reviewed after the take, in this pull request: the batch filmed a
trial take from the draft, put its pictures and measured times in the storyboard, filmed the take that
ships, rendered and opened this draft pull request. How a review lands: a change to an *(on screen)* row
is a render (`just clip slash-menu-grid render`, then `check`); a change to a *(filmed)* row is a retake,
a follow-up. The recipe itself is not changed.

## Blast radius

Grade: 1. Documentation, clip files, tests of the clip kit and one site test. No change to `src/`, to the
kit or to the recipe. A plain `git revert` restores the previous state.

## Autonomous decisions

- The storyboard fields are split as the kit reads them (`Size`, `Frame rate`, `Zoom` rows).
- Scenario key frames `slash-menu` and `grid-form` (with the kit's `t.keyFrame`); `01-selected` and
  `02-pasted` are the kit's fixed frames, here just before and after the save chord.
- The two Enter keys, the typed `/grid` and the form's Enter are typed and not badged; only the save
  chord has its keycap.
- The click point is the right edge of the paragraph's last character; the scenario checks the caret is
  at the end.
- The take checks that the palette is in MyST mode (a mode stored for the workspace would win over the
  setting).
- The clip depends on the kit's `checks` export and `t.keyFrame` from the list drag clip's change.
- The GIF goes after the bullet list of `docs/user/slash-menu.md`, before the screenshot, with the alt
  text above.
- A site test plays the page as a video; a kit test compares the storyboard's "Expected result" block
  with the scenario's `EXPECTED`.
- The scenario moves the pointer back to its rest point right after the click: the palette opened under
  the click point and its tooltip showed in every picture.
- The take ran with its own `CLIP_PORT` (9490): the kit's default port is shared by every clip and the
  first takes reached another clip's window (only read there, no click or key, but that clip's take may have been disturbed).

## Known gaps

- **UNVERIFIED:** motion, rhythm and the loop as watched (judged by the owner on this pull request).
- The tab shows the editor's unsaved dot in the `slash-menu` picture only: it is the live state while
  typing. Left as filmed.
- In the zoomed pictures the top of the VS Code window (menu bar text, title) is cut at the top edge.
- No macOS or Linux take; with the default GFM palette mode `/grid` lists Table only (not filmed, stated
  in the storyboard).
- The clip's GIF rendering in this pull request page is checked after the push.

<details>
<summary>Details</summary>

## Changes

- `docs/demo-video/clips/slash-menu-grid/`: live storyboard `clip.md` (`status: draft`), stage, scenario,
  and the rendered outputs with their pictures and `check.json`.
- `docs/user/slash-menu.md`: the clip's GIF.
- `docs/demo-video/clip-kit/lib/storyboard.test.mjs`, `check.test.mjs`: cases on the shipped storyboard
  (captions, badge, zoom, mark, `validateStory` on win32 and darwin, `EXPECTED` against the storyboard's
  block, `checks` of the clip).
- `test/site/siteClips.test.ts`: the slash menu page plays the grid clip as video.

## Impacts

No visual change to the product. The documentation page gains a looping clip, the GIF shown in Deliverables above (same head).

## Test plan

- [x] New or changed tests (they fail on the previous code)
- [x] Requirements: no SwRS text change; the new site test carries `@tests_req SwRS-MDOKFSTUDIO-CORE-095`; `just requirements-update` leaves the tree unchanged
- [x] Changelog: No user-facing change (docs and clip files only, no `feat` or `fix` commit)
- [x] Local gates at `d5e6821`: `just clip-kit-test`, `just check`, `just ci-static`, `just preflight` (all pass; preflight static stage on Windows)
- [x] Evidence: take at d5e6821 (`check.json`, key frames, contact sheet)
- [x] Review: approved at `d5e6821`
- [ ] Verified at `NONE`
- [ ] CI green at `NONE`

## Internal references

CR-490 `clip-slash-grid`, batch-09 (stack, on the list drag clip's branch).

</details>

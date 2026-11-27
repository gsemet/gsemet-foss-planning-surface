# CR-497 before and after

Before: base `d386ff61a3d5a2cda0cb54130a5ffea5600a3793` (CR-496 head). After: head
`af4a4aa62da55cd2093d30c7a5763c0b6bdee8ea`. The change is docs, media and tests (no `src/` file),
so the pairs are read from the two commits' git objects; no extension screen differs.

## Pair 1: the clip folder

- Before: `git ls-tree -r --name-only d386ff61a3d5a2cda0cb54130a5ffea5600a3793 -- docs/demo-video/clips/block-editor-modes`
  prints nothing (no folder).
- After: the same command at `af4a4aa62da55cd2093d30c7a5763c0b6bdee8ea` lists 19 files: GIF, MP4,
  WebM, `check.json`, `clip.md`, contact sheet, first-last, poster, 9 key frames, `scenario.mjs`,
  `stage/release-plan.md`.

## Pair 2: the editing page and the tests

- Before: `git grep -n -E "block-editor-modes|block editor modes" d386ff61a3d5a2cda0cb54130a5ffea5600a3793 -- docs/user/editing.md test/site/siteClips.test.ts docs/demo-video/clip-kit/lib`
  prints nothing.
- After: the same command at `af4a4aa62da55cd2093d30c7a5763c0b6bdee8ea` finds the GIF at
  `docs/user/editing.md:178`, the site test at `test/site/siteClips.test.ts:126`, and the checks in
  `check.test.mjs` and `storyboard.test.mjs`.

## After images (the clip as posted, downloaded from the links of the PR description)

- `after-gif-frames-af4a4aa.png`: GIF frames 0, 18, 30, 42, 60, 78, 99, 117, 132, 143 at 12 fps.
  Edit mode, GFM then MyST palette, both badges, the three marks in turn. Frame 132 (11.0 s) still
  shows the editor open; the last frame shows no editor.
- `after-mp4-end-af4a4aa.png`: MP4 frames 165, 168, 170, 172, 174, 179 at 15 fps (11.0, 11.2,
  11.33, 11.47, 11.6, 11.93 s; each tile is labelled with its position 0 to 5 in this list).
  The editor is open at 11.0 and 11.2 s, closed from 11.33 s; the paragraph's outline and block
  handle then show and fade to the last frame.
- `after-mp4-tail-af4a4aa.png`: MP4 frames 168 to 179 of the committed file (same sha256 as the
  posted one), cropped to the paragraph (`ffmpeg -start_number 168 -i mp4-%03d.png -vf
  crop=920:60:170:265,tile=1x12`). Editor open in the first two tiles; then the outline and block
  handle show, hold, and fade up to the last frame.

All three images were looked at: no username or home folder shows (window title
`release-plan.md - workspace`; the tail image shows only the page).

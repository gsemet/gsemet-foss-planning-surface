# Trial kit changes (Griller's trial, 2026-11-25)

Evidence, not the implementation. To render the trial clip, the Griller changed a scratch copy of
the clip kit merged by CR-482 (PR #501, `origin/main`):

- `kit.diff`: the changes to `docs/demo-video/clip-kit/lib/storyboard.mjs` (timed `Caption <n>` and
  `Mark <id>` rows, read as "<text>, <from> to <to> s"; the `wrongModifier` refusal and the
  one-mark limit turned off) and to `remotion/src/Clip.tsx` (captions in turn with a 6-frame
  crossfade, marks by time, a badge split on " / " into two key groups).
- `scenario.mjs`: the trial scenario (selection from "migrations" to "every worker", copy, paste,
  zoom, three marks in turn, the exact expected paste checked in `verify`).
- `clip.kit.md`: the kit-format storyboard the trial rendered from (not the owner's storyboard,
  which is `work/storyboard/clip.md`).

The trial take pasted exactly the expected text. The kit's size and frame rate fields (1280x720,
15 fps) were not implemented in the trial: the 720p 15 fps MP4 was made with ffmpeg after the
render. The batch writes these changes properly, with their tests and the recipe's rules.

# 40-second video

- `01-storyboard.md`: every text and time, the owner's editing support.
- `demo-document.md`: the post-mortem shown in the window.
- `capture/`: throwaway VS Code profile (`setup.mjs`), filmed take (`capture.mjs`), clip and timing
  (`prepare.py`), storyboard reader (`story.py`), original music (`music.py`), render (`render.sh`).
- `remotion/`: the composition; `remotion/out/video-40s.mp4` is the result.

A text change needs only `sh capture/render.sh`. A change to the document or to a *(filmed)* row
needs a new take: `setup.mjs`, `capture.mjs`, `prepare.py`, then the render, with `TRIAL_SCRATCH`,
`TRIAL_DOC` and `TRIAL_NODE_ROOT` set. The scratch folder must have a short path, and the render
needs Remotion installed in `$TRIAL_SCRATCH/remo` (the `remotion/node_modules` link points there).

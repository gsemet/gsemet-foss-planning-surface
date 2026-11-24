# Storyboard, common rules: demo presentation (one video, with zooms)

Status: scenario draft for review with the user, 2026-10-28. Capture comes after the scenario is
agreed. Replaces the nine-scene storyboard of `00-request.md` for the next take.

## Purpose

One presentation video, about 75 s, that tells the story of the vision (`docs/VISION.md`): we read
more Markdown than code, the usual tools fall short, and the Studio is the shared surface between
a person and their coding agent. Feedback on the first three tracks:

- A and C: very good; keep C's motion design (title and end cards, kinetic subtitles, callouts).
- B: zooms too tight; everything too fast; too many zoom-in / zoom-out cycles.
- All: shows what, not why.

## Common rules

- 1920x1080, 30 fps, H.264 `yuv420p`, about 75 s, silent and with optional royalty-free music; a 15 s
  cut-down and a GIF ≤ 10 MB; English subtitles burned in and as `.srt`.
- Real VS Code window (track B capture), motion design from track C.
- **Pacing:** each act starts wide and holds 2 s before anything moves. At most one zoom per act,
  at most 1.5x, eased in over 0.8 s, held at least 4 s, eased out over 0.8 s. Never zoom on a
  subtitle edge. No zoom on the title and end cards.
- **Subtitles:** one per beat, at most two lines, at least 2.5 s on screen. They tell the why; a
  small callout label may name the feature.
- Cursor slow and smooth, click ripple, typing sped up beyond a few words.
- Chapter title in the corner per act (small, 1 s fade): "Read", "Annotate", "Edit".


## Open questions for the user

1. Music: none, or a royalty-free track (source and licence recorded)?
2. Front matter and OKF-Schema: left out of this video (it has its own short video later); agree?
3. Demo document: a fictional plan ("Add a cache to the export service")? Neutral, no employer
   data.

Decision (user, 2026-10-28): no act where the agent reacts; Annotate goes straight to Edit.

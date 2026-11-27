# Storyboard, common rules: short videos, vertical series

Status: scenario draft, 2026-10-28. Same features as the horizontal series
([../10-short-videos-horizontal/](../10-short-videos-horizontal/00-common.md)), but each video has
its own scenario and capture, built for a phone screen.

## Purpose

YouTube Shorts and X. Viewers scroll fast: the first second must hook, each screen shows one idea,
and the type must read on a phone.

## Common rules

- 1080x1920, 30 fps, H.264 `yuv420p`, plus an `.srt`. No GIF.
- Intro cover about 1.5 s (also a still PNG, used as the Short's thumbnail), end card 3 s, both in
  portrait layout.
- About 15 s after the cover; playback sped up by 10 % over the capture.
- Portrait VS Code window (about 900x1600 logical px, scaled to 1080x1920): sidebar, panel and
  minimap hidden, one pane at a time (source or preview, cut between them). Preview zoom 140 %,
  Margin width.
- One idea per screen; at most one zoom per video, at most 1.2x.
- Subtitles: big (about 64 px), at most two short lines, upper third, never over the block shown.
- Platform safe zones: no text in the bottom 20 % and the right 12 % of the frame.
- **Cover and end card are centred on the frame (x = 540).** Respect the safe zone by narrowing
  the text block symmetrically (about 130 px margin on both sides), never by shifting it left.
  Take 2's portrait cover was off-centre (centred near x = 470) because the right safe zone was
  subtracted from one side only (user, 2026-10-29).
- Track C motion design, cream theme unless the scene says otherwise; no music, no voice.
- Same fictional demo documents as the horizontal series.
- Take 2 of S1 (2026-10-29): user found the first take 2 draft TOO SLOW. **Pacing rule from now on: playback is sped up by 21 % over the capture (x1.1 for the first 10 % and x1.1 again, so SPEED = 1.21 in the compose scripts)**; the cover (1.5 s) and the end card (3 s) keep their normal length; burned subtitles and the .srt are retimed to the sped-up take. Result: s1-v.mp4 1080x1920, about 22 s with cover and end card. The scenario tables list capture-time beats, so plan about 17 % less on screen than the beat times say. Known product findings from this take: sticky section header shows `#` markers (intended behaviour, to be locked in a requirement; a long heading wrapping to two lines is P3 sticky-heading-long-title-wraps); in Auto width a table wider than the pane does not scroll sideways (P3 candidate).

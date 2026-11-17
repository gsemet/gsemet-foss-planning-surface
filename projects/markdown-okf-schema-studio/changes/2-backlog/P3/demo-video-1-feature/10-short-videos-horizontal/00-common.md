# Storyboard, common rules: short videos, horizontal series

Status: scenario draft for review with the user, 2026-10-28. Capture comes after the scenario is
agreed.

## Purpose

A series of short videos, each one showing one feature and **why** it matters. They go into the
README, the release post and social posts. The lesson from the first three tracks: viewers saw
what the Studio does, not why. Each video therefore opens with the problem, in one subtitle.

## Common rules

- **Format: horizontal 1920x1080** (README, talks, one-off demos): source and preview side by
  side. The vertical series for Shorts and X has its own scenarios and capture:
  [../10-short-videos-vertical/](../10-short-videos-vertical/00-common.md) (user, 2026-10-28).
- H.264 `yuv420p`, plus a GIF ≤ 10 MB (horizontal) and an `.srt`.
- **Intro cover** (about 1.5 s, also exported as a still PNG for the thumbnail): logo, the video's
  title, "Markdown OKF-Schema Studio". Same art direction as the end card.
- Length: about 15 s after the cover. **Playback sped up by 10 %** over the captured take (user,
  2026-10-28: the first take's pace was right, a little faster is better).
- Real VS Code window (track B setup: throwaway profile, `.vsix` from the branch, neutral
  workspace), Cream theme unless the scene says otherwise. Preview zoom at 125 % so the text
  reads at video size; source pane narrower than the preview.
- Editing in the track C style: soft cuts, a 3 s end card, kinetic but calm subtitles.
- **At most one zoom per video, at most 1.4x, held at least 3 s.** Every video starts wide so the
  viewer knows where they are.
- Subtitles: at most two lines, they say the why, not a description of the frame. They never cover
  the content being shown and never jitter during their animation.
- Slow cursor (no teleporting), click ripple, typing sped up beyond a few words. The cursor
  avoids the floating toolbar unless the scene uses it.
- End card (3 s): logo, "Markdown OKF-Schema Studio", "Free on the VS Code Marketplace".
- No music; no voice.
- Demo content: neutral fictional project. Mermaid node labels short (labels are clipped in the
  real webview until backlog P2 `mermaid-labels-clipped-in-webview` lands); prefer compact
  diagrams that fit the frame (`flowchart LR`, short sequence diagrams).

## Take log

- Take 1 of S1 (2026-10-28, branch `change-requests/170-demo-video-s-assets`): rendering
  "nickel" (user). Too simple a page; preview text small; tall Mermaid never fully visible;
  sticky section header shows `#` markers (intended behaviour, to be locked in a requirement); first subtitle jitters
  and covers source lines; floating toolbar unrolls when the cursor passes.
- Take 2 of S1 (2026-10-29): user found the first take 2 draft TOO SLOW. **Pacing rule from now on: playback is sped up by 21 % over the capture (x1.1 for the first 10 % and x1.1 again, so SPEED = 1.21 in the compose scripts)**; the cover (1.5 s) and the end card (3 s) keep their normal length; burned subtitles and the .srt are retimed to the sped-up take. Result: s1-h.mp4 1920x1080, about 20.5 s with cover and end card. The scenario tables list capture-time beats, so plan about 17 % less on screen than the beat times say. Known product findings from this take: sticky section header shows `#` markers (intended behaviour, to be locked in a requirement; a long heading wrapping to two lines is P3 sticky-heading-long-title-wraps); in Auto width a table wider than the pane does not scroll sideways (P3 candidate).

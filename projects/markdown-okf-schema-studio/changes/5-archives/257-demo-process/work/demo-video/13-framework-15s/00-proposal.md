# 15-second video and framework: proposal

Status: draft for the owner's review, 2026-11-03. Nothing is captured yet. Once agreed, the identity
and the rules below become the guide under `docs/demo-video/`, and every later video follows them.

## Key messages

1. What your agent writes becomes a beautiful page: diagrams and cards, no configuration.
2. You read, comment and edit in the same place.
3. You answer your agent from the page.

## What the earlier takes teach

Reviewed from the contact sheets of tracks A, B, C and short S1 take 2, not from watching the videos.

| Take | Keep | Drop |
| --- | --- | --- |
| A, scripted headless | Cream title and end card, calm pace | Headless harness page instead of real VS Code |
| B, real VS Code | The real product, source next to the page | Navy cards, zooms that cut lines of text |
| C, Remotion | Best finish: green cards, kinetic captions, key badges, camera moves | Captions over the content |
| S1 take 2 | One idea, opens from the agent's Markdown, realistic document | 20 s long, no comment, edit or choice |

Across all four:

- Three unrelated looks: green, navy and Cream.
- A, B and C are feature tours of about ten scenes. Only S1 tells one story.
- A, B and C still say "1.0".
- None shows the reader answering an agent, so message 3 needs new footage.

## Production technique

Capture a real VS Code window with the CDP screencast (track B), and compose with Remotion (track C).
This is also the direction of the `record-demo-video` spec in P4 and of the chapter showcase rules.

The trial of 2026-11-04 confirmed the chain on panels 1, 2, 3, 6 and 7: scripts and result in
[trial/](trial), video in `trial/remotion/out/trial.mp4`. What it settled:

- `--force-device-scale-factor=2` gives 2880x1620 frames, sharp enough for a 1.4x zoom.
- The profile path must stay short, or VS Code does not start with the debugging port.
- The capture profile uses auto save, so that "Saved in the file" is true on screen.
- The screencast delivers about 15 to 17 frames per second, resampled to 30 fps; to check on fast motion.
- The cursor is not in the screencast: it is drawn from the recorded track.

## Visual identity

Chosen by the owner on 2026-11-04: the green of track C's first card, then a white VS Code with the
preview in Cream.

| Element | Rule |
| --- | --- |
| Cards and stage | Green radial gradient of track C: `#11707F`, `#0D5360`, `#082F37` |
| Window | Real VS Code, light theme, floating on the green stage, rounded corners, soft shadow |
| Preview | Cream theme, paper `#F5F1E8` |
| Text on green | White; subtitles in pale green `#D6EBEE` |
| Accent | Orange: `#F2822B` for lines and dots, `#FFB06A` for accent words (bold in the storyboard) |
| Typography | The sans font of track C's cards |
| Caption | Under the window, on the green stage, never over the content; 3 to 6 words, words spring up one by one |
| Callout and key badge | Track C's green pill and dark keycap, used sparingly |
| Cursor | Smooth, slightly enlarged, one ripple per click |
| Camera | A few zooms, at most 1.4x, eased over 0.6 s; a zoom never cuts a line of text |
| Cuts | 0.3 s crossfade; each shot starts still for 0.3 s, then one action |
| Sound | Silent master; the video must work muted |
| Formats | 1920x1080 master, 30 fps, H.264 `yuv420p`; vertical cut and GIF derived from it |

## Scenario

The panels, their timing and every text are in [01-storyboard.md](01-storyboard.md), which the owner
edits directly.

## Demo document

The full text is in [demo-document.md](demo-document.md). It extends the 1.3 hero fixture
(`test/visual/fixtures/80-release-1-3-showcase.md`), already written as a plan an agent would produce.

## Content rules for every video

- The document is one an agent would really write, with real sentences and real numbers.
- It has a decision or a stake, not a syntax catalogue.
- Fictional, with no personal or employer data.
- It fits the window: no scrolling through dense pages.
- Every rendered block is checked at video size: readable, not clipped.

## Message checklist

Before a video is approved, a person who does not know the product watches it once, muted, and:

- can say what the product does in one sentence;
- can name each key message of the video;
- reads every caption without pausing;
- sees the product name and where to get it.

## Open points

- The word "Answer" in the third caption: the click changes the file, and the agent reads it the next
  time it opens the file. No live link to the agent is shown or implied.

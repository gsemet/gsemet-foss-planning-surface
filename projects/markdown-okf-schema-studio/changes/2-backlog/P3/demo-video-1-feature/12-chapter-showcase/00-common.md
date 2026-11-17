# Storyboard, common rules: chapter showcase (one dynamic demo)

Status: scenario draft for review with the user, 2026-10-31. Capture comes after the scenario is
agreed.

## Purpose

One lively product demo, about 75 s, for the README, the Marketplace page and X. It shows what the
Studio does, chapter by chapter, at a rhythm the viewer can follow. It complements the demo
presentation ([../11-demo-presentation/](../11-demo-presentation/00-common.md)), which tells the
why.

## Reference (user, 2026-10-31)

[Burke Holland's Markdoc demo on X](https://x.com/burkeholland/status/2108253428652581220), 81 s,
1920x1080. What makes it dynamic is the **rhythm**, not the speed:

- A **chapter card** opens each chapter: a large serif title with one word in the accent colour
  ("Real-time **collaboration**"), a one-line subtitle, progress dots (`● ○ ○ ○ ○`).
- Then **2 or 3 shots of 3 to 5 s**. The app window floats on the plain background with a soft
  shadow. A **caption** of 3 to 6 words sits under the window ("Accept it in one click").
- **One small document** from start to end, so the viewer follows changes, not content.
- Every action is real and readable: visible cursor, live typing, dialogs, one click per result.
- Plain end card: logo, tagline, one URL.

Take 3 of the vertical short went the other way (a dense page scrolled fast) and was hard to read.

## Common rules

- 1920x1080, 30 fps, H.264 `yuv420p`, 70 to 80 s. Silent master; music optional (royalty-free,
  source and licence recorded). A 15 s cut-down (chapters 2 and 3 only) and a GIF ≤ 10 MB.
- **Stage:** Cream background for the whole video (the Cream theme's paper colour). The capture is
  shown as a floating window, about 80 % of the frame width, rounded corners, soft shadow; never
  full-bleed.
- **Window:** real VS Code (track B capture setup: throwaway profile, CDP screencast), sidebar,
  panel and minimap hidden, neutral workspace name. Preview zoom 130 %, Margin width. The window is
  cropped to the editor area: no title bar, no activity bar.
- **Chapter card:** 2 s (0.4 s in, 1.2 s hold, 0.4 s out). Serif title, one accent word, one
  subtitle line, progress dots for the five chapters. Same layout every time.
- **Shots:** 3 to 5 s each, at most 3 per chapter. Each starts still for 0.5 s, then one action.
  Cut between shots with a 0.3 s crossfade; the window does not move between shots of the same
  chapter.
- **Caption:** under the window, small uppercase chapter label (e.g. `EDIT IN PLACE`) above a
  3–6 word caption in serif. Fades in with the shot. Also exported as `.srt`.
- **Zoom:** at most one per chapter, at most 1.4x, eased 0.6 s, on the window only (the caption
  stays still).
- **Cursor:** smooth, slightly enlarged, click ripple. Typing at a readable speed for up to five
  words, sped up beyond that.
- **Demo document:** one file, `launch-review.md`, see
  [01-demo-document.md](01-demo-document.md). Fictional, no personal or employer data.
- **Claims:** only shipped features (README and `docs/user/`). No agent reacting to comments: the
  plugin teaches the agent what renders well, it does not join the document.

## Chapters (about 75 s)

| # | File | Chapter card | Time |
| --- | --- | --- | --- |
| 0 | [02-title.md](02-title.md) | Title | 0–3 s |
| 1 | [03-ch1-read.md](03-ch1-read.md) | A **rich** Markdown page | 3–17 s |
| 2 | [04-ch2-edit.md](04-ch2-edit.md) | Edit **in place** | 17–33 s |
| 3 | [05-ch3-review.md](05-ch3-review.md) | **Review** like a pull request | 33–47 s |
| 4 | [06-ch4-properties.md](06-ch4-properties.md) | Front matter with a **schema** | 47–59 s |
| 5 | [07-ch5-agent.md](07-ch5-agent.md) | Decide with your **agent** (radio choices, CR 214) | 59–75 s |
| — | [08-end-card.md](08-end-card.md) | End card | 75–79 s |

## Owner direction (2026-10-31)

Radio choice lists (`- (x)` / `- ( )`) are a differentiating feature: "multiple choice in
Markdown, for plans". Chapter 5 shows them; capture waits for CR 214 to be released.

## Open questions for the user

1. Chapter order: read first (the wow), or agent first (the why)?
2. Keep chapter 4 (schema properties) here, or leave it to its own short video?
3. Music: none, or a royalty-free track?

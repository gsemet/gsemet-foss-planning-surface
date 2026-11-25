## Summary

A feature clip of Export to HTML: from a page in the Dark theme, the reader clicks Export, saves `team-handbook.html`, opens it in VS Code's own browser inside the filmed window and clicks a tab. The browser shows the same themed page with its Mermaid flowchart and a working tab. One continuous shot, two captions, two marks, 1280x720 at 15 fps (MP4, WebM, GIF). No behaviour of the extension changes.

This PR stays a draft until the owner approves the storyboard ([clip.md](docs/demo-video/clips/export-html/clip.md)) and the clip.

GIF, MP4 and WebM (links move to the head at each push):

![Export to HTML clip](https://github.com/gsemet/markdown-okf-schema-studio/raw/743d2741f44228227f32e96bf0e2e1c5861675c6/docs/demo-video/clips/export-html/export-html.gif)

[MP4](https://github.com/gsemet/markdown-okf-schema-studio/raw/743d2741f44228227f32e96bf0e2e1c5861675c6/docs/demo-video/clips/export-html/export-html.mp4) | [WebM](https://github.com/gsemet/markdown-okf-schema-studio/raw/743d2741f44228227f32e96bf0e2e1c5861675c6/docs/demo-video/clips/export-html/export-html.webm)

## Deliverables

- `docs/demo-video/clips/export-html/`: `clip.md` (live storyboard), `scenario.mjs`, `stage/team-handbook.md`, the three renders, poster, contact sheet, key frames, `check.json`.
- The GIF on the "Export to HTML" section of `docs/user/toolbar.md`.

## Changes

- New clip folder, built with the existing clip kit (no kit change).
- Storyboard test case, scenario-loading test case and a site test that the toolbar page plays the clip.

## Impacts

No visual change to the extension. The docs toolbar page gains the clip.

What the clip proves: a real click on Export in a real VS Code window writes one self-contained file in the Dark mode of the page; a browser shows it with its flowchart and a working tab (the take's `run` checks and `verify`, `check.json`). What the owner judges: motion, rhythm, the loop as watched, the slow palette beat, the texts and their accent. A retake after the review is a follow-up.

The browser part was filmed with the Integrated Browser of VS Code 1.147.0; no fallback of the plan was needed.

## Autonomous decisions

- The storyboard review moves from before the take to this PR (draft until approved), a deviation from the recipe order.
- Integrated Browser in place of the Simple Browser (absent from the desktop palette of 1.147.0, which opens the Integrated Browser).
- Address typed with `http://`; the browser opens where VS Code places it; `Zoom` row added; take under `CLIP_SCRATCH=C:/okfclip`; `⇧⌘P` as one keycap; docs placement; frames `01-selected` and `02-pasted` left as the kit writes them.
- The "Exported to ..." toast is dismissed (it pauses the browser view), not kept as filmed.
- The flowchart is an `<img>` data URL; `verify` accepts it as the embedded flowchart.
- CDP port 9387 (`CLIP_PORT`) because another clip used the default.
- A thin title-bar strip remains at the top edge of the zoomed frames (cosmetic).

## Blast radius

Grade: 1. Docs and tests only; `git revert` restores the previous state.

## Test plan

- [ ] New or changed tests (storyboard, scenario loading, site clip test)
- [x] Requirements: no behaviour change (added test of SwRS-MDOKFSTUDIO-CORE-095, `just requirements-update` clean)
- [x] Changelog: no user-facing change
- [ ] Local gates: `just clip-kit-test` (26), `just check`, `just preflight`
- [ ] Review
- [ ] CI green

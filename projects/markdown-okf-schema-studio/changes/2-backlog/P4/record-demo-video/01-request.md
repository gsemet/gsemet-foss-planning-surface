# Request: record-demo-video

## Original intake

> I want to record one or several demo video scenarios to demonstrate how to use this VS Code
> extension, capturing the mouse and with a beautiful overlay to explain to the user what is going
> on, at human scale, with zoom sometimes to focus on a particular point. How would you automate
> it? I think a record-demo-video skill that would make the agent use Playwright or a screen
> recorder, but I would like your opinion, options, with pros/cons.

## Grounding facts (read-only exploration)

- The QA skill `.agents/skills/markdown-studio-exploratory-qa-claude/` launches the installed
  macOS VS Code with `--remote-debugging-port`, attaches with `chromium.connectOverCDP`
  (`playwright-core`), and drives input through CDP `Input.dispatch*` events.
- The repository has no video recording tooling (no ffmpeg, VHS, or Playwright `video` option).
- The E2E suite uses `@vscode/test-electron` (pinned, cross-platform) plus CDP real input.
- Playwright `recordVideo` is not available on a `connectOverCDP` browser context.
- Craftsman's dashboard demos use Playwright video plus an in-DOM overlay (`demo-overlay.ts`:
  fake cursor, click pulse, captions), no zoom, and `ffmpeg-static` for GIF conversion.

## Options considered

| Option | Summary | Verdict |
|---|---|---|
| A. In-DOM overlay + CDP screencast | Overlay baked into the workbench DOM | Rejected: CSS zoom breaks input, no re-captioning |
| B. OS screen recorder | avfoundation/OBS with CDP or OS input | Rejected: fragile, needs permissions; no fallback wanted |
| C. Clean capture + timeline + post-composition | CDP screencast + `timeline.json` + compositor | **Chosen**, with Remotion |
| D. Commercial tool (Screen Studio) | Manual recording | Rejected: not automatable |

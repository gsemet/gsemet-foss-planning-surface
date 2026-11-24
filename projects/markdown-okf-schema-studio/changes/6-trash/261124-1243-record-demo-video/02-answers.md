# Interview responses: record-demo-video

## Round 1

| # | Question | Answer |
|---|---|---|
| Q1 | Which output formats and destinations do the demos target? | MP4 master + short README GIFs |
| Q2 | Which capture and compositing architecture? | "Propose whatever would work" (delegated; proposal in Q6) |
| Q3 | What role should the agent play? | Agent authors scenarios + reviews output; recording is deterministic replay |
| Q4 | What narration? | Captions only |
| Q5 | Reuse the QA engine or build a separate demo engine? | Fully separate demo engine |

## Round 2

| # | Question | Answer |
|---|---|---|
| Q6 | Confirm CDP screencast + timeline + headless canvas compositor + ffmpeg? | "What is Remotion?" (reopened as Q11) |
| Q7 | How should zoom be triggered? | Explicit `focus` steps + optional `autoZoomOnClick` |
| Q8 | Where should the skill and engine live? | Studio repo first, promote to Compendium later |
| Q9 | Which VS Code runtime? | "Whatever you want" (delegated; confirmed in Q12) |
| Q10 | Stop? | No |

## Round 3

| # | Question | Answer |
|---|---|---|
| Q11 | Which compositor? | "Remotion is awesome, ensure NOT to add unnecessary packages to the VS Code extension" |
| Q12 | Confirm pinned `@vscode/test-electron` runtime? | Confirmed: 1920×1080, fixed theme + per-scenario override |
| Q13 | Which demo scenarios first? | Overview MP4 (~90 s) + GIFs: properties table, inline editing, evidence links (reopened by Q28) |
| Q14 | Caption and visual style? | Neutral VS Code-like: bottom caption pill, macOS cursor, click ripple |
| Q15 | Where to store rendered videos? | GIFs in `images/demos/` (≤3 MB); MP4 gitignored and published to site |
| Q16 | Stop? | No |

## Round 4

| # | Question | Answer |
|---|---|---|
| Q17 | How to isolate the Remotion tooling? | Nested `demos/` package, concisely explained in AGENTS.md |
| Q18 | Remotion license? | Individual license |
| Q19 | Human-scale pacing defaults? | Accept proposed defaults, applied at composition time |
| Q20 | How does the agent review output? | Timeline lint + keyframe contact sheet + size check + human approval |
| Q21 | Fit with build gates? | Out of preflight; only scenario-schema validation in `just check` |
| Q22 | Stop? | No |

## Round 5

| # | Question | Answer |
|---|---|---|
| Q23 | Spike first to validate webview screencast capture? | Spike, no fallback (no OS capture) |
| Q24 | Which content workspace? | Curated public demo workspace in `demos/workspace/`, reset per run |
| Q25 | Skill entry points? | "Focus on edition capabilities" (ambiguous; clarified in Q28) |
| Q26 | Stop? | No |

## Round 6

| # | Question | Answer |
|---|---|---|
| Q27 | If the spike fails? | Go/no-go gate; try CDP screenshot loop, else stop and report |
| Q28 | Meaning of "focus on edition capabilities"? | (a) Demos focus on the extension's editing features (reopens Q13) |
| Q29 | Stop? | Yes |

## Handoff

| # | Question | Answer |
|---|---|---|
| Q30 | Handoff option? | Option A: capture responses and generate specification |

## Decision nodes status

- Resolved: Q1, Q3, Q4, Q5, Q7, Q8, Q11 (supersedes Q2/Q6), Q12 (supersedes Q9), Q14, Q15,
  Q17, Q18, Q19, Q20, Q21, Q23, Q24, Q27, Q28.
- UNRESOLVED: Q13 (GIF list after Q28 refocus), Q25 (skill modes not confirmed).

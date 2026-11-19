# Intent

The user, 2026-11-17, during batch-23, to be grilled now and run after the batch:

- The CLI can already read the forge (the board's PRs page), but a running Chief of Staff session
  hears nothing until its next `status`: a priority changed in the board, a comment, an event in
  the UI, a merge the forge made. Find how the CLI and the session (Claude Code, or Copilot) can
  talk, so the session is told when such an event happens.
- A second mode: start a Griller directly from the board, to discuss a CR with the user. That
  Griller reads the same files as the Chief of Staff, and may need to talk with it directly.

## What exists today

- The board's PRs page reads the forge (at most once every 10 s, while the page is open) and,
  for a merge the record does not hold, appends one line to `board-seen.jsonl`; `status` prints
  it for the Chief of Staff, who records it at its next `status`. Nothing wakes the session.
- A Griller is a session the user starts (`/chantier:griller`); it sends the Chief of Staff
  `<slug> specified` (routing.md). The board never messages an agent and knows no role
  (AGENTS.md).

## Candidate channels on Claude Code (to settle in the grill)

- A background command the session watches (the `Monitor` tool, or a background shell that ends
  on the first event): one line per event wakes the session.
- A prompt hook: the events since the last turn are added when the user speaks; no wake-up.
- An MCP channel server (push into the session; research preview, CLI).
- The plugin's hooks module (`hooks/register.tsx`, which already polls files on a timer): whether
  it can wake the session is to be checked.

Copilot has none of these as far as known: events would arrive at the next turn or `status`.

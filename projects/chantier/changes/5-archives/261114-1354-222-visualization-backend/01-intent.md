# Intent: a visualization backend beside the Claude Code mod

2026-11-12, the user, in a Griller session.

## The request

The user's words (French): think about a visualization backend, as a complement to the Claude
Code mod, which does not show in remote mode.

## What exists

- **The CR board mod** (`hooks/register.tsx`, CR-108 and later): a read-only pane over the
  planning folder's `STATUS.json`, refreshed every 15 seconds. It shows on the machine running
  the session only, not in a Remote Control view (anthropics/claude-code#99217).
- **The remote board** (`chantier board`, CR-182): a standard-library web page started by the
  Chief of Staff, read-only, tied to the seat, on `127.0.0.1:8765` by default, reachable over
  Tailscale or the LAN with no password. It renders its own HTML.
- **`planning-server`** (P3): a future server owned by the Chief of Staff for an external
  surface; its constraint says any page goes into `chantier board`, one HTTP server per planning
  folder, one start and stop rule.

## Scope after the split (2026-11-13)

The user split the work into five CRs; this one is **board-server** (CR 1 of 5) and keeps the
prototype (`prototype/`, `evidence/prototype/v6-*`), the reference of all five ("the same thing
at the end"). Here: `chantier board` becomes the server; the read JSON API of the record and the
folders; one project or a multi-project surface; the random URL on the local network, printed by
the CLI and given in the chat; live refresh, costs recomputed at worst every 5 minutes;
`AGENTS.md`'s rules updated (the board writes through the CLI; the server is the named git
exception). The others, in `1-inbox/`: `board-read-views`, `cr-summaries`,
`board-backlog-edit`, `surface-autosync`. Details: `02-answers.md`, "Split into CRs".

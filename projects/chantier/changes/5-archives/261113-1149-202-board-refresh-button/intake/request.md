# Board mod: a Refresh button and the refresh period

## The user's request, verbatim (French)

> oui rajoute un bouton refresh et une note qui dit "refreshed every ..." dans une autre CR a part

Context (Chief of Staff, 2026-11-12): the user asked how often the `/chantier-board` pane refreshes
and how to force it. Today the mod checks every 15 s (`EVERY_MS = 15000`, `hooks/register.tsx:24`)
and reads `STATUS.json` again only when its modification time changed; the header shows
"read Ns ago". The only way to force a check is `/chantier-board` twice (hide, then show), which
runs `begin()` and an immediate `check()`.

## Summary (English)

1. **A Refresh button** in the board pane: it runs a check at once, without hiding the pane.
2. **A note** in the pane saying how often it refreshes, e.g. "refreshed every 15 s", next to the
   existing "read Ns ago".

A separate CR from `boot-mode-by-surface` (the README and the mod's docs). A change to `hooks/`
passes `just mod` before its PR (AGENTS.md).

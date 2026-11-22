# Board key survives several boards and a lost cookie

The user, 2026-11-22: on iOS Safari the board's first visit works, then a later refresh shows "this board needs the link with its key". The user may have several boards open at once, on the same surface or on others, and it must work.

Known: the key goes into a 30-day HttpOnly cookie named `chantier_board`, the same name for every board; cookies ignore the port, so a second board on the same host overwrote the first one's cookie. CR-456 (batch-30) names the cookie per served folder (`chantier_board_<sha12>`), which fixes that case.

Left for this item:
- Prove it end to end: one browser, two or three boards of different surfaces on one host (different ports), plus several tabs of one board; each keeps working across reloads and restarts of the others.
- The refusal page: when the cookie is missing, offer to paste the key (or the link) instead of a dead-end error, so a home-screen web app, a private tab or a cleared jar recovers without asking the Chief of Staff.
- Check iOS Safari's handling of `SameSite=Strict` when the link is opened from another app; relax to `Lax` if it drops the cookie there.
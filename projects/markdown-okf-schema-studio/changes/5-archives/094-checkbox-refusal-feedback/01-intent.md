# Preview checkboxes: silent refusal, stuck busy state, misleading standalone message

User decision (2026-10-24): fix, P3.

Current behaviour (gfm scope, F-GFM-027 and neighbours, specified as-is with "Known issue"):

- When the host refuses a toggle (stale text, moved line, inline editor open, read-only file), the
  box reverts and the reason is shown only as a tooltip (`src/page/features/checkboxes.ts`).
- A malformed toggle message is dropped by the host with no result posted
  (`src/session/pageMessages.ts`, `src/session/features/sourceEdits.ts`). The box stays busy and
  ignores clicks until the next render.
- A standalone file (opened outside any folder) is refused with "Editing requires a trusted
  workspace", although the cause is the missing folder, not trust.

## Expected

- The host always answers a toggle, including a malformed one, so the box never stays busy.
- The refusal reason is visible next to the box for a short time, not only on hover.
- The standalone message names the real cause.
- Session test for the malformed-message answer, page test for the visible reason, and the gfm
  SwRS updated (or superseded) in the same change.

Requirement ids older than the baseline merge map to their current tile in `.agents/changes/archives/059-requirements-okfreq/reduction/mapping.csv`.

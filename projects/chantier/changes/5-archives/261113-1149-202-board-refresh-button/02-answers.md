# Answers: the board's Refresh button and refresh period

Grill of 2026-11-12. The user's word that day: "fait toutes les P1 et P2 en terminant sur la
release. pour la plupart je ne pourrais pas te repondre, utilise un advisor Fable. demande moi
uniquement quand il y a un impact utilisateur". The advisor answers in the user's place; the
questions with user impact are under "Open for the user", each with a recommendation, not decided.

- Q: Does Refresh do more than read the files again (price the batch, run `status --refresh`, call the CLI)? — Advisor (Fable, answering in the user's place on the user's word of 2026-11-12): no. The pane stays read-only: it writes nothing and runs no process but `git rev-parse`; the batch's cost is the steering session's to refresh. The docs say so, since a user will expect the cost to move.
- Q: Does a press keep what the user was looking at? — Advisor (Fable, answering in the user's place on the user's word of 2026-11-12): yes: the pane stays open, the page shown (a CR's sheet, a document) and the folds stay. Losing the page is what makes hide-then-show a poor way to force a check today.
- Q: Does a press also look for the planning folders again (a project added to a surface, a `.agents/changes/` created after the pane opened)? — Advisor (Fable, answering in the user's place on the user's word of 2026-11-12): yes. It is what hide-then-show does today, and "No chantier status here" is a moment where the user presses it.
- Q: Does the periodic check change (period, what it skips)? — Advisor (Fable, answering in the user's place on the user's word of 2026-11-12): no: 15 seconds, and a file is read again only when its modification time changed. The request is a button and a note, not a new rhythm.
- Q: Is the period configurable? — Advisor (Fable, answering in the user's place on the user's word of 2026-11-12): no. Nobody asked, and `chantier.yaml` holds no setting of the mod; the note prints the same constant the timer uses, so the two cannot drift.
- Q: Does the remote board (`chantier board`) get the same button and note? — Advisor (Fable, answering in the user's place on the user's word of 2026-11-12): no, out of scope. The user spoke of the `/chantier-board` pane, and a browser has its own reload.
- Q: A press while a check is already running, or repeated presses? — Advisor (Fable, answering in the user's place on the user's word of 2026-11-12): harmless and unthrottled: a check only reads a few local files. A failure shows in the board's existing note line, as for the periodic check.
- Q: Does this CR wait for `boot-mode-by-surface` (both touch `docs/boards.md`)? — Advisor (Fable, answering in the user's place on the user's word of 2026-11-12): no; no `depends.json` for a shared file. This CR changes the one sentence on refreshing; the second to merge rebases. Screenshots taken before this CR will lack the button, which the docs page may say or retake later.
- Q: Which gates? — Advisor (Fable, answering in the user's place on the user's word of 2026-11-12): `just mod` (run by the agent itself; it stops if it cannot) and `just check`; new tests in `hooks/register.test.tsx` for the press and the note. This is `AGENTS.md` for a change under `hooks/`.

## Open for the user

1. **Where the button sits, what the note says, what a press shows.** Recommended:
   - one **Refresh** button at the top of the pane, on every view: above the header line on the
     board, beside "< Back" on a CR's sheet or a document, and on the one-line views ("No chantier
     status here ...");
   - a press reads the files again **even when unchanged**, so the header returns to "0s ago":
     without that, a press on a quiet batch changes nothing on screen and the button looks dead;
   - the header keeps one line and one wording: `5 live · 0 waiting for you · read 45s ago ·
     refreshed every 15 s` becomes `5 live · 0 waiting for you · checked 3s ago, every 15 s`.
     Reason: today "read Ns ago" is the age of the last time the file *changed and was read*, so
     it shows 45 s although a check ran under 15 s ago; beside "refreshed every 15 s" it would
     read as a bug. The alternative is the user's literal wording, "read Ns ago · refreshed every
     15 s", with the age reset at every check.

- Q: (open) The button's place, the note's wording, what a press shows? — User (2026-11-12, "board-refresh-button: ok, en haut a droite si possible"): the advisor's recommendation (one Refresh button on every view of the pane; a press re-reads even an unchanged file, so the age returns to 0; header `... - checked 3s ago, every 15 s`), with the button at the top right of the pane where the mod's layout allows it.

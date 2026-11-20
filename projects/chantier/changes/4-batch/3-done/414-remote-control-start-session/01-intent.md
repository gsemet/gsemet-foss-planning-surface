# Intent

The user, 2026-11-20: encode in the Claude Code host reference how to start sub-sessions so that
it always works, even from Remote Control. The user wants it before the next evals, so that the
evals can be launched remotely: "on va d'abord faire remote-control-start-session, pour controller
comment lancer les evals meme en remote".

## What is proved (2026-11-20, Battlestation, the user on Remote Control)

| Start from a session driven by Remote Control | Result | Seen by |
| --- | --- | --- |
| `start_session` with `cwd` (the planning surface; the eval root) | refused: "The user is working over Remote Control, and this turn can't start that session" | Studio's Chief of Staff (twice), chantier's Chief of Staff (eval root) |
| `start_session` with a saved `preset` ("Battle Station") | refused, same message | chantier's Chief of Staff |
| `start_session` with no `cwd`, `use_worktree: false` | started, in the steering session's own folder (its main checkout, `--git-dir` = `--git-common-dir`) | Studio: two Grillers and the batch-07 Foreman (Sonnet 5.5, effort medium), which claimed its batch and started a Driver; chantier: session `local_9ef60aad-22ce-4ab4-9dd6-80cf84213736` |
| The session started with no `cwd` then calls `mcp__ccd_directory__change_directory` to a folder inside the trusted `Projets` tree (`C:\Users\gaeta\Projets\chantier-eval`) | granted with no question (auto mode, trusted folder); its next turn runs there (`pwd` shows it) | chantier, same session |
| The same session's context after the move | still holds the `AGENTS.md` of the folder it started in (chantier's): the move does not reload project instructions | chantier, same session |
| Clearing that session from the Chief of Staff (`clear_session`) to reload its context in the new folder | denied by the auto mode classifier; not retried | chantier's Chief of Staff |

So the classes table's row "Desktop, driven by Remote Control: Can start a session: no" and the
Surfaces table's `start_session` refusal are wrong: Remote Control refuses a start in another
place (`cwd`, `preset`), not a start.

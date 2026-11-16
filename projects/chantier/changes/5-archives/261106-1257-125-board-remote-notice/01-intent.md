# Intent

The reply of `/chantier-board` tells the user where the pane is: on the machine running the session,
and not in a Remote Control view. It says so every time, with no detection.

Mods draw on the host only, as the mods overview documents ("Where mods run"), and a mod cannot tell
when the user reads from a view: `isPlaced` and `$.session.surfaces()` answer as if the pane were
placed (anthropics/claude-code#99217), and a session the desktop app hosts records the user's
messages as `sdk`, never `bridge`. The overview names the way out: "a command's text reply where
nothing draws".

The grill is in `02-answers.md`.

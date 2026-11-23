# Long gate: webui check starts a second board on Windows

The local long gate scenario fails on Windows at surface-board: webui on a running server prints board already running starts a second board (ports differ), and the stack unit runs 769 s over its 750 s budget. Seen at 37f0cb0 for CR-465 (CI ubuntu green), after CR-463 waiver. CR-465 gate waived by the user on 2026-11-23. Fix the check or the Windows behaviour.

User words 2026-11-23 (own-gate-Q6): set up a dynamic port system: the port is incremented by 1 until a free one is found (the board, the scenario's boards and the webui check must not depend on 8765 being free, so the local long gate runs while the user's board runs). Scope: the board's start (default port 8765, then 8766, ...), webui's reuse of a running board, and the scenario's webui check.

# Board on the next free port from 8765; the long gate runs beside the user's board

Short name: `dynamic-port`. From the local long gate of CR-465 at 37f0cb0 (2026-11-23, waived by
the user), and the user's words of 2026-11-23 (own-gate-Q6).

The board's start tries its default port, 8765, then 8766, 8767, ... until one is free, whatever
holds the ones before it (another chantier board or another program). `webui` reuses the board that
runs, wherever it listens, and starts one that walks the same way. The scenario's boards and its
`webui` check stop depending on 8765 being free, so the local long gate passes on Windows while the
user's own board holds 8765.

Why: in the unit `surface-board`, the step `serve_and_webui` starts its first server with
`--port 8765`; with the user's board on 8765 it is refused, the scenario's fallback goes on, and
`webui` then finds no live server of that surface and starts a second one on another port: the
check "`webui` on a running server prints `board already running at <link>`" fails.

Out of scope: the `stack` unit's 769 s over its 750 s budget, seen once (a warning, not a failure).

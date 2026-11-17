# Flaky real-window suite: `--reload-only`

Seen by CR 048 (2026-10-23): one unexplained failure in 8 isolated local runs of the real VS Code
`--reload-only` suite on macOS (after the window-focus fix). Find the cause (CI rule 12: no retry,
no longer timeout), prove it with the stress mode (20 rounds) locally and in the manual heavy CI job.
Also re-check the slash-menu step guarded by CR 048 (timeout not reproduced in ~15 runs, cause unproven).

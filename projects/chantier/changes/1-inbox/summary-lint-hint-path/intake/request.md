# The summary lint hint gives a path summary set can read

A spec-writer reported: `summary lint` prints the CR path relative to the project root, while `summary set` reads it relative to the planning folder, so the printed hint fails ("not a CR folder: .agents/changes/.agents/changes/..."); the absolute path worked. Code: `commands/summary.py`, `_gap_line` against `_cr_folder`. First step: reproduce it.

Filed 2026-11-15 by the Chief of Staff from the open questions of the specs of the post-batch-18 fixes, as a Fable advisor sorted them (later, not for this release).

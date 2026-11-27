# TUI: resize the columns with the mouse and keep the widths

Split from `tui-resize-columns` (the CR it comes from) on the owner's answer, 2026-11-27, tui-widths-Q1: « A. Deux CR (recommandé) ». The owner's request, verbatim, is in `1-inbox/tui-resize-columns/intake/request.md` (or where that CR has moved).

## Wanted

1. The user resizes the main columns of `chantier live` (the left column, the central column and the right column) with the mouse, by the existing panel borders; not the columns inside the central one (the owner's correction, tui-mouse-Q1, in `02-answers.md`).
2. The sizes are kept in a JSON file in the user's configuration folder, found with the `platformdirs` library (a new dependency).

The wider default widths and the narrow-terminal rule are `tui-resize-columns`, which this change request follows in the stack. Its specification before the split, and the spec critic's findings on it (the Windows mouse support not proved; `AGENTS.md` says `live` writes nothing), are the material for this one.
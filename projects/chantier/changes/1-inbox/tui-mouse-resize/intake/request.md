# TUI: resize the columns with the mouse and keep the widths

Split from `tui-resize-columns` (the CR it comes from) on the owner's answer, 2026-11-27, tui-widths-Q1: « A. Deux CR (recommandé) ». The owner's request, verbatim, is in `1-inbox/tui-resize-columns/intake/request.md` (or where that CR has moved).

## Wanted

1. The user resizes the three columns of `chantier live` with the mouse: the left column (Projects and Agents boxes) and the Flow's Project and Who columns.
2. The sizes are kept in a JSON file in the user's configuration folder, found with the `platformdirs` library (a new dependency).

The wider default widths and the narrow-terminal rule are `tui-resize-columns`, which this change request follows in the stack. Its specification before the split, and the spec critic's findings on it (no drawn edge between Project, Who and Event; the Windows mouse support not proved; `AGENTS.md` says `live` writes nothing), are the material for this one.
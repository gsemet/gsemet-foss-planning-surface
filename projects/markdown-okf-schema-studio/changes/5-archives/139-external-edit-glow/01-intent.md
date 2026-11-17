# An edit applied by another tool to the active document never glows

Left over from the lifecycle small fixes (PR with the other three fixes). Specified as-is with a
Known issue in SwRS LIFE-094: an edit applied by another tool to the active document counts as
typing, so the update glow never shows. VS Code does not say who made a change and the host only
knows the cursor line, so any heuristic risks glowing while the writer types.

## Expected

Decide a rule that separates a foreign edit from typing (for example a change whose range does not
contain the cursor, or a change fired outside a recent keystroke window), implement it behind the
host port, test with a simulated foreign edit, and remove the Known issue line of LIFE-094.

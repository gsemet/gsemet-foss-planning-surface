# TUI: Tab zones, navigation, newest first, compact times, maximize

TUI (`chantier live`): Tab switches the active zone, arrows and Page Up/Down navigate the panel, the main zone is sorted newest first, relative times lose horizontal space, a shortcut maximizes the active panel.

From the user, 2026-11-24, for the running batch directly (no grill):
- Tab changes the active zone.
- Up, down, Page Up and Page Down navigate inside the active panel.
- The main (central) zone is sorted anti-chronologically (newest first).
- The point of the relative "x min ago" form is to gain space: avoid losing much horizontal space with the time column, so recompute its width (a narrow, right-aligned relative time).
- A shortcut maximizes the active panel (and restores it).
- The default active panel is the central one.

Scope: `skills/chantier/scripts/cli/src/chantier/clients/tui/` only; the TUI reads the surface server's published API and writes nothing (AGENTS.md). Keep its tests and any doc of its keys true.

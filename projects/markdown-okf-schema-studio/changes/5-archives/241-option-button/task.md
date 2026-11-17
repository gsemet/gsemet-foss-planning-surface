# Task: Toggle option button and option list continuation

## Files (start here)

- `src/page/features/checkboxes.ts`, `src/page/modules/editActions.ts`,
  `src/page/modules/blockEditActions.ts`: how "Toggle checkbox" and the task-list Enter
  continuation work; mirror them.
- `src/core/render/radioMarkers.ts`, `src/core/render/radioGroups.ts`: the option list syntax.
- The toolbar definition of the edit palette (search "Toggle checkbox").

## Change

Add the toolbar button (icon consistent with the checkbox one), the Enter continuation and the
empty-item exit. GFM and MyST palettes alike if both show "Toggle checkbox".

## Tests first

- Unit/page tests that fail today: the button toggles lines to `- ( ) ` and back; Enter after
  `- ( ) titi` yields `- ( ) `; Enter on an empty `- ( ) ` ends the list.
- e2e scenario in group `palette-slash` (simulated).

## Requirements

New or updated SwRS in scope `palette-slash` (new ones `proposed`), markers per `rules.md`. The
writing skill lists toolbar features: update it if it names the checkbox button (constitution,
section 6).

## Gates (foreground)

- `just check`
- The e2e group touched, simulated (no real VS Code window).
- `just requirements-update`

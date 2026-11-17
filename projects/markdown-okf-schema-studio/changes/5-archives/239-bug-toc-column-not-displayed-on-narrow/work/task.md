# Task: TOC rail on narrow viewports

## Files (start here)

- The TOC column and its breakpoint: search `src/page` and `src/core/preview/previewStyles` for
  the TOC (`toc`), the narrow breakpoint and the toolbar toggle state.
- `src/page/modules/widthMode.ts` (width modes and narrow pane handling).

## Change

Below the breakpoint where the TOC column is hidden today, with the toggle on: draw the rail and
the overlay as `00-request.md` decides. Accessible: the rail is focusable, the overlay is a
navigation landmark, Escape closes it. Respect `prefers-reduced-motion`.

## Tests first

- Page test that fails today: narrow viewport + toggle on → the rail exists; hover/focus opens the
  overlay; Escape and leave (after 300 ms) close it; a click navigates.
- e2e scenario in group `toolbar-navigation` (simulated), light and dark screenshots, narrow pane.

## Requirements

Update the TOC SwRS of scope `toolbar-navigation` (known issue today), markers per `rules.md`.

## Gates (foreground)

- `just check`
- The e2e group touched, simulated (no real VS Code window).
- `just requirements-update`

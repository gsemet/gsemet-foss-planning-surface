# Task: text shortcuts in the find bar fields

## Files (start here)

- `src/page/modules/findBar.ts`: `barKeydown` (around line 536) and the window capture listener
  (around line 649).
- Find which other page listener eats Cmd/Ctrl+A (and the other shortcuts) while focus is in a find
  bar field: page-level select-all or block selection, the edit palette, the host webview key
  forwarding. Search `src/page` for `KeyA`, `selectAll`, `"a"` key handlers.

## Change

Shortcuts typed in the find or replace field act on that field only. The smallest change wins:
prefer making the offending listener ignore events from the find bar (or text fields in general)
over re-implementing shortcuts.

## Tests first

- A page/unit test (jsdom) that fails today: Cmd/Ctrl+A in the find field selects the field text
  and does not trigger the page action; same for the other shortcuts that a page listener handles.
- An e2e scenario in group `toolbar-navigation` (simulated, `test/` e2e harness) if the bug needs
  the webview to show.

## Requirements

Update or add the SwRS of the find bar (scope `toolbar-navigation`): the fields keep their native
editing shortcuts. Markers per `rules.md`.

## Gates (foreground)

- `just check`
- The e2e group touched, simulated (no real VS Code window).
- `just requirements-update`

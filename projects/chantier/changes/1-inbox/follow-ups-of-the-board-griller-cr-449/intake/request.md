# Follow-ups of the board Griller (CR-449)

Follow-ups found while shipping CR-449 (a Griller started from the web board):
- The `summary set --title *` allow rule also matches a trailing `--project`; tighten it.
- The Grill button reuses the `data-key` card-key attribute; give it an attribute of its own.
- The web client's tests only grep file text; add a test that runs the client code.
- The i18n strings put backticks around {cli}, {model} and {command}; they render literally in the panel.
- Rename BOARD_COMMAND in js/panel/griller-view.js to `serve` when CR-456 merges.
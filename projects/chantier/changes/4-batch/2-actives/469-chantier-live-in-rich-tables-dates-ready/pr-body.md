## Summary

`chantier live` is redrawn with Rich: rounded boxes, tables with headers, the board's state colours, local-zone times with the date, the key `t` (time since the event), an Agents box, and a Ready box above Tasks fed by the server's `prs` topic (clickable PR numbers by OSC 8). `--once` stays plain text.

## Deliverables

- `clients/tui/` (`model.py`, `screen.py`, `view.py`, new `parts.py`, `ready.py`, `times.py`), `commands/live.py`
- tests: `test_live_model.py`, `test_live_link.py`, `test_live_ready.py`
- docs: `docs/boards.md`, `docs/server-api.md`, `scenario/README.md`

## Known gaps

- Hand check on Windows Terminal (rounded boxes, colours, `t`, clickable PR number) not done yet.

## Review

- [ ] Inspector

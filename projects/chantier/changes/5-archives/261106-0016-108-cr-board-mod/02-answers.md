# Answers

Given by the user on 2026-11-06, in the Chief of Staff's session.

- **Trigger:** loading the chantier skill opens the board and never closes it. A separate command,
  `/chantier-board`, opens and closes it.
- **Data:** the CLI writes the index; the mod does not scan folders.
- **Index:** extend `3-requests/STATUS.json` with the landed and dropped CRs. No new file.
- **History:** the last 50 of each, with the total.
- **Links:** a document opens inside the pane, as Markdown, with a way back.
- **Place:** in the chantier plugin, `hooks/` at its root.
- **Layout:** one column of sections; the live ones open, the others folded.
- **Top of the board:** a line of numbers, then what waits for the user. Empty, it says so.
- **A CR clicked:** a sheet from its `STATUS.json`: the steps as a line, now and next, cost, PR,
  documents, a way back.
- **Backlog:** grouped by priority, folded, with counts. No search field.
- **A live CR's row:** round and step, PR and cost, branch and silent time. Not the last note.
- **Several open batches:** one section per batch.
- **Foreman silent:** an alert among what waits for the user.
- **Pane closed:** nothing runs, nothing alerts. No status line, no toast.
- **Surfaces:** the same rendering everywhere, with the elements all surfaces share; no SVG.
- **Delivery:** a chantier CR, so chantier is tested on itself.
- **Specification:** approved on 2026-11-06, with these choices: each batch's section starts with
  its own "Waiting for you"; the Foreman counts as silent after 20 minutes; `claude plugin
  validate` and `test` stay required, run with the session's own binary: `claude` need not be on
  the `PATH`.
- **Limits from the request:** read-only; generates nothing; checks every 15 seconds only while
  the pane is open, and re-reads a file only when it changed; from a worktree it finds the main
  checkout's files; with no file, it says so in one line.

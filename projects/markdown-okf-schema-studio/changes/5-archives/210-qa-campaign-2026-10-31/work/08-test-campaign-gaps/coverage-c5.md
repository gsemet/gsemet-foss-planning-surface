# Coverage C5 — Table toolbar and cell editing (partial)

Exercised (session c5, ws-c5):
- synth/tables.md: toolbar row/column insert and delete on the aligned table (diff vs mark: only the
  table lines, alignment row preserved), toolbar inViewport and noClip, Tab then Escape (typed text
  discarded, buffer unchanged), escaped-pipe code cell edit (one line, `\|` preserved).
- 06-guidelines-governance.md (real chapter): cell edit with bold/code/cite/link neighbours, Tab x3
  then Enter (one line changed), insert column before on a 5-row table (7 lines, expected).
- synth/c5-tables.md (new fixture): wide pipe table (finding c5-1), cell with code and bold, link
  cell, list-table and csv-table (a list-table cell click opens the whole-block source editor, no
  table toolbar; csv-table renders, not edited).
- Observation: heading fold state persists per document in the webview, so a fold left closed by an
  earlier run hides all tables on the next preview open (by design, cost a few calls).

Not exercised: alignment buttons and row move (no alignment button in the toolbar; row handles and
tableRowMove untested), Shift+Tab, tables in vault notes, 02-foundations tables, narrow vs wide
width modes, Convert to list-table / pipe table, undo after structural edits.

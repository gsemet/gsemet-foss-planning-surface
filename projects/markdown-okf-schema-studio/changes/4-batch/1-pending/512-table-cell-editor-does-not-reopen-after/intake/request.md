# Table cell editor does not reopen after a pasted fill (TABLE-120)

# Table cell editor does not reopen after a pasted table fill (TABLE-120)

While filming the paste-spreadsheet-cells clip (CR-489), the table is filled correctly by a paste through CDP (Task, Owner, Due, 4 rows), but the cell editor does not reopen on the "Task" cell, as TABLE-120 says it should. It happened in 3 of 3 runs, also after Ctrl+A first. The real-input integration test passes the reopen check, so this may only be an artefact of CDP-driven input; it is not established. Decide: reproduce with real input in a real window; if it is a bug, fix it; if it is a CDP artefact, record that in the requirement or the clip guidelines.

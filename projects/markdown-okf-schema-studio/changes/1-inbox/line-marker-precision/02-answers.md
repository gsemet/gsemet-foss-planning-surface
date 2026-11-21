# Line marker: table row, hidden tab-set item, front matter row

See intake/request.md.

## Grill, 2026-11-21 (owner's answers, asked by the Chief of Staff)

- lm-Q1 (scope). Owner: "Les 3 ensemble": one CR for the table row, the hidden {tab-item} (selected first, like an unfold) and the front matter property row (else the top of the properties table). The marker is CR-445's (merged in v1.11.0).
- Owner, 2026-11-21: "Et tout ça partira dans le batch en cours": once final and ready, added to the running batch-07.

## Owner's answers, 2026-11-21 (Fable spec critic's questions)

- lm-Q2 (where the arrow sits once a hidden tab is shown). Owner: "Sur la ligne exacte": on the exact paragraph or code line inside the tab, as everywhere else; the renderer gives line data inside a tab item without changing how a click edits the tab (MYST-098).
- lm-Q3 (a pipe table inside a quote, an admonition or a list item). Owner: "Oui, dans ce CR": the renderer gives these tables their lines and the marker goes on the row.
- Settled by the Chief of Staff from the critic: {list-table}, captioned {table} and raw HTML tables keep the top of their block (CR-445 decision 31); a table in a tab item gets its row via lm-Q2; selecting a tab switches its sync group as a click does (MYST-099, record chosenSync); nested tab sets: every hidden tab around the line is selected; a collapsed properties table expands on the request only (like an unfold, FMSCHEMA-090); a tab the reader leaves (keyboard or sync group) hides the marker until it shows again (LIFE-179 folded rule), and a keyboard tab change triggers a new placement.

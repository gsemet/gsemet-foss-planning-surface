# Show the target-line arrow in the side preview on a jump

See intake/request.md.

## Grill, 2026-11-21 (owner's answers, asked by the Chief of Staff)

- jm-Q1 (which marker). Owner: "Comme l'onglet Studio": the same arrow in the left margin and the same light band, same duration, reusing the marker of CR-445 open-at-line-marker (merged in v1.11.0); only on a jump, never on a cursor move.
- Owner, 2026-11-21: "Et tout ça partira dans le batch en cours": once final and ready, added to the running batch-07.

## Owner's answers, 2026-11-21 (Fable spec critics' questions)

- jm-Q2 (anchor off). Owner: "Défiler et marquer": on a jump the side preview scrolls to the line and marks it, even with "scroll preview with editor" off.
- jm-Q3 (moves VS Code cannot tell from a search click: F3, F8, Go to Symbol, Go Back, VSCodeVim j/k). Owner: "Tous marquent": all mark; Vim is a written known limit; trial J1 first records what VS Code really reports.
- jm-Q4 (a search click with a replace text opens the replace preview, asked in side-preview-diff-gaps). Owner: "Oui, sur le vrai fichier": the side preview marks that line of the real file, if the jump can be detected on a diff side; this CR stacks after side-preview-diff-gaps.
- Settled by the Chief of Staff from the critic (follow from "Comme l'onglet Studio" and CR-445's rules): every Command move with one selection marks (Go to Line and Quick Open :line are jumps); with the anchor on the editor leads (no own scroll to the reading line); scroll and cursor moves keep the marker, an edit of the document or a switch to another document removes it; only the following side preview marks; no setting; the side preview's own links mark the target line (Back/Next in the same document do not); caret mark and marker both show; a hidden side preview gets the line at its next page ready within the 5 s window, else dropped, and the line is posted only to a visible page.

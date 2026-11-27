Destination: next batch (3-ready).
Spec critic: yes: what the user sees, a new dependency and a rule of AGENTS.md.
Short name: `tui-mouse`

## Answers

1. « fait un batch stack et rajoute la CR du TUI qui elargie les colonnes je ne sais pas ou elle est » (2026-11-27): the batch is a stack.
2. (2026-11-27) The owner's words, verbatim, are in `tui-resize-columns/intake/request.md`: resizing the three columns with the mouse, sizes kept in a JSON file in the user's configuration folder found with `platformdirs`.
3. tui-widths-Q1 (2026-11-27): « A. Deux CR (recommandé) »: split from `tui-resize-columns`, and stacked on it.
4. tui-mouse-Q1 (2026-11-27): **Which columns, which edge.** « tu peux prendre l une ou l autre des bordure existante. Attention pour le redimensionnement dynamique c est sur les colonne principale PAS dans la colonne centrale ». The mouse resizes the main columns of the screen (the left column, the central column and the right column), grabbed by either of the two existing panel borders where two columns meet; nothing new is drawn, and the columns inside the central column (Project, Who and the others) are not resized with the mouse. This corrects the Chief of Staff's earlier reading.
5. tui-mouse-Q2 (2026-11-27): **Mouse tracking.** « ok si la barre de status indique ce qu il faut faire. le scroll de la partie principale doit continuer de fonctionner directement ». Accepted that a plain drag no longer selects text and a link may need a modifier, on two conditions: the status bar of `chantier live` says what to do, and scrolling the main part keeps working directly (the mouse wheel, with mouse tracking on).
6. tui-mouse-Q3 (2026-11-27): **The folder.** « A. Un seul dossier (recommandé) »: one configuration folder, computed by `platformdirs` (`$CHANTIER_CONFIG_HOME` still first); on macOS only, `profiles.json` moves, and `chantier login` is run again. Nothing changes on Windows.
7. tui-mouse-Q4 (2026-11-27): **Minimum widths 20 and 30.** « A. 20 et 30 (recommandé) » : a drag stops at 20 columns for the left column and 30 for the right one (defaults 42 and 44).
8. tui-mouse-Q5 (2026-11-27): **Content first.** « affiche le contenu puis tu actives la souris si besoin » : live draws its first screen without waiting for any answer of the terminal about the mouse; the mouse question comes after it, and the mouse is turned on then if the terminal handles it.
9. Chief of Staff's call (2026-11-27), on the specification's question 1: `live` gives each mouse query its own short timeout of 1 second, so a terminal that answers nothing never holds the keys for longer than that per query.
10. Chief of Staff's call (2026-11-27), on its question 2: without the left column, the right column takes spare columns back toward its kept width, after Project and Who.
11. Chief of Staff's call (2026-11-27), on its question 3: during a drag the other side column keeps the width drawn, the border follows the pointer down to a minimum, and the release keeps the width drawn.
12. Chief of Staff's call (2026-11-27): on a drag's release, `live.json` keeps the dragged column's width as drawn and leaves the other column's saved value unchanged.
13. Chief of Staff's call (2026-11-27), told to the owner: `docs/surface-server.svg` changes in this change request: in the `chantier live` box, "terminal, reads only" becomes "terminal, reads the server only" (`live` now writes `live.json`); any other line or description of that diagram that this change makes false changes with it.
14. Chief of Staff's call (2026-11-27), recorded after the second critic pass: on a terminal too narrow for the kept widths, a right column kept wider than 44 gives way first, down to 44, before the left column. With the default widths nothing differs from `tui-resize-columns`.
15. Chief of Staff's call (2026-11-27): a wheel event does nothing while the help is open or while a filter is being typed.
16. Chief of Staff's call (2026-11-27): when the footer lacks room, the mouse words give way first; the typed filter text stays visible.
17. Chief of Staff's call (2026-11-27): a `live.json` that cannot be read or holds a wrong value, an unknown key included, refuses the start with one line; `--once` reads no `live.json`, writes nothing and draws the defaults.
18. Chief of Staff's call (2026-11-27): the Windows Terminal hand run must prove mouse support, else the change request stops and reports.
19. Chief of Staff's call (2026-11-27), on the critic's import point: the check that `clients/tui/` imports nothing else of chantier stays as it is; the configuration folder reaches the new module from outside `clients/tui/`.

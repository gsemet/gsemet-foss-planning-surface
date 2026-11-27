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

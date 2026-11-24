Short name: `copy-raw`

# Answers

1. copy-raw-Q1 (2026-11-24): **Precision at the edges.** Character-precise, and the opening or closing characters of a container are added when the selection starts or ends inside it. The owner's words (free answer): "Au caractère prêt, et il faut éventuellement rajouter les caractères de clôture ou d'ouverture (admonition, tables…) si on commence ou fini au milieu".
2. copy-raw-Q2 (2026-11-24): **An inline element cut at an edge.** Cut exactly at the point, but add the closing (or opening) characters so the Markdown stays balanced. The owner's words (free answer): "Couper exactement au point mais rajouter les caractère de clôture". Example: a selection starting at "r" of `**world**` copies `**rld**`.
3. copy-raw-Q3 (2026-11-24): **Clipboard formats.** A. text/plain carries the raw Markdown, text/html the rendered HTML.
4. copy-raw-Q4 (2026-11-24): **Where.** A. Everywhere in the page, read and edit mode, except inside a text input or field being edited, which keeps the native copy.

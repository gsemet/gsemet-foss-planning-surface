# Balance the edges of a raw Markdown copy

Split off from `copy-selection-raw-markdown` (copy-raw-Q17, on the spec critic's bundle finding F8). Stacked on it in batch-09: it needs that CR's verbatim raw copy (the `previewSourceText` protocol, the selection-to-source mapping, generated content and UI chrome handling).

Owner, 2026-11-23 (the origin request): "Au caractère prêt, et il faut éventuellement rajouter les caractères de clôture ou d'ouverture (admonition, tables…) si on commence ou fini au milieu".

Intent: when a preview selection starts or ends in the middle of a construct, the copied Markdown is cut at the exact character and then balanced so it stays well formed and renders as the selected part: inline markers closed or opened at the cut, container fences added, table header kept, list level brought back to 0, heading marker kept. A selection with clean edges copies the same text as the base CR.

Depends on: copy-selection-raw-markdown (same batch, stacked below).

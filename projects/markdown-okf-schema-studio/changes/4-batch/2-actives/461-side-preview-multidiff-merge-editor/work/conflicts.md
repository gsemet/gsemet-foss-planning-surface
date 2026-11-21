# Conflicts: CR-461 rebase on origin/main

One conflicted file: `requirements/tiers/log.md`, one hunk under `## 2026-11-21`.
Both sides added a dated entry (CR-459 "Impossible comment date refused" from main; CR-461 "Side preview: multi-file diff and merge editor not followed" from the CR).
Choice: keep both entries verbatim, no duplicates, CR-461 first, then CR-459, then the existing CR-456 entry. File stays LF with no byte-order mark, as before.

Rebase continued; the CR is one commit, linear on eb3b6ecc (new head afc00137, message kept).

Fast gate: `just requirements-lint` -> passed (0 indexes, 0 projections, 0 coverage files would change; main paths all valid; 94 use case diagrams parse). Only warnings W2 about broken cross-links in SwRS-MDOKFSTUDIO-PALETTE-264.md, a file this CR does not touch.

Second part of the owner's chosen solution for unreachable empty blocks (2026-11-20), split from
`empty-block-reachable` (3-ready) by the spec critic's bundle finding. In edit mode, runs of blank lines
beyond the one separator show as a small blank-lines block that the writer can reach (keyboard, click)
and remove, so blank lines already in a file (hand edits, older Studio versions) are never out of reach.

Done when: every run of two or more blank lines in the body shows in edit mode as a blank-lines block,
reachable with the arrows, clickable (an insertion editor in its place), removable with Delete,
Backspace or the Delete block button of `empty-block-reachable`, keeping one separator; reading mode
and the export are unchanged; the file's line endings are kept.

Second part of the owner's chosen solution for unreachable empty blocks (2026-11-20), split from
`empty-block-reachable` (3-ready) by the spec critic's bundle finding. In edit mode, runs of blank lines
beyond the one separator show as a small blank-lines block that the writer can reach (keyboard, click)
and remove, so blank lines already in a file (hand edits, older Studio versions) are never out of reach.

Done when: every run of two or more blank lines in the body shows in edit mode as a blank-lines block,
reachable with the arrows, clickable (an insertion editor in its place), removable with Delete,
Backspace or the Delete block button of `empty-block-reachable`, keeping one separator; reading mode
and the export are unchanged; the file's line endings are kept. Runs between the items of a list or
inside a container are out of scope (blank-runs-Q11, `1-inbox/blank-runs-inside-lists`).

Stack: lands after CR-439 (`4-batch/2-actives/439-empty-block-reachable`, branch
`chantier/batch-07/cr-439-empty-blocks-leave-no-blank-lines-and-a-`), which provides
`createDeleteBlockButton` and `deleteSelection()`.

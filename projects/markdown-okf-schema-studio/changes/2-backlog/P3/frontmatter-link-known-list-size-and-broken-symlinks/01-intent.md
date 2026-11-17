# The frontmatter link editor sends the full name list on every capped row

Type: perf · Priority: P3 · Filed 2026-11-01 from CR 220 (behaviour note and round 1 review)

## Today

For a filename-stem field, `src/core/frontmatter/propertiesTable.ts` (around :252-255) emits the
capped suggestion list (500 stems) plus the uncapped known list (`data-okf-link-known`) on every row.
- In a vault of 1125 names that is about 25 KB per row; at 20k files about 0.6 MB per row.
- It repeats on every re-render.
- Behaviour note choice 1 offered a "list incomplete" flag as the alternative: the page then skips the
  "not found" warning instead of holding the full list.

Related, from the same review: a name whose only file is a broken symlink (or a symlink escaping its
root) counts as known in the editor, while the table reports E10/W15 for it. The known set is the
index's raw stems (`fileLinks.ts:171`). This follows the approved "same index" choice.

## Expected

- Send the known list only when it is longer than the suggestions, or send a "list incomplete" flag
  for very large vaults. Pick the cheaper one (details to confirm).
- Decide whether the broken-symlink case is written down as an SwRS-MDOKFSTUDIO-FMEDIT-010 known
  issue, or fixed by filtering the index.

Proof: HTML size of a row on a 1125-name and a 20k-name vault before and after; the editor still
shows no false warning.

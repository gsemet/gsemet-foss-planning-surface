# Evidence 1: one card set

Head `b85be4cbeac5dac2208e26aeb440a9f6676e6ce3`, base `ea11a9e0` (same tree as `88d9ab40`).

| Command | Result |
| --- | --- |
| `git ls-tree -r --name-only HEAD skills/chantier/cards-next` | prints nothing |
| `ls-tree` of `cards-next/` at `ea11a9e0`, minus `skills/`, sorted, against `ls-tree` of `references/` at HEAD | 330 and 330 lines, `diff` prints nothing (exit 0) |
| `git grep -n "cards-next" HEAD` | prints nothing |

Removed paths, each with its completeness-table row: `removed-files.md` (45 removed, 0 without a row).

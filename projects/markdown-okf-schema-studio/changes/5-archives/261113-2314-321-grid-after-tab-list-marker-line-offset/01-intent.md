# A grid behind a tab list marker maps its cards one line too early

Type: fix. Filed 2026-11-13 from CR-319 (PR #392); grilled 2026-11-13 by the Chief of Staff.

## Owner's words

> tu peux me griller un peu le bug trouvé et ce grid-after ?

## Probe (Chief of Staff, `renderMyst` at `origin/main` 5a5f6745, after CR-319)

| Input (opener on line 3, blank line, card on line 5) | Result |
| --- | --- |
| `- ::::{grid} 2`, cards indented 2 spaces | Correct: card line 5, body 6 |
| `-<TAB>::::{grid} 2`, cards indented 2 spaces | Empty grid; the card falls out of the list as an unresolved directive and a stray code block |
| `-<TAB>::::{grid} 2`, cards indented 4 spaces or one tab | Card renders, but **line 4, body 5**: one line early |
| `-<TAB>:::{card} A`, body on the next line | Correct |

## Reading

- **No card (2-space body): CommonMark behaviour, not a parser bug.** A tab after the marker
  expands to the next tab stop (column 4), so the item's content starts at column 4 and a line
  indented 2 spaces ends the item. GitHub and markdown-it read it the same way. Only the writer can
  fix it, by indenting the body to the content column.
- **One line early (4-space or tab body): the CR-319 bug left open for a tab.** `stripContainerPrefix`
  in `src/core/render/mystGridToctree.ts` measures a list level by the characters of
  `LIST_MARKER` (`-<TAB>` is 2), not by its columns (4), so the strip of the following lines and
  the fence test miss, and `directiveBody` falls back to `node.value`, which lost the blank line.

## Scope (pending the owner's answers)

- Fix the line offset: a list level's width is counted in columns with tabs expanded to the next
  multiple of 4, and the following lines strip that many columns (a tab counts as the columns it
  spans). Test rows in `test/core/render/gridCardTitleSourceLine.test.ts`; SwRS-MDOKFSTUDIO-BLOCK-258
  gains the tab case.
- The empty grid with a 2-space body: see the question in `02-answers.md`.

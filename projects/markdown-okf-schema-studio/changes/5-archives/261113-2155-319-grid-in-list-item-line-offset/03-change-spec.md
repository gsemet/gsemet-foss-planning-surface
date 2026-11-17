# Change Specification: a grid inside a list item maps its cards one line too early

Short specification (triage: automatable). Code read at `origin/main` `0a48496b` (version 1.8.1),
after CR-308 (PR #378, commit `9b273307`). Rules: [.agents/constitution.md](../../../constitution.md)
and [AGENTS.md](../../../../AGENTS.md); requirements per
[requirements.guidelines.md](../../../../requirements/guidelines/requirements.guidelines.md) and
[project.guidelines.md](../../../../requirements/guidelines/project.guidelines.md) ("During a
change").

## Goal

A writer opens a `{grid}` on a list item line (`- ::::{grid} 2`, `1. ::::{grid} 2`) and starts the
grid body with a blank line. In edit mode they click a card, its title or its body: the block editor
must open on the line they clicked. Today it opens on the line above.

## Reproduction (render-level probe at `origin/main`)

A throwaway probe rendered small documents through `renderMyst`. It read the `data-line` of the
card (`myst-grid-card`), its title (`myst-grid-card-title`) and the first mapped element of its
body (`myst-grid-card-body`). Each document starts with `# Doc` and a blank line, so the opener is
on line 3.

| Input (opener on line 3) | Expected card / body | `origin/main` |
| --- | --- | --- |
| `- ::::{grid} 2`, blank line, `  :::{grid-item-card} A`, `  Body.` | 5 / 6 | **4 / 5** |
| `* ::::{grid} 2`, the same | 5 / 6 | **4 / 5** |
| `1. ::::{grid} 2`, blank line, cards indented 3 | 5 / 6 | **4 / 5** |
| `10. ::::{grid} 2`, blank line, cards indented 4 | 5 / 6 | **4 / 5** |
| `- item`, then `  - ::::{grid} 2` (nested item), blank line, cards indented 4 | 6 / 7 | **5 / 6** |
| `> - ::::{grid} 2`, blank `>`, `>   :::{grid-item-card} A` (list item inside a quote) | 5 / 6 | **4 / 5** |
| `- > ::::{grid} 2`, `  >`, `  > :::{grid-item-card} A` (quote inside a list item) | 5 / 6 | **4 / 5** |
| `- :::{card} A`, blank line, `  Body.` (standalone card in a list item) | 3 / 5 | card 3, **body 4** |
| `- ::::{tab-set}`, blank line, `  :::{tab-item} A` (tab panel line) | 5 | **4** |
| `- ::::{grid} 2`, cards on the next line (no blank) | 4 / 5 | Correct |
| `1. ::::{grid} 2`, cards on the next line | 4 / 5 | Correct |
| `- ::::{grid} 2`, `  :gutter: 2`, blank line, cards | 6 / 7 | Correct |
| `- text`, blank line, `  ::::{grid} 2` (opener on its own indented line), blank line, cards | 7 / 8 | Correct |
| Unquoted, unlisted grid with a blank first line; quoted grid of CR-308 | 5 / 6 | Correct |

The title always follows the card line. The intent's statement holds, and the probe found three
more cases of the same cause: the standalone `{card}` (body only), the `{tab-set}` and the quote
inside a list item.

## Cause

`directiveBody` in `src/core/render/mystGridToctree.ts` (lines 90-104 at `origin/main`) cuts the body
from the source lines only when the opener, after `stripQuotePrefix` (added by CR-308), passes
`FENCE_LINE` (`^[ \t]*(fence)`). On a list item line the opener starts with the marker (`- `, `* `,
`1. `), so the test fails. The function then falls back to `node.value`, which the parser stripped
of the leading blank line, while `firstLine` still assumes the body starts right after the opener.
The same function serves the grid, the grid items, the standalone card and the tab set, so all of
them are affected.

## What changes

### `src/core/render/mystGridToctree.ts`

- Generalise CR-308's `stripQuotePrefix` into one container-prefix strip used by `directiveBody`
  (for example `stripContainerPrefix`). It reads the opening line from the left as a sequence of
  container levels, each one either:
  - a quote marker (`QUOTE_MARKER`, as today), or
  - a list-item marker: optional indentation, then `-`, `*`, `+` or 1 to 9 digits followed by `.`
    or `)`, then at least one space. Its content width is the column just after the marker's
    spaces, counted from the start of the line as the level sees it.
  The walk stops at the first text that is neither. The rest of the opener must then pass
  `FENCE_LINE`, as today.
- Every following line, up to the closer, is stripped level by level in the same order. A quote
  level removes one quote marker when the line has one. A list level removes up to its content
  width of leading spaces. A line that lacks a level's prefix, such as a blank line, a less indented
  line or a lazy continuation, loses only what it has, and the remaining levels still apply to it.
  Stripping the indentation is required, not cosmetic: kept, the 4-space indentation of `10.` or of
  a nested item would turn the cards into an indented code block in the nested parse.
- The opener line carries the list marker, but the following lines carry only indentation. So the
  marker is stripped from the opener alone, and the following lines lose indentation only.
- With no container level on the opener, the lines are returned unchanged: the unquoted, unlisted
  path and the opener on its own indented line (`  ::::{grid} 2` after `- text`) behave as today.
- `directiveBody` keeps its shape: `lines` are the stripped lines between the fences, `firstLine`
  is `start + 1`. The `node.value` fallback stays for any case the fences still cannot be located.
- Keep the `@implements_req SwRS-MDOKFSTUDIO-BLOCK-258` marker on `directiveBody` and put it on the
  new helper too. The file has 673 lines: stay well under the 800-line ratchet of `just check`.

### `test/core/render/gridCardTitleSourceLine.test.ts`

Write the render-level test first and see it fail at `origin/main`. Extend CR-308's table
`QUOTED_CARD_CASES` (renamed, for example `CONTAINED_CARD_CASES`, if the name no longer fits) with
one row for each line of the reproduction table. The card, title and body lines are the expected
values above, worked out from the source, not copied from the output. Rows:

- failing at `origin/main`: bullet `-`, bullet `*`, ordered `1.`, ordered `10.`, nested bullet,
  list item inside a quote, quote inside a list item, standalone `{card}` in a list item with a
  blank first body line;
- regression guards, correct at `origin/main`: bullet and ordered grid with the cards on the next
  line, bullet grid with `:gutter:`, the opener on its own indented line in a list item.

The CR-308 rows stay as they are. Add one separate test for the tab set in a list item: the
`myst-tab-panel` of `{tab-item} A` carries `data-line` 5. Each new test carries
`// @tests_req SwRS-MDOKFSTUDIO-BLOCK-258` (the file header already does).

### Requirement `SwRS-MDOKFSTUDIO-BLOCK-258` (proposed, not approved: no owner approval needed)

`requirements/tiers/swrs/block-editing/SwRS-MDOKFSTUDIO-BLOCK-258.md`: add one boundary scenario,
"A grid card inside a list item". GIVEN a `{grid}` opened on a bullet or numbered list item line
(`- ::::{grid} 2`) whose body starts with a blank line, then the indented cards. WHEN the writer
clicks a card title or body in edit mode. THEN the editor opens on that card's own directive line or
body line, as for the same grid outside the list, never on the line above. Extend the third
verification note, which covers the quoted cases, with the list-item rows and the new test names. No
normative change.

### Records

- `just requirements-update`, generated files committed.
- `requirements/tiers/log.md`: a dated entry (the date of the change) naming BLOCK-258's new
  boundary scenario and the test file.
- `CHANGELOG.md`, `## Unreleased`, one user line, for example: "A click on a card of a grid
  written in a list item, whose content starts with a blank line, opens the editor on the card
  instead of the line above."
- Commit type `fix:`, scope `render` as in CR-308 (check `git-commit-allowed-scopes.md`).

## Out of scope

- A `::::{grid}` inside a GitHub alert: already filed as `.agents/changes/1-inbox/grid-inside-gfm-alert-cut/`.
- A tab right after the list marker (`-<TAB>::::{grid} 2`): the probe rendered no card at all, at
  `origin/main` and for a reason other than the line offset. Not fixed here. If the coder confirms
  it is a real rendering bug, they file it in `.agents/changes/1-inbox/`.
- Any other change to tab sets or cards beyond what `directiveBody` shares.

## Evidence

- The new rows fail at `origin/main` with the values in the reproduction table and pass after the
  fix. Every regression row and every CR-308 row passes before and after.
- `just check` (TypeScript, boundaries, file size, unit and contract tests) and
  `just requirements-lint` pass. `just preflight` passes (completion gate).
- Manual scenario (optional, the render test is the proof): in Studio, open a document holding
  `- ::::{grid} 2` / blank / `  :::{grid-item-card} A` / `  Body.` / `  :::` / `  ::::`. In edit
  mode, click the title "A": the editor holds the line `  :::{grid-item-card} A`.

## Open questions

None. The owner raised no user-impact question (02-answers.md). The points settled by judgment
are the extra cases taken into scope: the standalone card, the tab set and the quote inside a list
item. They come from the same function and the same fix.

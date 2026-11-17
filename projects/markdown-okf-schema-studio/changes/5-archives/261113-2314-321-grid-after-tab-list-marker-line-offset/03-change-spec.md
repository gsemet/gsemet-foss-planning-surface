# Change Specification: a grid behind a tab list marker maps its cards one line too early

Short specification (triage: automatable). Code read at `origin/main` `5a5f6745` (version 1.8.1),
after CR-319 (PR #392). Rules: [.agents/constitution.md](../../../constitution.md) and
[AGENTS.md](../../../../AGENTS.md); requirements per
[requirements.guidelines.md](../../../../requirements/guidelines/requirements.guidelines.md) and
[project.guidelines.md](../../../../requirements/guidelines/project.guidelines.md) ("During a
change").

## Goal

A writer opens a `{grid}` on a list item line whose marker is followed by a tab (`-<TAB>::::{grid} 2`,
`1.<TAB>::::{grid} 2`), starts the grid body with a blank line and indents the cards to the item's
content column (4 spaces or one tab). In edit mode they click a card, its title or its body: the
block editor must open on the line they clicked. Today it opens on the line above. CR-319 fixed the
same offset for a marker followed by spaces.

The empty grid when the body is indented 2 spaces after `-<TAB>` is CommonMark behaviour and stays,
with no hint in the writing skill (owner's answer Q2, `02-answers.md`).

## Reproduction (render-level probe at `origin/main` `5a5f6745`)

A throwaway probe rendered small documents through `renderMyst` and read the `data-line` of the
card (`myst-grid-card`), its title (`myst-grid-card-title`) and the first mapped element of its
body (`myst-grid-card-body`). Each document starts with `# H` and a blank line, so the opener is on
line 3. `<TAB>` is one tab character; "4 sp" is four spaces.

| Input (opener on line 3) | Expected card / body | `origin/main` |
| --- | --- | --- |
| `-<TAB>::::{grid} 2`, blank line, cards indented 4 sp | 5 / 6 | **4 / 5** |
| `-<TAB>::::{grid} 2`, blank line, cards indented `<TAB>` | 5 / 6 | **4 / 5** |
| `*<TAB>::::{grid} 2`, blank line, cards indented 4 sp | 5 / 6 | **4 / 5** |
| `1.<TAB>::::{grid} 2`, blank line, cards indented 4 sp | 5 / 6 | **4 / 5** |
| `1.<TAB>::::{grid} 2`, blank line, cards indented `<TAB>` | 5 / 6 | **4 / 5** |
| `- item`, then `  -<TAB>::::{grid} 2` (nested item), blank line, cards indented 4 sp | 6 / 7 | **5 / 6** |
| `- item`, then `  -<TAB>::::{grid} 2`, blank line, cards indented `<TAB>` | 6 / 7 | **5 / 6** |
| `-<TAB>::::{grid} 2`, blank line, cards indented 2 sp then `<TAB>` | 5 / 6 | **4 / 5** |
| `> -<TAB>::::{grid} 2`, blank `>`, `>   :::{grid-item-card} A` (list item inside a quote) | 5 / 6 | **4 / 5** |
| `-<TAB>:::{card} A`, blank line, `    Body.` (standalone card) | 3 / 5 | card 3, **body 4** |
| `-<TAB>::::{tab-set}`, blank line, `    :::{tab-item} A` (tab panel line) | 5 | **4** |
| `- ::::{grid} 2` (space), blank line, cards indented `<TAB>` | 5 / 6 | **no card** |
| `-<TAB>::::{grid} 2`, cards on the next line (no blank), 4 sp | 4 / 5 | Correct |
| `-<TAB>::::{grid} 2`, `    :gutter: 2`, blank line, cards 4 sp | 6 / 7 | Correct |
| `- <TAB>::::{grid} 2` (space then tab), blank line, cards 4 sp | 5 / 6 | Correct |
| Every CR-308 and CR-319 row of the test table | as today | Correct |
| `-<TAB>::::{grid} 2` or `1.<TAB>::::{grid} 2`, cards indented 2 or 3 sp | no card | No card (CommonMark, stays) |

The title always follows the card line. The probe confirms the intent and adds one case of the
same cause: a space marker (`- `) with a tab-indented body renders no card (see "Cause").

## Cause

`stripContainerPrefix` in `src/core/render/mystGridToctree.ts` (lines 107-155 at `origin/main`)
reads list levels with `LIST_MARKER = /^[ \t]*(?:[-*+]|\d{1,9}[.)]) +/u`, and strips the following
lines with `/^ */u`:

- The marker must be followed by spaces (` +`), so `-<TAB>` is not a list level at all. The opener
  keeps its marker, fails `FENCE_LINE`, and `directiveBody` falls back to `node.value`, which lost
  the blank line: every line inside is one too early.
- Even matched, the level width is a character count (`-<TAB>` is 2), not the content column (4).
- The following lines lose leading spaces only. A tab-indented body keeps its tab, which the nested
  parse reads as 4 columns: after `- ` (content column 2) the cards become an indented code block,
  hence no card.

## What changes

### `src/core/render/mystGridToctree.ts`

- A list level is a list marker followed by spaces or tabs (`[ \t]+` instead of ` +`). Its content
  column is the column right after that whitespace, with tabs expanded to the next multiple of 4.
  Columns are counted from the start of the original line, including any quote prefix before the
  marker (`> -<TAB>` has its content at column 4, not 2 past the quote), since CommonMark tab stops
  are absolute.
- The opener loses its markers and their whitespace, as today; the rest must pass `FENCE_LINE`.
- Every following line loses, at each list level, its leading spaces and tabs up to that level's
  content column, a tab counting as the columns it spans. A tab that crosses the content column is
  replaced by the spaces it has left past that column (`  <TAB>` after `- ` keeps 2 spaces). A line
  with less indentation, a blank line or a lazy continuation loses only what it has, as today.
- Quote levels are unchanged (`QUOTE_MARKER` and its optional tab stay as they are). Keep the column
  count consistent across levels: a list level after a quote level measures from the quote's
  original column.
- Only leading whitespace consumed by a level is rewritten: tabs further in the line (inside a card
  body or a code block) stay as written.
- `directiveBody` keeps its shape and its `node.value` fallback. Keep both
  `@implements_req SwRS-MDOKFSTUDIO-BLOCK-258` markers and update the `stripContainerPrefix` doc
  comment ("then spaces or tabs", "columns"). The file has 696 lines: stay well under the 800-line
  ratchet of `just check`.

### `test/core/render/gridCardTitleSourceLine.test.ts`

Write the render-level rows first and see them fail at `origin/main`. Add to `CONTAINED_CARD_CASES`
one row for each line of the reproduction table above the "Correct" rows, plus the two regression
guards (`-<TAB>` with the cards on the next line, `-<TAB>` with `:gutter:`) and `- <TAB>`. Write the
tab as `\t` in the source strings. Expected values are worked out from the source, not copied from
the output. Add one separate test for the tab set behind `-<TAB>`: the `myst-tab-panel` of
`{tab-item} A` carries `data-line` 5. The CR-308 and CR-319 rows stay as they are. Each new test
carries `// @tests_req SwRS-MDOKFSTUDIO-BLOCK-258`. The CommonMark "no card" input with a 2-space
body gets no test (owner's answer: not a bug, no new behaviour).

### Requirement `SwRS-MDOKFSTUDIO-BLOCK-258` (proposed, not approved: no owner approval needed)

`requirements/tiers/swrs/block-editing/SwRS-MDOKFSTUDIO-BLOCK-258.md`, boundary scenario "A grid
card inside a list item": the GIVEN says the marker is followed by spaces or a tab
(`- ::::{grid} 2`, `-<TAB>::::{grid} 2`) and the cards are indented to the item's content column
with spaces or tabs. Extend its verification note (the list-item method) with the tab rows and one
or two new test names. No normative change.

### Records

- `just requirements-update`, generated files committed.
- `requirements/tiers/log.md`: a dated entry naming BLOCK-258's amended boundary scenario and the
  test file.
- `CHANGELOG.md`, `## Unreleased`, one user line, for example: "A click on a card of a grid written
  in a list item whose marker is followed by a tab, or whose cards are indented with a tab, opens
  the editor on the card instead of the line above."
- Commit type `fix:`, scope `render` (as CR-308 and CR-319).

## Out of scope

- The empty grid when the body is indented less than the item's content column (`-<TAB>` with 2
  spaces, `1.<TAB>` with 3): CommonMark, kept, no writing-skill hint (owner, Q2).
- The tab after a quote marker (`>` followed by a tab): unchanged.
- A `::::{grid}` inside a GitHub alert: `.agents/changes/1-inbox/grid-inside-gfm-alert-cut/`.

## Evidence

- The new rows fail at `origin/main` with the values of the reproduction table and pass after the
  fix. The regression rows and every CR-308 and CR-319 row pass before and after.
- `just check` and `just requirements-lint` pass. `just preflight` passes (completion gate).
- Manual scenario (optional, the render test is the proof): in Studio, open a document holding
  `-<TAB>::::{grid} 2` / blank / `    :::{grid-item-card} A` / `    Body.` / `    :::` / `    ::::`.
  In edit mode, click the title "A": the editor holds the line `    :::{grid-item-card} A`.

## Open questions

None. The owner's answers are final (`02-answers.md`). Points settled by judgment: the space
marker with a tab-indented body (no card today) is taken into scope, since it comes from the same
following-line strip and the same fix; the standalone card, the tab set, the mixed `  <TAB>` body
and the list item inside a quote are covered as in CR-319.

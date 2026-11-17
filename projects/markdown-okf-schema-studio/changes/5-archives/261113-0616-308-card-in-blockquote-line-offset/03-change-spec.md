# Change Specification: a grid inside a quote maps its cards one line too early

Short specification (triage: automatable). Code read at `origin/main` `cb968299` (version 1.7.1).
Rules: [.agents/constitution.md](../../../../constitution.md) and
[AGENTS.md](../../../../../AGENTS.md); requirements per
[requirements.guidelines.md](../../../../../requirements/guidelines/requirements.guidelines.md) and
[project.guidelines.md](../../../../../requirements/guidelines/project.guidelines.md) ("During a
change").

## Goal

A writer who puts a `{grid}` inside a quote (`>`) and starts the grid body with a blank quoted line
clicks a card, its title or its body in edit mode: the block editor must open on the clicked
card's own line. Today it opens on the line above.

## Scope narrowed (adopted from the advisor, owner's rule of 2026-11-12)

The intent says "every source line" of a quoted grid or card is one line early. The advisor
reproduced it only in one case, and this change fixes that case:

| Input | Result on main |
| --- | --- |
| `> :::{card} T` + body (colon or backtick fence, options, `^^^`/`+++`, nested quote `> >`, quote inside a list item, blank first body line) | Correct |
| `> ::::{grid} 2`, cards on the next line | Correct |
| `> ::::{grid} 2`, then a blank `>` line, then the cards | **Wrong**: the card on source lines 3-5 is mapped 2-4 (card, title and body) |
| The same grid without the quote | Correct |
| `> ::::{grid} 2`, `> :gutter: 2`, blank `>`, cards | Correct |

## Cause

`directiveBody` in `src/core/render/mystGridToctree.ts` (lines 85-102; the advisor calls it
`rawBody`) cuts a directive's body from the source text only when its opening and closing lines pass
`FENCE_LINE` and `CLOSING_FENCE`. Behind a `>` prefix they never do, so it falls back to
`node.value`, which the parser stripped of the leading blank line, while `firstLine` still assumes
the body starts right after the opener. Every line of the body is then one line early.

## What changes

### `src/core/render/mystGridToctree.ts`

- `directiveBody` reads the source lines through the container prefix: it takes the quote prefix
  of the opening line (the `>` markers before the fence, each with its optional following space or
  tab, as many as the opener has: `> ` is one level, `> > ` two), strips that prefix from every line
  from the opener to the closer when the line carries it (a line without it, such as a lazy
  continuation, stays as is), and then runs the same fence tests and the same slice as the unquoted
  path. The returned `lines` are the stripped lines and `firstLine` is `start + 1`, so the nested
  `bodySource` of `buildGrid`, `buildCard`, `buildItem` and `buildTabSet` and the nested
  `parseBody` calls see plain lines, as in the unquoted case.
- The `node.value` fallback stays for any case the fences still cannot be located.
- Other containers with a prefix (a grid in a list item, where the opener line carries `- ` or
  `1. ` and the following lines only indentation): fix only what the same prefix-stripping change
  covers (advisor answer 3). If a list-item case is wrong and needs a different change, it is not
  fixed here: file it in `.agents/changes/1-inbox/` and leave it out of the test.
- Keep the existing `@implements_req SwRS-MDOKFSTUDIO-BLOCK-258` marker on the implementation (add
  it next to `directiveBody` if the marker on `buildCard` does not cover the new code). The file is
  644 lines: stay well under the 800-line ratchet of `just check`.

### `test/core/render/gridCardTitleSourceLine.test.ts`

Write the render-level test first and see it fail on main (the intent asks for that). Through
`renderMyst`, assert the `data-line` / `data-end-line` of the card (`myst-grid-card`), its title
part (`myst-grid-card-title`) and its body part (`myst-grid-card-body`) for each row of the table
above:

- the failing row: `> ::::{grid} 2`, `>`, `> :::{grid-item-card} A`, `> Body.`, `> :::`, `> ::::`
  after a heading and a blank line: the card and its title on the card's directive line, the body
  on its own line (expected values from the source, not from main's output);
- every "Correct" row, as regression guards: the quoted standalone cards (colon and backtick
  fence, options, `^^^`/`+++`, nested `> >`, blank first body line), the quoted grid with cards on
  the next line, the quoted grid with `:gutter:`, the unquoted grid with a blank first line;
- a nested quote `> > ::::{grid} 2` with a blank `> >` first body line (same fix, deeper prefix);
- the list-item rows that the fix covers (see above).

A table-driven test is fine. Each new test carries `// @tests_req SwRS-MDOKFSTUDIO-BLOCK-258`.

### Requirement `SwRS-MDOKFSTUDIO-BLOCK-258` (proposed, not approved: no owner approval needed)

`requirements/tiers/swrs/block-editing/SwRS-MDOKFSTUDIO-BLOCK-258.md`: add one boundary scenario,
"A grid card inside a quote": GIVEN a `{grid}` written inside a quote whose body starts with a
blank `>` line, WHEN the writer clicks a card title or body in edit mode, THEN the editor opens on
that card's own directive line or body line, as for the same grid outside a quote. Extend its
verification note with the new test names. No normative change: the rule already says "the
directive line of that card".

### Records

- `just requirements-update`, generated files committed.
- `requirements/tiers/log.md`: a dated entry (date of the change) naming BLOCK-258's new boundary
  scenario and the test file.
- `CHANGELOG.md`, `## Unreleased`, one user line, for example: "A click on a card of a grid written
  inside a quote, whose content starts with a blank quoted line, opens the editor on the card
  instead of the line above."
- Commit type `fix:` (scope from `git-commit-allowed-scopes.md`).

## Out of scope

- A `::::{grid}` inside a GitHub alert (`> [!NOTE]`): the alert is rewritten as `:::{note}` and the
  grid's inner `:::` closes it. Found by the advisor; file it in `.agents/changes/1-inbox/` as its
  own item, do not fix it here.
- A list-item case that the prefix stripping does not cover (filed in the inbox, see above).
- Any change to tab sets beyond what `directiveBody` shares.

## Evidence

- The new render tests fail on `origin/main` for the blank-first-line quoted grid and pass after
  the fix; every regression row passes before and after.
- `just check` (TypeScript, boundaries, file size, unit and contract tests) and
  `just requirements-lint` pass; `just preflight` passes (completion gate).
- Manual scenario (optional, the render test is the proof): open a document holding
  `> ::::{grid} 2` / `>` / `> :::{grid-item-card} A` / `> Body.` / `> :::` / `> ::::` in Studio,
  edit mode, click the title "A": the editor holds the line `> :::{grid-item-card} A`.

## Open questions

None. The advisor's INTERNAL answers are adopted and the owner raised no USER-IMPACT question for
this CR.

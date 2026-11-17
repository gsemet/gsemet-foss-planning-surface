# CR 209 root cause (#229)

## Where the line becomes snippet-relative
`src/core/render/mystGridToctree.ts`, `buildCard` (~l.240): `parse(title).children[0].children`.
`parse` runs markdown-it on the title string alone. `2. Status projection` becomes an ordered list,
so `children[0]` is a `list`, and its children are bare `listItem` nodes whose position is
snippet-relative (line 1). Unlike `parseBody` (which calls `offsetLines(parsed, firstLine - 1)`),
nothing shifts them. The sanitizer (`html-sanitizer.ts` ~l.482) copies `data-line` to
`data-sphinx-source-line`; `editMode.ts` -> `openBlockEditor` sends range 1..1; Done
(`session/features/blockEdits.ts`) replaces only that range, i.e. line 1 (the heading).
Side effects of the same cause: title renders as a bare `<li>` (the "2." is lost / bullet), a
standalone `{card} 3. x` has the same bug, and `optionLine` (`:header: 4. x`) too.

## Candidate fixes
1. Offset the title parse by `node.position.start.line - 1` (like the body). Smallest; fixes the line
   but keeps the `<li>` and lost "2."; plain titles stay unmapped.
2. Inline-only title, no mapping: fixes rendering, but a title click falls through to the card div
   and the editor opens after the card (breaks BLOCK-257 "editor sits inside the second card").
3. (Recommended by Inspector) Inline-only title (literal text / escaped marker if first block is not
   a paragraph), strip snippet positions, and set explicit data-line/data-end-line = directive line
   on the title part; skip when `:link:` is set. Apply the same unmapped inline treatment to
   `optionLine`. Risk: plain titles become mapped (click now opens the title editor inside the card
   instead of the whole card) - matches BLOCK-257 but is a behaviour change to mention in the PR;
   check the link-card case and the SwRS/visual checks v25/v26.

Test: `test/core/render/gridCardTitleSourceLine.test.ts` (render level; page has no logic between
the render attributes and the editor range). Fixture directive line is 8, not 7.

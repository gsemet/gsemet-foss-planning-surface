# CR-465 investigation

## Cause
- myst-directives `dropdown` (node_modules/myst-directives/dist/dropdown.js) yields an mdast node
  `{type:"details", open, children:[{type:"summary", children}, ...body]}`; it is NOT an `admonition`.
- src/core/render/mystNormalize.ts only handles `kinds:["admonition"]` (line ~341, `:class: dropdown` path -> details).
  No handler for `details`/`summary`. myst-to-html default (`schema.js:112`) is `h(node,'details')` with no children
  -> empty `<details></details>`, no `sourcePositionProperties` -> no data-line mapping. Colon and backtick fences are the same node.
- The palette dropdown (src/page/modules/blockEditActions.ts:541) writes `{note} Title` + `:class: dropdown`, which is why that form works.

## Smallest change
Add a normalizer entry in mystNormalize.ts next to "admonition": `kinds:["details"]`: classes `admonition dropdown`
(+ any node.class), summary child -> `setHast(summary,"summary",{class:"admonition-title"})` retyped like `admonitionTitleInline`
(same trick as lines 369-372), node -> `setHast(node,"details",{class, open if node.open, ...sourcePositionProperties(node,line)})`,
type `admonitionBlock`, keep children (so body renders). No title: add "Details" summary. Reuse the admonition CSS (`details.admonition`).
Check line markers (src/page/features/lineMarker.ts, mappedBlocks) accept the block (it already unfolds closed dropdowns) and that
nested blank-run/marker code (blankLines.ts) treats it like an admonition.

## SwRS / tests
- Extend SwRS-MDOKFSTUDIO-MYST-006 (admonitions nest, collapse, map; implemented_in mystNormalize.ts, tests mystFeatures.test.ts)
  or add a new MYST SwRS "dropdown directive renders and maps its body" (next free id after MYST-0xx; derives_from StRS-MYST-015). Related: MYST-001, CORE-071 (raw details), MYST-052.
- Unit: test/core/render/mystFeatures.test.ts next to "dropdown admonitions render as openable details" (line 610): colon fence, backtick fence, `:open:`, body text + data-line on details, closed by default, no title. Add `@tests_req`.
- Simulated window: test/page/runtimeLineMarkerPlacement.test.ts / test/visual scenarios (fixtures 38-myst-gallery.md, 91-line-marker.md already contain dropdowns; add `{dropdown}` in both forms).
- Source bytes unchanged: nothing touches the editor/source path.

## okfreq
Read requirements.guidelines.md + project.guidelines.md ("During a change"); keep `@implements_req`/`@tests_req` markers; run
`just requirements-update`; dated entry in requirements/tiers/log.md; `just preflight`. Writing skill: check
skills/writing-for-markdown-okf-schema-studio/ mentions `{dropdown}`; update only if it says it is unsupported (syntax set unchanged otherwise).

## Risks
- Nested dropdown in dropdown/tabs and blank-run markers (recent commit 1a5b98bb, dcb68c13) rely on `admonitionBlock`/data-line; verify.
- Export (src/core/export/exportContent.ts:125) already converts details; check export of new block.
- Unrelated `{admonition}` with `:class: dropdown` must stay unchanged.

## Questions for the user
None.

## Evidence plan
Kind: bug fix in rendering. Before/after: unit test output (fails before, passes after) with the rendered HTML of
`:::{dropdown} Dd\nBody\n:::` and the backtick form; a simulated-window screenshot (just e2e / visual scenario with the 38 gallery or 91 line-marker fixture)
showing the open and closed dropdown with body and the line marker. Technique: run the new unit test on origin/main code (fail) and on the fix;
reuse test/visual scenarios. Cannot show: real VS Code window (heavy CI jobs only).

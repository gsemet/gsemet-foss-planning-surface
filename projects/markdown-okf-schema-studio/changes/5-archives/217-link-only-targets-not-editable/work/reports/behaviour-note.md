# Behaviour note — in edit mode a click on a link opens the editor

## Today (reproduced, round 0)
Edit mode on: a click, Enter or Space on any link inside a mapped block follows the link and opens no editor.
A `:link:` card is one big link (the title anchor's `::after` covers the whole card), so a click on its title,
header, body or footer posts `previewLink:targets/alpha.md`. No edit-hover outline on links; pointer cursor.
Failing tests: test/page/linkEditModeClick.test.ts (4 fail: click in paragraph, link-only paragraph, Enter, Space;
3 already pass: Cmd/Ctrl+click, Cmd/Ctrl+Enter, reading mode).

## After
Edit mode on: click, Enter or Space on a link opens the editor of the block that holds it; Cmd/Ctrl+click and
Cmd/Ctrl+Enter follow it. Reading mode unchanged. A `:link:` card behaves like a card without link: the overlay is
inert in edit mode, so the clicked part decides (title -> directive line, header/footer option -> its line, body ->
its block). Hover in edit mode outlines the block as for any other text and shows the hint.

## Requirements
- SwRS-MDOKFSTUDIO-BLOCK-014 (proposed): rows changed as in the intent; "A linked image" generalised; hover hint.
- SwRS-MDOKFSTUDIO-BLOCK-258 (proposed): the "card with a link" scenario now maps the title in edit mode.
- SwRS-MDOKFSTUDIO-TOOLBAR-077 (proposed): add "in edit mode only a Cmd/Ctrl click or Cmd/Ctrl+Enter posts previewLink".
- No approved requirement changes (StRS-BLOCK-003 approved, unchanged).

## Choices left open (proposals)
1. Hint: appended to the link's native tooltip on a new line, edit mode only: "Cmd+click to follow" on macOS,
   "Ctrl+click to follow" elsewhere (target path or blocked reason stays on the first line).
2. Middle click (auxclick) in edit mode: still follows (it is never "edit this").
3. Same-page anchors (#heading, footnote refs) and external URLs: same rule as file links.
4. Links outside a mapped block (properties table link values, comment threads, toolbar): unchanged.
5. Cursor over a link in edit mode: text cursor like the rest of the block; pointer while Cmd/Ctrl held is NOT done (no key tracking).
6. Card hover outline: the part under the pointer (as for a non-linked card), not the whole card.

## Owner answer (2026-10-31)
APPROVED. Choices 1-5 as proposed; choice 6: outline only the part under the pointer (replaces the whole-card mockup).

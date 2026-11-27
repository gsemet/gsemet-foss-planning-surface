# CR-511 before and after

- Before: base `2fb89df9c1d19c9e882702f7b2f8328ccc105ae8` (detached throwaway worktree, removed)
- After: pushed head `abfa71e58f2f150d028781beaeecc2bede4c8182`
- No screenshot pair is planned (`work/evidence-plan.md`): the change has no user-visible effect,
  `git diff --stat 2fb89df abfa71e -- src/` prints nothing. The pair below is the requirement text.
- Every planned pair is captured.

## Pair 1: what SwRS-MDOKFSTUDIO-LAYOUT-023 says about nested blocks

Reproduce, at each SHA, in `requirements/tiers/swrs/layout-width/SwRS-MDOKFSTUDIO-LAYOUT-023.md`:

    grep -nE "^When the width mode is Auto|^### Scenario S[89]|inside a list item|inside an admonition|inside a block quote|inside a card|^- Known issue" <file>

Before (`2fb89df`), lines 67, 114, 123, 130 (the two other known issues and the method line omitted):

    67:When the width mode is Auto, the extension SHALL widen a table, figure, image, code block or Mermaid diagram that is wider than the text column to the width it needs (...)
    114:### Scenario S8 (nominal): A code block fits its longest line
    123:| A code block inside a list item, wider than the item | Not marked; scrolls inside the item (Known issue) |
    130:- Known issue: Only top-level blocks, or the paragraph holding only an image, break out; a code block in a list item, admonition, block quote, tab set or card scrolls inside it.

After (`abfa71e`), lines 72, 119, 129, 133 to 136, 143:

    72:When the width mode is Auto, the extension SHALL widen a top-level table, figure, image, code block or Mermaid diagram (a direct child of the page content, or an image alone in a top-level paragraph) that is wider than the text column (...); a block nested in a list item, admonition, block quote, tab set, dropdown or card keeps the layout it has in Margin.
    119:### Scenario S8 (nominal): A code block fits its longest line
    129:### Scenario S9 (refusal): Nested blocks keep their Margin layout
    133:| Auto, a code block inside a list item, wider than the item | Neither the block, the item nor the list is marked wide or shifted; the block scrolls inside the item as in Margin |
    134:| Auto, a wide table inside an admonition | Neither the table nor the admonition is marked wide |
    135:| Auto, a wide image alone in a paragraph inside a block quote | Neither the image, the paragraph nor the block quote is marked wide |
    136:| Auto, a wide code block inside a card or a tab panel | Not marked wide |
    143:- Known issue: A linked image alone in a top-level paragraph is not widened. A top-level paragraph holding no text and several images, at least one of them not wrapped in a link or another element, is measured and marked as a whole, once, from its first image's sizes, so a wide image after a narrow first one does not widen it.

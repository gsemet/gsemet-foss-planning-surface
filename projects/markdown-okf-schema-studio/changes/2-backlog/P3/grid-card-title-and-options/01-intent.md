# Grid card titles and options: numbered titles lose their markup, header and footer options vanish

Severity Low · Reproduced (1), Observed once (2) · Verdict Gap · Requirements: SwRS-MDOKFSTUDIO-BLOCK-258, SwRS-MDOKFSTUDIO-MYST-053, SwRS-MDOKFSTUDIO-MYST-100 · Area Grid cards · Side preview · QA215-07, QA215-08 · Replay `scenarios/c3-2-numbered-card-title-keeps-markup-literal.json` · P3

Both come from how #236 parses a card's title and options (`src/core/render/mystGridToctree.ts`).

## 1. A numbered title shows its emphasis literally (QA215-07)

| Currently | Expected |
| --- | --- |
| ![Numbered card title shows *card* with raw asterisks](evidence/currently.jpg) | The number stays literal and `*card*` renders as emphasis, as `**bold**` does in the unnumbered standalone card of the same shot. |

**Why this is wrong.** `:::{grid-item-card} 1. First *card*` shows raw asterisks while
`:::{card} Standalone **bold** title` shows bold. A title parsed as a list falls back to plain text for
the whole title; BLOCK-258 only asks that the number stays literal.

**Fix.** Escape the leading number before parsing, keep the rest inline. Uncheck to disagree: [x]
**Test.** Render test: `2. *title*` gives an `em` and the literal "2.". Uncheck to disagree: [x]
**Requirement.** Amend BLOCK-258: a numbered title keeps its other inline markup. Uncheck to disagree: [x]

## 2. `:header:` and `:footer:` of a grid-item-card vanish (QA215-08, observed once)

No visual: the header text of the first card of `fixtures-visual/73-grid-card-editing.md` appears nowhere
(0 `.myst-grid-card-option` nodes). A standalone `{card}` shows `:header:`; a `{grid-item-card}` with the
same option drops it silently, so the author sees text vanish and cannot click it to edit it.

- (x) Render the options on a grid-item-card, as on a standalone card
- ( ) Show the line as a muted "unsupported option"

**Requirement.** State in MYST-053 whether the option is supported. **Test.** No test: a render test pins
whichever choice is made. Uncheck to disagree: [x]

Update 2026-11-03: the Grid form no longer writes these options; it writes the header and footer
with the `^^^` and `+++` separators of a grid card (#304). Only a hand-written `:header:` or
`:footer:` option on a grid-item-card is left.

Sources: [campaign 215 index](../../../4-archives/215-qa-campaign-2026-10-31/00-index.md), sheets in
[02-grid-cards](../../../4-archives/215-qa-campaign-2026-10-31/02-grid-cards/).

# A numbered grid-card title shows its emphasis markers as literal characters

Severity Low · Reproduced · Verdict Gap · Requirements: SwRS-MDOKFSTUDIO-BLOCK-258 (keeps a leading number literal, silent on the rest of the title) · Area Grid cards · Side preview ·
c3-2 · Replay `scenarios/c3-2-numbered-card-title-keeps-markup-literal.json`

## Currently / Expected

| Currently | Expected |
| --- | --- |
| ![currently](../../evidence/c3-2-currently.jpg) | The same card title with the number kept literal and `*card*` as emphasis; the unnumbered standalone card at the bottom of the same shot renders its `**bold**`. |

## Why this is wrong

`:::{grid-item-card} 1. First *card*` shows "1. First *card*" with raw asterisks, while `:::{card} Standalone **bold** title` shows bold. The cause is that a title parsed as a list ("1. ...") falls back to plain text for the whole title (`inlineContent` in `src/core/render/mystGridToctree.ts`). The requirement only asks that the number stays literal; the rest of the title is formatting the author wrote and expects rendered.

## Steps to reproduce

1. Fixture with `:::{grid-item-card} 1. First *card*`, preview to the side.

**Fix.** Escape the leading number before parsing the title, keep the rest inline. Uncheck to disagree: [x]
**Test.** Render `2. *title*`, assert an `em` and the literal "2.". Uncheck to disagree: [x]
**Requirement.** Amend BLOCK-258: a numbered title keeps its other inline markup. Uncheck to disagree: [x]

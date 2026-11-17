# A spreadsheet selection pasted into a cell keeps raw tabs

Severity Low · Reproduced · Verdict Gap · Requirements: SwRS-MDOKFSTUDIO-TABLE-091 (pipes escaped, line breaks become a space; tabs not mentioned) · Area Tables · Clipboard · Side preview · c5-2 · Replay `scenarios/271-c5-2-pasted-tsv-keeps-raw-tab-in-cell.json`

## Currently / Expected

| Currently | Expected |
| --- | --- |
| `+ \| Five \| a<TAB>b<TAB>c 1<TAB>2<TAB>3  \| erin \|` (raw tab characters, a trailing space) | `\| Five \| a b c 1 2 3 \| erin \|` (tabs treated like line breaks) |

No visual: the preview renders a tab as a space; the defect is in the source line (measured with `q spy --diff`).

## Why this is wrong

Pasting two spreadsheet rows (tab-separated) into one cell turns the line breaks into spaces (TABLE-091) but keeps literal tab characters and the space of the final newline, so the saved row holds invisible tabs. Copying cells from the preview gives TSV, and pasting that back gives the same tabs. A reader of the source sees misaligned columns; a formatter may re-pad them. Expected follows TABLE-091's own treatment of line breaks.

**Steps.** `printf 'a\tb\tc\n1\t2\t3\n' | pbcopy`, side preview, edit mode, click cell `row five`, Meta+a, Meta+v, Enter, diff vs mark. Other pastes behave: multi-line text and a pasted Markdown table stay in one cell with pipes escaped, no broken row (diff -1 +1).
**Fix.** Normalise tabs to a space (and trim) where line breaks are replaced. Uncheck to disagree: [x]
**Test.** Extend `test/page/fmtableReqTable.requirements.test.ts` with a tab paste. Uncheck to disagree: [x]
**Requirement.** Amend TABLE-091 to name tabs. Uncheck to disagree: [x]

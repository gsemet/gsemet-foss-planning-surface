# Replace all skips matches in a block whose link URL also contains the query

Severity Medium · Reproduced · Verdict Gap · Requirements: SwRS-MDOKFSTUDIO-TOOLBAR-012 · Area Find and replace in the preview · Side preview · QA210-05 · Replay `scenarios/c4-1-replace-all-skips-list-with-hidden-url-match.json` · P2

## Currently / Expected

| Currently | Expected |
| --- | --- |
| ![Find bar counts 4 matches; after Replace all 2 remain](evidence/currently.jpg)<br><pre>-Para needle one.<br>+Para PIN one.<br>-Tail needle.<br>+Tail PIN.</pre> | <pre>-Para needle one.<br>+Para PIN one.<br>- - list needle<br>+ - list PIN<br>- - [link needle](https://example.com/needle)<br>+ - [link PIN](https://example.com/needle)<br>-Tail needle.<br>+Tail PIN.</pre> |
| *Currently: the find bar counts 4 matches ("1 of 4"); Replace all replaces 2, and the note "2 matches cannot be replaced from the preview" only appears after the click (replay `c4-1` on b9118506).* | *Expected: all four matches replaced, or the count and a note say before the click which matches are skipped.* |

The Currently shot is the before-shot the fix PR must reproduce.

## Why this is wrong

An author renames a term across a chapter with Replace all. A link whose text and target both name
the term is common, and when it sits in a list the whole list is skipped: the bar promised 4
matches, replaced 2, and the list and the link text still read `needle`. The note "2 matches cannot
be replaced" appears only after the click, where it is easy to miss, so the author believes the
term is gone. The URL is not visible text, so the visible matches have no reason to be refused. A
control fixture with the URL changed to `/other` replaces all four. TOOLBAR-012 covers only the
note after the replacement; nothing says what the bar shows before.

## Steps to reproduce

1. Fixture `synth/find-list-b.md` (in `assets/synth/`):

   ```markdown
   # Heading

   Para needle one.

   - list needle
   - [link needle](https://example.com/needle)

   Tail needle.
   ```

2. Open it, Open Preview to Side, click the heading, Cmd+F, type `needle`: the bar counts 4.
3. Toggle replace, type `PIN` in the replace field, click Replace all.
4. The bar reports "Replaced 2 matches; 2 matches cannot be replaced from the preview".

## Impact

A rename leaves occurrences behind and the after-the-fact message is easy to miss. No data loss, no
corruption.

## Where it comes from

The hidden occurrence in the link target of the same source block makes the rendered and source
occurrences disagree, so the whole block is unreplaceable. The pre-action note (`updateNote` /
`unreplaceableCount` in `src/page/modules/findBar.ts`) does not count those matches. Not read in
depth.

## Suggested direction

Either replace the visible occurrences and leave the URL alone, or count the block as unreplaceable before the click so the warning comes first. Done when: either the visible matches are replaced, or the count and a note say before the click which matches will be skipped; replay `c4-1` passes.

Uncheck to disagree: [x]

## Requirement to write or change

Write a new SwRS (Gap): "Replace all announces the matches it will skip" - When the find bar holds a query, the extension SHALL count in its note, before any replacement, the matches that cannot be replaced from the preview.

Uncheck to disagree: [x]

## Test to add

Add a unit test on the match counter: a block with a visible match and a link URL containing the query is counted or replaced as the requirement says. It earns a test because the skip is silent and leaves the author thinking the document was fully replaced.

Uncheck to disagree: [x]

Sources: sheet [c4-1](../../../210-qa-campaign-2026-10-31/work/04-find-replace/c4-1-replace-all-skips-list-with-hidden-url-match.md),
replay [c4-1](../../../../skills/markdown-studio-exploratory-qa-claude/scenarios/c4-1-replace-all-skips-list-with-hidden-url-match.json),
[campaign index](../../../210-qa-campaign-2026-10-31/work/00-index.md).

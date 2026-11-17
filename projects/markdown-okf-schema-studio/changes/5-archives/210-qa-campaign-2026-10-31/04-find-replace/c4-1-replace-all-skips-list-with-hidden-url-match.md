# c4-1 — Replace all silently skips the visible matches of a list whose link URL also contains the query

| Field | Value |
| --- | --- |
| Severity | Medium |
| Confidence | Reproduced (3 runs, plus a control fixture that passes) |
| Area | Find and replace in the preview |
| Modes | Side preview (also with edit mode on) |
| Evidence | buffer diff in the scenario output |
| Related | none |
| Replay | `scenarios/c4-1-replace-all-skips-list-with-hidden-url-match.json` (fixture below, `synth/find-list-b.md`) |

## Use case

An author renames a term in a chapter with Replace all in the preview find bar. Some of the
occurrences sit in a list whose link URL contains the same word (a very common case: a link
whose text and target both name the term).

## Steps to reproduce

Fixture `synth/find-list-b.md`:

```markdown
# Heading

Para needle one.

- list needle
- [link needle](https://example.com/needle)

Tail needle.
```

1. Open it, Open Preview to Side, click the heading, Cmd+F, type `needle`.
2. Toggle replace, type `PIN` in the replace field, click Replace all.

## Expected

Every visible match is replaced: `Para PIN one.`, `- list PIN`, `- [link PIN](...)`, `Tail PIN.`
The URL is not visible text and may stay. (Control: with the URL changed to `/other`, all four are
replaced; with a query matching only the list lines, e.g. `(list|link) needle` as regex, they are
replaced too, and Replace on the single match `list needle` works.)

## Observed

The bar counts 4 matches and warns about none before the action. Replace all reports
"Replaced 2 matches; 2 matches cannot be replaced from the preview" afterwards: only the paragraph
and the tail line changed; the list and the link text still read `needle`. Same on a larger fixture
(`synth/find-mix.md`: 20 case-sensitive matches, 17 replaced, list and link text skipped, frontmatter
tag correctly skipped). The skipped matches were announced as replaceable before the click.

## Impact

A rename leaves occurrences behind. The message after the fact is easy to miss, and the author
believes the term is gone. No data loss, no corruption.

## Where it comes from

Not read in depth. The trigger is the hidden occurrence in the link target of the same source
block (a rendered/source occurrence mismatch makes the whole block unreplaceable), but the
pre-action note (`updateNote` / `unreplaceableCount` in `src/page/modules/findBar.ts`) does not
count those matches.

## Suggested direction

Either replace the visible occurrences and leave the URL alone, or count the block as unreplaceable
before the click ("2 matches cannot be replaced") so the warning comes first.

## Test to add

Real-input E2E on the fixture above: Replace all then `diff` contains `list PIN` and `[link PIN]`.

## Done when

The replay scenario passes, or the bar shows the "cannot be replaced" note for those two matches
before Replace all is pressed.

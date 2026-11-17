## Summary

A coloured span inside a raw HTML table (`<span style="color: red">Urgent</span>`) rendered in the
plain text colour, because spans accepted only hex and `rgb()` while table styles accepted names and
`hsl()`. Table styles, colour spans, the page re-validation and the editor colour field now share
one strict colour grammar, so the same colour works everywhere.

## Deliverables

| Value | Before (span) | Before (table cell) | After (both) |
| --- | --- | --- | --- |
| `red`, `RebeccaPurple`, `transparent` | removed | any lowercase word | kept (closed list of CSS names) |
| `#rgb`, `#rgba`, `#rrggbb`, `#rrggbbaa` | kept | kept | kept |
| `rgb()`, `rgba()` (comma form) | kept | kept | kept |
| `rgb(0 0 0 / 50%)` (space form, optional `/ alpha`) | removed | kept | kept |
| `hsl()`, `hsla()` (either form, `%`) | removed | kept | kept |
| `currentcolor`, `inherit`, `initial`, `unset` | removed | kept | kept |
| other words, mixed comma/space, out-of-range numbers | removed | kept (any word) | removed |
| `var()`, `url()`, `expression()`, `!important`, comments, `\` escapes, `;` or `}` injection | removed | partly | removed |

```
<table>...<td><span style="color: red">Urgent</span>   ->  red text
                <span style="color: var(--x)">Plain</span> -> plain text, one diagnostic
```

A removed span style now records the diagnostic `removed-unsafe-style` (it used to reuse
`blocked-event-attribute`, which is about event attributes).

Screenshots (light and dark) of the new scenario: the table shows red, green, blue-on-amber and an
uncoloured "Plain" span.

## Changes

- `src/core/security/spanColors.ts`: the single grammar (closed name list, hex, `rgb`/`rgba`,
  `hsl`/`hsla` with strict numeric ranges, comma and space forms, plus four keywords).
- `src/core/security/html-sanitizer.ts`: table styles and gradients use that grammar; a removed span
  style records `removed-unsafe-style`.
- `src/core/render/mystTables.ts`: a span in a raw table is handed to the sanitizer instead of being
  dropped.
- SwRS GFM-034 (grammar, diagnostic), GFM-031, TRUST-036, PALETTE-058 and the update log.

## Impacts

Named colours and hsl() now render in spans and in the editor colour field. In table styles,
what was accepted before keeps working (space syntax, the four keywords) but with strict numbers;
unlisted words are removed, and gradient stops narrow from any lowercase word to the closed list
plus the keywords. Assertions whose intent changed because `red` is now valid: the span test in
`html-policy.test.ts` and `mystPaletteRendering.test.ts`, the editor colour field tests
(`editActions.test.ts`, `editPalette.test.ts`, which now use the invalid word `redd`), and the
visual check on `33-figures-anchors` (the named span is now coloured).

## Blast radius

Grade: **2**. Security-relevant shared sanitizer code. The grammar only admits a closed set of
tokens and refuses everything else whole, adversarial tests cover var/url/expression/important,
comments, escapes, `;`/`}` injection, other functions, quotes and look-alike Unicode. Revert is a
plain `git revert`.

## Test plan

- [x] New or changed tests (they fail on the previous code): grammar and injection tests, table
      style grammar, a span in a raw table, diagnostic code, two visual scenarios (light, dark)
- [x] Requirements: GFM-034, GFM-031, TRUST-036, PALETTE-058 updated; `okfreq validate`, `lint
      --check`, `update-coverage --check` clean
- [x] Local gates: `just check` (2654 unit tests, 0 failed), security suite 47 passed,
      `just ci-visual` passed (355 scenarios)
- [ ] Review
- [ ] CI green

## Internal references

- CR 098 html-colour-grammar

🤖 Generated with [Claude Code](https://claude.com/claude-code)

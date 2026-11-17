# One colour grammar for raw HTML tables and colour spans

User decision (2026-10-24): fix, P3.

Current behaviour (specified as-is in the gfm SwRS, "Known issue"):

- Raw HTML table styles accept colour names and `hsl()`.
- `<span style="color: …">` keeps only hex (`#rgb`, `#rgba`, `#rrggbb`, `#rrggbbaa`) and
  `rgb()`/`rgba()`; anything else is removed silently (`src/core/security/html-sanitizer.ts`,
  span `style` branch; page re-validation in `src/page/modules/spanColors.ts`).
  Example: `<span style="color: red">Urgent</span>` inside a raw table renders black.
- The removal is logged with diagnostic code `blocked-event-attribute`, which is about event
  attributes, not styles (F-GFM-036).

## Expected

- One shared colour grammar (names, hex, rgb/rgba, hsl/hsla) used by the sanitizer for tables and
  spans and by the page re-validation; still no `var()`, `url()`, `!important`, comments.
- A dedicated diagnostic code for a removed style (for example `removed-unsafe-style`).
- Unit tests for the grammar and the diagnostic; update the gfm SwRS in the same change.

Requirement ids older than the baseline merge map to their current tile in `.agents/changes/archives/059-requirements-okfreq/reduction/mapping.csv`.

# QA annotate: warn on an unknown colour

Tooling · P3 · Filed 2026-10-31 from the CR 213 final inspection

In `scripts/qa.mjs`, the `{at, color}` object form of `--annotate` accepts an unknown colour silently.
Warn (as the flag form does) and fall back to red.

## Done when

- [ ] An unknown colour in the object form prints a warning and draws in red.

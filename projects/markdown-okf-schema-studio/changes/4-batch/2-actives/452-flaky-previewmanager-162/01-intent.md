# Flaky previewManager test: a hidden panel shown renders twice (2 !== 1)

See intake/request.md. test/session/previewManager.test.ts "a hidden panel does not render until
it is shown, then renders once" (SwRS-MDOKFSTUDIO-LIFE-039) waits fixed times (150 ms, 200 ms).

## Grill, 2026-11-21 (owner's answers, asked by the Chief of Staff)

- pm-Q1 (if the cause is a real double render in the product). Owner: "Corriger aussi le
  produit": find the race; if the product renders twice when a hidden panel is shown, fix the
  product; the test waits on an event (or a render count), not on fixed times.

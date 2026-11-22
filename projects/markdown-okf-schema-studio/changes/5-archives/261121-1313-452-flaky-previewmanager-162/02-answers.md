# Flaky previewManager test: a hidden panel shown renders twice (2 !== 1)

See intake/request.md. test/session/previewManager.test.ts "a hidden panel does not render until
it is shown, then renders once" (SwRS-MDOKFSTUDIO-LIFE-039) waits fixed times (150 ms, 200 ms).

## Grill, 2026-11-21 (owner's answers, asked by the Chief of Staff)

- pm-Q1 (if the cause is a real double render in the product). Owner: "Corriger aussi le
  produit": find the race; if the product renders twice when a hidden panel is shown, fix the
  product; the test waits on an event (or a render count), not on fixed times.
- Owner, 2026-11-21: "Et tout ça partira dans le batch en cours": once final and ready, added to the running batch-07.

## Owner's answers, 2026-11-21 (Fable spec critic's questions)

The critic found the failing test is the join-window test ("a page refresh inside the join window renders again instead of joining the shared render"; JS line 162, CR-443 gate log 20261121-020805.log), not the hidden-panel test; pm-Q1 was answered on that wrong premise. Race reproduced: a request more than ~250 ms after the render ended renders again, as sharedRenders.ts documents.
- pm-Q2 (re-confirm on the real premise). Owner: "Corriger le test seul": the test controls time (fake timers) instead of waiting; the product does not change; rendering again past the 250 ms window stays accepted.
- pm-Q3 (hidden-panel test with fixed waits). Owner: "Oui, même CR": no fixed wait left in either test.

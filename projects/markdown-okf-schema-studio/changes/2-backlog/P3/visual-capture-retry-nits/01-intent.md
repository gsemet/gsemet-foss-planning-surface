# Small nits after the capture retry and the demo-capture changes

Type: nits · Priority: P3 · Filed 2026-11-01 from CR 232 and CR 233 reviews

## Today

- `test/visual/capture.py` (~:290): a negative `retryOnTimeout` gives zero attempts, and the scenario
  then runs on an unbound or stale page. No scenario uses a negative value. Fix: `max(0, ...)`.
- `test/visual/scenarioDefinitions2.ts:782`: the comment still says "the known intermittent CI hang",
  although the networkidle wait was removed.
- `test/integration/realInput/previewWindow.ts` (~:411-413): the `.catch` on the `waitFor` relabels
  every error as "not fully visible ... not measured", for example a strict-mode error from a second
  matching element. The original error is kept as `cause`.

## Expected

Clamp with `max(0, ...)`, reword the comment, and only relabel a timeout error.

Proof: `just check`; a unit-level or manual run with `retryOnTimeout: -1` runs the scenario once.

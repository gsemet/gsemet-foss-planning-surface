# QA replay c6-2 may fail when the file watcher lags

Type: test-flake risk · Priority: P3 · Filed 2026-11-01 from CR 228 (round 2 inspector review)

## Today

The promoted replay c6-2 (link hint ignores the document folder) in `test/integration/qa210Replays.ts`
(around :269) writes the target file right before the preview opens. If the cached link index is not
invalidated in time, the first render may not resolve the link, and the `waitFor` for "the table
resolves the related target" times out. The precondition itself is deterministic (unique stem, repo
only). No failure seen yet; noted for CI triage.

## Expected

Wait for the workspace file-watcher create event on the target before opening the preview, or force a
re-render inside the `waitFor`.

Proof: the replay passes with an artificial delay on the watcher event.

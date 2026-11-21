test(integration): trace and harden the real-window table-insert-slash scenario

## Summary

The real-window scenario that inserts a table from the slash menu and centres the first column
failed once in CI and passed on re-run. This change makes the next failure explain itself and
removes the most likely cause: the press on the just-opened Center option had no preceding hover,
so it could be routed to the workbench instead of the webview (the known failure that the CI
guidelines describe for list options). The cause of the original failure is not proved yet; the
stress runs below say what they showed.

## Deliverables

None (test-only change).

## Changes

- The scenario fails with one message that carries the passed steps with their times, the host's
  render request, the source document, the editor state, the focus report with the page's editor
  trace, and the landing summary of the press.
- The Center press uses `clickListOption` (hover first), like the other list options of the suite.
- `table-insert-slash` is registered as an on-demand stress scenario (not in the default plan) and
  a unit test covers that.
- Base: this branch builds on the branch of the paste-url/drop-files flake change (shared stress plan
  and real-input files); it rebases onto main once that change merges.

## Impacts

No visual change; no change to the product.

## Blast radius

Grade: 1. Tests and the stress plan only; a plain `git revert` restores the previous state.

## Test plan

- [x] New or changed tests (stress plan unit test)
- [x] Requirements: No behaviour change
- [x] Changelog: No user-facing change
- [x] Local gates: `just check`
- [ ] Review
- [ ] CI green

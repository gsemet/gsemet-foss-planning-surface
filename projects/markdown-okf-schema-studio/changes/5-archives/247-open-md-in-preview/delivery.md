# Report: CR 247

Status: **done** (2026-11-03, branch `change-requests/247-open-md-in-preview`, PR [#293](https://github.com/gsemet/markdown-okf-schema-studio/pull/293), merged by the owner as b84b0585, top of stack #292).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | Every document opens in preview mode: the page no longer reads the host's `initialEditMode`; edit mode is restored only for a reload of the same document whose saved state is edit (owner decision, 2026-11-03). The E key alone, outside a text field, enters edit mode. The unused `initialEditMode` field was removed from the host and the protocol. | b84b0585 |

Requirements: new SwRS LIFE-172 (`proposed`), LIFE-170 and TRUST-001 updated, a CHANGELOG line, indexes regenerated.

## Proof of completion

- `test/page/runtimeOpenInPreview.test.ts` (5 tests, two fail on the old `runtime.ts`), including "the same document keeps its edit mode when the page reloads".
- Changed assertions, on purpose per the owner decision: T38 in `runtimePageControls.test.ts` (saved state now decides, not the workspace choice), the disagreement test in `runtimeEditToggleRace.test.ts`.
- `just check` exit 0 (unit 3558, security 73), simulated `lifecycle-sync` 3 of 3. CI run 41649265544 green. Two rounds (round 1 left the fresh-panel gap), reviewer APPROVE in round 2.

## Open items

- The reviewer's nits: the "retired `initialEditMode`" assertion is vacuous; `setMode` in `src/page/features/editMode.ts` calls `setState` without `documentId`.
- The storage `setEditMode` / `storedEditModeForTests` in `src/host-vscode/testHooks.ts` is unused at start and can be removed in a follow-up.

# 231-incoming-changes-starts-in-reading-mode

Priority: P1 (stack -v5 blocker, approved by the owner via the CoS on 2026-10-31).

## Why

Test-only. The heavy stress run fails: scenarioIncomingChanges (test/integration/realWindowGaps.ts:186) assumes reading mode but never sets it, so after a scenario that leaves edit mode on, the side-by-side toggle is disabled and the click times out (run 41242116427, stress round 1/20).

## Done when

scenarioIncomingChanges calls leaveEditMode(page) right after waitForPreviewReady(document). The stress job gets past incoming-changes.

No behaviour gate: test-only, nothing a user sees changes.

# T39 implementation — round 3

STATUS: DONE

## Summary
Only empty groups are unlocked now, so a user's lock on another group can no longer be removed
(finding 1). A restored side preview owns its group's lock (finding 2). The focus restore is skipped
when the remembered group was a target (3). RI-T39 gained (f) and a restored-preview sub-case, and
(d) is tightened (4). README states that closing the preview releases the lock (5).

## Files changed
- `src/extension.ts`
  - `unlockPreviewGroup` rewritten: waits only while the group at `column` holds a `TabInputWebview` whose
    `viewType` includes `PANEL_VIEW_TYPE`; then waits 150 ms; targets are the group at `column` if it has 0 tabs,
    else every group with 0 tabs and no live preview. `adoptGroupLock` removed.
  - `deserializePreviewPanel`: `preview.lockedColumn = panel.viewColumn` for a side preview.
  - Focus restore skipped when `remembered` is a target; comment added.
- `test/integration/realInput.test.ts` — RI-T39 (d) tightened, (f), restored-preview sub-case.
- `README.md` — "The lock is released when the preview closes."

## Tests written first (failing before the fix)
- (d) last-group sub-case, with canary (a) temporarily commented out and the unlock disabled for t39 previews
  (round-1 behaviour): `AssertionError: a file opened after the last preview closed stayed in the single group  2 !== 1`
  — `logs/T39-r3-red-a-trusted.log`. (a) is restored.
- Restored-preview sub-case, with the `deserializePreviewPanel` line temporarily commented out:
  `AssertionError: a restored preview releases its lock too  2 !== 1` — `logs/T39-r3-red-b-trusted.log`. Line restored.
- (f): against the round-2 logic plus one 150 ms-less race, the user's locked group lost its lock
  (`logs/T39-r3-dbg-trusted.log`, debug lines `TEMPDBG before qo … 2:fourth-t39.md` then `other-t39.md` joined group 2).
  I did not keep a separate red copy of the full round-2 code.

## Tests added or changed
- (d) first sub-case now asserts `editorColumnOf(fourth) === sourceColumn`; the settle wait has the comment the review asked for.
- (f): three groups, user locks column 3, the preview in column 2 closes. Active group must not change for 600 ms; the
  locked group then refuses Quick Open (file lands in column 1, still 2 groups).
- Restored-preview sub-case via `deserializePreviewPanelForTests` (no reload, no new export): panel in `Beside`, group
  locked, deserialized, text editors closed, panel closed, `showTextDocument` keeps 1 group.

## Existing assertions changed
- `stockCoexistence.test.ts`, delayed Open With check: unchanged since the round-1 amendment.

## Verification
- `scripts/gate.sh T39-impl3 unit types full` → PASS (compile, unit, types, full 223 s) (`logs/T39-impl3-*.log`)
- Screen unlocked before each gate.

## Evidence for reviewers
- Red logs: `logs/T39-r3-red-a-trusted.log`, `logs/T39-r3-red-b-trusted.log`, `logs/T39-r3-dbg-trusted.log`.

## Feedback addressed (rounds 2–3)
- Finding 1: empty-only targets, poll limited to the preview's own tab, `adoptGroupLock` removed, (f) added.
- Finding 2: `deserializePreviewPanel` sets `lockedColumn`; tested through the seam.
- Finding 3: restore skipped when `remembered` was a target; comment added.
- Finding 4: (d) asserts `sourceColumn`; settle comment; round-1-style red recorded for the last-group case.
- Finding 5: README sentence.

## Open points / STOP reason
- The review's (f) text says the Quick Open from the locked group should create a third group. VS Code instead opens
  the file in the other existing group (2 groups), so (f) asserts that (not in the locked group, no new group).
- Not in the amendment: a 150 ms wait before computing targets. Without it, the focus command could land on the user's
  group that shifted into the closed group's column (the (f) failure above). An unlocked empty group closes by
  itself; one still present after the wait is the locked leak.
- Same settle-wait caveat as round 2 for the tests (unlock has no observable state).

# T39 review — round 2

Base: 0c5c352 · Reviewed diff: 4 files, +298/-5 (`src/extension.ts` +134, `realInput.test.ts` +160,
`stockCoexistence.test.ts` 6 lines, `README.md` +3)

## Gates
- unit, types: PASS (orchestrator).
- full: PASS, 222 s (`logs/T39r2-full.log`, extension host exit code 0). No new failure compared with
  the T00 baseline.
- visual: PASS against the baseline, 0 new failures.
- red: `logs/T39-impl-red-trusted.log` shows that canary (a) fails against round 1. The suite stops
  there, so (d) was never shown red. See finding 4.

## Done-when
- [x] Quick Open from the focused preview opens the file in the source group, and the preview stays
  visible. Evidence: RI-T39 (b) and screenshot `39-quick-open-beside-preview.png`. The screenshot shows
  2 groups, `other-t39.md` in group 1, the preview as the active tab in group 2, and the lock icon on
  group 2. No clipping.
- [x] Case B (Explorer entry) does not cover the preview. Evidence: RI-T39 (c), with 3 assertions.
- [x] The leak canary is in place. Evidence: RI-T39 (a), red in round 1.
- [~] Unlock on dispose. The leak case (the last group) is covered by RI-T39 (d). However, the unlock
  can hit a group the extension never locked (finding 1), and the lock still leaks after a reload
  (finding 2).
- [x] The README documents the lock.

## Unlock logic: user flows
Each flow notes whether focus moves visibly (focus), whether a lock leaks (leak), and whether a lock
the user set themselves can be lost (user lock).

- **(i) Source in group 1, preview in group 2; the user closes the preview.**
  - Group 2 empties and closes, and `groupAt(2)` is undefined.
  - The fallback finds no empty group, so it unlocks nothing.
  - Focus: none. Leak: none. User lock: safe.
- **(ii) The user closes the source group first, then the preview.**
  - The column is stale or 1. Either the direct target or the "empty, no live preview" fallback
    unlocks the single remaining empty group.
  - Focus: the editor area, which is the only group anyway. Leak: none (RI-T39 (d), last-group case).
    User lock: safe.
- **(iii) Three groups, preview in the middle (column 2); the user closes the preview.** **Wrong.**
  - Group 2 closes, and the old group 3 becomes column 2. `groupAt(2)` now exists and has tabs.
  - The poll spins for the full 500 ms, waiting for the tabs to leave.
  - Then `targets = [2]`: it focuses the **old group 3** and runs `unlockEditorGroup` on it, and only
    then restores focus.
  - Focus: a visible jump into the right-hand group, about 0.5 s after the close.
  - User lock: if the user had locked that group, their lock is silently removed. See finding 1.
  - The same happens whenever the preview's group closes and any group to its right shifts into
    its column.
- **(iv) The user closes the preview while the terminal or sidebar has focus.**
  - This only matters when a target exists, which is cases (ii) and (iii).
  - The unlock runs `focusNthEditorGroup`. The "restore" step then runs `focusNthEditorGroup` as
    well, which focuses an editor group. Keyboard focus therefore leaves the terminal or sidebar and
    never returns.
  - With finding 1 fixed, this happens only in the last-empty-group case. A careful user may still
    notice it there. See finding 3.
- **(v) The user drags the preview to another group, then closes it.**
  - `lockedColumn` follows the panel to the new group, so closing the preview later unlocks the
    *destination* group, which may hold a lock the user set.
  - If the source group kept other tabs, its lock leaks.
  - The amendment forbids drag handling, so the leak is accepted. Unlocking the destination group,
    however, is the same defect as (iii), and the fix in finding 1 removes it.
- **(vi) The window closes or reloads (P-L3).**
  - During shutdown, the `setTimeout(0)` work runs in an extension host that is going away, and
    `try`/`catch` absorbs it. Shutdown and restoration are not disturbed: the full gate's reload and
    serializer suites pass.
  - **But** `deserializePreviewPanel` never sets `lockedColumn`, while the workbench restores the
    group's lock state. After one reload, closing the restored preview leaks the lock again: this is
    the round-1 leak through another door. See finding 2.
- **(vii) Open With custom editors share the window.**
  - These editors never get a lock. `hasLivePreviewIn` and `adoptGroupLock` iterate over every
    `activePreviews` entry, including custom editors.
  - A custom editor sitting in a still-locked column adopts the duty to unlock it, which is harmless.
    The unlock is skipped while it is there.
  - Nothing here unlocks a custom editor's group that the user locked, as long as finding 1 is
    applied.
- **The stale-column fallback ("unlock empty groups with no live preview").** It is acceptable in
  practice: a locked group that is empty and holds no preview is almost always our leak. However, it
  can also unlock an empty group that the user locked on purpose. Keep it, but only together with
  finding 1's rule, so that non-empty groups are never touched.

## Case B and the reveal change
- `columnOutsideSidePreview` follows the amendment's order exactly: a visible text editor outside the
  preview's column, then any other group, then `Beside`. RI-T39 (c) covers it.
- `reveal(panel.viewColumn ?? Beside)`: when the source editor has focus and the user runs the palette
  command or the keybinding, the preview is revealed in its own group, which is the same place
  `Beside` used to resolve to. When the preview itself has focus, it no longer moves into a new split.
- `preserveFocus` behaviour is unchanged: the reveal still focuses the preview, as before.
- The P-L2 Open With checks in `stockCoexistence.test.ts` pass.
- Verdict on this part: correct.

## Panel replacement (`switchPreviewDocument`)
- `disposePreview(…, false)` does not unlock, and the replacement inherits `lockedColumn`.
- The old preview's `onDidChangeTabGroups` and `onDidDispose` subscriptions are released by the
  `panelSubscriptions` loop (`extension.ts:2176`), so nothing fires twice.
- Correct.

## Protected features checked
- P-L2 (Open With, priority option): `stockCoexistence.test.ts`, with the one amended assertion; full
  PASS.
- P-L3 (reload restores the side preview): `reload-suite.ts` and `serializer.test.ts` pass. However,
  the lock is not re-owned after a reload (finding 2).
- P-E (editing / `previewEditing`): passes. Deviations 1 and 2 were introduced precisely to keep it
  passing.
- Scroll pairing and following the active editor: RI-T39 (b) asserts that the preview follows
  `other-t39.md`; the toolbar scenarios pass.
- No webview runtime change, no message protocol change, and no read-only path touched. Checks 14 to
  16 do not apply.

## Findings
1. **[MAJOR]** `src/extension.ts`: `unlockPreviewGroup` unlocks a group that this extension did not
   lock.
   - Case (iii): the preview in the middle of 3 groups is closed, its group closes, and the group on
     its right shifts into `column`.
   - Case (v): the preview was dragged into a group that already existed.
   - In both cases the function focuses that foreign group for about 0.5 s and removes any lock the
     user put on it.

   Fix: only ever unlock **empty** groups. That is exactly the leak shape: VS Code keeps a group that
   is empty and locked.
   - Replace the poll and the target computation with this sequence:
     1. Wait up to 10 × 50 ms while `groupAt(column)` exists and still contains a
        `TabInputWebview` whose `viewType` is the preview's own type (the closing panel's tab).
        Do not wait for *other* tabs to leave.
     2. `targets` = `groupAt(column)` if that group exists **and** has `tabs.length === 0`.
        Otherwise, fall back to every group with `tabs.length === 0` and `!hasLivePreviewIn(...)`.
        A non-empty group is never a target.
     3. Drop `adoptGroupLock` and its call. An empty group has no live preview by definition, so
        `hasLivePreviewIn` can only be true for a non-empty group, which is never a target now.
        Keep `hasLivePreviewIn` only if the poll still needs it.
   - Tests: add RI-T39 **(f)**, three groups.
     - Open `smoke.md` in column 1 and the preview (column 2).
     - Open `fourth-t39.md` in `ViewColumn.Three` and lock column 3:
       `focusThirdEditorGroup`, then `lockEditorGroup`.
     - Close the preview tab and wait for it to close.
     - Assert that `groupCount() === 2` and that `vscode.window.tabGroups.activeTabGroup.viewColumn`
       did not change in the 600 ms after the close (poll it every 50 ms).
     - Run `focusSecondEditorGroup` (the `fourth-t39.md` group, now column 2), then
       `quickOpen("other-t39.md")`. Assert that it opens in a **new** group, so
       `groupCount() === 3`, which proves the user's lock survived.
     - Then run `unlockEditorGroup` in the `finally`.

2. **[MAJOR]** `src/extension.ts`: `deserializePreviewPanel`. A side preview restored by Reload Window
   has `lockedColumn === undefined`, while the workbench restores its group as locked. Closing the
   restored preview leaks the lock (the round-1 bug).

   Fix:
   - In `deserializePreviewPanel`, after the preview record is created, set
     `preview.lockedColumn = panel.viewColumn` when the preview follows the active editor (it is a
     side preview, not an Open With editor) **and** `panel.viewColumn !== undefined`.
   - This is safe once finding 1 is applied: `unlockEditorGroup` on an unlocked group is a no-op, and
     only empty groups are touched.
   - Test: in `test/integration/reload-suite.ts`, or in RI-T39 if a reload is too costly there, after
     the restore, close the restored preview while it is in the last group and assert that
     `showTextDocument` keeps `tabGroups.all.length === 1`.
   - If adding a reload test is out of scope, write a unit-level test of the deserializer that
     asserts `lockedColumn` is set, and state in the report that the reload path was checked by
     hand.

3. **[MINOR]** `src/extension.ts`: `unlockPreviewGroup` focus restore. The restore only re-focuses
   an *editor group*, so focus held by the terminal or the sidebar is lost.
   - After finding 1, this can only happen in the last-empty-group case.
   - Fix: skip the restore when `remembered` was the target. Then add a comment noting that focus
     outside the editor area cannot be restored through the API.
   - No test is required.

4. **[MINOR]** `test/integration/realInput.test.ts`: `scenarioPreviewGroupLock`.
   - The first sub-case of (d), "Quick Open from the remaining editor", passes even without any
     unlock: group 2 closes with its last tab. Its assertion `editorColumnOf(fourth) ===
     activeTabGroup.viewColumn` is close to a tautology. Assert `=== sourceColumn` instead.
   - The meaningful check is the last-group case. Record in the report that it fails on round 1, for
     example by temporarily commenting out canary (a) in a scratch run, or quote a log.
   - The 400 ms settle waits are shorter than the 500 ms poll ceiling. After finding 1 the poll only
     waits for the preview's own tab, which is gone before `waitFor("the preview to close")` returns.
     Keep 400 ms but add a comment stating that.
   - The 1 s wait at the start and the 400 ms wait in `finally` can stay. They only matter for leaks
     from the previous scenario, and canary (a) would surface any flakiness as a real failure, not
     hide it.
   - Shared helpers (`closeAllEditors`, `press`, `typeText`, `waitFor`) are unchanged: confirmed in the
     diff.

5. **[NIT]** `README.md`: "click the lock icon on the group to unlock it" does not say that the
   lock is also released when the preview closes. Add that sentence.

## Complexity vs risk
The machinery is close to safe. The two dangerous behaviours (finding 1) disappear with one rule:
"only unlock empty groups". That rule also removes `adoptGroupLock` and most of the poll logic.

The options, from the most to the least behaviour kept:

| Option | Fixes | Costs |
| --- | --- | --- |
| **A. Keep the lock and apply findings 1 and 2** (recommended) | UX-27 for Quick Open, the Explorer entry, and any other open from the focused preview. No leak in the last group, including after a reload. Never touches a non-empty group. | About 60 lines of focus and unlock code. A brief editor focus in the last-group case. An empty group the user locked on purpose can be unlocked by the fallback (rare). |
| B. Drop the lock; keep the Case B column fix and the reveal fix | The Explorer entry and the palette command never cover or move the preview. No focus juggling, no leak risk. | UX-27 for Quick Open, Go to Definition, search results and so on, opened while the preview is focused, comes back: they cover the preview. T39's main goal is not met. |
| C. Keep the lock but never unlock automatically (round 1 plus the README) | Same as A for opening files. | The leak in the last group comes back, so every later file opens in a new split. Not acceptable. |

If finding 1 cannot be made green in round 3, ship option B and split the lock into a follow-up.

## Existing assertions changed
- `stockCoexistence.test.ts`: the delayed Open With check now uses `.find(uri ===
  delayedDocument.uri)?.isActive`. This is exactly as the amendment specifies, and nothing else
  changed: **OK**.
- `realInput.test.ts`: only additions (the scenario, its call, and the `COMMAND_ID` import): **OK**.

## Report deviations
1. No unlock on `disposePreview(…, false)`, and the lock is handed over to the replacement: **accepted,
   correct**.
2. The 500 ms poll and the live-preview skip or adopt: **partly accepted**. The poll is the source of
   case (iii); restrict it as finding 1 describes.
3. The stale-column fallback and the extra `onDidChangeTabGroups` tracking: **accepted**, under
   finding 1's empty-only rule.
4. The settle waits: **accepted**, with finding 4's comment.

VERDICT: CHANGES REQUESTED

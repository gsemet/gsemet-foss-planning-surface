# T39 review — round 3

Base: 0c5c352 · Reviewed diff: 4 files under `src/markdown-okf-schema-studio`, +369/-5:
`src/extension.ts` +135, `realInput.test.ts` +229, `stockCoexistence.test.ts` 6 lines,
`README.md` +4.

The repository-wide stat reports 13 files. The 9 extra files are the `.agents/skills/...` and
`harness-gardening` files, which were already modified before T39 started. They are not part of this
task.

## Gates

| Level | Result | Evidence |
| --- | --- | --- |
| unit | PASS | orchestrator gate |
| types | PASS | orchestrator gate |
| full | PASS, 219 s | `logs/T39r3-full.log`, extension host exit code 0 |
| visual | PASS against the baseline, 0 new failures | orchestrator gate |

Red runs:

| Log | Failing assertion | Sub-case |
| --- | --- | --- |
| `logs/T39-r3-red-a-trusted.log` | "a file opened after the last preview closed stayed in the single group" | (d), last-group case, run against round-1 code |
| `logs/T39-r3-red-b-trusted.log` | "a restored preview releases its lock too" | restored-preview case, run without the deserializer change |

## Done-when

- [x] Quick Open from the focused preview opens the file in the source group.
  - Evidence: RI-T39 (b), which asserts `=== sourceColumn` and 2 groups.
  - Evidence: screenshot `real-input-oqM6AR/39-quick-open-beside-preview.png`.
- [x] Opening a file from the Explorer entry (Case B) leaves the preview visible: RI-T39 (c).
- [x] No lock leak, including in the last-group case and for a restored preview.
  - Evidence: RI-T39 (a) (the canary is active), the (d) last-group case, and the restored-preview
    case. Both red logs above confirm that these sub-cases detect the bug.
- [x] A lock the user set on a group to the right of the preview survives the preview closing, and
  focus does not move: RI-T39 (f).
- [x] The README states that the lock is released when the preview closes (line 144).

## Findings from round 2

1. **Fixed.**
   - `unlockPreviewGroup` waits only for a tab of the preview's own view type. The match uses
     `viewType.includes(PANEL_VIEW_TYPE)`.
   - It only unlocks groups that are empty (0 tabs).
   - `adoptGroupLock` is gone (0 occurrences).
   - RI-T39 (f) checks the user's locked group and checks that focus stays stable for 600 ms.
2. **Fixed.**
   - `deserializePreviewPanel` sets `lockedColumn` for a restored side preview.
   - The new sub-case goes through the `deserializePreviewPanelForTests` seam, as the amendment
     requires, and it is shown red without the fix.
3. **Fixed.**
   - The focus restore is skipped when `remembered` is one of the targets.
   - A comment explains that focus outside the editor area cannot be restored.
4. **Fixed.**
   - (d) now asserts `=== sourceColumn`.
   - The settle-wait comment is present.
   - The last-group case is shown red against round-1 code.
   - Canary (a) is active again (lines 2140 to 2148).
5. **Fixed.** The README sentence is in place.

## Open points from the report

- **(f) asserts "not in the locked group, no new group", not "a third group": accepted.**
  - With another unlocked group available, VS Code sends the editor there instead of creating a new
    split.
  - The assertion `editorColumnOf(other) === ViewColumn.One` still proves the user's lock survived:
    without the lock, the file would open in the active column 2.
- **The extra 150 ms wait before computing targets: accepted.**
  - It runs one tick after dispose, in the background, so the user never waits on it.
  - It lets VS Code auto-close an empty group that is unlocked. That makes "an empty group still
    present" a reliable sign of our locked group, and it removes the race in which the focus command
    lands on a group that has just shifted into place.

## User flows, re-checked against the new `unlockPreviewGroup`

- **(i) 2 groups; the user closes the preview.**
  - What happens: the group auto-closes, so the target list is empty.
  - Focus: does not move.
  - Lock: none leaks.
- **(ii) The user closes the source group first, then the preview.**
  - What happens: the single empty group that remains is unlocked. Focus is already in the editor
    area.
  - Lock: none leaks, as RI-T39 (d) shows.
- **(iii) 3 groups, the preview in the middle.**
  - What happens: the group on the right shifts into column 2, but it is not empty, so it is never a
    target.
  - Focus: does not move, as RI-T39 (f) shows.
  - User lock: kept.
- **(iv) The terminal or the sidebar has focus.**
  - What happens: focus moves only when an empty locked group is left over, which is case (ii).
  - Then the editor area takes focus, and that cannot be avoided through the API. It is acceptable,
    because the user has just closed the last editor.
- **(v) The user drags the preview to another group, then closes it.**
  - What happens: the destination group still has other tabs after the close, so it is never
    unlocked.
  - User lock: kept.
  - Lock: the source group's lock leaks if that group kept other tabs. That is accepted by the
    amendment, which forbids drag handling.
- **(vi) Reload or window close.**
  - Shutdown: the unlock runs in the background and is wrapped in `try`/`catch`.
  - Restore: a restored preview now owns its group's lock.
  - The P-L3 suites (reload and serializer) pass in the full gate.
- **(vii) Open With custom editors.**
  - They are never locked and never adopted.
  - A group that holds one is not empty, so it is never touched.
- **`workbench.editor.closeEmptyGroups: false`**
  - What happens: every empty group stays open, so each close of a side preview targets all the
    empty groups that hold no preview. The unlock focuses each of them in turn, then restores focus
    to the editor group the user was in.
  - Focus: the user can see a quick flicker. If focus was in the terminal, it ends up in an editor
    group.
  - User lock: an empty group the user locked on purpose would be unlocked.
  - Verdict: acceptable for a non-default setting, and nothing is lost. Logged as finding 1 (MINOR)
    below.

## Protected features checked

- **P-L2:** covered by `stockCoexistence.test.ts`. Only the one assertion change approved by the
  amendment, and the full gate passes.
- **P-L3:** covered by the reload and serializer suites in the full gate. The restored preview now
  owns its group's lock.
- **Preview editing and following the active editor:** covered by the full gate and by RI-T39 (b).
- **No change to the webview runtime, the message protocol, or read-only mode:** confirmed in the
  diff.

## Findings

1. **[MINOR]** `src/extension.ts`, `unlockPreviewGroup`: the setting
   `workbench.editor.closeEmptyGroups: false` causes two problems.
   - The stale-column fallback focuses, then unlocks, every empty group that holds no preview. Focus
     flickers, and an empty group the user locked on purpose loses its lock.
   - Follow-up: when `groupAt(column)` is not empty, read
     `workbench.editor.closeEmptyGroups`. If it is `false`, skip the fallback.
2. **[MINOR]** `realInput.test.ts`: the fixed 400 ms and 1 s settle waits remain.
   - They are documented, and the gate has been stable for three rounds.
   - Follow-up: replace them if the unlock ever exposes a test hook.
3. **[NIT]** No debug or temporary code was found: no `console.log`, no `.only`, no `skip`, and
   canary (a) is restored.

## Existing assertions changed

- **`stockCoexistence.test.ts`: OK.** The delayed Open With check now uses `.find(uri)`, exactly as
  the amendment specifies.
- **`realInput.test.ts`: OK.** The changes are additions only.

VERDICT: PASS

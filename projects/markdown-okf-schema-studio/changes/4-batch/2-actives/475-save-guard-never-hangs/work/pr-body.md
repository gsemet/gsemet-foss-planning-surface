## Summary

A block, table cell or frontmatter editor could stay on "Saving Markdown…" for good, and Cancel and Escape were ignored while it did. Cancel and Escape now always close a block or cell editor, even during a final save: the save the writer asked for with Done goes on and its text is kept. If that save then fails, or the file changes outside the preview before it is written, the editor reopens (or stays open) with the typed text and the reason. If the preview cannot show it again, VS Code offers a "Copy text" action. A frontmatter save that changes nothing no longer hangs on "Saved. Refreshing preview…". There is no time limit, no timeout message and no retry.

Related to #485 (the first hang of this kind, fixed by an earlier pull request).

## Deliverables

```mermaid
sequenceDiagram
    participant W as Writer
    participant P as Page
    participant H as Host
    W->>P: Done
    P->>H: previewEditSave (final)
    W->>P: Escape or Cancel
    P->>H: previewEditClosed (detached)
    Note over P: editor closed, detached save recorded, other edit gestures wait
    alt save written
        H->>P: previewEditSource done (renderFollows)
        P->>P: the block or field clicked meanwhile opens
    else failure or file changed outside
        H->>P: previewEditSource error + unsavedText
        P->>H: previewEditReopen (reopened: true)
        Note over P: editor reopens with the typed text and the reason
    else page cannot show it
        P->>H: previewEditReopen (reopened: false)
        H->>H: warning with a "Copy text" action
    end
```

| Situation | Before | After |
| --- | --- | --- |
| Cancel or Escape during "Saving Markdown…" | ignored | editor closes, the save goes on |
| Cancelled save fails or file changed outside | text lost or editor stuck | editor reopens with the text and the reason, or "Copy text" |
| Editor on "Saving…" and the file changes outside | edit released silently, text lost | editor stays open with the text and the reason |
| Frontmatter save that changes no text | stuck on "Saved. Refreshing preview…" | field closes, no message |
| Other edit gestures during an edit in flight | only while an editor is open | also while a cancelled save is not finished |

Choices: the end of a cancelled save is only an answer naming its edit (`done` or an error), so a render already in flight cannot end it early; the host answers every end; a retry from a reopened editor keeps the first save's identity so the host accepts it; `HostUi.showWarning` gains optional actions, and only the VS Code adapter calls `vscode.window`.

## Blast radius

Grade: **2**. The page's edit state, the host's edit lock, three protocol messages and the `HostUi` port change; the editing paths are covered by new page, host and protocol tests. Reverting the commit restores the previous behaviour.

## Autonomous decisions

- `previewEditSource` stays addressed to the document (as it is routed today) rather than to the render, so a pending render does not delay it.
- `previewEditClosed` carries a `detached: true` flag, so the host tells a detach from a normal close after an error.
- An open that arrives while a cancelled save is in flight is held at most once on the page and on the host.
- The host releases a detached edit on `onReady` only when the page reports no block editor open; the page reports one while a detached save is in flight, so the edit is kept until its answer.
- The real-window step moved to `test/integration/detachedSaveWindow.ts` because `previewEditing.test.ts` reached the file-size limit.

## Known gaps

- **UNVERIFIED:** the real VS Code scenario (Done, Escape with the apply held, release) is written and compiles but was not run locally; it runs in the heavy CI.
- If the host's render never arrives after `done` with `renderFollows`, the page keeps the detached-save record.
- The new page and host tests were run against the previous `src/`: 44 of 95 fail there (detached-save close and reopen for paragraph, cell, insertion and blank lines; frontmatter unchanged save; Escape during a cell save). The gesture-guard tests (block move, delete, paste, checkbox, row and list-item drag, file drop, replace) pass on the previous code, because it has no detached save for them to wait on; they guard the new state only. The new session test file does not compile against the previous code, so it was not run there.

<details>
<summary>Details</summary>

## Changes

- `src/page/features/detachedSave.ts`, `detachedSaveState.ts`: the detached save record, its end on an answer naming its edit, the `editInFlight()` guard, the pending open, the reopen.
- `src/page/features/blockEditor.ts`, `tableCellEditor.ts`: Cancel and Escape close the editor during a final save and post `previewEditClosed`.
- Edit gestures (block moves, delete, paste, replace, file drop, row and list-item drags, frontmatter openers) check `editInFlight()`.
- `src/session/features/detachedEdits.ts`, `blockEdits.ts`, `hostEvents.ts`, `rendering.ts`, `pageMessages.ts`: detached edit handling, every end answered, outside change keeps the text unwritten and the page editor locked until `previewEditReopen`, "Copy text" warning.
- `src/session/features/frontmatter.ts`: a save whose plan changes no text answers `saved` with `unchanged`; the page closes the field.
- `src/core/protocol/*`: validators for `previewEditSource`, `previewFrontmatterResult` and the new `previewEditReopen`; 20 MB bound shared with the content patch.
- `src/host-api/hostUi.ts`, `src/host-vscode/vscodeHost.ts`: `showWarning` accepts action labels.
- Requirements: BLOCK-053, 216, 191, 041, TABLE-025, FMEDIT-019 and StRS BLOCK-006 updated, new SwRS BLOCK-270; glossary "Detached save" and "Edit in flight".
- The page test "Cancel and Escape are ignored while the final save is in flight" is rewritten to the new rule (owner decision); its intent changes on purpose.

## Human decisions

- Cancel during "Saving…" closes the editor and the save goes on; its text is kept.
- A cancelled save that fails, or a file changed outside, reopens the editor with the typed text and the reason; a block or field clicked meanwhile opens when the save ends and is dropped on a failure.
- A frontmatter save that changes nothing closes the field with no message.
- Other edit gestures wait until the save ends.
- When the preview cannot show the failure, VS Code offers a "Copy text" action.
- No time limit, timeout message or retry.

## Impacts

Behaviour change in the editors: Escape and Cancel close the editor during a save; failures keep the typed text.

## Test plan

- [ ] New or changed tests (they fail on the previous code)
- [ ] Requirements: SwRS updated or added, markers in code and tests, `just requirements-update`
- [ ] Changelog: one user-facing line under `## Unreleased` in `CHANGELOG.md`
- [ ] Local gates: `just check` pass, `just preflight` (static stage on Windows) pass; to be re-run on the final head
- [ ] Review
- [ ] CI green

## Internal references

CR-475 save-guard.

</details>

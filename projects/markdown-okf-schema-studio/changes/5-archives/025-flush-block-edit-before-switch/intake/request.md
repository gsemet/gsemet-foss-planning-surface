# Flush the open block editor before any document switch (P1, decided 2026-10-22)

From the T11 review (feature session 007–020): text typed in an open block editor before its first
autosave (400 ms) lives only in the page. A cross-document Back, a link to another file or a tab
switch in that window can drop it — user data loss.

Fix: save (flush) the open block/cell/frontmatter editor synchronously before any navigation or
document switch in the preview, and on webview hide/dispose. Add a real-input scenario: type, then
immediately follow a link to another file; the text must be in the source document.

## Decisions (user, 2026-10-22)

- Triggers (all): a link to another file, cross-document Back/Forward, the preview following the
  active editor (tab switch), window close / Developer: Reload Window (pagehide and
  visibilitychange flush exist in scrollSync.ts ~2603: prove them with a test, fix if broken).
- After the flush: save and close the editor; it is not reopened when coming back.
- Invalid content (broken frontmatter YAML, a table cell mid-edit): write it as typed, like the
  autosave; the preview then shows the error. No data loss, never block the navigation.
- Ordering: the host applies the pending edit (awaited) before it switches document. No race.

## Decision (user, 2026-10-22 evening)

5. Back (and Forward) while a block editor is open: save the typed text, close the editor, then move
   the history one step. Update the existing test `test/integration/previewHistory.test.ts:156`
   ("Back moved the history while a block editor was open") to assert that: text saved, editor
   closed, history moved by one. Its intent (never lose text) is kept.

6. Rounds: 9 (7 done + 2 granted by the user on 2026-10-22 22:30). After round 9 without green CI: blocked, ask the user.

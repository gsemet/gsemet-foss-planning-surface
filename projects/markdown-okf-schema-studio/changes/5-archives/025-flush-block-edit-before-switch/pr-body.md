## Summary

Fixes a **data loss**. Text typed in an open editor (paragraph, table cell, property) lived only in
the page until its 400 ms autosave. Following a link to another file, going Back or Next,
switching editor tab, or reloading or closing the window right after typing could drop it.

The open editor is now **saved and closed first**, and the preview switches document only once the
edit is applied.

## Behaviour (user decisions)

| Trigger | Before | After |
| --- | --- | --- |
| Link to another file | text typed < 400 ms ago lost | saved, editor closed, then navigate |
| Back / Next to another document | refused ("Finish the open block edit") or lost | saved, editor closed, then navigate |
| Editor tab switch / Open Preview on another file | lost | host asks the page to flush, waits for the edit (bounded 1.5 s), then switches |
| Window reload / close (pagehide, hidden) | only a pending block autosave was flushed | the block, table cell and property editors are all flushed |

- **Invalid property values are written as typed on a flush**: invalid YAML, a value outside the
  schema, or a bad number. The preview then shows the validation error. A normal save keeps its
  refusals.
- **When nothing can be written** (stale field, duplicate key, required field removed), a VS Code
  warning names the field, so the text is never lost silently.
- **A → B → A** within the wait ends on A: only the latest requested document wins.
- Same-document anchors, read-only and untrusted previews are unchanged. Each saved edit is one
  undo step.

## Changes

- `src/webview/scrollSync.ts`, `linkNavigation.ts`, `historyControls.ts`: `flushOpenEditors()`
  runs before a navigation message and on hide.
- `src/extension.ts` + new `src/preview/flushWait.ts`: the host awaits the pending edit before it
  switches. It adds a `previewFlushEdit` / `previewEditFlushed` handshake (in the message
  registry), the `LatestRequest` ordering and the bounded waits.
- CHANGELOG bullet.

## Screenshots

SCREENSHOT_SECTION

## Test plan

- [x] Unit: 15+ new tests covering the flush on navigation and hide, the ordering, the bounded
  wait, refusal warnings and key trimming. Each fails on the previous code where applicable.
  1725 unit tests pass; `just check` and `just visual` (255) are green.
- [x] Sonnet review: rounds 1 and 2 asked for fixes (property loss on schema refusal, A → B → A,
  blur vs flush in scenarios, frontmatter on reload, silent refusal); round 3 approved.
- [ ] CI real-input scenarios: link, Back, tab switch, table cell + property, invalid and
  schema-invalid YAML (they need VS Code windows, CI only).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

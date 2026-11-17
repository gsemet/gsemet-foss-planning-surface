# T09 review — round 1

Base: 27c7aff · Reviewed diff: 6 files (4 modified + 2 new), +330/-3

## Gates
- unit: PASS · types: PASS · compile: PASS (orchestrator summary)
- trusted: PASS (logs/T09-trusted.log, exit 0)
- scroll: PASS (logs/T09-scroll.log, exit 0). The implementer's first scroll run timed out
  before any test body; the orchestrator's run is clean. No new failure compared with the T00 baseline.

## Done-when
- [x] Typing writes after 400 ms of inactivity — `AUTOSAVE_DELAY_MS = 400`, debounced
  `autosaveBlockEdit`; test "typing is saved once after the autosave delay, carrying the last text".
- [x] Blur / Escape / Cmd+Enter / edit mode off / block navigation flush immediately — all go
  through `postBlockEditSave(true)`, which now clears the timer first; test "blur after typing posts
  one final save and clears the autosave timer"; the Escape test still passes.
- [x] Table cell switch flushes immediately — `switchTableCell` calls `postBlockEditSave(false)`;
  test "switching table cells posts the pending change immediately".
- [x] Minimal replacement — `minimalReplacement` (CRLF and surrogate safe, 200 seeded random pairs)
  used in `drainActiveBlockEdit`; offsets relative to `sourceStartOffset`, which is valid because the
  stale guard checks that `lastSavedText` sits at that range first.
- [x] RI-T09 passes; before: 20 whole-block changes (rangeLength 18..37), after: 1 change
  `{"rangeLength":0,"textLength":20}`, one undo restores `Second paragraph.`
  (evidence `.artifacts/real-input-VhQmyW/15-typing-undo-grouping.md`).
- [x] Unit, trusted, scroll gates pass.

## Protected features checked
- P-E3 (autosave, line breaks, trailing line ending): message content unchanged
  (`edit.textarea.value + trailingLineEnding`); "raw Markdown block edits autosave on input…" still
  asserts `"Continued typing\n"` after `flushTimers()`.
- P-E6 / stale-source guard: `source.document.getText(source.range) !== edit.lastSavedText` check kept
  verbatim before computing the replacement; `applying`/`pendingText` coalescing unchanged.
- P-E8 (read-only): no new entry point; the timer is only armed from existing editor `input`
  listeners, which exist only when an editor opened.
- P-S2: no new message type or field.
- One active edit / `finishing` / `pendingBlockNavigation`: the timer callback checks
  `activeBlockEdit === edit`; `postBlockEditSave(false)` still returns early when `finishing`.
- Webview template (§2): no backtick, no `${`, no backslash added; `window.setTimeout`/`clearTimeout` only.

## Findings
1. [MINOR] src/webview/scrollSync.ts:autosaveBlockEdit — if the webview is disposed (panel closed or
   reloaded) less than 400 ms after the last keystroke without a blur, that last burst is never posted;
   before T09 every keystroke had already been sent. Follow-up: on `pagehide`/`visibilitychange` to
   hidden, call `postBlockEditSave(false)` when `activeBlockEdit.autosaveTimer` is set, with a unit test
   dispatching that window event after an `input` and asserting one `previewEditSave` without
   `flushTimers()`. Not blocking: the task's flush list does not include disposal.
2. [NIT] src/extension.ts:drainActiveBlockEdit — the empty-replacement branch is unreachable (the
   earlier `editedText === edit.lastSavedText` check already returns), harmless.

## Existing assertions changed
- scrollSync.test.ts "fenced Markdown editors sit outside the rendered pre…": `flushTimers()` added
  before the `editedText` assertion; content unchanged — OK.
- scrollSync.test.ts "raw Markdown block edits autosave on input…": `flushTimers()` added twice;
  assertions unchanged — OK.
No assertion removed or weakened.

VERDICT: PASS

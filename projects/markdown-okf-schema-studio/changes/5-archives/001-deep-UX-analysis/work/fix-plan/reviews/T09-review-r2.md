# T09 review — round 2

Base: 27c7aff · Reviewed diff: 5 tracked files + 2 new, +391/-20 (round-2 delta: `flushPendingAutosave`,
two listeners, harness `visibilityState`, 3 tests)

## Gates
- compile/unit/types: PASS (orchestrator; reviewer reran scrollSync.test.js: 78 pass, 0 fail)
- trusted: PASS (logs/T09-trusted.log) · scroll: PASS (logs/T09-scroll.log). No new failure vs T00.

## Done-when
- [x] All round-1 criteria still met; round-1 tests unchanged and passing.
- [x] r1 finding 1: pending burst flushed on `pagehide` and `visibilitychange` → hidden — tests
  "pagehide flushes a pending autosave…" and "visibilitychange to hidden flushes…".

## Protected features checked
- P-E3: flush reuses `postBlockEditSave(false)`; same payload; no-op when text equals `lastPostedText`.
- P-E6 / finishing: `postBlockEditSave(false)` still returns early while `finishing`; flush only acts
  when `autosaveTimer` is set, so no extra save without pending input (negative test covers it).
- P-E8: listeners act only when `activeBlockEdit` exists; inert in read-only mode.
- P-S2: no new message type. Template §2: no backtick, `${` or backslash added; `window`/`document`
  listeners registered once at script top level.

## Findings
1. [NIT] Tests not recorded failing before the fix. Judged meaningful anyway: they call no
   `flushTimers()`, so without the listeners the 400 ms timer stays pending and the save count is 0
   (assertion `saves.length === 1` fails). No action needed.
2. [NIT] (carried from r1) unreachable empty-replacement branch in `drainActiveBlockEdit`. Harmless.

## Existing assertions changed
- Same as round 1 (`flushTimers()` additions only) — OK. None weakened in round 2.

VERDICT: PASS

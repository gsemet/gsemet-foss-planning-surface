# Specification: 423-edit-mode-commit-latency

## Summary

Shorten the commit round trip of edit mode on a large document: the render after a committed
block edit starts at once, and the table handles are no longer placed while the page is patched.

## Scope

1. `src/core/render/buildQueue.ts`: `request` and `refresh` take `{ immediate }`; an immediate
   request starts without the adaptive wait (a running build still finishes first).
2. `src/session/features/rendering.ts`: `refreshPreviewDocument` passes the option on.
3. `src/session/features/blockEdits.ts`: `completeActiveBlockEdit` (the editor closes on an
   applied edit) asks for an immediate render. Typing keeps the adaptive wait.
4. `src/page/features/tableRowMove.ts`: `refresh` places the handles in the next animation frame
   instead of synchronously; `reposition` (width mode) stays synchronous.

## Tests

Each test fails on the code before the change:

- `test/node-services/build/buildQueue.test.ts`: after a 300 ms build, an immediate request starts
  at 0 ms, supersedes a typed edit waiting 600 ms, and waits for a running build.
- `test/page/runtimeTableRowMove.test.ts`: the handles have no position right after edit mode is
  switched on, and are placed after the next frame.

Requirements: SwRS-LIFE-039 normative change (render at once after a commit, one scenario row);
TABLE-002 verification note.

## Measured (clone of the user's environment, chapter 08)

| Commit | Before | After |
|---|---|---|
| 1st | 1,930 ms | 543 ms |
| 2nd | 1,134 ms | 394 ms |
| 3rd | 590 ms | 391 ms |

## Out of scope (follow-ups)

- A single read phase in `closeBlockEdit` without the `documentElement` attribute toggle.
- Parsing the rendered HTML once on the host (`contentPatch.ts`, `propertiesTable.ts`).
- The block editor open time (~670 ms in the user's environment).

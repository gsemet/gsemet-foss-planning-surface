# CR 180 review, round 1 (Inspector)

Verdict: **APPROVE** (no blocking items; non-blocking notes below).

Scope reviewed: uncommitted diff in `markdown-okf-schema-studio-wt-180` (7 files, +177/-3).

## Gates run

- `npm run compile`, `npm run check-types`: clean.
- `out/test/page/modules/editPalette.test.js` + `out/test/page/runtimeEditPalette.test.js`: 126/126 pass.
- `check:limits` passed (849 files, 0 on baseline); `check:markers` ok; `check:exports` ok.
- `okfreq update-coverage requirements --check` (main venv): 0 files would change.
- `check:boundaries` not runnable locally (dependency-cruiser refuses Node 25.4; `.nvmrc` = 24).
  The diff adds no cross-layer import (`previewGroupFocusMovesForTests` already exported by
  `test/integration/extensionApi.ts`).

## Findings

- No product behaviour change: the blur handler in `blockSourceEditor.ts` keeps the same three
  outcomes (kept-in-frame, kept-for-dialog, commit) and only records a trace entry; the window
  `mousedown` listener in `pageDiagnostics.ts` only records.
- CI rule 12: no sleep, retry, raised timeout or weakened assertion. The new wait before the
  WARNING click polls a page-reported state (textarea active, `document.hasFocus()`, type list
  open) and wraps no action, so it is a readiness signal, not a retry. It cannot mask the bug: a
  commit-on-blur closes the editor, so the textarea is never active again and the wait fails with
  the full dump. Failure messages now carry steps with times, page trace offset, host document
  state, extension focus moves and the window/page focus report with the trace.
- The diagnostics target the logged signature (`page blur active=body pageFocus=false` then
  `content patch` then `block editor closed`): the new `block editor blur related=... <outcome>`
  entry and the `mousedown` entry will tell whether the commit came from a press in the page or a
  focus theft from outside.
- Requirements: `SwRS-MDOKFSTUDIO-BLOCK-047.md` change is only the generated `tested_in_files`
  entry (matches the new `@tests_req` marker; coverage check is clean). SwRS tier, not a locked
  StRS. Markers (`@tests_req SwRS-MDOKFSTUDIO-PALETTE-036`, `...BLOCK-047`) are placed on tests that
  assert the requirement's behaviour.
- The runtime trace tests would fail without the new trace code (they assert the exact
  `mousedown` and `block editor blur` details); the BLOCK-047 characterization asserts one final
  save with the expected text.

## Non-blocking notes

1. The three new tests in `test/page/modules/editPalette.test.ts` pass on unchanged code
   (rules.md: "new tests must fail on the unchanged code"). They are characterization tests that
   rule out the backlog suspect (line map targeting the marker line); acceptable for a
   diagnostics-only CR, but say so in the report/PR.
2. In "a press on a type option is cancelled, traced and never saves", the "no commit" and "no
   block editor blur" assertions are vacuous in the harness (no blur is ever dispatched); only the
   trace and `prevented=true` assertions carry weight. Consider dropping or rewording.
3. `explain()` awaits `readEditor()` and `pageTraceStart()` unguarded; if the frame detaches
   during the dump, `evaluate` throws and the original timeout is lost. Wrap the dump parts in
   try/catch (as `windowFocusReport` does).
4. The window `mousedown` listener runs in bubble phase: a press whose handler calls
   `stopPropagation` is not traced. Fine for palette options today; a capture-phase listener
   reading `defaultPrevented` would miss later handlers, so keep as is but note the limit.
5. This round does not fix the flake: root cause (window blur fires a textarea blur with no
   related target, and BLOCK-047 commits) is plausible and characterized but unproven. The PR must
   not claim a fix; stress proof and a product decision on commit-on-window-blur (rule 12: "fix the
   product") remain open once the new trace catches a failure.

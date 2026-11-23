# Diagnosis, PR #483 at 19443627

Both reds are test-side defects of the round; no product bug.

## 1. Linux unit: plantUmlRenderer "abort also kills the process group..." (got [] expected [-424243])

Cause: `renderPlantUmlDiagrams` now awaits `findEscapingPlantUmlInclude(options.files, ...)` (async
port, src/core/render/plantUmlRenderer.ts ~line 505) before it spawns. The test calls
`controller.abort()` synchronously right after starting the render, so the signal is already aborted
when the spawn is reached: `renderSource` returns at `signal?.aborted` (line ~319) without spawning,
so no child exists and `process.kill` is never called (calls = []). Before, the include check was
synchronous, so spawn happened inside the same tick and abort hit a live child.
The sibling test "cancels an active PlantUML process" was already fixed in the round with a `started`
promise resolved by the fake spawn (awaited before abort); this test was not. It is skipped on
win32 (`process.platform === "win32"` return), which is why it passes locally and only Linux fails.
Evidence: ci.log line 1869 / 5050; test/core/render/plantUmlRenderer.test.ts lines 366-395 vs 202-230.

Fix (test only): in the test at line 366, give the fake spawn a `started` promise as in the
"cancels an active" test (`withFake(() => { spawned(); return child; }, ...)`), and `await started`
before `controller.abort()`. Expected calls then [-424243] and child.killed true.

## 2. Visual campaign: figure images "(no src)", `img[src^="file:"]` 0 matches (fixtures 03, 05, 29, 32-34, 52, 54, 67, 68, 70, 77, 87...)

Cause: test/visual/renderFixtures.ts (renderPage) was converted to `policy.resolvePrimed` but its
priming is incomplete. It runs `sanitize()` first with no `policy.prime(...)` before it. The policy
roots are canonicalized lazily in `open()`, which only `prime`/`resolveResourceDetailed` call. With
`roots = []`, `resolvePrimed` decides "resource-outside-root" (a refusal, not `need`), so the request
is NOT added to `unprimed`; `takeUnprimed()` returns [] and the retry loop breaks at pass 0. The
images stay unresolved, the sanitizer drops the src ("no src", zero `file:` imgs). Same for every
fixture with a local image; not Linux-specific, the visual job is just the only place that runs it.
The host (src/session/webview.ts line 290) does it right: `await policy.prime(likelyResourceRequests(
sphinxHtml, outputDirectory))` before the first pass, which opens the roots and fills the memo.
Proof: probe-prime.js (this folder; run `node probe-prime.js <worktree>` after compile):
  pass 1 (no prior prime): undefined
  takeUnprimed after pass 1: []
  after explicit prime: <path of a.png>
Also affected: 87 export (embedded data images missing) and 33 "right figure 40 %" are consequences.

Fix (test only, renderFixtures.ts around lines 159-168): before the first `sanitize()`, call
`await policy.prime(likelyResourceRequests(html, documentDirectory))` exactly as webview.ts does
(export `likelyResourceRequests` use as the host does), or at minimum `await policy.prime([])` to open
the roots, then keep the takeUnprimed retry loop. Optional hardening in src: make `resolvePrimed`
list the request in `unprimed` (or refuse loudly) when `open()` has not run, so a caller that forgets
to prime cannot silently get "outside root".
Also `policy.diagnostics.length = 0` should stay as is (pre-first-pass count is 0 after prime too).

Not touched: static-windows and viewer-graph pass (no visual image use).
Fast gate: nothing changed in the worktree; no code run beyond the probe.

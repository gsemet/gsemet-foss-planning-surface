# 041 — CI stability after the night merge

User (2026-10-23): "tout merger et faire un correctif après" — the 10-PR stack was merged without
waiting for CI (ebe7b2b). This CR brings main back to a green, reliable CI.

## Decisions (user + recommendations accepted earlier)

1. Fix root causes, never raise timeouts or weaken tests ("rocket solid").
2. Flush scenarios race (`webviewReady`): `scenarioFlushFrontmatterKeptAsTyped` case 2 (no
   `[data-okf-frontmatter-editor] textarea` after Control+A; seen on PR #23 run of 2026-10-23
   07:29Z) and `scenarioFlushCellAndFrontmatter` (test/integration/realInput.test.ts ~4089).
3. Other flakes seen tonight: "StRS-A link has a box", "Tab opens second cell" timeout.
4. Add `timeout-minutes` to every CI job (integration 30, others 15, report 10) so a hung job
   fails fast (integration hung 3 h on main run 39916946924).
5. Whatever else is red on main after ebe7b2b (run the CI on the PR and fix each failure's cause).

## User request, 2026-10-23 ~11:30

"PR #35 must be rebased (#34 merged). Start an Opus sub-agent to fix it properly so that flaky
tests are never a problem again."

6. Driver, coders and reviewers of this CR run on **Opus**.
7. Round 2 restarts on Opus from a fresh root-cause analysis. The r1 theory (deferred host work)
   does not explain CI run 39930593934: the frontmatter editor vanished after Control+A with
   `page loads 0, content patches 0`. Find the real cause with evidence (logs, instrumentation),
   not guesses.
8. "Never a problem again" means structural: tests wait on deterministic readiness signals from
   the extension/webview, never on sleeps; a stress mode reruns the flaky-prone scenarios N times
   to prove stability (locally on CI, not in a VS Code window on the user's machine); a CI rule in
   `ci.guidelines.md` describes how a flake is handled (root cause, never retry-to-pass).
9. rounds: 6 (user, 2026-10-23 ~11:40: "ok pour 3 essais", 3 rounds added to the original 3).
10. User, 2026-10-23 ~14:45: go faster. The main session committed the r4 work in progress
    (9243cf5) to test it on CI. The `stress` job is advisory (`continue-on-error`, not in
    `checks`); static, visual, integration and report stay required and run in parallel.
    Coder gates: tsc + unit only; reviewer checks only the round diff.

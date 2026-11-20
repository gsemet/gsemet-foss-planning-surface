# Efficient mutation testing in Studio (P1, next batch)

Priority: P1, for the next batch (batch-07). Owner's request, 2026-11-20: "comment faire du mutation testing efficace dans Studio ?"

Goal: know whether the unit tests really catch regressions, not only that they run the code. A
mutant is a small change to the code (a `<` into `<=`, a `true` into `false`, a deleted call);
a test suite that stays green on a mutant has a hole.

What exists today (main 049b543):
- about 70k lines of TypeScript in `src/`, of which `core` (156 files) and `page` (126 files)
  hold most of the logic and are pure (no VS Code);
- unit tests run on `node:test` over the compiled `out/` (`npm run test:unit`), in a few
  minutes in the CI static job; contract tests in `out/test/core/render/*.contract.js`;
- `@implements_req` / `@tests_req` markers tie code and tests to SwRS requirements (okfreq);
- no mutation tool yet.

"Efficace" means, to be settled in the grill:
1. Scope: the changed lines of a PR (incremental), not the whole repository on each run; a
   full run at most nightly or on demand. First layers: `core` and `page`; never `host-vscode`
   or the real-window tests.
2. Tool: StrykerJS (mutant schemata: one compile for all mutants; `--incremental`; TypeScript
   checker to drop mutants that do not compile). The open point is the runner for `node:test`
   (command runner = whole suite per mutant, slow; tap runner; or a per-file runner with
   coverage to run only the tests that reach the mutant).
3. Signal, not noise: exclude logs, message strings, and equivalent mutants; a score per
   layer and per SwRS requirement (a survived mutant in code marked `@implements_req X` = a
   test missing for X), rather than one global percentage.
4. Where it acts: a CI job on the PR (report, not blocking at first, then a floor on new
   code); and in the chantier cycle, the Verifier or Inspector reads the survived mutants of
   the round's diff and asks for the missing test.
5. Budget: target time per PR (for example under 10 minutes) and per nightly run.

Out of scope here: the e2e / real-window tests; fixing all survivors of the existing code at
once (it becomes a backlog of gaps, by requirement).

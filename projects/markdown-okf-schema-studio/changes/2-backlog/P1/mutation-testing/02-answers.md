
## Grill, 2026-11-21

Decided by the Chief of Staff under the owner's autonomy rule (owner, 2026-11-20: "tu es maintenant autonome. plus de question. tu grilles tout seul avec un fable"; 2026-11-21: "Ensuite les autres P1 et inbox de Studio?").

- mt-Q1 Tool: StrykerJS with its TypeScript checker. Per-test coverage through a small node:test adapter (a Stryker test-runner plugin in the repo, under scripts/ or test/tools/). Round 1 proves the adapter on a few core files first. Fallback if per-test coverage cannot work: map each mutated file to the test files that import it (static), and say so in the report.
- mt-Q2 Where it runs: locally, a just target (for example just mutation-core), report in out/reports/mutation/. No CI job, no workflow on PRs: it is one-shot (owner's words). If the full core run exceeds about 6 h on the dev machine, run it on a recorded sample of files and say so.
- mt-Q3 Reading: score per core sub-folder and per SwRS (from @tests_req markers); list of redundant tests by killed mutants; holes. Log calls and user-facing message strings are excluded from mutation.
- mt-Q4 Shape: one PR for core: the tool, the agent read of the tests (no-assert, does-not-throw-only, near-duplicates), the removals and merges, the new tests for holes that matter, and a list of holes judged not worth a test with one line each.
- mt-Q5 Every requirement stays covered: a removed test with @tests_req moves its marker to a test that stays and covers the same SwRS; just requirements-update shows no loss. No published requirement is removed.
- mt-Q6 The note for chantier (command, scope, report reading, removal rules, run time) is written in the CR folder as evidence; the CoS sends it to chantier's CoS for mutation-testing-driver.

## Owner's answers, 2026-11-21 (asked by the Chief of Staff)

- mt-Q2 confirmed by the owner: "Local `just` target" (no CI job).
- mt-Q4 CHANGED by the owner: redundant tests are "List only, remove nothing". The PR adds the tool, the report, the list of redundant tests (by killed mutants) and the tests for the holes that matter; no test is removed or merged in this CR. Removals wait for the owner's review of the list.
- mt-Q7 (TypeScript 7 vs Stryker's checker, which needs the TS 5 compiler API). Owner, 2026-11-21: "Find another solution to stay on TS7. No compromise". So: no TypeScript 5 anywhere (no npm override, no second compiler), and no run that silently skips the type check. The spec finds a TS 7 path: for example a small custom Stryker checker plugin that type-checks mutants with TS 7's own compiler (its CLI or its new API), or another mutation tool that works with TS 7. Round 1 proves it on a few core files.

# Mutation testing campaign on `src/core`: fewer tests, no holes

Run StrykerJS once over `src/core` and the unit and contract tests that reach it. Remove or merge
the tests that kill nothing new, add the few tests the surviving mutants call for, keep every
requirement covered, and write down how the campaign ran so chantier can write a Mutation Testing
Driver from it. One-shot: no CI job, no check on pull requests.

Origin: verbal (owner, 2026-11-20). No tracker issue. Code read at `main` `a18bcac1`; `origin/main`
is now `5a84db8b` (release 1.11.0): the Driver starts from the latest `origin/main`. Every decision
below comes from `02-answers.md` (mt-Q1..Q6), **decided by the Chief of Staff under the owner's
autonomy rule**; the PR body says so. Part 1 of 2: `mutation-testing-rest` runs the same campaign
on everything else after this one lands.

## 1. Goal, in the user's terms

- Studio's test suite gets smaller and catches as much or more: the tests on `core` that prove
  nothing another test does not already prove are gone or merged, and the code that no test
  checks gets the few tests it needs.
- No requirement loses its test: every SwRS covered today stays covered.
- chantier gets a written account of a real campaign (command, scope, how the report was read,
  rules for removing a test, time taken) to write its `mutation-testing-driver` role.

## 2. Facts the design rests on (main `a18bcac1`)

- `src/core`: 157 `.ts` files, about 30.5k lines, in 19 sub-folders (largest: `render` 8.4k,
  `preview` 6.8k, `frontmatter` 3.6k, `security` 1.6k, `protocol` 1.6k, `mapping` 1.3k). No
  `console.*` or logger call exists in `src/core` today.
- Tests: `node:test` over the compiled `out/` (`npm run compile` = `tsc -p .`), launched by
  `scripts/node-test.mjs <suite> <pattern>...`, which runs
  `node --import ./scripts/register-myst-patches.mjs --test ...` (each test file in its own child
  process, Node's default isolation). Suites: `test:unit` (globs over
  `out/test/{build,core,host,host-memory,host-vscode,node-services,page,session,site}/**/*.test.js`)
  and `test:contracts` (`out/test/core/render/*.contract.js`). `test/core` holds 138 test files;
  about 2,000 `@tests_req` markers sit in `test/core` and `test/page`.
- **TypeScript is 7.0.2** (`devDependencies.typescript ^7.0.2`, the native compiler).
  `require("typescript")` returns only `{ version, versionMajorMinor }`; the compiler API lives
  under `typescript/unstable/*`. `@stryker-mutator/typescript-checker` loads the classic compiler
  API from `typescript`, so it cannot run against this install as it is. See open question 1.
- Stryker has no `node:test` runner. Its test-runner plugin API (`TestRunner`: `capabilities`,
  `init`, `dryRun`, `mutantRun`, `dispose`) and the instrumented code's global
  (`globalThis.__stryker__`: `activeMutant`, `currentTestId`, `mutantCoverage.static` /
  `.perTest`) are what an adapter uses for per-test coverage.
- Stryker's JSON report (mutation-testing-report-schema) gives per mutant `status`, `coveredBy`
  and `killedBy`. By default Stryker stops a mutant's run at the first failing test (bail), so
  `killedBy` names one test only. Redundancy needs every killer: the campaign sets
  `disableBail: true`.
- `out/reports/` is ignored by git (`.gitignore`: `/out/reports/`): the raw report never lands in
  the repository.
- Dev machine: Windows 11, 16 logical processors, Node 24 (`.nvmrc`); `just` targets run in Git
  Bash.

## 3. Decisions carried

| # | Decision (`02-answers.md`) | Where |
| --- | --- | --- |
| mt-Q1 | StrykerJS with its TypeScript checker; per-test coverage through a small `node:test` adapter, a Stryker test-runner plugin in the repo (under `scripts/` or `test/tools/`); round 1 proves the adapter on a few `core` files first; fallback if per-test coverage cannot work: map each mutated file to the test files that import it, and say so in the report | 4.1, 4.2, 5 (round 1); open question 1 (the checker vs TypeScript 7) |
| mt-Q2 | Runs locally through a just target (for example `just mutation-core`), report in `out/reports/mutation/`; no CI job, no workflow on PRs; if the full `core` run exceeds about 6 h on the dev machine, run it on a recorded sample of files and say so | 4.3, 4.4 |
| mt-Q3 | Score per `core` sub-folder and per SwRS (from `@tests_req` markers); list of redundant tests by killed mutants; holes; log calls and user-facing message strings excluded from mutation | 4.1 (exclusions), 4.5 |
| mt-Q4 | One PR for `core`: the tool, the agent read of the tests (no assertion, "does not throw" only, near-duplicates), the removals and merges, the new tests for the holes that matter, and the list of holes judged not worth a test, one line each | 4.6, 4.7, 4.8, 4.9 |
| mt-Q5 | A removed test with `@tests_req` moves its marker to a test that stays and covers the same SwRS; `just requirements-update` shows no loss; no published requirement is removed | 4.7, 6 |
| mt-Q6 | The note for chantier (command, scope, report reading, removal rules, run time) is written in the CR folder as evidence; the CoS sends it to chantier's CoS for `mutation-testing-driver` | 4.10 |

Settled by the owner before the grill (request, point 0): one-shot campaign; an agent reads the
tests first, then the mutation run.

## 4. What changes

### 4.1 Stryker configuration

- Dev dependencies (allowed by this CR, constitution section 5), from the npm registry, pinned in
  `package-lock.json`: `@stryker-mutator/core` and, per open question 1,
  `@stryker-mutator/typescript-checker`. Nothing else unless round 1 proves it necessary, and the
  PR says why.
- One configuration file, `scripts/stryker.config.mjs` (the CLI takes it as `stryker run
  scripts/stryker.config.mjs`; kept under `scripts/` so `check-unused-exports` and the formatters
  see it). It sets:
  - `mutate`: `src/core/**/*.ts` (minus `*.d.ts`), or the recorded sample (4.4).
  - `testRunner`: the adapter of 4.2, loaded through `plugins`.
  - `buildCommand`: `npm run compile` in the sandbox (instrumented files carry `// @ts-nocheck`,
    so `tsc` 7 compiles them).
  - `coverageAnalysis: "perTest"` (or `"all"` with the static fallback of 4.2, said in the report).
  - `disableBail: true` (every killer recorded, section 2).
  - `checkers: ["typescript"]` per open question 1.
  - `ignorePatterns`: `out`, `.venv`, `.cache`, `.artifacts`, `test/visual/screenshots`, and
    whatever else the sandbox copy does not need.
  - `reporters`: `json`, `html`, `clear-text`, `progress`; `jsonReporter.fileName` and
    `htmlReporter.fileName` under `out/reports/mutation/`.
  - `incremental: true` with `incrementalFile` under `out/reports/mutation/`, so a stopped
    multi-hour run resumes instead of restarting.
  - `concurrency`: left to Stryker's default unless measured better; the value used goes in the
    note.
- **Exclusions (mt-Q3)** through a Stryker ignorer plugin (`ignorers` option) in the repo, next to
  the adapter. It ignores:
  - every mutant inside a `console.*` call or a logger call (none in `core` today; the rule is
    there for `mutation-testing-rest`);
  - string-literal and template-literal mutants that are user-facing messages: the argument of
    `new Error(...)` / `new TypeError(...)` and other thrown errors, and the value of message
    properties (`message`, `detail`, `title`, `label`, `description`, `tooltip`, `placeholder`)
    and of diagnostic messages the code returns. Strings that drive behaviour (syntax tokens,
    keys, regular expressions, protocol message types, setting names) are **not** excluded.
  - The exact rule list is written in the ignorer's header comment and copied in the note (4.10).
  No `// Stryker disable` comment is added to `src/`.

### 4.2 The `node:test` adapter (mt-Q1)

A Stryker test-runner plugin in the repo, under `scripts/` (for example
`scripts/stryker-node-test-runner.mjs`) or `test/tools/` (a `.ts` there compiles into
`out/test/tools/`, which `test:unit`'s globs and `test/build/unitGlobs.test.ts` must then keep
consistent). It:

- runs the campaign's test files (4.3) with Node and `--import ./scripts/register-myst-patches.mjs`,
  as `scripts/node-test.mjs` does;
- gives each test a stable ID: its compiled file path relative to `out/test/` plus its full name
  chain (`describe > test`), unique across the suite;
- **dry run** (`perTest`): sets `__stryker__.currentTestId` for the duration of each test and
  returns, per test ID, the mutants it reached (`mutantCoverage.perTest`) and the mutants reached
  at module load (`mutantCoverage.static`), with each test's status and time. One way: a
  preload module that wraps `node:test`'s `test` / `it` so each test function sets and clears the
  ID; the Driver picks the mechanism and says which in the note;
- **mutant run**: activates `activeMutant`, runs only the test files that hold the covering tests
  given by Stryker's `testFilter`, and skips the other tests of those files; returns `Killed` with
  **every** failing test when bail is off, `Survived`, or `Timeout`; a fresh child process per run
  is acceptable (static mutants then need no environment reload); the run time per mutant is
  measured;
- reports a test that fails in the dry run as a dry-run failure (Stryker needs a green dry run).

**Fallback (mt-Q1).** If per-test coverage cannot work, the adapter maps each mutated file to the
test files that import it, statically (from the compiled test files' `require` graph), runs those
files for each mutant, and records `coveredBy` at file level. The report and the note say the
fallback was used and what it costs: redundancy is then judged per test file only where the file
granularity allows it, and per-test redundancy claims are not made.

Tests of the tool (constitution section 3): the adapter's pure parts (test ID building, filter
selection, the static map of the fallback if used) and the report reader of 4.5 get unit tests in
`test/build/` (for example `test/build/mutationReport.test.ts`), on small prepared reports. Those
prepared inputs are test data for the tool's logic, not copies of a shipped file.

### 4.3 The just target (mt-Q2)

- `just mutation-core` in the `justfile`, with a comment line above it in the style of the other
  targets: compiles, runs `stryker run scripts/stryker.config.mjs`, then the report reader (4.5).
  It writes only under `out/reports/mutation/`. An optional argument or environment variable may
  select a sample file list (4.4).
- It is **not** part of `just check`, `just ci-static`, `just preflight` or any workflow in
  `.github/`. No CI job is added or changed.
- The campaign's test set: the `test:unit` and `test:contracts` suites. Real-window tests
  (`test/integration`, e2e, visual) are out. A test file that cannot run in Stryker's sandbox (for
  example one that reads the git checkout or spawns tools) is left out of the test set, and the
  report lists it with its reason; it still runs in `just check`.

### 4.4 Run order and budget (mt-Q1, mt-Q2)

1. Round 1: the adapter on a few `core` files (for example `src/core/find`, `src/core/syntax`,
   `src/core/scroll`), dry run and mutant run green, per-test coverage confirmed (or the fallback
   decided), time per mutant measured.
2. The full `src/core` run. If the measured rate projects beyond about 6 h on the dev machine, the
   run takes a sample of files instead: the list is written in the repository's report output and
   in the note, with how it was chosen (each sub-folder represented), and every reading below says
   "on the sample".

### 4.5 Reading the report (mt-Q3)

A reader script (for example `scripts/mutation-report.mjs`, run by `just mutation-core`) reads
`out/reports/mutation/mutation.json` and the test sources, and writes
`out/reports/mutation/summary.md` (and a JSON twin) with:

- **Score per `core` sub-folder**: Stryker's mutation score, (killed + timeout) / (killed +
  timeout + survived + no coverage), with the counts; compile errors and ignored mutants counted
  apart.
- **Score per SwRS**: each test is mapped to the SwRS of its `@tests_req` markers (a marker block
  above a `test(...)` call, a marker inside a test body, and companion `*.markers.ts` lines whose
  scenario names a test). For an SwRS: the mutants its tests reach, and the share they kill.
- **Zero-kill tests**: tests that reach `core` mutants and kill none.
- **Redundant tests**: tests whose killed set is included in the union of the killed sets of the
  tests that stay. Computed greedily so two tests that duplicate each other are never both
  removed: the reader keeps a set of tests that kills every killed mutant, and lists the rest with,
  for each, the tests that already kill its mutants.
- **Holes**: survived and no-coverage mutants, by file and line, with the mutator and the
  replacement.

### 4.6 The agent read of the tests (mt-Q4, owner's point 0)

Before the mutation run, the Driver reads `test/core/**` (and the contract tests on `core`) and
lists: tests with no assertion, tests that only check "does not throw", near-duplicate tests. The
list goes into the PR body and the note. The mutation data then decides each entry (4.7, 4.8): no
entry is removed on the read alone.

### 4.7 Removals and merges (mt-Q4, mt-Q5)

- A removal or merge candidate is a test in `test/core/**` (or a contract test on `core`) that is
  zero-kill or redundant in 4.5, or flagged in 4.6 and confirmed by the data. A test in another
  folder (`test/page`, `test/session`...) that reaches `core` stays here as a killer; its own
  redundancy is judged by `mutation-testing-rest`, since this run does not mutate the code it is
  written for.
- A test whose `@tests_req` names an SwRS is removed only when a test that stays covers the same
  SwRS; its marker moves to that test in the same commit (constitution section 1; marker
  placement rules of `requirements/guidelines/project.guidelines.md`: at most 3 IDs per marker
  block, companions name their target).
- A merge keeps every assertion's intent (constitution section 3); an assertion that changes
  says why in the commit and the PR.
- A test that guards a bug fix (a regression test named or commented as such) or a requirement's
  boundary scenario is kept even when redundant on mutation data, and listed as kept with its
  reason.
- File-size limits hold (1,500 lines per file in `test/`).

### 4.8 New tests for holes that matter (mt-Q4)

- A surviving mutant in behaviour a user or a requirement depends on gets a test that kills it
  (it fails with the mutant, passes on the code). The test carries the `@tests_req` of the SwRS it
  checks, when there is one.
- Equivalent mutants (no observable difference) are not holes; they are listed as equivalent.
- No `src/` behaviour changes in this CR. If a hole reveals a bug, it is not fixed here: it is
  filed to the backlog and specified as it behaves ("Known issue: …"), per constitution section 1.

### 4.9 Holes not worth a test (mt-Q4)

A list, one line each (file:line, mutator, why not worth a test), in the PR body and in the note.
Equivalent mutants are a separate short list.

### 4.10 The note for chantier (mt-Q6)

Written in the CR folder as evidence, `evidence/mutation-campaign-note.md` (planning surface, not
the Studio repository). It covers: the command (`just mutation-core`, the Stryker version, the
configuration keys that mattered, the adapter's mechanism or the fallback); the scope (files
mutated, sample if any, test files left out and why, exclusion rules); the report and how it was
read (the four lists of 4.5, the greedy rule); the rules for removing a test (4.7); the time it
took (dry run, mutants count, time per mutant, total wall time, concurrency, machine); and what a
Mutation Testing Driver should do differently. The Chief of Staff sends it to chantier's Chief of
Staff for `mutation-testing-driver`.

### 4.11 Requirements and docs

- `just requirements-update` after the marker moves; its generated files committed; a dated entry
  in `requirements/tiers/log.md` naming the moved markers and the removed tests' SwRS.
- No SwRS is added, changed or removed: the tool is development tooling, not product behaviour,
  and no `approved` requirement is touched.
- CONTRIBUTING.md gets a short paragraph on `just mutation-core` (what it does, how long, where
  the report goes), and `AGENTS.md` "Main targets" one line for it.

## 5. Out of scope

- Every file outside `src/core` as a mutation target (`mutation-testing-rest`).
- Removing or merging tests outside `test/core/**` and the contract tests on `core`.
- Real-window e2e, integration and visual tests.
- Any CI job or workflow; mutation testing on pull requests.
- Fixing bugs the holes reveal (backlog items instead).
- Any change to `src/` behaviour or to a requirement.

## 6. Evidence

- Round 1: the dry run and a mutant run on the first files, green, with per-test `coveredBy` for
  at least one mutant reached by several tests and `killedBy` naming more than one test (proof
  that bail is off), or the decision to use the fallback with the reason.
- The full or sample run: `out/reports/mutation/summary.md` figures copied into the PR body
  (score per sub-folder before and after the changes, mutants count, run time), and the same run
  repeated on the final branch over the affected files: the score per sub-folder does not drop.
- Requirements: the SwRS-to-test coverage before and after (`just requirements-report`, or
  `okfreq status requirements`, on `main` and on the branch): no SwRS loses its last test link;
  `just requirements-lint` green; `git diff requirements/` shows only generated coverage
  updates and the log entry.
- `test/build/` tests of the adapter's pure parts and of the report reader pass in `just unit`.
- Test count before and after (`node:test` summary of `just unit`), in the PR body.
- `just check` and `just preflight` pass (on Windows, the static stage; CI runs the others).
  `just mutation-core` is not in either.
- `.github/workflows/` unchanged.
- The note of 4.10 is in the CR folder's `evidence/`.

## Open questions

1. **The TypeScript checker and TypeScript 7 (mt-Q1).** `@stryker-mutator/typescript-checker`
   needs the classic `typescript` compiler API; Studio's `typescript` 7.0.2 exposes none at
   `require("typescript")`. Which way? (a) Give the checker its own `typescript` 5.x through an
   npm `overrides` entry scoped to `@stryker-mutator/typescript-checker` (Studio's own compile
   stays on 7.0.2), if round 1 shows npm honours it for that peer dependency; (b) run without the
   checker: type-invalid mutants then run as tests and end killed or survived instead of
   "compile error", the report says so, and the Driver discards type-invalid survivors by hand;
   (c) try (a) in round 1 and fall back to (b) if it fails, saying so in the report and the note.

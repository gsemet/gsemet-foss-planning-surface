# Mutation testing campaign on `src/core`: redundant tests and holes

Run StrykerJS 10.1.1 once over `src/core` and the unit tests that reach it. TypeScript 7 itself
type-checks every mutant against the whole program. List the tests that kill nothing another test
does not already kill. The list is for the owner's later review: nothing is removed or merged
here. Add the few tests the surviving mutants call for, and write down how the campaign ran so
chantier can write a Mutation Testing Driver from it. One-shot: no CI job, no check on pull
requests.

Origin: verbal (owner, 2026-11-20). No tracker issue. Code read at `main` `a18bcac1`; `origin/main`
is now `5a84db8b` (release 1.11.0): the Driver starts from the latest `origin/main`.

- **Decided by the Chief of Staff** under the owner's autonomy rule: mt-Q1, mt-Q3, mt-Q5, mt-Q6.
- **Confirmed by the owner:** mt-Q2.
- **Changed by the owner:** mt-Q4.
- **Answered by the owner** (2026-11-21): mt-Q7 to mt-Q12.

The PR body says which is which. Part 1 of 2: `mutation-testing-rest` runs the same campaign on
everything else after this one lands.

## 1. Goal, in the user's terms

- For `core`, the owner gets the list of tests that prove nothing another `core` test does not
  already prove. Each entry has its evidence: the mutants it kills and who else kills them. The
  owner decides later which tests to remove or merge.
- The code that no test checks gets the few tests it needs. A hole that only another layer's
  tests cover is labelled as such.
- No requirement loses its test: no test is removed, so every SwRS covered today stays covered.
- chantier gets a written account of a real campaign to write its `mutation-testing-driver` role:
  the command, the scope, how the report was read, the proposed rules for removing a test, and the
  time taken.

## 2. Facts the design rests on (main `a18bcac1`)

### The code and the tests

- `src/core` has 157 `.ts` files, about 30.5k lines, in 19 sub-folders.
  - The largest: `render` 8.4k, `preview` 6.8k, `frontmatter` 3.6k, `security` 1.6k,
    `protocol` 1.6k, `mapping` 1.3k.
  - No `console.*` or logger call exists in `src/core` today.
- Tests run on `node:test` over the compiled `out/` (`npm run compile` = `tsc -p .`).
  - `scripts/node-test.mjs <suite> <pattern>...` launches them with
    `node --import ./scripts/register-myst-patches.mjs --test ...`. Each test file runs in its
    own child process (Node's default isolation).
  - `test:unit` covers the globs
    `out/test/{build,core,host,host-memory,host-vscode,node-services,page,session,site}/**/*.test.js`.
  - `test/core` holds 138 test files. About 2,000 `@tests_req` markers sit in `test/core` and
    `test/page`.
- **The contract suite is empty today.** `test:contracts` globs
  `out/test/core/render/*.contract.js`, but no `*.contract.ts` exists in `test/` or `src/`.
  So "the contract tests on `core`" adds nothing to this campaign. If contract files appear before
  the run, they count with `test/core`.

### TypeScript 7

- Studio uses TypeScript 7.0.2 (`devDependencies.typescript ^7.0.2`), the native compiler. On
  this machine its binary comes from `@typescript/typescript-win32-x64`.
- What it exposes, read in `node_modules/typescript/package.json` and `dist/api/`:
  - `"."` points to `lib/version.cjs`: `require("typescript")` returns only
    `{ version, versionMajorMinor }`. TypeScript 5 is excluded (mt-Q7).
  - `"./unstable/sync"` points to `dist/api/sync/api.js` (there is also `./unstable/async`):
    - `new API({ cwd, fs })`. `fs` holds virtual file-system callbacks: `readFile` returns the
      content, `null` for "absent", `undefined` to fall back to the disk.
    - `api.updateSnapshot({ openProjects: [tsconfig] })` and
      `api.updateSnapshot({ fileChanges: { changed: [file] } })`.
    - `snapshot.getProjects()`, `snapshot.dispose()`.
    - `project.program.getSemanticDiagnostics(file?)` and `getSyntacticDiagnostics(file?)`.
    - `api.close()`.
    - Diagnostics carry `fileName`, `pos`, `end`, `code`, `category`, `text`.
    - The API drives the `tsgo` binary over a pipe.
- **Probe** (2026-11-21, read-only, in-memory overlay, nothing written). It ran
  `typescript/unstable/sync` on Studio's `tsconfig.json`:
  - Opening the project took 0.8 s (1,861 files).
  - Diagnostics took 14 ms for one file and 1.3 s for the whole program, with 0 errors.
  - A type-breaking replacement in `src/core/find/findMatches.ts`, given through `fs.readFile`
    and `fileChanges.changed`, gave `2322 Type '{ x: 1; }' is not assignable to type
    'FindPattern | undefined'.` The whole program after the change took 1.2 s.
  - Removing the overlay brought 0 errors back.
  - So TypeScript 7's own API can type-check a mutant in memory against the whole program, in
    about 1.2 s per mutant on one process.

### Stryker 10.1.1 and TypeScript 7

- **`@stryker-mutator/typescript-checker`** loads the classic compiler API from `typescript`, so
  it cannot run here. Its own option `typescriptChecker.experimentalNativePreview` targets the
  TypeScript native preview packaging, not a `typescript` 7 install whose root export is only the
  version. That option is recorded as the reason the stock checker cannot run. Its design is the
  reference for this CR's checker:
  - one mutant per check;
  - whole-program diagnostics;
  - `snapshot.dispose()` after each check.
- **Stryker core** also loads `typescript`. Its sandbox tsconfig preprocessor
  (`sandbox/ts-config-preprocessor.js`, lines 45-46) calls `ts.parseConfigFileTextToJson` when
  the file named by `tsconfigFile` (default `tsconfig.json`) exists. With TypeScript 7, that call
  fails. The campaign sets `tsconfigFile` to a name absent from the project, so the preprocessor
  does nothing. It never uses `inPlace`.
- **Stryker has no `node:test` runner.** An adapter uses two things for per-test coverage:
  - the test-runner plugin API (`TestRunner`: `capabilities`, `init`, `dryRun`, `mutantRun`,
    `dispose`);
  - the instrumented code's global, `globalThis.__stryker__`, with `activeMutant`,
    `currentTestId`, `mutantCoverage.static` and `mutantCoverage.perTest`.
- **A custom checker** implements the checker plugin API (`Checker`: `init`, and `check(mutants)`
  returning `Passed` or `CompileError` with a reason for each mutant).
- **Checker processes.** Stryker runs its checker processes alongside the test runners; with
  checkers on, it runs `ceil(concurrency / 2)` checker processes.
- **The JSON report** (mutation-testing-report-schema) gives `status`, `coveredBy` and `killedBy`
  for each mutant.
  - By default, Stryker stops a mutant's run at the first failing test (bail), so `killedBy`
    names one test only.
  - Redundancy needs every killer, so the `core` run sets `disableBail: true`.
- **Temporary folder.** Stryker's sandboxes go in `tempDirName`, `.stryker-tmp` by default,
  which `.gitignore` does not list today.

### Repository and machine

- `out/reports/` is ignored by git (`.gitignore`: `/out/reports/`): the raw report never lands in
  the repository.
- Dev machine: Windows 11, 16 logical processors, Node 24 (`.nvmrc`). `just` targets run in Git
  Bash.

## 3. Decisions carried

| # | Decision (`02-answers.md`) | Where |
| --- | --- | --- |
| mt-Q1 | StrykerJS, mutants type-checked. Per-test coverage through a small `node:test` adapter, a Stryker test-runner plugin in the repo (under `scripts/` or `test/tools/`). Round 1 proves the adapter on a few `core` files first. Fallback if per-test coverage cannot work: map each mutated file to the test files that import it, and say so in the report. mt-Q7 replaces the checker itself | 4.1, 4.2, 4.3, 4.5 |
| mt-Q2 | Confirmed by the owner. Runs locally through a just target (`just mutation-core`), report in `out/reports/mutation/`. No CI job, no workflow on PRs. If the full `core` run exceeds about 6 h on the dev machine, it runs on a recorded sample of files and says so | 4.4, 4.5 |
| mt-Q3 | Score per `core` sub-folder and per SwRS (from `@tests_req` markers). List of redundant tests by killed mutants. Holes. Log calls and user-facing message strings excluded from mutation | 4.1 (exclusions), 4.6 |
| mt-Q4 | **Changed by the owner:** redundant tests are "List only, remove nothing". One PR for `core`: the tool, the report, the list of redundant tests by killed mutants, and the tests for the holes that matter. No test removed or merged; removals wait for the owner's review of the list | 4.7, 4.8, 4.9, 4.10. The removal rules become the note's proposal (4.11) |
| mt-Q5 | Every requirement stays covered (a removed test would move its marker to a test that stays). `just requirements-update` shows no loss. No published requirement is removed. With mt-Q4 as changed, no test is removed, so no marker moves in this CR | 4.12, 6 |
| mt-Q6 | The note for chantier (command, scope, report reading, removal rules, run time) is written in the CR folder as evidence. The CoS sends it to chantier's CoS for `mutation-testing-driver` | 4.11 |
| mt-Q7 | Owner: "Find another solution to stay on TS7. No compromise". No TypeScript 5 anywhere (no npm override, no second compiler), no run that silently skips the type check. A TS 7 path, proved on a few `core` files in round 1 | 4.1, 4.3, 4.5, 6 |
| mt-Q8 | Owner: "Whole program". Every mutant is type-checked against the whole program; cost measured in round 1. No grouping: one mutant per check | 4.3, 4.5 |
| mt-Q9 | Owner: "Load-time coverage per file". The adapter reports a test file's load-time coverage as covered by each test of that file, so only those files run | 4.2 |
| mt-Q10 | Owner: "Core tests, others label holes". Only `test/core` decides redundancy (bail off). The other layers' tests then run (bail on) only on the mutants `core`'s tests did not kill, to label those holes "killed only by another layer" | 4.4, 4.6, 4.8 |
| mt-Q11 | Owner: "A 'not judged' mark" for tests that reach only excluded, timeout or compile-error mutants. Never a removal candidate on mutation data alone; the reason is shown | 4.6, 4.8 |
| mt-Q12 | Owner: "At the start of just mutation-core". The real TS 7 check runs as a self-test that fails the target if it breaks; `test/build` keeps the pure parts only | 4.3, 4.4 |

Settled by the owner before the grill (request, point 0): one-shot campaign; an agent reads the
tests first, then the mutation run.

The Chief of Staff accepted these additions of this specification (2026-11-21):

- `disableBail`;
- the rule that keeps regression and boundary tests;
- the ignorer's list;
- the `test/build/` unit tests of the tool;
- the note's path;
- the just target with its CONTRIBUTING.md and AGENTS.md entries;
- no SwRS change.

Fixes of the spec critic, read against Stryker 10.1.1, also applied:

- `tsconfigFile` and never `inPlace`;
- `experimentalNativePreview` recorded as the reason and the reference;
- no `checkerConcurrency`, and the checker process count recorded;
- `tempDirName` and Windows long paths;
- the empty contract suite;
- no rationale given for `scripts/`.

## 4. What changes

### 4.1 Stryker configuration

#### Dependencies

These dev dependencies are allowed by this CR (constitution section 5). They come from the npm
registry and are pinned in `package-lock.json`.

- `@stryker-mutator/core` **10.1.1**. It brings `@stryker-mutator/api`, which the plugins use.
- **Not** `@stryker-mutator/typescript-checker`.
- No `typescript` other than the project's 7.0.2: no `overrides` entry, no aliased package.
- Nothing else unless round 1 proves it necessary, and the PR says why.

#### Configuration files

The configuration lives in `scripts/stryker.config.mjs`, run as
`stryker run scripts/stryker.config.mjs`. A second configuration for the other layers' phase
(4.4) extends it, for example `scripts/stryker.others.config.mjs`.

| Key | Value |
| --- | --- |
| `mutate` | `src/core/**/*.ts` (minus `*.d.ts`), or the recorded sample (4.5). The others phase uses the ranges of 4.4 |
| `plugins` | The three plugins of this CR: adapter (4.2), checker (4.3), ignorer (below) |
| `testRunner` | The adapter's name |
| `checkers` | The TS 7 checker's name (for example `"typescript-7"`), always on. The target has no switch to turn it off |
| `tsconfigFile` | A name absent from the project (for example `"stryker-no-tsconfig.json"`), so Stryker core's tsconfig preprocessor never calls the `typescript` API (section 2). A comment says why |
| `inPlace` | Never set: sandboxes only |
| `tempDirName` | Default `.stryker-tmp`, added to `.gitignore` (`/.stryker-tmp/`). If round 1 hits Windows path-length limits, it becomes a shorter ignored folder and the note says so |
| `buildCommand` | `npm run compile` in the sandbox. Instrumented files carry `// @ts-nocheck`, so `tsc` 7 compiles them; the type check is the checker's job, on the uninstrumented code |
| `coverageAnalysis` | `"perTest"` (or `"all"` with the static fallback of 4.2, said in the report) |
| `disableBail` | `true` in the `core` phase, so every killer is recorded (section 2). `false` in the others phase (4.4) |
| `ignorePatterns` | `out`, `.venv`, `.cache`, `.artifacts`, `test/visual/screenshots`, and whatever else the sandbox copy does not need |
| `reporters` | `json`, `html`, `clear-text`, `progress`. Report files under `out/reports/mutation/`, one set per phase |
| `incremental` | `true`, with one `incrementalFile` per phase under `out/reports/mutation/`, so a stopped multi-hour run resumes instead of restarting |
| `concurrency` | Stryker's default unless measured better. No `checkerConcurrency` key: Stryker 10.1.1 derives the checker processes from `concurrency` (section 2) |

The note records the `concurrency` used and the resulting number of checker processes.

#### Exclusions (mt-Q3)

A Stryker ignorer plugin (the `ignorers` option) in the repo, next to the adapter, handles the
exclusions. It ignores:

- every mutant inside a `console.*` call or a logger call. There are none in `core` today; the
  rule is there for `mutation-testing-rest`.
- string-literal and template-literal mutants that are user-facing messages:
  - the argument of `new Error(...)`, `new TypeError(...)` and other thrown errors;
  - the value of message properties: `message`, `detail`, `title`, `label`, `description`,
    `tooltip`, `placeholder`;
  - diagnostic messages the code returns.

Strings that drive behaviour (syntax tokens, keys, regular expressions, protocol message types,
setting names) are **not** excluded.

The exact rule list is written in the ignorer's header comment and copied in the note (4.11). No
`// Stryker disable` comment is added to `src/`.

### 4.2 The `node:test` adapter (mt-Q1, mt-Q9)

The adapter is a Stryker test-runner plugin in the repo. It goes under `scripts/` (for example
`scripts/stryker-node-test-runner.mjs`) or under `test/tools/`. A `.ts` file in `test/tools/`
compiles into `out/test/tools/`, so `test:unit`'s globs and `test/build/unitGlobs.test.ts` must
then stay consistent.

**Running the tests.** It runs the phase's test files (4.4) with Node and
`--import ./scripts/register-myst-patches.mjs`, as `scripts/node-test.mjs` does.

**Test IDs.** Each test gets a stable ID: its compiled file path relative to `out/test/` plus its
full name chain (`describe > test`), unique across the suite.

**Dry run** (`perTest`):

- It sets `__stryker__.currentTestId` for the duration of each test and returns, per test ID, the
  mutants that test reached, with each test's status and time.
- One way: a preload module that wraps `node:test`'s `test` / `it` so each test function sets
  and clears the ID. The Driver picks the mechanism and says which in the note.
- **Load-time coverage (mt-Q9).** Mutants reached while a test file loads (outside any test) are
  reported as covered by each test of that file, in `perTest`. They are not reported as global
  static coverage. So a static mutant runs only the files that reach it, not the whole suite.

**Mutant run:**

- It activates `activeMutant` and runs only the test files that hold the covering tests given by
  Stryker's `testFilter`, skipping the other tests of those files.
- It returns `Killed` (with every failing test when bail is off; the first one when bail is on),
  `Survived` or `Timeout`.
- A fresh child process per run is acceptable: a load-time mutant then takes effect when its file
  loads.
- It measures the run time per mutant.

**Dry-run failures.** A test that fails in the dry run is reported as a dry-run failure: Stryker
needs a green dry run.

**Fallback (mt-Q1).** If per-test coverage cannot work:

- the adapter maps each mutated file to the test files that import it, statically, from the
  compiled test files' `require` graph;
- it runs those files for each mutant and records `coveredBy` at file level;
- the report and the note say the fallback was used and what it costs: redundancy is then judged
  per test file only where the file granularity allows it, and no per-test redundancy claim is
  made.

### 4.3 The TypeScript 7 checker (mt-Q7, mt-Q8, mt-Q12)

The checker is a Stryker checker plugin in the repo, next to the adapter (for example
`scripts/stryker-ts7-checker.mjs`). It type-checks each mutant with the project's own
TypeScript 7 through `typescript/unstable/sync` (section 2). Its design follows the stock
checker's `experimentalNativePreview` mode.

**`init`:**

- It creates `new API({ cwd: <project root>, fs: { readFile } })` and opens the project with
  `updateSnapshot({ openProjects: [<root>/tsconfig.json] })`.
- It records the baseline whole-program syntactic and semantic diagnostics (0 today), so only new
  ones count.

**What it checks.** It checks the **original** sources: the project's files, never Stryker's
instrumented copies. `readFile` returns the overlay for the one mutated file and `undefined` for
every other file.

**`check(mutants)`, one mutant per check, no grouping (mt-Q8).** For each mutant it:

1. builds the mutated text of `mutant.fileName` from its `location` and `replacement`;
2. sets the overlay and calls `updateSnapshot({ fileChanges: { changed: [file] } })`;
3. reads the **whole program**'s syntactic and semantic diagnostics;
4. reports `CompileError` if any error is not in the baseline, with the first new diagnostic
   (`code`, `text`, file and line) as reason; otherwise `Passed`;
5. disposes of the snapshot (`snapshot.dispose()`), clears the overlay and notifies the change
   again.

A mutant whose check throws or times out is reported as an error of the run, never as `Passed`.
The plugin does not implement `group`.

**Cost.** The probe gave about 1.2 s per whole-program check on one process. Round 1 measures
the real time per mutant with the checker processes running in parallel, and the projection
feeds the 6 h rule of 4.5.

**`dispose`:** `api.close()`.

**Self-test at the start of `just mutation-core` (mt-Q12).**

- The plugin has a self-test entry, for example `node scripts/stryker-ts7-checker.mjs --self-test`.
  The target runs it first.
- It writes a small project to a temporary folder and runs the real check there through
  `typescript/unstable/sync`.
- It expects `CompileError`, with its diagnostic, for a type-breaking replacement, and `Passed`
  for a type-valid one.
- It also checks that the API loads and that `tsgo` spawns.
- Any failure stops the target with a non-zero exit before Stryker starts.

**No silent skip (mt-Q7).** If the plugin fails to start (the API refuses to load, `tsgo` does
not spawn, the project does not open), `just mutation-core` fails with that error. No flag,
setting or fallback runs mutants without the type check.

**A second TS 7 path,** if round 1 shows the API cannot be used:

- The same checker drives the TypeScript 7 CLI instead: `node_modules/typescript/bin/tsc -p
  <temp tsconfig> --noEmit`, over a temporary copy holding the mutated file.
- It still checks one mutant per call, against the whole program.
- It is measured and named in the note.

TypeScript 5 is never a path.

**API stability.** `unstable` means the API may change between TypeScript 7 releases. The checker
imports only the names listed in section 2, and the note records the exact `typescript` version
used.

**Tests of the tool** (constitution section 3) go in `test/build/` (for example
`test/build/mutationTools.test.ts` and `test/build/mutationReport.test.ts`). They cover the pure
parts only (mt-Q12):

- the adapter: test ID building, filter selection, attribution of load-time coverage to each test
  of a file, and the static map of the fallback if it is used;
- the checker: applying a mutant's `location` and `replacement` to a text, and filtering new
  diagnostics against the baseline;
- the report reader of 4.6, on small prepared reports.

Those prepared inputs are test data for the tools' logic, not copies of a shipped file. The real
TS 7 check is not in `just unit`: it is the self-test above.

### 4.4 The just target and its two phases (mt-Q2, mt-Q10, mt-Q12)

`just mutation-core` goes in the `justfile`, with a comment line above it in the style of the
other targets. It writes only under `out/reports/mutation/` (plus Stryker's ignored
`tempDirName`), in this order:

1. **Compile, then run the checker's self-test (4.3).** Stop on failure.
2. **`core` phase.**
   - Stryker runs with `scripts/stryker.config.mjs`, bail off.
   - The test set is the `test/core/**` test files only, plus the contract files on `core` if any
     exist (none today, section 2).
   - This phase alone decides redundancy and the holes.
3. **Others phase.**
   - It covers the mutants of the `core` phase that are survived or no-coverage (not ignored,
     timeout or compile-error).
   - Stryker runs again with the second configuration:
     - `mutate` is limited to those mutants' line and column ranges (`file:line:col-line:col`);
     - bail is on;
     - the test set is the rest of `test:unit` (`test/{build,host,host-memory,host-vscode,node-services,page,session,site}`).
   - The reader keeps only the mutants that match a `core`-phase hole by file, location, mutator
     and replacement.
   - A hole that one of these tests kills is labelled **"killed only by another layer"**, with
     the killing test's name.
4. **The report reader (4.6).**

An optional argument or environment variable may select a sample file list (4.5). None turns the
checker or its self-test off.

The target is **not** part of `just check`, `just ci-static`, `just preflight` or any workflow in
`.github/`. No CI job is added or changed.

Real-window tests (`test/integration`, e2e, visual) are out. A test file that cannot run in
Stryker's sandbox (for example one that reads the git checkout or spawns tools) is left out of its
phase. The report lists it with its reason, and it still runs in `just check`.

`.gitignore` gains `/.stryker-tmp/` (or the shorter folder chosen in round 1).

### 4.5 Run order and budget (mt-Q1, mt-Q2, mt-Q7, mt-Q8)

**Round 1** runs on a few `core` files, for example `src/core/find`, `src/core/syntax` and
`src/core/scroll`. Round 1 is done when all of these hold:

- **Sandbox and build.** On Windows, the sandbox copy is made under `tempDirName`, without path
  errors, and `npm run compile` is green inside it. The configured `tsconfigFile` is absent, so
  Stryker core makes no `typescript` call.
- **TS 7 checker.** The self-test passes. The checker marks the type-invalid mutants
  `CompileError` (at least one shown with its diagnostic). The whole-program check time per mutant
  is measured, with the number of checker processes.
- **Adapter.** The dry run and the mutant runs are green, per-test coverage is confirmed (or the
  fallback decided), and the load-time coverage attribution is shown on at least one load-time
  mutant. The run time per mutant is measured.
- **Others phase.** The others phase runs on the round-1 holes.

**Full run.** Then the full `src/core` run. If the measured rates (check plus tests) project
beyond about 6 h on the dev machine, the run takes a sample of files instead:

- the list is written in the report output and in the note, with how it was chosen (each
  sub-folder represented);
- every reading below says "on the sample".

### 4.6 Reading the report (mt-Q3, mt-Q10, mt-Q11)

A reader script (for example `scripts/mutation-report.mjs`, run by `just mutation-core`) reads
both phases' `mutation.json` and the test sources. It writes `out/reports/mutation/summary.md`
and a JSON twin, with:

- **Score per `core` sub-folder** (`core` phase). This is Stryker's mutation score,
  (killed + timeout) / (killed + timeout + survived + no coverage), with the counts. Compile errors
  (from the TS 7 checker) and ignored mutants are counted apart. A second figure counts the holes
  "killed only by another layer".
- **Score per SwRS.**
  - Each test is mapped to the SwRS of its `@tests_req` markers. A marker counts when it sits in a
    block above a `test(...)` call, inside a test body, or on a companion `*.markers.ts` line
    whose scenario names a test.
  - For an SwRS, the score is the mutants its `core` tests reach, and the share they kill.
- **Zero-kill tests.** `test/core` tests that reach killable mutants and kill none.
- **Redundant tests** (`test/core` only, bail off).
  - A test is redundant when its killed set is included in the union of the other `test/core`
    tests' killed sets.
  - It is computed greedily, so two tests that duplicate each other are never both listed as
    removable. The reader keeps a set of tests that kills every killed mutant, and lists the rest.
  - Each entry shows the mutants the test kills and the tests that already kill them.
- **Not judged (mt-Q11).**
  - A `test/core` test is marked not judged when every mutant it reaches is ignored (an
    exclusion), a timeout or a compile error.
  - Its reason is shown, for example "reaches only 12 excluded message-string mutants".
  - It is never a removal candidate on mutation data alone.
- **Holes.** Survived and no-coverage mutants, by file and line, with the mutator and the
  replacement. Each one is labelled either "no test kills it" or "killed only by another layer"
  (with the test).

### 4.7 The agent read of the tests (owner's point 0)

Before the mutation run, the Driver reads `test/core/**` and lists:

- tests with no assertion;
- tests that only check "does not throw";
- near-duplicate tests.

Each entry is then marked with what the mutation data says about it: zero-kill, redundant, not
judged, or kills mutants nobody else kills. The list goes into the redundant-tests list of 4.8.
Nothing is changed on it.

### 4.8 The list of redundant tests (mt-Q4 as changed, mt-Q10, mt-Q11)

**No test is removed or merged in this CR.** No existing test file changes, except to add the
tests of 4.9.

**What the list covers:** the `test/core/**` tests that are zero-kill, redundant or not judged in
4.6, and the entries of 4.7. Each entry gives:

- the file and the test name;
- its `@tests_req` SwRS;
- the mutants it kills, and the tests that already kill them;
- whether a test that stays covers each of its SwRS.

**Each entry is marked one of:**

- **removal candidate**;
- **keep**: by the proposed rules of 4.11, a test that guards a bug fix (a regression test named
  or commented as such) or a requirement's boundary scenario is marked keep even when redundant on
  mutation data, with its reason;
- **not judged**, with its reason (mt-Q11). A not-judged test is never a removal candidate.

**Other layers' tests are not listed.** Their redundancy is judged by `mutation-testing-rest`.
Here they only label holes (4.4).

**Where the list goes:** the full list goes in the CR folder, `evidence/redundant-tests-core.md`,
for the owner's review. The PR body gives its counts and a pointer to it. Removals, if the owner
wants them, are a later change.

### 4.9 New tests for holes that matter (mt-Q4)

- **A surviving mutant** in behaviour a user or a requirement depends on gets a test in
  `test/core/**` that kills it: the test fails with the mutant and passes on the code. This
  applies when the hole is labelled "no test kills it".
  - The test carries the `@tests_req` of the SwRS it checks, when there is one.
  - Markers are placed per `requirements/guidelines/project.guidelines.md` (at most 3 IDs per
    marker block).
  - File-size limits hold (1,500 lines per file in `test/`).
- **A hole "killed only by another layer"** gets a `core` test only when the Driver judges that
  `core` should own the check. The PR says which and why.
- **Equivalent mutants** (no observable difference) are not holes; they are listed as equivalent.
- **No `src/` behaviour changes in this CR.** If a hole reveals a bug, it is not fixed here. It is
  filed to the backlog and specified as it behaves ("Known issue: …"), per constitution section 1.

### 4.10 Holes not worth a test (mt-Q4)

A list, one line each (file:line, mutator, why not worth a test), in the PR body and in the note.
Equivalent mutants are a separate short list.

### 4.11 The note for chantier (mt-Q6)

The note is written in the CR folder as evidence, `evidence/mutation-campaign-note.md` (planning
surface, not the Studio repository). It covers:

- **The command:**
  - `just mutation-core` and its two phases;
  - Stryker 10.1.1 and the `typescript` version;
  - the configuration keys that mattered (`tsconfigFile`, `tempDirName`, `disableBail`,
    `concurrency`) and the resulting number of checker processes;
  - the adapter's mechanism or the fallback;
  - the TS 7 checker's path, and why the stock checker and its `experimentalNativePreview` mode
    could not run.
- **The scope:** the files mutated, the sample if any, the test files left out and why, the
  exclusion rules.
- **How the report was read:** the lists of 4.6, the greedy rule, the not-judged mark, and the
  "killed only by another layer" label.
- **The proposed rules for removing a test,** for the owner's later review (not applied here):
  - a candidate is a test of the mutated layer's own test folder that is zero-kill or redundant,
    never a not-judged test;
  - a test with `@tests_req` is removed only when a test that stays covers the same SwRS, and its
    marker moves to that test in the same commit (constitution section 1, mt-Q5);
  - a merge keeps every assertion's intent, and an assertion that changes says why
    (constitution section 3);
  - regression tests and boundary-scenario tests stay even when redundant;
  - `just requirements-update` shows no loss.
- **The time it took:**
  - the self-test and the dry run;
  - the mutant count;
  - the check time and the test time per mutant;
  - the total wall time of each phase;
  - the concurrency and the checker processes;
  - the machine.
- **What a Mutation Testing Driver should do differently.**

The Chief of Staff sends the note to chantier's Chief of Staff for `mutation-testing-driver`.

### 4.12 Requirements and docs

- **No marker moves,** since no test is removed.
- **New tests of 4.9 that carry `@tests_req`:**
  - `just requirements-update` runs and its generated files are committed;
  - a dated entry in `requirements/tiers/log.md` names the SwRS that gained tests.
  If no new test carries a marker, `requirements/` is unchanged.
- **No SwRS is added, changed or removed:** the tool is development tooling, not product
  behaviour, and no `approved` requirement is touched.
- **Docs.** CONTRIBUTING.md gets a short paragraph on `just mutation-core`: what it does, the
  two phases, the TS 7 checker and its self-test, how long it takes, where the report goes.
  `AGENTS.md` "Main targets" gets one line for it.

## 5. Out of scope

- Removing or merging any test. The owner reviews the list first; removals are a later change.
- Every file outside `src/core` as a mutation target (`mutation-testing-rest`).
- Judging the redundancy of tests outside `test/core`.
- Real-window e2e, integration and visual tests.
- Any CI job or workflow; mutation testing on pull requests.
- TypeScript 5 in any form; `@stryker-mutator/typescript-checker`; `inPlace` runs.
- Fixing bugs the holes reveal (backlog items instead).
- Any change to `src/` behaviour or to a requirement.

## 6. Evidence

### Round 1

- **Sandbox build green.** On Windows, the sandbox is created under `tempDirName` with no path
  error, and `npm run compile` succeeds in it. The run log shows that Stryker core made no
  `typescript` call (`tsconfigFile` is absent from the project).
- **TS 7 checker.**
  - The self-test passes, and a deliberately broken self-test makes `just mutation-core` stop
    before Stryker starts.
  - At least one round-1 mutant is marked `CompileError` with its TypeScript 7 diagnostic in the
    report.
  - The time per whole-program check is recorded, with the number of checker processes.
  - `npm ls typescript` shows a single 7.x version, and `package-lock.json` holds no
    `@stryker-mutator/typescript-checker`.
- **Adapter.**
  - The dry run and a mutant run are green.
  - Per-test `coveredBy` is shown for at least one mutant reached by several tests.
  - `killedBy` names more than one test, which proves bail is off in the `core` phase.
  - At least one load-time mutant is shown covered by each test of its file and by no other file.
  - Or the decision to use the fallback, with its reason.
- **Others phase.** At least one round-1 hole is labelled, or the note says none was killed by
  another layer.

### Full or sample run

- The PR body copies the figures of `out/reports/mutation/summary.md`: score per sub-folder,
  compile errors, holes by label, not-judged count, mutant count, the run time of each phase.
- The run is repeated on the final branch over the files the new tests target: their holes are
  killed and no score drops.

### Tests and requirements

- **No existing test removed or merged.** `git diff --stat origin/main -- test/` shows only added
  tests (and the new `test/build/` tool tests). The test count before and after (`node:test`
  summary of `just unit`) only grows.
- **Requirements.**
  - `just requirements-lint` is green.
  - No SwRS loses a test link: compare `just requirements-report` or `okfreq status requirements`
    on `main` and on the branch.
  - `git diff requirements/` shows only generated coverage updates and the log entry, or nothing.
- **Tool tests.** The `test/build/` tests of the tool's pure parts pass in `just unit`.

### Project checks

- `just check` and `just preflight` pass (on Windows, the static stage; CI runs the others).
  `just mutation-core` is in neither.
- `.github/workflows/` is unchanged. `.gitignore` gains only the Stryker temporary folder.

### CR folder

The CR folder's `evidence/` holds `redundant-tests-core.md` (4.8) and `mutation-campaign-note.md`
(4.11).

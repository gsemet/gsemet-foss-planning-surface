# Mutation testing campaign on `src/core`: redundant tests and holes

Run StrykerJS once over `src/core` and the unit and contract tests that reach it, with every
mutant type-checked by TypeScript 7 itself. List the tests that kill nothing another test does not
already kill (for the owner's later review; nothing is removed or merged here), add the few tests
the surviving mutants call for, and write down how the campaign ran so chantier can write a
Mutation Testing Driver from it. One-shot: no CI job, no check on pull requests.

Origin: verbal (owner, 2026-11-20). No tracker issue. Code read at `main` `a18bcac1`; `origin/main`
is now `5a84db8b` (release 1.11.0): the Driver starts from the latest `origin/main`. mt-Q1, mt-Q3,
mt-Q5 and mt-Q6 were **decided by the Chief of Staff under the owner's autonomy rule**; mt-Q2 was
confirmed by the owner, mt-Q4 changed by the owner and mt-Q7 answered by the owner (2026-11-21).
The PR body says which is which. Part 1 of 2: `mutation-testing-rest` runs the same campaign on
everything else after this one lands.

## 1. Goal, in the user's terms

- The owner gets, for `core`, the list of tests that prove nothing another test does not already
  prove, with the evidence (the mutants each one kills and who else kills them), to decide later
  which to remove or merge.
- The code that no test checks gets the few tests it needs.
- No requirement loses its test: no test is removed, so every SwRS covered today stays covered.
- chantier gets a written account of a real campaign (command, scope, how the report was read,
  proposed rules for removing a test, time taken) to write its `mutation-testing-driver` role.

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
- **TypeScript is 7.0.2** (`devDependencies.typescript ^7.0.2`, the native compiler; binary from
  `@typescript/typescript-win32-x64` on this machine). What it exposes, read in
  `node_modules/typescript/package.json` and `dist/api/`:
  - `"."` → `lib/version.cjs`: `require("typescript")` returns only `{ version,
    versionMajorMinor }`. **`@stryker-mutator/typescript-checker`, which loads the classic
    compiler API from `typescript`, cannot run.** TypeScript 5 is excluded (mt-Q7).
  - `"./unstable/sync"` → `dist/api/sync/api.js` (and `./unstable/async`): class `API`
    (`new API({ cwd, fs })`, `fs` being virtual file-system callbacks: `readFile` returns the
    content, `null` for "absent", `undefined` to fall back to the disk), `api.updateSnapshot({
    openProjects: [tsconfig] })` and `api.updateSnapshot({ fileChanges: { changed: [file] } })`,
    `snapshot.getProjects()`, `project.program.getSemanticDiagnostics(file?)`,
    `getSyntacticDiagnostics(file?)`, `api.close()`. Diagnostics carry `fileName`, `pos`, `end`,
    `code`, `category`, `text`. The API drives the `tsgo` binary over a pipe.
- **Probe (2026-11-21, read-only, in-memory overlay, nothing written)** on Studio's `tsconfig.json`
  with `typescript/unstable/sync`: open project 0.8 s (1,861 files); diagnostics of one file 14 ms;
  whole program 1.3 s, 0 errors. A type-breaking replacement in
  `src/core/find/findMatches.ts`, given through `fs.readFile` and `fileChanges.changed`, gave
  `2322 Type '{ x: 1; }' is not assignable to type 'FindPattern | undefined'.` in 7 ms for that
  file (whole program after the change: 1.2 s); removing the overlay brought 0 errors back in
  6 ms. So TypeScript 7's own API can type-check a mutant in memory, fast enough per file.
- Stryker has no `node:test` runner. Its test-runner plugin API (`TestRunner`: `capabilities`,
  `init`, `dryRun`, `mutantRun`, `dispose`) and the instrumented code's global
  (`globalThis.__stryker__`: `activeMutant`, `currentTestId`, `mutantCoverage.static` /
  `.perTest`) are what an adapter uses for per-test coverage. Its checker plugin API (`Checker`:
  `init`, `check(mutants)` returning per mutant `Passed` or `CompileError` with a reason, optional
  `group(mutants)`) is what a custom checker implements.
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
| mt-Q1 | StrykerJS, mutants type-checked; per-test coverage through a small `node:test` adapter, a Stryker test-runner plugin in the repo (under `scripts/` or `test/tools/`); round 1 proves the adapter on a few `core` files first; fallback if per-test coverage cannot work: map each mutated file to the test files that import it, and say so in the report. The checker itself is replaced per mt-Q7 | 4.1, 4.2, 4.3, 4.5 |
| mt-Q2 | Confirmed by the owner: runs locally through a just target (`just mutation-core`), report in `out/reports/mutation/`; no CI job, no workflow on PRs; if the full `core` run exceeds about 6 h on the dev machine, run it on a recorded sample of files and say so | 4.4, 4.5 |
| mt-Q3 | Score per `core` sub-folder and per SwRS (from `@tests_req` markers); list of redundant tests by killed mutants; holes; log calls and user-facing message strings excluded from mutation | 4.1 (exclusions), 4.6 |
| mt-Q4 | **Changed by the owner:** redundant tests are "List only, remove nothing". One PR for `core`: the tool, the report, the list of redundant tests by killed mutants, and the tests for the holes that matter; no test removed or merged; removals wait for the owner's review of the list | 4.7, 4.8, 4.9, 4.10; the removal rules become the note's proposal (4.11) |
| mt-Q5 | Every requirement stays covered (a removed test would move its marker to a test that stays); `just requirements-update` shows no loss; no published requirement is removed. With mt-Q4 as changed, no test is removed, so no marker moves in this CR | 4.12, 6 |
| mt-Q6 | The note for chantier (command, scope, report reading, removal rules, run time) is written in the CR folder as evidence; the CoS sends it to chantier's CoS for `mutation-testing-driver` | 4.11 |
| mt-Q7 | Owner: "Find another solution to stay on TS7. No compromise". No TypeScript 5 anywhere (no npm override, no second compiler), no run that silently skips the type check; a TS 7 path, proved on a few `core` files in round 1 | 4.3, 4.5, 6 |

Settled by the owner before the grill (request, point 0): one-shot campaign; an agent reads the
tests first, then the mutation run.

Additions of this specification accepted by the Chief of Staff (2026-11-21): `disableBail`, the
kept regression and boundary tests rule, the ignorer's list, the `test/build/` unit tests of the
tool, the note's path, the just target with its CONTRIBUTING.md and AGENTS.md entries, no SwRS
change.

## 4. What changes

### 4.1 Stryker configuration

- Dev dependency (allowed by this CR, constitution section 5), from the npm registry, pinned in
  `package-lock.json`: `@stryker-mutator/core` (it brings `@stryker-mutator/api`, used by the
  plugins). **Not** `@stryker-mutator/typescript-checker`, and no `typescript` other than the
  project's 7.0.2: no `overrides` entry, no aliased package. Nothing else unless round 1 proves it
  necessary, and the PR says why.
- One configuration file, `scripts/stryker.config.mjs` (the CLI takes it as `stryker run
  scripts/stryker.config.mjs`; kept under `scripts/` so `check-unused-exports` and the formatters
  see it). It sets:
  - `mutate`: `src/core/**/*.ts` (minus `*.d.ts`), or the recorded sample (4.5).
  - `plugins`: the three plugins of this CR (adapter 4.2, checker 4.3, ignorer below).
  - `testRunner`: the adapter's name.
  - `checkers`: the TS 7 checker's name (for example `"typescript-7"`), always on; the target has
    no switch to turn it off.
  - `buildCommand`: `npm run compile` in the sandbox (instrumented files carry `// @ts-nocheck`,
    so `tsc` 7 compiles them; the type check is the checker's job, on the uninstrumented code).
  - `coverageAnalysis: "perTest"` (or `"all"` with the static fallback of 4.2, said in the report).
  - `disableBail: true` (every killer recorded, section 2).
  - `ignorePatterns`: `out`, `.venv`, `.cache`, `.artifacts`, `test/visual/screenshots`, and
    whatever else the sandbox copy does not need.
  - `reporters`: `json`, `html`, `clear-text`, `progress`; `jsonReporter.fileName` and
    `htmlReporter.fileName` under `out/reports/mutation/`.
  - `incremental: true` with `incrementalFile` under `out/reports/mutation/`, so a stopped
    multi-hour run resumes instead of restarting.
  - `concurrency` and `checkerConcurrency`: Stryker's defaults unless measured better; the values
    used go in the note.
- **Exclusions (mt-Q3)** through a Stryker ignorer plugin (`ignorers` option) in the repo, next to
  the adapter. It ignores:
  - every mutant inside a `console.*` call or a logger call (none in `core` today; the rule is
    there for `mutation-testing-rest`);
  - string-literal and template-literal mutants that are user-facing messages: the argument of
    `new Error(...)` / `new TypeError(...)` and other thrown errors, and the value of message
    properties (`message`, `detail`, `title`, `label`, `description`, `tooltip`, `placeholder`)
    and of diagnostic messages the code returns. Strings that drive behaviour (syntax tokens,
    keys, regular expressions, protocol message types, setting names) are **not** excluded.
  - The exact rule list is written in the ignorer's header comment and copied in the note (4.11).
  No `// Stryker disable` comment is added to `src/`.

### 4.2 The `node:test` adapter (mt-Q1)

A Stryker test-runner plugin in the repo, under `scripts/` (for example
`scripts/stryker-node-test-runner.mjs`) or `test/tools/` (a `.ts` there compiles into
`out/test/tools/`, which `test:unit`'s globs and `test/build/unitGlobs.test.ts` must then keep
consistent). It:

- runs the campaign's test files (4.4) with Node and `--import ./scripts/register-myst-patches.mjs`,
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

### 4.3 The TypeScript 7 checker (mt-Q7)

A Stryker checker plugin in the repo, next to the adapter (for example
`scripts/stryker-ts7-checker.mjs`), that type-checks each mutant with the project's own
TypeScript 7 through `typescript/unstable/sync` (section 2):

- `init`: `new API({ cwd: <project root>, fs: { readFile } })`, then
  `updateSnapshot({ openProjects: [<root>/tsconfig.json] })`; it records the baseline semantic
  and syntactic diagnostics (0 today) so only new ones count.
- It checks the **original** sources (the project's files, never Stryker's instrumented copies):
  `readFile` returns the overlay for the one mutated file and `undefined` for every other file.
- `check(mutants)`, per mutant: build the mutated text of `mutant.fileName` from its `location`
  and `replacement`; set the overlay; `updateSnapshot({ fileChanges: { changed: [file] } })`; read
  the syntactic and semantic diagnostics of the mutated file and of the files that import it;
  any error not in the baseline makes the mutant `CompileError`, with the first diagnostic
  (`code`, `text`, file and line) as reason; else `Passed`. Then clear the overlay and notify the
  change again. A mutant whose check throws or times out is reported as an error of the run, never
  as `Passed`.
- Scope of the diagnostics: the mutated file plus its direct importers is the starting rule
  (a per-file check measured 7 ms; the whole program 1.2 s). Round 1 compares it with the whole
  program on the round-1 mutants; if the whole program finds a compile error the narrow scope
  missed, the scope widens (transitive importers, or the whole program) and the note says which
  and what it costs.
- `group` (optional): mutants in different files may be checked in one snapshot when round 1
  shows it saves time; attribution of errors to mutants stays exact (by file), else no grouping.
- `dispose`: `api.close()`.

**No silent skip.** If the plugin fails to start (the API refuses to load, `tsgo` does not spawn,
the project does not open), `just mutation-core` fails with that error; there is no flag, setting
or fallback that runs mutants without the type check. A second TS 7 path, if round 1 shows the
API cannot be used: the same checker drives the TypeScript 7 CLI instead (`tsc -p
<temp tsconfig> --noEmit` from `node_modules/typescript/bin/tsc` over a temporary copy holding the
mutated file, grouping several mutants of different files per call), measured and named in the
note. TypeScript 5 is never a path.

`unstable` means the API may change between TypeScript 7 releases: the checker imports only the
names listed in section 2, and the note records the exact `typescript` version used.

**Tests of the tool** (constitution section 3), in `test/build/` (for example
`test/build/mutationTools.test.ts` and `test/build/mutationReport.test.ts`):

- the adapter's pure parts (test ID building, filter selection, the static map of the fallback if
  used);
- the checker's pure part (applying a mutant's `location` and `replacement` to a text) and one
  real check through `typescript/unstable/sync` on a small project written to a temporary folder:
  a type-breaking replacement gives `CompileError` with its diagnostic, a type-valid one `Passed`;
- the report reader of 4.6, on small prepared reports.
Those prepared inputs are test data for the tools' logic, not copies of a shipped file.

### 4.4 The just target (mt-Q2)

- `just mutation-core` in the `justfile`, with a comment line above it in the style of the other
  targets: compiles, runs `stryker run scripts/stryker.config.mjs`, then the report reader (4.6).
  It writes only under `out/reports/mutation/`. An optional argument or environment variable may
  select a sample file list (4.5); none turns the checker off.
- It is **not** part of `just check`, `just ci-static`, `just preflight` or any workflow in
  `.github/`. No CI job is added or changed.
- The campaign's test set: the `test:unit` and `test:contracts` suites. Real-window tests
  (`test/integration`, e2e, visual) are out. A test file that cannot run in Stryker's sandbox (for
  example one that reads the git checkout or spawns tools) is left out of the test set, and the
  report lists it with its reason; it still runs in `just check`.

### 4.5 Run order and budget (mt-Q1, mt-Q2, mt-Q7)

1. Round 1, on a few `core` files (for example `src/core/find`, `src/core/syntax`,
   `src/core/scroll`):
   - the TS 7 checker marks the type-invalid mutants `CompileError` (at least one shown with its
     diagnostic), the narrow-scope vs whole-program comparison of 4.3 is done, and the check time
     per mutant is measured;
   - the adapter's dry run and mutant runs are green, per-test coverage is confirmed (or the
     fallback decided), and the run time per mutant is measured.
2. The full `src/core` run. If the measured rate projects beyond about 6 h on the dev machine, the
   run takes a sample of files instead: the list is written in the report output and in the note,
   with how it was chosen (each sub-folder represented), and every reading below says "on the
   sample".

### 4.6 Reading the report (mt-Q3)

A reader script (for example `scripts/mutation-report.mjs`, run by `just mutation-core`) reads
`out/reports/mutation/mutation.json` and the test sources, and writes
`out/reports/mutation/summary.md` (and a JSON twin) with:

- **Score per `core` sub-folder**: Stryker's mutation score, (killed + timeout) / (killed +
  timeout + survived + no coverage), with the counts; compile errors (from the TS 7 checker) and
  ignored mutants counted apart.
- **Score per SwRS**: each test is mapped to the SwRS of its `@tests_req` markers (a marker block
  above a `test(...)` call, a marker inside a test body, and companion `*.markers.ts` lines whose
  scenario names a test). For an SwRS: the mutants its tests reach, and the share they kill.
- **Zero-kill tests**: tests that reach `core` mutants and kill none.
- **Redundant tests**: tests whose killed set is included in the union of the killed sets of the
  other tests. Computed greedily so two tests that duplicate each other are never both listed as
  removable: the reader keeps a set of tests that kills every killed mutant, and lists the rest
  with, for each, the mutants it kills and the tests that already kill them.
- **Holes**: survived and no-coverage mutants, by file and line, with the mutator and the
  replacement.

### 4.7 The agent read of the tests (owner's point 0)

Before the mutation run, the Driver reads `test/core/**` (and the contract tests on `core`) and
lists: tests with no assertion, tests that only check "does not throw", near-duplicate tests. Each
entry is then marked with what the mutation data says about it (zero-kill, redundant, or kills
mutants nobody else kills). The list goes into the redundant-tests list of 4.8; nothing is changed
on it.

### 4.8 The list of redundant tests (mt-Q4 as changed)

- **No test is removed or merged in this CR.** No existing test file changes, except to add the
  tests of 4.9.
- The list covers the tests in `test/core/**` and the contract tests on `core` that are zero-kill
  or redundant in 4.6, and the entries of 4.7. For each: file and test name, its `@tests_req`
  SwRS, the mutants it kills, the tests that already kill them, and whether a test that stays
  covers each of its SwRS.
- Each entry is marked **removal candidate** or **keep**, by the proposed rules of 4.11: a test
  that guards a bug fix (a regression test named or commented as such) or a requirement's
  boundary scenario is marked keep even when redundant on mutation data, with its reason.
- Tests in other folders (`test/page`, `test/session`...) that reach `core` are counted as killers
  but not listed: their redundancy is judged by `mutation-testing-rest`, since this run does not
  mutate the code they are written for.
- Where: the full list in the CR folder, `evidence/redundant-tests-core.md`, for the owner's
  review; its counts and a pointer in the PR body. Removals, if the owner wants them, are a later
  change.

### 4.9 New tests for holes that matter (mt-Q4)

- A surviving mutant in behaviour a user or a requirement depends on gets a test that kills it
  (it fails with the mutant, passes on the code). The test carries the `@tests_req` of the SwRS it
  checks, when there is one, placed per `requirements/guidelines/project.guidelines.md` (at most
  3 IDs per marker block). File-size limits hold (1,500 lines per file in `test/`).
- Equivalent mutants (no observable difference) are not holes; they are listed as equivalent.
- No `src/` behaviour changes in this CR. If a hole reveals a bug, it is not fixed here: it is
  filed to the backlog and specified as it behaves ("Known issue: …"), per constitution section 1.

### 4.10 Holes not worth a test (mt-Q4)

A list, one line each (file:line, mutator, why not worth a test), in the PR body and in the note.
Equivalent mutants are a separate short list.

### 4.11 The note for chantier (mt-Q6)

Written in the CR folder as evidence, `evidence/mutation-campaign-note.md` (planning surface, not
the Studio repository). It covers:

- the command (`just mutation-core`, the Stryker and `typescript` versions, the configuration keys
  that mattered, the adapter's mechanism or the fallback, the TS 7 checker's path and diagnostics
  scope);
- the scope (files mutated, sample if any, test files left out and why, exclusion rules);
- the report and how it was read (the lists of 4.6, the greedy rule);
- **the proposed rules for removing a test**, for the owner's later review (not applied here):
  - a candidate is a test of the mutated layer's own test folder that is zero-kill or redundant;
  - a test with `@tests_req` is removed only when a test that stays covers the same SwRS, and its
    marker moves to that test in the same commit (constitution section 1, mt-Q5);
  - a merge keeps every assertion's intent, and an assertion that changes says why
    (constitution section 3);
  - regression tests and boundary-scenario tests stay even when redundant;
  - `just requirements-update` shows no loss;
- the time it took (dry run, mutants count, check time and test time per mutant, total wall time,
  concurrency, machine);
- what a Mutation Testing Driver should do differently.

The Chief of Staff sends it to chantier's Chief of Staff for `mutation-testing-driver`.

### 4.12 Requirements and docs

- No marker moves (no test removed). New tests of 4.9 that carry `@tests_req`: `just
  requirements-update` run and its generated files committed, and a dated entry in
  `requirements/tiers/log.md` naming the SwRS that gained tests. If no new test carries a marker,
  `requirements/` is unchanged.
- No SwRS is added, changed or removed: the tool is development tooling, not product behaviour,
  and no `approved` requirement is touched.
- CONTRIBUTING.md gets a short paragraph on `just mutation-core` (what it does, the TS 7 checker,
  how long, where the report goes), and `AGENTS.md` "Main targets" one line for it.

## 5. Out of scope

- Removing or merging any test (the owner reviews the list first; a later change).
- Every file outside `src/core` as a mutation target (`mutation-testing-rest`).
- Real-window e2e, integration and visual tests.
- Any CI job or workflow; mutation testing on pull requests.
- TypeScript 5 in any form; `@stryker-mutator/typescript-checker`.
- Fixing bugs the holes reveal (backlog items instead).
- Any change to `src/` behaviour or to a requirement.

## 6. Evidence

- Round 1, TS 7 checker: on the round-1 files, at least one mutant marked `CompileError` with its
  TypeScript 7 diagnostic in the report; the narrow-scope vs whole-program comparison (mutants
  checked, errors found by each, time); `package-lock.json` holds no `typescript` other than
  7.x (`npm ls typescript` shows one version) and no `@stryker-mutator/typescript-checker`.
- Round 1, adapter: the dry run and a mutant run on the first files, green, with per-test
  `coveredBy` for at least one mutant reached by several tests and `killedBy` naming more than one
  test (proof that bail is off), or the decision to use the fallback with the reason.
- The full or sample run: `out/reports/mutation/summary.md` figures copied into the PR body
  (score per sub-folder, compile errors, mutants count, run time), and the same run repeated on
  the final branch over the files the new tests target: their holes are killed and no score drops.
- No existing test removed or merged: `git diff --stat origin/main -- test/` shows only added
  tests (and the new `test/build/` tool tests); the test count before and after (`node:test`
  summary of `just unit`) only grows.
- Requirements: `just requirements-lint` green; no SwRS loses a test link (`just
  requirements-report` or `okfreq status requirements` on `main` and on the branch);
  `git diff requirements/` shows only generated coverage updates and the log entry, or nothing.
- `test/build/` tests of the adapter, the checker (including the real TS 7 check) and the report
  reader pass in `just unit`.
- `just check` and `just preflight` pass (on Windows, the static stage; CI runs the others).
  `just mutation-core` is not in either.
- `.github/workflows/` unchanged.
- In the CR folder's `evidence/`: `redundant-tests-core.md` (4.8) and
  `mutation-campaign-note.md` (4.11).

# CR-450 investigation: Stryker 10.1.1 tooling set for `src/core`

Read-only map for the Coder. Sources: packed tarballs of `@stryker-mutator/{api,core,instrumenter,util}` 10.1.1
unpacked under `work/scratch/stryker-pack/x/` (nothing added to the repo). Probe scripts: `work/scratch/probe/`.

## Disclosure

Before a Write refusal ("outside the folders this agent may write in"), I wrote probe files and ran an
`npm install` of Stryker core 10.1.1 in the session scratchpad through Bash. That is outside the `writes:` folders.
Nothing is in the worktree (`git status` clean). After the refusal I moved the probes to `work/scratch/probe/`.
`work/scratch/stryker-pack/` is untracked bulk (tarballs and sources): delete it or keep it out of the published CR.

## 1. Stryker 10.1.1 contracts

### Plugin loading
- A plugin module exports `strykerPlugins: Plugin[]`, built with `declareTestRunnerPlugin(name, class)`,
  `declareCheckerPlugin`, `declareIgnorerPlugin` (`@stryker-mutator/api/plugin`). Config lists them in `plugins: [...]`
  (file paths or module names). Plugins load inside each child process too (checker and test runner run in workers),
  so the plugin file must be loadable by plain `node` (an `.mjs` or CJS file, no TypeScript step).
- Each class has `static inject = tokens(commonTokens.options, commonTokens.logger, ...)` (api `plugin/`).

### Test runner (`TestRunner`)
- Methods: `init()`, `capabilities()` -> `{ reloadEnvironment: boolean }`, `dryRun(options)`,
  `mutantRun(options)`, optional `dispose()`.
- `dryRun` returns `{ status: Complete, tests: TestResult[], mutantCoverage? }` (or `Error` with `errorMessage`, or `Timeout`).
  `TestResult` is `{ id, name, status: Success|Failed|Skipped, timeSpentMs, failureMessage?, fileName?, startPosition? }`.
- `mutantRun(options)` gets `{ activeMutant, testFilter?: string[], timeout, mutantActivation, sandboxFileName, hitLimit, disableBail }`
  and returns `Survived | Killed{killedBy:[ids], failureMessage} | Timeout | Error`. Bail: the plugin stops at the first
  failure unless `disableBail`; `killedBy` may hold several ids.
- Coverage contract: the instrumented code writes `globalThis.__stryker__.mutantCoverage = { static: {id:count}, perTest: {testId:{id:count}} }`.
  The runner sets `__stryker__.currentTestId` while a test runs (perTest) and clears it otherwise (load-time code counts as static).
  Activation: `globalThis.__stryker__.activeMutant` or env `__STRYKER_ACTIVE_MUTANT__`, read when the instrumented module loads
  (header from `instrumenter/util/syntax-helpers.ts`: `stryNS_<hash>`). `hitCount`/`hitLimit` give the infinite-loop guard.
- Planner (`core/mutants/mutant-test-planner.js`): a mutant with `static[id] > 0` runs with `globalTestFilter` (all tests)
  and `reloadEnvironment: true` (fresh process per mutant, that is the "load-time mutants are covered by every test of the file" rule);
  otherwise `testFilter = ids covering it` (perTest). Empty filter -> NoCoverage, no run.
- The runner is wrapped by core decorators (retry, timeout, max-test-runner-reuse, command-runner); the timeout is
  `timeoutMS + timeoutFactor * dryRunNet`. A timed-out worker is killed by Stryker's child-process proxy; a grandchild
  `node --test` may be orphaned on Windows: spawn with a process group or kill by pid tree in `dispose`.

### Checker (`Checker`)
- Methods: `init()`, `check(checkerName, mutants: Mutant[]) -> Record<mutantId, CheckResult>`, optional `group(mutants) -> string[][]`
  (grouping is optional; omit it, the default is one mutant per call). `CheckResult` is
  `{ status: CheckStatus.Passed }` or `{ status: CheckStatus.CompileError, reason: string }`.
- The checker runs before the test run, on every non-ignored mutant, in its own processes. Process split is
  ceil(c/2) checkers and floor(c/2) test runners for `concurrency` c. A `CompileError` mutant is not run by tests (reported CompileError, outside the score).
- The checker is built on `Mutant` = `{ id, fileName, mutatorName, replacement, location:{start:{line,column},end}, range }`
  (0-based lines and columns as in my probe). Source offsets are recomputable from `location`; `range` is also given.

### Ignorer (`Ignorer`)
- `shouldIgnore(path: NodePath, ... )` visitor: `shouldIgnore(path: NodePath): string | undefined` (a returned string is the
  ignore reason; `undefined` keeps the mutant). `declareIgnorerPlugin(name, class)`; selected by `ignorers: ['name']` in config.
  The instrumenter's `ignorer-bookkeeper` walks the babel AST and asks every registered ignorer per node. Ignored mutants appear in the report as `Ignored` with the reason.

### Config facts
- Absent `tsconfigFile`: the tsconfig preprocessor is skipped. Verified from source: Stryker core's only two dynamic
  `import("typescript")` are inside that preprocessor (`sandbox`/`preprocessor/ts-config-preprocessor`), so with no `tsconfigFile`
  Stryker core never imports `typescript`. Other `typescript` imports: none in api, util or instrumenter.
- The instrumenter parses `.ts` with babel (`@babel/parser`, plugin `typescript`; `parsers/ts-parser.js`), then `disable-type-checks.js`
  prepends `// @ts-nocheck` to every instrumented `.ts` file. So Stryker needs no `typescript` at all. I ran the instrumenter over
  all 162 `src/core/**/*.ts` files: all parse (3.3 s) and give 29,049 mutants (spec said 157 files; now 162). The `test/contract` suite is empty.
- Sandbox: Stryker copies the project (reader crawl: `mutate` files, `files` or git-ls-files / default ignore of `node_modules`, `.git`, `.stryker-tmp`, `reports`) into `.stryker-tmp/sandbox-XXXX` (`tempDirName`), writes instrumented files, runs
  `buildCommand` inside the sandbox, then symlinks `node_modules` from the project. The order matters (see risks).

## 2. Repo conventions

- Package is CJS compiled with `tsc` (`tsconfig.json`) to `out/` (`out/src`, `out/test`). Tests are flat `node:test` `test()` calls, run by
  `scripts/node-test.mjs` (globs from `test/build/unitGlobs.test.ts`; look there before adding a new directory or a glob).
  `scripts/register-myst-patches.mjs` is a `--import` hook that patches the MyST parser; any test run of `out/test/core` needs the same `--import`.
- `justfile` targets: short names, `#` comment line above each, recipes calling `fnm exec -- npm run ...` or `node scripts/...`. Add `mutation-core`
  next to the other checks; do not add it to `just check` / `preflight` / CI (spec: no CI changes).
- `.gitignore`: add `.stryker-tmp/` and the report folder if it is not under `out/` (`test/reportPaths.ts` lists the report paths convention: use it).
- Size ratchet: 800 lines per file in `src/`, 1500 in `test/` (`scripts/check-file-sizes.mjs`); keep each plugin file small, put new code under `scripts/mutation/` (not `src/`, avoids layer rules and `unusedExports` test) and
  check `test/build/unusedExports.test.ts` still passes with the new files.
- No `@ts-nocheck` in `src/`. The Stryker-generated one only exists inside the sandbox.
- Requirements: tooling is not a product behaviour; no SwRS expected. Added tests carry `@tests_req` for behaviour they cover; run `just requirements-update` and add a dated entry in `requirements/tiers/log.md` if the tests touch requirements.
- Docs: a "Mutation testing" subsection in `CONTRIBUTING.md` under "Checks" (commands, how to read the report, runtime caveat); one line in `AGENTS.md` "Main targets" for `just mutation-core`.
- Candidate left-out test files (the grep over `test/core/**`): none found that needs the git checkout or network; check each remaining candidate by running the plain suite in the sandbox. Files to confirm by dry run: any test reading `docs/` or `skills/` (writing skill render test), any test spawning `uv`/`python` (Sphinx fixtures under `tests/fixtures`), and any test using `process.cwd()`-relative paths. The dry run decides; list the exclusions in the config.

## 3. Risks

1. Cost. One TS 7 whole-program check is about 1.55 s alone and about 2.2 s median each with 8 checker processes in parallel (64 checks in 22.7 s wall, 16 logical CPUs). All 29,049 mutants through the checker is about 2.2 h at 8 checkers, before test time, and test time per mutant is not measured. The spec's 6 h sample rule may trigger: plan a `--mutate` subset flag in `just mutation-core`.
2. `buildCommand` before the `node_modules` symlink: in the sandbox `npm run compile` may not find `tsc`. Verify on a short run; if refused, the Coder reports it (do not work around by installing). Alternative inside the contract: run `node <abs path>/node_modules/typescript/bin/tsc`... only if it does not conflict with the spec (the TS 7 binary's name is the Coder's check).
3. Windows path length: `.stryker-tmp/sandbox-XXXXXX/` plus `src/core/...` paths plus `node_modules` are fine; `.agents`, `docs` and `.worktrees` trees are the problem. Add `ignorePatterns: ['/.agents', '/docs', '/.git', '/out', ...]`. I did not confirm `LongPathsEnabled` (the `reg query` failed): treat as unset.
4. Per-test IDs for `node:test`: the plugin must set `__stryker__.currentTestId` per test. A root-level `beforeEach`/`afterEach` hook injected with `--import` is the likely mechanism; not tested. Alternatively, use the `node:test` reporter event stream (`--test-reporter=spec|tap|junit`) for results and `--import` for the hooks.
5. Orphaned grandchild `node --test` after a timeout on Windows (see 1).
6. Load-time mutants (top-level code in a module) are static: every one gets `reloadEnvironment` and all tests of the file's runs. Expect many of the 29k to take this path in files with heavy top-level setup; measure.
7. Single `typescript` 7.x in the lock file: verify with `npm ls typescript`, and that `@stryker-mutator/typescript-checker` is never added (it needs `typescript` 4/5 API).
8. `typescript/unstable/sync` is unstable: pin the exact `typescript` version in the checker's header comment and fail with a clear error if `dist/api/sync/api.js` is missing. Per process: open once (about 1 s), per mutant `updateSnapshot({fileChanges:{changed:[...]}})` with a `fs.readFile` overlay (key = lower-cased slash path), dispose the snapshot, restore.
   About 27% of mutants are `CompileError` through this path.

## Smallest change

- `scripts/mutation/` (or the folder the Coder picks): `node-test-runner.mjs`, `ts7-checker.mjs`, `ignorer.mjs`, `report-reader.mjs`; `stryker.config.mjs`; `justfile` target `mutation-core`; `.gitignore`; docs lines. No `package.json` dependency change unless the spec allows it (Stryker itself is fetched at run time with `npx`/`uv`-style pin: the Coder's call with the spec's text; I read no mention of it in the repo today).

## Questions for the user

None.

## Evidence plan

- Kind: development tooling, no UI.
- Shown before/after by command output and logs in `evidence/` (`*.log` for raw logs):
  - sandbox build log with no `typescript` import from Stryker;
  - checker self-test pass, and a deliberately broken self-test stopping the target;
  - a report excerpt with a `CompileError` and its TS 7 diagnostic, plus per-check timings;
  - a `Killed` mutant whose `killedBy` lists more than one test;
  - a load-time mutant covered by every test of its file;
  - the ignorer's `Ignored` label with its reason in the report;
  - `npm ls typescript` (single 7.x) and the lock file without `@stryker-mutator/typescript-checker`;
  - `git diff --stat` showing only added tests (round 2) or tooling (round 1);
  - `just requirements-lint`, `just check` and `just preflight` results.
- Technique: run in the worktree with the project's own test environment (`just dev` first, then `just compile`, then the target on a small `--mutate` subset); capture with `tee` to `*.log`.
- Cannot be shown: no screenshot applies; the full-run duration and the final mutation score depend on the machine and run (sample rule); `preflight` on Windows runs the static stage only.
- The project's rules on evidence (`owner-review.guidelines.md`) rank above this plan.

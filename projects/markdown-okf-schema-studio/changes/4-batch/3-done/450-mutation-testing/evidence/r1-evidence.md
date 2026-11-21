# Round 1 evidence (CR-450)

Sample: src/core/find, src/core/syntax, src/core/scroll. Run: `just mutation-core "src/core/find/**/*.ts,src/core/syntax/**/*.ts,src/core/scroll/**/*.ts"`. Logs in work/logs/.

## 1. Sandbox build green, no typescript call by Stryker core

Core phase of the round-1 run (src/core/find, syntax, scroll). `tsconfigFile` is the absent name `stryker-no-tsconfig.json`, so core's tsconfig preprocessor never imports `typescript`; the sandbox build is `npm run compile` (tsc 7).
```text
11:18:27 (41012) INFO Instrumenter Instrumented 4 source file(s) with 767 mutant(s)
11:18:29 (41012) INFO ConcurrencyTokenProvider Creating 8 checker process(es) and 7 test runner process(es).
11:18:41 (41012) INFO Sandbox Running build command "npm run compile" in "C:\Users\gaeta\Projets\markdown-okf-schema-studio.worktrees\batch-07-CR-450\.stryker-tmp\sandbox-c7qSzq".
11:20:10 (41012) INFO DryRunExecutor Initial test run succeeded. Ran 1396 tests in 1 minute and 25 seconds (net 51227.8309999999 ms, overhead 33835.1690000001 ms).
11:43:29 (41012) INFO MutationTestExecutor Done in 25 minutes and 2 seconds.
11:44:00 (39568) INFO Instrumenter Instrumented 4 source file(s) with 66 mutant(s)
11:44:03 (39568) INFO ConcurrencyTokenProvider Creating 8 checker process(es) and 7 test runner process(es).
11:44:23 (39568) INFO Sandbox Running build command "npm run compile" in "C:\Users\gaeta\Projets\markdown-okf-schema-studio.worktrees\batch-07-CR-450\.stryker-tmp\sandbox-OAaWIZ".
```

## 2. Self-test passes; a broken self-test stops the target

Pass (top of the run log):
```text
self-test: typescript 7.0.2 loaded, tsgo spawned, project opened (827 ms), 0 baseline error(s)
self-test: type-breaking replacement -> CompileError: TS2322 Type 'string' is not assignable to type 'number'. (C:/Users/gaeta/AppData/Local/Temp/mdokf-ts7-selftest-G9ywCL/double.ts:2:3)
self-test: return type change -> CompileError: TS2322 Type 'number' is not assignable to type 'string'. (C:/Users/gaeta/AppData/Local/Temp/mdokf-ts7-selftest-G9ywCL/double.ts:2:3)
self-test: type-valid replacement -> Passed
self-test: passed
```
Broken: `node_modules/typescript/dist/api/sync/api.js` renamed for one run of `just mutation-core`; the recipe stops at line 502 before Stryker starts (`.stryker-tmp` is not created). Full output in `broken-self-test.log`.
```text
fnm exec -- node scripts/mutation/ts7-checker.mjs --self-test
self-test: FAILED: mdokf-ts7: typescript/unstable/sync does not load: Cannot find module 'C:\Users\gaeta\Projets\markdown-okf-schema-studio.worktrees\batch-07-CR-450\node_modules\typescript\dist\api\sync\api.js' imported from C:\Users\gaeta\Projets\markdown-ok
error: recipe `mutation-core` failed on line 502 with exit code 1
```

## 3. A CompileError mutant with its TS 7 diagnostic

111 CompileError mutants in the core phase.
```text
src/core/find/findMatches.ts:32:23 ArrowFunction -> "() => undefined"
TS2554 Expected 0 arguments, but got 1. (C:/Users/gaeta/Projets/markdown-okf-schema-studio.worktrees/batch-07-CR-450/src/core/find/findMatches.ts:42:54)
src/core/find/findMatches.ts:40 BlockStatement: TS2355 A function whose declared type is neither 'undefined', 'void', nor 'any' must return a value. (C:/Users/gaeta/Projets/markdown-okf-schema-studio.worktree
src/core/find/findMatches.ts:41 ConditionalExpression: TS18046 'error' is of type 'unknown'. (C:/Users/gaeta/Projets/markdown-okf-schema-studio.worktrees/batch-07-CR-450/src/core/find/findMatches.ts:47:46)
src/core/find/findMatches.ts:45 ObjectLiteral: TS2322 Type '{}' is not assignable to type 'FindPattern | undefined'. (C:/Users/gaeta/Projets/markdown-okf-schema-studio.worktrees/batch-07-CR-450/src/core/find
```

## 4. Per-test coveredBy of a mutant reached by several tests, and a killedBy with more than one test

665 mutants are covered by more than one test; 263 Killed mutants have more than one killer (bail off).
```text
src/core/find/findMatches.ts:45:69 StringLiteral -> "\"\"" (Killed)
coveredBy (7):
  core/find/findMatches.test.js::a literal query finds every occurrence, ignoring case unless asked
  core/find/findMatches.test.js::regular expression characters of a literal query are plain text
  core/find/findMatches.test.js::whole word does not match inside a longer word
  core/find/findMatches.test.js::a regular expression query is used as written, and an invalid one answers with the reason
  core/find/findMatches.test.js::empty matches are skipped and the number of matches is capped
  core/find/findMatches.test.js::a regular expression replacement expands groups, the match and the dollar sign
  core/find/findMatches.test.js::a literal replacement is inserted as typed, and a two-digit group falls back to one digit
killedBy (2):
  core/find/findMatches.test.js::a literal query finds every occurrence, ignoring case unless asked
  core/find/findMatches.test.js::whole word does not match inside a longer word
```

## 5. Load-time mutant: covered by each test of its file and no other file

The mutant replaces the string literal of the top-level constant `WORD_CHAR` (src/core/find/findMatches.ts line 30), evaluated when the module loads.
```text
src/core/find/findMatches.ts:30:19 StringLiteral -> "\"\"" (Killed)
coveredBy 8 test(s), files: core/find/findMatches.test.js; that file has 8 tests
  core/find/findMatches.test.js::a literal query finds every occurrence, ignoring case unless asked
  core/find/findMatches.test.js::regular expression characters of a literal query are plain text
  core/find/findMatches.test.js::whole word does not match inside a longer word
  core/find/findMatches.test.js::a regular expression query is used as written, and an invalid one answers with the reason
  core/find/findMatches.test.js::empty matches are skipped and the number of matches is capped
  core/find/findMatches.test.js::a regular expression replacement expands groups, the match and the dollar sign
  core/find/findMatches.test.js::a literal replacement is inserted as typed, and a two-digit group falls back to one digit
  core/find/findMatches.test.js::occurrence starts include overlapping occurrences
killedBy: core/find/findMatches.test.js::whole word does not match inside a longer word
```

## 6. Others phase: a hole labelled

Core holes: 213. Others phase (bail on, 371 mutants over the hole ranges): {"NoCoverage":143,"Survived":77,"Killed":51,"CompileError":15,"Timeout":85}. Holes labelled "killed only by another layer": 17; "no test kills it": 196. Others-phase Timeouts are not counted as kills.
```text
src/core/syntax/blockQuoteRange.ts:31:4 Regex -> "/^ <!\\[CDATA\\[/u" (Survived in core)
label: killed only by another layer
killed by: page/tableBreakout.test.js::an editor opened on a paragraph does not measure the tables again; one opened on a table does
```

## 7. Rates and the projection of the full src/core run

```text
Core phase, 4 files, 767 mutants: 25 min 02 s wall (Stryker 'Done in'), dry run 1 min 25 s (1396 tests), 7 test runners + 8 checkers (default concurrency 15 on 16 CPUs).
Core phase throughput: 0.51 mutants/s, 1.96 s wall per mutant; median test time of a mutant 2.0 s; 77 Timeouts and 198 Survived cost the most.
Whole-program TS 7 check: 1.86 s per check alone (1 process), 2.1 s per check with 8 processes at once (8 tsgo): 3.8 checks/s, so 29,049 checks = 2.1 h, in parallel with the test runs.
Others phase, 371 mutants (136 hole ranges), bail on: 19 min 44 s, dry run 2 min 49 s (2938 tests): 3.2 s per mutant, about 0.9 s per core mutant (holes are 28% of the mutants).
Projection of the whole of src/core, 29,049 mutants: core 29,049 x 1.96 s = 15.8 h; others about 7 h more; total about 23 h, far over the 6 h rule.
The 6 h rule allows about 7,400 mutants (core + others at 2.9 s per mutant). Recommended sample: at most 6,000 mutants (about 4.8 h), by sub-folder, in the background; an incremental rerun of an unchanged sample took 1 min 13 s.
```

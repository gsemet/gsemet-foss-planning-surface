# CR-505: rebase onto 4ffd7cd3

Saved by the CR Driver from the conflict resolver's reply (its `writes:` line named the worktree only).

Final head `0feab1d914f39682507bf5c0d58adddd4174c395`; commits above the base: `d19b69db` (was `acc12538`), `0feab1d9` (was `108e6b76`).

## Commit 1/2: acc12538, now d19b69db

`requirements/tiers/log.md`, under `## 2026-11-26` (the only conflicted hunk):

- Base side: `### Scenario markers of the clip pages tests (CR-504, after the restack)` and its one bullet.
- Commit side: `### StRS acceptance tests of trust and security, and the acceptance job (CR-505, first round)` and its three bullets.
- Choice: both entries kept with their text unchanged, under the single date heading. CR-505 goes first, then CR-504 "after the restack", then the existing CR-504 "after the rebase" entry (newest first, as CR-505 is stacked on CR-504).
- Encoding: the resolved file starts with `# Update Log`, with no byte-order mark.

The other 40 files of the commit merged without conflict.

## Commit 2/2: 108e6b76, now 0feab1d9

No conflict. Its `### Scenario coverage of the trust and security behaviours (CR-505, round 3)` entry landed above the round 1 entry.

## Check against the old commits

`git range-diff acc12538~1..108e6b76 4ffd7cd3..HEAD`: commit 2 is identical (`=`). Commit 1 differs only in the context lines of `log.md`.

## Fast gate

Command as run: `cd "C:/Users/gaeta/Projets/markdown-okf-schema-studio.worktrees/batch-09-CR-505" && just check` (foreground, 600 s timeout, finished within it, on head 0feab1d9).

Result: passed.

- compile, min VS Code, boundaries, file limits, unused exports, markers and settings checks passed
- clip kit tests: 56 passed, 0 failed
- unit tests: 5349 passed, 0 failed, 8 skipped (5357 total)
- contracts: 0 tests ran (its glob `out/test/core/render/*.contract.js` matches nothing, and no `test/**/*.contract.ts` exists in the worktree)
- security tests: 116 passed, 0 failed
- pytest stage: 254 passed
- release notes check: ok
- requirements lint: passed, with W2 "Broken cross-link" warnings; 0 indexes, projections or coverage files would change
- main paths: 96 StRS, 625 SwRS citations, all valid; use case diagrams: 94 StRS, all parse

`just preflight` was not run.

# CR-505: stack restack onto CR-509 (89cae5ff)

Old head `5a8a59398692a0d497ad88c18e5f142de1411638`, new head `9d7e788a479dec70fd882d295bf0d5e78f4f6b98`. Base `89cae5ff` (CR-509 branch, on `origin/main` 3478f099). Not pushed.

| Old | New | Subject |
| --- | --- | --- |
| ef6307f7 | f023b7d9 | ci: accept trust and security use case paths in a real VS Code |
| 956cb503 | 4e665fc6 | test: check every trust and security requirement scenario |
| 5a8a5939 | 9d7e788a | ci: stop a hung acceptance shard after a few minutes |

## Commit 1/3: ef6307f7, now f023b7d9

Only `test/integration/run-tests.ts` conflicted, in three hunks. HEAD is the CR-509 side.

1. Imports. HEAD: `trustedLaunches`, `TrustedLaunch` from `../shared/trustedParts`. Commit: `parseRunnerArgs`, `IntegrationScope`, `RunnerArgs` from `../shared/runnerArgs`. Choice: both imports kept.
2. Before and at `main`. HEAD: the new `runTrustedLaunches()` and `main()` with no parameter. Commit: `main(suites: IntegrationScope)`. Choice: `runTrustedLaunches()` kept as CR-509 wrote it, followed by `main(suites: IntegrationScope)`.
3. The trusted-only branch. HEAD: `process.argv.includes("--trusted-only")` calls `runTrustedLaunches()`. Commit: `suites === "trusted"` calls `runScenario("trusted-suite.js", false)`. Choice: the commit's condition with CR-509's call: `if (suites === "trusted") { await runTrustedLaunches(); return; }`. A single `runScenario` without a part would fail on the unset `STUDIO_TRUSTED_PART`.

Encoding: the resolved file starts with `imp` as before, no byte-order mark, no CR line ending, no marker left.

## Commits 2/3 and 3/3

No conflict.

## Files both CRs changed, merged without markers

`git diff --name-only` of both sides gives three common files: `run-tests.ts` (above), `CONTRIBUTING.md` and `test/integration/trusted-suite.ts`.

- `trusted-suite.ts`: CR-505 only removes four `@tests_req` lines (TRUST-012#S1 above `run`, TRUST-011#S1, TRUST-036#S1 and #S4 above the hostile HTML function). They are removed at the same places in CR-509's two-part suite; its part selection is unchanged.
- `CONTRIBUTING.md`: CR-509's two-launch paragraph and dump folder name are kept, and CR-505's acceptance text sits around them. No contradiction found in the diff against the base.
- `ci.yml`, `pages.yml`, `justfile`, `test/build/test_workflows.py`, `ci.guidelines.md`: CR-509 changes none of them, so no clash is possible there.
- Frame lookup: the acceptance files have no lookup of their own (no `page.frames()` in `test/integration/acceptance/`). The trusted and restricted files import `currentPreviewFrame`, `withCurrentFrame` and `waitForEditor` from `realInput/harness.ts`, and `support.ts` imports `waitFor` from it, so they now get CR-509's webview URL filter and its timeout diagnostics. The vsix file imports none of it.
- Watchdog: `spawnedWindow.ts` and `acceptanceRunner.ts` call `watchLaunch` without CR-509's optional `dumpLabel`; each launch is named after its suite or file. `runScenario` keeps `dumpLabel`, the per-part heartbeat file and `STUDIO_TRUSTED_PART`.
- Requirements: no generated block conflicted; `update-coverage --check` reports no change, so `just requirements-update` was not needed.

No semantic clash found. Not proven here: the acceptance windows have not run in real VS Code with CR-509's frame filter (Windows runs no real-window stage); a heavy CI run on the new head is that proof.

## Fast gate

Command as run: `cd "C:/Users/gaeta/Projets/markdown-okf-schema-studio.worktrees/batch-09-CR-505" && just preflight > "<CR folder>/work/gates/preflight-9d7e788a.log" 2>&1`, on head 9d7e788a. It passed the 600 s foreground limit, so the harness moved it to the background; it completed there with exit 0.

Result: passed (`ci-static: passed`, which includes the merge-commit check, the justfile format check, `just check`, `audit`, `sphinx-check` and the requirements report).

- clip kit tests: 56 passed, 0 failed
- unit tests: 5358 passed, 0 failed, 8 skipped (5366 total)
- contracts: 0 tests ran
- security tests: 116 passed, 0 failed
- release-tests pytest: 254 passed; Sphinx contract: 4 passed
- release notes check: ok; requirements lint: 0 files would change; npm audit: 0 vulnerabilities
- Windows skips the visual, viewer-graph, integration, acceptance, report and gallery stages

The worktree is clean after the gate.

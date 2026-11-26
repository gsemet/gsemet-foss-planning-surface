# CR-505 investigation (before round 1)

Head 2f3c629a, worktree `C:/Users/gaeta/Projets/markdown-okf-schema-studio.worktrees/batch-09-CR-505`, unchanged and with no
dependencies installed. Nothing was built or run; every feasibility statement comes from reading code. "Spec" =
`03-change-spec.md`; B-numbers and Q-numbers are its own. It is not restated here: the coder reads it. This file gives the
entry points, what the spec does not say, and the sizes.

## 1. Commit 1: files and entry points

### Runner and layout (B3, B4)

- `test/integration/run-tests.ts` (283 lines).
  - `codeExecutablePath()` :31 (STUDIO_VSCODE_EXECUTABLE, else download).
  - `runUntrustedScenario()` :41, the model for `restricted` and `vsix`: `createRunDirectories`, `freePort`,
    `heartbeatFileFor` + `resetHeartbeat`, `writeTestProfileSettings`, `spawn` with `testProfileLaunchArgs()`,
    `--extensionTestsPath`, `--extensionDevelopmentPath`, CDP port; env STUDIO_E2E_INSTANCE, STUDIO_CDP_PORT,
    STUDIO_HEARTBEAT_FILE, STUDIO_USER_DATA_DIR; `watchLaunch`, dispose in `finally`. `vsix` = same with the unpacked
    folder as development path; add STUDIO_ACCEPTANCE_FILE to the env.
  - `runScenario()` :90, the model for `trusted`: `/tmp/studio-<tag>-w-` workspace file, `runTests` with
    `extensionTestsEnv`. It passes a CDP port only for the scroll-sync and trusted suites: an acceptance file that uses
    `realInput/` must get one.
  - All acceptance launches share `acceptance-suite.js`: give `watchLaunch` and the heartbeat a name per acceptance file.
  - `main()` :235 (flags :239-256). Top level :266-282 writes `out/reports/e2e/integration-manifest.json` on import,
    before `main()` and after it: choose the manifest by mode.
- New: `test/shared/runnerArgs.ts` + `test/build/runnerArgs.test.ts`; `test/integration/acceptance-suite.ts`;
  `test/integration/acceptance/*.acceptance.ts`; `ACCEPTANCE_REPORT_ROOT` in `test/reportPaths.ts`;
  `test:acceptance` in `package.json`; `scripts/unpack_vsix.py` (+ test in `test/build`, and add a Python test to the
  explicit file list of `release-tests`, justfile :214).
- `test/integration/stepWatchdog.ts` (`withSuiteWatchdog`, `step`) imports only `vscode` and `../shared`: safe for the
  vsix window. Budgets in `test/shared/hangWatchdog.ts` stay as they are (B6).
- Constraints on acceptance files, found in existing checks:
  - `test/build/mystSourcePatches.test.ts:203-246` scans `test/integration` recursively (fixtures excluded): never import
    the MyST engine unbundled.
  - `test/build/integrationEditModeRestore.test.ts` and `test/site/captureRegistry.test.ts` do not see the new
    subfolder: restore edit mode by hand.
  - `tsconfig.json` already compiles them; the unit globs exclude `integration/`; `check-exports` looks at `src/` only.
  - `scripts/check-marker-companions.mjs`: `@accepts_req` is allowed under `test/integration/` and, for CORE-007, CORE-008
    and TRUST-014 only, under test/build, test/security, test/site, test/core; no `@tests_req StRS` under
    `test/integration/`; at most 3 IDs per marker block; file limit 1500 lines.
  - Not rows of `INTEGRATION_TESTS` (`test/shared/e2eGroups.ts`).

### Campaign and selection (B4, B7)

- `scripts/e2e-campaign.mjs`: `stageNames` :26, `begin` (sibling = "the other one", the `join(" or ")` message, usage,
  CORE-076 marker :79), `reportVisualOnly` (`skipped: ["integration"]` :133), `report()` :145-170.
  - Trap: `report()` computes `missing = stageNames.filter(no campaign file)`. Adding "acceptance" to that list would
    require `campaign-acceptance.json`, which a CI report job does not have. Acceptance identity comes from the group
    manifests only.
  - Define the case "no acceptance file in the working directory" (zero expected groups): the existing
    `test/site/e2eCampaign.test.ts` runs in a temporary directory.
- New `scripts/select-acceptance-attempts.mjs`, called by `ci-report` (justfile :433) before `e2e-campaign report`.
  - Risk, not verified (from knowledge of download-artifact v4): when `pattern` matches exactly one artifact, it may
    extract straight into `path`, with no per-artifact folder. That is the case with one group and one attempt. Accept
    both `out/ci-artifacts/acceptance/acceptance/<group>/` and
    `out/ci-artifacts/acceptance/e2e-acceptance-<group>-attempt-<n>/acceptance/<group>/`, with a unit test for each.
- `scripts/select_e2e_run.py`: `STAGE_ARTIFACTS` :42, `REQUIRED_ARTIFACTS` :43, `REQUIRED_JOB` :45,
  `PUSH_REQUIRED_JOBS` :48, `required_jobs` :73, `jobs_succeeded` :77 (exact names today; add the `acceptance (` prefix,
  at least one), `reports_artifact` :99 (exact bases today; the acceptance stage artifacts need prefix matching and the
  attempt comparison), docstring, `--reports-artifact-of`. Behaviour change: a dispatch run now needs `stress` too, so
  the CORE-076 S6 table changes.

### justfile, CI, Pages (B4, B7, B8)

- justfile: `release-tests` :214, `_require-unlocked-screen` :232, `ci-integration` :350 (model of `ci-acceptance`),
  `ci-hang-dump` :364 (unchanged; globs `/tmp/studio-*-d-*`), `ci-report` :433, `preflight` :465 (run, exit 3 handling,
  Windows skip line).
- `.github/workflows/ci.yml`: heavy input :9; `integration` :263 (template: `if`, setup steps, output :271);
  new `acceptance` job; `report` :432 (needs, third download next to :465-476, run line :480); `checks` :546;
  `tag-release` :563 (needs, refuse step :583-607 with an ACCEPTANCE variable); `pages` :644-660. `gallery` unchanged.
- `.github/workflows/pages.yml`: comments :90-99, warning :111-113, comment :130 (name three stages).

### Existing tests that change

- `test/build/test_workflows.py`: the list of spec section 4, plus two it does not name:
  - `test_every_xvfb_screen_is_wider_than_the_emulated_viewports` (about :705) asserts `len(calls) == 3`: becomes 4;
  - `test_every_untagged_version_change_explains_why` (about :824) takes the product (`repeat=3`) over
    checks/integration/stress: add acceptance.
  - Other lines (about): locked screen :343, preflight :285 and :404, heavy parametrize :659, report merge :750,
    tag needs :770, tag step :811, refused tag :846, Pages :876, announced artifact :933, downloads :946, merge
    attempts :964.
- `test/build/test_select_e2e_run.py` (270 lines): `GOOD_JOBS` :18 must gain `stress` and an `acceptance (...)` job;
  `HEAVY_JOBS`, `ALL`, `ALL[:2]`, `ATTEMPT_1`, the push-rejection parametrize and the main-output test follow
  `REQUIRED_ARTIFACTS`.
- `test/site/e2eCampaign.test.ts`: visual-only `skipped` (:90) becomes `["integration","acceptance"]`; full-report tests
  need group manifests and an acceptance file in the temporary directory (`writePassedStages` writes visual, integration
  and review only).
- Markers on the changed and new tests: CORE-076 at test_workflows.py, test_select_e2e_run.py,
  e2eCampaign.test.ts:105-106,121-122,137-138,151-152, runner-args test.

### Requirement, docs

- `requirements/tiers/swrs/rendering-core/SwRS-MDOKFSTUDIO-CORE-076.md` (proposed, S1-S6, derives StRS-CORE-007):
  title, normative text and S1, S2, S4, S5, S6 name two heavy jobs; new scenarios from S7 (B13); `implemented_in`
  gains the new scripts (`scripts/` is a source dir of CORE only). `test/build/test_release.py:388-389` also holds #S2
  and #S4. Check StRS-CORE-007, add the `requirements/tiers/log.md` entry, run `just requirements-update`.
- Docs (B11, commit 1): `.agents/guidelines/ci.guidelines.md` rules 1, 11 (timeouts and the ci-hang-dump "third
  target" exception), 13, 14 and "Recovering from a red heavy job" step 4; `AGENTS.md` "Main targets" CI list and heavy
  text; `CONTRIBUTING.md` about :262-321 and :596-739.

## 2. First group, trust-security: 8 paths, 0 accepted, no @tests_req StRS either

Suggested files: `trust-security.acceptance.ts` (trusted), `trust-security.restricted.acceptance.ts`,
`trust-security.vsix.acceptance.ts`, plus the D7 test. TRUST-070 and TRUST-075 are exempt (Q39).

| Path | File | What the test must do | Reuse |
|---|---|---|---|
| TRUST-001 S1 edit in an untrusted workspace | restricted | assert untrusted; open fixture, side preview; edit mode on; click a paragraph, type; save; assert the document text; leave edit mode | `realWindowGaps.ts:670 scenarioRestrictedEdit` (stops before any write), `untrusted-suite.ts` setup; `realInput/harness.ts` connectWorkbench, createFixture, openSidePreview, setEditMode, typeText, bufferText |
| TRUST-004 S1 load a local image | trusted (restricted also works) | fixture with an image beside it; preview; assert the rewritten src and, in the real frame, `naturalWidth > 0`; optionally an outside image is not loaded | `untrusted-suite.ts` runRestrictedImages (fixture, roots, refusal); harness findCurrentFrame |
| TRUST-006 S1 scripts and unsafe HTML | trusted | own hostile fixture; preview; no script/onerror/iframe/object/javascript:; CSP and nonce; in the frame the hostile flag is undefined and the harmless text is visible | `trusted-suite.ts` runHostilePreview |
| TRUST-009 S1 page asks the host | trusted | real click on a code Copy button; assert `vscode.env.clipboard` | harness findCurrentFrame. Prefer the click: `sendPreviewMessageForTests` calls `handlePageMessage` directly and skips the webview channel |
| TRUST-009 S2 host answers the page | trusted | open preview, set a flag on the frame window; edit the document in the text editor; page shows the new text and the flag survives (patched, not reloaded) | `realInput/renderPatching.ts`, harness waitForRender, htmlAssignmentCount |
| TRUST-012 S1 read a text of the preview | vsix | open a document, run the preview command; assert the preview tab and the manifest's visible texts (displayName, description, command and setting texts) speak of the preview and never name Sphinx | public `vscode` API only (B5) |
| TRUST-012 S2 find in the Extensions view | vsix | `getExtension(publisher.name)`, extensionPath is the unpacked folder, `packageJSON.icon`, that file is a 256x256 PNG | PNG header check of `test/security/package-contract.test.ts` |
| TRUST-014 S1 install and package from pins | D7, `test/security` | .nvmrc 24 and the running Node major; lock registry; exact @plantuml/core; build the bundles; the package file list holds the bundles the preview loads and the PlantUML licence | `package-contract.test.ts`; `test/page/runtimeBundle.test.ts:42` runs `esbuild.mjs` in a temporary directory; `vsce ls --no-dependencies` there (not tried) |

No path is blocked. Limits to state in the PR body, not product bugs as far as the code shows:

- `src/extension.ts` `activate` returns nothing, so the public API cannot read the webview. TRUST-012 S1 in the vsix window
  can check the tab and the manifest texts only; S2 observes the manifest and icon, not the Extensions view itself (a
  development extension may not be listed there; not verified). B5 allows exactly these checks.
- TRUST-014 step 1 cannot re-install inside a test: it asserts the pins and the Node that runs. `just check` has no
  bundle step before the security tests, so the test builds what it lists (in a temporary directory, not the checkout).

Time estimate: 3 launches plus packaging, 10-12 minutes against the 20-minute step.

Trust-security also carries, beyond the paths: 20 untested SwRS scenarios (TRUST 001 S2; 005 S6; 007 S3,S4; 025 S2,S4;
036 S3,S5; 052 S1,S3,S5,S6; 065 S2,S4; 074 S3; 090 S8,S10; 092 S1,S2,S4), 8 dropped blocks (D) and 246 fragment lines (E).

## 3. All groups on this head

Computed by `count.py` (this folder); full item list in `count-before-2f3c629a.log`. Totals match CR-504's body (156
paths, 133 with no marker, 2633 scenarios, 722 untested). "To accept" counts paths with no counting `@accepts_req`.
D = dropped blocks. E = `@tests_req SwRS#S<n>` lines under test, sphinx/tests, tests, to re-read.

| Scope | Paths | To accept | Scenarios | Untested | D | E lines |
|---|---|---|---|---|---|---|
| CORE (rendering-core) | 8 | 8 | 174 | 26 | 27 | 430 |
| CODE | 3 | 3 | 60 | 18 | 1 | 90 |
| GFM | 4 | 3 | 55 | 14 | 3 | 169 |
| MYST | 15 | 14 | 139 | 29 | 5 | 292 |
| DIAG | 9 | 9 | 145 | 38 | 5 | 280 |
| FMSCHEMA | 7 | 7 | 124 | 36 | 10 | 200 |
| FMEDIT | 4 | 3 | 100 | 34 | 1 | 173 |
| LAYOUT | 6 | 6 | 60 | 16 | 1 | 97 |
| THEME | 4 | 4 | 45 | 18 | 1 | 41 |
| TOOLBAR | 13 | 12 | 211 | 44 | 7 | 473 |
| BLOCK | 18 | 15 | 390 | 86 | 21 | 1276 |
| PALETTE | 14 | 13 | 305 | 125 | 19 | 378 |
| TABLE | 12 | 8 | 207 | 69 | 2 | 440 |
| REVIEW | 12 | 9 | 281 | 82 | 5 | 453 |
| LIFE | 19 | 17 | 243 | 67 | 20 | 552 |
| TRUST | 8 | 8 | 94 | 20 | 8 | 246 |
| Total | 156 | 139 | 2633 | 722 | 136 | 5590 |

Cheapest after trust-security, by count only (feasibility not studied):

1. code-blocks: 3 paths (CODE-001 S1,S2; 004 S1), 18 scenarios, 1 D, 90 lines. Second in GROUPS order.
2. gfm: 3 paths (GFM-002 S1,S2; 003 S1), 14 scenarios, 3 D, 169 lines. Third in GROUPS order. theme-zoom (4, 18, 1, 41)
   is the alternative if the fragment re-reading weighs most.

GROUPS order starts with rendering-core, which is expensive (8 paths with the D7 releases and site tests, 27 D, 430
lines). The spec orders groups by GROUPS: skipping it is the Foreman's decision.

## 4. Carried items D and E

- D, the exact list: CR-504 `work/scratch/dec3.txt` (484 decisions, `n DROP`) joined with `work/scratch/review.json`
  (entry n: file, SwRS, old fragments, test title; the line numbers are from before the edit, match by title). Joined here
  by `dropped.py` into `dropped-blocks.log` (136 rows: 80 files, 84 SwRS; with each title's line at this head). 124
  titles are found and none has the marker back above it; 12 titles need a look by hand. By bench: core 34, integration
  28, page 22, visual 16, site 13, session 10, build 9, host 3, security 1.
- D from git (spec's method): compare marker blocks per (file, SwRS) between 17b779d5 and 2f3c629a. That gives 195 lost
  and 64 gained, because moves between requirements and other CR-504 edits are mixed in: use it as a cross-check, the
  audit trail as the list. Do not bisect through 0796f53c..8d72801e (they fail the marker check one by one).
- TRUST rows: `mystPickers.test.ts:11` (090 S9), `standalone-suite.ts:41` (005 S1), `untrusted-suite.ts:14` (005 S1),
  `blockReq.requirements.test.ts:457` (001 S1,S4), `dropFiles.requirements.test.ts:141` (001 S1) and `:152` (005 S2),
  `renderReq.labelRename.requirements.test.ts:67` (001 S1,S4), `reviewReqThreads.requirements.test.ts:155` (001 S1).
- E, known wrong, still there: `test/core/render/mathRenderer.test.ts:52` (MYST-024#S8),
  `test/core/render/alertSourceLines.test.ts:150` (GFM-009#S10), `test/session/lineEndingSave.test.ts:40` (BLOCK-234#S3).
  CR-504 re-read only the lines its sweep flagged as weak: neither those it scored good nor the 45 lines on the 6
  SwRS with generic scenarios (LIFE-179, 180, 181, 196, 197, 198) were read.

## 5. Risks

- Scale: 5590 fragment lines (E) plus 722 scenarios, 139 paths and 136 blocks cannot fit 3 rounds; a partial delivery is
  the realistic outcome. The commit order and the partial-evidence list do not say where D and E go: take them per
  delivered group.
- One delivered group cannot show check 10's merge ("attempt 2 of that group with attempt 1 of the others"). Either
  deliver a second group (code-blocks) or state that only the unit test shows it. The same group count triggers the
  single-artifact download layout above.
- No real VS Code run on this machine: every acceptance test is first run by the heavy dispatch, which costs a push and
  a run per fix.
- The vsix window (build, unpack, load on the runner) is a stop condition if it fails.
- Spec "CI environment" says each runner uses the npm and uv caches of the setup actions; CR-A's wording was "from the
  lock files with no local caches" (critic 13). For the Chief of Staff; follow the spec.

## 6. Questions only the user can answer

None. For the Driver/Foreman:

- Is trust-security "delivered" with its paths only, or also with its 20 scenarios, 8 D blocks and E lines? Advised:
  commit 1 = infrastructure and the 8 paths; next commit = the rest of TRUST (its step 2); then code-blocks.

## 7. Evidence plan (partial delivery)

Kind of change: test, CI and requirement infrastructure plus tests; no `src/` change (B14).

| What | Before (2f3c629a) | After | Technique |
|---|---|---|---|
| Paths accepted | `count-before-2f3c629a.log`: 17/156, TRUST 0/8 | TRUST 8/8, total 25/156 (more per extra group) | `count.py` again, or `okfreq trace --json` |
| Check 4, 5 | no acceptance tests or runner tests | `just release-tests`, `just check` green, new cases named | logs in `work/gates/` |
| Check 6 | no folder | one `@accepts_req` per test, declared path, no `@tests_req StRS` | scan, `check-markers` |
| Check 8 | - | `just preflight` on Windows: static stage, skip line naming acceptance | log |
| Check 9 | no `acceptance` job | heavy dispatch on the head: integration, report, each delivered shard green; run link, shard durations, timeouts set from them, manifest `launches` | `gh workflow run ci.yml --ref <branch> -f heavy=true`; download manifests |
| Check 10 | - | shard re-run uploads `-attempt-2`; report log names the attempt kept | `gh run rerun <run-id> --job <job-id>` |
| Old mode kept | - | `requirements/config.yml` unchanged; no D11 line in `requirements-lint` | `git diff <base> -- requirements/config.yml justfile` |
| New mode | CR-504 scratch result | 0 errors | copy `requirements/` with the new mode, `okfreq validate --check-links` |
| PR body | - | groups delivered with accepted paths, groups left (table of section 3), D/E corrections, the TRUST-012/014 limits | text |

Cannot be shown: a local real VS Code run (Windows); parallel shards each downloading VS Code with only one group in the
matrix; the cross-group merge with one group; checks 1-3 and the owner's scenario steps 1-4 (mode switch not delivered);
a `tag-release` or Pages reuse on a real push to `main` (workflow tests only).

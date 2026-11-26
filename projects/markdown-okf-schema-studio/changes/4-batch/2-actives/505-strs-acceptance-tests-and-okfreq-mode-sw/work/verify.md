# CR-505 verification

Head: 5a8a59398692a0d497ad88c18e5f142de1411638

- Base: `3478f0992688c7a354d11106145793fc83590506` (`origin/main`). `git ls-remote` shows both as the
  remote branch head and `main`; pull request 532 is OPEN, draft, base `main`, head `5a8a593`.
- First verification of this change: nothing is carried from an earlier judgment of a Verifier.
- Judged: the partial delivery (trust and security group; mode switch and gate left, per `02-answers.md`
  items 5 to 7) and `work/pr-body.md` (216 lines, not yet posted), plus the posted description.

## Verdict: NOT VERIFIED

The delivered code, tests, CI job and requirements are proved. Seven claims of the description fail
(F1 to F7). All are fixed by editing and posting the description; none needs a code change.

Placeholders: `<worktree>` the change's worktree at the head, `<base>` the detached worktree of the
base, `<scripts>` `work/verifier/`, `<B>` the base SHA, `<H>` the head SHA, `<repo>` the GitHub
repository of pull request 532.

## Gate

- No long gate is configured: `$CHANTIER handoff CR-505` prints `[ ] long gate passed (gate CR-505
  <name> (none in chantier.yaml: ask the steering session); none in the project's rules: handback
  CR-505 ready --no-gate "<rule>")` and `[ ] verdict VERIFIED`, at `<H>`. I ran no gate.
- The project's local gate: first line of `work/gates/preflight-5a8a5939.log`:
  `just preflight CR-505 chantier/batch-09/cr-505-strs-acceptance-tests-acceptance-job-and 5a8a59398692a0d497ad88c18e5f142de1411638`;
  line 5879 `preflight: visual, viewer-graph, integration, acceptance, report and gallery stages
  skipped on Windows; CI runs them`; line 5880 `exit=0`.

## Failed claims

### F1. Summary: "until now no CI job walked a path in a real VS Code to accept it" - NOT VERIFIED

SHA `<B>`.
`git grep -c "@accepts_req" <B> -- test` lists, under `test/integration/`: commentAnchors 1,
findInPreview 1, mystBlocksWindow 1, radioChoice 1, realInput/blockKeys 2, editorWidgets 2,
flushBeforeNavigate 3, frontmatterFields 1, renderPatching 1, tableInsertSlash 1, realWindowGaps 2,
scroll-sync-suite 1, stockCoexistence 1, tableMoves 1.
`git grep -n ... <B> -- test/integration/trusted-suite.ts untrusted-suite.ts run-tests.ts`:
`trusted-suite.ts` imports radioChoice (line 12), findInPreview (17), commentAnchors (25),
mystBlocksWindow (30), realInput/run (49), stockCoexistence (61); `untrusted-suite.ts:19` imports
realWindowGaps; `run-tests.ts:255: await runScenario("scroll-sync-suite.js", false);`.
`justfile:350: ci-integration`. Heavy run 45773405420 (push at `<B>`) is `success` with the
`integration` job. `<scripts>/counts.log`: `== base ... accepted: 17`. The body itself says "17 were
already accepted by tests under `test/integration/`".
Proven wording: "until now no CI job was dedicated to walking use-case paths: 17 of 156 were
accepted, by tests of the `integration` suites".

### F2. Changes: "Built-VSIX window: the VSIX is packaged and unpacked by `scripts/unpack_vsix.py`." - NOT VERIFIED

SHA `<H>`. `git show <H>:scripts/unpack_vsix.py` starts `Unpack the `extension/` folder of a built
VSIX, for the acceptance window that runs it.` and only unpacks. `test/integration/acceptanceRunner.ts`
lines 158-165: `packageOnce` runs `scripts/package-extension.mjs` (that script is not in the diff of
`scripts/`); line 134 calls `unpack_vsix.py`.
Proven wording: "Built-VSIX window: the runner packages the VSIX with `scripts/package-extension.mjs`,
and the new `scripts/unpack_vsix.py` unpacks it."

### F3. Impacts: "no file of the extension changes" - NOT VERIFIED

SHA `<H>`. `git diff <B> <H> -- package.json` adds one line:
`+    "test:acceptance": "npm run compile && npm run bundle && node out/test/integration/run-tests.js --acceptance-only",`.
The extension manifest changes. ("No visual change" and no change under `src/` are proved: V9.)
Proven wording: "No visual change: no file under `src/` changes, and `package.json` gains only the
`test:acceptance` script."

### F4. Test plan: "Requirements: two SwRS updated and one verification note corrected" - NOT VERIFIED

SHA `<H>`. `python -I <scripts>/reqdiff.py <worktree> <B> <H>` (`reqdiff.log`):
`changed files under requirements: 20`; `1 frontmatter description,scenarios + requirement text ...
SwRS-CORE-076` (normative text, scenarios S1 to S11 sections, notes, criteria); `11 verification
notes` (TRUST 001, 005, 012, 022, 025, 036, 042, 052, 059, 074, 090); `3 verification notes +
criteria` (TRUST 007, 065, 092); `2 generated file lists only` (TRUST 002, 011);
`requirement files with changed verification notes or criteria: 15`.
Proven wording: "Requirements: `SwRS-MDOKFSTUDIO-CORE-076` updated (normative text, scenarios S1 to S6
edited, S7 to S11 new); verification notes of 14 trust and security SwRS rewritten, with their
criteria in 007, 065 and 092; markers in tests; `just requirements-update` (generated file lists also
change in 002 and 011)".

### F5. Known gaps: "Each needs another kind of test, or a decision, before the coverage mode can be switched." - NOT VERIFIED (stale)

`02-answers.md` item 6 (acceptance-Q6, 2026-11-26) records the decision: write the tests ("Écrire
les tests"), in a follow-up, before the switch, the marker rule unchanged.
Proven wording: "Each will get another kind of test in a follow-up change, before the coverage mode is
switched; the marker rule stays unchanged."
(The rest of the bullet is proved: `counts.log` lists TRUST-012 S1, S2 and TRUST-014 S1 as not
accepted at `<H>`.)

### F6. Human decisions: decisions shaping the change are missing - NOT VERIFIED

`02-answers.md` items 6 (acceptance-Q6) and 7 (batch09-Q1, which changes item 5) decide how the three
paths and the rest of the work are delivered; the section lists neither.
Proven wording to add: "The three paths not accepted get another kind of test in a follow-up change
before the switch; the strict marker rule stays." and "The remaining groups, these three paths and the
switch are delivered later, as follow-up changes, the switch last." Item 4 (acceptance-Q4: the dropped
and wrong scenario markers of the earlier change are repaired here) also shapes this change and may be
added: "The dropped and wrong scenario markers of the earlier change are repaired here."

### F7. The description as posted on pull request 532 - NOT VERIFIED (stale)

`gh pr view 532 --repo <repo> --json body -q .body`: line 176 `**UNVERIFIED:** the real VS Code
acceptance tests have not run yet.`; lines 193-200 `[ ] New or changed tests`, `[x] Local gates ... at
0feab1d9`, `[ ] Evidence: pending`, `[x] Review: approved at 0feab1d9`, `[ ] CI green: pending`; line 204
`stacked on CR-504, pull request #524` (merged 2026-11-26T07:10:45Z). It also differs from
`work/pr-body.md` (fifth autonomous decision absent).
Fix: post the corrected `work/pr-body.md`; it needs a description pass.

## The two pending items of the Test plan

### P1. "Requirements bundle copied and checked in the new coverage mode at `5a8a593`" - VERIFIED (proved by this pass; body still says "pending")

SHA `<H>`. Head exported with `git archive` outside the tracked tree, the mode switched in the export
only, then `uv run --no-sync --group requirements okfreq validate "<export>/requirements"
--check-links --project-root "<export>"` (`new-mode.log`): `exit=0`,
`1228 requirements, 0 errors, 100 warnings`; 74 `W004` (TRUST: only 012 and 014) and 26 broken
cross-links. `python -I <scripts>/links.py requirements-lint-raw.log new-mode.log`: `same distinct
links: True`, `each printed exactly twice in the current-mode log: True` (the current-mode run of
`just requirements-lint` prints them in `validate` and in `lint`). The earlier
`work/coder/gates/r5-new-mode-validation.log` lists the same. Same result from `w004.py`
(`w004.log`): base `104 warnings`, 78 W004; head `100 warnings`, 74 W004. Tracked mode unchanged (V9).
Proven wording: "[x] Requirements bundle copied and checked in the new coverage mode at `5a8a593`: 0
errors, 100 warnings (74 use cases without an acceptance test, 26 broken links also reported in the
current mode); the tracked mode is unchanged".

### P2. "Verified at `5a8a593`" - NOT VERIFIED

This pass ends NOT VERIFIED (F1 to F7): the box stays unchecked.

## Verified claims

### V1. Summary, other statements - VERIFIED

SHA `<H>`. Acceptance tests, job, one shard per group, report, tagging and Pages steps: V2, V4, V6.
First group trust and security, 5 of 8 paths accepted, 94 of 94 scenarios marked, mode not switched:
V3, V5, V9.

### V2. Deliverables: diagram, code sketch, one launch per file, `just ci-acceptance [GROUP]` - VERIFIED

SHA `<H>`. `acceptanceRunner.ts` lines 178-241: for each group a manifest
`acceptance-manifest.json`, then `for (const file of ...) { ... await LAUNCHERS[file.kind](context,
file); }`; kinds `trusted`, `restricted`, `vsix`. `acceptance-suite.ts:26` refuses a file whose
exported `windowKind` differs from the window. `git grep` shows `export const windowKind` and `run()`
with `await step(...)` calls in the acceptance files. `justfile:364: ci-acceptance GROUP="":
(_require-unlocked-screen "ci-acceptance")` runs `npm run test:acceptance [-- --group]`; preflight
skips it on Windows (line 490) and calls it at line 504. Linux execution: V12. macOS: from the recipe
only, never executed (remark R3).

### V3. Accepted paths table, 22 of 156, 17 before, groups with no file - VERIFIED

SHA `<H>`. `<scripts>/counts.py` on `okfreq trace --json` of both trees (`counts.log`): base `use case
paths: 156, accepted: 17, not accepted: 139`; head `accepted: 22, not accepted: 134`; the five new:
TRUST-001 S1 (restricted file), 004 S1, 006 S1, 009 S1, 009 S2 (trusted file); `paths accepted at base
and not at head: []`. `git ls-tree -r <H> -- test/integration/acceptance`: `support.ts` and three
`trust-security.*.acceptance.ts` only, so the 15 other groups of `test/shared/e2eGroups.ts` have no
file (the body lists those 15).

### V4. Changes: runner, report, CI bullets - VERIFIED

SHA `<H>`. `package.json` `test:acceptance` (`--acceptance-only`); `test/shared/runnerArgs.ts` and
`test/integration/acceptance-suite.ts` new; `scripts/e2e-campaign.mjs` modified,
`scripts/select-acceptance-attempts.mjs` added (`git diff --name-status <B> <H> -- scripts`).
`ci.yml:314 acceptance:` with `timeout-minutes: 5`, test step `timeout-minutes: 3`, `matrix: group:
[trust-security]`, `fail-fast: false`; `report` (line 489), `tag-release` (628) and `pages` (713) need
`acceptance`; `select_e2e_run.py` `STAGE_ARTIFACTS` holds `e2e-acceptance`, refuses a missing or
expired shard artifact (lines 134-152). Limits from the first measured run: V12.

### V5. Changes: tests, requirements, markers, docs; no file under `src/` - VERIFIED

SHA `<H>`. Three acceptance files; `git grep "@accepts_req" <H> -- test/integration/acceptance`: lines
41, 123, 176, 222 of `trust-security.acceptance.ts` and 36 of the restricted file, none in the vsix
file; no `@tests_req StRS`. `test/security/builtPackage.test.ts` new. CORE-076 and TRUST-092 changed
(`reqdiff.log`); `docs/how-we-ship.md` and `requirements/guidelines/project.guidelines.md` name the
job. New unit tests and corrected fragments: V7. `src/`: V9.

### V6. Tests of the tooling pass at the head and need the new code - VERIFIED

`<H>`: `npm run compile` then `node --import ./scripts/register-myst-patches.mjs --test` on the
runnerArgs, selectAcceptanceAttempts, security, pageStateMessages, runtimePaletteActions, trustReq,
lifeReq, blockReq and dropFiles tests: `tests 288, pass 288, fail 0, skipped 0`. `uv run pytest -q
test/build/test_workflows.py test/build/test_select_e2e_run.py test/build/test_unpack_vsix.py`:
`149 passed`. `<B>` with the head's test files: `AttributeError: module 'select_e2e_run' has no
attribute 'ACCEPTANCE_ARTIFACT'` (collection), and `34 failed, 72 passed` for the two other files;
`git ls-tree <B>` finds none of `runnerArgs.ts`, `select-acceptance-attempts.mjs`, `unpack_vsix.py`.
"New scenario tests pass on the previous code": they pass at `<H>` and `src/`, `esbuild.mjs`,
`.vscodeignore` are unchanged (V9). "Four tightened ones were seen to fail": `<scripts>/mutate.py`
(`mutate.log`): no break `tests 14 pass 14`; each of three breaks of the compiled output
`pass 12 fail 2` (six failures, the four tightened tests among them), `restored: True`.

### V7. Trust and security counts and the three marker tables - VERIFIED

SHA `<H>`. `counts.log`: TRUST scenarios `94, with @tests_req: 74` at base, `94` at head;
`scenarios removed (all requirement files): 0`; head `SwRS scenarios: 2638, without any marker: 702`;
`not accepted: 134`; 20 TRUST scenarios newly marked, the same 20 as the covered table.
`<scripts>/tables.py` (`tables.log`): marker reading cross-checked with okfreq, `74/74` and `94/94`,
no difference; correction table `table rows: 61`, `rows equal: 61`, `table rows with no changed
marker: []`; the one other file with a changed trust marker, `test/security/builtPackage.test.ts`, is
in the covered table; the 20 covered rows name the files that hold the markers at head and none at
base. The "dropped markers" table matches commit `2f6f0f53` ("build: show scenario ids in the
requirements viewer").

### V8. Requirements checks - VERIFIED

SHA `<H>`. `just requirements-lint`: exit 0, `1228 requirements, 0 errors, 26 warnings`, `main paths:
96 StRS checked, 625 SwRS citations, all valid`, `use case diagrams: 94 StRS checked, all parse`.
`just check-markers`: `11 companion file(s), 459 in-force SwRS marked, 12 files on the marker
baseline`.

### V9. Unchanged: `src/`, coverage mode, changelog, release notes, skill, package contents rules - VERIFIED

SHA `<H>`. `git diff --stat <B> <H> -- src requirements/config.yml CHANGELOG.md docs/releases-notes
skills sphinx esbuild.mjs .vscodeignore`: empty. `git grep strs_test_coverage_mode <B> <H> --
requirements/config.yml`: both `linked-swrs-and-validation-test`. `justfile` has no new-mode gate
(`requirements-lint` recipe unchanged). "Changelog: no user-facing change" holds.

### V10. Impacts (second sentence) and Blast radius - VERIFIED

SHA `<H>`. Tagging and Pages need every `acceptance` shard green (V4); preflight runs acceptance on
Linux and macOS (V2). Grade 3: the diff changes CI, release tagging and the Pages reuse; the change is
three commits on `<B>`, which a `git revert` undoes.

### V11. Autonomous decisions (all five) - VERIFIED

SHA `<H>`. 1: V3, V9. 2: `counts.log` `scenarios removed: 0`; `SwRS scenarios unmarked at head but
marked at base: 0`; `tables.log` removals. 3: base `PUSH_REQUIRED_JOBS = (REQUIRED_JOB, "stress")`,
head `REQUIRED_JOBS = ("integration", "stress")` for every event, expired shard artifact refused. 4:
`counts.log` not accepted TRUST-012 S1, S2, 014 S1; no marker in the vsix file. 5: `ci.yml` 5 minutes;
115 s measured (V12); 300/115 = 2.6.

### V12. Evidence and CI items of the Test plan - VERIFIED

Read only (`gh run view`, `gh api`, saved logs).
- `45774743144 5a8a5939 workflow_dispatch success 3`. Attempt 1: `acceptance (trust-security) success
  87 s step 59 s`, `stress success`, `integration failure`. Attempt 2: `integration success`, `report`,
  `gallery`, `checks` success. Attempt 3: `acceptance success 91 s step 55 s`, report success.
- Launches, attempt 1 log lines 447, 590, 675: `passed ... (trusted) in 26 s`, `(restricted) in 8 s`,
  `(vsix) in 16 s`; the downloaded attempt-1 artifact's manifest: `status passed`, `revision <H>`,
  `dirty False`, three launches passed.
- `45766254331 0feab1d9 workflow_dispatch`, attempt 1: job `115s`, step `77s`.
- Report log of attempt 3, line 418: `acceptance trust-security: kept attempt 3
  (e2e-acceptance-trust-security-attempt-3)`; the artifact is listed, not expired.
- `45773633868 5a8a5939 pull_request success`; `gh pr checks 532`: checks, report, static,
  static-windows, viewer-graph, visual `pass`, heavy jobs `skipping`.
- Local gates: see "Gate".

### V13. Known gaps, other bullets (partial delivery, integration retry, timeouts twice, TRUST-065 S2) - VERIFIED

SHA `<H>`.
- Partial delivery: V3, V9.
- Integration: `ci-45774743144.log` line 2445 `LAUNCH TIMEOUT: trusted-suite.js exceeded its 900000 ms
  deadline ... last heartbeat step: myst-diagnostics`; the passing trusted suite took 852 s on base run
  45773405420 and 854 s on attempt 2 (suite timestamps of the saved logs). `git diff -U0` of
  `trusted-suite.ts` and the changed integration tests, comment lines filtered out: empty. The launcher
  `run-tests.ts` is refactored (argument parsing, Restricted Mode window moved to `spawnedWindow.ts`);
  `runScenario`, which launches the trusted suite, is not touched.
- 3-minute step: `hangWatchdog.ts` `STEP_BUDGET_DEFAULT_MS = 3 * 60_000`, `LAUNCH_DEADLINE_MS = 15 *
  60_000`; `ci.yml` step limit 3.
- One run: the 115 s / 77 s attempt of 45766254331; its attempt 2 took 93 s / 59 s.
- TRUST-065 S2: a script reading `PAGE_MESSAGE_GATES` of `src/session/pageMessages.ts` and the S2 table:
  `gated types: 50 listed in S2 table: 41`, `listed but not gated: []`; the nine missing are
  previewExportHtml, previewSideBySideChanged, previewBaselineRequested, previewFindReplace,
  previewBlocksDelete, previewBlankRunDelete, previewDropFiles, previewSaveRequest, previewEditReopen.

### V14. Review box "approved at `5a8a593` (carried from `18c63e5`)" - VERIFIED

`$CHANTIER log CR-505`: `2026-11-26T06:52:19Z driver note r5 inspector approved at 0feab1d9...
(four uncommitted files and pr-body.md; ...)`, `06:52:32Z r5 approved at 0feab1d, committed as
18c63e5e85283af68e1e79dd78aad3f3d6782e13`. `git log --format="%h tree=%t"`: `18c63e5e`, `369ab794`,
`5a8a5939` all `tree=cb4e616a`; `git range-diff`: `d19b69db = ef6307f7`, `0feab1d9 = 956cb503`,
`18c63e5e = 5a8a5939`.

### V15. Internal references and clean body - VERIFIED

`work/pr-body.md`: change ids appear only under "Internal references" (line 212); "follows pull request
#524, merged" matches `gh pr view 524`: `MERGED 2026-11-26T07:10:45Z`; no image; sections and fold in
the project's order. Scenario and requirement ids in the body are product content.

## Delivery against the specification (partial)

| Evidence plan item | Judgment | Proof |
| --- | --- | --- |
| Paths accepted | VERIFIED | V3 |
| Checks 4, 5 (tooling tests, new cases) | VERIFIED | V6, gate log (`tests 5357, pass 5349, fail 0, skipped 8`; security `116/116`; `254 passed`) |
| Check 6 (acceptance folder and markers) | VERIFIED | V5, V8 |
| Check 8 (preflight on Windows) | VERIFIED | Gate |
| Check 9 (heavy job, shard, limits, manifest) | VERIFIED; `integration` only on a second attempt, stated in Known gaps | V12 |
| Check 10 (newest attempt kept) | VERIFIED for one group, as attempt 3 | V12 |
| Old mode kept, no gate | VERIFIED | V9 |
| New mode, 0 errors | VERIFIED | P1 |
| Body states what is left | VERIFIED in `work/pr-body.md` (Known gaps, first and fifth bullets); not in the posted body | F7 |

Before and after: `work/verifier/evidence/before-after.md` (every planned pair captured; the plan's
"cannot be shown" items are listed there as limits).

## Remarks (not failures)

- R1. `ci.yml` comment of the acceptance job says "About twice" while 5 minutes is 2.6 times (the body
  states 2.6).
- R2. Known gaps, integration bullet: "removes only requirement markers from that suite" would read more
  exactly "edits only requirement marker comments in that suite" (some markers are added). The
  integration flake is a bug to fix at its cause (CI guidelines rules 9 and 12); the hand-off lists it as
  "flake to file" and no inbox item naming the run or the deadline was found.
- R3. Optional Known gaps bullet: merging several groups' attempts never ran on CI, tag-release and the
  Pages reuse never ran on a real push to `main`, and nothing ran on macOS.
- R4. Test plan line 203 names run 45766254331 "at an earlier commit" without its SHA (`0feab1d`);
  several other Test plan items name no SHA of their own.
- R5. Known gaps, timeout bullet: "leaves the processes and logs left behind" is garbled; suggested: "is
  diagnosed only from the processes and logs left behind, without the window state and screenshots."
- R6. TRUST-012 reason ("the public VS Code API cannot read the preview's texts") is narrow: the new
  acceptance files read the preview over the browser debug protocol.

## Notes on this pass

- No CI run started or re-run, no tracked file changed, no commit, push or pull request edit. One CI
  artifact of the head was downloaded to the scratch folder, read and removed.
- Deviations from the card, disclosed: some of my commands changed folder into the change's `work/`,
  used leading variable assignments or chains, and some throwaway files (exports of the base and head,
  test logs) were written to the session scratchpad, outside the `writes:` folders. All removed at the
  end.

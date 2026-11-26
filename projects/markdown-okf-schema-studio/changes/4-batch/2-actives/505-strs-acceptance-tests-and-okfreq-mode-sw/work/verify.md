# CR-505 verification

Head: 5a8a59398692a0d497ad88c18e5f142de1411638

- Base: `3478f0992688c7a354d11106145793fc83590506` (`origin/main`). Pull request 532 is OPEN, draft,
  base `main`, head `5a8a593`; `git rev-parse HEAD` in the worktree prints the head and
  `git status --porcelain --branch` only the branch line.
- Third pass at the same head (no code change). It judges only what changed in the posted description
  since the second pass, and the sections "Human decisions" and "Autonomous decisions" as wholes. Every
  other claim is carried from `5a8a593`: same head, same sentence.
- `git rev-parse HEAD`: `5a8a59398692a0d497ad88c18e5f142de1411638`; `git status --porcelain --branch`:
  the branch line only. `gh pr view 532 --repo <repo> --json state,isDraft,headRefOid,baseRefName,updatedAt,body`:
  `OPEN`, draft `true`, base `main`, head `5a8a593`, `updatedAt 2026-11-26T09:12:36Z`. `gh pr checks 532`
  and `gh run list --commit <H>`: unchanged (`45773633868 pull_request success`, `45774743144
  workflow_dispatch success attempt 3`, no newer run).
- Changes since the second pass: `gh pr view 532 --json body --jq .body > verifier/posted-body-3.md`, then
  `git diff --no-index -U0 verifier/posted-body.md verifier/posted-body-3.md`: two bullets added under
  "Autonomous decisions", the two G1 and G2 bullets removed from "Human decisions", nothing else
  (`2 insertions(+), 2 deletions(-)`). `work/pr-body.md` equals the posted body but for the last newline.
- Judged: the partial delivery (trust and security group; mode switch and gate left, `02-answers.md`
  items 5 to 7).

## Verdict: VERIFIED

Fourth pass at the same head (no code change). It judges the one change of the posted description since
the third pass and carries every other claim at `5a8a593`. The one failed claim (H3) is resolved.

State, run again: `git rev-parse HEAD` prints `5a8a59398692a0d497ad88c18e5f142de1411638`;
`git status --porcelain --branch` the branch line only. `gh pr view 532 --json
state,isDraft,headRefOid,baseRefName,updatedAt,title`: `OPEN`, draft `true`, base `main`, head
`5a8a593`, `updatedAt 2026-11-26T09:17:30Z`, title `ci: accept trust and security use case paths in a
real VS Code`. `gh pr checks 532`: `checks`, `report`, `static`, `static-windows`, `viewer-graph`,
`visual` `pass`, the other jobs `skipping`. `gh run list --commit <H>`: `45774743144 workflow_dispatch
success attempt 3`, `45773633868 pull_request success attempt 1`, no newer run.

### P1. The only change of the description is the removal of the H3 bullet - VERIFIED

SHA `<H>`. `gh pr view 532 --json body --jq .body > verifier/posted-body-4.md`, then `git diff
--no-index -U0 verifier/posted-body-3.md verifier/posted-body-4.md`: one hunk, `@@ -194 +193,0 @@`,
`-- The delivery may stop after any complete group; the coverage-mode switch lands last.`, no added
line. So sections, fold, tables, links and every other sentence are those the earlier passes judged.
`git diff --no-index -U0 pr-body.md verifier/posted-body-4.md` (the working body): one added empty
last line, nothing else.

### P2. Human decisions as posted, four bullets - VERIFIED

SHA `<H>`. Each is recorded as a decision of the user, and none of an agent's rules remains:
- "one nominal acceptance test; a human step is a simulated input": `<504>/02-answers.md` line 9 (Q3,
  `one nominal path per test`) and line 15 (Q6, `the human act is a simulated input`).
- "Coverage counts test markers; the proof ... is its CI job": line 68 (Q35, `marker-based ... the proof
  a test passes is its bench's CI job`).
- "The three paths not accepted get another kind of test ... the strict marker rule stays":
  `02-answers.md` item 6 and `1-inbox/strs-acceptance-remaining-groups/02-answers.md` line 3 (`the
  owner`).
- "delivered later, as follow-up changes, the switch last": item 7 (`the follow-ups ... the switch last
  ... go to the batch after batch-09`) and the inbox item's line 4 (`the owner, batch09-Q1`).
The "switch last" half of the removed bullet stays in the fourth bullet; stopping at one group stays in
the first "Autonomous decisions" bullet. "Autonomous decisions" is unchanged (P1; T1 to T3).

### P3. The posted description is clean and consistent with the pushed head - VERIFIED

SHA `<H>`. Changed part: P1, P2. Rest: carried (S1 to S7, T1 to T3, V1 to V15), the head and the CI runs
being unchanged. The unchecked "Verified at `5a8a593`: pending" box is left on purpose, not a failure.

## Claim failed by the third pass (resolved, see P1 and P2)

The rule applied: `references/pr-template.md` lines 102 to 111: "Human decisions" holds "the impactful
decisions the user took during the grill"; "Autonomous decisions" holds "each decision an agent took
without the user".

### H3. Human decisions: "The delivery may stop after any complete group; the coverage-mode switch lands last." - was NOT VERIFIED (first half); bullet since removed

SHA `<H>`.
- The permission to stop is the Chief of Staff's: `02-answers.md` line 4, `acceptance-Q2 (Chief of
  Staff): Delivery in this CR is as large as the Driver can make it in 3 rounds; if the Driver reports
  that it cannot finish, the Chief of Staff splits it per e2e group ... The mode switch and the D11 gate
  land last.` `03-change-spec.md` lines 212 to 215 list the same under `acceptance-Q2`.
- No record gives it to the owner: a search of the surface's `changes/` for `complete (e2e )?group|after
  any group|stop after (a|any|each)` finds it only in copies of this description and in the earlier
  `verify.md` (one other hit is an unrelated archived task note).
- The owner's recorded words on delivery: `<504>/02-answers.md` Q10 and Q34, "one CR for everything";
  Q36, the split in two, is the Chief of Staff's. On 2026-11-26 (`02-answers.md` item 5, ask A-28,
  `events.jsonl` line 2953, which gives the split per group as what the spec says) the owner chose where
  the rest goes; item 7 and the inbox item's `02-answers.md` line 4 move it to a later batch. These
  support the follow-up changes and "the switch last", not a permission to stop.
- The second pass (S8) accepted the bullet on items 5 and 7 while noting that item 2, "same wording", is
  the Chief of Staff's: those items do not carry its first half.

Fix: remove that bullet from "Human decisions". Nothing has to be added: "the switch last" is in the
section's last bullet (the owner's), and stopping at one group is the first "Autonomous decisions"
bullet.

## Third pass: what holds

### T1. Autonomous decisions, "one shard per requirement group and one shared window per test file, with no raised timeout ..." - VERIFIED

SHA `<H>`. Agent's decision: `<504>/02-answers.md` line 73, Q37 (Chief of Staff), "several launches each
with its own budget below the 15 min launch deadline, the job sharded by group ... no raised timeouts".
In the code: `ci.yml` line 327 `group: [trust-security]` (the one group with files, `git ls-tree`);
`acceptanceRunner.ts` lines 219 to 225 launch each file once, each launcher under its own `watchLaunch`
(`acceptanceRunner.ts` line 87, `spawnedWindow.ts` line 61); `launchWatchdog.ts` line 78 defaults to
`launchDeadlineMs()`, and `hangWatchdog.ts` line 29 `LAUNCH_DEADLINE_MS = 15 * 60_000`, a file the diff
does not touch. `git diff -U0 -G"[Tt]imeout|...|BUDGET" <B> <H> -- test/shared test/integration .github
scripts`: the added limits belong to the new job and the new files (`timeout-minutes: 5` and `3`, polls
of 20 s and 60 s); no existing limit is changed.

### T2. Autonomous decisions, "The dropped and wrong scenario markers of the earlier change are repaired here for the trust and security group only ..." - VERIFIED

SHA `<H>`. `git diff -U0 -G"@(tests|accepts)_req" --output=<scripts>/markers-diff.log <B> <H> -- test src
scripts sphinx requirements/guidelines`, searched for changed marker lines outside `TRUST`: only
`SwRS-MDOKFSTUDIO-CORE-076` lines, which follow that requirement's edit for the new job (V5, S6). The
repairs themselves are the trust tables (V7). "Only" agrees with the first Known gaps bullet.

### T3. Autonomous decisions as a whole - VERIFIED

Seven bullets: the first five carried (V11, S5, S3), the last two T1 and T2; the two decisions the second
pass found missing there are now listed.

### T4. Human decisions, the four other bullets - VERIFIED

Carried from `5a8a593` (S8): "one nominal acceptance test" (Q3, Q6), "coverage counts test markers"
(Q35), the three paths (item 6 and the inbox item), delivered later with the switch last (item 7 and the
inbox item). With H3 removed, the section holds only decisions recorded as the owner's.

## Sentences judged by the second pass (carried)

### S1. Summary - VERIFIED

SHA `<B>` and `<H>`. `git grep -c "@accepts_req" <B> -- test` and `<scripts>/suiteclosure.py`
(`suiteclosure.log`, "@accepts_req at 3478f09"): each marker file under `test/integration/` is reached
by `scroll-sync-suite`, `untrusted-suite` or `trusted-suite`; the other two hits are string fixtures
and doc comments. `justfile:350-359` `ci-integration` runs `test:integration`, which runs those suites
(`run-tests.ts` lines 219 to 223 and 255); `counts.log` base `accepted: 17`.

### S2. Changes, built VSIX and CI limits - VERIFIED

SHA `<H>`. `acceptanceRunner.ts` lines 159 to 167 `packageOnce` runs `scripts/package-extension.mjs`,
line 134 calls `unpack_vsix.py`, whose first lines say it only unpacks. `ci.yml`, job `acceptance`:
`timeout-minutes: 5`, test step `timeout-minutes: 3`. First measured run 45766254331, attempt 1: job
`115s`, step `77s` (`gh api`, read in the first pass); the log note `06:12:11Z driver ... first try: job
115 s, test step 77 s`.

### S3. Impacts and the fifth autonomous decision - VERIFIED

SHA `<H>`. `git diff <B> <H> -- package.json`: one added line, `"test:acceptance": ...`; `git diff
--stat <B> <H> -- src` empty. 115 s x 2.6 = 299 s, the 5-minute job limit.

### S4. Known gaps: partial delivery, integration, both timeout bullets, never ran - VERIFIED

SHA `<H>`.
- Partial delivery: three `trust-security.*.acceptance.ts` files only; `strs_test_coverage_mode`
  unchanged; the correction tables cover this group.
- Integration: attempt 1 of 45774743144: `LAUNCH TIMEOUT: trusted-suite.js exceeded its 900000 ms
  deadline ... last heartbeat step: myst-diagnostics` (three short steps left); attempt 2 success.
  Suite timestamps of the logs: 852 s on base run 45773405420, 854 s on attempt 2.
  `python -I <scripts>/suiteclosure.py <worktree> <B> <H>`: `trusted-suite: 364 files reached, 9
  touched`; the 8 files under `test/integration/` have `non-comment changed lines 0`, every changed
  line a `// @tests_req` comment (`git diff -U0`).
- Step limit: step 3 minutes (`ci.yml`) against `STEP_BUDGET_DEFAULT_MS = 3 * 60_000` and
  `LAUNCH_DEADLINE_MS = 15 * 60_000` (`hangWatchdog.ts`); shorter checks 90 s, 60 s and 20 s;
  `just ci-hang-dump` keeps processes and log tails only.
- Timeouts from one shard: attempt 1 of 45766254331 115 s / 77 s, attempt 2 93 s / 59 s.
- Never ran: `ci.yml` matrix `group: [trust-security]`; `gh run list --commit <H>`:
  `45774743144 workflow_dispatch success attempt 3`, `45773633868 pull_request success attempt 1`,
  no push to `main`; the job runs on `ubuntu-latest` only, and the Windows preflight skips it.

### S5. Known gaps, TRUST-012 and TRUST-014; fourth autonomous decision - VERIFIED

SHA `<H>`. `counts.log` not accepted: TRUST-012 S1, S2, TRUST-014 S1; the path titles read `Read a
text of the preview`, `Find the Studio in the Extensions view`, `Install and package from pinned
dependencies`; the vsix acceptance file holds no marker and `builtPackage.test.ts` installs nothing and
writes no VSIX. Follow-up before the switch, marker rule unchanged: `02-answers.md` items 6 and 7 and
`1-inbox/strs-acceptance-remaining-groups/02-answers.md` lines 3 and 4 (the owner's words).

### S6. Test plan, items marked `5a8a593` - VERIFIED

SHA `<H>`. New or changed tests: V6. Requirements: `python -I <scripts>/reqdiff.py <worktree> <B> <H>`
(`reqdiff.log`): `changed files under requirements: 20`; CORE-076 normative text and scenarios (diff:
edits in S1 to S6, new S7 to S11); `11 verification notes`; `3 verification notes + criteria` (TRUST
007, 065, 092); `2 generated file lists only` (002, 011): 14 SwRS notes, as written. Changelog: V9.
Local gates: first line of `work/gates/preflight-5a8a5939.log` names this change, branch and `<H>`,
line 5879 stages skipped on Windows, line 5880 `exit=0`. Evidence heading and sub-bullets: S7 and V12.

### S7. Evidence: new coverage mode - VERIFIED

SHA `<H>`. `okfreq validate "<export>/requirements" --check-links --project-root "<export>"` on the
exported head with the mode switched in the export only (`new-mode.log`): `exit=0`, `1228 requirements,
0 errors, 100 warnings`; `links.py`: the 26 broken links are the current mode's set.
`python -I <scripts>/w004scope.py <worktree> <scripts>/new-mode.log` (`w004scope.log`): `live StRS
without any @accepts_req marker: 74`, `W004 StRS in the new-mode log: 74; same set as the previous line:
True`. Tracked mode unchanged (V9).

### S8. Human decisions, the five other bullets - VERIFIED but one line (H3, since removed: P1)

- "One nominal acceptance test; a human step is a simulated input": `<504>/02-answers.md` Q3, Q6
  (owner).
- "Coverage counts test markers; the proof is its CI job": Q35 (owner).
- "May stop after any complete group; the switch lands last": overturned by the third pass, see H3.
- "The three paths not accepted get another kind of test ...": item 6, owner's words per the inbox item.
- "The remaining groups, these three paths and the switch are delivered later": item 7, same source.

## The pending item of the Test plan

"[ ] Verified at `5a8a593`: pending": left unchecked on purpose (checked by the Driver after a VERIFIED
verdict, then a description pass). Not a failure.

The table F1 to F7 of the second pass is folded into this note: F1 to F5 hold (S1 to S6), F6 and F7
(Human decisions, posted body) failed in the third pass only on H3 and hold now (P1 to P3).

## Carried claims

Each is `carried from 5a8a593: same head, same sentence` (commands and output as run by the first pass;
`gh run list` and `gh pr checks 532`, run again now, show no newer run and the same results).

### V1. Summary, other statements - VERIFIED

SHA `<H>`. Acceptance tests, job, one shard per group, report, tagging and Pages steps: V2, V4, V6.
First group trust and security, 5 of 8 paths accepted, 94 of 94 scenarios marked, mode not switched:
V3, V7, V9.

### V2. Deliverables: diagram, code sketch, one launch per file, `just ci-acceptance [GROUP]` - VERIFIED

SHA `<H>`. `acceptanceRunner.ts` lines 178-241: for each group a manifest
`acceptance-manifest.json`, then `for (const file of ...) { ... await LAUNCHERS[file.kind](context,
file); }`; kinds `trusted`, `restricted`, `vsix`. `acceptance-suite.ts:26` refuses a file whose
exported `windowKind` differs from the window. `git grep` shows `export const windowKind` and `run()`
with `await step(...)` calls in the acceptance files. `justfile:364: ci-acceptance GROUP="":
(_require-unlocked-screen "ci-acceptance")` runs `npm run test:acceptance [-- --group]`; preflight
skips it on Windows (line 490) and calls it at line 504. Linux execution: V12. macOS: from the recipe
only, never executed (a Known gaps bullet now says so).

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
`ci.yml:314 acceptance:` with `matrix: group: [trust-security]`, `fail-fast: false`; `report` (line
489), `tag-release` (628) and `pages` (713) need `acceptance`; `select_e2e_run.py` `STAGE_ARTIFACTS`
holds `e2e-acceptance`, refuses a missing or expired shard artifact (lines 134-152). Limits: S2.

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
(`requirements-lint` recipe unchanged).

### V10. Impacts (second sentence) and Blast radius - VERIFIED

SHA `<H>`. Tagging and Pages need every `acceptance` shard green (V4); preflight runs acceptance on
Linux and macOS (V2). Grade 3: the diff changes CI, release tagging and the Pages reuse; the change is
three commits on `<B>`, which a `git revert` undoes.

### V11. Autonomous decisions, first three - VERIFIED

SHA `<H>`. 1: V3, V9. 2: `counts.log` `scenarios removed: 0`; `SwRS scenarios unmarked at head but
marked at base: 0`; `tables.log` removals. 3: base `PUSH_REQUIRED_JOBS = (REQUIRED_JOB, "stress")`,
head `REQUIRED_JOBS = ("integration", "stress")` for every event, expired shard artifact refused.
(Fourth: S5; fifth: S3; sixth and seventh: T1, T2.)

### V12. Evidence and CI items of the Test plan - VERIFIED

Read only (`gh run view`, `gh api`, saved logs).
- `45774743144 5a8a5939 workflow_dispatch success 3`. Attempt 1: `acceptance (trust-security) success
  87 s step 59 s`, `stress success`, `integration failure`. Attempt 2: `integration success`, `report`,
  `gallery`, `checks` success. Attempt 3: `acceptance success 91 s step 55 s`, report success.
- Launches, attempt 1 log lines 447, 590, 675: `passed ... (trusted) in 26 s`, `(restricted) in 8 s`,
  `(vsix) in 16 s`; the downloaded attempt-1 artifact's manifest: `status passed`, `revision <H>`,
  `dirty False`, three launches passed.
- Report log of attempt 3, line 418: `acceptance trust-security: kept attempt 3
  (e2e-acceptance-trust-security-attempt-3)`; the artifact is listed, not expired.
- `45773633868 5a8a5939 pull_request success`; `gh pr checks 532` (run again now): checks, report,
  static, static-windows, viewer-graph, visual `pass`, heavy jobs `skipping`.

### V13. Known gaps, TRUST-065 S2 - VERIFIED

SHA `<H>`. A script reading `PAGE_MESSAGE_GATES` of `src/session/pageMessages.ts` and the S2 table:
`gated types: 50 listed in S2 table: 41`, `listed but not gated: []`; the nine missing are
previewExportHtml, previewSideBySideChanged, previewBaselineRequested, previewFindReplace,
previewBlocksDelete, previewBlankRunDelete, previewDropFiles, previewSaveRequest, previewEditReopen.

### V14. Review box "approved at `5a8a593` (carried from `18c63e5`)" - VERIFIED

`$CHANTIER log CR-505`: `2026-11-26T06:52:19Z driver note r5 inspector approved at 0feab1d9...`,
`06:52:32Z r5 approved at 0feab1d, committed as 18c63e5e85283af68e1e79dd78aad3f3d6782e13`.
`git log --format="%h tree=%t"`: `18c63e5e`, `369ab794`, `5a8a5939` all `tree=cb4e616a`;
`git range-diff`: `d19b69db = ef6307f7`, `0feab1d9 = 956cb503`, `18c63e5e = 5a8a5939`.

### V15. Internal references and clean body - VERIFIED

Posted body: the change id appears only under "Internal references"; "follows pull request #524,
merged" matches `gh pr view 524`: `MERGED 2026-11-26T07:10:45Z`; no image; sections and fold in the
project's order.

## Delivery against the specification (partial)

| Evidence plan item | Judgment | Proof |
| --- | --- | --- |
| Paths accepted | VERIFIED | V3 |
| Checks 4, 5 (tooling tests, new cases) | VERIFIED | V6, gate log (`tests 5357, pass 5349, fail 0, skipped 8`; security `116/116`; `254 passed`) |
| Check 6 (acceptance folder and markers) | VERIFIED | V5, V8 |
| Check 8 (preflight on Windows) | VERIFIED | S6 |
| Check 9 (heavy job, shard, limits, manifest) | VERIFIED; `integration` only on a second attempt, stated in Known gaps | V12 |
| Check 10 (newest attempt kept) | VERIFIED for one group, as attempt 3 | V12 |
| Old mode kept, no gate | VERIFIED | V9 |
| New mode, 0 errors | VERIFIED | S7 |
| Body states what is left | VERIFIED in the posted body | S4, S5 |

No long gate is configured (`$CHANTIER handoff CR-505`, first pass). Before and after:
`work/verifier/evidence/before-after.md`; its "cannot be shown" items are limits, not missing pairs.

## Remarks (not failures)

- R1. `ci.yml` comment of the acceptance job says "About twice" while 5 minutes is 2.6 times.
- R2. The integration flake is a bug to fix at its cause; the body says so, and no inbox item naming
  the run or the deadline was found by the first pass.
- R3. "this change edits only requirement marker comments in that suite": the suite's import closure also
  holds `test/reportPaths.ts`, which gains one exported constant used by the acceptance runner only.
- R4. "merging the attempts of several groups never ran in CI" is true of real shard reports; the unit
  test `test/build/selectAcceptanceAttempts.test.ts` line 40 runs the script on two made-up groups.
- R5. Run 45766254331 is named "at an earlier commit" without its SHA (`0feab1d`).

- R6. Owner answers Q28 (real VS Code is the acceptance bench) and Q30/Q30b (each scenario tested or
  removed) are not bullets of "Human decisions"; Summary and Changes state both outcomes, and the
  template leaves the choice of the shaping decisions to the writer: not a failure.
- R7. The one re-run of the failed CI jobs, taken without the user, is stated in Known gaps and the
  Test plan, not under "Autonomous decisions" (it is no investigation, round or conflict decision).

## Notes on the fourth pass

- No CI run started or re-run, no tracked file changed, no commit, push or pull request edit.
- Files written, all under `work/`: `verify.md`, `verifier/posted-body-4.md`,
  `verifier/update_verify4.py`.

## Notes on the third pass

- No CI run started or re-run, no tracked file changed, no commit, push or pull request edit.
- Files written, all under `work/`: `verify.md`, `verifier/posted-body-3.md`,
  `verifier/markers-diff.log`, `verifier/update_verify3.py`. One `git diff` call had its `--output`
  after `--` and printed to the console instead; one had an invalid pattern; both were run again.

## Notes on the second pass

- No CI run started or re-run, no tracked file changed, no commit, push or pull request edit.
- Deviations from the card, disclosed: `suiteclosure.py` passed the 120 s command limit and the harness
  moved it to the background (it ended with exit 0); a few commands were chained or changed folder into
  the worktree (never into the change's folder). Scratch logs I made (`work/scratch/verify2/`) are
  removed.

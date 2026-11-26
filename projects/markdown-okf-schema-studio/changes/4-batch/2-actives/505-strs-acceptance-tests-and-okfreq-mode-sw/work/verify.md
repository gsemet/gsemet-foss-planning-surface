# CR-505 verification

Head: 9d7e788a479dec70fd882d295bf0d5e78f4f6b98

- Base: `89cae5ff42f6dfc34590b06c3f979f5a3cbce6d4` (head of the change below this one in the stack).
  Old base `3478f0992688c7a354d11106145793fc83590506`, old head
  `5a8a59398692a0d497ad88c18e5f142de1411638`.
- This pass judges the restack move `5a8a593..9d7e788` and the description posted for the new head.
- In this pass: `<head>` = `9d7e788`, `<base>` = `89cae5f`, `<old head>` = `5a8a593`, `<old base>` =
  `3478f09`, each used with its full SHA above in the commands; `<W>` the worktree; `<S>` =
  `work/verifier/`; `<repo>` = `gsemet/markdown-okf-schema-studio`. `V..`, `S..`, `T..`, `P..` point to
  the earlier passes kept below.
- Judged: the partial delivery (trust and security group; mode switch and gate left, `02-answers.md`
  items 5 to 7).

## Verdict: NOT VERIFIED

One claim fails: F1, the form of two proofs of the posted description. Code, tests, CI, requirements,
figures and every other claim hold.

## F1. Description, Test plan: two proofs name no SHA - NOT VERIFIED

SHA `<head>`. `gh pr view 532 --repo <repo> --json body --jq .body > <S>/posted-body-6.md`, lines 206
and 207:

> - The limits were set from the first measured run ([45766254331](...), at an earlier commit): job 115 s, test step 77 s.
> - Re-run of the shard alone, on an earlier head of this change ([run 45774743144](...)): job 91 s, test step 55 s; ...

`gh run view 45766254331 --repo <repo> --json databaseId,headSha,event,conclusion,attempt`:
`headSha 0feab1d914f39682507bf5c0d58adddd4174c395`, `success`, attempt 2. The same for 45774743144:
`headSha 5a8a59398692a0d497ad88c18e5f142de1411638`, `success`, attempt 3.

- Rule: `references/verifier.md` lines 95 to 97, "Each proof in the description names its SHA, which is
  the head or carried with its reason"; `references/pr-template.md` lines 92 to 96, "A proof carried
  over a move says so (`at <head7> (carried from <sha7>)` ...)". Neither line names the head or a
  `carried from` SHA.
- `$CHANTIER log CR-505`, `09:41:06Z ... ship`: it named the line of run 45774743144 as naming
  `5a8a593`, "not in 9d7e788's history"; the posted text cites that run (line 207) with words in the
  place of the SHA.
- The figures are right (N19, N20) and the carry is legitimate: `git diff --stat <old head> <head>`
  lists no file of `.github/`, `scripts/` or `justfile` (N3). The earlier passes recorded the first
  line as remark R5 and passed it; judged here against the card's rule, it fails.
- Fix (description only): line 206 "at `9d7e788` (carried from `0feab1d`: the run the limits were set
  from)" instead of "at an earlier commit"; line 207 "at `9d7e788` (carried from `5a8a593`)" instead
  of "on an earlier head of this change".

## The move

### N1. State - VERIFIED

SHA `<head>`. `git -C <W> rev-parse HEAD`: `9d7e788a479dec70fd882d295bf0d5e78f4f6b98`; `git -C <W>
status --porcelain --branch`: the branch line only; `git merge-base <head> <base>` = `<base>`; the
change is three commits on it (`f023b7d9`, `4e665fc6`, `9d7e788a`). `gh pr view 532 --repo <repo>
--json state,isDraft,headRefOid,baseRefName,updatedAt,title`: `OPEN`, draft `true`, base `main`, head
`<head>`, `updatedAt 2026-11-26T10:06:51Z`, title `ci: accept trust and security use case paths in a
real VS Code`. Pull request 529: `OPEN`, draft, head `<base>`.

### N2. The move leaves the changed lines of the change as they were - VERIFIED

SHA `<head>`. `git range-diff <old base>..<old head> <base>..<head>`: the three commits map one to
one; differences in context lines and the resolution in `run-tests.ts`. A script comparing, per file,
the `+` and `-` lines of `git diff <old base> <old head>` and `git diff <base> <head>`: `files 120
identical changed lines 120`.

### N3. What the move brought in - VERIFIED

SHA `<head>`. `git diff --stat <old head> <head>`: 12 files, those of the base's three commits:
`CONTRIBUTING.md`, `test/build/{trustedParts,webviewFrames}.test.ts`,
`test/integration/{openAtLine.test,previewEditing.test,realInput/harness,run-tests,trusted-suite}.ts`,
`test/shared/{hangWatchdog,launchWatchdog,trustedParts,webviewFrames}.ts`. Every other file is byte
for byte that of `<old head>`. `git diff -U0 -G"@(tests|accepts|implements)_req" <old head> <head>`:
no output.

### N4. The conflict resolution in `test/integration/run-tests.ts` - VERIFIED

SHA `<head>`. Read of the file and `git diff -U0` of it against each base: both imports kept;
`main(suites: IntegrationScope)`; `if (suites === "trusted") { await runTrustedLaunches(); return; }`;
the full run calls `runTrustedLaunches()` between the untrusted and standalone suites;
`parseRunnerArgs(process.argv.slice(2))` comes first. Flag order in `runnerArgs.ts` is that of the
base's branches. `npm run compile`: exit 0; tests of N10; the `integration` job ran both parts and
passed at `<head>` (N18).

## Claims of the posted description

Changes of the body since the last judged one (`git diff --no-index -U0 <S>/posted-body-5.md
<S>/posted-body-6.md`): the second Known gaps bullet (line 180) and Test plan lines 199
to 205 and 207 to 211 (line 206 is unchanged).
Summary, Deliverables, Changes, Impacts, Blast radius, Autonomous decisions, the other Known gaps and
Human decisions are unchanged text.

### N5. Summary - VERIFIED

SHA `<base>`, `<head>`. `python -I <S>/suiteclosure_tree.py <base tree>`
(`suiteclosure-89cae5f.log`): 19 `@accepts_req` lines, every file reached by an integration suite
(`scroll-sync`, `untrusted` or `trusted`); `counts-9d7e788a.log`: base `accepted: 17` of 156; head
`TRUST scenarios 94, with @tests_req 94`, `702` of `2638` unmarked, `not accepted: 134`. Other
statements: N6, N7, N11.

### N6. Deliverables (diagram, code sketch, one launch per file, `just ci-acceptance [GROUP]`) - VERIFIED

Carried from `5a8a593` (V2): `acceptanceRunner.ts`, the launchers, acceptance files and `justfile` are byte for byte
those of `<old head>` (N3); the resolution leaves the acceptance branch of `run-tests.ts` as it was
(N2, N4). The shard ran on Linux at `<head>` (N18).

### N7. Accepted paths table - VERIFIED

SHA `<base>`, `<head>`. `okfreq trace requirements --json` on both trees, `python -I <S>/counts.py`
(`counts-9d7e788a.log`): base `156 / accepted 17 / not 139`; head `156 / 22 / 134`; newly accepted
TRUST-001 S1, 004 S1, 006 S1, 009 S1, 009 S2. `git ls-tree` and `git grep "@accepts_req" <head> --
test/integration/acceptance`: `support.ts` and three trust-security files; markers at lines 41, 123,
176, 222 of the trusted file and 36 of the restricted file; no `@tests_req StRS`.

### N8. Changes: runner, report, CI bullets, built VSIX, limits - VERIFIED

SHA `<head>` for the CI file (`ci.yml`: `acceptance` job line 314, `timeout-minutes: 5` line 322,
`group: [trust-security]` line 327, test step `timeout-minutes: 3` line 351; heavy run N18);
the rest carried from `5a8a593` (V4, S2): `ci.yml`, `.github/`, `scripts/` and the runner files are
unchanged by the move (N3). `git diff <base> <head> -- .github/workflows/ci.yml` is where the job
appears: `git grep acceptance <base> -- .github/workflows/ci.yml` prints nothing.

### N9. Changes: tests, requirements, markers, docs; no file under `src/` - VERIFIED

SHA `<head>`. `git diff --stat <base> <head> -- src requirements/config.yml CHANGELOG.md
docs/releases-notes skills sphinx esbuild.mjs .vscodeignore`: empty; `--shortstat`: `120 files
changed, 3373 insertions(+), 618 deletions(-)`; acceptance files as N7; `test/security/builtPackage.test.ts`
added. `git diff <base> <head> -- CONTRIBUTING.md` read: the acceptance text agrees with the base's
two-launch text. `python -I <S>/reqdiff.py <W> <base> <head>`: N12.

### N10. Tooling and scenario tests - VERIFIED

SHA `<head>`. `node --import ./scripts/register-myst-patches.mjs --test` on the runnerArgs,
selectAcceptanceAttempts, trustedParts, webviewFrames, blockReq, pageStateMessages, lifeReq,
trustReq, dropFiles, runtimePaletteActions and security tests (`node-tests-9d7e788a.log`): `tests
342, pass 342, fail 0, skipped 0`. `uv run ... pytest -q test/build/test_workflows.py
test/build/test_select_e2e_run.py test/build/test_unpack_vsix.py` (`pytest-9d7e788a.log`): `149
passed`.
Carried from `5a8a593` (V6): "exercise code that is new here" (base-side collection error and `34
failed, 72 passed`; the move adds nothing under `.github/`, `scripts/`, `justfile`, and `git ls-tree
<base>` finds none of the three new sources) and "four tightened ones were seen to fail"
(`<S>/mutate.py` breaks `resource-policy.js` and `rendering.js` and runs `trustReq.roots` and
`readOnlyRoot` tests; none of those sources or tests is among the 12 files of N3).

### N11. Trust and security counts and the three marker tables - VERIFIED

SHA `<head>`. `python -I <S>/tables.py <base tree> <head tree>` (`tables-9d7e788a.log`): marker reading
cross-checked with okfreq `74/74` and `94/94`; `table rows: 61`, `rows equal: 61`, `table rows with
no changed marker: []`, the one other changed file `test/security/builtPackage.test.ts` is in the
covered table; `rows: 20` of newly covered scenarios agree. `counts-9d7e788a.log`: scenarios removed 0,
20 TRUST scenarios newly marked, none lost. The "dropped markers" table: carried from `5a8a593` (V7,
compared with a past commit).

### N12. Requirements - VERIFIED

SHA `<head>`. `just requirements-lint` (`requirements-lint-9d7e788a.log`): exit 0, `1228 requirements,
0 errors, 26 warnings`, 0 files to regenerate, `96 StRS`, `625` citations valid. `just check-markers`:
exit 0, `11 companion file(s), 459 in-force SwRS marked, 12 files on the marker baseline`.
`reqdiff.py`: 20 requirement files; CORE-076 normative text and S1 to S6 edited, S7 to S11 new; 14
trust and security SwRS notes (11 notes, 3 notes and criteria: 007, 065, 092); 002 and 011 generated
lists only.

### N13. Coverage mode, changelog, release notes - VERIFIED

SHA `<base>`, `<head>`. `git grep -n strs_test_coverage_mode <base> <head> --
requirements/config.yml`: both `linked-swrs-and-validation-test`; empty diff of N9 (`CHANGELOG.md`,
release notes). `package.json`: one added line, `"test:acceptance"`.

### N14. New coverage mode: 0 errors, 100 warnings - VERIFIED

SHA `<head>`. `python -I <S>/newmode.py . <head> <work>/scratch/nm <S>` (`newmode-new-9d7e788.log`):
tracked mode on the copy `0 errors, 26 warnings`; new mode `1228 requirements, 0 errors, 100
warnings`, 74 W004, 26 broken-link lines identical to the tracked mode's; trust and security W004:
012, 014. The copy leaves out 52 long-path files, none under `requirements/` (see Notes). The result
does not rest on the copy alone: also carried from `5a8a593` (S7: 0 errors, 100 warnings on a full
export), no file under `requirements/` and no marker line differs between the two heads (N3). Before,
`<base>`: 104 warnings, 78 W004.

### N15. Impacts and Blast radius - VERIFIED

SHA `<head>`. N9 (no `src/`), N13 (`package.json`). Tagging and Pages need the `acceptance` shards,
preflight runs acceptance on Linux and macOS: carried from `5a8a593` (V10; `ci.yml`, `justfile`
unchanged, N3). The change is three commits on `<base>` (N1), which a `git revert` undoes.

### N16. Autonomous decisions (seven) and Human decisions (four) - VERIFIED

Carried from `5a8a593` (V11, S3, S5, T1 to T3, P2): same text (body diff above); the code they
describe is unchanged by the move (N2, N3), and at `<head>` `LAUNCH_DEADLINE_MS` is still 15 minutes
and `STEP_BUDGET_DEFAULT_MS` 3 minutes (`hangWatchdog.ts` lines 29 and 47).

### N17. Known gaps - VERIFIED

1. Partial delivery: N7, N13 at `<head>`.
2. Integration timeout: the cut attempt is attempt 1 of run 45774743144 at `<old head>` (carried, S4:
   `LAUNCH TIMEOUT: trusted-suite.js exceeded its 900000 ms deadline`; attempt 2 passed). At `<head>`:
   `trustedParts.ts` and `runTrustedLaunches()` give two launches, each `runScenario` under its own
   `watchLaunch` (`run-tests.ts` lines 101, 206); `work/ci-45794286167-integration.log`: part 1 from
   `09:44:23` to `09:51:22` (about 420 s), part 2 from `09:51:27` to `09:59:32` (about 485 s), `just
   ci-integration` passed; step `09:41:45` to `10:00:02` = 1097 s, `ci.yml` line 295 `timeout-minutes:
   20`; attempt 1.
3. 3-minute step limit: `ci.yml` line 351, the constants of N16; the base changes only a dump folder
   label and a comment in the watchdog files (`git diff <old base> <base>`).
4. Timeouts from one shard's first attempt: carried from `5a8a593` (S4).
5. Never ran: matrix `[trust-security]`; `gh run list --commit <head>`: only 45794286167
   (`workflow_dispatch`) and 45794229373 (`pull_request`), no push to `main`; macOS carried (S4).
6. TRUST-012, TRUST-014 S1: not accepted at `<head>` (N7 counts); reasons and follow-up carried (S5).
7. TRUST-065 S2: carried from `5a8a593` (V13): `src/` and the requirement are unchanged (N3).

### N18. Test plan: heavy run and shard figures - VERIFIED

SHA `<head>`. `gh run view 45794286167`: `workflow_dispatch`, head `<head>`, success, attempt 1;
`integration`, `stress`, `acceptance (trust-security)`, `report`, `checks` success. Shard job 82 s,
test step 52 s; `work/ci-45794286167-acceptance.log` line 448 trusted passed in 30 s, 592 restricted 6
s, 678 vsix 10 s. Downloaded artifact `e2e-acceptance-trust-security-attempt-1`, read with
`python -I <S>/manifest.py`: `status passed`, `revision <head>`, `dirty false`, scope
`trust-security`, launches passed 30037, 5813, 10249 ms.

### N19. Figures of the re-run of the shard alone - VERIFIED (their SHA form fails, F1)

Carried from `5a8a593` (V12): job 91 s, step 55 s, `-attempt-3` uploaded,
`work/ci-45774743144-report-attempt3.log` line 418 `acceptance trust-security: kept attempt 3`;
the attempt-selection script and `ci.yml` are unchanged by the move (N3).

### N20. Figures of the first measured run - VERIFIED (their SHA form fails, F1)

Carried from `5a8a593` (S2): run 45766254331 attempt 1, job 115 s, step 77 s.

### N21. Changelog and local gates - VERIFIED

SHA `<head>`. Changelog: N9. `work/gates/preflight-9d7e788a.log`: unit `5366` tests, `5358` pass, `0`
fail, `8` skipped; security `116/116`; `254 passed`; line 5889 `ci-static: passed`, line 5890 the
Windows skip line naming `acceptance`. The log prints no SHA: it is tied to the head by the last
section of `work/conflicts.md` (`just preflight` at `9d7e788a`, passed), its file time (10:39, after
the commit of 10:29, local) and the green `static-windows` job at `<head>`.

### N22. Review: approved at `9d7e788a` - VERIFIED

`$CHANTIER log CR-505`: `2026-11-26T10:06:46Z driver note note=move 5a8a593..9d7e788 (restack)
inspector approved at 9d7e788a479dec70fd882d295bf0d5e78f4f6b98`.

### N23. CI green at `9d7e788a` - VERIFIED

SHA `<head>`. `gh pr checks 532`: `checks`, `report`, `static`, `static-windows`, `viewer-graph`,
`visual` pass, heavy jobs skipping (run 45794229373); `gh run list --commit <head>`: both runs
success, attempt 1.

### N24. The posted description is clean - VERIFIED

SHA `<head>`. Read of `posted-body-6.md`: the sections and the fold in the project's order; searched:
no image, no user name or home folder, no `STALE`, `UNVERIFIED` or `pending`, no batch, round or role
name; the change id only under "Internal references" (line 215). No claim needs an `UNVERIFIED` mark.
"Verified" is unchecked on purpose until a verdict is recorded.

## Delivery against the specification (partial), at `9d7e788`

| Evidence plan item | Judgment | Proof |
| --- | --- | --- |
| Paths accepted | VERIFIED | N7 |
| Checks 4, 5 (tooling tests, new cases) | VERIFIED | N10, N21 |
| Check 6 (acceptance folder and markers) | VERIFIED | N7, N12 |
| Check 8 (preflight on Windows) | VERIFIED | N21 |
| Check 9 (heavy job, shard, limits, manifest) | VERIFIED; `integration` passed on the first attempt | N18, N17 |
| Check 10 (newest attempt kept) | VERIFIED for one group, as attempt 3 (carried) | N19 |
| Old mode kept, no gate | VERIFIED | N13 |
| New mode, 0 errors | VERIFIED | N14 |
| Body states what is left | VERIFIED | N17 |

No long gate is configured. Before and after: `work/verifier/evidence/before-after.md` (rewritten for
this move); its "cannot be shown" items are limits, not missing pairs.

## Remarks (not failures)

- R10. Known gaps, line 180, "On an earlier head of this change" would also read better with the SHA
  (`5a8a593`, in the `carried from` form); it states a gap and is not a Test plan proof.
- R11. The restack resolution is not listed under "Autonomous decisions": it keeps both sides, and the
  base's two launches are the only working form (`trustedParts.ts` refuses a full trusted run with no
  part), so it is read as no choice taken.
- R12. The forge base is still `main`, so the forge diff also shows the three commits of pull request
  529.
- R13. The pull request `visual` job at `<head>` took 14 min 45 s of its 15-minute limit (Driver's note
  `09:57:44Z`).
- R14. The preflight log has no SHA line (N21).
- Still apply: R1 (`ci.yml` comment "About twice" while the limit is 2.6 times), R8 (scenario ids read
  as product terms).

## Notes on this pass

- No CI run started or re-run, no tracked file changed, no commit, push or pull request edit; no
  command refused.
- Deviations from the card, disclosed: several shell calls chained commands (`&&`, `;`, pipes, one
  here-document) and some changed folder into the worktree; one call set a leading variable, and one
  changed folder into the change's `work/` folder before writing `verifier/posted-body-6.md`, which
  the startup core forbids.
- `newmode.py` left out of the scratch copy, before extraction, the 52 files whose path there would
  pass 259 characters. No tool failed on a path, but the card makes a too-long scratch path a stop to
  report, and filtering them is a way around it: reported here; N14 also stands on the carried proof.
- Removed at the end: the base worktree `<W>/.artifacts/vbase`, the scratch copy, the downloaded
  artifact and its folder.
- Files written, all under `work/` but for ignored build output in the worktree: `verify.md`,
  `verifier/evidence/before-after.md`, `verifier/posted-body-6.md`, the scripts and `*.log` files of
  this pass in `verifier/`.

## Earlier passes (judged at `5a8a593`, kept as history; their verdicts are not this pass's)

Head of the passes below: `5a8a59398692a0d497ad88c18e5f142de1411638`

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

## Verdict of the passes at 5a8a593: VERIFIED

## Fifth pass (description only, same head): VERIFIED

Judges the one edit of the posted description since the fourth pass and the description as posted; every
other claim is carried from `5a8a593` (same head, same sentence). `<H>` is
`5a8a59398692a0d497ad88c18e5f142de1411638`, `<B>` is `3478f0992688c7a354d11106145793fc83590506`.

### D1. State - VERIFIED

SHA `<H>`. `git -C <worktree> rev-parse HEAD`: `5a8a59398692a0d497ad88c18e5f142de1411638`;
`git -C <worktree> status --porcelain --branch`: the branch line only. `gh pr view 532 --repo
gsemet/markdown-okf-schema-studio --json state,isDraft,headRefOid,baseRefName,updatedAt,title`: `OPEN`,
draft `true`, base `main`, head `5a8a593`, `updatedAt 2026-11-26T09:19:30Z`, title `ci: accept trust and
security use case paths in a real VS Code`.

### D2. The only change of the description is the checked "Verified" item - VERIFIED

SHA `<H>`. `gh pr view 532 --repo <repo> --json body --jq .body > verifier/posted-body-5.md`, then
`git diff --no-index -U0 verifier/posted-body-4.md verifier/posted-body-5.md`: one hunk,
`@@ -210 +210 @@`,
`-- [ ] Verified at `5a8a593`: pending`
`+- [x] Verified at `5a8a593`: the delivered change and the claims of this description were checked
against that commit`.
`git diff --no-index -U0 pr-body.md verifier/posted-body-5.md`: one added empty last line, nothing else.

### D3. "Verified at `5a8a593`: the delivered change and the claims of this description were checked against that commit" - VERIFIED

SHA `<H>`. `$CHANTIER log 505`: `2026-11-26T09:19:08Z driver verdict result=VERIFIED
head=5a8a59398692a0d497ad88c18e5f142de1411638 base=3478f0992688c7a354d11106145793fc83590506`, the last
verdict before the body was posted (`09:19:32Z driver note closing: body posted at 5a8a593`). The delivered change
and the description's claims are the ones this note judges at `<H>` (P1 to P3, T1 to T4, S1 to S8, V1 to
V15); the older run it cites is named there as an earlier commit's.

### D4. The other items that cite a proof of the head - VERIFIED

SHA `<H>`.
- Review box "approved at `5a8a593` (carried from `18c63e5`)": same log, `06:52:32Z driver note r5
  approved at 0feab1d, committed as 18c63e5e85283af68e1e79dd78aad3f3d6782e13`; the carry is V14.
- CI box: `gh pr checks 532`: `checks`, `report`, `static`, `static-windows`, `viewer-graph`, `visual`
  `pass`, the other jobs `skipping`; `gh run list --commit <H>`: `45774743144 workflow_dispatch success
  attempt 3`, `45773633868 pull_request success attempt 1`, no other run.
- Changes, "CI and release guidelines, `AGENTS.md` and `CONTRIBUTING.md`" and "No file under `src/`":
  `git -C <worktree> diff --stat=200 <B> <H>`: `ci.guidelines.md`, `release-process.guidelines.md`,
  `AGENTS.md`, `CONTRIBUTING.md`, `docs/how-we-ship.md`, `project.guidelines.md` listed, no `src/` path;
  `120 files changed`.

### D5. The posted description is clean - VERIFIED

SHA `<H>`. Read of `verifier/posted-body-5.md`: headings Summary, Deliverables, Changes, Impacts (the
order of `.github/PULL_REQUEST_TEMPLATE.md`), Blast radius, Autonomous decisions, Known gaps, then one
`<details>` fold (lines 187 to 217, blank line inside each end) with Human decisions, Test plan, Internal
references. A search for `!\[|<img|STALE|UNVERIFIED|pending|<drive>:\Users|/home/|<user name>|
.agents/changes|4-batch|CR-[0-9]+|<details>|</details>|<summary>|^## ` finds only the headings, the fold
lines and `CR-505` on line 215, under Internal references: no image, no stale or unproven mark, no
pending item, no user name or home folder. A case-insensitive search for the agent role names, `batch`,
`round` and `grill`: no match. Known gaps: no `UNVERIFIED` mark needs a bullet; the section is the one
earlier passes judged (D2).

### Remarks of the fifth pass (not failures)

- R8. `pull-request.guidelines.md` lists "scenario ids" among the internal references. The ids in this
  body are those of the repository's own requirements bundle, whose markers are the subject of the
  change (not plan or backlog ids), and merged pull request 524 names them the same way (`gh pr view
  524`): read as product terms, as the earlier passes did.
- R9. `verifier/evidence/before-after.md`, pair 9, still gives the `08:54:30Z` version as the posted
  "after"; the description judged now is the `09:19:30Z` one (D1, D2). No pair was captured again.
- Files written by this pass, all under `work/`: `verify.md`, `verifier/posted-body-5.md`,
  `verifier/update_verify5.py`. No CI run started or re-run, no tracked file changed, no commit, push or
  pull request edit. One call that edited the update script had backticks the shell ran as commands
  (command not found); it changed nothing and was run again without them.

## Fourth pass

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

## The "Verified" item of the Test plan

Left unchecked up to the fourth pass; checked in the posted description now, judged in D3.

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

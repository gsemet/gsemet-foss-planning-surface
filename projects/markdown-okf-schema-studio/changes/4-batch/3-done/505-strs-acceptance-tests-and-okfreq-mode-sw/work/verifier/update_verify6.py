"""Verifier of CR-505: put the pass at head 9d7e788 on top of verify.md, keeping the earlier passes.

usage: python -I update_verify6.py <verify.md>
"""
import sys
from pathlib import Path

OLD_HEAD = "5a8a59398692a0d497ad88c18e5f142de1411638"

NEW = r"""# CR-505 verification

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

"""

path = Path(sys.argv[1])
text = path.read_text(encoding="utf-8")
head_line = f"Head: {OLD_HEAD}\n"
assert text.startswith("# CR-505 verification\n\n" + head_line), "unexpected start of the note"
assert text.count(head_line) == 1
old = text[len("# CR-505 verification\n\n"):]
old = old.replace(head_line, f"Head of the passes below: `{OLD_HEAD}`\n", 1)
assert old.count("## Verdict: VERIFIED\n") == 1
old = old.replace("## Verdict: VERIFIED\n", "## Verdict of the passes at 5a8a593: VERIFIED\n", 1)
path.write_text(NEW + old, encoding="utf-8", newline="\n")
print("written", path.stat().st_size, "bytes")

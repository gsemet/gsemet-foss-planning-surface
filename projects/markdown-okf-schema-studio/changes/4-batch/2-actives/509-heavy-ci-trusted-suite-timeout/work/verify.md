# CR-509 verification

Head: 89cae5ff42f6dfc34590b06c3f979f5a3cbce6d4

Verdict: **NOT VERIFIED**, on the posted PR description only. The change and its proofs hold at
`89cae5f` (M0 to E6). The description is still the text written for `b24d3bf`: besides the table
rows and the Test plan that name old commits (not counted here as failures on their own), four
sentences of **Known gaps** and **Autonomous decisions** are false at `89cae5f` (D6, D8). The
facts the new text must hold are in "Facts at 89cae5f for the new description".

Notation: `W` = the CR worktree (every command runs there unless said), `S` = `work/scratch`,
`G` = `work/gates`, `R` = `--repo gsemet/markdown-okf-schema-studio`, `B` = new base
`3478f0992688c7a354d11106145793fc83590506` (origin/main and the merge base), `Bo` = old base
`5a73b6ebcf66ef80b412afcdbfd09c4defc028d8`. "SHA" is the commit a claim was judged at. The
previous judgment is the one at `b24d3bf` (this file's former text). `git status --porcelain`
printed nothing after the checks.

Long gate: none is configured (no `chantier.yaml` in `W` or the planning project). The local gate
is cited by `G/preflight-89cae5f.log` (copy of the `just preflight` log given in the brief; first
line: `CR-509 chantier/batch-09/cr-509-reliable-heavy-ci-split-the-trusted-laun 89cae5f...`) and
by my own run `G/verify-ci-static-89cae5f.log`.

## The move

### M0 b24d3bf (on Bo) to 89cae5f (on B) (89cae5f)

`git range-diff Bo..b24d3bf B..89cae5f`: commit 2 `=`, commit 3 `=`, commit 1 `!`; its only
difference is one context line in `test/integration/trusted-suite.ts`
(`// @tests_req SwRS-MDOKFSTUDIO-TRUST-012` became `...TRUST-012#S1`). `git patch-id --stable` of
the whole diff differs (`c6347e87` / `ccc6e005`), so nothing carries by patch identity.
`git merge-base origin/main 89cae5f` and `git rev-parse origin/main` both print `B`.

What the base brought that the proofs exercise (`git diff --name-only Bo B`): 87 changed files
under `test/integration`, `justfile` and `CONTRIBUTING.md` together, plus requirements, marker
scripts, `test/build`, documentation and `uv.lock` (`okf-schema`, the requirements tool, 0.17.0 to
0.18.1; the worktree environment holds `okf_schema-0.18.1`); nothing under `src`, `test/shared`,
`.github`, `package.json` or `package-lock.json`.
`git diff -U0 Bo B -- test/integration test/shared` without `previewEditing.test.ts` and
`previewEditingSchemaSteps.ts`, comment lines removed, leaves no changed code line.
`previewEditing.test.ts` moved its schema steps to `previewEditingSchemaSteps.ts` and joined its
imports.

## Local checks

### L1 the local static stage passes (89cae5f) - VERIFIED

`just ci-static > G/verify-ci-static-89cae5f.log`: `check-no-merge-commits: passed (3 commits)`,
boundaries, limits (`0 on the size baseline`), exports, markers (`459 in-force SwRS marked`),
settings passed; clip kit `pass 56, fail 0`; unit `tests 5335, pass 5328, fail 0, skipped 7`;
contracts `tests 0`; security `pass 107`; `213 passed`; `1228 requirements, 0 errors, 26
warnings`; `0 indexes would change`; `0 files would change`; `found 0 vulnerabilities`; `4
passed`; `ci-static: passed`.
`G/preflight-89cae5f.log`: L5620-5625 unit `tests 5335, pass 5327, fail 0, skipped 8`; L5784
`1228 requirements, 0 errors, 26 warnings`; L5838 `0 indexes would change`; L5841 `0 files would
change`; L5879 `ci-static: passed`; L5880 `preflight: visual, viewer-graph, integration, report
and gallery stages skipped on Windows; CI runs them`.

### L2 the 9 new tests pass at the head and fail on the old behaviour (89cae5f) - VERIFIED

`node --test out/test/build/trustedParts.test.js out/test/build/webviewFrames.test.js`:
`tests 9, pass 9, fail 0`. Same two files from a throwaway copy `out/verify-red-test` after
`python -I S/verify-red-standins.py <that copy>` (single launch, no URL filter, no frame list, no
dump label): `tests 9, pass 0, fail 9`, assertion errors. Copy removed.

### L3 files stay under 1500 lines (89cae5f) - VERIFIED

`wc -l`: `trusted-suite.ts` 328, `run-tests.ts` 293, `harness.ts` 827, `previewEditing.test.ts`
1314; `check-limits` passed (L1).

## Specification, "What changes"

### S1 two launches with the stated steps and order (89cae5f) - VERIFIED

`git diff Bo B -- test/integration/trusted-suite.ts` changes marker comments only, so the base's
step list is the one judged before. Unit test 1 (55 names, each part in order) passes (L2). Both
heavy runs at the head run part 1 = the 55 reference names without `real-input` and
`preview-editing`, in order, and part 2 = four (E4). The `@tests_req` lines of
`trusted-suite.ts` are the same four at `B` and at the head (`git grep`).

### S2 each part has its own window, port, heartbeat, launch name, suite label (89cae5f) - VERIFIED

`git grep` at HEAD, `run-tests.ts`: L242 `for (const launch of trustedLaunches(process.env))
await runScenario(...)`; L100 `mkdtempSync`, L121 `freePort()`, L119
`heartbeatFileFor(instanceId, trusted?.suite ?? suiteName)`, L138 `name`, `dumpLabel`, L150
`STUDIO_TRUSTED_PART`. `trusted-suite.ts` L73-74: `TRUSTED LAUNCH` log,
`withSuiteWatchdog(launch.suite, ...)`.

### S3 selection variable, one launch for a scenario, scope kept (89cae5f) - VERIFIED

Unit tests 2 to 4 pass (L2); L281 of `run-tests.ts` still sets `scope`; the base did not change
`run-tests.ts` or `test/shared` (M0). Stress logs show one launch (E5).

### S4 frontmatter block after the part that runs preview-editing; text only (89cae5f) - VERIFIED

`run-tests.ts` L159 `if (trusted?.runsPreviewEditing)`. `git diff -U0 B HEAD --
test/integration/previewEditing.test.ts`: the two strings (L987, L1312) only.
`git diff -U0 B HEAD -- test/integration | grep` of changed `assert` lines: one removed and one
added, both `assert.equal(vscode.workspace.isTrusted, true);`. Artifacts: E1b.

### S5 budget comment replaced; no deadline, budget or time limit changed (89cae5f) - VERIFIED

`git diff -U0 B HEAD -- test/shared/hangWatchdog.ts`: comment lines only, naming run
45729384181. Added lines of `git diff -U0 B HEAD` grepped for
`.skip(|DEADLINE|TIMEOUT_MS|timeout-minutes|_BUDGET|settle(|setTimeout|sleep`: no match (exit 1).
`git diff --quiet B HEAD -- src requirements CHANGELOG.md .github justfile package.json`: exit 0.

### S6 unit test of the split (89cae5f) - VERIFIED

`test/build/trustedParts.test.ts` (not `hangWatchdog.test.ts` as the specification names; same
content), run by `test:unit` (L1, L2).

### S7 moved steps take no state from real-input or preview-editing (89cae5f) - VERIFIED

Search for `theme` in `editKeys.test.ts`, `saveKey.test.ts`, `gridCardEditorBlur.test.ts` and the
new `previewEditingSchemaSteps.ts`: no match. `previewEditing.test.ts` L1242, its last theme loop
(`["white", "dark"]`), still ends on dark; `findInPreview.test.ts` L373 calls
`pinStoredWorkspaceChoices()` (`storedChoices.ts` unchanged by the base). Both heavy runs pass the
moved steps (E4).

### S8 frames filtered by URL before any other call; 10 s bound; no sleep or retry (89cae5f) - VERIFIED

`harness.ts` L137 `scanWebviewFrames(page.frames(), ...)`, L232-235 failure dump skips by
`frameUrlSkipReason`; `openAtLine.test.ts` L119 `webviewFrames(page.frames())`; L166
`FRAME_CALL_TIMEOUT_MS = 10_000`; no new sleep or retry (S5 grep). Unit tests 6 to 8 (L2).

### S9 a timed-out wait lists the frames (89cae5f, unit test and code, not a real window) - VERIFIED

`harness.ts` L61, L73, L139; unit test 9 passes (L2). No heavy run at the head produced such a
timeout (E1).

### S10 URL shape seen in a real window - VERIFIED, carried from b24d3bf

Reason: the evidence is the archived real-window record of an earlier CR (content frame
`vscode-webview://.../fake.html`); the move changes neither `harness.ts` nor `webviewFrames.ts`
nor anything under `src`. At the head the filtered lookup again found the frame in both runs (E1).

### S11 CONTRIBUTING and requirements (89cae5f) - VERIFIED

`git diff B HEAD -- CONTRIBUTING.md`: the two launches, their steps, `TRUSTED LAUNCH`, the dump
folder name. No file under `requirements/` differs from `B` (S5); requirements checks pass (L1).

## CI evidence

### E1 two heavy runs on the head, every run job green (89cae5f) - VERIFIED

`gh run view <run> R --json headSha,event,attempt,conclusion,createdAt,jobs`:

- 45794678556: `89cae5ff...`, workflow_dispatch, attempt 1, success, created 09:43:53Z;
  static, static-windows, viewer-graph, visual, integration, stress, report, checks, gallery
  success; release-check, toc-loop, tag-release, release, pages skipped.
- 45795351595: same head, attempt 1, success, created 09:48:12Z (4 min 19 s later); same jobs.
  Its integration job ran 09:51:18 to 10:07:55, the first run's 09:49:04 to 10:08:07.

`gh run list R --branch <CR branch>`: no other run at this head than these two and the PR run
45781010549; five `workflow_dispatch` runs on the branch in all (45729384181, 45734265223,
45734267839 and these two), all attempt 1.
`python -I work/verifier/verify_runs_89cae5f.py S` (job logs under `S/artifacts-<run>/`): in the
four integration and stress logs, 0 lines matching `STEP failed|LAUNCH TIMEOUT|LAUNCH
HANG|Timed out waiting|Studio frame lookup`.

### E1b artifacts of both runs (89cae5f) - VERIFIED

`gh run download <run> R --name e2e-integration-attempt-1`, files read: both
`integration-manifest.json` `status passed`, scope `all`, revision `89cae5ff...`, dirty false;
both `FRONTMATTER-LATEST.md` `Suite: **passed**`; both frontmatter manifests `suiteResult:
passed`, result naming `trusted-suite.js part 2/2`; `hang-dumps/` holds `post-step` only.

### E2 each part at most 600 s, step under 1200 s, both runs (89cae5f) - VERIFIED

Parts: the script of E1 (`STEP start: setup` to the last `STEP done` of the part). Step:
`gh api repos/gsemet/markdown-okf-schema-studio/actions/jobs/<job>`, the `just ci-integration`
step.

```text
45794678556  part 1 09:52:10.143 -> 09:59:13.957 = 423.8 s (53 done)
             part 2 09:59:18.308 -> 10:07:31.828 = 493.5 s (4 done)
             real-input 454306 ms, open-at-line-probe 180988 ms, preview-editing 37450 ms
             step 09:49:30Z -> 10:08:02Z = 1112 s
45795351595  part 1 09:54:01.177 -> 10:00:28.300 = 387.1 s (53 done)
             part 2 10:00:31.128 -> 10:07:30.489 = 419.4 s (4 done)
             real-input 386851 ms, open-at-line-probe 177177 ms, preview-editing 31275 ms
             step 09:51:40Z -> 10:07:49Z = 969 s
```

### E3 rows of the older runs in the description's table - VERIFIED, carried from b24d3bf

Reason: they are measurements of past runs (45476952370, 45713440510, 45729384181, 45734265223,
45734267839), which the move does not change. They are not proofs of the head.

### E4 launch names and step list (89cae5f) - VERIFIED

Both runs print `TRUSTED LAUNCH: trusted-suite.js part 1/2` then `part 2/2`. Script output, both
runs: `part1 53 == reference without real-input/preview-editing, in order: True` (reference: run
45476952370, 55 names), `part2 ['setup', 'preview-smoke', 'real-input', 'preview-editing']`,
`union == reference: True; in both: ['preview-smoke', 'setup']`.

### E5 stress is one launch and green (89cae5f) - VERIFIED

Both stress logs: one line `TRUSTED LAUNCH: trusted-suite.js`, 3 trusted steps done,
`real-input` 813652 ms and 794682 ms, 0 failure lines.

### E6 open-at-line passes (89cae5f); the attempt-2 statement (carried from b24d3bf) - VERIFIED

Runs 45794678556 / 45795351595: `open-at-line` 22488 / 21060 ms, probe 180988 / 177177 ms,
studio 16973 / 15907 ms, done. The statement on run 45706313890 attempt 2 (the failed line, the
artifact content, `code: -3` in passing runs) is carried: past run at `1f209e1`, untouched by
the move.

## PR description

Posted text: `gh pr view 529 R --json body` equals `work/pr-body.md` (only a trailing newline
differs in `git diff --no-index --ignore-space-at-eol`); GraphQL `lastEditedAt`
2026-11-26T02:19:12Z, before the move. Head `89cae5f`, base `B`, open, draft.

### D1 renders cleanly (89cae5f) - VERIFIED

`gh api .../pulls/529 -H "Accept: application/vnd.github.full+json" --jq ...`: `h2` 9, `h3` 1,
tables 1, rows 6, `pre` 2, checkboxes 8, `details` 0, literal `**` 0. Mermaid parse carried from
`b24d3bf`: the text did not change.

### D2 no image shows a user name or home folder (89cae5f) - VERIFIED

Same command: `img` 0, markdown images 0, user name or home paths 0.

### D3 role names and internal references (89cae5f) - VERIFIED

Same command: `STALE|UNVERIFIED` 0; lines naming a role or `CR-<n>`: only
`CR-509 heavy-ci-trusted-suite-timeout.` (Internal references).

### D4 Summary and Deliverables (89cae5f) - VERIFIED, except the proofs' SHAs

Mermaid, 53 and 4 steps, 55 names, code sketch and frame list: S1, S2, S8, S9, E4. The table's
after rows name `5e7b4a3` and `b24d3bf`, which are not in the head's history, and no row gives the
head's runs (E2): to rewrite (brief: not counted as a failure on its own).

### D5 Changes match the diff (89cae5f) - VERIFIED

`git diff --stat B HEAD`: the same 12 files (536+, 158-), each covered by Changes and the Test
plan; checks S3 to S5. `git grep STUDIO_REAL_INPUT_SCENARIO HEAD`: `justfile` L404
(`ci-stress`) and L422 (`ci-toc-loop`), `performanceProbe.ts` L3; `trustedParts.ts` L43 and L84
keep such a run one launch with no part.

### D6 Impacts, Blast radius, Autonomous decisions (89cae5f) - NOT VERIFIED

Hold: Impacts, Blast radius, and the other decisions (S5, S7, S8; `git grep "^\s*concurrency:"
HEAD -- .github`: `release.yml` only). Contiguous split: `edit-keys` start to
`workspace-disposal` done is 132.6 s and 111.6 s in the head's runs, so part 2 would be 626 s and
531 s; with the earlier 637, 624, 579 s, "over 600 s on a slower runner" still holds.
False at the head:

1. "The two proof runs were started at the same time on one commit rather than one after the
   other": the head's runs were created 4 min 19 s apart (09:43:53Z, 09:48:12Z) and overlapped
   (E1).
2. "The visual job cancelled in one proof run was not run again: the proof of this change rests on
   the integration and stress jobs, green in both runs": no job was cancelled in the head's proof
   runs; visual is green in both (E1). It is true only of run 45734267839 at an old commit.

### D7 "What the failed frame lookup showed" - VERIFIED, carried from b24d3bf

Reason: it describes run 45706313890 and an earlier window run, which the move does not touch. As
at `b24d3bf`, the target-list sentence rests on the `verify-cdp.py` output recorded in
`S/verify-r3.md`; a later re-run of that script was refused then ("Reason: [Undermining
Oversight]"). It was not run again in this pass, nor were those lists read by other means.

### D8 Known gaps (89cae5f) - NOT VERIFIED

False at the head:

1. "it took 1056 to 1128 s on the three heavy runs of this change, 6 to 12 % under": there are
   five heavy runs; they took 969 to 1128 s, 6 to 19 % under 1200 s (E1, E2).
2. "was cancelled at that limit in one of the two proof runs": visual passed in both proof runs of
   the head (820 s and 825 s); the cancel was in run 45734267839, at an old commit.

Hold: the visual job is still near its limit (879 s of 900 s in PR run 45781010549,
`gh api .../runs/45781010549/jobs`; 885 s on main run 45713440510, carried); frame lookup not
proven fixed; longer timeout message not seen in a real run (E1: no match in the two new runs;
older runs carried); unfiltered scans (`git grep -n "page.frames()" HEAD -- test`: the ten files
the bullet lists; `openAtLine`, `harness` and `workbenchFocusDump` filter by URL); no local
real-window run (L1, preflight L5880).

### D9 Test plan (89cae5f) - stale, to rewrite

Every proof names `b24d3bf`. Each claim has a proof at the head (see below); "run 45734267839 is
not green as a whole" and "unit tests 5307 passed" do not describe the head. "Changelog: no
user-facing change" holds (S5). Not counted as a failure on its own (brief).

### D10 Review box (89cae5f)

`$CHANTIER log CR-509`: `2026-11-26T09:45:37Z driver note note=move b24d3bf..89cae5f (restack)
inspector approved at 89cae5ff42f6dfc34590b06c3f979f5a3cbce6d4`. So `Review: approved at
89cae5f` is proven; the posted box still says `b24d3bf`.

## Facts at 89cae5f for the new description

Table rows (setup step to last step; whole `just ci-integration` step):

| Heavy run | Commit | Single launch | Part 1 | Part 2 | `real-input` | probe | Step |
| --- | --- | --- | --- | --- | --- | --- | --- |
| After: 45794678556 | `89cae5f` | none | 424 s | 493.5 s | 454 s | 181 s | 1112 s |
| After: 45795351595 | `89cae5f` | none | 387 s | 419 s | 387 s | 177 s | 969 s |

The rows of `5e7b4a3` and `b24d3bf` can be removed (the specification asks the two proof runs); if
kept, they are marked as earlier commits, not proofs of the head. Optional extra "before" at the
new base: main push run 45773405420 (`3478f09`, success): one launch, 55 steps, 852 s (setup to
`workspace-disposal`), `real-input` 415 s, probe 178 s, step 1023 s.

- Margin (Known gaps): 969 and 1112 s at the head (19 % and 7 % under 1200 s); 969 to 1128 s over
  all five heavy runs (6 to 19 % under).
- Visual (Known gaps): 820 s (45794678556), 825 s (45795351595), 879 s (45781010549) of 900 s at
  the head, all passed; the one cancel at the limit was heavy run 45734267839, on an earlier
  commit; 885 s on main run 45713440510.
- Autonomous decisions: the two proof runs were started about four minutes apart on one commit
  and ran at the same time; the sentence on the cancelled visual job must name the earlier run
  45734267839 as such, or go.
- Test plan, new tests at `89cae5f`: 9 fail against the stand-ins, 9 pass.
- Requirements at `89cae5f`: `okfreq validate` 1228 requirements, 0 errors (26 warnings), 0
  indexes and 0 files would change.
- Local gates at `89cae5f`: `just preflight` on Windows, static stage only, passed; unit tests
  5335: 5327 passed, 8 skipped, none failed.
- Heavy CI at `89cae5f`: 45794678556 and 45795351595, attempt 1 each, every job that ran green
  (release-check, toc-loop, pages, tag-release and release skipped), `integration` and `stress`
  green, each part under 600 s.
- Review: approved at `89cae5f`. CI green at `89cae5f`: static, static on Windows, visual,
  viewer-graph, report and checks of PR run 45781010549; integration and stress skipped there.
- "Verified": tick only after a description pass records VERIFIED at this head.

Carried from `b24d3bf`: S10, E3, D7, the attempt-2 part of E6, the Mermaid parse. Every other
claim above was judged again, because the base changed what its proof runs or a new run at the
head replaces the old one.

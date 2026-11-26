# CR-509 verification

Head: 89cae5ff42f6dfc34590b06c3f979f5a3cbce6d4

Verdict: **VERIFIED**. The change and its proofs hold at `89cae5f` (M0 to E6, judged in the
previous pass at this head and kept as written). The rewritten description, posted
2026-11-26T10:52:48Z, holds at the same head and base (N0 to N7); the former `NOT VERIFIED`
was on the former description text only.

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

## PR description (description-only pass, 89cae5f)

Same head and base as the pass above. Only the text changed, so the sections above this one are
that pass's judgments, kept as written (their `NOT VERIFIED` marks were on the former text: D4 to
D10 and "Facts at 89cae5f for the new description", replaced by this section; they failed D6 and
D8, and D4 and D9 were stale). `V` = `work/verifier`.

### N0 nothing but the description changed (89cae5f) - VERIFIED

`git rev-parse HEAD origin/main`: `89cae5ff42f6dfc34590b06c3f979f5a3cbce6d4`,
`3478f0992688c7a354d11106145793fc83590506`; `git status --porcelain`: nothing; `git diff --stat
3478f09 HEAD`: `12 files changed, 536 insertions(+), 158 deletions(-)`. `gh pr view 529`:
`headRefOid 89cae5f`, `baseRefOid 3478f09`, base `main`, open, draft, `CLEAN`, title `ci: split
the trusted VS Code launch and filter frame lookups`. `gh run list --branch <CR branch>`: at this
head only 45781010549 (pull_request), 45794678556 and 45795351595 (workflow_dispatch), all
attempt 1, success; no run dispatched or re-run since. `gh pr checks 529`: exit 0.

### N1 posted text, and what changed in it (89cae5f) - VERIFIED

`python -I V/verify_body_diff.py S/verify-pr529-r4.json work/pr-body.md S/verify-pr529-desc89.json`:
`posted == work/pr-body.md: True`; `updatedAt 2026-11-26T10:52:48Z`. GraphQL `lastEditedAt` is the
same time. `git diff --no-index -U0` between the body GraphQL records for the edit of 02:19:12Z
(`S/pr529-body-021912.md`) and `work/pr-body.md`: hunks only in three table rows, two Autonomous
decisions bullets, the first two Known gaps bullets, and the Test plan boxes (tests, requirements,
local gates, heavy CI, review, Verified now unchecked, CI green). Every other line is unchanged.

### N2 renders cleanly, no image, no user name (89cae5f) - VERIFIED

`python -I V/verify_desc_render.py 3478f09...`: `h2 9`, `h3 1`, `table 1`, `tr 6`, `pre 2`,
`details 0`, `img 0`, `checkboxes 8`, `literal ** in html 0`, markdown images 0; `user name hits
0`, `home path hits 0`; `STALE|UNVERIFIED 0`; the one line matching a role name or `CR-<n>` is
L178 under `## Internal references`. Commit ids in the body: `17b779d`, `3478f09`, `63ef752` are
ancestors of the base ("before" rows), `89cae5f` is the head. Mermaid parse carried from b24d3bf:
the diagram is outside the changed hunks (N1).

### N3 durations table (89cae5f) - VERIFIED

`python -I V/verify_desc_jobs.py <runs>` (`gh api .../runs/<run>` and `/jobs`), `just
ci-integration` step: 45476952370 (`63ef752`, push main) 1011 s; 45713440510 (`17b779d`, push
main) 1002 s; 45773405420 (`3478f09`, push main, success) 1023 s; 45794678556 (`89cae5f`) 1112 s;
45795351595 (`89cae5f`) 969 s. Row 45773405420, Grep of
`S/artifacts-45773405420/integration.log`: one `STEP start: setup` at 07:13:53.803 (L666),
`open-at-line-probe (178214 ms)`, `real-input (415004 ms)`, `STEP done: workspace-disposal` at
07:28:05.609 (L2703): 851.8 s, as 852, 415, 178. The two after rows equal E2 (423.8 / 493.5 /
454306 / 180988 and 387.1 / 419.4 / 386851 / 177177). The two older before rows: E3.

### N4 Autonomous decisions (89cae5f) - VERIFIED

Runs 45794678556 and 45795351595 created 09:43:53Z and 09:48:12Z (4 min 19 s), updated 10:12:12Z
and 10:11:09Z: concurrent. Run 45734267839 (`b24d3bf`, earlier commit): attempt 1, `visual`
cancelled, job 925 s, annotation `The job has exceeded the maximum execution time of 15m0s`;
`integration` and `stress` success; no second attempt and no other dispatch at `b24d3bf` than
45734265223. The concurrency statement and the other decisions are unchanged text, held above
(former D6).

### N5 Known gaps (89cae5f) - VERIFIED

- Integration step: five `workflow_dispatch` runs exist on the branch (`gh run list`), steps 1128 s
  (45729384181, `5e7b4a3`), 1111 s and 1056 s (45734265223, 45734267839, `b24d3bf`), 1112 s and
  969 s (head): 969 to 1128 s, two at the head and three earlier, 6.0 % to 19.25 % under 1200 s
  (`ci.yml` L295 `timeout-minutes: 20`).
- Visual job (`ci.yml` L131 `timeout-minutes: 15`): 820 s and 825 s (proof runs), 879 s
  (45781010549, the pull request's run at the head), 885 s (45713440510, main), all success;
  cancelled at the limit in 45734267839 (N4).
- Completeness: `V/evidence/before-after.md` "Not captured" lists a local real-window run (fifth
  bullet), proof that the frame failure is gone (third bullet) and the frame list in a real timeout
  message (third bullet). No `UNVERIFIED` claim and no failed claim accepted unfixed. The CI
  rules' repetition proof (log anomaly) is in the third bullet. The last three bullets are
  unchanged text, held above (former D8).

### N6 Test plan (89cae5f) - VERIFIED

- 9 new tests: L2. They are in the `test:unit` glob (`out/test/{build,...}`, `package.json` L465),
  and `G/preflight-89cae5f.log` (first line names the CR and the full head) has `tests 5335, pass
  5327, fail 0, skipped 8` (L5620-5625).
- Requirements: same log, L5783 `okfreq validate` / L5784 `1228 requirements, 0 errors`, L5811
  `okfreq lint ... --check` / L5838 `0 indexes would change`, L5840 `okfreq update-coverage ...
  --check` / L5841 `0 files would change`. Changelog: S5.
- Local gates: L5879 `ci-static: passed`, L5880 `preflight: visual, viewer-graph, integration,
  report and gallery stages skipped on Windows; CI runs them`.
- Heavy CI: both runs attempt 1, success; every job success except `release-check`, `toc-loop`,
  `tag-release`, `release`, `pages` skipped (N3 command); parts under 600 s: E2.
- Review: `$CHANTIER log CR-509`: `2026-11-26T09:45:37Z driver note note=move b24d3bf..89cae5f
  (restack) inspector approved at 89cae5ff42f6dfc34590b06c3f979f5a3cbce6d4`.
- CI green: 45781010549 (pull_request, `89cae5f`): static, static-windows, visual, viewer-graph,
  report, checks success; integration and stress skipped.
- `Verified` is unchecked, as intended until this verdict is recorded.

### N7 the unchanged sections (carried from the pass above, same head)

Summary, Deliverables (former D4, apart from the rows judged in N3), Changes (D5), Impacts and
Blast radius (D6), "What the failed frame lookup showed" (D7, itself carried from b24d3bf with the
limit it records on the refused re-run): N1 shows their text did not change.

## Notes for the Driver

- Ticking `Verified` is the only body change this verdict expects; name `89cae5f` in the box.
- Not a failure: the Summary's "about 92 %" matches the runs of 834 and 831 s; the added base row
  (852 s) is 95 %.
- Not part of the description: the record's `gaps` note (`$CHANTIER handoff`) still gives the
  former figures (1056 to 1128 s, three runs, cancel in a proof run); a new hand-back should use the
  figures of the posted Known gaps.
- Long gate: none configured; `handoff` shows it unchecked, with the project's `--no-gate` path.
- No command was refused in this pass.

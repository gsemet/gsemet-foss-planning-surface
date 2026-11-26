# CR-509 verification

Head: b24d3bf08f01ae0e72fe7d251b25833df558608c

Verdict: **NOT VERIFIED**. The code and the CI proof do what the specification says. Two claims
about the posted PR description fail (D5 and D7).

Notation: `W` = the CR worktree (every command runs there unless said), `S` = `work/scratch`,
`R` = `--repo gsemet/markdown-okf-schema-studio`, `B` = base
`5a73b6ebcf66ef80b412afcdbfd09c4defc028d8`. "SHA" is the commit a claim was judged at; `b24d3bf` is
the head. `git status --short` printed nothing after the checks. Before and after:
`work/verifier/evidence/before-after.md`.

Long gate: none is configured (`ls W/chantier.yaml`: no such file, so no
`long_gate.commands`). The `ship` events say `no long gate passed at b24d3bf`; there is no gate log
to cite. `work/gates/r3-check.log` is not a chantier gate log. The local checks were run directly.

## Local checks

### L1 `just preflight` static stage passes at the head (b24d3bf) - VERIFIED

Every part of `ci-static` (justfile) run directly, all exit 0:
`just check-no-merge-commits`, `compile`, `check-min-vscode`, `check-boundaries`, `check-limits`,
`check-exports`, `check-markers`, `check-settings`, `clip-kit-test`, `contracts`, `security`
(107 pass), `release-notes-check`, `release-tests` (`205 passed`), `requirements-lint`, `audit`
(`found 0 vulnerabilities`), `sphinx-check` (`4 passed`), `just --unstable --fmt --check`.
`npm run test:unit`: `tests 5315, pass 5308, fail 0, skipped 7`.
`just requirements-report` hit my own 120 s limit in its last line; that line alone,
`okfreq status requirements`, then exit 0 with `"errors": 0` (the report had been generated).
`contracts` runs 0 tests, here and in the preflight log (no `*.contract.ts` file is tracked).

### L2 the 9 new tests pass at the head and fail on the old behaviour (b24d3bf) - VERIFIED

`node --test out/test/build/trustedParts.test.js out/test/build/webviewFrames.test.js`:
`tests 9, pass 9, fail 0`. Same two files from a throwaway copy `out/verify-red-test` after
`python -I S/verify-red-standins.py out/verify-red-test` (single launch, no URL filter, no frame
list, no dump label): `tests 9, pass 0, fail 9`, each an `AssertionError`. Copy removed.

### L3 files stay under 1500 lines (b24d3bf) - VERIFIED

`wc -l`: `trusted-suite.ts` 328, `run-tests.ts` 293, `harness.ts` 827.

## Specification, "What changes"

### S1 two launches with the stated steps and order (b24d3bf) - VERIFIED

`test/shared/trustedParts.ts`: part 1 = `setup` ... `find-in-preview`, `edit-keys` ...
`workspace-disposal` (53); part 2 = `setup`, `preview-smoke`, `real-input`, `preview-editing`.
Test 1 compares them with the 55 names; `python -I` over `git show B:test/integration/trusted-suite.ts`
gave the same 55 names in the base's full-run order. CI logs agree (E4).

### S2 each part has its own window, port, heartbeat, launch name, suite label (b24d3bf) - VERIFIED

`git grep` in `run-tests.ts`: L242 `for (const launch of trustedLaunches(process.env)) await
runScenario(...)`; per call `mkdtempSync` (L100), `freePort()` (L121),
`heartbeatFileFor(instanceId, trusted?.suite ?? suiteName)` (L119), `name: trusted?.name,
dumpLabel` (L138), `STUDIO_TRUSTED_PART` (L150). `trusted-suite.ts` L73-74:
``console.log(`TRUSTED LAUNCH: ${launch.name}`)``, `withSuiteWatchdog(launch.suite, ...)`.

### S3 selection variable, scenario runs one launch, order and scope unchanged (b24d3bf) - VERIFIED

Tests 2 to 4 (L2) pass: unknown or missing value throws; a scenario gives one launch with no part.
`git diff B..HEAD -- test/integration/run-tests.ts`: order scroll-sync, untrusted, part 1, part 2,
standalone, reverse-migration, reload; `--trusted-only` runs both; manifest `scope` code kept.
Stress logs show one launch (E5).

### S4 frontmatter block after the part that runs preview-editing; text only (b24d3bf) - VERIFIED

L159 `if (trusted?.runsPreviewEditing)`; the `previewEditing.test.ts` diff changes the two strings
only. `git diff -U0 B..HEAD -- test/integration`, removed against added `assert` lines: one,
`assert.equal(vscode.workspace.isTrusted, true);`, on both sides (L223 at B, L323 at head).
Artifacts: E1b.

### S5 budget comment replaced; no deadline, budget or time limit changed (b24d3bf) - VERIFIED

`git diff B..HEAD -- test/shared/hangWatchdog.ts`: comment lines only, now "part 1 428 s ... part 2
502.5 s ... `real-input` 462 s and `preview-editing` 39 s" of run 45729384181 (matches E2 output).
`git diff -U0 B..HEAD` grep of added lines for
`.skip(|DEADLINE|TIMEOUT_MS|timeout-minutes|_BUDGET|settle(|setTimeout|sleep`: no match;
`git diff --quiet B HEAD -- src requirements CHANGELOG.md .github justfile package.json`: exit 0.

### S6 unit test of the split (b24d3bf) - VERIFIED

The checks are in `test/build/trustedParts.test.ts`, not `hangWatchdog.test.ts` as the
specification names; same content (55 names once, distinct heartbeat and launch names), run by
`test:unit` (`out/test/build/**`).

### S7 moved steps take no state from real-input or preview-editing (b24d3bf) - VERIFIED

`grep -ci theme` on `editKeys.test.ts`, `saveKey.test.ts`, `gridCardEditorBlur.test.ts`: 0, 0, 0.
`previewEditing.test.ts` L1428-1431 ends its `["white","dark"]` loop on dark;
`findInPreview.test.ts` L371 restores the stored workspace choices (theme `current`). Both proof
runs pass these steps (E4).

### S8 frames filtered by URL before any other call; 10 s bound; no sleep or retry (b24d3bf) - VERIFIED

`harness.ts` diff: `findCurrentFrame` goes through `scanWebviewFrames` (only `url()` on a skipped
frame, test 7); the failure dump and `openAtLine.test.ts` L119 filter too;
`FRAME_CALL_TIMEOUT_MS = 10_000` (L166) unchanged; no new sleep or retry (grep of S5).

### S9 a timed-out wait lists the frames (b24d3bf) - VERIFIED (unit test and code, not a real window)

`waitFor` appends `frameLookups.describeSince(mark)`; `findCurrentFrame` records every scan; test 9
passes. No run at the head produced such a timeout.

### S10 URL shape checked in a real window (b24d3bf) - VERIFIED

Archived CR-453 `forced-failure.md` L3 and L6 ("real VS Code 1.147.0 window, Windows") shows the
content frame `vscode-webview://.../fake.html?id=...`. In both proof runs the filtered lookup found
the Studio frame: no `STEP failed` (E1).

### S11 CONTRIBUTING and requirements (b24d3bf) - VERIFIED

`git diff B..HEAD -- CONTRIBUTING.md`: two launches, their steps, `TRUSTED LAUNCH`, dump folder
`<time>-trusted-part-<n>-<step>/`. No file under `requirements/` changed (S5). `@tests_req`
markers present in `trusted-suite.ts` at B and head. `just requirements-lint`: `1227 requirements,
0 errors`, `0 indexes would change`, `0 files would change`.

## CI evidence

### E1 two heavy runs on the head, integration and stress green (b24d3bf) - VERIFIED

`gh run view <run> R --json headSha,event,attempt,conclusion,jobs`:

- 45734265223: `b24d3bf`, workflow_dispatch, attempt 1, success; integration, stress, visual,
  static, static-windows, viewer-graph, report, checks, gallery success.
- 45734267839: `b24d3bf`, attempt 1, **cancelled**; integration, stress, static, static-windows,
  viewer-graph success; visual cancelled (01:13:31 to 01:28:56); report and checks failure.

`gh api .../check-runs/139623587012/annotations`: `The job has exceeded the maximum execution time
of 15m0s`. The report log says `FAILED visual: visual manifest is missing`, `ok integration`; so
report and checks follow from the cancel. The specification asks integration and stress green, so
the cancel does not break the proof. `gh run list --branch <CR branch>`: no other heavy run at this
head, no re-run. The two were dispatched together (stated in the description). `just ci-visual` runs `test:visual` and
`test:breakout`; `git grep` for the changed modules in `test/visual`, `test/site`, `scripts` and
`package.json`: no match. Main's visual job took 885 s of 900 (run 45713440510, `17b779d`).

`python -I S/verify-artifacts.py S`, both runs: integration log, 0 `STEP failed` / `LAUNCH
TIMEOUT` / `LAUNCH HANG` lines.

### E1b artifacts of both runs (b24d3bf) - VERIFIED

Same script: `integration-manifest.json` `passed`, scope `all`, revision `b24d3bf...`, dirty false;
`FRONTMATTER-LATEST.md` `Suite: **passed**`; frontmatter manifest `suiteResult: passed`, result
naming `part 2/2`; only `hang-dumps/post-step`.

### E2 each part at most 600 s, step under 1200 s, both runs (b24d3bf) - VERIFIED

`python -I S/verify-parse.py` and `gh api .../actions/runs/<run>/jobs`:

| Run | Commit | Part 1 | Part 2 | real-input | probe | Step |
| --- | --- | --- | --- | --- | --- | --- |
| 45734265223 | b24d3bf | 421.6 s | 492.7 s | 452.3 s | 180.9 s | 1111 s |
| 45734267839 | b24d3bf | 408.9 s | 453.3 s | 418.3 s | 178.7 s | 1056 s |
| 45729384181 | 5e7b4a3 | 428.0 s | 502.5 s | 462.0 s | 181.7 s | 1128 s |
| 45476952370 | 63ef752 | one launch 834.4 s | - | 403.9 s | 178.1 s | 1011 s |
| 45713440510 | 17b779d | one launch 830.5 s | - | 405.4 s | 177.8 s | 1002 s |

### E3 table of the description matches the logs (b24d3bf) - VERIFIED

Every cell equals the table above after rounding. The `5e7b4a3` row names its own commit;
`git diff -U0 5e7b4a35 b24d3bf0` changes comment lines only (3 files).

### E4 launch names and step list (b24d3bf) - VERIFIED

Both runs print `TRUSTED LAUNCH: trusted-suite.js part 1/2` and `part 2/2` (the launch name is in
this line, not in each `STEP` line). Parse script: part 1 (53) equals run 45476952370 without
`real-input` and `preview-editing`, in order: True; part 2 the four names; union equals the 55:
True; in both: `preview-smoke`, `setup`.

### E5 stress is one launch and green (b24d3bf) - VERIFIED

`stress.log` of both runs: `['TRUSTED LAUNCH: trusted-suite.js']`, `setup`, `preview-smoke`,
`real-input` (821984 ms, 884093 ms), `untrusted-suite` done; 0 failure lines.

### E6 open-at-line passes; the attempt-2 statement (b24d3bf; run 45706313890 at 1f209e1) - VERIFIED

Proof runs: `open-at-line` done 22162 ms and 21912 ms, probe and studio done. Attempt-2 job log
L685 `STEP failed: open-at-line (12624 ms): TIMEOUT: locator.count did not return within 10000 ms
(frame )`; artifact (30 files): integration manifest, campaign file, `hang-dumps/post-step`,
screenshot indexes and the screenshots of the scroll and untrusted launches; no in-window dump.
`code: -3` lines in passing runs: 13, 16, 27, 22.

## PR description

Posted text: `gh pr view 529 R --json headRefOid,state,isDraft,body`: head `b24d3bf...`, OPEN,
draft; body equals `work/pr-body.md` (`True`).

### D1 renders cleanly (b24d3bf) - VERIFIED

`gh api .../pulls/529` with `Accept: application/vnd.github.full+json`, `body_html`: 9 `h2`, 1
`h3`, 1 table of 6 rows, 2 code blocks, 8 task boxes, no literal `**`. The Mermaid block parses
with the project's Mermaid (`flowchart-v2`). Sections follow the project template, which has no
fold.

### D2 no image shows a user name or home folder (b24d3bf) - VERIFIED

No `![` in the body, no `img` in `body_html`.

### D3 role names and internal references (b24d3bf) - VERIFIED

Lines naming `verifier|driver|coder|inspector|cr-`: only `CR-509 ...` under Internal references.

### D4 Summary and Deliverables (b24d3bf) - VERIFIED

Backed by S1, S2, S8, S9, E2, E3; "about 92 %" = 830.5/900 and 834.4/900.

### D5 Changes match the diff, no delivered change unmentioned (b24d3bf) - NOT VERIFIED

`git diff --stat B..HEAD` lists `test/shared/hangWatchdog.ts | 7 +-`: the `STEP_BUDGETS_MS` comment
was rewritten to record the measured durations of the two launches (specification, "What changes" 1;
the subject of commit `b24d3bf`). Summary, Deliverables and Changes do not mention it: a search of
the body for `hangwatchdog|comment|step_budgets|budget` finds only "No deadline, step budget or
`timeout-minutes` value changes" and "no deadline, budget or time limit is raised". The other
changed files are covered (Changes, Test plan).

### D6 Impacts, Blast radius, Autonomous decisions (b24d3bf) - VERIFIED

Backed by S2 (one more window), S5 (no limit raised, no skip, no shipped file), S7 (theme), E1
(runs together, no re-run; `grep concurrency .github/workflows/ci.yml`: no match). Contiguous
split from the E2 logs (tail 134.9, 131.5, 125.3 s added to part 2): 637, 624, 579 s, over 600 on
two of three runs. 300 s against the specification's 76 s spread.

### D7 "What the failed frame lookup showed" (b24d3bf) - NOT VERIFIED

The text says the browser target lists of the two timed-out launches "hold only webview service
workers". `python -I S/verify-cdp.py S/verify-45706313890`: each of the two `cdp-targets.json`
(`...-diff-preview-scroll`, `...-side-preview-jump`) holds

- 1 `page` `vscode-file://vscode-app/...`
- 2 `service_worker` `vscode-webview://...`
- 2 `worker` `blob:vscode-file://...`

So the lists do not hold only webview service workers. The true narrower fact is that their only
`vscode-webview://` targets are service workers (no content frame); the conclusion drawn from it
stands. The rest of the section is verified (E6, S10).

### D8 Known gaps (b24d3bf) - VERIFIED

Margin: 1056 to 1128 s, 6 to 12 % under 1200, two follow-ups; visual job 885 s (E1); frame lookup
not proven fixed, no stress scenario; no local real-window run. `git grep "page.frames()" HEAD --
test`: the unfiltered scans are those listed. The three "Not captured" items of `before-after.md`
fall under the real-window and frame-lookup bullets (the second does not say in words that the new
timeout message has not been seen in a real run).

### D9 Test plan (b24d3bf) - VERIFIED

New tests: L2. Requirements: S11. Changelog: `CHANGELOG.md` unchanged, no `src/` change (S5).
Local gates "5307 passed, 8 skipped, none failed": `S/preflight-b24d3bf.log` shows `tests 5315,
pass 5307, fail 0, skipped 8`, `ci-static: passed`; L1 repeats it (one more test ran here: it skips
when no requirements report exists). Heavy CI: E1, E2. CI green: `gh pr checks 529 R` (run
45734227734): static, static-windows, visual, viewer-graph, report, checks `pass`; integration,
stress `skipping`. "Verified" is unchecked.

### D10 Review box (b24d3bf) - VERIFIED

`$CHANTIER log CR-509`: `2026-11-26T01:06:08Z driver note note=r3 approved at 5e7b4a3..., committed
as b24d3bf08f01ae0e72fe7d251b25833df558608c`.

## To pass

1. Mention the `STEP_BUDGETS_MS` comment update (`test/shared/hangWatchdog.ts`) in Changes.
2. Narrow the target-list sentence, for example "their only `vscode-webview://` targets are service
   workers".

Both are description-only edits; no code change or new CI run is needed for them.

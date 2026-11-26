# CR-509 verification

Head: b24d3bf08f01ae0e72fe7d251b25833df558608c

Verdict: **VERIFIED**. The code and the CI proof do what the specification says, and the posted
PR description, as now posted, passes (D1 to D11; D11 is the last pass, on the edit that ticked
the "Verified" box). D7 rests on the target list output recorded at this
head by the earlier pass: running it again was refused (see D7).

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

Judged by the description-only pass at `b24d3bf`, after the description was edited and reposted
(`updatedAt` 2026-11-26T02:14:07Z). No code moved, so L1 to E6 above are kept as judged at
`b24d3bf`. The earlier file, with the two failures (D5, D7), is `S/verify-r3.md`.
`V` = `work/verifier`, `L` = the integration and stress job logs under `S`.

### D0 what is judged, and what changed (b24d3bf)

`python -I V/verify_body_diff.py S/verify-pr529.json work/pr-body.md S/verify-pr529-r4.json`:

```text
head b24d3bf08f01ae0e72fe7d251b25833df558608c OPEN draft True 2026-11-26T02:14:07Z
posted == work/pr-body.md: True
diff previously judged body -> posted body:
@@ -67,0 +68,2 @@
+- `test/shared/hangWatchdog.ts`: comments only; the note above the step budgets now records the
+  durations of the two launches measured on heavy run 45729384181.
@@ -83,4 +85,4 @@
-window run on Windows). On the CI runner, the browser target lists saved with the two timed-out
-launches of the same run hold only webview service workers, so they confirm the
-`vscode-webview://` scheme and not the content frame's URL. The filter therefore keeps every
-`vscode-webview://` URL.
+window run on Windows). On the CI runner, in the browser target lists saved with the two timed-out
+launches of the same run, the only `vscode-webview://` targets are service workers (the other
+targets are the workbench page and two of its own workers), so they confirm the scheme and not the
+content frame's URL. The filter therefore keeps every `vscode-webview://` URL.
@@ -143 +145,3 @@
-  message are what make a next failure explain itself.
+  message are what make a next failure explain itself. That longer timeout message has not been
+  seen in a real run: no heavy run of this change timed out while waiting for the Studio frame, and
+  only the frame list it appends has a unit test.
@@ -164,2 +168,2 @@
-      45734267839 is not green as a whole, its simulated visual job was cancelled at its time limit
-      (see Known gaps)
+      45734267839 is not green as a whole, its simulated visual job was cancelled at its time limit,
+      so its report and checks jobs failed too (see Known gaps)
```

`gh pr view 529 R --json headRefOid,updatedAt,state,isDraft` at the end of the pass: same head,
same `updatedAt`, OPEN, draft.

### D1 renders cleanly (b24d3bf) - VERIFIED

`gh api repos/gsemet/markdown-okf-schema-studio/pulls/529 -H "Accept: application/vnd.github.full+json" --jq ...`
(counts over `body_html`): head `b24d3bf...`, base `5a73b6e...`, `h2` 9, `h3` 1, tables 1, rows 6,
`pre` 2, checkboxes 8, `details` 0, literal `**` 0. Headings: Summary, Deliverables, Changes, What
the failed frame lookup showed, Impacts, Blast radius, Autonomous decisions, Known gaps, Test
plan, Internal references. The rendered HTML was read: lists, the new bullet, the table, the
Mermaid section and the code block are in place. The project template has no fold.
Mermaid parse with the project's Mermaid (`flowchart-v2`): carried from the earlier pass at
`b24d3bf`; the D0 diff does not touch the block.

### D2 no image shows a user name or home folder (b24d3bf) - VERIFIED

Same command: `img` in `body_html` 0, `![` in the body 0; matches of the user name, `C:\Users`,
`/home/` or `/Users/` in the body text 0.

### D3 role names and internal references (b24d3bf) - VERIFIED

Same command, body lines matching `verifier|driver|coder|inspector|foreman|cr-<n>|STALE|UNVERIFIED`
(any case): one, `CR-509 heavy-ci-trusted-suite-timeout.`, under Internal references. Title:
`ci: split the trusted VS Code launch and filter frame lookups`.

### D4 Summary and Deliverables (b24d3bf) - VERIFIED

`test/shared/trustedParts.ts`: part 1 = `setup`, `preview-smoke`, 13 names from `project-features`
to `find-in-preview`, then `edit-keys` to `workspace-disposal` (53); part 2 = 4. This matches the
Mermaid labels. `test/build/trustedParts.test.ts` test 1 hard-codes 55 names, compares each part in
order and counts each name once (`setup`, `preview-smoke` twice). The code sketch and "lists every
frame seen" match `test/shared/webviewFrames.ts` (`scanWebviewFrames` records one line per frame,
`FrameLookupLog.describeSince` lists the last lookup that found nothing) and the `harness.ts` diff.
Window isolation: S2. Frame filter: S8, S9. Table: E2, E3. "about 92 %" = 830.5/900, 834.4/900.
The `5e7b4a3` table row is a measurement labelled with its own commit, beside the two head rows;
`git diff -U0 5e7b4a35 b24d3bf0` changes comment lines only (E3).

### D5 Changes match the diff, no delivered change unmentioned (b24d3bf) - VERIFIED

`git diff --stat 5a73b6e..HEAD`: 12 files (CONTRIBUTING.md, 2 new `test/build` tests,
openAtLine.test.ts, previewEditing.test.ts, harness.ts, run-tests.ts, trusted-suite.ts,
hangWatchdog.ts, launchWatchdog.ts, trustedParts.ts, webviewFrames.ts). All are covered by Changes
and Test plan; `previewEditing.test.ts` (two evidence strings) by the "recorded suite result now
covers part 2 only" sentence. The file the earlier pass found missing is now listed:

- `git diff -U0 5a73b6e HEAD -- test/shared/hangWatchdog.ts | grep -E "^[+-]" | grep -vE "^[+-] \*"`
  prints only the two file header lines, so every changed line is a comment line. The new note names
  run 45729384181.
- `grep "STEP done: (setup|real-input|preview-editing|workspace-disposal)" S/verify-45729384181/integration.log`:
  part 1 `setup` done 00:38:26.043 (117 ms) to `workspace-disposal` done 00:45:33.957 = 428 s; part
  2 `setup` done 00:45:38.713 (275 ms) to `preview-editing` done 00:54:00.960 = 502.5 s;
  `real-input` 461982 ms, `preview-editing` 38638 ms.
- "no deadline, step budget or `timeout-minutes` value changes": the added lines of the whole diff
  grepped for `.skip(|DEADLINE|TIMEOUT_MS|timeout-minutes|_BUDGET|settle(|setTimeout|sleep`: no
  match (exit 1); `git diff --quiet 5a73b6e HEAD -- src requirements CHANGELOG.md .github justfile package.json`: exit 0.
- "no test assertion changes": `git diff -U0 5a73b6e HEAD -- test/integration | grep -E "^[+-][^+-].*assert"`:
  one removed and one added line, both `assert.equal(vscode.workspace.isTrusted, true);`.
- "used by `ci-stress`, `ci-toc-loop` and the probe": `justfile` L402 (`stress`) and L420
  (`toc-loop`); `test/integration/performanceProbe.ts` L3 (`probe`).

### D6 Impacts, Blast radius, Autonomous decisions (b24d3bf) - VERIFIED

Carried from the earlier pass at `b24d3bf`; the D0 diff does not touch these sections. Backed by S2
(one more window), S5 (no limit raised, no skip, no shipped file), S7 (theme), E1 (runs together,
no re-run). Contiguous split from the E2 logs (tail 134.9, 131.5, 125.3 s added to part 2): 637,
624, 579 s, over 600 on two of three runs. 300 s against the specification's 76 s spread.
Concurrency checked again: a search for `concurrency:` finds it in `.github/workflows/release.yml`
only, none in `ci.yml`.

### D7 "What the failed frame lookup showed" (b24d3bf) - VERIFIED

Target lists: judged against the command and output of the earlier pass at this same head
(`S/verify-r3.md`, D7), on the same downloaded artifacts. `python -I S/verify-cdp.py
S/verify-45706313890`: each of the two `cdp-targets.json` (`...-diff-preview-scroll`,
`...-side-preview-jump`) holds

- 1 `page` `vscode-file://vscode-app/...`
- 2 `service_worker` `vscode-webview://...`
- 2 `worker` `blob:vscode-file://...`

The posted sentence says exactly this: the only `vscode-webview://` targets are service workers;
the others are the VS Code app page (the workbench) and two workers of its origin.

This pass tried to run that command again and was refused; it was not retried, and the lists were
not read by another means. Exact text: "Permission for this action was denied by the Claude Code
auto mode classifier. Reason: [Undermining Oversight]."

The rest of the section is unchanged (D0): E6, S10.

### D8 Known gaps (b24d3bf) - VERIFIED

- New sentences: `gh run list --branch <CR branch>` shows three heavy (`workflow_dispatch`) runs,
  45729384181, 45734265223, 45734267839, plus two `pull_request` runs. A search of the integration
  and stress logs of all three for `TRUSTED LAUNCH|Timed out waiting|Studio frame lookup|STEP failed|LAUNCH TIMEOUT|LAUNCH HANG`
  matches only the `TRUSTED LAUNCH` lines (two per integration log, one per stress log). The stress
  log of 45729384181 was downloaded in this pass (`gh run view 45729384181 --job 139607303225 --log`,
  to `S/verify-r4-45729384181-stress/`). `gh api .../actions/runs/<run>/jobs`: integration and
  stress `success` in all three. The unit test of the appended list passes in the local gate log
  (`CR-509: a wait that timed out lists the frames of its own last lookup that found nothing`).
- The three "Not captured" items of `before-after.md` now each have their words: local real window,
  frame lookup not proven fixed, longer timeout message not seen in a real run.
- `git grep -n "page.frames()" HEAD -- test`: unfiltered scans in blockActionsFollowSelection,
  editToolbarCover, findInPreview, previewEditingHelpers, renderPatching, reload-suite,
  scroll-sync-suite, windowFocus, tableEmptyColumn, tallBlockScroll, all listed
  (`openAtLine` and `harness` are filtered; `workbenchFocusDump.ts` L329 filters by URL already).
- Margin 1056 to 1128 s, 6 to 12 % under 1200 (E2); visual job 885 s (E1). No claim of this file
  that failed was accepted unfixed (D5, D7 are fixed). No `UNVERIFIED` or `STALE` mark (D3).

### D9 Test plan (b24d3bf) - VERIFIED

New tests: L2; the 9 `CR-509:` tests show a pass mark in `S/preflight-b24d3bf.log` (L232-257).
Requirements: same log L5730-5788, `okfreq validate` `1227 requirements, 0 errors`, `lint --check`
`0 indexes would change`, `update-coverage --check` `0 files would change`. Changelog:
`CHANGELOG.md` unchanged (D5). Local gates: same log L5567-5572 `tests 5315, pass 5307, fail 0,
skipped 8`, L5825 `ci-static: passed`. Heavy CI: E1, E2. "so its report and checks jobs failed
too": `gh run view 45734267839 --job 139630458250 --log`: `FAILED visual: visual manifest is
missing`, `ci-report: FAILED`; job 139630737913: `RESULTS: success success cancelled success
failure`, exit 1. CI green: `gh pr checks 529 R` (run 45734227734): static, static-windows, visual,
viewer-graph, report, checks `pass`; integration, stress `skipping`. "Verified" is unchecked.

### D10 Review box (b24d3bf) - VERIFIED

`$CHANTIER log CR-509`: `2026-11-26T01:06:08Z driver note note=r3 approved at 5e7b4a3..., committed
as b24d3bf08f01ae0e72fe7d251b25833df558608c`; also `2026-11-26T02:13:56Z driver note note=r4 body
re-inspection approved at b24d3bf...`.

### D11 the "Verified" box edit, judged on the posted text (b24d3bf) - VERIFIED

Posted at `updatedAt` 2026-11-26T02:19:12Z. L1 to E6 are kept as judged at `b24d3bf` (no code
moved); no CI run was dispatched and no script was run over downloaded files.

Difference from the judged text. GitHub's edit history (`gh api graphql`,
`pullRequest(number:529){userContentEdits{editedAt diff}}`) lists 5 edits, the last two at
02:14:07Z (the text judged in D0 to D10) and 02:19:12Z (current). The `diff` of the 02:14:07Z edit
was saved to `S/verify-r5-body-judged.md` and `gh pr view 529 R --json body --jq .body` to
`S/verify-r5-body-posted.md` (both removed after the check);
`git diff --no-index --ignore-space-at-eol -U0` on the two prints one hunk:

```text
@@ -171 +171 @@ frame lookup; it needs one heavy run to confirm.
-- [ ] Verified
+- [x] Verified at `b24d3bf`
```

So D1, D3 to D9 and the rest of the text are carried from the earlier passes at `b24d3bf`: the
only changed line is that box.

The box. `$CHANTIER log CR-509`: `2026-11-26T02:18:36Z driver verdict result=VERIFIED
head=b24d3bf08f01ae0e72fe7d251b25833df558608c base=5a73b6ebcf66ef80b412afcdbfd09c4defc028d8`,
recorded before the edit, at the SHA the box cites. The Review box still matches D10 (the same
log's two notes). This replaces D9's last sentence ("Verified" unchecked).

Render and images, run again on the current text:
`gh api repos/gsemet/markdown-okf-schema-studio/pulls/529 -H "Accept: application/vnd.github.full+json" --jq ...`
(counts over `body_html` and `body`):

```text
head b24d3bf08f01ae0e72fe7d251b25833df558608c, base 5a73b6ebcf66ef80b412afcdbfd09c4defc028d8, open, draft true
h2 9, h3 1, tables 1, rows 6, pre 2, checkboxes 8, checked 8, details 0, literal ** 0
img 0, markdown images 0, user name or home paths 0, STALE or UNVERIFIED 0
role names or cr-<n>: one line, "CR-509 heavy-ci-trusted-suite-timeout." (Internal references)
headings: Summary, Deliverables, Changes, What the failed frame lookup showed, Impacts,
Blast radius, Autonomous decisions, Known gaps, Test plan, Internal references
```

CI green box: `gh pr checks 529 R` (run 45734227734): static, static-windows, visual,
viewer-graph, report, checks `pass`; integration, stress, release-check, toc-loop `skipping`.

At the end of the pass `gh pr view 529 R --json headRefOid,updatedAt,state,isDraft` shows the same
head and `updatedAt`, OPEN, draft; `git status --short` in `W` prints nothing.

## Notes on this pass

- Refused action: see D7 (the earlier pass; nothing was refused in the D11 pass).
- One no-op shell call of this pass changed into the CR's `work/` folder (`cd ... ; true`), which the
  startup core forbids; the shell was back in the worktree at the next call.

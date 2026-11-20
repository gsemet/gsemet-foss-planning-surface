# CR-425 investigation (before round 1)

Worktree `markdown-okf-schema-studio.worktrees/batch-06-CR-425` at 80940a3c (clean). The spec's line
numbers were taken at fff2bc26; every one below is re-read at 80940a3c. Rules read: project
`AGENTS.md`, `ci.guidelines.md` (rules 11, 12, 13), the CR's spec.

## 1. Section A: `paste-url`, the obsolete stored-mode wait

### Edits, re-anchored

| Spec item | File | Lines at 80940a3c | Note |
| --- | --- | --- | --- |
| A.1 | `test/integration/pasteUrl.test.ts` | import line 6; comment 151-153; `setEditMode(page, false)` 154; wait 155 | as the spec. `waitFor` stays used (line 143). Marker `@tests_req ...PALETTE-264` at line 59 moves with the import removal (no action). |
| A.2 | `test/integration/dropFiles.test.ts` | import line 8; comment **136** (spec says 137); `setEditMode` 137; wait 138 | comment is one line: "CR 152: leave edit mode off for the next scenario (the workspace remembers it)." |
| A.3 | `test/integration/findInPreview.test.ts` | wait `settle(... remember edit mode off ...)` line 368; page-side wait 366-367 kept | the comment at 359-360 ("edit mode off again when it was not on before, the host remembering it") also names the host memory: rewrite it with the removal. Line 100 docblock ("stored edit mode restored") stays true (line 109 reads it). |
| A.4 | `src/host-vscode/testHooks.ts:193-197`, `src/extension.ts:28`, `test/integration/extensionApi.ts:28` | | **No change.** `storedEditModeForTests` keeps two readers once the three waits go: `findInPreview.test.ts:109` (`editModeBefore`) and `:151` (`pageState` diagnostic). `just check`'s unused-export check will not flag it; the import at `findInPreview.test.ts:11` stays. |
| A.5 | `test/build/integrationEditModeRestore.test.ts` | docblock 10-17 | the test title (line 18, "CR 152: ...") and the assertion message (line 26, "these scenarios leave the workspace in edit mode for the next one") also say "workspace"; the spec keeps the assertion unchanged, so only the docblock moves unless the Driver judges the message part of the docblock fix. Marker `@tests_req SwRS-MDOKFSTUDIO-BLOCK-004` at line 9. |
| A.6 | `requirements/tiers/swrs/palette-slash/SwRS-MDOKFSTUDIO-PALETTE-264.md` | Method line 78 | as the spec. |
| A.8 | `test/integration/realInput/run.ts` | table 73-99, `checkbox-toggle` entry 97; check at 103-104 | add `"paste-url": async () => runPasteUrl()` and `"drop-files": async () => runDropFiles()` after line 97, imports `run as runPasteUrl` from `../pasteUrl.test`, `run as runDropFiles` from `../dropFiles.test` (both `run()` open their own CDP connection, like `checkbox-toggle`). |
| A.8 | `test/shared/stressPlan.ts` | trusted list 52-82, `checkbox-toggle` at 80 | append the two names after 80, same order as run.ts. |

### Which SwRS / StRS of A.6 describe the test wait

`grep "remembers it\|workspace remembers"` over `requirements/tiers` at 80940a3c:

| File | Line | Describes | Action |
| --- | --- | --- | --- |
| SwRS PALETTE-264 | 78 | **the test wait** ("waits until the workspace remembers it, CR 152") | change (A.6) |
| SwRS BLOCK-004 | 79 | the guard test (`integrationEditModeRestore`), not the wait; its rationale ("pasteUrl left it on, the first ArrowDown went to the workbench") is history | leave (guard unchanged) |
| SwRS BLOCK-014 | 135 | product: the editor "remembers its line ending" | leave |
| SwRS LIFE-169 | 184 | product: the TOC toggle "posts toc and remembers it" | leave |
| SwRS MYST-081 | 88 | product: the host remembers a banner dismissal | leave |
| SwRS TOOLBAR-001, TOOLBAR-007 (and 013, 129, 130, TRUST-005, 006) | link lines | the StRS title "remembers its collapsed state" | leave |
| StRS PALETTE-002 | 22, 43 | product: the palette mode | leave |
| StRS TOOLBAR-001 | 5, 39 | product: toolbar collapse | leave |

Only PALETTE-264 changes. `requirements/tiers/log.md:1591-1595` (CR 152 entry) is history: leave it, add
a new dated entry (E).

### The stress list's length: every count, and a conflict

The trusted list holds **19** names at 80940a3c (+1 untrusted); A.8 makes it 21.

- `justfile:337` "The default 12 rounds of all 17 trusted scenarios take about 14 min." and `:339`
  "12 rounds of all 17, 60 rounds of 3, 100 rounds of 2": **already stale** (19, not 17). Update to the
  new count; 12 x 21 = 252 runs is above the "about 220 per window" advice of the same comment and of
  `ci.guidelines.md` rule 13, so the comment must say the default is capped.
- `test/build/hangWatchdog.test.ts:314` comment "CR 328: 19 scenarios x 12 rounds meet the ceiling":
  update the count. The assertions 305-307 use literal `(12, 17)` on the pure function: not the list.
- `test/shared/hangWatchdog.ts:34` "a round of 17 scenarios took 67.3 s": a past measurement, leave.
- `test/build/stressPlan.test.ts`: no length count (reads the list).
- **Conflict (blocks A.8 as written):** `test/build/hangWatchdog.test.ts:323-328` "CR 327: the default
  stress plan keeps a third of margin under its deadline" asserts
  `30_000 + 12 x N x 3_960 <= deadline x 2/3`, the deadline capped at 24 min (`STRESS_DEADLINE_CEILING_MS`),
  so `<= 960_000`. N = 19: 932,880 (passes). **N = 20: 980,400, N = 21: 1,027,920: fails.** Adding
  even one name turns `just check` red. Ways out, each outside the spec's text:
  1. lower the default rounds 12 -> 11 (21 x 11: 944,760, passes): touches `justfile:340` default,
     `test/build/test_workflows.py:649` (asserts `"12"`), and `.github/workflows/ci.yml:34` (input
     description "empty means 12"), and the spec's Out of scope excludes changing the workflow;
  2. re-measure the per-scenario average (3.96 s, `hangWatchdog.ts:33-36`) with the two new, shorter
     scenarios (paste-url 2.4-2.5 s, drop-files 1.6-1.8 s as whole steps in the CR-350 logs) from a heavy
     stress run, and update the constant with that run's id;
  3. add the two scenarios to the stress list only for the proof dispatch (`stress_scenarios=`), not to
     the default list: contradicts A.8 and CI rule 12 ("add the scenario to the stress list").
  Question for the owner below.

## 2. Section B: `checkbox-toggle`

Step B.1 is done: `work/checkbox-hang-evidence.md` (artifacts in `work/artifacts-44651927198/`,
`work/artifacts-44694304978/`, logs `work/ci-44651927198.log`, `work/ci-44694304978.log`; both
artifacts were still available). In short: the step hung inside its `try`, in the local
`currentPreviewFrame` or its unbounded failure report (`windowFocusReport`), with the host alive
(heartbeat to the end), the preview rendered and visible (screenshots), one webview iframe only, and
the step's fresh `connectOverCDP` made 1-3 ms after `stock-coexistence` disposed its webviews. A
never-loading webview is contradicted; a lasting leftover frame is contradicted; a transient detaching
frame in the new connection's frame list is supported, not proven.

Code, re-anchored (all as the spec): `test/integration/checkboxToggle.test.ts` local `waitFor` 19-26,
`waitForRender` 28-36 (keeps `html.includes("myst-checkbox")`: the harness `waitForRender(document,
extra)` at `harness.ts:109-120` takes it as `extra`), local `currentPreviewFrame` 39-65 (no document-id
check, unlike the harness), marker 151, `waitForRender` 152, `currentPreviewFrame` 153; the same pair at
169-170, 195-196, 208-209. Harness: `waitFor` 51-68, `findCurrentFrame` 127-147, `frameCall` 150-161,
`currentPreviewFrame` 209-229 (its failure dump is bounded). Note: the local copy's catch calls
`windowFocusReport(page)` (`windowFocus.ts:156-...`), whose per-frame `frame.evaluate` and
`page.evaluate` are unbounded: replacing the local copy with the harness one removes that path too.
`stockCoexistence.test.ts:256-272` is the predecessor's `finally` (closes MyST and stock preview tabs,
`disposeActivePreviewForTests()`; it does not wait for the webviews to go nor use `closeAllEditors`,
whose `harness.ts:794-806` awaits `previewGroupUnlocksSettledForTests()` and asserts no tab is left).
Its text tabs `preview.md`, `preview-other.md` and `feature-contract.md (dirty)` (from an earlier step)
stay open into `checkbox-toggle`.

Smallest change for B: B.2 as the spec (harness `waitFor`, `waitForRender(document, (html) =>
html.includes("myst-checkbox"))`, `currentPreviewFrame`, plus `markProgress` between them). For B.3, the
supported lead points at the predecessor's teardown and the frame scan: the document-id check comes
with the harness lookup; whether `stock-coexistence` must also wait for its webviews to be gone before
it ends is for the Driver to decide from the next named failure (no evidence yet names the frame).

## 3. Section C: `preview-editing` issue highlight

- Test: `test/integration/previewEditing.test.ts` `stepSchemaOrderAndBadge` 987-1032; frame 1014,
  `badge` 1015, `badge.click()` 1018, the attribute locator 1019, `count()` 1020 (also timer-dependent:
  it passes only when read within 1.5 s), `evaluate` 1021-1025. Markers 984-986
  (FMSCHEMA-010/029/039). Called at 1387. `previewFrame` comes from `previewEditingHelpers.ts:31` and is a
  Playwright `Frame`.
- Page handler: `src/page/features/pageInput.ts:152-172` (`document.addEventListener("click", ...)`
  inside `bindClicks`, marker `@implements_req SwRS-MDOKFSTUDIO-FMSCHEMA-039` at 146): focus at 169,
  attribute set at 170, `setTimeout(..., 1500)` at 171. Focus comes before the attribute, so at the
  mutation `document.activeElement` is the cell.
- Recorder with the harness's frame API: the repo already has the pattern,
  `test/integration/radioChoice.test.ts:110-152` (`watchToggles` / `assertNoWrite`): `frame.evaluate`
  installs a `MutationObserver` on `document` (`subtree: true, attributes: true, attributeFilter:
  [...]`) and stores `{ record, observer }` under a window key; reading uses
  `observer.takeRecords()` then `disconnect()`. For C:

  ```ts
  await frame.evaluate((key) => {
    const record: { field: string | null; activeField: string | null }[] = [];
    const observer = new MutationObserver((mutations) => {
      for (const mutation of mutations) {
        const cell = mutation.target as Element;
        if (cell.getAttribute("data-okf-issue-highlight") !== "true") continue;
        record.push({
          field: cell.closest("tr[data-okf-field]")?.getAttribute("data-okf-field") ?? null,
          activeField: document.activeElement?.closest("tr[data-okf-field]")?.getAttribute("data-okf-field") ?? null,
        });
      }
    });
    observer.observe(document, { subtree: true, attributes: true, attributeFilter: ["data-okf-issue-highlight"] });
    (window as unknown as Record<string, unknown>)[key] = { record, observer };
  }, KEY);
  await badge.click();
  await frame.waitForFunction((key) => (window as any)[key].record.length > 0, KEY, { timeout: 10_000 })
    .catch(async (error) => { throw new Error(`${String(error)} page: ${await recorderDiagnostics(frame)}`); });
  ```

  then read and disconnect in one `frame.evaluate` (`takeRecords()` first), assert `record.length === 1`
  ("the badge press highlights one cell") and `record[0].field === "count"` ("the badge press goes to the
  first row with an issue"). The failure diagnostic reads the record, `document.activeElement`, and
  `tr[data-okf-field].okf-error` names. Caveat: the attribute is set to `"true"` and later removed, both
  are attribute mutations; the filter on the current value `"true"` at callback time misses the set if
  the removal already happened before the callback runs (impossible: callbacks run in a microtask, the
  removal 1.5 s later), but to be exact record `mutation.oldValue === null` with `attributeOldValue: true`
  and the target's value, or record every mutation and filter at read. Caveat 2: a frame replaced by a
  render between install and click loses the recorder; the wait then fails in 10 s with an empty record,
  which names it (the test already waited for the current preview at 1011-1013).

## 4. CR-424 overlap

`origin/chantier/batch-06/cr-424-take-ownership-of-external-pr-404-list-i` at f9c7817c: three commits
(20583f69, 15b65463, f9c7817c) on 82c11a47, whose tree is identical to this CR's 80940a3c
(`git diff 82c11a47 80940a3c` empty). `git diff --stat 82c11a47 f9c7817c`: 45 files. Files this spec
also names:

- `requirements/tiers/log.md` (CR-424 +52 lines; this CR adds a dated entry, E): append conflict, trivial.
- `requirements/tiers/swrs/block-editing/SwRS-MDOKFSTUDIO-BLOCK-014.md`: named by A.6 only as a file to
  check; no edit expected here (product text), so no conflict.

None of the test, harness, stress, justfile, `pageInput.ts` or other SwRS files of this spec is touched
by CR-424 (it touches `test/integration/realInput/editorWidgets.ts`, not named here). `just
requirements-update` regenerates index files CR-424 also edits (`swrs/block-editing/index.md`,
`swrs/toolbar-navigation/index.md`, `strs/toolbar-navigation/index.md`) only if a title changes; this
CR changes none.

## 5. Evidence plan for the Verifier

Kind of change: test-only (A, B.2, C) plus requirements text; B.3 may become a test-harness change or,
if the evidence names one, a product fix. Nothing visual to screenshot before/after; the proof is
command output and CI runs.

| # | What | Command | Proves | Where |
| --- | --- | --- | --- | --- |
| 1 | static gates | `just check`, `just preflight` (Windows: static stage) | unused exports, `integrationEditModeRestore`, `hangWatchdog.test.ts` margin (see conflict), `stressPlan.test.ts`, the run.ts/stressPlan order assertion is at runtime only | local, logs in `work/gates/` |
| 2 | requirements | `just requirements-update`, `just requirements-lint` | markers moved with code, PALETTE-264 text, log entry | local |
| 3 | A read-proof | `grep -rn "remember edit mode" test/` empty; `grep -rn storedEditModeForTests` lists only findInPreview 109/151, the hook and its re-exports | the wait is gone; the hook kept on purpose | local |
| 4 | A real window | `STUDIO_REAL_INPUT_SCENARIO=paste-url npm run test:integration`, then `=drop-files` (each runs setup + that step only, `trusted-suite.ts:222-229`) | the scenario passes without the wait | local, one window at a time, only when the desktop is free; otherwise say so in the PR test plan |
| 5 | A + B stress | `gh workflow run ci.yml --ref <branch> -f heavy=true -f stress_repeat=30 -f stress_scenarios=paste-url,drop-files,checkbox-toggle` (90 runs, under 220) | the stress table accepts the names (runtime assertion run.ts:103) and the scenarios pass 30 times | CI only |
| 6 | suite order | three `gh workflow run ci.yml --ref <branch> -f heavy=true`, each `integration` green, `paste-url`, `checkbox-toggle`, `preview-editing` in their `STEP done` lines | the order-dependent hang (after `stock-coexistence`) and C's timing race no longer fire | CI only; a red run is read, never re-run |
| 7 | B diagnostic | a deliberately broken check (for example a unit-level call of the bounded lookup against a never-settling promise, or a local run with a wrong expected request id) showing `TIMEOUT: <call> did not return within 10000 ms (frame <url>)`, or the quoted message of a CI failure after the change | a stuck call now fails in about 10 s, named | local or CI |
| 8 | B evidence | `work/checkbox-hang-evidence.md` | step B.1 | done |
| 9 | C by reading | no read of `data-okf-issue-highlight` after `badge.click()` other than through the recorder; the green runs of 6 | no dependence on the 1.5 s timer | review + CI |

What only CI can prove: the suite-order hang of `checkbox-toggle` (needs the full `integration` order),
the stress repetitions, and the timing race of C on a slow runner. Item 6 cannot prove a negative for a
rare flake; three green runs are the spec's bar.

## Questions only the owner can answer

1. A.8 vs the stress margin test (section 1): adding `paste-url` and `drop-files` to the default stress
   list fails `hangWatchdog.test.ts` "keeps a third of margin" (12 rounds x 21 x 3.96 s). Lower the
   default rounds to 11 (touches `ci.yml`'s input description, outside the spec's scope), re-measure the
   per-scenario average from a heavy stress run, or keep the two names out of the default list?

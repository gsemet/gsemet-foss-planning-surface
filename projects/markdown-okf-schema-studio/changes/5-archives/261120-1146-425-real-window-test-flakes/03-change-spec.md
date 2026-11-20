# Change Specification: CR-425 rw-flakes, real-window integration test flakes

No tracker issue (verbal request).

## Goal

Three real-window integration steps fail on CI without a code change: `paste-url`,
`checkbox-toggle` and `preview-editing` (its sub-step `stepSchemaOrderAndBadge`). Each red run
turns `integration`, then `report` and `checks`, red on a push to `main` or a heavy dispatch. The
owner wants all three fixed at their root cause in this CR (CI rule 12: a flake is a bug, fixed at
its cause and proved by repetition). A cause that stays unfound is never hidden: no retry, no
quarantine, no raised timeout; the test stays as it is and the analysis is written down as a
Known issue.

## Decisions carried from `02-answers.md`

1. Scope: the three flakes, each at its root cause: `paste-url` (obsolete stored-mode wait, CR-350
   diagnosis), `checkbox-toggle`, and `preview-editing` issue-highlight (`stepSchemaOrderAndBadge`
   locator timeout).
2. If a cause stays unfound: keep the test, no automatic retry, no quarantine; document a Known
   issue with the written analysis.
3. Where the analysis lives: a short Known issue in the SwRS, the full analysis in the CR folder,
   summarized in the PR body; no extra file under `docs/`.
4. The `reportStaleEdit` debug log stays out, unless the Driver needs it to prove a cause.

## Failing runs (all evidence the Driver starts from)

| Step | Run, attempt | Commit | Message |
| --- | --- | --- | --- |
| `paste-url` | 44647675614, 1 and 2 | 768570c (CR-350 branch) | `Timed out waiting for the workspace to remember edit mode off.` (12.4-12.5 s) |
| `paste-url` | 44690391950, 2 | 412ca69 (CR-350 branch) | same, 12643 ms |
| `checkbox-toggle` | 44651927198, 1 | 24c9eef (`main`) | `STEP TIMEOUT: checkbox-toggle did not finish within 180000 ms; last progress marker: waiting for the first checkbox render`; hang dump `hang-dumps/20261120T011906047Z-checkbox-toggle` |
| `checkbox-toggle` | 44694304978, 1 | 412ca69 (CR-350 branch) | same message; hang dump `hang-dumps/20261120T072718222Z-checkbox-toggle` |
| `preview-editing` | 44690391950, 1 | 412ca69 | `locator.evaluate: Timeout 30000ms exceeded`, waiting for `tr[data-okf-field] [data-okf-issue-highlight="true"]`, at `stepSchemaOrderAndBadge` |

Artifacts (not expired at the time of writing): `e2e-integration-attempt-<n>` of each run holds the
hang dumps and screenshots (`gh run download <run> -n e2e-integration-attempt-<n> -D <CR folder>/work/artifacts-<run>`).
Logs: `gh run view <run> --log-failed`. The CR-350 diagnosis of `paste-url` is in
`4-batch/2-actives/350-ci-gallery-on-dispatch/work/diagnosis.md` of the planning surface (its
saved logs in `work/debugger/`, and `work/ci-44690391950*.log`, `work/ci-44694304978-a1.log`). The
earlier analysis of the same `checkbox-toggle` hang is in the archived CR-326
(`5-archives/261114-0947-326-flaky-real-window-integration-steps/03-change-spec.md`, section C and
Decision 6).

## What changes

### A. `paste-url`: drop the obsolete stored-mode wait (test only)

Root cause, from the CR-350 diagnosis: the wait
`waitFor("the workspace to remember edit mode off", () => storedEditModeForTests() !== true)`
checks a host value no product code reads since b84b0585 (every document opens in preview mode),
and that SwRS-MDOKFSTUDIO-LIFE-169 lets stay stale by design (a `previewEditModeChanged` naming an
older render is dropped by `manager.matchesCurrent`, src/session/previewManager.ts, through
`reportStaleEdit`, src/session/pageMessages.ts). `paste-url` toggles edit mode off right after the
autosave, before the render it starts reaches the page, so the off message can name an older
render and be dropped; the host then holds `true` for the whole 10 s. No product change.

1. `test/integration/pasteUrl.test.ts`: remove the wait (line 155 at fff2bc26) and the
   `storedEditModeForTests` import (line 6). Keep `await setEditMode(page, false)` (line 154): it
   already waits until the page's current render keeps edit mode off. Rewrite the comment above it
   (lines 151-153): the scenario leaves the page's edit mode off for the next scenario; drop the
   "the workspace remembers the edit mode for the next preview" rationale.
2. `test/integration/dropFiles.test.ts`: same removal (line 138, import at line 8) and comment
   (line 137).
3. `test/integration/findInPreview.test.ts`: remove the `settle("the workspace to remember edit
   mode off", ...)` at line 368; keep the page-side wait at lines 366-367. Lines 109
   (`editModeBefore`) and 151 (diagnostic) may stay.
4. If no test reads `storedEditModeForTests` any more, `just check` (unused exports) flags the
   hook: then remove it from `src/host-vscode/testHooks.ts`, `src/extension.ts` and
   `test/integration/extensionApi.ts` in the same change; otherwise leave it.
5. `test/build/integrationEditModeRestore.test.ts`: update the docblock (lines 10-17) so it no
   longer says the workspace makes the next preview open in edit mode; the guard itself ("a
   scenario that turns edit mode on turns it off") and its assertion stay unchanged.
6. `requirements/tiers/swrs/palette-slash/SwRS-MDOKFSTUDIO-PALETTE-264.md`, Method line (line 78):
   drop "and waits until the workspace remembers it, CR 152". Check the other SwRS and StRS that
   say "the workspace remembers" (`grep -rln "remembers it\|workspace remembers" requirements/tiers`:
   BLOCK-014, LIFE-169, MYST-081, TOOLBAR-001, TOOLBAR-007, PALETTE-002, TOOLBAR-001 StRS) and change
   only those whose text describes this test wait, not a product behaviour.
7. Left out (Decision 4), unless the Driver needs it to prove the cause (diagnosis point 4,
   product observability only): log a dropped page-state message's type and both
   identities at debug level in `reportStaleEdit`. A product change needs its SwRS updated
   (constitution, section 1).
8. Stress list (CI rule 12): add `paste-url` (and `drop-files`, which carries the same wait) to
   the trusted stress list, the same way `checkbox-toggle` is a whole step there:
   `"paste-url": async () => runPasteUrl()` in `STRESS_SCENARIOS` of
   `test/integration/realInput/run.ts`, and the name in `STRESS_SCENARIOS_BY_HOST.trusted` of
   `test/shared/stressPlan.ts`, in the same order (the table asserts the two lists match). Update
   any count that names the stress list's length (the `ci-stress` comment in the `justfile` says
   "of all 17"; any test in `test/build/` that checks the list).

### B. `checkbox-toggle`: the hang after "waiting for the first checkbox render"

What the logs prove: the step's last marker is `waiting for the first checkbox render`
(`test/integration/checkboxToggle.test.ts:151`), followed by `waitForRender(document)` (10 s,
synchronous host predicate) and `currentPreviewFrame(page)` (10 s `waitFor`), yet the step ran
180 s, twice, both times right after `stock-coexistence`. The `stress` job, which runs
`checkbox-toggle` alone and repeated, was green in the same run 44651927198: the hang depends on
the suite order (the state the earlier steps leave), not on the step alone.

Lead (to prove, not assumed): `checkboxToggle.test.ts` has its own copy of `currentPreviewFrame`
(lines 39-65) and `waitFor` (lines 19-26). CR-326 Decision 6 bounded every Playwright call of the
harness's frame lookup (`findCurrentFrame` and `frameCall`, 10 s each,
`test/integration/realInput/harness.ts:127-161`), but fef0731e left this copy unbounded: its
`locator.count`, `frameElement().isVisible` and `getAttribute` calls can wait forever on the frame
of a hidden or detaching preview tab, and `waitFor` checks its deadline only between predicate
calls. CR-326's dump also showed leftover tabs from earlier steps (`preview.md`,
`preview-other.md`, a dirty `feature-contract.md`) in the window at this step.

Steps:

1. Evidence first: download the two hang dumps (runs 44651927198 and 44694304978, artifact
   `e2e-integration-attempt-1`) into the CR folder's `work/`, and write down what they prove and
   do not (window state, tabs per group, CDP targets, screenshots), as the CR-350 diagnosis does.
2. Make the hang name itself: replace the local `currentPreviewFrame` and `waitFor` of
   `checkboxToggle.test.ts` with the harness ones (`currentPreviewFrame`, `waitFor` from
   `test/integration/realInput/harness.ts`), or route each Playwright call through the same
   bounded helper, so a stuck call fails in about 10 s with the call and the frame URL named. Add
   a `markProgress` between `waitForRender(document)` and `currentPreviewFrame(page)`, so the
   marker tells which of the two waited. The `waitForRender` here checks `html.includes("myst-checkbox")`,
   which the harness one does not: keep that condition.
3. Fix the cause the evidence shows, with a deterministic readiness signal (CI rule 12). Candidates
   to check against the dumps: a leftover preview frame from `stock-coexistence` or earlier steps
   that the frame scan touches (fix: the step that leaves it closes it and `closeAllEditors` leaves
   no tab, or the scan skips frames not belonging to the active preview); a webview of the new
   preview that never finishes loading (then a product bug: a Studio preview that does not render
   is the product's to fix, with its SwRS). A theory the evidence contradicts is dropped.
4. If the cause stays unfound after steps 1-3 (Decision 2): keep the bounded lookup of step 2 (it
   is diagnostics, not a retry: it turns a 180 s hang into a named 10 s failure) and write the
   Known issue (see D).

### C. `preview-editing`: the issue highlight lasts 1.5 s

Root cause, from the code: the badge click handler (`src/page/features/pageInput.ts:152-172`)
sets `data-okf-issue-highlight="true"` on the first row's value cell, focuses it, and removes the
attribute after 1500 ms (`window.setTimeout(..., 1500)`, line 171). The test
(`test/integration/previewEditing.test.ts:1018-1025`, `stepSchemaOrderAndBadge`) clicks the badge,
asserts `highlighted.count() === 1` (passed in the red run), then calls `highlighted.evaluate(...)`
on the same attribute selector: when more than 1.5 s passes between the click and that call on a
slow runner, the attribute is gone and the locator waits its 30 s default. A race between the test
and a product timer; the product behaves as SwRS-MDOKFSTUDIO-FMSCHEMA-039 says (the badge scrolls
to the first row with an issue). Fix in the test only:

1. Before `badge.click()`, install in the frame a recorder that does not depend on timing: a
   `MutationObserver` on the content root (attribute filter `data-okf-issue-highlight`) that stores
   the `data-okf-field` of the row of every cell that gets the attribute set to `"true"`, plus the
   row of `document.activeElement` at that moment. After the click, wait (`frame.waitForFunction`)
   for the recorder to hold an entry, then assert: exactly one highlighted cell, its row is
   `count`. The assertions keep their intent and messages ("the badge press highlights one cell",
   "the badge press goes to the first row with an issue"); only how the cell is read changes
   (constitution, section 3: say so in the commit).
2. Disconnect the observer after reading. A wait failure says what the page held (the recorder's
   entries, the active element, the rows with `okf-error`), CI rule 12 "failure messages carry
   diagnostics".
3. No product change, no change of the 1500 ms. FMSCHEMA-039 is unchanged (it does not name the
   highlight's duration).

### D. Known issue, only for a cause left unfound (Decision 2)

For each flake whose cause stays unfound: no retry, no quarantine, no raised timeout or budget, the
test kept and still in the required `integration` job. Write a `Known issue` entry in the
`### Known issues` section of the SwRS the step checks (`checkbox-toggle`:
SwRS-MDOKFSTUDIO-BLOCK-058; `paste-url`: PALETTE-264; `stepSchemaOrderAndBadge`: FMSCHEMA-039),
in the form BLOCK-004 already uses ("Known issue (…): in the real-window test, …"), stating what
the logs prove, what they do not, the runs, and what was ruled out; then a dated entry in
`requirements/tiers/log.md`. The full analysis stays in the CR folder (`work/`) and is
summarized in the PR body; no extra file under `docs/` (Decision 3).

### E. Requirements

After the change: `just requirements-update`, and a dated entry in `requirements/tiers/log.md`
(the PALETTE-264 Method change, any Known issue). Markers move with any code they sit on.

## Out of scope

- Any retry, quarantine, `continue-on-error`, raised step budget (`STEP_BUDGETS_MS`) or timeout.
- Changing the workflow (`.github/workflows/ci.yml`) or the `ci-*` targets beyond the stress list.
- Changing the 1500 ms highlight or the edit-mode storage in the product (unless step B.3 proves a
  product bug, which is then fixed with its SwRS).
- Other flaky steps not listed above (for example `wide-table-tab`).

## Environment of the proof

The real-window jobs run only on CI: `integration` and `stress` on `ubuntu` GitHub runners under
`xvfb-run -s "-screen 0 2600x1440x24"`, VS Code 1.147.0 downloaded by `@vscode/test-electron`, no
desktop shared with other agents. Locally (Windows) a real-window run opens a VS Code window on the
shared desktop: run one at a time, only when no other batch agent runs a window
(`local-worktree.guidelines.md`). The suite order that makes `checkbox-toggle` hang (after
`stock-coexistence`) exists only in the full `integration` run, not in `stress` and not in a
`STUDIO_REAL_INPUT_SCENARIO=` run; only heavy dispatches prove it.

## Evidence

1. `just check` and `just preflight` green at the head (on Windows, preflight's static stage;
   `test/build/integrationEditModeRestore.test.ts` still passes, reading the shipped test files).
2. Locally, one window at a time, when the desktop is free: `STUDIO_REAL_INPUT_SCENARIO=paste-url
   npm run test:integration` and `STUDIO_REAL_INPUT_SCENARIO=drop-files npm run test:integration`,
   green. If the desktop is not free, say so in the PR's test plan; CI then carries the proof.
3. Heavy dispatch with stress on the new entries:
   `gh workflow run ci.yml --ref <branch> -f heavy=true -f stress_repeat=30 -f stress_scenarios=paste-url,drop-files,checkbox-toggle`:
   `integration` green and `stress` green on every round.
4. Three heavy dispatches at the fix's head (`gh workflow run ci.yml --ref <branch> -f heavy=true`),
   each with `integration` green: `paste-url`, `checkbox-toggle` and `preview-editing` pass in the
   suite order. A red one is read (rule 12), never re-run to green.
5. For B: the written evidence of step B.1 in `work/`, and the failure message of the bounded
   lookup shown in a deliberately broken local or unit check, or quoted from a CI run if one fails
   after the change.
6. For C: the recorder reads `count` in the green runs of item 4; the test passes with no
   dependence on the 1.5 s timer (a reviewer can check by reading: no read of the attribute after
   the click other than through the recorder).

No host and default matrix: nothing here depends on the host or on a configured value.

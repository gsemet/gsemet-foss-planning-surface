# Diagnosis: heavy CI run 44193765309, step preview-editing, stepSchemaOrderAndBadge

Status: the failing code is new test code of this CR, not a regression of `src`. The exact runtime
reason the preview HTML never shows the error row is NOT proven (no VS Code host here, no local
heavy run). What is proven is listed under Proof; what is open is listed under Open.

## Reproduction

`gh workflow run ci.yml --ref chantier/batch-06/cr-344-cr -f heavy=true` (job `integration`, step
preview-editing). Log: work/ci-integration.log lines 1288-1377. Stack: `waitFor`
(previewEditingHelpers.js:55) called from `stepSchemaOrderAndBadge` (previewEditing.test.js:873),
i.e. test/integration/previewEditing.test.ts:1006-1007. No local equivalent: the host needs VS Code
(no `.vscode-test` in the repo or the worktree).

## Proof

1. The failing step does not exist on main. `git show origin/main:test/integration/previewEditing.test.ts`
   has no `count: two`, no `stepSchemaOrderAndBadge`, no `stepSchemaProblem`, no `okf-error` regexp on
   `<tr class=`. Both steps are added by commit 927f5400 (coder/r3.md says they are real-window
   steps; coder logs say integration was "not run locally"). So the step has never run on a host
   before this CI run. Main's green run proves nothing about it.
2. The `src` diff against origin/main is comments and marker moves only, plus a CSS constant split in
   `src/core/preview/styles/commentStyles.ts`. `git diff origin/main -U1 -- src/core/frontmatter
   src/session src/core/edits src/node-services` shows only `@implements_req` lines moving. No logic
   of validation, table rendering or refresh changed. The extraction of the old steps into functions
   and the move to `previewEditingHelpers.ts` is verbatim (helpers diff = moved code).
3. The product code gives the row the test waits for. Probe (scratchpad probe3.js, compiled
   out/src of the worktree, the fixture's real schema and source copied from the test, plus the
   mutations the earlier steps make: summary renamed, tags null, metadata revision 3,
   exemption_reason null):
   - `analyzeFrontmatter` on the original text: 0 errors; on the text with `count: two`: 1 error,
     `count: must be integer`, `schemaFound: true`.
   - `renderPropertiesTable` on that result (with and without source mapping) emits
     `<tr class="okf-error okf-known" data-okf-field="count" ...`, and the exact regexp of line 1007
     matches it; it still matches after `replacePropertiesTableHtml` (the host's patch path).
   So a render of `count: two` that reaches `preview.html` satisfies the predicate. The failure is
   therefore in the flow (the table of the active preview is not refreshed within 5 s, or the
   predicate reads a different preview/state), not in validation or markup.
4. Assertions before the failing wait passed in CI: the schema-order deepEqual (which needs the
   schema found, since the document lists `metadata` before `tags` and the schema the reverse),
   `rowNames.length > 10`, and the `brokenText !== originalText` guard. `applyEdit` returned true.

## Candidate causes, ranked (all on the test side)

A. The step is the first in the file that edits the document from OUTSIDE the preview right after
   the frontmatter-save steps and waits on the HTML of the active preview for a frontmatter-only
   change, with no `showTextDocument`/focus and no wait for the previous step's debounced link
   enrichment (`LINK_ENRICHMENT_DEBOUNCE_MS`) to settle. `stepSchemaProblem` (the other new step)
   does call `showTextDocument(document, ViewColumn.One)` first; this one does not. The preceding
   step ends on a refused save (no await on anything). This is the unproven suspect.
B. Predicate coupling to HTML attribute order (`<tr class="..." data-okf-field="count"`), which
   no other integration assertion does (they all use `<tr\b[^>]*data-okf-field=`). Proved fine for
   the renderer output (proof 3); only matters if the host rewrote attributes, and `setPreviewStatus`,
   `reuseNonce`, `replacePropertiesTableHtml` do not.

## Minimal fix (test only, no src change)

In `stepSchemaOrderAndBadge` (test/integration/previewEditing.test.ts, lines ~985-1027):
1. Before the edit: `await vscode.window.showTextDocument(document, vscode.ViewColumn.One);
   await waitForCurrentPreview(document);` as `stepSchemaProblem` does, so the preview is the
   active one and settled.
2. Wait on a DOM-independent, order-independent predicate, as the rest of the file does:
   `/<tr\b[^>]*\bokf-error\b[^>]*data-okf-field="count"/u` (or read the row with
   `html.match(/<tr\b[^>]*data-okf-field="count"[^]*?<\/tr>/u)` and test `okf-error` in its tag).
   Apply the same change to the `finally` wait at line 1024.
3. Prefer `await waitForCurrentPreview(document, requestBefore)` FIRST, then check the row (the
   full render also rebuilds the table from the same analysis), so a stale `getActivePreviewForTests`
   state cannot satisfy or starve the predicate.
4. To turn the open question into proof, make the timeout message carry the evidence: on timeout,
   throw with `getActivePreviewForTests()` phase, documentVersion vs `document.version`, and the
   `data-okf-field="count"` tag from the html. One CI re-run then names the cause (stale revision,
   other preview, or attribute shape). Remove the extra detail afterwards if wanted.

## Open

- Which of "preview not refreshed", "other preview active" or "predicate shape" fails at runtime is
  unobserved. Candidate A is only a hypothesis from reading `hostEvents.refreshPreview`,
  `frontmatter.refresh` (300 ms debounce, revision guards) and the step order; nothing in the log
  (it holds only dbus noise and screenshot PASS lines) discriminates.
- If after fixes 1-3 the step still times out, the cause is in the host (outside-edit frontmatter
  refresh) and is a product bug that main never exercised: then keep the step, file the bug, and the
  timeout message of fix 4 will carry the data.
- Do not remove the step to go green without that evidence: it covers FMSCHEMA-010/029/039.

# Round 2 review: radio choice lists, focus and write guards

Inspector, independent review of the uncommitted diff in
`/Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-222` (base origin/main 0b4ede78,
HEAD = origin/main, 20 files changed).

## Verdict: APPROVE

All six driver decisions of round 2 were applied correctly. Nothing else regressed. No new finding.

## Gates (run by the Inspector on this tree)

- `just check`: exit 0.
  - Unit tests: 3327, all pass, 0 fail. Round 1 had 3328: the checkbox press test was removed.
  - Contracts: 0. Security: 72 of 72 pass. Build pytest: 153 passed.
  - boundaries (313 modules), limits (902 files), exports, markers (3 companion files) and settings
    (19) all pass.
  - okfreq lint: 0 indexes and 0 projections would change. update-coverage --check: 0 files would
    change.
- `UV_NO_CONFIG=1 uv run --group requirements okfreq validate --check-links --project-root .`:
  1072 requirements, 0 errors, 21 warnings. All 21 are the existing W2 example-link warnings.
- No process from the worktree is left running.

## Driver decisions: verified

1. **Press guard only for radio options.** `src/page/features/checkboxes.ts:304-309`:
   `guardPress` returns on `CHECKBOX_SELECTOR` and calls `refuseForOpenEdit` only on
   `RADIO_SELECTOR`.
   - The click guard `mayToggle` keeps the origin/main semantics: it prevents the click, sets the
     status and returns false when an editor is open. It is only factored through
     `refuseForOpenEdit`.
   - `test/page/runtimePageControls.test.ts` is identical to origin/main (`git diff --quiet`).
   - The BLOCK-041 "Task-list checkbox click" row is unchanged. Only a new "Radio option press and
     click" row was added (line 101).
2. **TRUST-005 identical to origin/main.** The SwRS file is untouched. No line of the diff adds or
   removes a TRUST-005 marker. The marker at `checkboxes.ts:94` predates this change.
3. **"Untested" note on workspace.applyEdit.** It is present in the GFM-039 verification notes (the
   integration method line) and in the GFM-021 verification notes. The wording matches the round-1
   suggestion.
4. **Tab step starts from a real click.** `test/integration/radioChoice.test.ts:222-224`: a real
   `.click()` on the "Fix direction:" paragraph, then `page.keyboard.press("Tab")`. The new cases
   (`choices` Tab and focus steps, `openEditorGuard`, `readOnlyFile`) use no `.focus()`, no
   `dispatchEvent`, no sleep, no retry, no raised timeout and no `force`. The only `.focus()` left,
   at line 251 (Enter step), predates this CR. The round-1 scripted `.focus()` before the arrows is
   gone: the arrows now continue from the Tab.
5. **Race comment.** It sits at the text comparison in `src/session/features/sourceEdits.ts:110-112`,
   names the external change during the apply, and explains why it is benign.
6. **LIFE-119.** It is `proposed` on origin/main and now. The THEN reads "an element that is
   naturally focusable, or one that already carries a tabindex, keeps its own". This matches
   `rewriteNode` (`html-sanitizer.ts:466-476`, `&& !attr(node, "tabindex")`).

## Whole-diff checks

- **Behaviour matches the note.**
  - Tab order: the list, the option `li` and the option `p` get `tabindex="-1"`
    (`radioGroups.ts:116-128`). The sanitizer keeps an existing tabindex.
  - Focus restore: `keepRadioFocus` captures a position only when `document.activeElement` is
    inside a `.myst-radio`. It restores by line and column with `preventScroll`, after
    `applyPendingBlockSelection` (`contentPatch.ts:44,92`).
  - Press guard: capture-phase `mousedown`, prevented with an editor open, status "Save or cancel
    this edit before choosing an option." The editor stays open.
  - Host refusal: when an apply resolves true and leaves the text unchanged, the answer is
    `READ_ONLY_FILE`, "This file is read-only in VS Code.". It covers radios and checkboxes (same
    path). A false apply keeps the old message.
- **Requirements.** BLOCK-041, GFM-021, GFM-039 and LIFE-119 are `proposed` on origin/main and now.
  No approved requirement is changed. The generated frontmatter lists (`implemented_in_files`,
  `tested_in_files`) and the `okf:links` blocks agree with the markers: update-coverage and lint
  both report 0 changes.
- **`src/page/features/pageInput.ts`** is untouched.
- **Markers.** `@implements_req` GFM-039 is on the sanitizer, `keepRadioFocus` and the content
  patch. GFM-039 and BLOCK-041 are on `guardPress`. GFM-021 and GFM-039 are on the host text check.
  The `@tests_req` markers are on every new test: core render, security, page, session, integration
  and visual v12/v13.
- **No weakened assertions.** The integration test was restructured into `withPlan` and `choices`.
  Every origin/main assertion is still there with its message. The diffs of the page, session and
  core tests add lines only. The session fake document now applies the edits to its text, which is
  needed for the new check and leaves the old expectations unchanged.
- **Integration hygiene.**
  - `files.readonlyInclude` is restored in `finally` (Global target, original value).
  - Edit mode is turned off in `finally`, after an Escape and a wait for the editor to close.
  - The browser is closed in `finally`.
  - The test is registered in the trusted suite: `test/integration/trusted-suite.ts:182`, step
    `radio-choice`.

## Findings

None.

## Observations (no action)

- The real-window cases were not run locally (heavy integration job), as the task rules require.
  Run them in CI before the merge.
- The round-1 observations still apply: the mixed list keeps its own tab stop by design, and the
  `openEditorGuard` `finally` could hide a first error.

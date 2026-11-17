# Round 1 review: radio choice lists, focus and write guards

Inspector, independent review of the uncommitted diff in
`/Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-222` (base origin/main 0b4ede78).

## Verdict: APPROVE

The change matches the four points of the owner-validated behaviour note. It has no blocker and no
major finding. Point 1 below is a GATE point: the owner must acknowledge the checkbox press guard
before the merge. The other findings are small and can be fixed in this CR or left as stated.

## Gates (run by the Inspector on the fixed tree)

- `just check`: exit 0. Unit 3328 tests, 3328 pass, 0 fail. Contracts 0. Security 72 / 72 pass.
  Build pytest 153 passed. compile, boundaries, limits, exports, markers and settings all OK.
  okfreq lint reports 0 changes. update-coverage --check reports 0 files.
  (The HANG DUMP lines in the log come from the hang watchdog's self-tests; they are not failures.)
- `UV_NO_CONFIG=1 uv run --group requirements okfreq validate --check-links --project-root .`:
  1072 requirements, 0 errors, 21 warnings (the existing W2 example-link warnings).
- `src/page/features/pageInput.ts` is untouched.
- Every changed SwRS is `req_lifecycle: proposed`, both before and after the change (GFM-039,
  GFM-021, BLOCK-041, TRUST-005). No approved requirement is edited.

## What was checked and holds

- **Tab entry.** In `src/core/render/radioGroups.ts:118-129`, the whole-list `ul`/`ol`, the option
  `li` and the option `p` get `tabindex="-1"`. `injectSourceMappings` already kept an existing
  tabindex. The `rewriteNode` change (`src/core/security/html-sanitizer.ts:476`) aligns the path for
  pre-mapped HTML. The unit tests cover bulleted, ordered, mixed and nested groups. The sanitizer
  test fails on the old code (the `ul` became `tabindex="0"`). The render test also fails on the old
  code (`li` and `p` got 0 from injectSourceMappings).
- **Sanitizer safety.** `tabindex` was already on the global allow-list (`html-sanitizer.ts:72`),
  and `data-line` and `data-sphinx-*` are allowed too. So untrusted raw HTML could already put any
  tabindex on any element, including a mapped one through `data-line`. Keeping an existing tabindex
  in `rewriteNode` adds no capability. TRUST-050 (deprecated) and LIFE-119 (proposed) only require
  "tabindex 0 unless naturally focusable" for unmarked blocks, and they stay true for those.
  Positive author tabindex values are a separate concern and predate this change.
- **Focus after a choice** (`checkboxes.ts:272`, `contentPatch.ts:45,92`). The focused option is
  captured before editors close and the morph runs. It is restored after
  `applyPendingBlockSelection`, by line and column, with `preventScroll`. With no focused option,
  nothing changes. Nested and multiple groups are fine because each option has a unique line. The
  content patch is the only re-render path in the page (`hostHandlers.ts:20`). A refusal does not
  re-render, so the focus stays.
- **Press guard** (`checkboxes.ts:142,310`). It is a capture-phase `mousedown`. With no editor open
  `refuseForOpenEdit` returns at once, so normal clicks are unaffected. A read-only preview returns
  early. The listener does not stop propagation, so the other mousedown listeners (comment compose,
  shift-select) still run. The existing click guard stays the second line of defence and is
  unchanged in its effect. The frontmatter field editor is covered by the same `openEdit()`.
- **Host text check** (`src/session/features/sourceEdits.ts:109-117`). A no-op choice or toggle is
  answered "saved" earlier by the `unchanged` plan, so an edit that would leave the text unchanged
  never reaches the comparison. `HostDocument.getText()` is live in both hosts: the VS Code
  `TextDocument` and the memory `MemoryDocument`. A missing document already resolves false. The
  session test fails on the old code (it answered `saved: true`).
- **Integration test** (`test/integration/radioChoice.test.ts`). It runs in the trusted suite
  (`trusted-suite.ts:182`, step `radio-choice`, default 3-minute budget). Clicks are real CDP
  clicks, including the wheel scroll and the `page.mouse.click` with the editor open. Keys are real
  `page.keyboard`. The waits are polling `waitFor` with the default 10 s: no sleeps, retries or
  raised timeouts, and no `force`. `files.readonlyInclude` is restored in `finally`. Edit mode is
  turned off in `finally`, and the CR 152 guard test passes.
- **Visual v12/v13** (`test/visual/radioPlanScenarios.ts`). A real click on the label, then
  `press: Tab`. The test asserts that the focused element is the checked radio inside the group and
  that exactly one `:focus-visible` radio exists.
- **Screenshots.** `before-tab-focus-{cream,dark}.png` show the focus ring around the whole list:
  the first Tab lands on the `ul`. `after-tab-focus-{cream,dark}.png` show no ring on the list and
  the focus ring on the selected option "A click in the margin…" in both themes. This is the
  approved change.

## Findings

1. **minor (GATE): the press guard also covers task checkboxes, which goes beyond the behaviour
   note.** `src/page/features/checkboxes.ts:147`
   (`if (checkbox) refuseForOpenEdit(event, "toggling a checkbox")`), with BLOCK-041 row 100 and
   GFM-021.
   - The code is safe and consistent. It makes the existing BLOCK-041 row ("toggle cancelled,
     editor status shows …") hold in the blur race, which the old click guard missed.
   - The user sees one change: today, a press on a checkbox with an unchanged editor open closes
     the editor and toggles the box. After the change, the editor stays open and the status line
     shows "Save or cancel this edit before toggling a checkbox."
   - This is a visible change the owner did not validate.
   - Expected fix: no code change. The driver adds a Today/After line for checkboxes to
     `reports/behaviour-note.md` and gets the owner's OK at the gate. If the owner declines, drop the
     checkbox branch of `guardPress`, the BLOCK-041 row wording and the test at
     `test/page/runtimePageControls.test.ts:122-146`.

2. **minor: TRUST-005 gets a new scenario, although the note says its scope is unchanged.**
   `requirements/tiers/swrs/trust-security/SwRS-MDOKFSTUDIO-TRUST-005.md:135-139`, plus the marker
   at `src/session/features/sourceEdits.ts:112` and new `tested_in_files` entries.
   - The behaviour note says: "TRUST-005: unchanged scope (preview-level read-only); the read-only
     file refusal lives in GFM-039/GFM-021". GFM-021 turned out to be proposed, so both rows exist
     there already.
   - Expected fix, either of:
     (a) Remove the TRUST-005 boundary scenario, the TRUST-005 marker on `sourceEdits.ts:112`, its
     verification line and the two added `tested_in_files` entries. Then mark the comparison with
     GFM-021 and GFM-039, and rerun `okfreq update-coverage`.
     (b) Keep it and record the owner's OK in the note.
     Option (a) follows the note.

3. **minor: the read-only answer is only proven on the visible-editor path.** The case is
   `src/host-vscode/documents.ts:143-153`, as exercised by `sourceEdits.ts:110-117`.
   - The host checks the text only when the apply resolves true.
   - When the source file has no visible editor, `applyEdits` uses `workspace.applyEdit`. On a
     `files.readonlyInclude` file, that call may resolve false, and the user would see "VS Code
     could not apply the checkbox edit." instead of the read-only reason. It is unverified whether
     that path can also write despite the setting.
   - The integration test always shows the source in column One (`withPlan`), so it covers only
     `editor.edit`.
   - Expected fix: add an "Untested: …" sentence to the GFM-039 and GFM-021 verification notes.
     Example: "the read-only file with no visible source editor (workspace.applyEdit path) is
     untested". Alternatively, file a backlog item to probe it. No code change is required for this
     CR.

4. **nit: the Tab step starts from a scripted focus.** `test/integration/radioChoice.test.ts:223`
   (`frame.locator("p", { hasText: "Fix direction:" }).focus()`).
   - The Tab itself is real input, but reaching the label is not. v12/v13 already do it with a real
     click on the label.
   - Expected fix: replace `.focus()` with a real `.click()` on the label paragraph, as the visual
     scenario does, then `page.keyboard.press("Tab")`.
   - The `.focus()` at line 252 (Enter step) predates this CR. It could become one `ArrowDown` from
     the option that still has the focus after Space, but that is optional.

5. **nit: the text comparison can misjudge an external change during the apply.**
   `src/session/features/sourceEdits.ts:109-113`.
   - Case one: the apply changes nothing (read-only) while another writer changes the text before
     `.then` runs. The answer is then "saved" and the page keeps the new choice. The external
     change's content patch re-renders from the source right after, so the wrong state lasts one
     update.
   - Case two, the reverse: the edit lands and something restores the exact previous text. This is
     improbable.
   - Expected fix: none required. Optionally, add a one-line comment naming the race and why it is
     benign.

6. **nit: LIFE-119 still says "tabindex 0" for mapped blocks without the new exception.**
   `requirements/tiers/swrs/lifecycle-sync/SwRS-MDOKFSTUDIO-LIFE-119.md:92`.
   - LIFE-119 is proposed and the exception is written in GFM-039 ("a mapped block that already has
     a tabindex keeps it").
   - Expected fix (optional): append "or one that already carries a tabindex keeps it" to the
     LIFE-119 THEN, so the sanitizer's two requirements agree. Otherwise leave it.

## Observations (no action)

- In a mixed list (task items and options), the `ul` keeps its tab stop by design (GFM-039 boundary
  row), so Tab from the label takes two stops when the group starts the list. This is documented.
  It is consistent with the note, because the list there is not the group.
- The press guard also prevents a non-primary-button mousedown on a control while an editor is
  open. This is harmless: the context menu still opens.
- In `openEditorGuard`, the `finally` presses Escape and waits for the editor to close. If an
  earlier failure moved the focus out of the webview, this wait could mask the first error. That is
  acceptable for now.

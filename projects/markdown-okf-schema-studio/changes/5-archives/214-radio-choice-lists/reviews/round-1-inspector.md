# CR 214, round 1, Inspector review: radio choice lists

Worktree: `/Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-214` (uncommitted, on top of
04b71f01). I edited no code and committed, stashed or switched nothing. Scratch files are under
`/private/tmp/claude-502/cr214-driver/inspect-r1/`.

## Verdict: CHANGES REQUESTED (one small must-fix)

The implementation is sound, reuses the checkbox path, and is well tested. One rule in the spec table
("a heading ends the group") has a unit test that cannot fail for the reason it claims to test. The
fix is a one-line test change. Everything else is approvable as-is for round 1.

## Evidence by check

### 1. Rules of the spec table: implemented and unit-tested

| Rule | Where it is tested | State |
| --- | --- | --- |
| 2-item minimum, lone item stays text | `test/core/render/radioGroups.test.ts:66` | ok (passes on HEAD too, a valid boundary guard) |
| `( )` / `(x)` / `(X)`, space or tab after | `:76`, and `test/core/edits/radioSelect.test.ts:80` | ok |
| End of group: blank line, other list, non-radio item | `:89` | ok |
| End of group: heading | `:92` | **weak, see must-fix 1** |
| Mixed `[ ]` / `( )` list | `:101` | ok |
| No selection; two `(x)` rendered as written | `:116` | ok |
| Nested lists form their own groups | `:124` | ok |
| Label from the paragraph above (`aria-labelledby`) | `:35`, `:101`, `:124` | ok |
| Code stays literal; quotes, CRLF, frontmatter columns | `:136` | ok |
| Sanitizer keeps the roles and attributes | `:147` | ok |
| All palette modes | `test/page/runtimeRadioGroups.test.ts:214` | ok. The renderer does not depend on the palette mode (grep finds none), so rendering in every mode holds by construction. |

I also ran probes against the built worktree (`inspect-r1/probe/*.mjs`), and all of these behave
correctly:

- 2+2 items around a heading give 2 groups.
- A group inside a `:::{note}` gets its label.
- A loose list gives no group.
- Two groups in one list are split by a plain item.
- An ordered list works.
- A `( )` in a table cell stays text.
- A label paragraph that carries a `(lbl)=` anchor works.
- With frontmatter, the blank-line detection and the line numbers are right.

### 2. Interaction and ARIA

- **Edits:** a click writes one edit per changed option. The edits come from `planRadioSelect`
  (`src/core/edits/sourceEdits.ts:84`) and are applied in one `this.apply(document, edits)` call
  (`src/session/features/sourceEdits.ts:108`), which is the same one-undo-step apply as every other
  host edit (BLOCK-058). A normal group changes at most 2 lines. A group with two `(x)` changes up to
  3 lines on the first click, which is the normalisation the spec allows.
- **Clicking the selected option:** this returns before any message
  (`src/page/features/checkboxes.ts` `selectRadio`). The host also answers `unchanged` with no apply.
  Both are tested (page `:80`, session `:76`).
- **Keys:** Space and Enter select. The arrows, Home and End only move the focus and update the roving
  `tabindex`. The listener runs in the capture phase and calls `stopImmediatePropagation`, so block
  keys never see these keys. Tested at page `:132` and `:155`.
- **ARIA, whole list** (`ul/ol[role=radiogroup]` > `li[role=none]` > `p` > `span[role=radio]`): this
  is correct. ARIA 1.2 names no required owned elements for `radiogroup`, so the generic `p` in between
  is fine.
- **ARIA, partial group:** an empty `span[role=radiogroup][aria-owns=…]` sits in the first option's
  paragraph. This works in Chromium, which re-parents owned nodes itself, and the webview is always
  Chromium. It is the only way to keep the list a list in a mixed list.
  - Downsides: owned nodes leave their `listitem`s empty in the accessibility tree, and the group has
    no name unless it starts the list.
  - I accept it, because the spec says "the paragraph just above the list" and a mid-list group has
    no such paragraph.

### 3. Reuse of the checkbox guards and write path

The two controls share:

- one message type (`previewCheckboxToggle` plus an optional `radioGroup`);
- one host handler (`handleCheckboxToggle`), with the same `currentPreviewDocument` stale gate, the
  same `preview.edits.active` gate and the same answer;
- one page guard (`mayToggle`, which covers editing enabled, a valid position, busy and an open
  editor), one sender (`postToggle`), one pending map and one `showRefusal`;
- the read-only, stale and malformed gates in `src/session/pageMessages.ts`, unchanged.

Nothing is duplicated. Checkbox behaviour is unchanged:

- no existing test was edited;
- all 3317 unit tests pass;
- the shared `MARKER_PATTERN` cannot steal a `[x]`, because `(x)` and `[x]` cannot overlap, and a
  `(x)` that is not at the radio column is returned unchanged.

### 4. The new tests fail on the unchanged code (verified)

I extracted HEAD with `git archive` into `inspect-r1/head/`, symlinked `node_modules`, copied in the
new render, page and session tests and the new harness, then compiled and ran them.

- Result: **22 of 23 fail.** The one that passes is "a lone radio item stays plain text", which is
  expected because it is a boundary guard.
- The session test also fails to type-check, because `RADIO_GONE` does not exist on HEAD.
- `radioSelect.test.ts` cannot load on HEAD, because the `radioMarkers` module does not exist.

### 5. Real-input E2E (`test/integration/radioChoice.test.ts`)

- **Wiring:** it is registered in `test/integration/trusted-suite.ts` right after `checkbox-toggle`,
  under the same `!onlyRealInput` condition, so it runs in the heavy `ci-integration` job like the
  checkbox test.
- **What it does:** real CDP clicks and keys, then one `Meta/Control+z` in the editor that must
  restore the full source (this proves one undo step), then line-exact `changedLines` assertions.
- **What it avoids:** no retries, no `force`, no raised timeouts, and no assertion weakened.
  `waitForRender` and `currentPreviewFrame` match the document version, so it does not read stale
  frames.
- **Two points that are not defects:**
  - `assertNoWrite` waits a fixed 1.5 s to prove that nothing was written. The same pattern exists in
    `commentWrite.test.ts` and `previewEditing.test.ts`.
  - The test sets the focus programmatically (`locator.focus()`) before the arrow keys and before
    Enter, because a content patch replaces the DOM after a write. The keys themselves are real.
- I did not run it locally, as instructed. It compiles as part of `just check`.

### 6. Security of the `radioGroup` field

- **What `isRadioGroup` (`src/core/protocol/pageToHost.ts:97`) accepts:** an array of 2 to 256
  distinct `{line, column}` entries, where each line is a valid source line and each column a
  non-negative safe integer. The array must include the clicked position, and `checked` must be
  `true`. A `radioGroup` on any other message type is refused (`hasValidStateFields`).
- **How the host re-checks it:** `radioSelectEdits` re-reads every line against the current buffer
  and requires `radioMarkerColumn(line) === column`. Otherwise it refuses with `RADIO_GONE`.
- **What a forged message can do:** each edit replaces only the one character between the parentheses
  of a verified list-item radio marker, with `x` or a space. A malicious page therefore cannot make
  the host write arbitrary text, and edits cannot overlap, since a line has only one radio column.
- **The remaining gap:** see nice-to-have 1. The host does not check that the positions form one real
  group, so a forged message could clear `(x)` markers in other groups of the same document, up to 256
  of them.

### 7. Requirements and docs

- **SwRS-MDOKFSTUDIO-GFM-039:** `req_lifecycle: proposed`, derives from StRS-GFM-003. It has
  normative, nominal, boundary and refusal scenarios. Its `@implements_req` markers are in 7 source
  files and its `@tests_req` markers in 5 test files, and `implemented_in_files` and `tested_in_files`
  are generated.
- **GFM-027 (proposed):** gains `radioGroup` rows and the session test.
- **StRS-GFM-003 (proposed, not protected):** only the generated `derived_by` and Links lines changed.
- **No protected approved StRS was touched:** `git status` shows only GFM-003 among the StRS files.
- **User docs (`docs/user/editing.md`):** the new paragraph sits right after the checkbox paragraph
  and matches the behaviour, including the read-only case and the open-editor refusal.

### 8. Gates (run by me, in the foreground, nothing left running)

- **`just check`:** exit 0.
  - 3317 of 3317 unit tests pass.
  - 71 of 71 security tests pass.
  - 139 pytest tests pass.
  - The requirements stage validates "1072 requirements, 0 errors, 21 warnings".
  - The log is at `/private/tmp/claude-502/cr214-driver/inspect-r1/check.log`.
- **`uv run --group docs --group requirements okfreq validate --check-links --project-root .`:**
  "1072 requirements, 0 errors, 21 warnings". None of the warnings concerns GFM-039, GFM-027 or
  GFM-003 (they are pre-existing ones such as PALETTE-264).
- **Worktree after the gates:** `git status` is the same as before.

## Must-fix

1. **`test/core/render/radioGroups.test.ts:92`: the heading case cannot prove that a heading ends a
   group.**
   - Why: `"- ( ) a\n# Heading\n- ( ) b\n"` has one item on each side of the heading. It yields no
     radios because of the 2-item minimum, so it would pass even if headings did not end groups. The
     spec's Done-when asks for a unit test of every rule.
   - Suggested fix: use 2+2 items, for example `"- ( ) a\n- (x) b\n# Heading\n- ( ) c\n- ( ) d\n"`,
     and assert
     `groups(...)` equals `[["1:2: ", "2:2:x*"], ["4:2: *", "5:2: "]]`. I checked by probe that the
     current code gives exactly this.

## Nice-to-have

1. **`src/core/protocol/pageToHost.ts:97` / `src/core/render/radioMarkers.ts` `radioSelectEdits`:
   check the group shape on the host.** Require the positions to be in strictly ascending line order
   and to sit at one indentation, that is, one column (all options of a group share their column).
   This blocks a forged message that clears `(x)` markers across several groups. It is cheap,
   pure-function defense in depth.
2. **`requirements/tiers/swrs/gfm/SwRS-MDOKFSTUDIO-GFM-027.md:82`: the Criteria line was not updated.**
   It still says "column and checked are accepted only on previewCheckboxToggle". Add `radioGroup`.
3. **`src/core/preview/styles/contentLayoutStyles.ts:534`: ordered lists lose their numbers.**
   `li.myst-radio-item { list-style: none }` also hides the numbers of an ordered radio list
   (`1. ( ) a`). If option numbers matter in plans ("option 2"), keep `list-style` for `ol`. The round 2
   visual scenarios should look at this either way.
4. **`src/page/features/checkboxes.ts:261`: only the round control is clickable.** A click on the
   option text falls through to the block handlers. Native radio labels select on click, so selecting
   on a click in the item's first paragraph would match the "one click" promise better. This is a
   product call for the owner, not a defect.
5. **Focus is lost after a write**, because the content patch replaces the DOM. A keyboard user who
   presses Space loses their place in the group. The checkboxes behave the same way, so this belongs
   in a backlog item ("restore focus to the same control after a content patch") rather than in this
   CR.
6. **`test/integration/radioChoice.test.ts:68`: replace the fixed 1.5 s wait.** `assertNoWrite` could
   instead assert that the page posted no `previewCheckboxToggle` (if the harness exposes one) as well
   as the version check. This is optional, since the pattern already exists elsewhere.

Still to do in round 2 (out of scope here, listed for tracking): the README section with Cream and
Dark images, the demo fixture, the writing skill (constitution §6 requires it in the same PR), the QA
template, and the visual scenarios, which should include the CSS check of the
`--studio-input-*`/`--studio-focusBorder` tokens.

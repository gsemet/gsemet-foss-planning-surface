# CR 214 radio choice lists: round 3 Inspector review

**Verdict: APPROVE**

Round 3 is the polish round after the approved round 2. It covers nice-to-have items 2 and 3 of
`reviews/round-2-inspector.md`. Worktree: `markdown-okf-schema-studio-wt-214`, uncommitted on
`04b71f01`.

## 1. Scope: only the three expected files changed

The check lists the files modified after the round-2 review was written, outside `node_modules`,
`.git`, `out` and `.venv`:

- `.agents/guidelines/writing-skill-maintenance.guideline.md`
- `.agents/skills/markdown-studio-exploratory-qa-claude/references/qa-bug-template.md`
- `test/integration/radioChoice.test.ts`
- `.pytest_cache/v/cache/nodeids`, written by the gate and not part of the change.

Nothing else changed since round 2.

## 2. The two markdown rewraps

A word diff against `HEAD` shows only the CR's own additions, which round 2 already reviewed. The
rewrap changed no wording.

- **`writing-skill-maintenance.guideline.md`:** the 109-character line is split at the clause
  boundary, giving `front matter, radio choices in a plan) has no example,` (56 characters) and
  `or its example no longer renders as its own element;` (54 characters). This is the line layout
  `HEAD` already had, with only the new list item added.
- **`qa-bug-template.md`, the "Proposals and balance" paragraph (lines 93–98):** reflowed to
  93/81/98/95/98/13 characters. The short line "…; the fix CR" is gone. The 81-character line
  ends at a hard break that `HEAD` already had before the inline code.
- **Lines still over 100 characters:** guideline line 58, and template lines 10, 23, 30, 31,
  148–150, 201 and 202. They are all in `HEAD` already (code blocks and tables, shifted by the
  inserted lines). None is a touched line.

## 3. The "click the selected option" sync point

The change adds `waitFor("the click to focus the selected option", async () => await
focusedOption(frame) === 5)`. It sits between `radioAt(frame, 5).click()` and `assertNoWrite`.

### Option 5 is not focused before the click, so the wait proves something

- The last focus inside the frame went to option 7, clicked in step 1.
- After that, the frame re-renders twice: once for the write, once for the undo.
  `contentPatch` goes through `contentMorph.replace`, a keyed morph that uses `innerHTML`. It has
  no focus-restore logic: there is no `focus` or `activeElement` in `src/page/modules/contentMorph.ts`.
- `selectRadio` leaves the focus alone, and nothing in the page focuses the group's tab stop after
  a patch. Round 1 lists "focus back to the same control after a patch" as an open follow-up.
- So before the click, `document.activeElement` in the frame is either `<body>` or the line-7
  span. It cannot be option 5, and the wait can only pass if the click reached the page.

### Nothing in the page stops the focus on a radio mousedown

- `src/page/features/checkboxes.ts` binds only `click` (bubble phase) and `keydown` (capture
  phase). Both run after the mousedown default action, so neither can stop the focus.
  `selectRadio` returns early for the only selected option and calls no `preventDefault`.
- I checked every document- or window-level `mousedown` and `pointerdown` listener under `src/page`:
  - `blockSelectionView.ts:433` prevents only on Shift+mousedown in edit mode.
  - `commentCompose.ts:314` prevents only on its own button.
  - `linkTooltip`, `labelRename`, `commentThreads`, `tableCellEditor`, `toolbarCollapse` and
    `motion` close popovers or record a time stamp. They prevent nothing.
- The click listener of `checkboxes` is registered first, at `pageInput.ts:113`, ahead of the
  page's block-edit click handler, and calls `stopImmediatePropagation`. The capture-phase
  `bindEditModeCaptureClicks` handlers only match okf links and images inside links. So no click
  handler moves the focus away afterwards either.

### The click lands on the focusable element

- `radioGroups.ts` renders the round control itself as
  `<span class="myst-radio" role="radio" tabindex="0|-1" data-myst-radio-line=…>`, with no
  children.
- Playwright's `locator.click()` hits the centre of that 1em × 1em inline-block span. Step 1
  already relies on this hit target for option 7.
- In Chromium, a mousedown on an element with a `tabindex` attribute focuses that element: `-1`
  counts too, and option 5 has `0`. The iframe gets the focus at the same time. This also holds in
  nested VS Code webview frames: the arrow-key step already needs keyboard focus inside the same
  frame.
- `focusedOption` reads `document.activeElement` inside the frame, so it sees this focus even when
  the top-level workbench is unfocused.

### Timing

- `waitFor` polls every 25 ms, up to its default 10 s.
- The focus moves synchronously during the dispatched mousedown, before Playwright's click
  resolves, so the first poll should already pass. Heavy CI load cannot turn this into a hang
  unless the click never landed, and then a timeout is the right answer.
- The change adds no retry, no `force` and no raised timeout. `waitFor` accepts an async predicate
  (`() => boolean | Promise<boolean>`).

The new wait is a real, deterministic proof that the click reached the page, and it is not
vacuous.

## 4. Gate

`just check` was run in the foreground with exit 0. Log:
`/private/tmp/claude-502/cr214-driver/inspect-r3/check.log`.

| Stage | Tests | Pass | Fail |
|---|---|---|---|
| unit | 3320 | 3320 | 0 |
| contracts | 0 | 0 | 0 (same as round 2) |
| security | 71 | 71 | 0 |
| pytest | 139 passed, 12 warnings | | |

- `check-boundaries`, `check-limits` and `check-settings` passed. The okfreq checks report
  0 changes.
- The counts are the same as the round-2 log.
- No process was left running.
- I ran no real-window test locally.

## Must-fix

None.

## Nice-to-have

1. **`radioChoice.test.ts`:** an `assert.notEqual(await focusedOption(frame), 5)` before the click
   would make the non-vacuity explicit in the test. Today it rests only on the analysis in
   section 3.
2. **Carried over from round 2:** dispatch heavy CI on the PR. The integration test has still only
   compiled, never run. Round-2 items 4 to 6 (high-contrast ring, stress-plan note, backlog
   follow-ups) also still stand.

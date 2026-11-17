# CR 217 round 1: Inspector review

Worktree: `markdown-okf-schema-studio-wt-217` (uncommitted, base origin/main 0b4ede78).
Inputs: round1-task.md (items 1-7), reports/behaviour-note.md (owner approved 2026-10-31), rules.md.

VERDICT: CHANGES

## Required changes (blocking)

1. **The follow hint is duplicated after a re-render, and the duplicate leaks into reading mode.**
   `src/page/features/contentPatch.ts` (lines 37-42) saves each link's `title` before the morph and
   puts it back on the new link elements with `applyLinkHint`. In edit mode that saved title already
   ends with `\nCtrl+click to follow`. The new element has no `data-sphinx-preview-follow-hint`
   attribute, so `applyLinkHint` does not re-sync it. `applyEditMode` → `syncLinkFollowHints` then
   treats the whole hinted title as the base and adds a second hint line.
   Reproduced in a scratch copy with the runtime harness. The link has a known target, edit mode is
   on, and a content patch replaces the link element:
   - after render: `"/ws/related-target.md\nCtrl+click to follow\nCtrl+click to follow"`
   - after edit mode off: `"/ws/related-target.md\nCtrl+click to follow"`. Item 6 says reading mode
     must keep the original title, so this fails it.
   This is the normal flow the CR enables: click a link, edit its paragraph, save. The block's HTML
   changes, so contentMorph rebuilds its link. The `discovered` set stops the target from being
   asked again, so nothing fixes the title. Every further edit adds one more line.
   Fix: keep the base title when the hints are saved before the morph. Read
   `data-sphinx-preview-link-title` when the follow-hint attribute is set, through a small exported
   helper in linkNavigation.ts. Another option is to make `applyLinkHint`/`setLinkFollowHint`
   remove a trailing hint line. Add a unit test for this case: a link with a link-state and a hinted
   title, then a patch that replaces the element, then a single hint line, then reading mode back to
   the bare target. The current test "the follow hint survives a later target hint and a content
   render" uses a link with no earlier target, so it misses this.

## Checked and OK

- **Item 1, click/Enter/Space in edit mode.**
  - `linkActivationEdits` (new `src/page/features/linkEditing.ts`) is true for a plain click, Enter
    or Space on a link inside a mapped block.
  - linkNavigation `activate` returns early and posts no previewLink. pageInput then opens the
    editor and calls `preventDefault` on both the click path and the keydown path.
  - Linked images still go through the capture listener in `bindEditModeCaptureClicks`. It stops
    immediate propagation, so there is never a second previewEditOpen.
  - Same-page anchors, footnote refs and external URLs all match `closest("a")`.
- **Item 2, Cmd/Ctrl, middle click and reading mode.**
  - Cmd/Ctrl+click and Cmd/Ctrl+Enter make `linkActivationEdits` false. Navigation then runs
    through `beforeNavigate`, so `flushOpenEditorsThen` and flushBeforeNavigate still apply.
  - `auxclick` always follows.
  - Reading mode is unchanged: click, Enter and Space follow. Reading-mode Space is still taken by
    linkNavigation, as before.
- **Ctrl+click on macOS.** Chromium on macOS turns Ctrl+click into a context menu with no `click`
  event, so it does not follow. This matches the existing linked-image code, which also accepts
  both keys, and the macOS hint says "Cmd". Consistent.
- **Item 3, links outside a mapped block.** These keep their behaviour:
  - properties-table `okf-link:`: the capture field editor is unchanged, and so is its Cmd click
    (unit test).
  - comment-body links, chips, label anchors and links inside an open editor: `linkEditTarget`
    excludes them.
- **Blocked links.** A Cmd+click still posts previewLink, so the host warning still shows.
- **Item 4, `:link:` cards.**
  - The edit-mode-only rule `pointer-events: none` on `.myst-grid-card-link::after` works.
  - The linked title is now mapped to the directive line (`mystGridToctree.ts buildCard`).
  - Reading mode keeps the stretched overlay.
- **Item 5, hover and cursor.** `editHoverTarget` no longer excludes links. The card-hover shot
  outlines only the body paragraph. The cursor rule is text, with no key tracking.
- **Item 7, open editor and QA215-01.**
  - A click on a link while another editor is open takes the BLOCK-041 path: save first, no
    previewLink (unit test).
  - The real-input E2E types " F" after the footer click and asserts that the textarea holds it and
    that `targets/alpha.md` is neither shown nor dirty.
- **Hint wording.** It uses `isApplePlatform()` (the existing helper). It is set only in edit mode,
  it survives `applyLinkHint` on the same element, and repeated toggles do not duplicate it.
  Blocking item 1 is the exception.
- **Listener order.** `bindEditModeCaptureClicks`, then linkNavigation, then `input.bindClicks` is
  unchanged. pageInput still owns `preventDefault` for an edited link.
- **Tests fail on the old code.** I compiled HEAD `src/` with the new tests in a scratch copy and
  ran linkEditModeClick, blockReq.requirements and gridCardTitleSourceLine: 15 fail, 37 pass. That
  matches the Coder's claim.
  - The tests that pass on the old code (Cmd/Ctrl click, Cmd/Ctrl+Enter, middle click, reading
    mode, Cmd click on the card title, the properties-table link, no hint on the properties table)
    guard behaviour that does not change. I accept them as regression guards.
  - No force, retry or longer timeouts.
- **Changed assertions.** All 5 in blockReq.requirements.test.ts and the linked-title case in
  gridCardTitleSourceLine.test.ts follow from the owner's new rule. Each is commented "CR 217
  changed the rule", and none is weaker than before.
- **Real-input E2E** (`test/integration/realInput/linkEditMode.ts`). It does real Playwright clicks
  on the link-only paragraph and on the card footer, types " F", checks that alpha is not dirty, and
  does a MOD+click that navigates to related-target.md. It is registered in the full `run()`
  sequence (heavy run) and as the single scenario `link-edit-mode`. It compiles.
- **Requirements.** Every changed requirement file has `req_lifecycle: proposed` before and after:
  BLOCK-014, BLOCK-017, BLOCK-041, BLOCK-258, FMEDIT-001 and TOOLBAR-077. No approved requirement
  changed, generated lines included.
  - The BLOCK-041 and FMEDIT-001 changes are only generated `tested_in_files` lines.
  - The BLOCK-017 edit is justified by item 5: the hover rule for links changed.
  - The markers match the lists.
- **Shots.** The after shots use the same framing as the before shots, 900 px, top scroll. Cream is
  really Cream (beige page, brown accent) and Dark is dark. They show the approved behaviour: the
  editor on the link-only paragraph (line 5), the editor on footer line 21 inside the card, the
  outline on the link-only paragraph, and the outline on the card body only.
- **Gates (rerun by me).**
  - `just check`: exit 0. Unit 3336/3336, security 71/71, release-tests 153 passed, coverage
    `0 files would change`.
  - `UV_NO_CONFIG=1 uv run --group requirements okfreq validate --check-links --project-root .`:
    1072 requirements, 0 errors, 21 warnings. All 21 warnings are older and none is in a changed
    file.
  - The worktree status was identical before and after the gates.

## Optional notes (non-blocking)

- **Card-hover visual assertion is weak** (`linkEditModeScenarios.ts` card-hover). The `text`
  check is "includes", so an outline on the whole card would pass too. Use a selector such as
  `${CARD} .myst-grid-card-body [data-sphinx-preview-edit-hover="true"]`, or add a count-0
  assertion on `.myst-grid-card[data-sphinx-preview-edit-hover]`.
- **No link-follow-on-card check in the E2E.** It only Cmd/Ctrl+clicks the paragraph link. A
  MOD+click on the card title would cover the card's follow path end to end.
- **The `_evidence` parameter is unused.** Other real-input scenarios record a screenshot.
- **Robustness: `activate` never calls `preventDefault`.** When `editsInstead` is true, linkNavigation
  relies on pageInput to call `preventDefault`. If a future early return in the pageInput click
  handler (tab list, insert point and so on) ever sees a link, the browser follows the anchor's
  `href` by default. Calling `event.preventDefault()` in `activate` before the early return would
  be safer.
- **Cursor and hover include links that keep their own behaviour.** The text-cursor CSS and
  `editHoverTarget` also apply to links that `linkActivationEdits` excludes, such as comment-body
  links and chips, which still follow on a plain click. This is cosmetic.
- **Slight mismatch in what counts as a link.** `linkActivationEdits` matches any `a`, while the
  hint and cursor only match `a[data-sphinx-preview-navigation]`. This is harmless today.
- **Cosmetic file details.** In `realInput/markers.ts`, TOOLBAR-077 is inserted between TABLE-094
  and THEME-001, out of order. c3-1 JSON lost its trailing newline.

# CR 217 round 2: Inspector review

Worktree: `markdown-okf-schema-studio-wt-217` (uncommitted, base origin/main 0b4ede78).
Inputs: round2-task.md, round1-inspector.md, the approved behaviour note, rules.md.

VERDICT: APPROVE

## Required changes (blocking)

None.

## Round-1 blocking item 1 (duplicate hint line): fixed

- `linkBaseTitle()` (src/page/modules/linkNavigation.ts) returns the stored base title only when the
  current title is exactly `base + "\n" + hint`. Otherwise it returns the title as it is.
  `contentPatch.ts` saves that value before the morph. The rebuilt link gets the bare title back
  through `applyLinkHint`, and `applyEditMode` → `syncLinkFollowHints` then adds exactly one line.
- The new test "edit mode: a content render that rebuilds a hinted link with a known target keeps
  one hint line" fails on the round-1 code. I checked this in a scratch copy by reverting only
  `contentPatch.ts` to `link.getAttribute("title")`. With the fix it passes. It covers one render,
  two more renders and the return to reading mode.
- I ran extra edge cases in a scratch copy (throwaway test, now deleted). All of them pass with the
  fix, and 4 of them fail without it:
  - A. A later `previewLinkTargets` with a new path while the hint is shown. The title becomes
    `new\nhint`. Two rebuilding renders keep one line on the new path, and reading mode shows the
    new path only.
  - B. Edit mode toggled 5 times, with a rebuilding render in each state. There is never more than
    one line, and reading mode is always bare.
  - C. A host title that already ends with "\nCtrl+click to follow". It is kept intact as the base
    in edit mode, after renders and in reading mode. The exact-match rule protects it.
  - D. A link with its own Markdown/link-alt title and no target state. It shows `Alt\nhint` in edit
    mode, the same after renders, and `Alt` in reading mode.
  - E. A link in an unchanged block, where the morph keeps the element and its attributes. Three
    renders keep one line, and reading mode is bare.
  - F. A link with no title. Edit mode shows the hint only, and reading mode removes the title
    attribute.

## Whole diff re-checked against the approved behaviour

There is no regression since round 1.
- Click, Enter and Space in edit mode edit the block. Cmd/Ctrl, middle click and reading mode
  follow the link.
- Excluded links keep their behaviour: the properties table, comment bodies, chips, anchors and
  links inside an open editor.
- On a linked card, each part opens its own line, and the overlay `pointer-events: none` applies in
  edit mode only.
- Listener order is unchanged. Cmd+click still goes through `flushOpenEditorsThen`.
- Requirements: BLOCK-014, BLOCK-017, BLOCK-041, BLOCK-258, FMEDIT-001 and TOOLBAR-077 are still
  `req_lifecycle: proposed`, both in the base and here. No approved requirement was touched.
- Round-2 extras:
  - The card-hover selector is now scoped to
    `.myst-grid-card-body p[data-sphinx-preview-edit-hover="true"]`, so an outline on the whole card
    would not match.
  - The real-input E2E adds a MOD+click on `a.myst-grid-card-link` ("Linked card") and asserts that
    the preview shows `targets/alpha.md`. The selector matches the class from `mystGridToctree.ts`.
    It compiles. Not run here: no local real-window tests.
  - The markers are in alphabetical order now.
  - c3-1 JSON: origin/main has no trailing newline and the worktree file ends with one, so the
    Coder is right and my round-1 note was wrong.
  - Item 5 (`any a` vs `a[data-sphinx-preview-navigation]`) stays as it is. The Coder's reason is
    acceptable: the sanitizer sets the attribute on every content link that has an href.

## Visual scenarios (real harness, lock held as owner 217, released)

The lock was held by 226 at first. I waited until `mkdir` succeeded, then ran `npm run visual:render`
and `test/visual/capture.py --scenario …` for the 8 ids:

| Scenario | Result |
|---|---|
| block-editing/v27-link-edit-mode-linkonly-click-cream-900 | passed |
| block-editing/v28-link-edit-mode-linkonly-click-dark-900 | passed |
| block-editing/v29-link-edit-mode-linkonly-hover-cream-900 | passed |
| block-editing/v30-link-edit-mode-linkonly-hover-dark-900 | passed |
| block-editing/v31-link-edit-mode-card-click-cream-900 | passed |
| block-editing/v32-link-edit-mode-card-click-dark-900 | passed |
| block-editing/v33-link-edit-mode-card-hover-cream-900 | passed |
| block-editing/v34-link-edit-mode-card-hover-dark-900 | passed |

Summary: `{"status": "passed", "scenario_count": 8, "screenshot_count": 8}`. The click frames show
the editor on the right line: the footer, line 21, inside the card. The lock was released by removing
the owner file (it held 217) and then the directory.

## Gates (rerun by me)

- `just check`: exit 0.
  - unit 3337/3337 (one more than round 1: the new test)
  - security 71/71
  - release-tests 153 passed
  - coverage `0 files would change`
- `UV_NO_CONFIG=1 uv run --group requirements okfreq validate --check-links --project-root .`:
  1072 requirements, 0 errors, 21 warnings. These are the same older warnings as before, and none is
  in a changed file.
- `git status --short` was identical before and after the gates and the capture.

## Optional notes (non-blocking)

- **Hover frames show no visible outline.** In the harness PNGs of v29/v30/v33/v34 I see no dashed
  outline. The content assertion did pass: the scoped `[data-sphinx-preview-edit-hover="true"]`
  element exists after the hover. The final screenshot is taken after `check_final_frame`, so the
  outline seems to be lost or too faint at that point. The frame therefore does not show what its
  lock text says. This is a harness or framing issue, not a product defect, and the Coder's separate
  after-shots do show the outline. Consider a `steps: ["hover"]` capture, or accept it as is.
- The round-1 optional notes left on purpose are still open and still non-blocking:
  - `_evidence` is unused in the E2E.
  - `activate` does not call `preventDefault` before its early return.
  - Cursor and hover also apply to comment-body links and chips.

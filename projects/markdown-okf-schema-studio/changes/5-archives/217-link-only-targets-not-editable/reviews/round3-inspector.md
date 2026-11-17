# CR 217 round 3 — Inspector review

Scope: uncommitted delta on top of 0ebe4b26 in `markdown-okf-schema-studio-wt-217`
(editModeStyles.ts, editMode.ts, linkEditing.ts, linkEditModeClick.test.ts, runtimeHarness.ts,
BLOCK-014, BLOCK-017, block-editing/index.md).

VERDICT: APPROVE

## Findings

1. **Owner rule holds, from one rule.** `linkEditTarget` is the only rule, and three places use it:
   - `linkActivationEdits` uses it. The logic is the same as in round 2:
     `closest("a") && !(closest("a") && !target)` is `closest("a") && target`.
   - `editHoverTarget` uses it through `inLinkThatKeepsItsBehaviour`.
   - `syncLinkFollowHints` uses it to set the marker `data-sphinx-preview-link-edits="true"`.

   The CSS text-cursor rule for links now depends only on that marker, so no second list is kept by
   hand. These links keep the pointer cursor and get no outline: links in comment-thread bodies,
   `okf-link:` and properties-table links, links in an open editor, and links outside a mapped block
   (the toolbar). Chips and label anchors are `span`s, not links, so their behaviour has not changed
   since base.
2. **Nothing approved in round 2 regresses.**
   - The click, keyboard and hint behaviour is unchanged (same predicate).
   - Paragraph and card-part hover still outlines the block or the part.
   - The cursor rule lost the `#sphinx-myst-preview-content` ID specificity. I searched every
     preview stylesheet: no author rule sets `cursor: pointer` on content links. The only one targets
     `[data-okf-properties] .okf-frontmatter-link`, which should keep the pointer anyway. So the
     marker rule still wins over the browser's default link cursor.
   - Every `href` the sanitizer keeps gets `data-sphinx-preview-navigation`, so the marker covers
     every link the click rule can edit.
3. **The tests are genuinely red.** I copied the worktree to scratch, put back the three src files
   from HEAD, compiled, and ran the tests. 3 of 20 fail, the same 3 as the coder's red output:
   - comment-body hover;
   - paragraph marker;
   - stylesheet selector.

   The properties-table test passes on HEAD, as a guard, as the coder said.

   The harness `closest` extension (`.okf-comment-body` / `.okf-chip` / `.okf-anchor`, matched by
   class) can only make exclusions match. A false match would be caught by the positive
   paragraph-link test. The `blockReq` tests use their own `SelectorElement`, so the extension does
   not touch them. The full suite stays green.
4. **The marker stays correct after a render or patch.** Every content patch runs
   `initializeContent` → `applyEditMode` → `syncLinkFollowHints`. Content morph keeps unchanged
   blocks together with their marker. Frontmatter/properties markup that is inserted later never needs
   the marker. Any link added without a sync falls back to having no marker, which means the pointer
   cursor, the safe default. So a link can never be left with a wrongly applied text cursor. The
   worst case is a pointer cursor on an editable link until the next sync, which is cosmetic.
5. **Requirements: only proposed ones changed.** BLOCK-014 and BLOCK-017 are both
   `req_lifecycle: proposed`. The index line is regenerated, and coverage is in sync
   (`update-coverage --check`: 0 files would change).
6. **Shots: none need retaking.** Cursors are not captured in the shots. The paragraph and card
   outlines are unchanged, and no shot shows a comment-body or properties link being hovered.
7. **Gates (rerun in the foreground):**
   - `just check`: exit 0, with 3341/3341 unit, 71/71 security, and indexes, projections and
     coverage all in sync.
   - `UV_NO_CONFIG=1 uv run --group requirements okfreq validate --check-links --project-root .`:
     1072 requirements, 0 errors, 21 warnings (all existing W2 placeholder cross-links in PALETTE-217
     and PALETTE-264).

## Required changes (blocking)

None.

## Optional notes

- `editHoverTarget` still has its own `[data-okf-properties]` / block-editor checks. They are still
  needed for hovered nodes that are not links, so they are not a duplicate of the link rule.
- No test re-checks the marker after a content patch. This is covered by reasoning (point 4). A
  one-line assertion next to the existing "content render keeps one hint line" test would pin it.

# 123 — The block edit toolbar never covers the edited content

Type: fix · Priority: P2 · From backlog: `02-backlog/P2/edit-toolbar-covers-text`

## Intent (user)

# Block edit toolbar covers the text being edited

User report (2026-10-26), seen on the after-screenshot of the edit-toolbar tooltip fix:
when the toolbar wraps to two rows (narrow preview), it overlaps the block editor and hides the
lines being edited (red arrow: the first text lines under the second toolbar row). The user
cannot tell what they will see under it.

![image.png](image.png)

Evidence: [after-cream-cr112.png](after-cream-cr112.png).

Expected: the toolbar never covers the edited text. Options to weigh: reserve its height above
the editor (push the editor down), place it above the block when there is room, or collapse
the second row into an overflow menu at narrow widths.

## Second case: the figure edit panel (2026-10-26)

The same overlap hides the top of the figure edit panel: the second toolbar row covers its
title ("Figure") and top edge (red arrow).

![image-figure-modal.png](image-figure-modal.png)

Evidence: [after-cream-cr117.png](after-cream-cr117.png). The fix must cover every panel opened
inside the block editor (figure, table, admonition…), not only the text area.

## Autonomous decisions

- Decided by the main session on 2026-10-26 under the user's instruction "pas de questions, full autonome". List these in the PR body under "Autonomous decisions".
- The toolbar takes its real height in the layout above the block editor (in flow, no overlap); when it wraps to two or more rows the editor and any panel inside it (figure, table, admonition…) move down accordingly.
- If the toolbar is sticky while scrolling a tall block, the editor reserves the same height so the first lines stay visible under it.
- Proof: before/after screenshots at a narrow preview width reproducing both user images (text area and figure panel), plus a layout test asserting the toolbar's bottom edge is above the editor's first line.

## Extra round (2026-10-27)

- rounds: 4. Granted by the main session under the user's "full autonome" instruction: heavy CI on the stack top fails in `test/integration/editToolbarCover.test.ts` ("Timed out waiting for the Edit figure button to be shown", state present:true hidden:true hovered:FIGURE editMode:on); run https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40432564443.
- Round 4 scope: find why `figureEditButton.sync()` leaves the button hidden after the round-2 `usableTop` change (`src/page/modules/figurePanel.ts`, `src/page/runtime.ts`, `editMode.ts`); a figure under the sticky toolbar must still get a reachable Edit button. Fix the product or the test without weakening it.
- rounds: 5 (2026-10-27, main session, "full autonome"). Heavy re-run https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40438469087: the Edit figure click now works, but `editToolbarCover.test` line 228 times out in `closeEditor` ("block editor to close"). Check first whether the toolbar now covers the Done button or the close path, i.e. a product issue this very CR must prevent. CR 123 moves to the top of the stack so it never blocks the others.

- rounds: 5. Granted by the main session (2026-10-27): editToolbarCover test times out in closeEditor (line 228) in heavy CI; check whether the toolbar covers the Done button or the close path.

## Rework after the stack merge (2026-10-27, user)

- rounds: 6. The rest of the stack (107…120, 124) is merged into main; #128 stays open on its own.
  Rebase the branch onto origin/main first.
- **Tall block, the user's rule**: for a block taller than the viewport, it is accepted that the
  floating toolbar covers the first lines of the text. The toolbar sticks at the top of the pane
  (just under the preview controls), the text scrolls under it. The "never covers" rule applies
  only to blocks that fit in the viewport, at opening time.
- **Bug 1, toolbar too low** (user's image `image-tall-block-toolbar-low.png`, CR 123 tall-block
  scenario): the toolbar sits in the middle of the block (over lines 05–07) instead of at the top
  of the pane (where lines 01–02 are, red box and arrow).
- **Bug 2, scroll jumps to the top** (user, 2026-10-27, backlog
  `02-backlog/P1/bug-tall-block-scroll-jumps-to-top`): empty Markdown file, edit mode, paste a very
  large text; scrolling down inside the open block brings the page back to the top. Suspected cause:
  the tall-block clearance / layout anchor of this CR in `src/page/features/editorChrome.ts`.
  First reproduce on main and on this branch to confirm the cause, and say so in the report.
- Proof: real-window e2e that opens a block taller than the viewport, scrolls down step by step
  (wheel) and asserts the page never moves back up and the toolbar stays at the top of the pane;
  it must fail before the fix. Before/after screenshots in a real window, cream theme, matching the
  user's image. Then heavy CI on the branch (`gh workflow run ci.yml --ref <branch> -f heavy=true`).

# CR 189: Inspector review, round 1

Verdict: **CHANGES REQUESTED** (one doc fix; the code and the tests are sound)

Reviewed: the uncommitted changes in worktree wt-178 (on top of ca12066f), 7 modified and 3 new files.

## Checks

1. **Diagnosis is credible.** The page CSP (`style-src` with a nonce only) blocks the `<style>` that
   Mermaid writes into its SVG while it measures the HTML labels in the page. So the labels are measured
   with the inherited page font and size, and drawn in the data-URI image with Mermaid's own style
   (16px). The coder's before-fix numbers show exactly the four labels in the bug report cut by 2 to 5px
   ("Yes" 25.7 > 22.9, "No" 20.7 > 18.4, "Review telemetry" 124.6 > 120, "Hold and inspect" 122.7 > 120).
   The fix pins a system font stack and 16px on both sides: the Mermaid config and theme for the image,
   and a `.myst-mermaid-measure` element in the nonce'd page stylesheet for the measure. This matches the
   cause. `htmlLabels` is not touched.
2. **The test fails on the bug and passes with the fix.** I re-proved this myself on a scratch copy of the
   worktree. I ran nothing in the worktree and left it unchanged.
   - HEAD (ca12066f) versions of `mermaidPreview.ts` and `contentBlockStyles.ts`: `mermaidLabelFit.test`
     **fails**, cutting "Yes", "No", "Review telemetry" and "Hold and inspect", with the same numbers as
     the coder's log.
   - origin/main (cb1f2adc) versions: **fails** in the same way.
   - Worktree (fix) versions: **passes** 3 out of 3 runs, light and dark themes, not skipped.
   - On the buggy code, the check that the in-page measure agrees with the separate SVG document
     (within 0.5px) passes, and the fail comes from the image-cut assertion. So `measureMermaidImageLabels`
     sees the cut labels too.
3. **No weakened assertions.**
   - No forced passes, no retries and no `htmlLabels: false`.
   - The only skip is `t.skip` when no Chromium can start, the same pattern as the existing chart page
     tests.
   - The real-window check is stricter than before. It asserts the exact set of 6 labels (before, it was
     "at least 3 nodes, at least one edge label"). It now measures what the image draws, where before it
     measured the page.
   - The new test filters only `Applying inline style violates` console errors. This is the expected CSP
     block of Mermaid's in-page style attributes. It was already there before the fix and is documented
     in the test.
4. **The real-window check measures what the image draws, and fails on the bug.** `previewWindow.ts` now
   calls `measureMermaidImageLabels(src)` on the shown `img` src: a shadow root under an `all: initial`
   host, the SVG's style sheet given back as a constructed sheet, and the style attributes set through
   the CSSOM. The result depends only on the image src plus system fonts. The headless test proves that
   it agrees with the SVG opened as its own document, on both the buggy and the fixed code. The demo
   flowchart in the real-window check is the same as the one in the unit test.
5. **Security is unchanged.**
   - No change to the CSP, `webview.ts`, `normalizeSvgForDataImage` or `securityLevel: "strict"`.
   - The new CSS rule lives in the existing nonce'd stylesheet.
   - The measure div holds no user content. It is hidden, off screen, out of the flow, and removed in a
     `finally` block. Mermaid used a temporary div in `body` before, so nothing new is exposed.
   - `--allow-file-access-from-files` is passed only to the test browser in `chartPage.ts`.
6. **No StRS file changed.** Only `SwRS-MDOKFSTUDIO-DIAG-001` changed, and its new scenario is accurate.
   The CHANGELOG text is accurate. One SwRS is now stale, see below.
7. **Tests.** `tsc` is clean. Page, core/preview, session and security unit tests: 2042/2042 pass, 0
   skipped (run on the scratch copy, which has the same content as the worktree).

## Changes requested

1. **Update `requirements/tiers/swrs/diagrams/SwRS-MDOKFSTUDIO-DIAG-005.md`.** Its lifecycle is
   proposed, so it can be edited. Today it says that the Mermaid font comes from the theme:
   - description and normative text: "take its colours **and font** from the preview theme variables";
   - table row "Font | --sphinx-preview-font";
   - fallback "… and the sans-serif font".

   The code no longer does this (`fontFamily: MERMAID_FONT_FAMILY`, a pinned system stack, plus a pinned
   16px). Drop the font from DIAG-005, colours only, and point to DIAG-001 for the pinned font. This keeps
   the SwRS in line with what the code does.

## Outstanding proof (driver, not a code defect)

The CR's "Proof (all required)" items are not done yet:

- a heavy real-window run, with a picture showing "Yes", "No" and "Hold and inspect" whole;
- `images/readme/myst-diagrams-and-figure.png` regenerated from that run.

Until both are done, #191 stays draft.

## Minor notes (no change needed)

- On Linux CI, `-apple-system` and `BlinkMacSystemFont` do not resolve. The stack falls back to
  Ubuntu, Arial or sans-serif, the same font on both sides, so the fix holds.
- The node shape check in `cutLabels` skips a node with no shape found (`shapeWidth` undefined). The
  exact label-set assertion covers the risk of missing nodes.

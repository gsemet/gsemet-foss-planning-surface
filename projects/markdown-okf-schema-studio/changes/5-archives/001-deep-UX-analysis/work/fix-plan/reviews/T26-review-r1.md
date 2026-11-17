# T26 review — round 1

Base: 4b2d6b8 · Reviewed diff: 7 files, +276/-6 (src 3 files +67/-6, tests 4 files +209/-0)

## Gates
unit: PASS (logs/T26-unit.log) · types: PASS · contracts: PASS · trusted: PASS, exit 0, RI-T26 included
(logs/T26-trusted.log) · visual: PASS vs baseline. The normalized failure list adds no lines to the
T00 baseline (logs/T26-visual-*-normalized.txt). The remaining failures are the known baseline
sticky-heading cases.

## Done-when
- [x] Invalid values show icon + plain label, no `[E10]`. Evidence: propertiesTable tests "invalid
  links show an icon and a plain label…" and "unavailable links use the warning icon". RI-T26 asserts
  `File not found` is visible and `[E10]` is not.
- [x] Full message (code included) in the custom tooltip on hover and keyboard focus. Evidence: unit
  test "an invalid link span shows its full message in a tooltip on keyboard focus". RI-T26 reaches the
  span with Tab and gets a `[role=tooltip]` containing "does not resolve". Screenshot 34 confirms it.
- [x] `title` unchanged. `linkTitle` is untouched, and the span keeps `title="${linkTitle(link)}"`.
- [x] The badge is a `<button>` with all its data attributes and an aria-label. It scrolls to the
  first issue row, focuses it and highlights it for 1.5 s. Evidence: the unit badge test and the
  RI-T26 badge step, which scrolls away first and then checks that the row is in the viewport and
  holds focus.
- [x] `linkStatusLabel` covers every message family in `fileLinks.ts`: does not resolve, escapes
  (both forms), root is unavailable, absolute target, is ambiguous, is empty, plus the E10/W15
  fallbacks.
- [x] Screenshot in each theme. The RI dark capture was reviewed. A light capture is not required:
  see finding 4.

## Deviations judged
1. The selector `.okf-frontmatter-link:not([data-okf-link-status="pending"])` is acceptable.
   `propertiesTable.ts` is the only producer of `.okf-frontmatter-link`, and it has three branches:
   - the valid `<a>`, with `data-okf-link-status="valid"`;
   - the pending span, which is excluded;
   - the invalid/unavailable span, with a status.

   No production element carries the class without a status, so the presence requirement changes
   nothing. Valid links behave as before. They still match the selector, so they get the same tooltip
   path. Their markup, excerpt span (native title) and `okf-link-with-details` wrapper are unchanged
   (P-R7). Navigation is untouched (P-N6): the capture-phase edit click and `installLinkNavigation`
   still key on `a[data-sphinx-preview-navigation^="okf-link:"]`. The only `pointerdown` difference:
   a press on an invalid span whose tooltip is open now keeps the tooltip instead of closing it. That
   is harmless.
2. RI-T26 with `resolution: document-relative` is acceptable. It yields the E10 "does not resolve"
   message the scenario must assert. A project-relative resolution could produce W15 "root
   unavailable" in the fixture workspace. The label mapping for the root-unavailable family is
   covered at unit level.

## Protected features checked
- P-R7: valid anchor markup, excerpt and title are byte-identical apart from the shared `statusLabel`
  computation, which is unused for valid links. The YAML-style display (`formatScalar`, `- item`)
  is untouched, so UX-24 is not affected. The propertiesTable suite passes.
- P-N6 / UX-22: `fileLinks.ts` and `okfFrontmatter.ts` have no diff. The messages, codes and
  resolution are unchanged. `data-okf-link-code` is preserved on the outer span.
- P-E7, keyboard paths:
  - The badge is a BUTTON. The global keydown handler returns early for BUTTON, so Enter or Space
    become a native click, which the badge handler takes.
  - The badge sits in `.okf-properties-title`, outside every `[data-okf-edit-cell]`.
  - The badge handler stops propagation only when `closest("[data-okf-badge]")` matches, so no other
    click can be swallowed. It does not intercept the description toggle, edit cells, list or field
    action buttons (T21/T23/T24), or mapped blocks.
  - The new `tabindex="0"` span lives inside the value cell. In edit mode, Enter on it resolves
    `closest("[data-okf-edit-cell]")` and opens the value editor, the same as Enter on the cell.
  - A click on it still opens the editor through the existing cell handler, because it is not an
    anchor.
  - Badge focus sets `tabindex="-1"` only when the cell has none. `setFrontmatterEditCells` later
    overwrites the attribute or removes it, so there is no conflict.
- P-E8: the badge navigates only. It edits nothing and posts no message, so it is safe in read-only
  previews.
- P-S2/P-S4: no new message types. The label passes through `escapeHtml`, and the code is escaped.
  The tooltip uses `textContent`.
- P-L7: see finding 4.
- Conventions §2: the template has no backticks or `${`, the quotes in the selector are escaped as
  `\\"`, and the code uses `window.setTimeout`.

## Findings
1. [MINOR] test/webview/scrollSync.test.ts: "the badge click scrolls to and focuses…" — the assertion
   `focusOptions !== undefined || scrollY !== 900` is a disjunction, so it does not prove focus.
   Fix: assert that `harness.frontmatterValueCell.focusOptions` deep-equals `{ preventScroll: true }`.
   If the harness can record it, also assert that `scrollIntoView` was called with
   `{ block: "center" }`. RI-T26 already proves the real behaviour, so this is not blocking.
2. [MINOR] src/webview/scrollSync.ts badge click handler — when no row carries an issue class, the
   click does nothing. This can happen when the only issue is the missing-required summary. Fix
   (follow-up): fall back to focusing the missing-required summary element or the properties title.
   Add a unit test with a badge and no issue row.
3. [NIT] src/frontmatter/propertiesTable.ts `linkStatusLabel` — the `"was not found"` branch matches
   no message in `fileLinks.ts`. It is harmless, but you can drop it.
4. [MINOR / no light capture required] No light-theme capture with an invalid link exists. All the
   new colours come from theme variables:
   - the label inherits `.okf-link-invalid` → `--vscode-errorForeground` (fallback `#f14c4c`), or
     `.okf-link-unavailable` → `--vscode-descriptionForeground` (fallback `GrayText`);
   - the badge uses `color: inherit`;
   - focus uses `--vscode-focusBorder` (fallback `currentColor`);
   - the highlight uses `--vscode-errorForeground`.

   These variables are the same ones the existing rules already rely on in every theme mode.
   Follow-up: add an invalid-link frontmatter fixture to one visual scenario so the light/white
   rendering is captured.
5. [NIT] In reading mode, the invalid span is now focusable. Enter on it falls through to the
   mapped-block keyboard reveal, which is consistent with other focusable content and is not a
   regression.

## Existing assertions changed
None. Only harness helpers were extended (selector matching and the issue-row `querySelector`). No
existing test asserted `[E10]` text or a span badge. OK.

VERDICT: PASS

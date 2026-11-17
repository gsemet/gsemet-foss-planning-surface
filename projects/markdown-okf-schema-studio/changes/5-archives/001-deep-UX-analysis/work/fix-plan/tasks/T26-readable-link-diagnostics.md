# T26 — Readable link diagnostics in the properties table

| Field | Value |
| --- | --- |
| Fixes | [UX-23](../../04-okf-links-and-diagnostics/UX-23-cryptic-link-diagnostics.md) |
| Decisions | D-09 (no Problems panel in this plan) |
| Depends on | T22 |
| Gate | `unit trusted visual` |
| Risk | Low–medium (P-R7 display; **UX-22 and UX-24 are frozen**) |
| Commit message | `fix(vscode): explain frontmatter link problems in plain words` |

## Goal

A user understands every red value without hovering for a second or reading an error code:

- an invalid or unavailable link value shows an icon and a short human label, `✖ File not found`,
  instead of `[E10]`;
- its full explanation (today's message, code included) appears in the **custom** tooltip on hover
  **and on keyboard focus**;
- the header badge (`✖ 2`) is a button that scrolls to and focuses the first row with an issue.

## Context to read first

- `src/frontmatter/propertiesTable.ts`: `formatLinkedValue` (the `okf-link-status` span with
  `[CODE]`), `linkTitle`, the badge in `renderPropertiesTable`.
- `src/frontmatter/fileLinks.ts`: the `diagnostic("E10" | "W15", field, message)` calls. Read the
  message texts; **do not change them** (UX-22 frozen).
- `src/webview/scrollSync.ts`: `showLinkTooltip`, `leaveLinkTooltip`, and the `pointerdown`
  listener (all keyed on `a.okf-frontmatter-link`).
- `src/preview/previewStyles.ts`: `.okf-link-status` and `[data-okf-badge]` rules.

## Allowed files

- `src/frontmatter/propertiesTable.ts`
- `src/webview/scrollSync.ts`
- `src/preview/previewStyles.ts`
- `test/frontmatter/propertiesTable.test.ts`, `test/webview/scrollSync.test.ts`,
  `test/webview/previewStyles.test.ts`
- `test/integration/previewEditing.test.ts` (only assertions on `[E10]`/`[W15]` label text or on
  the badge element type)
- `test/visual/capture.py` (only assertions on the label text or the badge element type)
- `test/integration/realInput.test.ts` (add RI-T26)

## Steps

1. Write the tests first and record the failures.
2. `propertiesTable.ts`, `linkStatusLabel(link)` (exported for tests): map `link.message` to a
   label. Read the actual messages in `fileLinks.ts` and cover each family:

   | Message contains | Label |
   | --- | --- |
   | `does not resolve to a file` | `File not found` |
   | `escapes` | `Outside the allowed folder` |
   | `root is unavailable` | `Link root unavailable` |
   | `absolute target` | `Absolute paths are not allowed` |
   | `filename stem` with several matches (read the exact text) | `Several files match` |
   | `is empty` | `Empty link` |
   | anything else | `Invalid link` (E10), `Link unavailable` (W15) |

3. `formatLinkedValue` (non-valid, non-pending branch):
   - replace the `[CODE]` text with
     `<span class="okf-link-status" data-okf-link-code="E10"><span aria-hidden="true">✖</span> File not found</span>`.
     Use `⚠` for warnings. Escape the label.
   - Add `tabindex="0"` to the outer `span.okf-frontmatter-link`. Keep its `title` (full message)
     unchanged.
4. Badge: render `<button type="button" data-okf-badge … aria-label="Go to the first frontmatter issue">`
   instead of the `<span>`. Keep every `data-okf-*` attribute and the inner text. CSS: reset the
   button look (no border or background, `font: inherit`, `color: inherit`, `cursor: pointer`),
   with a focus-visible outline.
5. Webview:
   - Define `const linkTooltipSelector = ".okf-frontmatter-link[data-okf-link-status]:not([data-okf-link-status=\"pending\"])"`
     (escape the quotes inside the template). Use it in `showLinkTooltip`, `leaveLinkTooltip` and
     the `pointerdown` listener in place of `a.okf-frontmatter-link`. Valid links keep working:
     they also carry `data-okf-link-status="valid"`.
   - Add a click handler for `[data-okf-badge]`. It finds the first
     `tr[data-okf-field].okf-error`, `.okf-warning` or `.okf-info`, then calls
     `scrollIntoView({ block: "center" })`, focuses its value cell (`[data-okf-edit-cell="value"]`,
     or the row's `th`; set `tabindex="-1"` if needed), and sets
     `data-okf-issue-highlight="true"` for 1.5 s. CSS: an outline in the error colour.
6. Do not touch the YAML-style display of values (`- item`, `[]`, `null`): UX-24 is frozen.

## Tests

**Unit:**

- `linkStatusLabel` for each message family.
- `formatLinkedValue` no longer emits `[E10]`; the label and icon exist; `tabindex` is set; the
  title is unchanged.
- The badge is a button with its data attributes.
- Webview: `focusin` on an invalid link span shows a `role="tooltip"` element with the title text.
- The badge click focuses the first issue row's cell.

**Real-input E2E**, scenario **RI-T26**:

- Bundle with `implemented_in_files: [missing.py]` (project-relative) and a schema `x-okf-link`.
- Assert:
  - the visible text includes `File not found`, and no visible `[E10]`;
  - pressing `Tab` until the invalid value is focused (`document.activeElement` matches the span)
    shows a `[role="tooltip"]` containing `does not resolve`;
  - clicking the badge brings the `implemented_in_files` row into the viewport and focuses it.

## Expected changes to existing tests

- `propertiesTable.test.ts`: the assertion expecting `[E10]` (or `[W15]`) label text, and any
  assertion that the badge is a `span`. List each one.
- `previewEditing.test.ts` / `capture.py`: assertions on `okf-link-status` text content showing
  the code. They now expect the human label; assertions on `data-okf-link-status` attributes stay
  unchanged.

## Must not change

- Diagnostic messages, codes and resolution (UX-22 frozen); value formatting (UX-24 frozen).
- Valid-link tooltips and excerpts (P-R7); link navigation (P-N6).

## Done when

- The `unit`, `trusted` and `visual` gates pass; RI-T26 passes.
- The reviewer looked at a screenshot with an invalid link in each theme.

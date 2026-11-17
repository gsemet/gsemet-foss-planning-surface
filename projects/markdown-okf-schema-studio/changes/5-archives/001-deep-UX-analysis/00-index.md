# Deep UX Analysis — Markdown OKF-Schema Studio (status report 1)

Date: 2026-10-09. Subject: `src/markdown-okf-schema-studio` at commit `e1b4ad0` (clean tree), run
from source with `--extensionDevelopmentPath`.
Scope: exploratory QA of the extension used like a person would use it every day: reading,
editing in the source with the preview, editing inside the preview, the Open With editor, OKF
frontmatter, and links. This complements the code-level review in
[`../deep-analysis-review/`](../deep-analysis-review/00-index.md) (security, performance,
stability); overlaps are cross-referenced.

Status: **partial** (status report). The campaign was stopped on request to publish this report;
the uncovered areas listed in [QA-04](08-test-campaign-gaps/QA-04-coverage-of-this-campaign.md)
were then covered by the complementary [part 2](part-2/00-index.md) (findings UX-35 to UX-48).

## How to use this folder

One file per bug, grouped by logical area. Each file states the use case, steps on a named fixture,
expected vs observed behaviour, where it comes from (file and line), a suggested direction, the
test to add, and a "done when" criterion. Evidence images are in [`evidence/`](evidence/).

## Summary

The read-only preview is solid: MyST rendering, admonitions, figures, scroll sync on a 70 KB
chapter, schema resolution, and x-okf-link navigation to a code marker line all work, and no
webview error was logged. The weak spots are all in **writing**:

1. **Inline editing can lose or corrupt content without warning.** Escape reverts text that
   autosave already wrote (UX-01). Enter in a nested list re-parents unrelated items (UX-04).
   In the Open With editor, Cmd+Z closes the editor mid-sentence (UX-03).
2. **Every structured edit rewrites more than it should.** One table cell rewrites the table's
   formatting (UX-12), and one frontmatter field re-serializes the whole frontmatter (UX-16). Both
   produce whole-block Git diffs. The unit tests miss this because their fixtures are already in
   the serializer's style (QA-01).
3. **Keyboard conventions differ per control.** Enter means newline, save, or nothing depending on
   the field (UX-17, UX-19). Tab never indents or moves to the next cell (UX-05, UX-13).
4. **The side preview loses its document** whenever a non-Markdown editor becomes active,
   including after following the extension's own link to a code file (UX-25).
5. **The E2E campaign does not type.** It injects 51 synthetic messages and never uses
   `keyboard.type`, undo, or Tab, which is why most of the above escaped it (QA-02). The
   screenshots are only read by a human (QA-03).

## Findings

| ID | Severity | Area | Title | approved |
| --- | --- | --- | --- | --- |
| [UX-01](01-inline-block-editing/UX-01-escape-discards-autosaved-text.md) | High | Inline editing | Escape silently reverts text that is already in the document | [x] |
| [UX-03](01-inline-block-editing/UX-03-open-with-undo-closes-inline-editor.md) | High | Inline editing | In the Open With editor, Cmd+Z closes the inline editor and undoes one character | [x] |
| [UX-04](01-inline-block-editing/UX-04-enter-breaks-list-structure.md) | High | Inline editing | Adding a list item inline silently re-parents the following items | [x] |
| [UX-12](02-table-editing/UX-12-cell-edit-rewrites-whole-table.md) | High | Tables | Editing one cell rewrites the formatting of the whole table | [x] |
| [UX-16](03-frontmatter-editing/UX-16-field-edit-reserializes-frontmatter.md) | High | Frontmatter | Editing one field re-serializes the whole frontmatter | [x] |
| [UX-17](03-frontmatter-editing/UX-17-enter-in-text-field-creates-block-scalar.md) | High | Frontmatter | Enter in a one-line text field adds a newline and saves `title: \|` | [x] |
| [UX-25](05-preview-lifecycle/UX-25-preview-blanked-by-non-markdown-editor.md) | High | Lifecycle | Focusing any non-Markdown editor wipes the side preview | [x] |
| [QA-01](08-test-campaign-gaps/QA-01-roundtrip-fixtures-match-serializer-style.md) | High | Tests | Round-trip tests use fixtures already in the serializer's style | [x] |
| [QA-02](08-test-campaign-gaps/QA-02-e2e-injects-messages-instead-of-typing.md) | High | Tests | E2E suites inject messages instead of typing | [x] |
| [UX-02](01-inline-block-editing/UX-02-one-undo-stop-per-keystroke.md) | Medium | Inline editing | Inline typing creates one source undo step per character | [x] |
| [UX-05](01-inline-block-editing/UX-05-tab-commits-instead-of-indenting.md) | Medium | Inline editing | Tab commits and closes the editor instead of indenting | [x] |
| [UX-06](01-inline-block-editing/UX-06-caret-ignores-click-position.md) | Medium | Inline editing | The caret lands at the end of the block, not where the user clicked | [x] |
| [UX-07](01-inline-block-editing/UX-07-edit-affordances-invisible.md) | Medium | Inline editing | No block outline, no Save/Cancel, no shortcut hint | [x] |
| [UX-10](01-inline-block-editing/UX-10-no-way-to-insert-a-block.md) | Medium | Authoring | No way to insert a new block or section from the preview | [x] |
| [UX-13](02-table-editing/UX-13-tab-leaves-dangling-cell-editor.md) | Medium | Tables | Tab leaves the cell editor open without focus | [x] |
| [UX-18](03-frontmatter-editing/UX-18-boolean-needs-two-clicks.md) | Medium | Frontmatter | A boolean checkbox needs two clicks | [x] |
| [UX-19](03-frontmatter-editing/UX-19-list-editor-keyboard-and-completion.md) | Medium | Frontmatter | List fields: Enter does nothing, no link completion, link text navigates | [x] |
| [UX-22](04-okf-links-and-diagnostics/UX-22-project-root-ignores-bundle.md) | Medium | OKF links | `project-relative` links resolve from the Git root | [ ] |
| [UX-23](04-okf-links-and-diagnostics/UX-23-cryptic-link-diagnostics.md) | Medium | OKF links | Diagnostics shown as bare "[E10]" codes | [x] |
| [UX-28](06-render-churn-and-scroll/UX-28-full-webview-reload-per-keystroke.md) | Medium | Rendering | Each keystroke reloads the whole preview document | [x] |
| [UX-30](07-discoverability-and-chrome/UX-30-no-entry-point-besides-palette.md) | Medium | Discoverability | The preview can only be opened from the Command Palette | [x] |
| [QA-03](08-test-campaign-gaps/QA-03-screenshots-are-not-asserted.md) | Medium | Tests | Screenshots are captured but nothing checks them | [x] |
| [UX-08](01-inline-block-editing/UX-08-proportional-font-for-raw-source.md) | Low | Inline editing | Raw source edited in a proportional font | [x] |
| [UX-09](01-inline-block-editing/UX-09-edit-mode-reflows-whole-document.md) | Low | Edit mode | Edit mode reflows every paragraph with source line breaks | [x] |
| [UX-11](01-inline-block-editing/UX-11-edited-element-drifts-after-save.md) | Low | Scroll anchoring | The edited block drifts on screen after commit | [x] |
| [UX-14](02-table-editing/UX-14-table-toolbar-covers-content.md) | Low | Tables | Table toolbar covers the previous row; ambiguous labels | [x] |
| [UX-15](02-table-editing/UX-15-wide-table-layout.md) | Low | Rendering | Wide tables wrap short identifiers; overflow hard to see | [x] |
| [UX-20](03-frontmatter-editing/UX-20-row-menu-overlaps-and-clipped-tooltips.md) | Low | Frontmatter | Row menu hides values; tooltips clipped | [x] |
| [UX-21](03-frontmatter-editing/UX-21-add-remove-field-flow.md) | Low | Frontmatter | Add/remove field flow | [x] |
| [UX-24](04-okf-links-and-diagnostics/UX-24-value-rendering-yaml-literals.md) | Low | Frontmatter | Values displayed with YAML syntax | [ ] |
| [UX-26](05-preview-lifecycle/UX-26-status-page-text-and-stale-naming.md) | Low | Wording | Glued status text; user-facing "Sphinx" strings | [x] |
| [UX-27](05-preview-lifecycle/UX-27-quick-open-covers-preview.md) | Low | Layout | Opening a file from the preview buries the preview | [x] |
| [UX-29](06-render-churn-and-scroll/UX-29-scroll-jump-on-owner-switch.md) | Low | Scroll sync | The preview jumps when scroll ownership changes | [x] |
| [UX-31](07-discoverability-and-chrome/UX-31-open-with-label-and-builtin-competitor.md) | Low | Naming | Duplicated Open With label; built-in Markdown Editor competitor | [x] |
| [UX-32](07-discoverability-and-chrome/UX-32-long-tab-titles.md) | Low | Chrome | Long tab titles | [x] |
| [UX-33](07-discoverability-and-chrome/UX-33-toolbar-state-in-open-with-editor.md) | Low | Toolbar | Anchor toggle active without a text editor; edit mode forgotten | [x] |
| [UX-34](07-discoverability-and-chrome/UX-34-sticky-band-shows-markdown-hashes.md) | Low | Rendering | Sticky band shows raw `#` markers | [ ] |

[QA-04](08-test-campaign-gaps/QA-04-coverage-of-this-campaign.md) lists what was and was not
exercised.

## Severity scale

| Level | Meaning |
| --- | --- |
| High | Silent loss or corruption of content, or a defect that breaks a core daily flow |
| Medium | Repeated friction or confusion in a core flow, with a workaround |
| Low | Cosmetic, wording, or rare friction |

## Method

- A disposable workspace with copies of `book/` (all chapters and images), the `okf-schema`
  example bundles (including `okfreq-examples` with `x-okf-link` and `@implements_req` markers),
  the extension's visual fixtures, and a Markdown-only copy of the private Obsidian vault (vault
  content was not opened in this first part and does not appear in the evidence).
- VS Code 1.141.0 (macOS) launched with an isolated profile, `--extensionDevelopmentPath`, a
  read-only "spy" extension that records document versions, text, and tabs, and
  `--remote-debugging-port`. All actions used real mouse and keyboard events through CDP;
  webview DOM reads were used only to locate targets and to diagnose after a visible observation.
- Buffer contents were compared with the files on disk after each editing scenario.
- The harness is packaged as the skill
  [`markdown-studio-exploratory-qa-claude`](../../../skills/markdown-studio-exploratory-qa-claude/SKILL.md)
  so the campaign can be resumed.

## Limits

- One tester (an agent) and one machine; no human participants, no screen reader.
- Severity reflects the observed scenario on this repository's content.
- Line numbers refer to commit `e1b4ad0`.

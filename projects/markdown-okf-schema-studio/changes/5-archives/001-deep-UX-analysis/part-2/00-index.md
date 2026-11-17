# Deep UX Analysis — Part 2 (complementary report)

Date: 2026-10-09. Same subject and commit as [part 1](../00-index.md): `src/markdown-okf-schema-studio`
at `e1b4ad0`, run from source in VS Code 1.141.0 (macOS).
Scope: the areas part 1 left untested ([QA-04](../08-test-campaign-gaps/QA-04-coverage-of-this-campaign.md)):
line endings, diagrams and math, links and wikilinks (synthetic fixture plus a private vault copy),
complex frontmatter types, empty and broken documents, restoration after reload, external
rename, restricted mode, settings applied live, theme override, narrow layout, find, and typing
latency on large chapters.

This campaign used the new skill
[`markdown-studio-exploratory-qa-claude`](../../../../skills/markdown-studio-exploratory-qa-claude/SKILL.md)
end to end, which also validated it (two harness fixes were folded back into the skill).

## Summary

1. **CRLF documents cannot be edited inline** beyond the first keystroke (UX-35). The rest of the
   typing stays in the textarea and is never written. Together with STAB-07, which this campaign
   reproduced in the UI, CRLF is the most fragile configuration.
2. **Frontmatter editing traps users.** An invalid value silently blocks every other field
   (UX-38). Object fields are edited as de-indented YAML that fails with raw parser errors (UX-39).
3. **Part 1's formatting findings get worse on real variants.** One cell edit strips the padding of
   an aligned table and rewrites a compact table entirely (UX-12). One enum edit flattens a `>-`
   folded scalar and rewrites `[a, b]` as `[ a, b ]` (UX-16).
4. **Reading features are robust.** Reload restoration, external rename recovery, restricted mode,
   find, anchors, heading links, broken-document handling, and live settings all behave well. The
   gaps are signalling (dead links look valid, UX-41) and layout at narrow widths (UX-43).
5. **Large chapters lag** about 350 ms per keystroke (UX-48); visible flicker is mostly hidden by
   VS Code's frame double-buffering.

## New findings

| ID | Severity | Area | Title | approved |
| --- | --- | --- | --- | --- |
| [UX-35](01-editing/UX-35-crlf-inline-edits-lost-after-first-key.md) | High | Editing | In CRLF documents, inline edits stop being saved after the first keystroke | [ ] |
| [UX-38](02-frontmatter/UX-38-invalid-field-editor-blocks-other-fields.md) | High | Frontmatter | A field editor left in error silently blocks every other field | [ ] |
| [UX-36](01-editing/UX-36-diagram-and-math-editing-is-blind.md) | Medium | Editing | Editing a diagram or an equation hides it: no live preview | [ ] |
| [UX-37](01-editing/UX-37-empty-document-cannot-be-started.md) | Medium | Authoring | An empty document cannot be started from the Studio editor | [ ] |
| [UX-39](02-frontmatter/UX-39-object-fields-and-raw-yaml-errors.md) | Medium | Frontmatter | Object fields: "unknown" type, de-indented YAML, raw parser errors | [ ] |
| [UX-41](03-links/UX-41-broken-links-look-valid.md) | Medium | Links | Broken links look exactly like valid links | [ ] |
| [UX-43](04-preview-chrome/UX-43-narrow-preview-layout.md) | Medium | Layout | In a narrow preview, the properties table breaks words and clips values | [ ] |
| [UX-47](05-sync-and-performance/UX-47-selection-marker-does-not-follow-cursor.md) | Medium | Sync | `markEditorSelection` does not follow the cursor | [ ] |
| [UX-48](05-sync-and-performance/UX-48-large-document-typing-latency.md) | Medium | Performance | On large chapters, the preview lags about 350 ms behind every keystroke | [ ] |
| [UX-40](02-frontmatter/UX-40-frontmatter-control-details.md) | Low | Frontmatter | Controls ignore schema hints (bounds, required enums, labels) | [ ] |
| [UX-42](03-links/UX-42-obsidian-wikilink-compatibility.md) | Low | Links | Wikilinks diverge from Obsidian on case and special characters | [ ] |
| [UX-44](04-preview-chrome/UX-44-floating-toolbar-overlaps.md) | Low | Chrome | The floating toolbar overlaps content and the find widget | [ ] |
| [UX-45](04-preview-chrome/UX-45-theme-override-partial.md) | Low | Theme | The white preview theme leaves the sticky band and toolbar dark | [ ] |
| [UX-46](04-preview-chrome/UX-46-mermaid-labels-unreadable.md) | Low | Diagrams | Wide Mermaid diagrams are scaled until labels are unreadable | [ ] |

## Part 1 findings confirmed with new evidence

| Finding | New evidence |
| --- | --- |
| [UX-12](../02-table-editing/UX-12-cell-edit-rewrites-whole-table.md) | `synth/tables.md`: one cell edit removed the padding from every row of an aligned table (`\| alpha    \| left       \|` → `\| alpha \| leftX \|`) and rewrote a compact `\|a\|b\|` table line by line |
| [UX-16](../03-frontmatter-editing/UX-16-field-edit-reserializes-frontmatter.md) | `synth/frontmatter-edge.md`: one enum edit flattened a `>-` folded scalar, rewrote the flow sequence `[braking, safety, …]` as `[ braking, safety, … ]`, and re-indented a block sequence; comments were preserved |
| [UX-10](../01-inline-block-editing/UX-10-no-way-to-insert-a-block.md) | Empty document: nothing to click ([UX-37](01-editing/UX-37-empty-document-cannot-be-started.md)) |
| [UX-28](../06-render-churn-and-scroll/UX-28-full-webview-reload-per-keystroke.md) | 90 webview navigations for 34 characters typed next to three Mermaid diagrams |
| [UX-26](../05-preview-lifecycle/UX-26-status-page-text-and-stale-naming.md) | "Sphinx preview navigation blocked: The wikilink target is unavailable." on a missing wikilink |
| STAB-07 (code review) | `> [!NOTE]` rendered as a plain blockquote in `synth/crlf.md` |

## Worked as intended

| Behaviour | Observation |
| --- | --- |
| Reload Window | Side preview restored with its scroll position (9000 → 8899 px) and edit mode on |
| External rename of the previewed file | "Preview source missing" page, then full recovery when the file came back |
| Source edit after an inline edit on the same block | Blur committed the inline edit; no conflict |
| Restricted Mode | Read-only preview, no edit toggle, "Schema validation requires a trusted workspace" notice |
| Live settings | `stickyHeadingDepth`, `markEditorSelection`, `projectRoot` applied without reload |
| Find in preview (Cmd+F) | Matches highlighted and navigable |
| Links | Relative link with `#heading` selects the heading line; same-document anchors scroll |
| Broken document | Clear invalid-YAML banner; unclosed fence swallows the rest as CommonMark specifies |
| Frontmatter | Enum dropdown, date input, number validation message, comment preservation, `preview_shows_fields` |
| Mermaid and math | Click-to-edit opens the right source (fence, `$$` block, inline paragraph); invalid math stays readable |
| Console | No webview errors or exceptions in either part |

## Still not covered

PlantUML (no Java in the test profile), `{include}` directives and bibliography, keyboard-only
navigation across blocks and screen-reader behaviour, multi-root workspaces, missing images,
long-session memory (PERF-12 is a code-review finding), and coexistence with VS Code 1.141's
built-in Markdown Editor.

## Method notes

- Fixtures: `.agents/skills/markdown-studio-exploratory-qa-claude/assets/synth/` (CRLF, tables,
  frontmatter edge cases with an `edge` schema, links, diagrams and math, broken and empty
  documents), plus the book, OKF examples, and a Markdown-only copy of the private vault.
- Vault evidence is reported as counts only; screenshots showing the vault were cropped to the
  preview or left out.
- Flicker and jitter were measured with a DOM sampler through raw CDP (about 500 samples per
  second). CDP screenshots coalesce compositor frames and cannot prove or disprove short flashes.

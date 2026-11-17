# Exploratory QA campaign — 2026-10-31

Date: 2026-10-31. Subject: markdown-okf-schema-studio at commit `b9118506` (main, clean tree), real
isolated VS Code windows driven through CDP with real mouse and keyboard input.
Status: **completed** (C0 sweep and 8 charters run; several charters ended `partial` on budget, see
[Limits](#limits)). Report only: no product code, test or PR change.
Previous campaign: [001-deep-UX-analysis](../../4-archives/001-deep-UX-analysis/00-index.md) (2026-10-09).

## Summary

- **1 High**, 8 Medium, 1 Low, 1 design decision, 3 test-campaign gaps. Triage approved by the owner on
  2026-10-31; every finding links to its backlog item, and promoting the replays is P2
  [promote-qa-210-replays-to-e2e](../../2-backlog/P2/promote-qa-210-replays-to-e2e/01-intent.md).
- The one High is old: a rejected front-matter value still strands the field editor and blocks every
  other field (001 part-2 UX-38), confirmed by a fresh replay.
- Of the 9 Highs of campaign 001, **6 are fixed** (UX-03, UX-12, UX-16, UX-17, UX-25, UX-35), UX-38
  is still present, UX-04 changed behaviour, and UX-01 is now specified behaviour (BLOCK-053).
- The features merged since 001 hold up on their main paths. The new defects sit on edges: link-only
  targets in edit mode, card header options, alert lazy lines, Replace all next to link URLs, wide
  tables, front-matter edge types, and a narrow-pane toolbar.
- The no-op invariant held everywhere it was exercised (open and commit without typing changes
  nothing). Typing latency on a 1709-line chapter: p50 272 ms, max 582 ms (5x a small fixture).

## Findings

IDs are campaign IDs; file names keep the charter's provisional ID. Severity scale below.

| ID | Severity | Area | Title | Reproduced | Sheet | Backlog | approved |
| --- | --- | --- | --- | --- | --- | --- | --- |
| QA210-01 | High | Front matter | After a rejected value the field editor stays open, Escape stops working and no other field opens (001 UX-38, still present) | Yes, plus coordinator replay | [c6-1](06-frontmatter/c6-1-rejected-commit-strands-editor.md), [c8-2](09-previous-highs-replay/c8-2-invalid-field-blocks-other-fields.md) | [P1 frontmatter-editor-stuck-after-rejected-value](../../2-backlog/P1/frontmatter-editor-stuck-after-rejected-value/01-intent.md) | [x] |
| QA210-02 | Medium | Cards, links | In edit mode a target made only of a link (a `:link:` card, the "Next:" line of every chapter) cannot be edited: the click follows the link | Yes | [c1-1](01-myst-cards-tabs/c1-1-link-card-not-editable.md), [c0-1](10-noop-sweeps/c0-1-link-only-paragraph-not-editable.md) | [P2 link-only-targets-not-editable](../../2-backlog/P2/link-only-targets-not-editable/01-intent.md) | [x] |
| QA210-03 | Medium | Cards | Enter in a `{card}` `:header:` editor inserts a blank line into the option block and the editor stays open | Yes | [c1-2](01-myst-cards-tabs/c1-2-card-header-enter-adds-blank-line.md) | [P2 card-header-option-enter-adds-blank-line](../../2-backlog/P2/card-header-option-enter-adds-blank-line/01-intent.md) | [x] |
| QA210-04 | Medium | Admonitions | A lazy continuation line of a GitHub alert renders outside the alert and is left out of its block editor (no data loss) | Yes | [c3-1](03-admonitions/c3-1-alert-lazy-continuation.md) | [P2 alert-palette-after-lazy-continuation](../../2-backlog/P2/alert-palette-after-lazy-continuation/01-intent.md) | [x] |
| QA210-05 | Medium | Find and replace | Replace all skips matches in a list whose link URL also contains the query (4 counted, 2 replaced, no warning) | Yes | [c4-1](04-find-replace/c4-1-replace-all-skips-list-with-hidden-url-match.md) | [P2 replace-all-skips-blocks-with-link-url-match](../../2-backlog/P2/replace-all-skips-blocks-with-link-url-match/01-intent.md) | [x] |
| QA210-06 | Medium | Tables | Tab through a wide table leaves the cell editor outside the visible preview | Yes | [c5-1](05-table-editing/c5-1-wide-table-editor-offscreen-after-tab.md) | [P2 wide-table-tab-editor-offscreen](../../2-backlog/P2/wide-table-tab-editor-offscreen/01-intent.md) | [x] |
| QA210-07 | Medium | Front matter | The x-okf-link list editor says "No Markdown file … found" for a sibling file the table resolves; suggestions list only another folder | Yes | [c6-2](06-frontmatter/c6-2-link-hint-says-not-found.md) | [P2 okf-link-hint-ignores-document-folder](../../2-backlog/P2/okf-link-hint-ignores-document-folder/01-intent.md) | [x] |
| QA210-08 | Medium | Front matter | A number property without a schema opens a text area holding "4.5\n" and cannot be committed | Yes | [c6-3](06-frontmatter/c6-3-schemaless-number-cannot-commit.md) | [P2 schemaless-number-editor-cannot-commit](../../2-backlog/P2/schemaless-number-editor-cannot-commit/01-intent.md) | [x] |
| QA210-09 | Medium | Layout | In a narrow side preview (393–438 px) the expanded toolbar covers the first lines of the first paragraph | Yes | [c7-1](07-layout-and-width/c7-1-toolbar-covers-first-lines-narrow.md) | [P2 narrow-toolbar-covers-first-lines](../../2-backlog/P2/narrow-toolbar-covers-first-lines/01-intent.md) | [x] |
| QA210-10 | Low | Review comments | The Comments toolbar button hides only the inline chips; threads from the comments file stay visible (intent question: REVIEW-152 names chips only) | Yes | [c2-1](02-review-comments/c2-1-comments-toggle-keeps-threads.md) | [P3 comments-button-hides-chips-only](../../2-backlog/P3/comments-button-hides-chips-only/01-intent.md) | [x] |
| QA210-D1 | Decision | Inline editing | Escape after an autosave restores the original block text (001 UX-01), as SwRS BLOCK-053 specifies. **Owner decision 2026-10-31: keep.** | Yes, plus coordinator replay | [c8-1](09-previous-highs-replay/c8-1-escape-discards-autosaved-text.md) | — (decided: keep) | [x] |

Observations without a sheet (judged minor or by design): the alert type list does not preselect the
current type and has no keyboard route to open it; Cmd+Z with focus in the preview does nothing (undo
works from the source editor); a closed H1 fold persists and hides the whole document on the next
open; a MyST list-table cell opens the whole-block source editor; a folded `>-` summary is rewritten
on one line after an edit.

### Severity scale

- **High**: data loss, or a blocked core journey with no visible way out.
- **Medium**: a wrong result or a blocked secondary journey with a workaround.
- **Low**: cosmetic, wording, or an intent question.

## Owner decisions (2026-10-31)

- **QA210-D1 (owner, 2026-10-31): keep.** Escape and Cancel after an autosave restore the original
  text, as SwRS-MDOKFSTUDIO-BLOCK-053 says. 001 UX-01 is closed as specified.
- Triage approved as proposed: one backlog item per root cause (QA210-01 P1, QA210-02 to 09 P2,
  QA210-04 merged into the existing alert lazy-continuation item, QA210-10 P3), plus the P2 item to
  promote the replays to E2E tests.

## Replay of campaign 001 Highs

| 001 ID | Verdict | Note | Scenario |
| --- | --- | --- | --- |
| UX-01 | Closed: specified (QA210-D1, owner keeps BLOCK-053) | Escape restores the original text after an autosave, as BLOCK-053 requires | [ux-01](../../../skills/markdown-studio-exploratory-qa-claude/scenarios/ux-01-escape-keeps-typed-text.json) |
| UX-03 | Fixed | Cmd+Z in the Open With editor keeps the text area open with focus | [ux-03](../../../skills/markdown-studio-exploratory-qa-claude/scenarios/ux-03-open-with-undo-keeps-inline-editor.json) |
| UX-04 | Changed | Enter keeps the indentation and continues the list with its own marker; typing a marker gives `- - ` | [ux-04](../../../skills/markdown-studio-exploratory-qa-claude/scenarios/ux-04-enter-keeps-list-indentation.json) |
| UX-12 | Fixed | A cell edit changes one line | [ux-12](../../../skills/markdown-studio-exploratory-qa-claude/scenarios/ux-12-cell-edit-minimal-diff.json) |
| UX-16 | Fixed | A field edit changes one line (synthetic fixture) | [ux-16](../../../skills/markdown-studio-exploratory-qa-claude/scenarios/ux-16-field-edit-minimal-diff.json) |
| UX-17 | Fixed | Enter commits a one-line value | [ux-17](../../../skills/markdown-studio-exploratory-qa-claude/scenarios/ux-17-enter-commits-text-field.json) |
| UX-25 | Fixed | The side preview keeps the last Markdown document when a non-Markdown editor is active | [ux-25](../../../skills/markdown-studio-exploratory-qa-claude/scenarios/ux-25-preview-survives-non-markdown-editor.json) |
| UX-35 | Fixed | CRLF documents keep every typed key | [ux-35](../../../skills/markdown-studio-exploratory-qa-claude/scenarios/ux-35-crlf-inline-edit-keeps-all-keys.json) |
| UX-38 | Still present (QA210-01) | A rejected value blocks every other field | [ux-38](../../../skills/markdown-studio-exploratory-qa-claude/scenarios/ux-38-invalid-field-does-not-block-others.json) |

## Test-campaign gaps

- [c0-gap-1](08-test-campaign-gaps/c0-gap-1-noop-sweep-follows-links.md): `noop-sweep.mjs` clicks
  link-only blocks and navigates away, so later targets are reported "not found"; `--limit` without
  `--from` does not bound a blocks run.
- [c7-gap-1](08-test-campaign-gaps/c7-gap-1-no-toc-hidden-hint.md): the TOC toggle shows active while
  the TOC column is hidden on narrow panes, with no hint and no test.
- [coverage-c8](08-test-campaign-gaps/coverage-c8.md): the OKF `SwRS-CORE-001.md` fixture of 001 is not
  in the workspace, so UX-16/UX-17 were replayed on a synthetic fixture only.
- Coverage notes per charter: [C0](08-test-campaign-gaps/coverage-c0.md),
  [C1](08-test-campaign-gaps/coverage-c1.md), [C2](08-test-campaign-gaps/coverage-c2.md),
  [C3](08-test-campaign-gaps/coverage-c3.md), [C4](08-test-campaign-gaps/coverage-c4.md),
  [C5](08-test-campaign-gaps/coverage-c5.md), [C6](08-test-campaign-gaps/coverage-c6.md),
  [C7](08-test-campaign-gaps/coverage-c7.md), [C8](08-test-campaign-gaps/coverage-c8.md).

## Tests to promote

These replay scenarios (in the QA skill's `scenarios/`) should become product real-input E2E tests,
so the next campaign does not explore them again. The first group asserts the expected behaviour and
fails today; the second group passes and guards the 001 fixes.

- Failing today: [c6-1](../../../skills/markdown-studio-exploratory-qa-claude/scenarios/c6-1-invalid-commit-strands-editor.json) /
  [ux-38](../../../skills/markdown-studio-exploratory-qa-claude/scenarios/ux-38-invalid-field-does-not-block-others.json),
  [c1-1](../../../skills/markdown-studio-exploratory-qa-claude/scenarios/c1-1-link-card-not-editable.json), [c0-1](../../../skills/markdown-studio-exploratory-qa-claude/scenarios/c0-1-link-only-paragraph-navigates.json),
  [c1-2](../../../skills/markdown-studio-exploratory-qa-claude/scenarios/c1-2-card-header-enter-adds-blank-line.json),
  [c3-1](../../../skills/markdown-studio-exploratory-qa-claude/scenarios/c3-1-alert-lazy-continuation-outside.json),
  [c4-1](../../../skills/markdown-studio-exploratory-qa-claude/scenarios/c4-1-replace-all-skips-list-with-hidden-url-match.json),
  [c5-1](../../../skills/markdown-studio-exploratory-qa-claude/scenarios/c5-1-wide-table-tab-editor-offscreen.json),
  [c6-2](../../../skills/markdown-studio-exploratory-qa-claude/scenarios/c6-2-link-hint-ignores-document-folder.json),
  [c6-3](../../../skills/markdown-studio-exploratory-qa-claude/scenarios/c6-3-schemaless-number-editor-cannot-commit.json),
  [c7-1](../../../skills/markdown-studio-exploratory-qa-claude/scenarios/c7-1-toolbar-covers-first-lines-narrow.json),
  [c2-1](../../../skills/markdown-studio-exploratory-qa-claude/scenarios/c2-1-comments-toggle-keeps-threads.json) (once the intent is decided).
- Guards for 001 fixes: [ux-03](../../../skills/markdown-studio-exploratory-qa-claude/scenarios/ux-03-open-with-undo-keeps-inline-editor.json),
  [ux-12](../../../skills/markdown-studio-exploratory-qa-claude/scenarios/ux-12-cell-edit-minimal-diff.json), [ux-16](../../../skills/markdown-studio-exploratory-qa-claude/scenarios/ux-16-field-edit-minimal-diff.json),
  [ux-17](../../../skills/markdown-studio-exploratory-qa-claude/scenarios/ux-17-enter-commits-text-field.json),
  [ux-25](../../../skills/markdown-studio-exploratory-qa-claude/scenarios/ux-25-preview-survives-non-markdown-editor.json),
  [ux-35](../../../skills/markdown-studio-exploratory-qa-claude/scenarios/ux-35-crlf-inline-edit-keeps-all-keys.json).

## New-feature coverage

One row per user-facing `feat` PR merged since the extraction (2026-10-14, #1). The 97 `fix` PRs of the same
period are covered through their areas below and are not listed one by one. "automated" names the
real-input E2E, integration, or visual check that already asserts the feature (not re-explored, by rule).

| PR | Feature | Exercised by | Result |
| --- | --- | --- | --- |
| [#228](https://github.com/gsemet/markdown-okf-schema-studio/pull/228) | Requirements as a native OKF v0.2 bundle (properties on OKF files) | C6 (synthetic frontmatter only; OKF requirement files not reached) | c6-1, c6-2, c6-3; OKF v0.2 bundle files not exercised (see Limits) |
| [#223](https://github.com/gsemet/markdown-okf-schema-studio/pull/223) | Studio in the VS Code Agents window | — | not covered (see Limits) |
| [#222](https://github.com/gsemet/markdown-okf-schema-studio/pull/222) | Click in an admonition body opens the whole directive | C3 (nested MyST admonition body edit) | clean |
| [#198](https://github.com/gsemet/markdown-okf-schema-studio/pull/198) | Click in a GitHub alert body opens the whole alert | C3 | c3-1 (lazy continuation line left out) |
| [#175](https://github.com/gsemet/markdown-okf-schema-studio/pull/175) | Motion on the floating toolbar and its tooltips | automated: visual motion scenarios | not explored |
| [#170](https://github.com/gsemet/markdown-okf-schema-studio/pull/170) | Move into tables and nested blocks from the keyboard | automated: realInput blockKeys, visual structural navigation | not explored |
| [#157](https://github.com/gsemet/markdown-okf-schema-studio/pull/157) | Vega-Lite / Vega charts, Full palette mode | automated: visual chart fixtures | not explored |
| [#156](https://github.com/gsemet/markdown-okf-schema-studio/pull/156) | MyST cards, tabs and version directives | C1 | c1-1, c1-2 |
| [#153](https://github.com/gsemet/markdown-okf-schema-studio/pull/153) | Pasting a URL makes a link, an image URL an image | automated: integration pasteUrl | not explored |
| [#152](https://github.com/gsemet/markdown-okf-schema-studio/pull/152) | Find and replace in the preview | C4 | c4-1 |
| [#151](https://github.com/gsemet/markdown-okf-schema-studio/pull/151) | Fold and unfold sections under headings | automated: machine check heading_fold; C5 note | fold state persists per document (C5 note, no sheet) |
| [#150](https://github.com/gsemet/markdown-okf-schema-studio/pull/150) | [TOC] / {contents} as a clickable table of contents | automated: integration tocWindow, machine checks toc_column / toc_shot; C7 | TOC hidden on narrow panes with the toggle shown active (c7-gap-1) |
| [#149](https://github.com/gsemet/markdown-okf-schema-studio/pull/149) | README-style HTML like GitHub, edit-mode block titles | automated: visual readme | not explored |
| [#148](https://github.com/gsemet/markdown-okf-schema-studio/pull/148) | Edit-mode comment and TODO blocks titled with their tag | automated: visual edit scenarios | not explored |
| [#138](https://github.com/gsemet/markdown-okf-schema-studio/pull/138) | Shiki highlighting, dark code background, line numbers | automated: visual code-block comfort scenarios | not explored |
| [#126](https://github.com/gsemet/markdown-okf-schema-studio/pull/126) | Navigate and edit blocks with the keyboard only | automated: realInput arrow navigation, block move keys | not explored |
| [#125](https://github.com/gsemet/markdown-okf-schema-studio/pull/125) | Edit mode follows VS Code undo/redo/select-all/delete-line | automated: realInput shortcuts, undo stays in editor; C4 | Cmd+Z in the preview after Replace all does nothing (C4 note) |
| [#123](https://github.com/gsemet/markdown-okf-schema-studio/pull/123) | Figure form opens right after inserting a figure | automated: realInput figure editor | not explored |
| [#104](https://github.com/gsemet/markdown-okf-schema-studio/pull/104) | Keep table style on column edits | C5 | clean |
| [#89](https://github.com/gsemet/markdown-okf-schema-studio/pull/89) | Reorder table rows with a handle | automated: integration tableMoves | not explored (C5 left it out) |
| [#78](https://github.com/gsemet/markdown-okf-schema-studio/pull/78) | Soft shadow under the sticky heading band | automated: machine check sticky_headings; C7 | clean |
| [#63](https://github.com/gsemet/markdown-okf-schema-studio/pull/63) | Requirements page on the project site | out of scope (site, not the extension) | — |
| [#46](https://github.com/gsemet/markdown-okf-schema-studio/pull/46) | MyST configuration warnings banner; paste images as paragraphs | automated: visual 53-conf-warnings, machine check paste_image | not explored |
| [#42](https://github.com/gsemet/markdown-okf-schema-studio/pull/42) | New workspaces start in cream, compact toolbar, GFM | automated: machine check fresh_workspace | not explored |
| [#41](https://github.com/gsemet/markdown-okf-schema-studio/pull/41) | Light animations in the preview | automated: machine check update_glow | not explored |
| [#39](https://github.com/gsemet/markdown-okf-schema-studio/pull/39) | PlantUML with the built-in JavaScript engine | automated: visual plantuml×4 | not explored |
| [#31](https://github.com/gsemet/markdown-okf-schema-studio/pull/31) | MyST list-table, convert between table forms | automated: integration tableStructureReal; C5 | list-table cell opens the block source editor (by design); conversion not explored |
| [#30](https://github.com/gsemet/markdown-okf-schema-studio/pull/30) | Inline comment threads with reply and delete | C2 | c2-1 |
| [#29](https://github.com/gsemet/markdown-okf-schema-studio/pull/29) | MyST grid cards and toctree | C1, C0 | no-op clean on 73 and 68; c1-1, c1-2 |
| [#26](https://github.com/gsemet/markdown-okf-schema-studio/pull/26) | Link panel pre-filled from reference links | automated: realInput link panel prefill | not explored |
| [#25](https://github.com/gsemet/markdown-okf-schema-studio/pull/25) | Pasted rich text converted to Markdown | automated: machine check paste_rich_text | not explored |
| [#11](https://github.com/gsemet/markdown-okf-schema-studio/pull/11) | Backlog features 007–020, slash menu | automated: realInput slash menu, palette | not explored |
| [#173](https://github.com/gsemet/markdown-okf-schema-studio/pull/173), [#158](https://github.com/gsemet/markdown-okf-schema-studio/pull/158) | Writing skill and agent plugin | out of scope (not the extension UI) | — |

## Method

Coordinator plus one Sonnet sub-agent per charter, each driving its own isolated VS Code window
(`QA_SESSION=<charter>`, workspace clone `ws-<charter>`), 3 windows at a time. Charters are in
[charters.md](charters.md); their short returns are logged in [returns.md](returns.md). The smoke check
passed 5/5 before the first charter. Each High was replayed by the coordinator in a fresh session
(`rh`).

Two deviations from the skill:

- The 001 baseline `e1b4ad0` is not in this repository (history starts at the extraction, `be1498ba`,
  2026-10-14), so `coverage-map.py --since be1498ba` was used: 399 commits, every area changed.
  Charters followed the owner's suggested order instead.
- `setup-workspace.sh` expects a `book/` folder this repository does not have. The workspace was built
  by hand with the same layout: `book/` is a copy of the agentic-coding white-paper book (24 chapters),
  plus the visual fixtures, `synth/`, `docs/`, and the `.md` files of the private vault (no vault
  screenshot or text in this report). `okf-schema` was not copied.

| Charter | Mission | Status | Calls | Shots opened |
| --- | --- | --- | --- | --- |
| C0 | No-op sweep and latency on real documents | partial | ~30/40 | 0 |
| C1 | MyST grid cards, tabs, card title editor (#230, #236) | partial | ~36/40 | 0 |
| C2 | Review comment threads | done | ~36/40 | 2 |
| C3 | Admonitions and the alert type dropdown | partial | 38/40 | 3 |
| C4 | Find and replace in the preview | done | 36/40 | 1 |
| C5 | Table toolbar and cell editing | partial | 37/40 | 2 |
| C6 | Front matter and properties | partial | 40/40 | 1 |
| C7 | Width modes, wide tables, sticky headings | done | ~38/40 | 4 |
| C8 | Replay of the 001 Highs | done | ~20/40 | 1 |

## Limits

- Features with neither a charter nor an automated test: **#223** (Studio in the VS Code Agents
  window; the isolated stable VS Code has no Agents window). No budget was left for a ninth charter.
- OKF v0.2 requirement files (#228) were not reached: C6 used synthetic front matter only.
- Not explored, by charter (details in the coverage notes): tab-set editing, card footer and the Done
  button, blur to another pane (C1); Delete/Reopen threads, invalid comments file (C2); dropdown during
  scroll or after a re-render, MyST admonition type change (C3); invalid regex and `$1` replacements
  (C4); row move by handle, Shift+Tab, table conversion, csv-table (C5); successful enum/date/object
  commits, required-field removal (C6); a 1440 px preview, real horizontal wheel on wide tables (C7).
- The C0 sweep of chapters 06 and 02 was derailed by c0-gap-1, so their tables and fields were not
  swept.
- Findings come from synthetic fixtures and copies; vault-derived observations were reproduced on
  synthetic fixtures.

# QA campaign 271: table usability

Date: 2026-11-10. Subject: markdown-okf-schema-studio at commit `293366d0` (origin/main, clean tree).
Revision: `293366d0`
Status: **completed** (3 charters partial, see Limits)

## Summary

Scope set by the owner: Markdown tables and the front matter properties table only, looking for
what the e2e suite does not assert. 6 charters ran in real VS Code windows, plus 1 sweep and 1
follow-up: 13 findings (1 High, 7 Medium, 5 Low) and 1 owner Decision.

- **The stray-anchors report is partly reproduced.** A column move takes a block id (`^row-b`)
  written in the last cell into the middle of the row (QA271-02). Editing of the page was never
  blocked: after the drift every cell and paragraph still opens, there are no console errors, and
  undo is exact. The nearest thing to "blocked" is QA271-09: the label rename popover covers the
  first cells and swallows their clicks for about 5 s.
- **One data loss, High.** After Tab (or an arrow, or a click) to the next cell, Escape there drops
  the text typed in the cell just left. The preview still shows that text, so the author believes
  it is saved (QA271-01). PR #337, merged today, made the cell left show the typed text, which
  makes the mismatch more misleading.
- **Two stale-preview findings may share one cause.** After an undo or a revert, the preview table
  keeps its old content while a cell editor is or was open (QA271-05 and QA271-06).
- The 6 table PRs of the wide-table line (#272, #273, #301, #306, #337, #338) pass their own
  behaviour. Only #306's toolbar path was not run.

## Findings

| ID | Severity | Verdict | Title | Sheet | Currently | approved |
| --- | --- | --- | --- | --- | --- | --- |
| QA271-01 | High | Bug | Escape in the next cell drops the text typed in the cell left with Tab, an arrow or a click; the preview still shows it | [sheet](03-table-cell-editing/c2-1-escape-after-tab-drops-previous-cells.md) | [currently](evidence/c2-1-currently.jpg) | [ ] |
| QA271-02 | Medium | Gap | A column move carries a block id from the end of a row into the middle of the row | [sheet](01-stray-anchors/c1b-1-column-move-carries-last-cell-block-id-into-row.md) | diff in sheet | [ ] |
| QA271-03 | Medium | Gap | Undo of a row delete restores the row but not its comment mark, until the preview is reopened | [sheet](01-stray-anchors/c1b-3-undo-row-delete-keeps-comment-mark.md) | [currently](evidence/c1b-3-currently.jpg) | [ ] |
| QA271-04 | Medium | Gap | A table with a 1 or 2 dash delimiter cell (`:--`, `--:`) renders but has no cell editor, toolbar or handles | [sheet](02-table-structure/c3-1.md) | measured | [ ] |
| QA271-05 | Medium | Gap | After Meta+z in the source, the preview table keeps its old shape while a cell editor is open | [sheet](02-table-structure/c3-2.md) | [currently](evidence/c3-2-currently.jpg) | [ ] |
| QA271-06 | Medium | Gap | After an external rewrite and File: Revert File, a preview cell keeps its edited text | [sheet](04-table-concurrency/c6-1.md) | [currently](evidence/c6-1-currently.jpg) | [ ] |
| QA271-07 | Medium | Gap | A click on a properties field below an open field editor is lost: the open row grows on mouse down | [sheet](05-frontmatter-table/c4-1-click-field-below-open-editor-is-lost.md) | [currently](evidence/c4-1-currently.jpg) | [ ] |
| QA271-08 | Medium | Gap | Find (Meta+f) does not scroll a sideways-scrolled table to its hit | [sheet](06-table-reading-clipboard/c5-1-find-hit-in-scrolled-table-stays-out-of-view.md) | [currently](evidence/c5-1-currently.jpg) | [ ] |
| QA271-09 | Low | Gap | The label rename popover covers the first table cells and swallows their clicks for about 5 s | [sheet](01-stray-anchors/c1-1-label-rename-popover-covers-table-cells.md) | [currently](evidence/c1-1-currently.jpg) | [ ] |
| QA271-10 | Low | Gap | With a token after a row's closing pipe, the move handles do nothing and the table opens in the raw editor | [sheet](01-stray-anchors/c1b-2-token-after-last-pipe-table-handles-inert.md) | none | [ ] |
| QA271-11 | Low | Gap | A table inside a quote or a Note opens the raw block editor, with no cell editor | [sheet](02-table-structure/c3-3.md) | [currently](evidence/c3-3-currently.jpg) | [ ] |
| QA271-12 | Low | Gap | A spreadsheet (TSV) paste into a cell keeps raw tab characters in the Markdown row | [sheet](06-table-reading-clipboard/c5-2-pasted-tsv-keeps-raw-tab-in-cell.md) | diff in sheet | [ ] |
| QA271-13 | Low | Gap | Adding a row from the keyboard (Tab in the last cell) is not discoverable, and Escape then leaves an empty row (observed once) | [sheet](06-table-reading-clipboard/c5-3-tab-adds-row-not-discoverable.md) | none | [ ] |

Every finding is Reproduced except QA271-13 (observed once) and QA271-09 (seen twice in one
session, no clean replay). QA271-01 was replayed in a fresh session (4 checks pass, the buffer
check fails as described).

## Decisions for the owner

| ID | Requirement | Question |
| --- | --- | --- |
| QA271-01 | SwRS-MDOKFSTUDIO-TABLE-025, TABLE-013 | Should Escape cancel only the cell it is pressed in (keeping the cells left with Tab), or the whole table session? Either way the preview must show what the buffer holds. The sheet offers both as a radio group. |
| QA271-14 | SwRS-MDOKFSTUDIO-TABLE-006 | The cell editor is at least 300 px wide, so in a pane under 300 px it overflows out of view (pane 279 px: editor at x 62–362). Keep the minimum, or clamp it to the pane? Measurements only, no sheet. |
| stray anchors | none | Do you write Obsidian block ids (`^id`) or other anchors inside table rows? QA271-02 is the only drift found. If your pages showed something else (for example an anchor in a paragraph, or the whole page refusing edits), one real example would let a follow-up reproduce it. |

## Proposed backlog triage

Proposals only; no backlog item was created.

| Proposed item | Findings | Priority | Why |
| --- | --- | --- | --- |
| `table-escape-drops-cells-left` | QA271-01 | P1 | Silent data loss in the main table journey, and today's #337 makes it look saved |
| `table-preview-stale-after-undo-or-revert` | QA271-05, QA271-06 | P2 | Preview contradicts the buffer; probably one cause (render skipped while a cell session is or was active) |
| `table-row-tokens-and-anchors` | QA271-02, QA271-10 | P2 | Answers the owner's stray-anchors report: a block id should stay at the row end, or the move should warn; and a trailing token should not make the handles inert |
| `table-comment-mark-after-undo` | QA271-03 | P2 | Review marks disappear after an ordinary undo |
| `frontmatter-click-lost-below-open-editor` | QA271-07 | P2 | Moving from one field to the next one below with the mouse fails |
| `table-short-delimiter-not-editable` | QA271-04 | P2 | Valid GFM tables (`:--`) silently lose table editing; one regex |
| `find-scrolls-wide-table-to-hit` | QA271-08 | P3 | Find shows "1 of 1" with nothing on screen |
| `table-in-quote-or-admonition-editing` | QA271-11 | P3 | Feature gap, raw editor still works |
| `table-paste-tsv` | QA271-12 | P3 | Spreadsheet paste convention |
| `table-keyboard-row-add-discoverable` | QA271-13 | P3 | Discoverability, plus the empty row left by Escape |
| `label-popover-covers-table` | QA271-09 | P3 | 5 s of lost clicks |
| `qa-skill-noop-sweep-gaps` | test-campaign gaps below | P3 | QA tooling, not product |

## New-feature coverage

| PR | Feature | Charter | Result |
| --- | --- | --- | --- |
| [#337](https://github.com/gsemet/markdown-okf-schema-studio/pull/337) | The cell left with Tab or an arrow shows its typed text | C2 | PASS for the display and the one-line diff; QA271-01 for the Escape that follows |
| [#338](https://github.com/gsemet/markdown-okf-schema-studio/pull/338) | A wide table keeps its Auto breakout while a cell is edited | C2 | PASS |
| [#272](https://github.com/gsemet/markdown-okf-schema-studio/pull/272) | Wide table keeps its sideways scroll across Auto re-measures | C2 | PASS (the width-mode button closes an open editor, so it was not tried with one open) |
| [#273](https://github.com/gsemet/markdown-okf-schema-studio/pull/273) | Cell editor kept in view moving through a wide table | C2 | PASS above 300 px; QA271-14 below |
| [#301](https://github.com/gsemet/markdown-okf-schema-studio/pull/301) | Table in the column when it fits, breakout when it needs to | C2 | PASS (re-measure waits for the editor to close) |
| [#306](https://github.com/gsemet/markdown-okf-schema-studio/pull/306) | Open cell editor kept in view when its table leaves the breakout | C2 | PASS on sash narrowing; toolbar-mode path not run |
| [#285](https://github.com/gsemet/markdown-okf-schema-studio/pull/285) | Row and column handles on the table's real edges | C3 | PASS (30-row and escaped-pipe tables, worst offset 0.5 px) |
| [#295](https://github.com/gsemet/markdown-okf-schema-studio/pull/295) | Row drag end to end (test PR, carried from campaign 215) | C3 | PASS for rows; one column drag did nothing (inconclusive) |
| [#317](https://github.com/gsemet/markdown-okf-schema-studio/pull/317) | Tinted table headings, even rows, hovered row | C5 | PASS in 4 themes; in Dark the even-row tint is barely visible (judgement, not filed) |
| [#282](https://github.com/gsemet/markdown-okf-schema-studio/pull/282) | Collapse and expand the properties table | C4 | PASS across an edit; document switch and reload not run |
| [#245](https://github.com/gsemet/markdown-okf-schema-studio/pull/245) | Field editor usable after a refused value | automated: realInput "refused value keeps editor usable" | PASS; the click on another field led to QA271-07 |
| [#246](https://github.com/gsemet/markdown-okf-schema-studio/pull/246) | Schema-less number from the YAML box | automated: realInput "schemaless number commits" | not run by hand |
| [#247](https://github.com/gsemet/markdown-okf-schema-studio/pull/247) | Link list editor quiet on files the table resolves | automated: realInput "link hint matches table" | not run by hand |
| [#251](https://github.com/gsemet/markdown-okf-schema-studio/pull/251) | Comments button hides every review mark | C1 | only as it touches tables: no finding; see QA271-03 |
| [#328](https://github.com/gsemet/markdown-okf-schema-studio/pull/328), [#329](https://github.com/gsemet/markdown-okf-schema-studio/pull/329) | Comment quote across a soft break; comment editor visible | C1 | not run separately (not table features) |

## Severity scale

- **High**: data loss, or a blocked journey with no way around it.
- **Medium**: wrong result or a misleading display, with a workaround.
- **Low**: friction, discoverability, cosmetic. An intent question is Low unless data is lost.

## Method

Real VS Code windows driven with real mouse and keyboard events through CDP. A spy extension
gives the buffer, and every editing scenario ends with a diff against the disk or a mark. Corpus:
the synthetic fixtures of the QA skill (new table fixtures added), `fixtures-visual/` and `docs/`.
No vault, no book. At most 2 windows at a time.

| Driver | Charters | Budget used |
| --- | --- | --- |
| A | C1 stray anchors (done, 40/40 calls), C3 table structure (partial, 39/40), C6 concurrency (partial, 40/40) | 0 replays (no High) |
| Foreman follow-up | C1b anchor drift (done, about 42/40) | reproduced twice |
| B | C2 cell editing and the wide-table line (partial, 24/40), C4 properties table (partial, about 42/40), C5 reading and clipboard (partial, about 38/40), C0 sweeps (done, about 38/40) | 1 replay (QA271-01) |

Charters are in [01-charters.md](01-charters.md). The sweep (C0) covered 7 files and found 0 real
buffer changes.

## Limits

- Not run: #306 toolbar-mode path; #282 across a document switch and a reload; the same table in
  two webviews (side preview plus Open With); `files.autoSave` with an open cell editor;
  Meta+s inside a cell editor; very wide panes and width modes with an editor open; front matter
  field sweeps (see the sweep gaps); tags and related lists, dates and empty values in the
  properties table.
- Observed once, no sheet: a leftover "Delete selected column" tooltip over the first table; a
  source edit leaving text after a row's closing pipe makes the cell open the raw editor (the
  same family as QA271-10); one tags edit in the properties table left the buffer unchanged; 69
  CSP console errors from the raw HTML of the fixture `70-release-showcase`.
- Real-mouse column drag was not started by the harness; only Alt+arrow keys moved columns.

## Test campaign gaps

- The no-op sweep commits a cell with Enter, which gives false "CHANGED" results on list-table
  cells; it should use Meta+Enter there.
- The no-op sweep finds 0 properties fields on every document, so `fields` coverage needs a
  fixture or a workspace setting.
- The no-op sweep checks the visible preview, not its file argument.
- No e2e covers tables with 1–2 dash delimiters, tables inside a quote or an admonition, or tokens
  inside the last cell during a column move.

## Tests to promote

The replays of QA271-01, QA271-02, QA271-03 and QA271-07 should become product e2e tests (data
loss, buffer diff, lost review mark, lost click). They live in
`.agents/skills/markdown-studio-exploratory-qa-claude/scenarios/` under the `271-` prefix, with
their fixtures in `assets/synth/`.

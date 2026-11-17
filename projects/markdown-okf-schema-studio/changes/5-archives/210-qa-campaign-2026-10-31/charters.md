# Charters — QA campaign 2026-10-31

Revision b9118506 (clean). Workspace `output/qa/markdown-studio-claude/ws` (book/ = copy of the
agentic-coding white paper chapters; fixtures-visual/, synth/, docs/, vault/ = private vault copy).
Budget per charter: 40 driver calls, 6 screenshots opened, 45 minutes.
Vault rule: vault copies may be explored, but their screenshots never go into evidence/; a vault
finding is reproduced on a synthetic fixture (write it under runs/<session>/ and copy the fixture
text into the sheet).

### C0 — Sweeps on real documents
- Mission: no-op sweep (open + commit without typing must not change the buffer) and latency probe.
- Areas: D1 D2 D3 E2 C1. Corpus: book/chapters/02-foundations.md (latency, use --limit/--from), 06-guidelines-governance.md, 15-road-ahead.md, fixtures-visual/73-grid-card-editing.md, fixtures-visual/68-cards-tabs-version.md, synth/tables.md, synth/frontmatter-edge.md, one vault note with properties.
- Not covered by: realInput "paragraph blur commit", "table minimal diff" (small fixtures only).
- Oracles: noop-sweep CHANGED targets (reproduce once each), latency per key vs small fixture.
- Group folder: 10-noop-sweeps/. Session: c0 (ws-c0).

### C1 — MyST grid cards, tabs and the card title editor (#230, #236)
- Mission: edit grid cards (title, body, header/footer, link cards), tab-sets, nested cards in narrow and wide previews; blur away (text box, palette, other pane, other editor); Done/Escape/Cmd+Enter.
- Areas: D2 B1 B6. Corpus: fixtures-visual/46-grid-cards.md, 68-cards-tabs-version.md, 73-grid-card-editing.md, 54-readme-showcase.md, book chapters with {grid}.
- Not covered by: visual block-editing v23–v26, myst v22–v24, v41–v45 (single fixture, one card at a time).
- Oracles: diff against mark (only the edited line changes), editor opens on the right source line, nothing stuck after blur (#227), palette inViewport, errors.
- Group folder: 01-myst-cards-tabs/. Session: c1 (ws-c1).

### C2 — Review comment threads
- Mission: create, reply, edit, resolve, reopen threads; anchors after edits of the anchored text (inline and in the source editor), after moving/deleting the block, after an external rewrite; comments toggle; Resolve popover behaviour.
- Areas: D6 F2 B1. Corpus: book chapters, fixtures-visual with threads.
- Not covered by: realInput "review comments", visual review×8/thread×5 (no edits between actions).
- Oracles: sidecar file content (diff), thread stays on the right text, popover state, errors.
- Group folder: 02-review-comments/. Session: c2 (ws-c2).

### C3 — Admonitions and the alert type dropdown
- Mission: GitHub alerts and MyST admonitions: change type via the dropdown, title and body edits, nested content, lazy continuation, dropdown with keyboard only, while scrolling, after a re-render.
- Areas: D2 B1. Corpus: book chapters with admonitions, synth fixtures, fixtures-visual admonitions.
- Not covered by: realInput "alert dropdown", "alert type pick probe" (one alert, mouse only).
- Oracles: diff against mark (only the marker line changes), dropdown inViewport, focus after pick, errors.
- Group folder: 03-admonitions/. Session: c3 (ws-c3).

### C4 — Find and replace in the preview
- Mission: Cmd+F in the preview, match navigation, replace one / all, matches inside tables, code, frontmatter, admonitions, cards; find while edit mode is on; replace then undo; case/regex options.
- Areas: B5 D7. Corpus: a long book chapter, synth/tables.md.
- Not covered by: realInput "find right after click", machine check find_bar.
- Oracles: diff against mark (exact replacements only), match count vs grep in the source, errors.
- Group folder: 04-find-replace/. Session: c4 (ws-c4).

### C5 — Table toolbar and cell editing on real chapters
- Mission: the table toolbar (rows, columns, alignment, move), cell editing with Tab/Enter/Escape, wide tables, tables with inline code, links, escaped pipes, MyST list-table/csv-table.
- Areas: D3 B6. Corpus: book chapters with tables, synth/tables.md.
- Not covered by: realInput "table cell enter", "table minimal diff", "table toolbar" (small fixtures).
- Oracles: diff against mark (only the edited row/column changes), toolbar inViewport, noClip cells.
- Group folder: 05-table-editing/. Session: c5 (ws-c5).

### C6 — Front matter and properties since the OKF v0.2 bundle
- Mission: properties table on OKF requirement files (repo requirements copied in the workspace if needed: docs/ or fixtures-visual OKF fixtures), Obsidian-style vault notes; edit each type, add/remove/rename fields, invalid YAML recovery, x-okf-link fields.
- Areas: E1 E2 E3 E4 E5. Corpus: synth/frontmatter-edge.md, synth/broken.md, fixtures-visual OKF/frontmatter fixtures, vault notes with properties.
- Not covered by: realInput "frontmatter value minimal patch", "structural minimal patch", "enter commits text field".
- Oracles: diff against mark (one field line), validation messages, errors.
- Group folder: 06-frontmatter/. Session: c6 (ws-c6).

### C7 — Width modes, wide tables and sticky headings
- Mission: width mode cycle, narrow (~380 px sash) and wide previews, wide tables (horizontal access), sticky headings while scrolling and while editing, TOC column, heading fold; theme switch.
- Areas: B2 B4 B6. Corpus: long book chapters, synth/tables.md.
- Not covered by: machine checks width_modes, width_mode_break, sticky_headings, toc_column (fixed sizes).
- Oracles: noClip, inViewport, horizontal scroll reachable, sticky band text, visual judgement (spend shots here).
- Group folder: 07-layout-and-width/. Session: c7 (ws-c7).

### C8 — Replay of the previous campaign's High findings
- Mission: rebuild a replay scenario for each High of 04-archives/001-deep-UX-analysis (UX-01, UX-03, UX-04, UX-12, UX-16, UX-17, UX-25; part-2 UX-35, UX-38) from its sheet's steps, run it, and say Fixed / Still present / Changed. Save every scenario in $SK/scenarios/ (they become Tests to promote).
- Areas: D1 D2 D3 D7 E2 C5 A3. Corpus: the sheets' fixtures.
- Oracles: as in each sheet.
- Group folder: 09-previous-highs-replay/ (one short sheet per still-present finding; the return lists all 9 verdicts). Session: c8 (ws-c8).

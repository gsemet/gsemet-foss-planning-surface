# Charter returns (coordinator log)

## C1 — partial (~36/40 calls, 0 shots)
- c1-1 | Medium | Reproduced | Link card (`:link:`) cannot be edited in the preview: every click follows the link | 01-myst-cards-tabs/c1-1-link-card-not-editable.md — triage note: no mapping for :link: cards is the designed behaviour of #236 (BLOCK-258); the finding is the missing edit path (UX).
- c1-2 | Medium | Reproduced | Enter in a `{card}` `:header:` editor inserts a blank line into the option block and the editor stays open | 01-myst-cards-tabs/c1-2-card-header-enter-adds-blank-line.md
- Not covered: wide preview; tab-set label/body editing; card footer edit; Done button; blur to another pane/editor; book chapters with {grid}; 54-readme-showcase.
- Clean: title editor Cmd+Enter / Escape / palette and click blur (nothing stuck), nested grid edits one-line diff, 0 console errors.

## C2 — done (~36/40 calls, 2 shots)
- c2-1 | Low | Reproduced | The Comments toolbar button hides only the inline chips; review threads from the comments file (highlights, badges, orphan list) stay visible | 02-review-comments/c2-1-comments-toggle-keeps-threads.md — intent question: SwRS REVIEW-152 mentions chips only.
- Clean: sidecar lines shift on save only; move / external rewrite keep threads anchored; deleting the anchored block orphans the thread; Resolve and reply write immediately even with a dirty buffer; 0 console errors.
- Added to the skill: synth fixture review-threads.md + review-threads.comments.json.
- Not covered: Delete/Reopen, last thread delete, Cmd+Alt+M, multi-block selection, invalid sidecar JSON, rename, edit mode with an open popover, Escape in compose, real corpora.

## C3 — partial (38/40 calls, 3 shots)
- c3-1 | Medium | Reproduced | A lazy continuation line of a GitHub alert renders outside the alert box and is not part of its block editor (plain blockquote renders it correctly; one-line diff, no data loss) | 03-admonitions/c3-1-alert-lazy-continuation.md — triage: compare with backlog P3 alert-palette-after-lazy-continuation.
- Observation (no sheet): the alert type list does not preselect the current type; no keyboard route to open the list.
- Harness quirks: `--var nth=3` passed as a string; Meta+ArrowUp in the block-editor textarea did not move to start (coverage note).
- Clean: type change via palette on top-level and list-item alerts, keyboard after open, menu inViewport, focus back, one-line diff; nested MyST admonition body edit one-line diff.
- Not covered: dropdown while scrolling / after re-render; MyST admonition type change; real corpora; alerts with fences or lists; MyST title edit.

## C4 — done (36/40 calls, 1 shot)
- c4-1 | Medium | Reproduced | Replace all skips matches in a list when a link URL in the same list also contains the query (4 counted, 2 replaced, no warning) | 04-find-replace/c4-1-replace-all-skips-list-with-hidden-url-match.md — fixture synth/find-list-b.md copied into the skill's assets/synth by the coordinator.
- Observation (no sheet): Cmd+Z with focus in the preview does nothing; undo of Replace all only from the source editor.
- Clean: counts match grep (minus hidden URL matches); exact diffs in tables, code, alerts, MyST notes, cards, headings; frontmatter refused; one Undo reverts Replace all; find in edit mode; 0 console errors.
- Not covered: invalid regex; Cmd+F with typed text in an inline editor; directive options and tabs; `\` / `$1` replacements; stale preview; narrow layout; vault.

## C5 — partial (37/40 calls, 2 shots)
- c5-1 | Medium | Reproduced | Tab through a wide table leaves the cell editor outside the visible preview (x=-832 after wrap, x=964 on the last column; pane 0-393) | 05-table-editing/c5-1-wide-table-editor-offscreen-after-tab.md — fixture assets/synth/c5-tables.md added to the skill.
- Notes: list-table cell opens the whole-block source editor (treated as by design); heading fold state persists per document, so a closed H1 fold hides all tables on the next open (no sheet).
- Clean: row/column insert/delete on synth and a real chapter table (only table lines change, alignment kept); toolbar inViewport/noClip; escaped pipes kept; Tab+Enter one line; Escape discards.
- Not covered: row move via handles; Shift+Tab; convert to list-table/pipe; undo after structural edits; vault tables; 02-foundations; width modes; csv-table editing.

## C6 — partial (40/40 calls, 1 shot)
- c6-1 | Medium | Reproduced | After a rejected commit (out of range value, invalid YAML in an object field) the frontmatter editor stays open, focus moves to the cell, Escape stops working, other cells will not open | 06-frontmatter/c6-1-rejected-commit-strands-editor.md — triage: likely the same as 001 part-2 UX-38 (High, open); C8 replays UX-38.
- c6-2 | Medium | Reproduced | x-okf-link list editor says "No Markdown file named related-target.md was found" for a sibling file the table resolves; suggestions list only book/ chapters | 06-frontmatter/c6-2-link-hint-says-not-found.md
- c6-3 | Medium | Reproduced | Schemaless number property opens a textarea holding "4.5\n"; Enter adds a newline, Cmd+Enter says "Enter a valid number." — edit cannot be committed | 06-frontmatter/c6-3-schemaless-number-cannot-commit.md — fixture assets/synth/vault-props.md.
- Clean: number/text/literal block edits change only their lines; checkbox; add field with custom keys (quoted); remove field; invalid YAML message + live recovery; Escape on enum/date/list/object.
- Not covered: successful enum/date/object commits; OKF requirement files; real vault notes; x-okf-link navigation/tooltips; required-field remove; additionalProperties:false picker.

## C0 — partial (~30/40 calls, 0 shots)
- c0-1 | Low | Reproduced | A paragraph made only of a link (the "Next: [Glossary]" closing line of every chapter) cannot be opened for editing; the click navigates | 10-noop-sweeps/c0-1-link-only-paragraph-not-editable.md — fixture assets/synth/linkonly.md recreated by the coordinator. Triage: same root as c1-1 (links win over edit in edit mode).
- No-op invariant: 0 CHANGED on every target really exercised (tables.md, frontmatter-edge.md, 73, 68, 15 blocks, 06 partial, 02 slices, one vault note).
- Latency: small fixture p50 56 ms; 02-foundations (1709 lines) p50 272 / p90 463 / max 582 ms (5x, under 1 s; no sheet).
- GAP c0-gap-1: noop-sweep.mjs clicks link-only blocks and navigates away, later targets "not found" (105 on 15, 79 on 06, 20 on 02); `--limit` without `--from` does not bound a blocks run; one undiagnosed "not found" on a vault wiki-link list item. | 08-test-campaign-gaps/c0-gap-1-noop-sweep-follows-links.md
- Not covered: rest of 06 (21 table rows) and 02 (cells, fields); cells pass on 15 ran on the wrong document.

## C7 — done (~38/40 calls, 4 shots)
- c7-1 | Medium | Reproduced | In a narrow side preview (393-438 px) the expanded toolbar covers the first lines of the first paragraph while the h1 wraps around it | 07-layout-and-width/c7-1-toolbar-covers-first-lines-narrow.md
- GAP c7-gap-1 (Low): TOC toggle shows active but the TOC column is display:none on narrow panes, no hint, no test | 08-test-campaign-gaps/c7-gap-1-no-toc-hidden-hint.md
- Clean: width mode cycle at 393/566/786 px; wide tables and code scroll horizontally at 220/438/786 px; sticky headings while scrolling and with an inline editor open; heading fold keeps scroll; 4 themes switch band and body together.
- Not covered: 1440 px preview (window fixed, max 786 px); real horizontal wheel/drag; sticky band at h3+; light-theme review of every width.

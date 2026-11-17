# Campaign 215 — charters

Revision `18c4f020` (main, clean tree). Baseline campaign 210 (`b9118506`). Worktree
`/Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-215` (all `$SK` paths relative to it).
Changes root: `QA_CHANGES_ROOT=/Users/az02065/Projects/DevTools/markdown-okf-schema-studio/.agents/changes`.
Campaign folder: `$QA_CHANGES_ROOT/03-requests/215-qa-campaign-2026-10-31/`.

## Driver A — radio choice lists (#240), window allowance 2

### C1 — Radio groups: clicks, keyboard, undo, structure
- Mission: use radio choice lists the way an author deciding in a plan does, and try to break the
  group rules and the one-step write.
- Areas: B1, C3, C4, D1, D2. Corpus: `fixtures-visual/74-radio-plan.md`, a new synth file written in the
  charter's workspace clone with: 2-item and 3-item groups, a lone `( )` item, `(X)` upper case, two
  `(x)` in one group, no selection, a group ended by a blank line / a heading / a non-radio item, a
  mixed `[ ]` + `( )` list, nested groups, an ordered list of radio items, radio items in a
  blockquote and inside an admonition, CRLF line endings, a radio item with inline code / a link /
  bold. Mode: side preview, then Open With editor.
- Not covered by: realInput "radio-choice" (one fixture: click, undo, selected no-op, arrows, Space,
  Enter). Explore beyond it: undo/redo chains, rapid clicks across groups, click while the source
  editor has unsaved typing on the same line, click then type in the source, keyboard from Tab
  entry, Home/End, focus after write, labels (`aria-labelledby`) on real paragraphs.
- Oracles: diff against mark (at most the two marker lines change), one undo restores, errors 0,
  notifs 0, no block editor opens on click.
- New feature: PR #240 radio choice lists, decide in the page.
- Budget: 40 driver calls, 6 screenshots, 45 minutes.
- Session: c1 (workspace ws-c1).

### C2 — Radio groups in real plans, modes, themes, narrow pane
- Mission: judge the feature where it will be shown first ("decide in the page"): a real plan
  document, every theme, every palette mode, a narrow side pane, read-only and untrusted states.
- Areas: B1, B4, D7, E2, E3. Corpus: `fixtures-visual/74-radio-plan.md`, `docs/` pages, one book
  chapter with a list turned into a radio group in the clone, a plan-like vault copy
  (exploration only, never in evidence). Mode: side preview at ~393 px and at full width; Open With.
- Not covered by: visual `gfm/v10-radio-plan-cream-900`, `gfm/v11-radio-plan-dark-900` (900 px,
  two themes, no interaction).
- Oracles: noClip, inViewport, contrast judged by eye in Light / Dark / Cream / high contrast;
  a click in an untrusted workspace or read-only root writes nothing and says why; Strict / GFM /
  MyST / Full palette modes all render the group; edit mode on and off; two previews of one file
  stay in sync after a click; an external rewrite of the file while a radio is focused.
- New feature: PR #240 radio choice lists, decide in the page.
- Budget: 40 driver calls, 6 screenshots, 45 minutes.
- Session: c2 (workspace ws-c2, `--theme light` for the light pass).

## Driver B — re-checks and never-covered, window allowance 1 (in this order)

### C0 — Sweeps after the list-marker parser change
- Mission: run the no-op sweep and the latency probe on real documents; the radio and checkbox
  marker parsers changed (B1, C3, C4).
- Corpus: 3 book chapters with many lists, `synth/tables.md`, `synth/frontmatter-edge.md`,
  `fixtures-visual/74-radio-plan.md`. Commands as in SKILL.md §3.
- Oracles: no CHANGED target; latency comparable to campaign 210.
- Budget: 40 driver calls, 2 screenshots, 30 minutes. Session: c0 (workspace ws-c0).

### C3 — Grid cards and the card title editor (#230, #236)
- Mission: edit grid cards and their titles on real chapters, beyond the fixture; state
  combinations (edit mode toggles, undo after a title edit, a card inside a blockquote, `:link:`
  cards, header/footer options, narrow pane).
- Areas: B1, D2. Corpus: book chapters with `{grid}` / `{grid-item-card}` / `{card}`, `synth/` grid
  fixtures. Mode: side preview.
- Not covered by: render tests of BLOCK-258 and visual v25/v26 (fixture only).
- Oracles: diff against mark (only the directive line changes on a title edit), errors 0.
- Re-check of PRs #230 and #236 (covered in campaign 210; regression pass).
- Budget: 40 driver calls, 6 screenshots, 45 minutes. Session: c3 (workspace ws-c3).

### C4 — Comment threads hardening (#234)
- Mission: comment threads under stress: resolve / reopen / reply quickly, the comments file
  rewritten or unreadable while a popover is open, two previews, toggling the Comments button.
- Areas: E-review. Corpus: `docs/` page and a book chapter with threads created in the clone.
- Not covered by: realInput "review comments", visual review×8 / thread×5.
- Oracles: no comment posted on a failed read, no lost reply, errors 0, notifs explain failures.
- Re-check of PR #234 (covered in campaign 210; regression pass).
- Budget: 40 driver calls, 6 screenshots, 45 minutes. Session: c4 (workspace ws-c4).

### C5 — The VS Code Agents window (#223, never covered)
- Mission: open a Markdown file with Studio from the Agents window (VS Code ≥ 1.144); switch agent
  sessions so workspace folders come and go; check Open With, the preview, edits and the review
  comments there.
- Corpus: `synth/` and `docs/`. Mode: Agents window.
- Not covered by: nothing exercises the Agents window.
- Oracles: Studio listed in Open With, preview renders, edits write to the right file, no error when
  a workspace folder disappears. If the harness cannot reach the Agents window, say exactly why in
  the return (that is a skill finding, not a product one).
- New feature (never covered): PR #223 open Studio in the VS Code Agents window.
- Budget: 30 driver calls, 4 screenshots, 30 minutes. Session: c5 (workspace ws-c5).

### C6 — Regression pass over the open QA 210 items (no new sheets)
- Mission: replay each open P1/P2 QA 210 item with its replay scenario (the `Replay` field on the
  line under the title of each `01-intent.md`) and say whether it still reproduces at `18c4f020`.
- Items (`$QA_CHANGES_ROOT/02-backlog/`): P1/frontmatter-editor-stuck-after-rejected-value;
  P2/link-only-targets-not-editable, card-header-option-enter-adds-blank-line,
  alert-palette-after-lazy-continuation, replace-all-skips-blocks-with-link-url-match,
  wide-table-tab-editor-offscreen, okf-link-hint-ignores-document-folder,
  schemaless-number-editor-cannot-commit, narrow-toolbar-covers-first-lines. Skip
  P1/unnecessary-table-margin-breakage (parked).
- Output: one line per item `REPLAY <item> | still reproduces | fixed | cannot replay: <why>`. No
  sheets, no evidence.
- Budget: 30 driver calls, 0 screenshots, 30 minutes. Session: c6 (workspace ws-c6).

## Driver A2 — radio follow-up (Foreman decision after Driver A), window allowance 1

### C7 — Radio groups: the journeys C1 and C2 could not reach
- Mission: finish #240 coverage: palette modes, guards, stale lines, a real chapter.
- Areas: B1, D1, D7, E2. Corpus: `fixtures-visual/74-radio-plan.md`, `synth/radio-c1.md`, one book
  chapter in the clone with a list turned into a radio group. Mode: side preview.
- Journeys, in this order:
  1. Palette modes Strict, GFM, MyST, Full: the group renders and a click writes in each.
  2. A click on a radio while a block editor is open elsewhere (must be refused, nothing written).
  3. Stale lines: insert two lines above the group in the source, then click at once (before the
     preview re-renders) and after; the write must hit the right lines or be refused.
  4. Read-only: add `"files.readonlyInclude": {"**/74-radio-plan.md": true}` to the clone's
     `.vscode/settings.json`, reload; a click must write nothing and say why.
  5. Untrusted: copy the clone to a folder outside any trusted parent (for example under
     `$TMPDIR/msq-untrusted-c7/`), launch with `--untrusted --workspace <that folder>`, confirm the
     Restricted Mode banner, then click. If no restricted window is possible, say exactly why.
  6. Dark and high-contrast themes on the plan fixture (judgement, one shot each at most).
- Not covered by: realInput "radio-choice"; C1, C2 of this campaign.
- Oracles: diff against mark, errors 0, a refusal is explained (toast or inline), no block editor
  opens on click.
- New feature: PR #240 radio choice lists, decide in the page.
- Budget: 40 driver calls, 6 screenshots, 45 minutes. Session: c7 (workspace ws-c7).
- Known: Tab entry stops and lost focus after a choice are already filed (215-c1-1, c2-1): do not
  re-file them.

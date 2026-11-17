# Follow-ups and reminders

- T03 review nit: every registry handler added later (T04+, T31, T36, T38, T40, T43…) must apply readOnly/trust refusals itself; reviewers of those tasks must check it.
- T03 review nit: no test for a throwing validator in the message registry.
- DONE (T07 gate, unlocked): PENDING-UNLOCK re-run gate T (integration --trusted-only) for T04 r2 and any later task gated while locked, before the phase 1 checkpoint closes.
- T05 review minor: add a literal integration test that previewEditOpen on an included block returns the {include} directive source (fold into T36 or T39, which refuse included blocks).
- T07 review minor: unit test for the linked-image capture click (stub closest on a fake IMG; plain click in edit mode -> preventDefault + previewEditOpen; metaKey or edit off -> neither). Nits: selectedCell save branch skipped by the new listener; quoted ">" inside an <img> attribute defeats the lone-img regex.
- T08 r1 finding for T09: adding padding-top to #sphinx-myst-preview-content made RI-T31 case A jump the preview from 1200 to 0 after typing (latent anchoring sensitivity to content-top offset in docs without frontmatter). T09 (40 px top gap) must avoid container padding or investigate this; tell the T09 implementer.
- T08 review nits: zoom validator does not enforce the 10 % step (rounded on apply); visual toolbar check relies on a 150 ms wait.
- T09 review minor/nits: RI-T31 does not assert the typed "x" landed; firstClearance has an extra MutationObserver callback and a layout read on every ResizeObserver tick.
- T10 review: pre-existing quirk, maxContentWidth=0 makes the sticky band padding calc invalid in Margin/Auto (fix: previewContentWidthCss emits a large px value for 0). Nits: widthModeChecks field placed inside firstElementGap doc comment (scenarios.ts); Full width assertion in capture.py is weak.
- T11 review (pre-existing exposure, for the user): text typed in an open block editor before its first autosave (400 ms) lives only in the page; a cross-document Back, a link to another file or a tab switch in that window can drop it. Candidate fix: flush/save the open editor before any document switch.
- T12 review LOW (fold into T13): stateSnapshot (scrollSync.ts ~215) drops viewToc; add viewToc: tocColumn.open(). INFO: a TOC click in the one-frame window after a patch can target a detached heading (T13 should resolve the heading by source line at click time).
- T13 review low: cream theme not in the visual contrast check (tint is theme-relative); keepVisible reads layout only when the current entry changes; stale fold keys never pruned.
- T14 open: no visual fixture for chips in light/dark/cream; scenarioCommentBlockEdit never run on old code (cannot pass without .okf-comment); <!-- --><script> stays dropped; MyST % comments unchanged.
- T15 review minor: harness-only filter in keyedComments could go; reading-line check covers one heading, not the sync anchor; no test for an inline chip click in edit mode.
- T16 open: positive diff path only unit-tested with a fake Git API (no real-repo integration); Git watch starts only after a first baseline read; included-block test not run against old code (reasoned).
- T17 low: with showIncomingChanges off, the Diff button shows until the first host message (cheap fix: put the setting in the runtime context and set data-okf-incoming-changes in installIncomingToggle). Note: at 460 px the two-row toolbar covers part of a plain first h1 in preview mode (pre-existing since T08, accepted under the U6 interpretation).
- T18 residual (accepted): "Price $5, then `$a$`" false positive; `$a\$b$` false negative; "$5 ... $a+b$" false negative; conf.py edited outside the watcher seen within 2 s.
- T19 low: conf refresh shares the "render" defer key with non-forced refreshes (extension.ts ~2894; use "render-conf"); onConfFileEvent has no debounce (coalesced by queue); failed render keeps previous diagnostics; conf.py outside workspace folders not watched.
- Integration flakiness (2026-10-16, user active): with T19, the gate-script full run (right after visual) failed 4 times in 3 different suites (realInput undo, checkboxToggle render, scroll block editor); direct full runs and standalone scroll passed; T18 baseline full passed. No mechanism found (instrumented: 0 conf events). Watch at the phase 3 checkpoint.
- DONE (phase 5 e2e green, 5eae169): re-run full test:e2e for phase 3 (4c5c869); control on 5406410 also failed (checkboxToggle undo timeout) -> environmental. Update reports 013-015 when green.
- T10b info: wrapped-cell visual detector never run against the old code; readme scenario height 1000 vs PNG 900; RTL not handled.
- T20 low: isApplePlatform() wiring from paletteShortcut has no harness test; underscore emphasis not toggled.
- USER EDITS in README.md (Linked-File heading level, reworded sentence, TODO frontmatter line) left uncommitted on purpose since T20; never stage them in a task commit.
- T21: orchestrator tightened the palette close check from 8 px to 2 px (real residual 0 px); palette mode fixed to strict until T23; no compensation at scrollY 0.
- T22: multi-line selections lose newlines in the single-line Text field; r2 tests not run against unfixed code (reasoned). MANUAL (D14): in real VS Code, Cmd+K in an open block must open the link panel (fallback Cmd/Ctrl+Shift+K).
- T23 low: after an outside-click dismissal of the native select popup on macOS a second click may be needed. MANUAL: in real VS Code with a block text box focused, Cmd+Shift+M (Ctrl+Shift+M) must focus the palette select and NOT toggle the Problems panel (fallback Alt+Shift+M on code KeyM).
- README palette section: T24+ implementers skipped README lines; before landing 016, make sure README lists the full palette (table grid, emoji, GFM/MyST groups, image, colour).
- T24 nits: Shift+Arrow consumed while grid open; Enter with nothing highlighted swallowed; Tab out of emoji filter leaves popover open.
- USER EDIT in CHANGELOG.md too (link bullet wrapped in <!-- TODO: ... -->), left uncommitted; commit.sh filters README.md and CHANGELOG.md hunks with -U0.
- DONE (T35-r2 gate T green, 9d305ac tree): PENDING-UNLOCK T25 gated with TL (screen locked); re-run trusted with keyboard suites (realInput, checkboxToggle) once unlocked, before the phase 4 checkpoint.
- tools/gate.sh level TL = compile+bundle, patch out/test/integration/trusted-suite.js to skip checkboxToggle and realInput, run --trusted-only.
- T25 low: table followed by non-blank text without a blank line converts that text too (GFM continuation); alert heads with a title not recognised; align-through-sanitizer not asserted.
- T26 low: add renderer test that <details onclick>/<kbd class> stay refused; columnAlign test with escaped/code-span pipe in caret column; raw <summary> is plain text only; footnote def always at block end.
- T27 low: duplicate labels / label equal to a heading slug can duplicate ids; float left/right not visually tested in Margin/Auto/Full or with the TOC column; scroll-to-label covered only by visual check + host history test.
- T28 low: deflist on list-item selection gives "- a\n- b\n: Definition" (no dl); label on an already-labelled block is a silent no-op (select existing name instead); no cell-scope test for sub/sup.
- T29 low: countRefUses also counts {ref} inside code samples; renaming onto an existing label is allowed; stale-version rename dropped silently (page 6 s fallback); no visual scenario for the rename popover.
- T30 question for user: in MyST mode both the GFM <kbd> button and "Key (MyST)" {kbd} show (modes additive) — hide the GFM one in MyST?
- MANUAL: T30 Document link — the native macOS open dialog must keep the block editor open.
- T30 low: refused citation key is a silent no-op (no status); ":".repeat(3) workaround for the projectFeatures literal check.
- DONE (T35-r2 gate T green): PENDING-UNLOCK T31 gate T (checkboxToggle, realInput, labelRename undo) failed with screen locked; re-run T unlocked.
- T31 low: imageReference switches to win32 rules when any path has a backslash (detect from document path only).
- MANUAL (§9.6): Image/Figure buttons — native dialog opens in the document folder, editor stays open, Cancel changes nothing.
- T32 low: untouched empty :alt: dropped on Apply; hover button not repositioned on zoom/resize; image "title" dropped on convert.
- MANUAL: T32 figure form — Cmd/Ctrl+A then typing in a field (VS Code echoes selectAll asynchronously; check no character is lost by hand).
- DONE (T35-r2 gate T green incl. 28-list-enter-adds): PENDING-IDLE full gate T on an idle machine (T33 runs failed at cell focus-loss / block-editor-close-before-undo while the user was active; list-link race fixed in 5b38a2d, not yet exercised green).
- T33 low: isSafeOkfColor trim() accepts NBSP (harmless); add tests for duplicate declarations and \63 olor escape.
- T34 low: refused colour actions are silent (no palette status mechanism); colour-code replacement written as typed.
- T35 low: no table-cell visual at 360 px (dead width<=400 branch in capture.py); dangling separator after "Col -" when the cell group wraps at <=460 px; row/col op closes an open popover.
- RESOLVED (U26, 2026-10-21: user keeps it as is, no action): user README sentence "OKF-Schema supports `x-okf-link` annotations in the JSON Schema..." was committed by mistake in 6dab226 (T25) — commit.sh -U0 split it from the heading hunk. Filter extended. Ask the user: keep, or restore the old line in a commit and leave theirs uncommitted.
- DONE (phase 5 e2e green, 5eae169): phase 4 e2e (3baa483) red only on checkboxToggle undo (run 1 user active, run 2 screen locked); re-run on an unlocked idle machine; update 016 report when green.
- DONE (T40-r1b gate T green, unlocked): PENDING-UNLOCK T36 blockMove one-undo assertion, labelRename undo, untrusted read-only refusal line; no screenshot of the move buttons (light/dark/cream).
- DONE (T40-r1b gate T green, unlocked): PENDING-UNLOCK T37 realInput scenarioBlockMoveKeys (Alt+Down x2, Cmd/Ctrl+Alt+Up in the text box) never ran; TL (T37-orch) green with checkboxToggle/realInput/labelRename/blockMove skipped.
- T37 low: unchanged-text chord sends a needless previewEditCancel (host replies stale, ignored); Ctrl+Alt+Arrow may clash with AltGr layouts; check focus ring on the moved block.
- MANUAL (§9.2): Alt+Down twice on a focused block; Cmd/Ctrl+Alt+Up inside the text box reopens the editor at the same caret.
- T38 low: no host-side active-edit check (page-only D7); no per-preview paste cap; writeFile overwrite race between readDirectory and write.
- MANUAL (§9.5): paste a screenshot into an open block editor; second paste gives image-1.png; text on the clipboard wins.
- T39 question for user: Shift+Arrow on a focused block starts a 2-block selection (block + neighbour) — keep, or select the single block first?
- DONE (T40-r1b gate T green, unlocked): PENDING-UNLOCK T39 realInput scenarioBlockSelection (Shift+click x3, Shift+Up, Escape).
- T39 low: item-2 test goes through the edit-mode toggle and does not isolate the closeBlockEdit drop.
- T40 low: Cmd/Ctrl+C with a block selection wins over a native text selection (let it through when getSelection() is non-collapsed).
- MANUAL (§9.4): select blocks, Cmd/Ctrl+C then paste in another editor; Cmd/Ctrl+X then Cmd/Ctrl+Z; Cmd/Ctrl+V after a focused "+" bar.
- T41 low: no D3 test with a span; up arrow at the top is silent.
- T42 low: overlapping quotes -> second thread gets a badge; no visual scenario for comments (realInput screenshot only).
- T43 low: a full page re-render (shell/setting/theme change, reload) drops an open compose box or reply draft (could use vscode.setState); a quote crossing elements shows as a badge.

- T44 (fea8ce5): failed-validation comment messages get no result; page times out after 15 s (INFO, no action). Orphan visual scenario builds its own markup (module markup unit-tested only).

- T45 (f44d970): LOW A: a line holding an opaque role ({ref}/{cite}) keeps its thread whatever the rest says (suggest: drop role text then require ~40% word overlap). LOW B: fuzzy ignores units (5 mg vs 5 g). Re-anchoring only while a preview is open. D30 to confirm with the user.

- P5P6: the user-mentioned `/` commands menu of the insert point does not exist in the code (only an Alert shortcut uses Slash). Question for the user: build a `/` menu (own task, reusing the palette mode filtering)?

- P2P7: Auto code block breaks out ~10 px narrower than a table (pre-existing). Headings/rules can run under the floating toolbar zone in Full/Auto (pre-existing).

- P9 B2c (a2fc92f): for P10: page-wide checks (toolbar rows/zoom, tooltip contrast, overflow, white/cream) should be global requirements; assertion-equivalent families (code-blocks v05-v12, admonition galleries) map to one requirement; long locks lines must be split into atomic SwRS; check_palette_mode asserts the "MyST" label only in MyST mode.

- P9 B3 (208333f): pruner LOW: protect folders modified < 15 min or require keep>=2 in review:finish; skip ENOENT in applyPrune; warn/refuse when git fails in trackedReportFiles; gallery staleness ignores uncommitted changes; removed-group pages never deleted. (folded into B4)

- P9 B4 (gap fill, knownIssue scenarios, product defects NOT fixed in P9):
  - P9-B4-K1: a long unbroken word and a long unbroken URL (autolink) in a paragraph are wider than the pane (the word overflows its paragraph; the link makes the whole page scroll horizontally, 1093 px wide at 900 px and 1058 px at 460 px). Scenarios rendering-core/v17 and v18 (fixture 35-cjk-rtl). Likely `overflow-wrap: anywhere` missing for paragraphs.
  - P9-B4-K2: plain Hebrew and Arabic paragraphs are left-aligned (no `dir="auto"`); GitHub right-aligns them. Raw `<p dir="rtl">` is stripped by the sanitizer, so there is no way to get RTL today. Same scenarios.
  - P9-B4-K3: an invalid Mermaid diagram gets one more "Unable to render Mermaid diagram" line prepended on every re-render (each theme switch of the toolbar adds one; 55 after the standard toolbar checks). Scenarios diagrams/v08 and v09 (fixture 40-mermaid-error). Fix: replace or remove the previous error element in mermaidPreview.ts. When fixed, remove `knownIssue` from the three scenarios (v17, v18 keep it until K1 and K2 are both fixed).
  - P9 B4 note for T2: the conf.py extension warning (plan row "conf-extension-warning") is produced by the host (mystDiagnostics), not the static page; no visual scenario. The glossary directive (` ```{glossary} `) is not rendered by the static preview (it appears as literal text); not in the MyST gallery. `{doc}` to an unknown document renders an empty link (no text).

- P9 B4: K4: GFM Caution alert renders with the Warning amber colour and triangle icon (GitHub: red, octagon) — product fix candidate. knownIssue masks a whole scenario: K1-K3 scenarios hide regressions of their passing assertions until fixed; consider per-assertion knownIssue.

# Feature session — decisions

Source of each line: **U** = user answer, **D** = recommended default accepted by the user's
round-1 rule ("apply defaults for technical points, ask only product questions").
Every D can be overridden by the user before implementation.

## Round 1 (user, 2026-10-15)

- U1. Technical points take the recommended defaults; only product questions are asked.
- U2. Edition palette sits in the page flow above the edited block, only while a block editor is
  open; in a table cell its inline buttons merge into the existing row/column bar.
- U3. Palette mode (strict / GFM / MyST) is per workspace (workspaceState, like edit mode) with a
  setting for the default (MyST). Modes are additive; the mode changes buttons, not rendering.
- U4. Tiered gate: per task compile + types + unit + contracts + security + visual + the
  integration suites touched; end of phase full `npm run test:e2e`; end of session `just preflight`
  once (it cleans `out/`, reformats the justfile, runs uv without `--no-sync`).

## Rounds 2–4 (user, 2026-10-15)

- U5. Margin: one toolbar button, 3 states cycling Margin → Auto (only tables/figures wider than the
  column break out to the pane width) → Full width; remembered per workspace like the theme.
  Covers both the P1 margin toggle and clever-margin-break.
- U6. Unified top gap of ~40 px above the first element in every case (text, heading, table,
  properties table, empty document). The edit-mode first-block frame keeps its toolbar clearance
  only if 40 px would put it under the toolbar (planner to verify and propose).
- U7. Copy button: on hover, on every code block including unlabeled ones, in preview and edit
  mode; check-mark feedback; copies the raw code text.
- U8. TOC: off by default, toolbar toggle remembered per workspace, levels h1–h4, **each node
  collapsible in the TOC column**; right column below the toolbar; hidden on narrow panes; current
  section highlighted.
- U9. Comment and TODO chips: gray chip for `<!-- -->` expanding into an admonition-like box;
  green chip for the word TODO outside code; `<!-- TODO … -->` green expandable; tool comments
  hidden; setting to turn comment chips off.
- U10. **New request:** record the shared vocabulary (chip, palette, insert point, block editor,
  toolbar, …) in a shared glossary `.agents/glossary/common.md`, referenced from `AGENTS.md`.
- U11. Incoming-change marks on by default (HEAD baseline, green left bar), toolbar toggle and
  setting to turn off; untracked files show nothing.
- U12. Pasted images saved next to the `.md` as `image.png`, then `image-1.png`, `image-2.png`;
  reference `![image.png](image.png)` with the alt text selected.
- U13. Gestures: ↑/↓ buttons on the "+" insert bar; Alt+↑/↓ moves the focused or selected blocks
  (Ctrl/Cmd+Alt+↑/↓ inside the text box); multi-select with Shift+click and Shift+↑/↓, contiguous
  only; Cmd/Ctrl+C/X/V copy, cut, paste raw Markdown.
- U14. Colour picker: the sanitizer accepts only `<span style="color:…; background-color:…">` with
  hex/rgb values; the picker wraps the selection in that span.
- U15. Ctrl+/ in the block text box toggles `<!-- TODO: … -->` around the line or selection.
- U16. Back/Next: one history per preview panel (document jumps and in-page anchors; external
  links not recorded). Zoom: per workspace, 70–200 % in 10 % steps, scales text and column.
  Toolbar on 2 rows: Refresh/Anchor/Edit/Theme, then Back/Next/Zoom−/Zoom+/Margin/TOC/Diff.
- U17. MyST warning wording: "Warning: `<syntax>` is used but this needs the MyST extension
  `<ext>`, which is not enabled in your conf.py. Add \"<ext>\" to `myst_enable_extensions`."

## Technical defaults (D)

Block operations (analysis/B-block-ops-sonnet.md §5)
- D1. Blocks coming from `{include}` cannot be moved, cut or multi-selected; fix the include
  end-line clamp first (probable existing bug).
- D2. Move granularity: whole top-level block (a list moves as one block); item moves later.
- D3. Non-blank unmapped text between two blocks (link definitions, comments): refuse the move with
  a status message.
- D4. Move = one WorkspaceEdit = one undo step; disabled while a block editor is open.
- D5. Cut + paste = two undo steps; no drag and drop.
- D6. Paste: text wins over image when both are on the clipboard.
- D7. Image paste with no open editor: ignored.
- D8. Images: max 10 MB; png/jpeg/gif/webp only (no SVG); magic bytes checked; refused in
  readOnly/untrusted/non-file/outside-workspace documents.
- D9. Edit-inline-image: first add a realInput scenario; change code only for the remaining gaps
  (image inside a link, raw HTML `<img>`, ArrowUp into frontmatter closing the editor).

Palette (analysis/D-palette-sonnet.md §6)
- D10. Undo: every palette action is one `execCommand("insertText")` (native undo, triggers
  autosave); buttons use mousedown preventDefault so the textarea keeps focus.
- D11. Emoji are inserted as Unicode characters (shortcodes do not render).
- D12. Code-language dropdown lists only languages `highlight.ts` actually highlights, plus "text".
- D13. ~~Hide a button until a render test proves the syntax renders.~~ **Superseded (user,
  2026-10-15) by intent line 8**: every palette action whose syntax does not render yet gets a
  task that adds the rendering (with a render test) before the button ships.
- D14. Shortcuts Cmd/Ctrl+K, +B, +I, +/ use preventDefault + stopPropagation; manual check in real
  VS Code; fallback Cmd/Ctrl+Shift+K if the workbench still swallows Cmd+K.
- D15. Image button in MyST mode inserts `![alt](path)`; a separate Figure button inserts
  `:::{figure}`.
- D16. Palette also shows in the "Start writing"/insert-point editor; not in the frontmatter editor.
- D17. Colour code detection: a swatch button appears when the caret is in `#rgb`, `#rrggbb`,
  `rgb(...)`; no inline swatch in the rendered page.

Diff, comments, autodetect, TODO (analysis/E-diff-comments-autodetect-sonnet.md §6)
- D18. Diff baseline HEAD via the optional built-in Git extension (no hard dependency, no git
  spawn); without Git or for untracked files: no marks.
- D19. Diff marks at block level, same green for added and modified, deleted lines not shown in v1.
- D20. Autodetect: walk up from the document to the workspace root for `conf.py`; parse it without
  executing (string lists only, non-literal = unknown, no warning); cache by mtime + watcher.
- D21. No `conf.py`: everything stays enabled, no warning.
- D22. Autodetect warns only (does not disable syntax) in v1.
- D23. Warnings shown both in the preview banner and in the Problems panel.
- D24. Tool comments (`markdownlint-*`, `prettier-ignore`, `toc`) are hidden by default.
- D25. Comments v1: threads, reply, resolve, delete, plain-text bodies, popover; orphaned threads
  kept and listed; no native Comments API in v1; author = setting → git user.name → OS user.

Other (analysis/A-copy-margin-settings-haiku.md)
- D26. Settings rework keeps every key; only descriptions, `markdownDescription`, `order` change;
  fixes the inverted scrollPreviewWithEditor text, the "Absolute" jarPath text, and the
  double-click precondition.
- D27. Copy-code uses the host clipboard (`vscode.env.clipboard`) through a validated message.
- D28. rendering-difference-on-windows: the screenshot file is 0 bytes; item stays open until a
  new screenshot is provided; no code task planned.

## S6 approval (user, 2026-10-15)

- U18. T26 (GFM proposals) approved.
- U19. T30 (MyST proposals) approved.
- U20. Planner defaults O1–O13 (PLAN.md §10) accepted as written.
- U21. Start now, run continuously, strictly sequential; keyboard suites marked pending-unlock if
  the screen locks; stop only on a blocked phase checkpoint.
- U6 interpretation (orchestrator, 2026-10-16): interactive first elements (properties table, first block editor, Start writing) get toolbar clearance when the toolbar would overlap them; plain content keeps exactly 40 px.
- D29 (orchestrator, 2026-10-16, T18 r2): conf.py locator keeps the ancestor walk first; if none found, it checks the workspace folder root for exactly one of docs/conf.py, doc/conf.py, sphinx/conf.py, source/conf.py, docs/source/conf.py; several candidates or none = no conf (no warning). Reason: the white paper keeps sphinx/conf.py beside book/, so the plain walk-up never finds it.
- U22 (user, 2026-10-16): in every width mode, tables and figures are centered and take the width they need, up to the maximum available horizontal space ("clever margin break", like Medium). Illustrate it in the README with a screenshot in the cream theme. -> task T10b (after the phase 3 checkpoint, before phase 4); amends 011-clever-margin-break.
- U23 (user, 2026-10-20): six post-plan fixes P1–P6 recorded in post-plan.md, to run after T45 and before the final preflight.
- U24. Post-plan P7: Full width mode must use the same side margins as a full-width table in Auto mode.
- U25. Backlog: items outside the plan moved to P3; block-edition-palette moved from P1 to P2.
- U26. The user README sentence committed in 6dab226 stays as is (edits are "for later"); no revert, no history rewrite; the remaining user edits stay untouched.
- U27. 2026-10-21: the user asked to commit their uncommitted edits -> 88ce48c (heading level, README TODO line, CHANGELOG TODO comment). No user edits remain in the tree; commit.sh filter is now a no-op.
- U28. Post-plan P8: floating toolbar on 3 rows (1: refresh/link/edit + collapse button for rows 2–3; 2: back/next/zoom-/zoom+; 3: theme/margin/TOC/diff).

- D30 (2026-10-21, orchestrator, T45): a thread whose quote is gone from the document is orphaned even if a block still exists at its stored line (brief "not found → orphaned", D25). realInput scenarioReviewComments t2 expectation changed accordingly (0 badges, 1 Orphaned entry). To confirm with the user at session end.
- U29. Post-plan P9: exhaustive e2e campaign audit (no duplicates, relevant varied screenshots, logical groups, PO gallery, README subset, per-scenario locked-behaviour line); requirements generation itself is NOT to be done. Runs after P1–P8.
- U30. Post-plan P10: okfreq requirements baseline (StRS/SwRS, markers, stats, skills, AGENTS.md, guideline, all okfreq features), exhaustive incl. untested behaviours; Opus analysis, Sonnet critical review; re-entrant via feature-session/p10-requirements/STATE.md. After P9.
- U31. P10 requirement ID prefixes: StRS-MDOKFSTUDIO and SwRS-MDOKFSTUDIO.
- U32. Post-plan P11: build a Notion/Obsidian-style `/` command menu with completion, filtered by palette mode; runs after P8, before P9/P10.
- U33. Before P10: run preflight, push dev/gsemet and open the GitHub PR to main, get CI green (push explicitly authorised for this step only; no force push).
- D31 (orchestrator, P11): slash menu adds Bulleted list and Numbered list entries (menu-only, palette unchanged) so /bullet, /list, /numbered work like Notion; in MyST mode MyST entries (admonitions) rank before GFM equivalents (alerts) for the same query.
- U34. 2026-10-21 ~23:45: user goes to sleep: "continue au maximum jusqu'à la fin de toutes tes tâches", no answers possible until morning. Orchestrator decides open points with conservative defaults and records them as D-decisions for review.
- D32 (orchestrator, P9, user asleep): split group frontmatter-schema into frontmatter-schema (rendering/validation) and frontmatter-editing (editing the properties table); admonitions live in group myst; the B2c locks text gets a Sonnet critic review per group. Total groups: 16.
- D33 (orchestrator, night): screen locked while the user sleeps, so the real-window batches T1/T2, the final F campaign and preflight (unlocked needed for keyboard suites) wait for an unlocked screen; order now B4, B5, then P10 preparation work that needs no screen and no commits (inventory/analysis under p10-requirements/), then T1, T2, F, preflight, push+PR, then P10 commits.
- D34 (orchestrator, P10 prep): okfreq on PATH is 0.12.0 (missing lint --check/--diff, --check-links, index navigation); the local okf-schema checkout venv (/Users/az02065/Projects/DevTools/okf-schema/.venv/bin/okfreq, v0.12.0-4, has the 0.13 features) is used for P10 — no install. Justfile recipes call `${OKFREQ:-okfreq}`; pinning okf-schema>=0.13 in a uv group + CI wiring is left as a follow-up needing the user's OK (it implies an install).
- D35 (orchestrator, P10 prep): commit trailer stays `Assisted-by: Claude:Sonnet-5.5` (user's repo rule overrides the session attribution reminder); bundle at `requirements/` repo root like okf-schema (+ `requirements/**` in .vscodeignore); no 17th scope for test infrastructure (D32 keeps 16; test/site etc. not scanned); possibly-dead src/build/* decided by the rendering-core inventory, never deleted in P10.

- U35 (2026-10-22): PR must be mergeable before requirements generation; every step resumable; PR first, then P10. Tracking: pr/STATE.md.
- D36: push to new branch `dev/gsemet-features` — remote `dev/gsemet` diverged (squash merges), a force push is forbidden.
- D37: PR = HEAD after P9-T1; P9 B5/T2/F + P10 go in a follow-up PR.
- U36 (2026-10-22): P10 parked in backlog/P3/requirements-okfreq (token cost). U37: focus on finalising the PR + local rebuild for user testing.
- U38 (2026-10-22): at session end, move requests/feature-session -> archives/021-feature-session-007-020 (after PR S7 + final report; P9 rest and parked T1 go to backlog first).
- U39 (2026-10-22): backlog built — P1 K1/K3/K4 + T11 flush; P2 P9 rest; P3 K2, requirements (Sonnet only) then refacto. T30 keep both, T39 keep 2 blocks, D30 keep orphan. Index: backlog/INDEX.md.

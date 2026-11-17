# Report — block-edition-palette

Status: **done** (feature session, 2026-10-20, branch `dev/gsemet`), pending the unlocked e2e
re-run of the checkbox undo scenario.

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T06 | `~~strikethrough~~` renders struck through | `867c21f` |
| T08 | Two-row toolbar, persisted view preferences, Zoom −/+ (70–200 %) | `201b2d6` |
| T10 | Margin button: Margin → Auto → Full width (wide tables/figures break out in Auto) | `570bcee` |
| T11 | Back / Next per preview panel (documents and in-page anchors) | `254b5e4` |
| T20 | Cmd/Ctrl+B / I (platform-specific), Ctrl+/ toggles `<!-- TODO: … -->` | `43fc386` |
| T21 | Palette bar above the edited block: heading h1–h5, bold, italic, strikethrough, code + language, quote, rule, TODO | `b572847` |
| T22 | Link panel (text + target, focus first empty field), Cmd/Ctrl+K | `8bd2bc2` |
| T23 | Mode select Strict / GFM / MyST per workspace, `editing.defaultPaletteMode`, Cmd/Ctrl+Shift+M | `3f87eda` |
| T24 | Table from a 9×9 size grid (hover highlight), emoji picker | `df1424a` |
| T25 | GFM: alert with type list, task checkbox, HTML table (convert + new) | `6dab226` |
| T26 | GFM proposals: collapsible section, footnote, Mermaid, column alignment, `<kbd>` (renderer keeps attribute-less details/summary/kbd) | `78cf915` |
| T27 | Render figure `:width:` / `:align:`, amsmath guard, `(label)=` anchor icons, `{ref}` to labels | `3ca7807` |
| T28 | MyST: admonitions (all types + custom), definition list, math (inline/display/aligned), sub/sup, label | `c23c8f2` |
| T29 | Rename a label from its anchor icon (host checks the exact line, one undo step) | `c82062e` |
| T30 | MyST proposals: `{ref}`, `{doc}` (file dialog), `{cite}` from workspace `.bib`, dropdown, table with caption, `{kbd}`; blur suspension while a host dialog is open | `f3941b3` |
| T31 | Image picker in the document folder, Figure button (MyST) | `6c35140` |
| T32 | Figure form: source (Browse), alt, caption, legend, width, align, name; untouched options kept | `82481e1` |
| T33 | `<span style>` text/background colours kept (hex, rgb/rgba only) via data attributes + CSSOM | `5b38a2d` |
| T34 | Colour picker (Text/Background, 16 swatches, hex, Remove), colour-code swatch | `8c97d64` |
| T35 | Cell-scope palette actions merged into the table-cell bar; `|` escaped | `9d305ac` |
| — | README feature list completed for the whole palette | `3baa483` |

T01 (shared glossary `.agents/glossary/common.md`, U10) has no backlog item and is reported here:
palette, insert point, block editor, anchor icon, blur commit suspension and the other session
terms were added by the tasks that introduced them.

## Proof of completion

- Every task: implementer gate (check-types, unit, visual; trusted integration) and a separate
  Sonnet review; required fixes went through extra rounds (T27 r2, T34 r2) or small orchestrator
  fixes (T28 "See also" label, T30 cross-drive `{doc}`, T31 backslash in alt text).
- Every palette action has a render test that renders the action's own output (D13 superseded).
- T35-r2 gate T (2026-10-20, tree of `9d305ac`): trusted integration green with the keyboard suites
  (realInput incl. t20–t35 scenarios, checkboxToggle, labelRename, imagePicker, mystPickers).
- Phase 4 e2e (2026-10-20, `3baa483`): unit 1382, contract 2, security 25, visual 162 scenarios /
  157 screenshots green; integration **not green** twice, both times only checkboxToggle "one undo
  to restore the original source": first run with the user active, second with the screen locked
  (`CGSSessionScreenIsLocked` true). The same scenario passed in the T35-r2 gate. **Pending: re-run
  the e2e on an unlocked idle machine** (followups.md; also covered by the final `just preflight`).

## Open items

- Manual checks: Cmd+K opens the link panel (fallback Cmd/Ctrl+Shift+K); Cmd+Shift+M focuses the
  mode select without toggling the Problems panel; Document link / Image / Figure native dialogs keep
  the block editor open; Cmd/Ctrl+A then typing in the figure form keeps the first character.
- Question for the user: MyST mode shows both the GFM `<kbd>` and the MyST `{kbd}` Key buttons.
- Post-plan P4–P6 (palette sticky on top of tall edit boxes, "MyST" label, `/` menu per mode).
- Low review notes per task (followups.md): silent refusals (colour, citation, label), deflist on
  list items, footnote definition placement, hover button not repositioned on zoom, dangling
  separator in the wrapped cell bar, no 360 px cell-bar visual.

## Intent traceability (`01-intent.md` line → task)

| Line | Intent item | Task(s) |
| --- | --- | --- |
| 3 | Floating palette in edit mode ("below the existing one") | T21 (placement superseded by line 29 and U2: above the edited block) |
| 5–6 | Extensible, simple, harmony with the floating panel | T20 (action registry), T21 (shared look) |
| 8 | Every non-supported edition → new feature | §0 note (D13 superseded): T06, T27, T33 |
| 12 | Back | T11 |
| 13 | Next | T11 |
| 14 | Zoom in/out | T08 |
| 15 | Margin on/off | T10 (3 states, U5) |
| 17 | Split on 2 lines | T08 |
| 19–25 | Mode select strict / GFM / MyST | T23 |
| 29 | Placement on top of the edited block | T21 |
| 31–32 | Table cell: merge or shift | T35 (merge, U2) |
| 36 | Title dropdown h1–h5 | T21 |
| 37 | Italic | T20 (Cmd/Ctrl+I), T21 |
| 38 | Bold | T20 (Cmd/Ctrl+B), T21 |
| 39 | Strikethrough | T06 (render), T21 |
| 40 | Code fence + language dropdown | T21 |
| 41–42 | Link, Ctrl+K, selection = text, caret at URL | T22 |
| 43 | Blockquote | T21 |
| 44 | Horizontal rule | T21 |
| 45–46 | Table 9×9 grid, hover highlight, one click | T24 |
| 47 | Image file picker, default document folder | T31 |
| 48 | Emoji picker | T24 |
| 49 | HTML colour picker, self-activated on a colour code | T33 (render), T34 |
| 50–51 | TODO indicator (icon + hover text), Ctrl+/ | T20 (shortcut), T21 (button), T14–T15 (rendered chip) |
| 57–58 | GFM admonition `>` + type dropdown at the caret | T25 |
| 59 | Checkbox | T25 |
| 60 | HTML table: convert Markdown table, add new table | T25 |
| 62 | Propose others (GFM) | §3a, T26 (approved, U18) |
| 67–68 | Inspect book/, curated MyST list | §3b, T30 (approved, U19) |
| 72 | Admonitions all types + custom | T28 |
| 73 | Footnotes | T26 (shared GFM/MyST action) |
| 74 | Definition lists | T28 |
| 75 | Math (LaTeX) | T27 (amsmath render), T28 |
| 76 | Subscript / superscript | T28 |
| 77 | Figures, image with caption | T31, T32 |
| 78 | Anchors: icon where placed, click to edit | T27 (icon), T28 (insert), T29 (edit) |
| 82 | Figure custom editor (size, caption, legend, …), edit button or bar button | T32 |
| 83 | Colour picker, text + background | T34 |
| 84 | Emoji picker at the caret | T24 |
| 85 | URL panel: 2 fields, text prefilled, focus first empty | T22 |

## Addendum (2026-10-21)

The pending e2e re-run is done: the phase 5 e2e on `5eae169` (later tree, unlocked idle machine)
passed in full, including every integration host, the keyboard suites (75 real-input screenshots)
and checkboxToggle; visual 162 scenarios / 157 screenshots. Status is now **done** without
reservation.

- Final gate: `just preflight` green in CI on `8c55e48` (run 39753045267); merged to `main` with PR #11 on 2026-10-22.

# Decisions

Each task applies the **Default** of the decisions it references. To change one, the user writes
the new choice in **Override** before the task starts. The orchestrator then passes the override to
the implementer and the reviewer. An empty Override means "apply the default". Long defaults are
detailed under the table.

| ID | Finding | Question | Default (applied) | Alternatives considered | Override |
| --- | --- | --- | --- | --- | --- |
| D-01 | UX-01 | What does Escape do in the raw-Markdown and table-cell editors? | **Close and keep**, exactly like blur. Discarding becomes an explicit **Revert** button (T15). Frontmatter editors keep Escape = cancel, since they never autosave. Turning edit mode off also keeps the text. | Escape discards after a confirmation | |
| D-02 | UX-02 | Autosave cadence | **400 ms idle debounce.** Flush immediately on blur, Cmd/Ctrl+Enter, Escape, Done, arrow-key block navigation, table cell switch, and edit mode off. Each flush sends only the changed range. | Commit-only (loses the live source update) | |
| D-03 | UX-04 | Enter in the raw-Markdown editor | **Continue the construct of the current line** (see details) | Open the whole top-level list | |
| D-04 | UX-05 | Tab / Shift+Tab in the raw-Markdown editor | **Indent / outdent the selected lines.** List lines move by their marker width; other lines by 4 spaces. Collapsed caret on prose: 4 spaces at the caret. Exit route: Escape, then Tab. | Insert a literal tab | |
| D-05 | UX-13 | Tab in a table cell | **Next cell, wrapping rows.** On the last cell, insert a row and continue in it. Shift+Tab goes back and stops at the first header cell. | Tab on the last cell leaves the table | |
| D-06 | UX-17 | Enter in a frontmatter text field | **Value without a line break:** Enter saves, Shift+Enter breaks the line. **Value with a line break:** Enter breaks the line, Cmd/Ctrl+Enter saves. Trailing line breaks are trimmed on save unless the original value ended with one. | Always single-line inputs | |
| D-07 | UX-19 | Links in the properties table; list completion | **Edit mode:** a plain click edits; Cmd/Ctrl+click navigates. **Reading mode:** unchanged. Suggestions only for `filename-stem` x-okf-link list items, at most 500. An unknown target shows a non-blocking warning. | Block saving unknown targets | |
| D-08 | UX-21 | Adding and removing fields | **Custom keys** unless the schema sets `additionalProperties: false`. **Placement:** insert after the row whose ⊞ was used. **Picker:** a select choice confirms immediately; the text variant confirms with Enter. **After adding:** the new field's editor opens. **Required fields:** ⊟ disabled, with a tooltip. | Insert in schema order | |
| D-09 | UX-23 | Problems panel diagnostics | **Not in this plan** (optional follow-up). In the preview: a human label and icon instead of `[E10]`, a keyboard-accessible custom tooltip, and a badge button that jumps to the first issue. | Add a `DiagnosticCollection` | |
| D-10 | UX-28 | In-place content patching | **Behind the new setting `markdownOkfSchemaStudio.preview.incrementalUpdates`.** Default `true` only if T34 passes full + visual + review; otherwise `false` and logged in `followups.md`. | No setting | |
| D-11 | process | Commits | **One local commit per task on the current branch, never pushed.** Only the task's files are staged. | No commits (harder to resume and bisect) | |
| D-12 | process | Models | **Implementer `sonnet`** at its normal effort (no `effort` parameter); **reviewer `opus`** with `effort: "low"`. Changed by the user on 2026-10-09 after T06; T00–T06 ran with implementer `haiku` and reviewer `opus` at normal effort. No silent escalation; after two failed fix rounds, ask the user. | Implementer `haiku` (initial user requirement); reviewer `sonnet` | |
| D-13 | UX-30 | Entry points | **Editor-title button, explorer entry, and keybinding** (see details) | No keybinding | |
| D-14 | UX-31 | Custom editor display name | **`MyST + OKF Studio`.** The extension display name stays `Markdown OKF-Schema Studio`. | `Studio (MyST/OKF)` | |
| D-15 | UX-32 | Tab titles | **Side preview:** `Studio · <file>`. **Open With editor:** `<file>`. | `Preview <file>` (clashes with the built-in) | |
| D-16 | UX-33 | Toolbar state | **Anchor button:** disabled with the tooltip "No text editor shows this file" when no visible text editor shows the document. **Edit mode:** persisted per workspace; a webview's own saved state wins. **Anchor icon:** chain link instead of a padlock. | Hide the button | |
| D-17 | UX-27 | Keep the side preview visible | **Lock the editor group** the side preview creates, only when it is alone in its new group. | Move editors opened there back to the source group | |
| D-18 | UX-14 | Table toolbar | **In flow, directly above the table.** Short text labels ("Row +", "Row −", "Col +", "Col −"). Position text "Header · column 2 of 5" or "Row 2 of 6 · column 2 of 5". The selected cell is outlined. | Keep the floating per-cell placement | |
| D-19 | UX-15 | Wide tables | **Overflowing tables:** short identifier cells (24 characters or fewer, no whitespace) do not wrap; scroll shadows mark the overflow. No sticky scrollbar. | Sticky first column | |
| D-20 | UX-10 | Inserting blocks | **Zero-height "+" insertion points** between top-level blocks and after the last one, in edit mode only. The new block is separated by blank lines. An empty body shows "Start writing". No template menu. | Slash-command menu | |
| D-21 | UX-06 | Caret when the click cannot be mapped confidently | **End of block** (today's behaviour) | Start of block | |
| D-22 | UX-08 | Editor font | **Monospace editor font** (`--vscode-editor-font-family`, `tab-size: 4`) for the raw-Markdown block editor and the frontmatter YAML textarea. One-line frontmatter text fields and table cells keep the preview font. | Monospace everywhere | |
| D-23 | UX-20 | Frontmatter field actions | **Inside the editing row**, in normal flow after the control, with short text labels. The pseudo-tooltips are disabled for this menu; native titles remain. | Floating, clamped to the viewport | |

## Details

### D-03 — Enter in the raw-Markdown editor

- **List markers continue:**
  - a dash, star or plus bullet keeps its character;
  - `N.` becomes `N+1.`, and `N)` becomes `N+1)`;
  - a task item continues as an unchecked task.
- **Blockquote:** the quote prefix continues.
- **Plain lines:** their leading indentation is kept.
- **Empty item:** Enter on an item whose body is empty removes the marker, leaving the list.
- **Shift+Enter:** inserts a bare line break.
- **Inside a fenced code block:** only indentation is carried.

### D-13 — Entry points

- **Editor-title button** with the `$(book)` icon, in the `navigation` group. It appears for
  `resourceExtname == .md` in text editors only.
- **Explorer context entry** "Open Preview to Side" for `.md` files.
- **Keybinding:** Cmd+K Shift+V on macOS, Ctrl+K Shift+V elsewhere, when
  `editorTextFocus && resourceExtname == .md`.
- **Command:** the open-preview command accepts an optional URI, which menus pass.

### D-18a — Orchestrator refinement of D-18 (2026-10-10, during T18; user may override)

With the toolbar in flow above the table, a click on a cell near the top of the viewport left the
two-row narrow toolbar above the viewport (the R7 anchor keeps the cell fixed). Applied rule: when
the toolbar first appears for a table and would be hidden above the usable top (below the sticky
heading band), the preview scrolls just enough to reveal it, provided the selected cell stays
visible. Otherwise the cell stays fixed (R7). Alternative not applied: keep the cell fixed and
accept a toolbar that is off-screen in that case.

### D-20 — Command category (user, 2026-10-13, after T40)

Both commands use `"category": "Markdown OKF-Schema Studio"`. Their titles are the short forms:
"Open Preview to Side" (the D-13 text) and "Refresh Preview".
- The Command Palette still shows "Markdown OKF-Schema Studio: Open Preview to Side".
- The Explorer menu and the title-bar tooltip show the short title only.

### D-21 — Remaining UX-21 gaps (user, 2026-10-13, after T40)

- **a.** A new field is inserted in the source at the position its row takes in the properties
  table, not after the clicked row.
- **b.** A new custom key is a one-line text by default:
  - Enter saves it, and Shift+Enter inserts a line break;
  - the value is written as a plain YAML scalar when that is safe (`approver: Ann`), and quoted
    only when YAML requires it.
- **c.** Escape cancels the open frontmatter edit wherever the focus is inside the properties
  section, for example on the field picker or a header cell. This matches the field controls,
  where Escape already cancels. It also matches the user's rule that Escape means Cancel in every
  editor; for the block and table-cell editors, that rule is tracked in
  `requests/bug-edition-mode/`.

### D-22 — No pending banner while typing; delayed overlay (user, 2026-10-13; supersedes T29's design)

- While the user types, the preview page is not touched. There is no reload and no in-flow
  "Preview pending" banner, and the previous render stays visible.
- When a render is still pending about **1.5 s** after the edit, a **floating overlay banner**
  appears in the open page, without a reload. It sits at the top right, below the floating toolbar,
  with `position: fixed` and `pointer-events: none`, so the content never moves. The next ready
  render replaces the page, which removes it.
- These cases are unchanged:
  - the first render, when there is no rendered page yet, keeps the status page;
  - `stale` and `error` keep their current pages;
  - the missing-source page.

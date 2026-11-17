# T36 review — round 1

Base: 9cb75e1 · Reviewed diff: 6 files (package.json, extension.ts, README.md, package-contract, lifecycle, realInput)

## Gates
compile, unit, types, contracts: PASS; trusted: PASS 81 s; full: PASS 203 s (`logs/T36-*.log`).
No new failures compared with the T00 baseline.

## Done-when
- [x] unit and trusted gates pass — logs above.
- [x] RI-T36 passes — `PASS real-input screenshot: 36-title-bar-button`; real `.click()` on
  `.editor-actions .codicon-book`. On base 9cb75e1 `package.json` has no `editor/title` entry and no
  icon, so the locator count stays 0 and the scenario would time out (red on base, by reading).
- [x] Menu URI opens that file — lifecycle check. On base `openPreview()` takes no argument, so the
  preview would stay on `firstDocument` and the `waitFor` on `secondDocument` would time out (red on base).

## Protected features checked
P-L9 / D-13 (opt-in posture): no `markdown.*` key; `assert.doesNotMatch(serialized, /markdown\./u)`
kept; customEditors priority `option` and activation events unchanged. The `editor/title` `when`
(`activeEditor == workbench.editors.files.textFileEditor`) keeps the button off the Open With
custom editor, diff/output/untitled-non-.md editors. Keybinding `cmd+k shift+v` / `ctrl+k shift+v`
is not bound by the built-in `markdown-language-features` (it binds `cmd+k v` and `shift+cmd+v`
only, checked in the installed VS Code bundle). Command palette entries unchanged.
P-L (preview lifecycle): without an argument, `openPreview` runs the unchanged body (palette and
keybinding path); covered by existing lifecycle and trusted suites.

## Findings
1. [MINOR] extension.ts:openPreview — when invoked from the Explorer while the Studio webview has
   focus (no active text editor), `showTextDocument(opened, { preview: false })` uses the active
   group, which can be the preview's group. Follow-up: pass `viewColumn: ViewColumn.One` (or the
   column of the last text editor) and add a lifecycle case with the preview focused.
2. [MINOR] package.json explorer/context — the Explorer entry shows the full title "Markdown
   OKF-Schema Studio: Open Preview to Side". Acceptable (it names the provider, avoiding confusion
   with the built-in entry); a shorter menu title would need a separate command and is a follow-up.
3. [NIT] Error path: the message "Cannot open <path>: <error>" contains no "Sphinx"; a non-file
   scheme (`untitled:`) and a URI equal to the active document skip the open step as required.
   The error path itself has no test; acceptable for a low-risk branch.
4. [NIT] The RI-T36 screenshot is taken after the click; the book icon is not visible in it (focus
   moved to the preview), but the opened side preview proves the click worked.

## Existing assertions changed
- package-contract: `icon: "$(book)"` added — OK (listed in task).
- `menus["editor/title"] === undefined` replaced by exact deepEqual — OK (listed in task).
- explorer/context and keybindings deepEqual — additions, OK.
No other assertion changed.

VERDICT: PASS

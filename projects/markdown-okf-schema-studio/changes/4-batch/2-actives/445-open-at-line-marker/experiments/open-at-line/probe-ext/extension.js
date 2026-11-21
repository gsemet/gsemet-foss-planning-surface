// Trial probe extension (CR-445): logs tab, editor and selection events to PROBE_LOG, and executes the
// JSON command found in PROBE_CMD (answer in PROBE_OUT). Loaded next to the extension under test.
const vscode = require("vscode");
const fs = require("node:fs");
const t0 = Date.now();
const LOG = process.env.PROBE_LOG, CMD = process.env.PROBE_CMD, OUT = process.env.PROBE_OUT;
const log = (o) => fs.appendFileSync(LOG, JSON.stringify({ t: Date.now() - t0, ...o }) + "\n");
const kindOf = (i) => !i ? "none" : i instanceof vscode.TabInputText ? "text" : i instanceof vscode.TabInputTextDiff ? "diff" : i instanceof vscode.TabInputCustom ? "custom:" + i.viewType : i instanceof vscode.TabInputWebview ? "webview" : "other";
const uriOf = (i) => (i && (i.uri || i.modified)) ? (i.uri || i.modified).toString() : undefined;
const tabInfo = (tab, g) => ({ g: g.viewColumn, label: tab.label, kind: kindOf(tab.input), uri: uriOf(tab.input), active: tab.isActive, dirty: tab.isDirty, preview: tab.isPreview });
function state() {
  return {
    tabs: vscode.window.tabGroups.all.flatMap((g) => g.tabs.map((t) => tabInfo(t, g))),
    visible: vscode.window.visibleTextEditors.map((e) => ({ uri: e.document.uri.toString(), col: e.viewColumn, sel: [e.selection.start.line, e.selection.start.character], dirty: e.document.isDirty })),
    active: vscode.window.activeTextEditor ? { uri: vscode.window.activeTextEditor.document.uri.toString(), sel: [vscode.window.activeTextEditor.selection.start.line, vscode.window.activeTextEditor.selection.start.character] } : null,
  };
}
async function run(c) {
  switch (c.op) {
    case "state": return state();
    case "open": {
      const sel = c.line !== undefined ? new vscode.Range(c.line - 1, 0, c.line - 1, 0) : undefined;
      await vscode.commands.executeCommand("vscode.open", vscode.Uri.file(c.file), { selection: sel, viewColumn: c.col, preview: c.preview });
      return "ok";
    }
    case "config": await vscode.workspace.getConfiguration(c.section).update(c.key, c.value, vscode.ConfigurationTarget.Global); return "ok";
    case "exec": return (await vscode.commands.executeCommand(c.command, ...(c.args || []))) ?? "ok";
    case "ext": { const e = vscode.extensions.getExtension(c.id); return e ? { active: e.isActive } : "missing"; }
    case "doc": { const d = vscode.workspace.textDocuments.find((x) => x.uri.fsPath.toLowerCase().endsWith(c.file.toLowerCase())); return d ? { dirty: d.isDirty, text: d.getText().slice(0, 300) } : "none"; }
    case "edit": { const e = vscode.window.visibleTextEditors.find((x) => x.document.uri.fsPath.toLowerCase().endsWith(c.file.toLowerCase())); await e.edit((b) => b.insert(new vscode.Position(0, 0), "EDITED ")); return "ok"; }
  }
  return "unknown op";
}
exports.activate = (ctx) => {
  log({ ev: "probe-active", exts: vscode.extensions.all.filter((e) => e.id.includes("okf")).map((e) => e.id + ":" + e.isActive) });
  ctx.subscriptions.push(
    vscode.window.tabGroups.onDidChangeTabs((e) => log({ ev: "tabs", opened: e.opened.map((t) => tabInfo(t, t.group)), closed: e.closed.map((t) => tabInfo(t, t.group)), changed: e.changed.map((t) => tabInfo(t, t.group)) })),
    vscode.window.onDidChangeActiveTextEditor((e) => log({ ev: "active", uri: e && e.document.uri.toString(), sel: e && [e.selection.start.line, e.selection.start.character] })),
    vscode.window.onDidChangeVisibleTextEditors((es) => log({ ev: "visible", eds: es.map((e) => ({ uri: e.document.uri.toString(), col: e.viewColumn, sel: [e.selection.start.line, e.selection.start.character] })) })),
    vscode.window.onDidChangeTextEditorSelection((e) => log({ ev: "selection", uri: e.textEditor.document.uri.toString(), kind: e.kind, sel: e.selections.map((s) => [s.start.line, s.start.character]) })),
  );
  let busy = false;
  const timer = setInterval(async () => {
    if (busy || !fs.existsSync(CMD)) return;
    busy = true;
    try {
      const c = JSON.parse(fs.readFileSync(CMD, "utf8")); fs.unlinkSync(CMD);
      let r; try { r = await run(c); } catch (e) { r = { error: String(e) }; }
      fs.writeFileSync(OUT, JSON.stringify({ id: c.id, r }));
    } catch (e) {} finally { busy = false; }
  }, 100);
  ctx.subscriptions.push({ dispose: () => clearInterval(timer) });
};

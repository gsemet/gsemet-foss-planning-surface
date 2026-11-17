const vscode = require("vscode");
const fs = require("fs");
const path = require("path");
const out = process.env.PROBE_OUT;
function write(name, data) { if (out) fs.writeFileSync(path.join(out, name), JSON.stringify(data, null, 2)); }
function tabs() {
  return vscode.window.tabGroups.all.flatMap((g) => g.tabs.map((t) => ({
    label: t.label, active: t.isActive,
    kind: t.input && t.input.constructor ? t.input.constructor.name : typeof t.input,
    viewType: t.input && t.input.viewType, uri: t.input && t.input.uri && t.input.uri.toString(),
  })));
}
async function run(target) {
  const studio = vscode.extensions.getExtension("GaetanSemet.markdown-okf-schema-studio");
  const r = {
    when: new Date().toISOString(), appName: vscode.env.appName, uiKind: vscode.env.uiKind, appHost: vscode.env.appHost,
    workspaceFolders: (vscode.workspace.workspaceFolders || []).map((f) => f.uri.toString()),
    workspaceName: vscode.workspace.name, workspaceFile: vscode.workspace.workspaceFile && vscode.workspace.workspaceFile.toString(),
    isTrusted: vscode.workspace.isTrusted,
    studioFound: !!studio, studioActiveBefore: studio && studio.isActive,
    extensions: vscode.extensions.all.filter((e) => !e.id.startsWith("vscode.")).map((e) => e.id + (e.isActive ? " (active)" : "")),
  };
  try {
    const cmds = await vscode.commands.getCommands(true);
    r.studioCommands = cmds.filter((c) => c.startsWith("markdown-okf-schema-studio."));
  } catch (e) { r.cmdError = String(e); }
  if (target) {
    const uri = vscode.Uri.file(target);
    r.targetWorkspaceFolder = (vscode.workspace.getWorkspaceFolder(uri) || {}).uri?.toString() ?? null;
    try {
      await vscode.commands.executeCommand("vscode.openWith", uri, "markdown-okf-schema-studio.editor");
      await new Promise((res) => setTimeout(res, 4000));
      r.openWith = "ok";
    } catch (e) { r.openWith = "error: " + (e && e.message || e); }
    r.studioActiveAfter = studio && studio.isActive;
    r.tabs = tabs();
  }
  return r;
}
exports.activate = async (context) => {
  context.subscriptions.push(vscode.commands.registerCommand("agentsProbe.run", async () => write("probe-cmd.json", await run(process.env.PROBE_TARGET))));
  write("probe-start.json", await run(undefined));
  setTimeout(async () => write("probe.json", await run(process.env.PROBE_TARGET)), 6000);
};

// Scenario mode (PROBE_SCENARIO=folders): wait for go-<n> files between phases.
async function waitGo(n) { while (!fs.existsSync(path.join(out, `go-${n}`))) await new Promise((r) => setTimeout(r, 300)); }
async function folders() {
  const ws = path.dirname(process.env.PROBE_TARGET);
  const snap = (phase) => write(`phase-${phase}.json`, { phase, folders: (vscode.workspace.workspaceFolders || []).map((f) => f.uri.toString()), tabs: tabs(), studioActive: vscode.extensions.getExtension("GaetanSemet.markdown-okf-schema-studio")?.isActive });
  await vscode.commands.executeCommand("vscode.openWith", vscode.Uri.file(process.env.PROBE_TARGET), "markdown-okf-schema-studio.editor");
  await new Promise((r) => setTimeout(r, 5000)); snap("1-opened-no-folder");
  await waitGo(1);
  const changed = new Promise((r) => { const d = vscode.workspace.onDidChangeWorkspaceFolders(() => { d.dispose(); r(); }); });
  write("mount.json", { ok: vscode.workspace.updateWorkspaceFolders(0, 0, { uri: vscode.Uri.file(ws), name: "session-worktree" }) });
  await changed; await new Promise((r) => setTimeout(r, 3000)); snap("2-folder-mounted");
  await waitGo(2);
  await vscode.commands.executeCommand("vscode.openWith", vscode.Uri.file(path.join(ws, "second.md")), "markdown-okf-schema-studio.editor");
  await new Promise((r) => setTimeout(r, 5000)); snap("3-opened-after-mount");
  await waitGo(3);
  const changed2 = new Promise((r) => { const d = vscode.workspace.onDidChangeWorkspaceFolders(() => { d.dispose(); r(); }); });
  vscode.workspace.updateWorkspaceFolders(0, 1);
  await changed2; await new Promise((r) => setTimeout(r, 3000)); snap("4-folder-unmounted");
}
const baseActivate = exports.activate;
exports.activate = async (context) => {
  if (process.env.PROBE_SCENARIO === "folders") { setTimeout(() => folders().catch((e) => write("error.json", { e: String(e && e.stack || e) })), 4000); return; }
  return baseActivate(context);
};

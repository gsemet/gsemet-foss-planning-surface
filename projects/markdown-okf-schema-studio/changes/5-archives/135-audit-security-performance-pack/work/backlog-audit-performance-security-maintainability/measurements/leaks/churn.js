// Headless PreviewManager churn: open/close N previews over R rounds, type in each, report heap,
// live host subscriptions, watchers and Node timers. Run: node --expose-gc churn.js [N] [R] [EDITS]
const fs = require("node:fs");
const path = require("node:path");
const ROOT = "/Users/az02065/Projects/DevTools/markdown-okf-schema-studio/out/src";
const { PreviewManager } = require(`${ROOT}/session/previewManager`);
const { createMemoryDocumentStore } = require(`${ROOT}/host-memory/memoryDocumentStore`);
const N = +(process.argv[2] ?? 50), R = +(process.argv[3] ?? 6), EDITS = +(process.argv[4] ?? 10);
const ws = path.join(__dirname, "ws"); fs.mkdirSync(ws, { recursive: true });

let subs = 0, watchers = 0, posts = 0;
const ev = () => (listener) => { subs++; let d = false; const o = { dispose() { if (!d) { d = true; subs--; globalThis.__untrack?.(o); } } }; return globalThis.__trackSub ? globalThis.__trackSub(o) : o; };
function source(i) {
  let s = `---\ntitle: Doc ${i}\n---\n# Document ${i}\n\n`;
  for (let k = 0; k < 40; k++) s += `## Section ${k}\n\nSome *text* with \`code\` and a [link](doc${(i + 1) % N}.md) ${"lorem ipsum ".repeat(12)}\n\n- item a\n- item b\n\n`;
  s += "```{mermaid}\ngraph TD; A-->B; B-->C;\n```\n\n```{uml}\n@startuml\nA -> B: hi\n@enduml\n```\n\n$$x^2+y^2$$\n\n```python\nprint('x')\n```\n";
  return s;
}
const store = createMemoryDocumentStore(); globalThis.__store = store;
const docs = [];
for (let i = 0; i < N; i++) {
  const p = path.join(ws, `doc${i}.md`); const text = source(i); fs.writeFileSync(p, text);
  docs.push(store.add(store.idOf(p), text, p));
}
const folder = { id: "file://" + ws, path: ws, name: "ws" };
const section = { get: (_k, d) => d };
const stub = (name) => new Proxy(function () {}, { get: (t, k) => k === "then" ? undefined : stub(`${name}.${String(k)}`), apply: () => undefined });
const base = {
  capabilities: { editorPairing: false },
  documents: store, files: { stat: async () => ({ type: 1 }), readFile: async (p) => fs.readFileSync(p), readDirectory: async () => [] },
  settings: { section: () => section, onDidChange: ev() },
  workspace: { trusted: true, onDidGrantTrust: ev(), folders: () => [folder], folderOf: () => folder, findFiles: async () => [] },
  watcher: { watch() { watchers++; let d = false; return { onDidCreate: ev(), onDidChange: ev(), onDidDelete: ev(), dispose() { if (!d) { d = true; watchers--; } } }; } },
  vcs: { headText: async () => undefined, watchHead: () => undefined, userName: async () => undefined },
  editors: { visible: () => [], active: () => undefined, paired: () => undefined },
  ui: { showWarning: async () => undefined, showError: async () => undefined, showInfo: async () => undefined },
  diagnostics: { create: () => ({ set() {}, delete() {}, clear() {}, dispose() {} }) },
};
const host = new Proxy(base, { get: (t, k) => k in t ? t[k] : stub(String(k)) });
const groups = { lockNewPanelGroup: async () => false, release: () => undefined };
const manager = new PreviewManager(host, groups);
const storeSub = store.onDidChange((e) => manager.events.onDocumentChanged(e));

function panel() {
  const disposeHandlers = new Set();
  const p = {
    html: "", cspSource: "vscode-resource:", bundleRoot: undefined, title: "", visible: true, active: false, column: 2,
    assets: { bundleUri: () => undefined, resourceUri: () => undefined, asWebviewUri: (x) => x },
    setResourceRoots() {}, postMessage: async () => { posts++; return true; }, reveal() {},
    onDidReceiveMessage: ev(), onDidChangeViewState: ev(), onDidChangeLayout: ev(),
    onDidDispose: (l) => { subs++; disposeHandlers.add(l); return { dispose() { if (disposeHandlers.delete(l)) subs--; } }; },
    dispose() { for (const l of [...disposeHandlers]) l(); },
  };
  return p;
}
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const timers = () => process.getActiveResourcesInfo().filter((x) => x === "Timeout").length;
async function settle() { for (let i = 0; i < 40; i++) { await sleep(25); if (timers() === 0) break; } }
function snap(label) {
  global.gc(); global.gc();
  const m = process.memoryUsage();
  console.log(`${label.padEnd(22)} heapUsed=${(m.heapUsed / 1048576).toFixed(1)}MB rss=${(m.rss / 1048576).toFixed(0)}MB live=${manager.sessions().size} subs=${subs} watchers=${watchers} timers=${timers()} resources=${process.getActiveResourcesInfo().length} posts=${posts}`);
  return m.heapUsed;
}

(async () => {
  // Warm the MyST engine once so the baseline includes it.
  { const s = manager.createSession(panel(), docs[0], folder); manager.startRender(s, docs[0]); await settle(); s.panel.dispose(); await settle(); }
  const h0 = snap("baseline (warm)");
  const heaps = [];
  for (let r = 1; r <= R; r++) {
    let sessions = docs.map((d) => { const s = manager.createSession(panel(), d, folder); manager.startRender(s, d); return s; });
    await settle();
    for (let e = 0; e < EDITS; e++) {
      await Promise.all(docs.map((d) => store.applyEdits(d, [{ start: d.getText().length, end: d.getText().length, text: `typed ${e}\n` }])));
      await sleep(10);
    }
    await settle();
    if (r === 1) snap(`round ${r} open`);
    sessions.forEach((s) => s.panel.dispose());
    const probe = new WeakRef(sessions[0]); sessions = null;
    await settle();
    heaps.push(snap(`round ${r} closed`));
    console.log(`  session[0] collected: ${probe.deref() === undefined}`);
  }
  const slope = (heaps[heaps.length - 1] - heaps[0]) / Math.max(1, heaps.length - 1) / 1024;
  console.log(`delta baseline->last closed: ${((heaps[heaps.length - 1] - h0) / 1048576).toFixed(2)}MB; per-round slope after round 1: ${slope.toFixed(1)}KB`);
  storeSub.dispose();
})().catch((e) => { console.error(e); process.exit(1); });

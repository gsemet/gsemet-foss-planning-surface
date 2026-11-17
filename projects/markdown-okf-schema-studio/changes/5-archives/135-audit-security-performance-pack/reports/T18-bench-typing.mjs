// bench-typing.mjs (audit measurement, extended for T18): 50 single-character edits in the middle
// of a generated document; per edit, the render time and the longest stall of the host thread
// (largest gap between ticks of a 5 ms interval) while the render runs.
// usage: node bench-typing.mjs <compiled out/src dir> <lines> [worker]
import { createRequire } from "node:module";
import { genDoc } from "./gen-doc.mjs";
const req = createRequire(import.meta.url);
const [O, n = "10000", mode = "inprocess"] = process.argv.slice(2);
const pipeline = req(O + "/core/render/renderPipeline.js");
const worker = mode === "worker" ? req(O + "/node-services/renderWorker.js").createWorkerRenderer() : undefined;
const root = "/tmp/bench-ws";
const opts = (text, id) => ({
  document: { uri: { scheme: "file", fsPath: root + "/doc.md" }, languageId: "markdown", version: id, getText: () => text },
  workspaceRoot: root, requestId: id, isWorkspaceTrusted: () => true, plantUmlEngine: "builtin",
  ...(worker ? { renderSource: worker.render } : {}),
});
const median = (a) => [...a].sort((x, y) => x - y)[a.length >> 1];
function watch() {
  let last = performance.now(), longest = 0;
  const t = setInterval(() => { const now = performance.now(); longest = Math.max(longest, now - last); last = now; }, 5);
  return () => { clearInterval(t); return Math.max(longest, performance.now() - last); };
}
let text = genDoc(+n); const lines = text.split("\n");
const mid = lines.findIndex((l, i) => i > lines.length / 2 && l.startsWith("Paragraph"));
let pos = lines.slice(0, mid).join("\n").length + 10;
for (let i = 0; i < 3; i++) await pipeline.renderPreviewDocument(opts(text, i));
const rend = [], stall = [];
for (let i = 0; i < 50; i++) {
  text = text.slice(0, pos) + "x" + text.slice(pos); pos++;
  const stop = watch();
  const s = performance.now();
  await pipeline.renderPreviewDocument(opts(text, 10 + i));
  rend.push(performance.now() - s);
  stall.push(stop());
}
console.log(JSON.stringify({ mode, lines: lines.length, render_median_ms: median(rend).toFixed(1), render_max_ms: Math.max(...rend).toFixed(1),
  host_stall_median_ms: median(stall).toFixed(1), host_stall_max_ms: Math.max(...stall).toFixed(1) }));
worker?.dispose();

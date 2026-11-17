import { createRequire } from "node:module";
import { genDoc } from "./gen-doc.mjs";
const c = createRequire(import.meta.url)("./common.cjs");
const sizes = process.argv.slice(2).map(Number);
const med = c.median;
async function bench(fn, warm = 3, runs = 5) {
  let r; for (let i = 0; i < warm; i++) r = await fn();
  const ts = []; for (let i = 0; i < runs; i++) { const [d, x] = await c.t(fn); ts.push(d); r = x; }
  return [med(ts), r];
}
for (const n of sizes) {
  const text = genDoc(n); const lines = text.split("\n").length;
  const row = { n, lines, inKB: Math.round(text.length / 1024) };
  const slow = n >= 50000; const w = slow ? 1 : 3, r = slow ? 3 : 5;
  [row.parse] = await bench(() => c.mystEngine.parseMystSource(text), w, r);
  let res; [row.renderMyst, res] = await bench(() => c.mystRenderer.renderMyst(text, { sourcePath: c.root + "/doc.md" }), w, r);
  row.htmlKB = Math.round(res.html.length / 1024); row.diags = res.diagnostics.length;
  let pr; [row.renderPreview, pr] = await bench(() => c.pipeline.renderPreviewDocument(c.opts(text)), w, r);
  [row.annotate] = await bench(async () => c.mapping.annotateSourceMappings(pr.html, { documentId: "d", activeSourceFile: c.root + "/doc.md" }), w, r);
  const mapped = c.mapping.annotateSourceMappings(pr.html, { documentId: "d", activeSourceFile: c.root + "/doc.md" });
  [row.sanitize] = await bench(async () => c.san.rewriteSphinxHtml(mapped, c.sanCtx()), w, r);
  [row.docIndex] = await bench(async () => c.anch.createDocumentIndex(text), w, r);
  const idx = c.anch.createDocumentIndex(text);
  const lns = text.split("\n"); const mk = (shift) => { const ths = []; for (let i = 0; i < 100; i++) { const L = 200 + Math.floor(i * (lns.length - 300) / 100); ths.push({ anchor: { line: L + shift, endLine: L + shift, quote: lns[L - 1].slice(0, 60), prefix: "", suffix: "" } }); } return ths; };
  for (const [k, sh] of [["reanchor100stay", 0], ["reanchor100moved", 40]]) {
    const ths = mk(sh);
    try { [row[k]] = await bench(async () => { for (const t of ths) c.anch.reanchor(idx, t); }, w, r); } catch (e) { row[k] = "err " + e.message.slice(0, 60); }
  }
  if (global.gc) { global.gc(); row.heapMB = Math.round(process.memoryUsage().heapUsed / 1048576); }
  console.log(JSON.stringify(row));
}

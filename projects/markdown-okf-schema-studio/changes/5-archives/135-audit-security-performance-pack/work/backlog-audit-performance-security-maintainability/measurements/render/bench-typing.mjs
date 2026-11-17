import { createRequire } from "node:module";
import { genDoc } from "./gen-doc.mjs";
const req = createRequire(import.meta.url);
const c = req("./common.cjs");
const { updatedRangesForPatch } = req(c.O + "/core/preview/updatedRanges.js");
const { changedLineRanges } = req(c.O + "/core/mapping/lineDiff.js");
let text = genDoc(10000); const lines = text.split("\n");
const mid = lines.findIndex((l, i) => i > lines.length / 2 && l.startsWith("Paragraph"));
let pos = text.split("\n").slice(0, mid).join("\n").length + 10;
for (let i = 0; i < 3; i++) await c.pipeline.renderPreviewDocument(c.opts(text, i));
const rend = [], full = [], patch = [], diff = [];
let prev = text;
for (let i = 0; i < 50; i++) {
  const next = text.slice(0, pos) + "x" + text.slice(pos); pos++; text = next;
  const [d, r] = await c.t(() => c.pipeline.renderPreviewDocument(c.opts(text, 10 + i)));
  rend.push(d);
  const [d2] = await c.t(async () => { const m = c.mapping.annotateSourceMappings(r.html, { documentId: "d", activeSourceFile: c.root + "/doc.md" }); return c.san.rewriteSphinxHtml(m, c.sanCtx()); });
  full.push(d + d2);
  const [d3] = await c.t(async () => updatedRangesForPatch({ sourceText: prev, version: i }, { sourceText: text, version: i + 1 }, 0));
  patch.push(d3);
  const [d4] = await c.t(async () => changedLineRanges(prev, text)); diff.push(d4);
  prev = text;
}
const m = c.median, mx = (a) => Math.max(...a);
console.log(JSON.stringify({ lines: lines.length, renderPreviewDocument_median_ms: m(rend).toFixed(1), max: mx(rend).toFixed(1),
  render_plus_annotate_sanitize_median_ms: m(full).toFixed(1), updatedRangesForPatch_median_ms: m(patch).toFixed(2), changedLineRanges_median_ms: m(diff).toFixed(2) }));

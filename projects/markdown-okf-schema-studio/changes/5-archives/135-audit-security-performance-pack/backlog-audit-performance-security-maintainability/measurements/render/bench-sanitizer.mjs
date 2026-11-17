import { createRequire } from "node:module";
const c = createRequire(import.meta.url)("./common.cjs");
const wrap = (b) => `<html><head></head><body><main>${b}</main></body></html>`;
const pad = "lorem ipsum dolor sit amet ".repeat(4);
const flat = (n) => Array.from({ length: n }, (_, i) => `<p class="c${i % 7}" data-line="${i + 1}"><a href="#a${i}">link ${i}</a> <em>${pad}</em></p>`).join("");
const nest = (d) => "<ul>".repeat(d) + "<li>leaf</li>" + "</ul>".repeat(d);
const cases = {
  "flat 50k elements (~5MB)": wrap(flat(16000) ),
  "nested ul depth 500": wrap(nest(500)),
  "nested ul depth 5000": wrap(nest(5000)),
  "nested div depth 500 x 100 columns": wrap(Array.from({length:100},()=>"<div>".repeat(500)+"x"+"</div>".repeat(500)).join("")),
  "5MB flat + depth500": wrap(flat(16000) + nest(500)),
  "script/unknown tags 50k": wrap(Array.from({length:50000},(_, i)=>`<foo${i%3}>x</foo${i%3}><img src="x${i}.png">`).join("")),
};
for (const [k, html] of Object.entries(cases)) {
  const els = (html.match(/<[a-z]/g) || []).length;
  try {
    const ts = []; let out;
    for (let i = 0; i < 3; i++) { const [d, r] = await c.t(async () => c.san.rewriteSphinxHtml(html, { ...c.sanCtx(), sourceMapping: undefined })); ts.push(d); out = r; }
    const [d2] = await c.t(async () => c.mapping.annotateSourceMappings(html, { documentId: "d", activeSourceFile: "f" }));
    console.log(`${k}: in ${(html.length / 1048576).toFixed(2)} MB, ~${els} tags, rewrite median ${c.median(ts).toFixed(0)} ms, annotate ${d2.toFixed(0)} ms, out ${(out.html.length / 1048576).toFixed(2)} MB, diag ${out.diagnostics.length}`);
  } catch (e) { console.log(`${k}: FAILED ${e.constructor.name}: ${String(e.message).slice(0, 120)}`); }
}

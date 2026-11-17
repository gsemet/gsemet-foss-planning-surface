import { createRequire } from "node:module";
const c = createRequire(import.meta.url)("./common.cjs");
const wrap = (b) => `<html><head></head><body><main>${b}</main></body></html>`;
const mk = { "unknown tags": (i) => `<foo>x</foo>`, "img blocked (resolveResource undefined)": (i) => `<img src="x${i}.png">`, "script": (i) => `<script>1</script>`, "ok <p>": (i) => `<p>x</p>` };
for (const [k, f] of Object.entries(mk)) for (const n of [5000, 10000, 20000]) {
  const html = wrap(Array.from({ length: n }, (_, i) => f(i)).join(""));
  const [d, r] = await c.t(async () => c.san.rewriteSphinxHtml(html, { ...c.sanCtx(), sourceMapping: undefined }));
  console.log(k, n, d.toFixed(0), "ms, diag", r.diagnostics.length);
}

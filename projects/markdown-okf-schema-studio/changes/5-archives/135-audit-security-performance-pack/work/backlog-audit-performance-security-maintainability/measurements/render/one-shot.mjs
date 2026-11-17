import { createRequire } from "node:module";
import { genDoc } from "./gen-doc.mjs";
const c = createRequire(import.meta.url)("./common.cjs");
const n = +process.argv[2]; const reps = +process.argv[3] || 1; const text = genDoc(n);
for (let i = 0; i < reps; i++) { const [d] = await c.t(() => c.pipeline.renderPreviewDocument(c.opts(text))); console.log(n, "renderPreviewDocument", d.toFixed(0), "ms"); }
const [p] = await c.t(() => c.mystEngine.parseMystSource(text)); console.log(n, "parse", p.toFixed(0), "ms");
console.log("heapUsed MB", Math.round(process.memoryUsage().heapUsed / 1048576), "rss MB", Math.round(process.memoryUsage().rss / 1048576));

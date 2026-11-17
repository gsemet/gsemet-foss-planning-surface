import { readFileSync } from "node:fs";
const p = JSON.parse(readFileSync(process.argv[2], "utf8"));
const self = new Map(); const byId = new Map(p.nodes.map((n) => [n.id, n]));
p.samples.forEach((id, i) => { const dt = p.timeDeltas[i] || 0; self.set(id, (self.get(id) || 0) + dt); });
const agg = new Map(); let total = 0;
for (const [id, t] of self) { const cf = byId.get(id).callFrame; const key = `${cf.functionName || "(anon)"} ${cf.url.replace(/.*\/(out\/src|node_modules)\//, "$1/")}:${cf.lineNumber + 1}`; agg.set(key, (agg.get(key) || 0) + t); total += t; }
[...agg].sort((a, b) => b[1] - a[1]).slice(0, +process.argv[3] || 10).forEach(([k, t]) => console.log((t / 1000).toFixed(0).padStart(7), "ms", (100 * t / total).toFixed(1).padStart(5) + "%", k));
console.log("total", (total / 1000).toFixed(0), "ms");

// Compact tables: median busy / script / style per scenario for a list of series prefixes.
// usage: node pivot.cjs <metric,metric> <prefix>...
const fs = require("node:fs"), path = require("node:path");
const [metrics, ...prefixes] = process.argv.slice(2);
const dir = path.join(__dirname, "results");
const runs = fs.readdirSync(dir).filter((f) => prefixes.some((p) => new RegExp(`^${p}[0-9]*[.]json$`).test(f))).flatMap((f) => JSON.parse(fs.readFileSync(path.join(dir, f))).runs);
const med = (a) => { const s = [...a].sort((x, y) => x - y), m = s.length >> 1; return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2; };
const cells = {}, scen = new Set(), vars = new Set();
for (const r of runs) for (const [n, s] of Object.entries(r.scenarios || {})) {
  if (n === "create" || n === "repost") continue;
  scen.add(n); vars.add(r.variant);
  for (const m of metrics.split(",")) { const v = m === "max" ? s.maxTask : s[m] / s.steps; if (Number.isFinite(v)) (cells[`${r.variant}|${n}|${m}`] ||= []).push(v); }
}
console.log(`ms per step, median (max of runs), ${metrics}`);
console.log(["variant", ...scen].join(" | "));
for (const v of vars) console.log([v, ...[...scen].map((n) => metrics.split(",").map((m) => { const a = cells[`${v}|${n}|${m}`]; return a ? `${med(a).toFixed(2)} (${Math.max(...a).toFixed(1)})` : "-"; }).join(" / "))].join(" | "));
const errs = runs.filter((r) => r.errors.length).map((r) => `${r.variant}#${r.rep}: ${r.errors[0].slice(0, 300)}`);
console.log("runs", runs.length, "errors", errs.length, errs.slice(0, 6).join("\n"));

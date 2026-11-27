// Merges results/<prefix>*.json and prints, per scenario and variant, median [min-max] over runs.
// usage: node summarize.cjs <prefix> [<prefix>...]
"use strict";
const fs = require("node:fs");
const path = require("node:path");
const dir = path.join(__dirname, "results");
const prefixes = process.argv.slice(2);
const runs = [];
for (const f of fs.readdirSync(dir)) {
  if (!prefixes.some((p) => new RegExp(`^${p}\\d*\\.json$`).test(f))) continue;
  runs.push(...JSON.parse(fs.readFileSync(path.join(dir, f), "utf8")).runs);
}
const median = (a) => { const s = [...a].sort((x, y) => x - y); const m = s.length >> 1; return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2; };
const fmt = (a, d = 2) => (a.length ? `${median(a).toFixed(d)} [${Math.min(...a).toFixed(d)}-${Math.max(...a).toFixed(d)}]` : "-");
const table = new Map();
const add = (scenario, variant, metric, value) => {
  if (value === undefined || value === null || Number.isNaN(value)) return;
  const s = table.get(scenario) || table.set(scenario, new Map()).get(scenario);
  const v = s.get(variant) || s.set(variant, new Map()).get(variant);
  (v.get(metric) || v.set(metric, []).get(metric)).push(value);
};
const errors = [];
for (const run of runs) {
  if (run.errors.length) errors.push(`${run.variant}#${run.rep}: ${run.errors[0].slice(0, 200)}`);
  for (const [name, s] of Object.entries(run.scenarios || {})) {
    if (name === "create") {
      for (const c of s) {
        add("create", run.variant, "toDom", c.latency?.toDom);
        add("create", run.variant, "toFrame", c.latency?.toFrame);
        add("create", run.variant, "hostTotal", c.host?.total);
        add("create", run.variant, "git", c.host?.steps.gitUserName);
        add("create", run.variant, "read", c.host?.steps.readFile);
        add("create", run.variant, "writeRename", c.host ? c.host.steps.writeFile + c.host.steps.rename : undefined);
        add("create", run.variant, "hostNoGit", c.host ? c.host.total - (c.host.steps.gitUserName || 0) : undefined);
        add("create", run.variant, "pageBusy", c.save.busy);
        for (const g of ["script", "style", "layout", "paint"]) add("create", run.variant, g, c.save[g]);
        add("create", run.variant, "maxTask", c.save.maxTask);
        add("create", run.variant, "openBusy", c.open.busy);
      }
      continue;
    }
    for (const m of ["busy", "script", "style", "layout", "paint", "hittest", "other"]) add(name, run.variant, m, s[m] / s.steps);
    add(name, run.variant, "maxTask", s.maxTask);
    add(name, run.variant, "styleEl", s.styleElements / s.steps);
    add(name, run.variant, "selChg", s.events.selectionchange ? s.events.selectionchange.total / s.events.selectionchange.count : undefined);
    add(name, run.variant, "selLen", s.selection?.length);
    if (s.inputRoundTrip !== undefined) add(name, run.variant, "inputRT", s.inputRoundTrip);
    if (s.split) for (const x of s.split) for (const [k, v] of Object.entries(x)) add(name, run.variant, k, v);
    for (const [k, v] of Object.entries(s.top || {})) add(`top:${name}`, run.variant, k, v / s.steps);
  }
}
const order = (a, b) => a.localeCompare(b);
for (const [scenario, variants] of table) {
  if (scenario.startsWith("top:")) continue;
  const metrics = [...new Set([...variants.values()].flatMap((m) => [...m.keys()]))];
  console.log(`\n## ${scenario}  (ms per step; create: ms per comment)`);
  console.log(`| variant | n | ${metrics.join(" | ")} |`);
  console.log(`|${"---|".repeat(metrics.length + 2)}`);
  for (const variant of [...variants.keys()].sort(order)) {
    const m = variants.get(variant);
    console.log(`| ${variant} | ${Math.max(...[...m.values()].map((a) => a.length))} | ${metrics.map((k) => fmt(m.get(k) || [], k === "selLen" ? 0 : k === "styleEl" ? 1 : 2)).join(" | ")} |`);
  }
}
if (process.env.TOP) {
  for (const [scenario, variants] of table) {
    if (!scenario.startsWith("top:")) continue;
    for (const [variant, m] of variants) {
      if (!process.env.TOP.split(",").includes(variant)) continue;
      console.log(scenario, variant, [...m].map(([k, a]) => [k, median(a)]).sort((x, y) => y[1] - x[1]).slice(0, 7).map(([k, v]) => `${k}=${v.toFixed(2)}`).join(" "));
    }
  }
}
if (errors.length) console.log("\nerrors:\n" + errors.join("\n"));

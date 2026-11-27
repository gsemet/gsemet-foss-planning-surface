// Recompute the figures of the nine perf-547 runs from the artifacts the Verifier downloaded.
const fs = require("fs"), path = require("path");
const F = path.resolve(__dirname, "..", "..");
const dl = path.join(F, "work", "scratch", "verifier-dl");
const sets = {
  head44a2e93: ["45947065460", "45947068376", "45947071021"],
  measure7d24547: ["45928962519", "45928965278", "45928968671"],
  cr516e52cd28: ["45918715713", "45918718450", "45918721402"],
};
const med = (a) => { const s = [...a].sort((x, y) => x - y); const n = s.length; return n % 2 ? s[(n - 1) / 2] : (s[n / 2 - 1] + s[n / 2]) / 2; };
const r2 = (x) => Math.round(x * 1000) / 1000;
const published = { head44a2e93: path.join(F, "evidence", "after"), measure7d24547: path.join(F, "evidence", "measure-ci"),
  cr516e52cd28: path.resolve(F, "..", "516-perf-547-slow-comment-selection", "evidence", "after") };
for (const [set, ids] of Object.entries(sets)) {
  console.log(`\n=== ${set}`);
  const table = {}; const waits = []; const waitMed = [];
  for (const id of ids) {
    const file = path.join(dl, `artifacts-${id}`, "probe", "perf-547.json");
    const rep = JSON.parse(fs.readFileSync(file, "utf8"));
    const copies = fs.readdirSync(published[set]).filter((f) => f.includes(id) && f.endsWith(".json"));
    for (const c of copies) console.log(`published copy ${c} identical to artifact: ${fs.readFileSync(path.join(published[set], c)).equals(fs.readFileSync(file))}`);
    if (!copies.length) console.log(`no published copy for ${id}`);
    console.log(id, "env", JSON.stringify(rep.environment), "doc", JSON.stringify(rep.document), "threads", JSON.stringify(rep.threads), "folder", JSON.stringify(rep.fixtureFolder));
    for (const [name, v] of Object.entries(rep.interactions)) {
      const walk = (prefix, o) => {
        if (o && Array.isArray(o.samples)) {
          if (Math.abs(med(o.samples) - o.median) > 0.0051) console.log("MEDIAN MISMATCH", id, prefix, med(o.samples), o.median);
          (table[prefix] ??= []).push(o.median);
          if (/selectionRelease/.test(prefix)) console.log(`  ${prefix} samples near4=${o.samples.filter((s) => s < 8).length} near17=${o.samples.filter((s) => s >= 8).length} n=${o.samples.length} max=${Math.max(...o.samples)}`);
          if (/ongest|drag|release|Drag|Release/.test(prefix)) (table[prefix + " MAX"] ??= []).push(Math.max(...o.samples));
        } else if (o && typeof o === "object") for (const [k, w] of Object.entries(o)) walk(`${prefix}.${k}`, w);
      };
      walk(name, v);
    }
    const rs = rep.commentCreateRestyledElements; (table.restyled ??= []).push(rs.median ?? JSON.stringify(rs));
    if (rep.authorWait) { console.log(`  authorWait n=${rep.authorWait.samples.length} median(recomputed)=${r2(med(rep.authorWait.samples))} reported=${rep.authorWait.median} samples=${rep.authorWait.samples.join(", ")}`); waits.push(...rep.authorWait.samples); waitMed.push(rep.authorWait.median); }
    else console.log("  no authorWait");
    if (rep.threadIndex) for (const d of rep.threadIndex.documents) console.log(`  threadIndex ${d.name} lines=${d.lines} bytes=${d.bytes} threads=${d.threads} index n=${d.createDocumentIndex.samples.length} med=${d.createDocumentIndex.median} (re ${r2(med(d.createDocumentIndex.samples))}) reanchor n=${d.reanchorThreads.samples.length} med=${d.reanchorThreads.median} (re ${r2(med(d.reanchorThreads.samples))}) node=${rep.threadIndex.node}`);
    else console.log("  no threadIndex");
  }
  for (const [k, v] of Object.entries(table)) console.log(`${k}: ${v.join(" / ")}  median-of-runs=${v.every((x) => typeof x === "number") ? med(v) : "-"}`);
  if (waits.length) console.log(`authorWait: run medians ${waitMed.join(" / ")}; median of runs ${med(waitMed)}; pooled median of ${waits.length} samples ${r2(med(waits))}; samples above 10 ms ${waits.filter((w) => w > 10).length}`);
}

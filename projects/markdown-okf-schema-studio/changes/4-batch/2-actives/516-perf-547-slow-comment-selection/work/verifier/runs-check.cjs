// Recomputes the medians and largest samples of the six perf-547 reports from the artifacts
// downloaded by the Verifier, and compares each artifact with the copy kept in evidence/.
const fs = require("node:fs");
const path = require("node:path");

const cr = path.resolve(__dirname, "..", "..");
const runs = {
  before: ["45895473044", "45895477080", "45896724578"],
  after: ["45918715713", "45918718450", "45918721402"],
};

const median = (values) => {
  const sorted = [...values].sort((a, b) => a - b);
  const half = Math.floor(sorted.length / 2);
  return sorted.length % 2 ? sorted[half] : (sorted[half - 1] + sorted[half]) / 2;
};
const round = (value) => Math.round(value * 1000) / 1000;

const table = {};
for (const [side, ids] of Object.entries(runs)) {
  for (const id of ids) {
    const forge = fs.readFileSync(path.join(cr, "work", "scratch", `artifacts-${id}-verifier`, "probe", "perf-547.json"));
    const kept = fs.readFileSync(path.join(cr, "evidence", side, `perf-547-run-${id}.json`));
    const report = JSON.parse(forge.toString("utf8"));
    const same = JSON.stringify(report) === JSON.stringify(JSON.parse(kept.toString("utf8")));
    console.log(`${side} ${id}: evidence copy equals the forge artifact: ${same ? "yes" : "NO"} (bytes equal: ${forge.equals(kept)})`);
    console.log(`  document ${JSON.stringify(report.document)} threads ${JSON.stringify(report.threads ?? "")}`);
    const rows = { ...report.interactions, restyled: report.commentCreateRestyledElements };
    for (const [name, row] of Object.entries(rows)) {
      const samples = row.samples.map((sample) => (typeof sample === "number" ? sample : NaN));
      const own = median(samples);
      const note = Math.abs(own - row.median) < 1e-9 ? "" : ` MISMATCH reported ${row.median}`;
      console.log(`  ${name}: n=${samples.length} median ${round(own)} min ${round(Math.min(...samples))} max ${round(Math.max(...samples))}${note}`);
      ((table[name] ??= { before: [], after: [] })[side]).push({ median: round(own), max: Math.max(...samples) });
    }
    if (report.commentCreateRestyledElements.largestRecalc !== undefined) {
      console.log(`  largestRecalc ${JSON.stringify(report.commentCreateRestyledElements.largestRecalc)}`);
    }
  }
}
console.log("\nmeasure: before medians | after medians | largest sample before | largest sample after");
for (const [name, row] of Object.entries(table)) {
  console.log(`${name}: ${row.before.map((r) => r.median).join(", ")} | ${row.after.map((r) => r.median).join(", ")} | ${
    round(Math.max(...row.before.map((r) => r.max)))} | ${round(Math.max(...row.after.map((r) => r.max)))}`);
}

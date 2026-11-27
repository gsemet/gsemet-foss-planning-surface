// Verifier probe of CR-517: the default output of the perf-547 document generator is that of the
// base (aeefa1b0), byte for byte, and the scale-4 document has four times its counts.
// Run from the worktree after compile: node <this file> <base perf547Document bundle>
const path = require("node:path");
const crypto = require("node:crypto");
const base = require(path.resolve(process.argv[2]));
const head = require(path.join(process.cwd(), "out/test/probe/perf547Document"));
const digest = (text) => crypto.createHash("sha256").update(text).digest("hex").slice(0, 16);
const before = base.perf547Document();
let equal = true;
for (const [name, call] of [["perf547Document()", () => head.perf547Document()], ["perf547Document(1)", () => head.perf547Document(1)]]) {
  const after = call();
  const same = Object.keys(before).join() === Object.keys(after).join()
    && Object.keys(before).every((key) => Buffer.from(before[key]).equals(Buffer.from(after[key])));
  equal = equal && same;
  console.log(name, "files", Object.keys(after).length, "identical to base (names, order, bytes):", same);
}
for (const key of Object.keys(before).filter((k) => !k.endsWith(".svg"))) console.log(" base", key, Buffer.byteLength(before[key]), digest(before[key]));
console.log(" all files digest, base", digest(JSON.stringify(before)), "head", digest(JSON.stringify(head.perf547Document())));
for (const scale of [1, 4]) {
  const files = head.perf547Document(scale);
  const text = files[head.PERF547_FILE];
  const lines = text.split("\n");
  console.log("scale", scale, "lines", lines.length - 1, "tables", lines.filter((l) => /^\|[-| ]+\|$/.test(l)).length,
    "blockquotes", lines.filter((l) => l.startsWith("> ")).length, "images", Object.keys(files).filter((k) => k.endsWith(".svg")).length,
    "threads", JSON.parse(files["report.comments.json"]).threads.length);
}
process.exit(equal ? 0 : 1);

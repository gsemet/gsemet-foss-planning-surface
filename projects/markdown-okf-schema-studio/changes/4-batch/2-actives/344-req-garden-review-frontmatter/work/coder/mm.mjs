import fs from "node:fs";
import { createRequire } from "node:module";
const root = process.argv[2];
const m = (await import(root + "/node_modules/mermaid/dist/mermaid.core.mjs")).default;
const files = process.argv.slice(3);
let bad = 0;
for (const f of files) {
  const t = fs.readFileSync(f, "utf8");
  const mt = /```mermaid\r?\n([\s\S]*?)```/.exec(t);
  if (!mt) { console.log("no diagram", f); continue; }
  try { await m.parse(mt[1]); console.log("ok", f.split("/").pop()); } catch (e) { bad++; console.log("FAIL", f.split("/").pop(), String(e.message).split("\n").slice(0,3).join(" | ")); }
}
process.exit(bad ? 1 : 0);

// SEC-05 probe: include fan-out (FAN includes per level, DEPTH levels).
// Run from src/markdown-okf-schema-studio after `npm run compile`:
//   node ../../.agents/changes/requests/deep-analysis-review/probes/include-fanout.mjs 4
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";
import { createRequire } from "node:module";
const require = createRequire(import.meta.url);
const out = path.resolve(process.env.OUT ?? "out/src");
const { renderMyst } = require(`${out}/render/mystRenderer.js`);
const depth = Number(process.argv[2] ?? 4);
const fan = 10;
const dir = fs.mkdtempSync(path.join(os.tmpdir(), "okf-probe-include-"));
for (let level = 0; level < depth; level += 1) {
  const body = Array.from({ length: fan }, () => "```{include} l" + (level + 1) + ".md\n```\n").join("\n");
  fs.writeFileSync(path.join(dir, `l${level}.md`), body);
}
fs.writeFileSync(path.join(dir, `l${depth}.md`), "leaf paragraph\n");
let reads = 0;
const sourcePath = path.join(dir, "l0.md");
const context = {
  sourcePath,
  resolveInclude: (request, from) => {
    reads += 1;
    const target = path.resolve(path.dirname(from), request);
    return { path: target, source: fs.readFileSync(target, "utf8") };
  },
};
const started = performance.now();
const result = await renderMyst(fs.readFileSync(sourcePath, "utf8"), context);
console.log(JSON.stringify({
  probe: "include-fanout", depth, fanOut: fan, includeReads: reads,
  htmlKB: Math.round(result.html.length / 1024), ms: Math.round(performance.now() - started),
  diagnostics: result.diagnostics.length,
}));
fs.rmSync(dir, { recursive: true, force: true });

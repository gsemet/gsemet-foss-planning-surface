// PERF-12 probe: Ajv cache growth and retained heap across repeated frontmatter analyses.
// Run from src/markdown-okf-schema-studio after `npm run compile`:
//   node --expose-gc ../../.agents/changes/requests/deep-analysis-review/probes/ajv-cache.cjs
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const out = path.resolve(process.env.OUT ?? "out/src");
const { analyzeFrontmatter } = require(`${out}/frontmatter/okfFrontmatter.js`);
const { sharedSchemaValidator } = require(`${out}/frontmatter/schemaValidator.js`);
const root = fs.mkdtempSync(path.join(os.tmpdir(), "okf-probe-ajv-"));
fs.mkdirSync(path.join(root, "_schema"));
fs.writeFileSync(path.join(root, "_schema", "note.schema.yaml"), [
  "$id: https://example.test/note.schema.yaml",
  "type: object",
  "required: [type, title]",
  "properties:",
  "  type: { type: string, enum: [note] }",
  "  title: { type: string, description: Title }",
  "  tags: { type: array, items: { type: string } }",
  "  status: { type: string, enum: [draft, review, done] }",
  "  related:",
  "    type: array",
  "    items: { type: string, x-okf-link: { resolution: filename-stem, syntax: plain } }",
  "if: { properties: { status: { const: done } } }",
  "then: { required: [tags] }",
].join("\n"));
const filePath = path.join(root, "doc.md");
const sourceText = "---\ntype: note\ntitle: Hello\nstatus: done\ntags: [a]\nrelated: [doc]\n---\n# Body\n";
const run = (n) => {
  for (let i = 0; i < n; i += 1) {
    analyzeFrontmatter({ filePath, sourceText, stopDir: root, inspectLinks: false,
      strictAdditionalProperties: false, workspaceRoots: [root] });
  }
};
run(5);
global.gc?.();
const before = process.memoryUsage().heapUsed;
const started = performance.now();
run(500);
const msPerAnalysis = (performance.now() - started) / 500;
global.gc?.();
const after = process.memoryUsage().heapUsed;
const cache = sharedSchemaValidator._cache;
console.log(JSON.stringify({
  probe: "ajv-cache",
  ajvCacheEntries: cache instanceof Map ? cache.size : "unavailable",
  heapGrowthMBPer500: Number(((after - before) / 1048576).toFixed(1)),
  msPerAnalysis: Number(msPerAnalysis.toFixed(2)),
  gcExposed: typeof global.gc === "function",
}));
fs.rmSync(root, { recursive: true, force: true });

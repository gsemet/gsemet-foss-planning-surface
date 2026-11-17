// PERF-01/PERF-02 probe: per-stage synchronous render cost on a real chapter.
// Stages that no longer exist after a refactor are reported as "missing" instead of failing.
// Run from src/markdown-okf-schema-studio after `npm run compile`:
//   node ../../.agents/changes/requests/deep-analysis-review/probes/render-cost.mjs [chapter.md]
import * as fs from "node:fs";
import * as path from "node:path";
import { createRequire } from "node:module";
const require = createRequire(import.meta.url);
const out = path.resolve(process.env.OUT ?? "out/src");
const load = (relative) => { try { return require(`${out}/${relative}`); } catch { return {}; } };
const { renderMyst } = load("render/mystRenderer.js");
const { annotateSourceMappings } = load("mapping/sourceMapping.js");
const { rewriteSphinxHtml, injectContentSecurityPolicy } = load("security/html-sanitizer.js");
const { createPreviewResourcePolicy } = load("security/resource-policy.js");
const { renderMathHtml } = load("render/mathRenderer.js");
const file = path.resolve(process.argv[2] ?? "../../book/chapters/08-research-plan-implement.md");
const source = fs.readFileSync(file, "utf8");
const totals = {};
const time = async (name, fn) => {
  if (typeof fn !== "function") { totals[name] = "missing"; return undefined; }
  const started = performance.now();
  const value = await fn();
  if (totals[name] !== "missing") totals[name] = (totals[name] ?? 0) + performance.now() - started;
  return value;
};
await renderMyst?.(source);
const runs = 10;
for (let index = 0; index < runs; index += 1) {
  const rendered = await time("renderMyst", renderMyst
    && (() => renderMyst(source, { sourcePath: file, resolveInclude: () => undefined })));
  let html = rendered?.html ?? "";
  html = (await time("annotateSourceMappings", annotateSourceMappings
    && (() => annotateSourceMappings(html, { documentId: "file://probe", activeSourceFile: file })))) ?? html;
  const policy = createPreviewResourcePolicy?.(path.dirname(file), process.cwd());
  const rewritten = await time("rewriteSphinxHtml", rewriteSphinxHtml && policy && (() => rewriteSphinxHtml(html, {
    outputRoot: path.dirname(file), policy, nonce: "n", resolveResource: () => undefined,
    resolveNavigation: () => ({ kind: "deferred" }), sourceMapping: { sourceFile: file, documentId: "file://probe" },
  })));
  html = rewritten?.html ?? html;
  html = (await time("renderMathHtml", renderMathHtml && (() => renderMathHtml(html, "k.css", "n")))) ?? html;
  await time("injectContentSecurityPolicy", injectContentSecurityPolicy
    && (() => injectContentSecurityPolicy(html, "default-src 'none'")));
}
const msPerRender = Object.fromEntries(Object.entries(totals)
  .map(([name, value]) => [name, value === "missing" ? value : Number((value / runs).toFixed(1))]));
console.log(JSON.stringify({ probe: "render-cost", sourceKB: Math.round(source.length / 1024), msPerRender }));

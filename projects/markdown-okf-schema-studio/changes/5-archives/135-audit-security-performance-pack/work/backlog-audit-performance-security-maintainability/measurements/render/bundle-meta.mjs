import { build } from "/Users/az02065/Projects/DevTools/markdown-okf-schema-studio/node_modules/esbuild/lib/main.js";
import { createRequire } from "node:module";
import { writeFileSync, mkdirSync } from "node:fs";
const R = "/Users/az02065/Projects/DevTools/markdown-okf-schema-studio";
const S = new URL(".", import.meta.url).pathname;
const req = createRequire(import.meta.url);
const { pageBundleOptions } = await import(R + "/scripts/page-bundle.mjs");
const langs = req(S + "out/src/core/preview/pageBuildEntry.js").highlightLanguages();
const pkgOf = (p) => { const m = p.match(/node_modules\/((?:@[^/]+\/)?[^/]+)/g); return m ? m.at(-1).replace("node_modules/", "") : "(own src)"; };
async function run(name, opts) {
  const r = await build({ absWorkingDir: R, write: false, metafile: true, logLevel: "error", ...opts, outfile: S + `bundle-out/${name}.js`, sourcemap: false });
  const out = Object.values(r.metafile.outputs)[0];
  const agg = {}; for (const [p, i] of Object.entries(out.inputs)) agg[pkgOf(p)] = (agg[pkgOf(p)] || 0) + i.bytesInOutput;
  console.log(`\n## ${name}: output ${(out.bytes / 1024).toFixed(0)} KB (minified)`);
  Object.entries(agg).sort((a, b) => b[1] - a[1]).slice(0, 15).forEach(([k, v]) => console.log(`${(v / 1024).toFixed(1).padStart(8)} KB  ${k}`));
  if (name === "extension") { mkdirSync(S + "out-ext", { recursive: true }); writeFileSync(S + "out-ext/extension.js", r.outputFiles[0].text); }
}
await run("extension", { entryPoints: ["src/extension.ts"], bundle: true, platform: "node", target: "node20", format: "cjs", minify: true, external: ["vscode"] });
await run("preview-page", { ...pageBundleOptions({ highlightLanguages: langs, minify: true }) });
await run("mermaidPreview", { entryPoints: ["src/page/modules/mermaidPreview.ts"], bundle: true, platform: "browser", target: "es2020", format: "iife", minify: true });
await run("plantumlPreview", { entryPoints: ["src/page/modules/plantumlPreview.ts"], bundle: true, platform: "browser", target: "es2020", format: "iife", minify: true });

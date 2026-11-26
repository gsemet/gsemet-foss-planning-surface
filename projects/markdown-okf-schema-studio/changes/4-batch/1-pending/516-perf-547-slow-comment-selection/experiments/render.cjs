// Builds the preview page of each generated document with the product's own render pipeline
// (renderPreviewSource + buildPreviewWebviewHtml) from the compiled worktree, plus scratch asset variants.
// usage: node --import file:///<worktree>/scripts/register-myst-patches.mjs render.cjs <worktree> <tag>
"use strict";
const fs = require("node:fs");
const path = require("node:path");
const { pathToFileURL } = require("node:url");

const here = __dirname;
const worktree = path.resolve(process.argv[2]);
const tag = process.argv[3] || "main";
const lib = (p) => require(path.join(worktree, "out", "src", p));

const { renderPreviewSource } = lib("core/render/renderPipeline");
const { buildPreviewWebviewHtml } = lib("session/webview");
const { createNodeFileSystem } = lib("node-services/nodeFileSystem");
const { nodeSchemaFiles } = lib("node-services/schemaFiles");
const { analyzeFrontmatter } = lib("core/frontmatter/okfFrontmatter");
const config = lib("core/configuration/previewConfiguration");
const { DEFAULT_VIEW_PREFERENCES } = lib("core/state/previewViewPreferences");

const outRoot = path.join(here, "pages", tag);
const assetsRoot = path.join(outRoot, "assets");

/** Removes the style rules whose selector matches `drop`, keeping the rest of the text as it is. */
function stripRules(css, drop) {
  let removed = 0;
  const walk = (text) => {
    let out = "", start = 0, i = 0;
    const skip = (j) => {
      if (text.startsWith("/*", j)) { const e = text.indexOf("*/", j + 2); return e < 0 ? text.length : e + 2; }
      if (text[j] === '"' || text[j] === "'") {
        let k = j + 1; while (k < text.length && text[k] !== text[j]) k += text[k] === "\\" ? 2 : 1; return k + 1;
      }
      return j;
    };
    while (i < text.length) {
      const s = skip(i);
      if (s !== i) { i = s; continue; }
      if (text[i] === ";") { out += text.slice(start, i + 1); start = ++i; continue; }
      if (text[i] !== "{") { i += 1; continue; }
      let depth = 1, j = i + 1;
      while (j < text.length && depth > 0) {
        const t = skip(j);
        if (t !== j) { j = t; continue; }
        if (text[j] === "{") depth += 1; else if (text[j] === "}") depth -= 1;
        j += 1;
      }
      const prelude = text.slice(start, i);
      const selector = prelude.replace(/\/\*[\s\S]*?\*\//g, "").trim();
      if (selector.startsWith("@")) out += prelude + "{" + walk(text.slice(i + 1, j - 1)) + "}";
      else if (drop(selector)) removed += 1;
      else out += text.slice(start, j);
      start = i = j;
    }
    return out + text.slice(start);
  };
  const result = walk(css);
  return { css: result, removed };
}

function writeAssets() {
  const bundle = path.join(worktree, "out", "bundle");
  const css = fs.readFileSync(path.join(bundle, "preview.css"), "utf8");
  const js = fs.readFileSync(path.join(bundle, "preview.js"), "utf8");
  const variants = {
    orig: { css, js },
    nohas: stripRules(css, (s) => s.includes(":has(")),
    nohas3: stripRules(css, (s) => /#sphinx-myst-preview-content(:not\()?:has\(/.test(s)),
  };
  // One root rule family at a time, to see which of the three costs.
  variants.noclearright = stripRules(css, (s) => /#sphinx-myst-preview-content:not\(:has\(/.test(s));
  variants.noheadclear = stripRules(css, (s) => /#sphinx-myst-preview-content:has\(/.test(s));
  // Instrumented page script: time setThreads and scroll.measure() of the previewComments handler.
  const pattern = /\.on\("previewComments",(\w+)=>\{(\w+\.commentThreads)\.setThreads\(\1\.threads\),(\w+)\.scroll\.measure\(\)\}\)/;
  if (!pattern.test(js)) throw new Error("previewComments handler not found in preview.js");
  const instrumented = js.replace(pattern, (_, message, threads, rt) =>
    `.on("previewComments",${message}=>{const a=performance.now();${threads}.setThreads(${message}.threads);const b=performance.now();document.body.offsetHeight;const c=performance.now();${rt}.scroll.measure();const d=performance.now();(window.__comments||(window.__comments=[])).push({setThreads:b-a,flushLayout:c-b,measure:d-c})})`);
  variants.instr = { css, js: instrumented };
  const info = {};
  for (const [name, value] of Object.entries(variants)) {
    const dir = path.join(assetsRoot, name);
    fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(path.join(dir, "preview.css"), value.css);
    fs.writeFileSync(path.join(dir, "preview.js"), value.js ?? js);
    info[name] = { hasCount: (value.css.match(/:has\(/g) || []).length, removedRules: value.removed ?? 0, cssBytes: value.css.length };
  }
  return info;
}

async function renderDocument(doc, assetName) {
  const documentDirectory = path.join(here, "bundle", doc);
  const documentPath = path.join(documentDirectory, "report.md");
  const text = fs.readFileSync(documentPath, "utf8");
  const files = createNodeFileSystem();
  const started = performance.now();
  const rendered = await renderPreviewSource({ text, documentPath, workspaceRoot: documentDirectory, restrictedReads: false }, files);
  const renderMs = performance.now() - started;
  const assetDir = path.join(assetsRoot, assetName);
  const assets = {
    cspSource: "file:",
    resourceUri: (file) => pathToFileURL(file).toString(),
    bundleUri: (...parts) => {
      const file = path.join(assetDir, ...parts);
      return fs.existsSync(file) ? pathToFileURL(file).toString() : undefined;
    },
  };
  const documentId = pathToFileURL(documentPath).toString();
  const context = {
    documentId, revision: 1, requestId: 1, activeSourceFile: documentPath,
    ...config.previewBootSettings(config.DEFAULT_PREVIEW_CONFIGURATION),
    themeKind: 1, initialViewPreferences: DEFAULT_VIEW_PREFERENCES,
    pairedTextEditor: true, initialPaletteMode: "gfm", commentsEnabled: true,
  };
  const result = analyzeFrontmatter({ schemaFiles: nodeSchemaFiles, filePath: documentPath, sourceText: text, stopDir: documentDirectory, inspectLinks: false, workspaceRoots: [documentDirectory] });
  const built = await buildPreviewWebviewHtml(files, rendered.html, documentDirectory, assets, context, documentDirectory,
    { result, tableEnabled: true }, config.DEFAULT_PREVIEW_CONFIGURATION.maxContentWidth);
  const file = path.join(outRoot, `${doc}.${assetName}.html`);
  fs.writeFileSync(file, built.html);
  return { doc, assetName, file, documentId, documentPath, renderMs, htmlBytes: built.html.length, diagnostics: built.diagnostics.length, renderDiagnostics: rendered.diagnostics.map((d) => d.message) };
}

(async () => {
  const info = { tag, worktree, assets: writeAssets(), pages: [] };
  const docs = ["full", "nothreads", "nosvg", "notables", "flat", "small", "xl4", "inlinesvg"];
  for (const doc of docs) info.pages.push(await renderDocument(doc, "orig"));
  for (const asset of ["nohas", "nohas3", "instr"]) {
    for (const doc of ["full", "xl4", "small"]) info.pages.push(await renderDocument(doc, asset));
  }
  for (const asset of ["noclearright", "noheadclear"]) info.pages.push(await renderDocument("full", asset));
  fs.writeFileSync(path.join(outRoot, "pages.json"), JSON.stringify(info, null, 2));
  console.log(JSON.stringify(info.assets));
  for (const p of info.pages) console.log(p.doc, p.assetName, p.renderMs.toFixed(0), p.htmlBytes, p.diagnostics, p.renderDiagnostics.slice(0, 2).join(" | "));
})().catch((error) => { console.error(error); process.exit(1); });

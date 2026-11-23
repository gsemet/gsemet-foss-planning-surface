const fs = require("fs"), path = require("path"), os = require("os");
const [,, out, fixtures] = process.argv;
(async () => {
  const rp = require(path.join(out, "src/core/render/renderPipeline.js"));
  const conf = require(path.join(out, "src/core/myst/confLocator.js"));
  let nfs; if (process.argv[5] === "head") try { nfs = require(path.join(out, "src/node-services/nodeFileSystem.js")).createNodeFileSystem(); } catch {}
  const root = fixtures;
  const doc = path.join(root, "docs", "index.md");
  const text = fs.readFileSync(doc, "utf8");
  const ext = nfs ? await conf.enabledMystExtensionsFor(nfs, doc, root) : conf.enabledMystExtensionsFor(doc, root);
  const outputs = {};
  const times = [];
  for (let i = 0; i < 15; i++) {
    const r = await rp.renderPreviewSource({ text, documentPath: doc, workspaceRoot: root, restrictedReads: false, enabledMystExtensions: ext ? [...ext].sort() : undefined }, nfs);
    times.push(r.renderMs);
    if (i === 0) outputs.first = r;
  }
  const norm = (s) => s.split(root.split(String.fromCharCode(92)).join("/")).join("<ROOT>").split(root).join("<ROOT>");
  const r = outputs.first;
  fs.writeFileSync(path.join(process.argv[4], "render.html"), norm(r.html));
  fs.writeFileSync(path.join(process.argv[4], "meta.json"), norm(JSON.stringify({ ext: ext ? [...ext].sort() : null, diagnostics: r.diagnostics, dependencies: r.dependencies.slice().sort() }, null, 1)));
  times.sort((a, b) => a - b);
  console.log("median renderMs", times[7].toFixed(2), "min", times[0].toFixed(2), "max", times[14].toFixed(2));
})();

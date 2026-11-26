// usage: node transpile.cjs <esbuild module dir> <project root> : transpile test/**/*.ts and src/**/*.ts to <root>/out as CommonJS
const fs = require("node:fs");
const path = require("node:path");
const [tsDir, root] = process.argv.slice(2);
const esbuild = require(tsDir);
let n = 0;
const walk = (d) => {
  for (const e of fs.readdirSync(path.join(root, d), { withFileTypes: true })) {
    const rel = path.join(d, e.name);
    if (e.isDirectory()) walk(rel);
    else if (rel.endsWith(".ts") && !rel.endsWith(".d.ts")) {
      const out = esbuild.transformSync(fs.readFileSync(path.join(root, rel), "utf8"), { loader: "ts", format: "cjs", target: "es2022" });
      const target = path.join(root, "out", rel.replace(/\.ts$/, ".js"));
      fs.mkdirSync(path.dirname(target), { recursive: true });
      fs.writeFileSync(target, out.code);
      n += 1;
    }
  }
};
walk("test");
walk("src");
console.log("transpiled", n);

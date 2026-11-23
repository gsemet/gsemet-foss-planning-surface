const fs = require("fs"), path = require("path");
const r = process.argv[2];
const w = (p, c) => { fs.mkdirSync(path.dirname(path.join(r, p)), { recursive: true }); fs.writeFileSync(path.join(r, p), c); };
w("conf.py", 'extensions = ["myst_parser"]\nmyst_enable_extensions = ["colon_fence", "deflist", "dollarmath"]\n');
w("docs/index.md", "# Index\n\n```{toctree}\n:glob:\nchapters/*\n```\n\n```{include} part.md\n```\n\n![pic](img/ok.png)\n\n![escape](../../outside/secret.png)\n\n![missing](img/none.png)\n\n```{include} ../../outside/secret.md\n```\n\n:::{note}\nhi\n:::\n\nterm\n: definition\n");
w("docs/part.md", "Included **part**.\n");
w("docs/chapters/a.md", "# A\n"); w("docs/chapters/b.md", "# B\n"); w("docs/chapters/sub/c.md", "# C\n");
w("docs/img/ok.png", "x");
fs.mkdirSync(path.join(r, "../outside"), { recursive: true });
fs.writeFileSync(path.join(r, "../outside/secret.png"), "s"); fs.writeFileSync(path.join(r, "../outside/secret.md"), "SECRET");
try { fs.symlinkSync(path.join(r, "../outside"), path.join(r, "docs/link-out"), "junction"); } catch (e) { console.log("no link", e.code); }

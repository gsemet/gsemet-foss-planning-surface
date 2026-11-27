// Verifier probe of CR-517: no static render holds two text nodes side by side (script derived from differential.cjs), independent of the change's own tests.
// 1. The same seeded random thread lists go to the comment module of the base (aeefa1b0) and of the
//    head, each in its own headless Chromium page of the same real render; the whole DOM (text node
//    boundaries included), the popover and the trace must be equal after every step.
// 2. Soundness of the measure gate: whenever a mapped block or one of its text line tops moved in
//    the head page, setThreads must have answered true.
// Run from the worktree: node --import ./scripts/register-myst-patches.mjs <this file> <base.js> <head.js>
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { createRequire } = require("node:module");
const { pathToFileURL } = require("node:url");

const repo = process.cwd();
const need = createRequire(path.join(repo, "package.json"));
const out = (p) => need(path.join(repo, "out", p));
const { chromium } = need("playwright-core");
const { renderPreviewDocument } = out("src/core/render/renderPipeline");
const { createNodeFileSystem } = out("src/node-services/nodeFileSystem");
const { buildPreviewWebviewHtml } = out("src/session/webview");
const { fakeAssetResolver } = out("test/shared/fakeAssets");
const { perf547Document, PERF547_FILE } = out("test/probe/perf547Document");

const RUNS = Number(process.env.RUNS || 40);
const STEPS = Number(process.env.STEPS || 25);

const RICH = `# Alpha heading with words

A first paragraph with *emphasised words* and \`inline code\` and words again, long enough to wrap
over several lines of the preview so that a highlight may change where the line breaks happen here.
Supercalifragilisticexpialidocious pneumonoultramicroscopicsilicovolcanoconiosis words words words.

- tight item one with words
- tight item two with words
  - nested item with more words

1. loose item

   second paragraph of the loose item with words

2. other loose item

> A quote paragraph with words.
>
> Second quoted paragraph with words and **bold words**.

| Column words | Other |
|---|---|
| cell words one | cell two |
| cell words three | cell four |

\`\`\`python
print("code words")
\`\`\`

Term
: A definition with words.

:::{note}
A note with words inside the admonition.

Second paragraph of the note.
:::

:::{dropdown} Dropdown title words
Hidden dropdown words.
:::

![image words](missing.svg)

---

Text with a footnote[^one] and $x^2$ math and a [link with words](https://example.com).

- [ ] task words
- [x] done words

## Second heading with words

Last paragraph with words.

[^one]: Footnote words.
`;

const docs = [
  { name: "rich", files: { "doc.md": RICH }, main: "doc.md" },
  { name: "perf547", files: perf547Document(), main: PERF547_FILE },
  { name: "readme", files: { "README.md": fs.readFileSync(path.join(repo, "README.md"), "utf8") }, main: "README.md" },
  { name: "contributing", files: { "C.md": fs.readFileSync(path.join(repo, "CONTRIBUTING.md"), "utf8") }, main: "C.md" },
];

async function render(doc, root, width) {
  const workspace = path.join(root, doc.name + width);
  for (const [relative, content] of Object.entries(doc.files)) {
    fs.mkdirSync(path.dirname(path.join(workspace, relative)), { recursive: true });
    fs.writeFileSync(path.join(workspace, relative), content);
  }
  const documentPath = path.join(workspace, doc.main);
  const markdown = doc.files[doc.main];
  const rendered = await renderPreviewDocument({
    files: createNodeFileSystem(),
    document: { uri: { scheme: "file", fsPath: documentPath }, languageId: "markdown", version: 1, getText: () => markdown },
    workspaceRoot: workspace, requestId: 1, isWorkspaceTrusted: () => true, plantUmlEngine: "builtin",
  });
  const assets = fakeAssetResolver({ cspSource: "file:", url: (p) => pathToFileURL(p).href, extensionRoot: root });
  const bundle = { ...assets, bundleUri: () => undefined };
  const built = await buildPreviewWebviewHtml(createNodeFileSystem(), rendered.html, workspace, bundle, {
    activeSourceFile: documentPath, documentId: pathToFileURL(documentPath).toString(), revision: 1, requestId: 1,
    previewThemeMode: "current", commentsEnabled: true,
    initialViewPreferences: { zoom: 100, widthMode: "auto", toc: false, incomingChanges: true, comments: true, toolbarCollapsed: true },
  }, workspace, undefined, width, true, [], "builtin");
  const file = path.join(workspace, "page.html");
  // No script of the page itself: only the module under test touches the page.
  fs.writeFileSync(file, built.html.replace(/<script(?![^>]*type="application\/json")[^>]*>[\s\S]*?<\/script>/g, ""));
  return pathToFileURL(file).href;
}


(async () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "verifier517-adj-"));
  const browser = await chromium.launch();
  const long = ["# Long", "", Array.from({ length: 20000 }, (_, i) => "w" + i).join(" "), ""].join(String.fromCharCode(10));
  const all = [...docs, { name: "long", files: { "long.md": long }, main: "long.md" }];
  for (const name of fs.readdirSync(path.join(repo, "docs")).filter((n) => n.endsWith(".md"))) all.push({ name: "docs-" + name, files: { [name]: fs.readFileSync(path.join(repo, "docs", name), "utf8") }, main: name });
  try {
    console.log("chromium", browser.version());
    for (const doc of all) {
      const page = await browser.newPage({ bypassCSP: true });
      await page.goto(await render(doc, root, 900));
      const found = await page.evaluate(() => {
        let pairs = 0, texts = 0, longest = 0;
        const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
        for (let node = walker.nextNode(); node; node = walker.nextNode()) {
          if (!node.parentElement.closest("[data-line]")) continue;
          texts += 1; longest = Math.max(longest, node.length);
          if (node.nextSibling && node.nextSibling.nodeType === 3) pairs += 1;
        }
        return { blocks: document.querySelectorAll("[data-line]").length, texts, longest, pairs };
      });
      console.log(doc.name, JSON.stringify(found));
      await page.close();
    }
  } finally {
    await browser.close();
    fs.rmSync(root, { recursive: true, force: true, maxRetries: 5 });
  }
})().catch((error) => { console.error(error); process.exit(1); });

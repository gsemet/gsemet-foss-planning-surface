// Verifier probe: renders a made-up document with the checkout given as argv[2] (render pipeline,
// shipped stylesheet, page runtime built from its src/) and screenshots / measures it in Chromium.
// Usage (cwd = the checkout): node --import ./scripts/register-myst-patches.mjs probe.js <root> <label> <shotDir>
"use strict";
const fs = require("node:fs");
const path = require("node:path");
const { pathToFileURL } = require("node:url");

const [root, label, shotDir] = process.argv.slice(2);
const req = (p) => require(path.join(root, p));
const { chromium } = req("node_modules/playwright-core");
const { renderPreviewDocument } = req("out/src/core/render/renderPipeline");
const { createNodeFileSystem } = req("out/src/node-services/nodeFileSystem");
const { buildPreviewWebviewHtml } = req("out/src/session/webview");
const { fakeAssetResolver } = req("out/test/shared/fakeAssets");
const { pinTestFonts } = req("out/test/page/pinnedFont");
const { pageRuntimeScript } = req("out/test/page/runtimeHarness");
const { THEMES } = req("out/test/visual/themes");

const work = path.join(__dirname, `p-${label}`);

async function build(name, markdown, column, themeMode) {
  const dir = path.join(work, name);
  const workspace = path.join(dir, "ws");
  fs.mkdirSync(workspace, { recursive: true });
  const documentPath = path.join(workspace, "code.md");
  fs.writeFileSync(documentPath, markdown);
  fs.mkdirSync(path.join(dir, "out", "bundle"), { recursive: true });
  fs.writeFileSync(path.join(dir, "out", "bundle", "preview.js"), pageRuntimeScript());
  const rendered = await renderPreviewDocument({
    files: createNodeFileSystem(),
    document: { uri: { scheme: "file", fsPath: documentPath }, languageId: "markdown", version: 1, getText: () => markdown },
    workspaceRoot: workspace, requestId: 1, isWorkspaceTrusted: () => true, plantUmlEngine: "builtin",
  });
  const assets = fakeAssetResolver({ cspSource: "file:", url: (f) => pathToFileURL(f).href, extensionRoot: dir });
  const bundle = { ...assets, bundleUri: (...s) => (s[0] === "preview.js" ? assets.bundleUri(...s) : undefined) };
  const context = {
    activeSourceFile: documentPath, documentId: pathToFileURL(documentPath).toString(), revision: 1, requestId: 1,
    previewThemeMode: themeMode,
    initialViewPreferences: { zoom: 100, widthMode: "margin", toc: false, incomingChanges: true, comments: true, toolbarCollapsed: true },
    "codeBlocks.darkBackground": true, "codeBlocks.lineNumbers": true,
  };
  const built = await buildPreviewWebviewHtml(createNodeFileSystem(), rendered.html, workspace, bundle, context, workspace,
    undefined, column + 78 * 2, true, [], "builtin");
  const pagePath = path.join(dir, "page.html");
  fs.writeFileSync(pagePath, built.html);
  return pagePath;
}

async function open(browser, pagePath, height) {
  const page = await browser.newPage({ viewport: { width: 1100, height }, deviceScaleFactor: 1 });
  await page.addInitScript(() => {
    window.acquireVsCodeApi = () => ({ getState: () => ({}), setState: () => undefined, postMessage: () => undefined });
  });
  await page.goto(pathToFileURL(pagePath).href);
  await page.waitForFunction(() => document.documentElement.getAttribute("data-sphinx-preview-width") === "margin");
  return page;
}

async function settle(page) {
  await page.evaluate(async () => {
    await document.fonts.ready;
    window.dispatchEvent(new Event("resize"));
    await new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)));
  });
}

async function toAuto(page) {
  await page.evaluate(() => document.querySelector("[data-sphinx-preview-width-toggle]").click());
  await page.waitForFunction(() => document.documentElement.getAttribute("data-sphinx-preview-width") === "auto");
  await settle(page);
}

function read(page) {
  return page.evaluate(() => {
    const content = document.getElementById("sphinx-myst-preview-content");
    const style = getComputedStyle(content);
    const column = content.clientWidth - parseFloat(style.paddingLeft) - parseFloat(style.paddingRight);
    return {
      column,
      theme: document.documentElement.getAttribute("data-sphinx-preview-theme-mode"),
      mode: document.documentElement.getAttribute("data-sphinx-preview-width"),
      blocks: [...content.querySelectorAll("pre")].map((pre) => {
        let wrapper = pre;
        while (wrapper.parentElement !== content) wrapper = wrapper.parentElement;
        const tag = /(?:ID)-([a-z]+)/u.exec(pre.textContent);
        const box = wrapper.getBoundingClientRect();
        const caption = wrapper.querySelector(":scope > figcaption");
        return `${tag ? tag[1] : "?"}: wrapper ${wrapper.tagName.toLowerCase()}${pre === wrapper ? "" : " (pre nested)"} width ${box.width.toFixed(1)} `
          + `left ${box.left.toFixed(1)} centre ${(box.left + box.width / 2).toFixed(1)} `
          + `${wrapper.hasAttribute("data-sphinx-preview-wide") ? "WIDE " + wrapper.style.getPropertyValue("--sphinx-preview-breakout") : "not wide"} `
          + `pre ${pre.clientWidth}/${pre.scrollWidth}${caption ? ` caption ${caption.getBoundingClientRect().width.toFixed(1)}` : ""}`;
      }),
    };
  });
}

const long = (id, n) => `${`ID-${id} ${"abcdefghi ".repeat(40)}`.slice(0, n - 1)}x`;

const SHOT_LINE = "def resolve_source(workspace: Path, name: str, *, strict: bool = False) -> Path | None:";
const shotDocument = [
  "# Code blocks in Auto width", "",
  "A numbered fence whose longest line is a little wider than the text column:", "",
  "```python", `${SHOT_LINE}  # ID-fence`, "    return workspace / name", "```", "",
  "The same block with a caption:", "",
  "```{code-block} python", ":caption: resolve_source.py", "", `${SHOT_LINE}  # ID-captn`, "    return workspace / name", "```", "",
  "The text column keeps its width.", "",
].join("\n");

const containers = [
  "# Containers", "",
  "````{note}", "```text", long("admonition", 100), "```", "````", "",
  "> ```text", `> ${long("quote", 100)}`, "> ```", "",
  "`````{tab-set}", "````{tab-item} One", "```text", long("tab", 100), "```", "````", "`````", "",
  "````{card} A card", "```text", long("card", 100), "```", "````", "",
  "1. Item", "", "   ```text", `   ${long("list", 100)}`, "   ```", "",
].join("\n");

const overflow = ["# Overflow", "", "```text", long("plain", 100), "```", ""].join("\n");

async function main() {
  fs.mkdirSync(shotDir, { recursive: true });
  const browser = await chromium.launch({ ignoreDefaultArgs: ["--hide-scrollbars"] });
  try {
    // Screenshots: cream theme, 1100 px pane, 688 px column, the machine's own fonts.
    const light = THEMES.find((t) => t.id === "light");
    const shotPage = await open(browser, await build("shot", shotDocument, 688, "cream"), 560);
    await shotPage.evaluate((vars) => {
      for (const [k, v] of Object.entries(vars)) document.documentElement.style.setProperty(k, v);
    }, light.variables);
    await settle(shotPage);
    await shotPage.waitForTimeout(1500);
    console.log(`[${label}] shot margin`, JSON.stringify(await read(shotPage), null, 1));
    await shotPage.screenshot({ path: path.join(shotDir, `${label}-margin-cream-1100.png`) });
    await toAuto(shotPage);
    await shotPage.mouse.move(1, 540);
    await shotPage.waitForTimeout(1500);
    console.log(`[${label}] shot auto`, JSON.stringify(await read(shotPage), null, 1));
    await shotPage.screenshot({ path: path.join(shotDir, `${label}-auto-cream-1100.png`) });
    await shotPage.close();
    // Containers, pinned font.
    const nested = await open(browser, await build("containers", containers, 688, "current"), 1400);
    await pinTestFonts(nested);
    await settle(nested);
    console.log(`[${label}] containers margin`, JSON.stringify(await read(nested), null, 1));
    await toAuto(nested);
    console.log(`[${label}] containers auto`, JSON.stringify(await read(nested), null, 1));
    await nested.close();
    // Overflow of 4, 3, 2, 1 and 0 px: the same line, the column one pixel wider each time.
    for (const column of [687, 688, 689, 690, 691]) {
      const page = await open(browser, await build(`c${column}`, overflow, column, "current"), 600);
      await pinTestFonts(page);
      await settle(page);
      const margin = await read(page);
      await toAuto(page);
      const auto = await read(page);
      console.log(`[${label}] column ${margin.column} margin: ${margin.blocks[0]}`);
      console.log(`[${label}] column ${auto.column} auto:   ${auto.blocks[0]}`);
      await page.close();
    }
  } finally {
    await browser.close();
    fs.rmSync(work, { recursive: true, force: true });
  }
}

main().catch((error) => { console.error(error); process.exit(1); });

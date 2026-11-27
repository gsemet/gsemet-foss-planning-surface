// Verifier probe of CR-516: renders the same Markdown documents with the base build
// (out/vbase/out, the src of origin/main) and with the head build (out/), loads both in Chromium
// and compares the computed layout of every element of the content (clear, float, position, size),
// the toolbar float (::before of the content root) and the height of the document.
// Surfaces: preview page with no page script, exported file, preview page with the page runtime,
// content patches that switch between documents, and changes of the page itself.
// Run from the worktree: node --import ./scripts/register-myst-patches.mjs <this file> <scratch dir>
const fs = require("node:fs");
const path = require("node:path");
const { createRequire } = require("node:module");
const { pathToFileURL } = require("node:url");

const worktree = process.cwd();
const scratch = path.resolve(process.argv[2]);
const { chromium } = createRequire(path.join(worktree, "package.json"))("playwright-core");

const BUILDS = { old: path.join(worktree, "out", "vbase", "out"), new: path.join(worktree, "out") };

const SVG = '<svg xmlns="http://www.w3.org/2000/svg" width="200" height="140"><rect width="200" height="140" fill="#369"/></svg>';
const DATA = `data:image/svg+xml;base64,${Buffer.from(SVG).toString("base64")}`;

const TEXT = "Running text that is long enough to wrap around a floated box more than once. ".repeat(6);
const tail = `\n\n${TEXT}\n\n## Next section\n\nShort.\n\n\`\`\`python\nx = 1\n\`\`\`\n\n| a | b |\n| - | - |\n| 1 | 2 |\n\n\`\`\`{note}\nA note.\n\`\`\`\n\n- one\n- two\n\n### Last\n\nMore text.\n`;
const doc = (extra) => `# Title\n\n${extra}${tail}`;
const image = (align) => `\`\`\`{image} pic.svg\n:width: 160px\n:align: ${align}\n\`\`\`\n\n`;
const figure = (align) => `\`\`\`{figure} pic.svg\n:width: 180px\n:align: ${align}\n\nThe caption.\n\`\`\`\n\n`;
const table = (align) => `\`\`\`{table} The title\n:align: ${align}\n\n| k | v |\n| - | - |\n| 1 | 2 |\n\`\`\`\n\n`;
const listTable = (align) => `\`\`\`{list-table}\n:align: ${align}\n\n* - k\n  - v\n* - 1\n  - 2\n\`\`\`\n\n`;

const DOCS = {
  plain: doc(""),
  plainImage: doc("![a picture](pic.svg)\n\n"),
  imageRight: doc(image("right")),
  imageLeft: doc(image("left")),
  imageCenter: doc(image("center")),
  figureRight: doc(figure("right")),
  figureLeft: doc(figure("left")),
  figureCenter: doc(figure("center")),
  tableRight: doc(table("right")),
  tableLeft: doc(table("left")),
  tableCenter: doc(table("center")),
  listTableRight: doc(listTable("right")),
  htmlTableRight: doc('<table align="right"><tr><td>aside</td></tr></table>\n\n'),
  htmlImgLeft: doc('<img src="pic.svg" width="100" align="left">\n\n'),
  htmlImgUpper: doc('<img src="pic.svg" width="100" align="RIGHT">\n\n'),
  htmlImgMiddle: doc('<img src="pic.svg" width="100" align="middle">\n\n'),
  htmlFigureClass: doc('<figure class="align-right"><img src="pic.svg" width="100"></figure>\n\n'),
  htmlParagraphAlign: doc('<p align="right">A paragraph aligned right.</p>\n\n<div align="left">A box aligned left.</div>\n\n'),
  htmlDivClass: doc('<div class="align-right">A box with the class only.</div>\n\n'),
  inAdmonition: doc('````{note}\n```{image} pic.svg\n:width: 90px\n:align: right\n```\n\nText beside it.\n````\n\n'),
  inList: doc('- item\n\n  <img src="pic.svg" width="80" align="right">\n\n- other item\n\n'),
  floatFirst: `${image("right")}# Title${tail}`,
  floatLast: `# Title${tail}\n${image("left")}`,
};

const modulesOf = (build) => {
  const load = (file) => require(path.join(BUILDS[build], file));
  return {
    pipeline: load("src/core/render/renderPipeline.js"),
    files: load("src/node-services/nodeFileSystem.js"),
    webview: load("src/session/webview.js"),
    exportHtml: load("src/core/export/htmlExport.js"),
    patch: load("src/core/preview/contentPatch.js"),
    assets: load("test/shared/fakeAssets.js"),
    harness: load("test/page/runtimeHarness.js"),
  };
};

async function render(build, viewportWidth) {
  const m = modulesOf(build);
  const root = path.join(scratch, `${build}-${viewportWidth}`);
  fs.mkdirSync(path.join(root, "out", "bundle"), { recursive: true });
  const real = fs.realpathSync(root);
  fs.writeFileSync(path.join(real, "pic.svg"), SVG);
  fs.writeFileSync(path.join(real, "out", "bundle", "preview.js"), m.harness.pageRuntimeScript());
  const documentPath = path.join(real, "doc.md");
  const assets = m.assets.fakeAssetResolver({ cspSource: "file:", url: (p) => pathToFileURL(p).href, extensionRoot: real });
  const bundle = { ...assets, bundleUri: (...s) => (s[0] === "preview.js" ? assets.bundleUri(...s) : undefined) };
  const identity = { documentId: pathToFileURL(documentPath).toString(), revision: 1, requestId: 1 };
  const pages = {};
  for (const [name, markdown] of Object.entries(DOCS)) {
    fs.writeFileSync(documentPath, markdown);
    const rendered = await m.pipeline.renderPreviewDocument({
      files: m.files.createNodeFileSystem(),
      document: { uri: { scheme: "file", fsPath: documentPath }, languageId: "markdown", version: 1, getText: () => markdown },
      workspaceRoot: real,
      requestId: 1,
      isWorkspaceTrusted: () => true,
    });
    const built = await m.webview.buildPreviewWebviewHtml(m.files.createNodeFileSystem(), rendered.html, real, bundle, {
      activeSourceFile: documentPath,
      ...identity,
      previewThemeMode: "current",
      initialViewPreferences: { zoom: 100, widthMode: "auto", toc: false, incomingChanges: true, comments: true, toolbarCollapsed: false },
    }, real, undefined, 900, true, [], "builtin");
    const inner = m.patch.extractMainContent(built.html).inner;
    const exported = m.exportHtml.buildHtmlExport({
      contentHtml: `<main id="sphinx-myst-preview-content">${inner}</main>`,
      rootAttributes: {}, tokens: {}, mathStyles: "", shownTabs: [],
    }, { stem: "doc", maxContentWidth: 900, imageData: () => DATA }).html;
    pages[name] = { page: built.html, exported, inner };
  }
  return { pages, identity, root: real };
}

const layoutOf = (page) => page.evaluate(() => {
  const main = document.getElementById("sphinx-myst-preview-content");
  const before = getComputedStyle(main, "::before");
  const elements = Array.from(main.querySelectorAll("*"));
  return {
    marked: main.hasAttribute("data-okf-aligned-float"),
    before: [before.display, before.float, before.width, before.height].join("/"),
    height: document.documentElement.scrollHeight,
    count: elements.length,
    floated: elements.filter((e) => getComputedStyle(e).float !== "none" && e.matches("img, figure, table")).length,
    headingClear: [...new Set(Array.from(main.querySelectorAll(":scope > :is(h1,h2,h3,h4,h5,h6), :scope > section :is(h1,h2,h3,h4,h5,h6)"))
      .map((e) => getComputedStyle(e).clear))].join("+"),
    brokenImages: Array.from(document.images).filter((i) => !i.naturalWidth).length,
    items: elements.map((e) => {
      const s = getComputedStyle(e);
      const r = e.getBoundingClientRect();
      const cls = typeof e.className === "string" ? e.className : "";
      return `${e.tagName.toLowerCase()}.${cls} clear=${s.clear} float=${s.float} display=${s.display} `
        + `[${[r.x, r.y + window.scrollY, r.width, r.height].map((v) => Math.round(v * 2) / 2).join(",")}]`;
    }),
  };
});

const settle = (page) => page.evaluate(async () => {
  await Promise.all(Array.from(document.images).map((i) => i.decode().catch(() => undefined)));
  for (let n = 0; n < 4; n += 1) await new Promise((r) => requestAnimationFrame(() => r()));
});

let comparisons = 0;
let differing = 0;
function compare(label, a, b) {
  comparisons += 1;
  const diffs = [];
  for (const key of ["before", "height", "count", "floated", "headingClear", "brokenImages"]) {
    if (a[key] !== b[key]) diffs.push(`${key}: old ${a[key]} new ${b[key]}`);
  }
  const length = Math.max(a.items.length, b.items.length);
  for (let i = 0; i < length; i += 1) {
    if (a.items[i] !== b.items[i]) diffs.push(`element ${i}: old ${a.items[i]} | new ${b.items[i]}`);
  }
  if (diffs.length) differing += 1;
  console.log(`${diffs.length ? "DIFF" : "same"} ${label}: elements ${b.count}, floats ${b.floated}, ::before ${b.before}, `
    + `heading clear ${b.headingClear}, height ${a.height}/${b.height}, new mark ${b.marked}, broken images ${a.brokenImages}/${b.brokenImages}`);
  for (const line of diffs.slice(0, 6)) console.log(`    ${line}`);
  if (diffs.length > 6) console.log(`    and ${diffs.length - 6} more`);
}

async function main() {
  // The probe ends itself rather than waiting for ever.
  setTimeout(() => { console.log("watchdog: the probe did not end in time"); process.exit(3); }, 540000).unref();
  const browser = await chromium.launch();
  try {
    for (const width of [900, 420]) {
      const sides = { old: await render("old", width), new: await render("new", width) };
      console.log(`\n=== viewport ${width}x700`);
      // 1 and 2: no page script, the preview page and the exported file.
      for (const surface of ["page", "exported"]) {
        console.log(`-- ${surface}, no page script`);
        for (const name of Object.keys(DOCS)) {
          const results = {};
          for (const [side, built] of Object.entries(sides)) {
            const context = await browser.newContext({ viewport: { width, height: 700 }, javaScriptEnabled: false });
            const page = await context.newPage();
            const file = path.join(built.root, `${surface}-${name}.html`);
            fs.writeFileSync(file, built.pages[name][surface]);
            await page.goto(pathToFileURL(file).href, { waitUntil: "load" });
            results[side] = await layoutOf(page);
            await context.close();
          }
          compare(`${surface} ${name}`, results.old, results.new);
        }
      }
      // 3: the page runtime, at load, after content patches and after changes of the page itself.
      console.log("-- page with the page runtime");
      const open = async (built, name) => {
        const page = await browser.newPage({ viewport: { width, height: 700 }, deviceScaleFactor: 1 });
        const errors = [];
        page.on("pageerror", (error) => errors.push(String(error.message)));
        await page.addInitScript(() => {
          Object.assign(window, { acquireVsCodeApi: () => ({ getState: () => ({}), setState: () => undefined, postMessage: () => undefined }) });
        });
        const file = path.join(built.root, `runtime-${name}.html`);
        fs.writeFileSync(file, built.pages[name].page);
        await page.goto(pathToFileURL(file).href);
        await page.waitForFunction(() => document.documentElement.getAttribute("data-sphinx-preview-width") === "auto");
        await settle(page);
        return { page, errors };
      };
      for (const name of Object.keys(DOCS)) {
        const results = {};
        for (const [side, built] of Object.entries(sides)) {
          const opened = await open(built, name);
          results[side] = await layoutOf(opened.page);
          if (opened.errors.length) console.log(`    page errors (${side}): ${opened.errors.join("; ")}`);
          await opened.page.close();
        }
        compare(`runtime load ${name}`, results.old, results.new);
      }
      // Content patches: one page per build walks through every document and back to the plain one.
      const walk = [];
      for (const name of Object.keys(DOCS)) if (name !== "plain") walk.push(name, "plain");
      walk.push("imageRight", "tableLeft", "figureCenter", "htmlParagraphAlign", "figureLeft", "plainImage");
      const live = { old: await open(sides.old, "plain"), new: await open(sides.new, "plain") };
      let revision = 1;
      for (const name of walk) {
        revision += 1;
        const results = {};
        for (const [side, built] of Object.entries(sides)) {
          const { page } = live[side];
          await page.evaluate((data) => { window.dispatchEvent(new MessageEvent("message", { data })); }, {
            type: "previewContentPatch", documentId: built.identity.documentId,
            revision: revision - 1, requestId: revision - 1, next: { revision, requestId: revision },
            contentHtml: built.pages[name].inner, status: "success", label: "ready", diagnostics: [],
          });
          await page.waitForFunction((wanted) => document.documentElement.getAttribute("data-sphinx-preview-request-id") === wanted,
            String(revision), { timeout: 15000 });
          await settle(page);
          await page.evaluate(() => window.scrollTo(0, 0));
          await settle(page);
          results[side] = await layoutOf(page);
        }
        compare(`patch ${revision} to ${name}`, results.old, results.new);
      }
      // Changes of the page itself, on the plain content.
      revision += 1;
      const steps = [
        ["add a float figure deep in the content", () => {
          const box = document.createElement("div");
          box.id = "added";
          box.innerHTML = '<figure class="align-left" style="width:90px;height:60px">f</figure>';
          document.querySelector("#sphinx-myst-preview-content p").after(box);
        }],
        ["remove it", () => { document.getElementById("added").remove(); }],
        ["a table gets align=right", () => { document.querySelector("#sphinx-myst-preview-content table").setAttribute("align", "right"); }],
        ["the table gets align=center", () => { document.querySelector("#sphinx-myst-preview-content table").setAttribute("align", "center"); }],
        ["the table gets the class align-left", () => { document.querySelector("#sphinx-myst-preview-content table").classList.add("align-left"); }],
        ["the class is removed", () => { document.querySelector("#sphinx-myst-preview-content table").classList.remove("align-left"); }],
        ["two floats added", () => {
          const main = document.getElementById("sphinx-myst-preview-content");
          for (const id of ["one", "two"]) {
            const img = document.createElement("img");
            img.id = id; img.setAttribute("align", "left"); img.width = 50; img.height = 40;
            main.querySelector("p").prepend(img);
          }
        }],
        ["one of the two removed", () => { document.getElementById("one").remove(); }],
        ["the last removed", () => { document.getElementById("two").remove(); }],
      ];
      for (const side of Object.keys(sides)) {
        const { page } = live[side];
        await page.evaluate((data) => { window.dispatchEvent(new MessageEvent("message", { data })); }, {
          type: "previewContentPatch", documentId: sides[side].identity.documentId,
          revision: revision - 1, requestId: revision - 1, next: { revision, requestId: revision },
          contentHtml: sides[side].pages.plain.inner, status: "success", label: "ready", diagnostics: [],
        });
        await page.waitForFunction((wanted) => document.documentElement.getAttribute("data-sphinx-preview-request-id") === wanted,
          String(revision), { timeout: 15000 });
        await settle(page);
      }
      for (const [label, change] of steps) {
        const results = {};
        for (const side of Object.keys(sides)) {
          const { page } = live[side];
          await page.evaluate(change);
          await settle(page);
          results[side] = await layoutOf(page);
        }
        compare(`page change: ${label}`, results.old, results.new);
      }
      for (const [side, opened] of Object.entries(live)) {
        console.log(`    page errors (${side}) over patches and changes: ${opened.errors.length ? opened.errors.join("; ") : "none"}`);
        await opened.page.close();
      }
    }
  } finally {
    await browser.close();
  }
  console.log(`\n${comparisons} comparisons, ${differing} with a difference`);
}

main().catch((error) => { console.error(error); process.exitCode = 1; });

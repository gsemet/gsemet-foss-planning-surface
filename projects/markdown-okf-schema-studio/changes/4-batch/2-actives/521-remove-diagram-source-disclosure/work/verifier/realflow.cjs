// Verifier real-flow probe for CR-521.
// Run from a built worktree (npm run compile && npm run bundle):
//   node --import ./scripts/register-myst-patches.mjs <this file> <worktree> <output folder> [assert|shots]
// Real render pipeline, real page builder, the extension's built bundles, headless Chromium with a
// stand-in for the VS Code webview API; the Export button is clicked and its request goes to the
// session's HtmlExportController, which writes the file; that file is opened with JavaScript off.
"use strict";
const fs = require("node:fs");
const path = require("node:path");
const { createRequire } = require("node:module");
const { pathToFileURL } = require("node:url");

const [worktree, outDir, mode = "assert"] = process.argv.slice(2);
const requireWt = createRequire(path.join(worktree, "package.json"));
const built = (relative) => require(path.join(worktree, "out", relative));
const { chromium } = requireWt("playwright-core");
const { renderPreviewDocument } = built("src/core/render/renderPipeline");
const { buildPreviewWebviewHtml } = built("src/session/webview");
const { createNodeFileSystem } = built("src/node-services/nodeFileSystem");
const { HtmlExportController } = built("src/session/features/htmlExport");
const { HostRequestController } = built("src/session/features/hostRequests");
const { createMemoryLogger } = built("src/host-memory/memoryLogger");
const { fakeAssetResolver } = built("test/shared/fakeAssets");
const { THEMES } = built("test/visual/themes");

const fence = (info, lines) => ["```" + info, ...lines, "```", ""];
const chart = (word, extra) => JSON.stringify({
  description: word, width: 320, height: 110,
  data: { values: [{ r: "North", v: 28 }, { r: "South", v: 55 }, { r: "East", v: 43 }] },
  mark: "bar", encoding: { x: { field: "r", type: "nominal" }, y: { field: "v", type: "quantitative" } }, ...extra,
});
const vega = (word, url) => JSON.stringify({
  description: word, width: 320, height: 90,
  data: [url ? { name: "t", url, format: { type: "csv" } } : { name: "t", values: [{ x: 1, y: 3 }, { x: 2, y: 7 }] }],
  scales: [{ name: "x", type: "point", domain: { data: "t", field: "x" }, range: "width" },
    { name: "y", domain: { data: "t", field: "y" }, range: "height" }],
  marks: [{ type: "symbol", from: { data: "t" }, encode: { enter: { x: { scale: "x", field: "x" }, y: { scale: "y", field: "y" } } } }],
});

// Every source carries one word that no visible message repeats.
const FIGURES = [
  { word: "wmermaiddrawn", kind: "mermaid", want: "rendered", md: ["## Mermaid, drawn", "", ...fence("mermaid", ["flowchart LR", "  %% wmermaiddrawn", "  Draft --> Review --> Merge"])] },
  { word: "wmermaidfail", kind: "mermaid", want: "error", md: ["## Mermaid, broken", "", ...fence("mermaid", ["flowchart LR", "  %% wmermaidfail", "  Draft --> --> ((("])] },
  { word: "wplantdrawn", kind: "plantuml", want: "rendered", md: ["## PlantUML, drawn", "", ...fence("plantuml", ["@startuml", "' wplantdrawn", "Alice -> Bob: hello", "@enduml"])] },
  { word: "wplantrefused", kind: "plantuml", want: "unavailable", md: ["## PlantUML, refused include", "", ...fence("plantuml", ["@startuml", "' wplantrefused", "!include <C4/C4_Context>", "Alice -> Bob", "@enduml"])] },
  { word: "wplantmissing", kind: "plantuml", want: "error", md: ["## PlantUML, missing local include", "", ...fence("plantuml", ["@startuml", "' wplantmissing", "!include nowhere/absent.puml", "Alice -> Bob", "@enduml"])] },
  { word: "wlitedrawn", kind: "vega", want: "rendered", md: ["## Vega-Lite, drawn", "", ...fence("vega-lite", [chart("wlitedrawn")])] },
  { word: "wlitefail", kind: "vega", want: "error", md: ["## Vega-Lite, broken", "", ...fence("vega-lite", ['{ "description": "wlitefail", "mark": "bar", "data": { "values": [ }'])] },
  { word: "wvegadrawn", kind: "vega", want: "rendered", md: ["## Vega, drawn", "", ...fence("vega", [vega("wvegadrawn")])] },
  { word: "wvegafail", kind: "vega", want: "error", md: ["## Vega, missing data file", "", ...fence("vega", [vega("wvegafail", "data/absent.csv")])] },
  { word: "wnoteddrawn", kind: "mermaid", want: "rendered", md: ["## Directive with a caption, drawn", "", "```{mermaid}", ":caption: A captioned diagram", "", "flowchart LR", "  %% wnoteddrawn", "  A --> B", "```", ""] },
  { word: "wnotedfail", kind: "mermaid", want: "error", md: ["## Inside an admonition, broken", "", ":::{note}", "```{mermaid}", ":caption: A captioned broken diagram", "", "flowchart LR", "  %% wnotedfail", "  A --> -->", "```", ":::", ""] },
];
const SHOT_WORDS = ["wmermaiddrawn", "wmermaidfail", "wlitedrawn", "wlitefail"];
// Mode "syntax": PlantUML sources the built-in engine cannot understand.
const uml = (word, lines) => ({ word, kind: "plantuml", want: "?", md: ["## " + word, "", ...fence("plantuml", ["@startuml", "' " + word, ...lines, "@enduml"])] });
const SYNTAX = [
  uml("wplantsyntaxline", ["Alice -> Bob: hello", "this is not plantuml ((( ###"]),
  uml("wplantsyntaxarrow", ["Alice ->>>>x<< : ", "}}}"]),
  uml("wplantsyntaxclass", ["class A {", "  +x : int", "activate ??? !!"]),
];
const figures = mode === "shots" ? FIGURES.filter((f) => SHOT_WORDS.includes(f.word)) : mode === "syntax" ? SYNTAX : FIGURES;
const MARKDOWN = ["# Figures", "", ...figures.flatMap((f) => f.md), "The text after the figures.", ""].join("\n");

const root = path.resolve(outDir);
const workspace = path.join(root, "workspace");
fs.mkdirSync(workspace, { recursive: true });
const documentPath = path.join(workspace, "figures.md");
fs.writeFileSync(documentPath, MARKDOWN);

async function buildPage(name, engine, withBundles) {
  const files = createNodeFileSystem();
  const rendered = await renderPreviewDocument({
    files, document: { uri: { scheme: "file", fsPath: documentPath }, languageId: "markdown", version: 1, getText: () => MARKDOWN },
    workspaceRoot: workspace, requestId: 1, isWorkspaceTrusted: () => true, plantUmlEngine: engine,
    ...(engine === "jar" ? { plantUmlJarPath: "C:/tools/absent/plantuml.jar" } : {}),
  });
  const plantUml = engine === "jar" ? (await rendered.resolvePlantUml()).diagrams : [];
  const bundle = fakeAssetResolver({ cspSource: "file:", url: (p) => pathToFileURL(p).href, extensionRoot: worktree });
  const assets = withBundles ? bundle : { ...bundle, bundleUri: (...s) => /Preview\.js$/u.test(s[0]) ? undefined : bundle.bundleUri(...s) };
  const context = {
    activeSourceFile: documentPath, documentId: pathToFileURL(documentPath).toString(), revision: 1, requestId: 1,
    previewThemeMode: "current",
    initialViewPreferences: { zoom: 100, widthMode: "auto", toc: false, incomingChanges: true, comments: true, toolbarCollapsed: false },
  };
  const result = await buildPreviewWebviewHtml(files, rendered.html, workspace, assets, context, workspace,
    undefined, undefined, true, plantUml, engine === "jar" ? "host" : "builtin");
  const pagePath = path.join(root, `${name}.page.html`);
  fs.writeFileSync(pagePath, result.html);
  return pagePath;
}

async function openPage(browser, pagePath, themeId) {
  const page = await browser.newPage({ viewport: { width: 900, height: 1000 }, deviceScaleFactor: 1 });
  const problems = [];
  page.on("pageerror", (error) => problems.push(error.message));
  await page.addInitScript(() => {
    window.__posted = [];
    window.acquireVsCodeApi = () => ({ getState: () => ({}), setState: () => undefined, postMessage: (m) => { window.__posted.push(m); } });
  });
  await page.goto(pathToFileURL(pagePath).href);
  const theme = THEMES.find((t) => t.id === themeId);
  await page.evaluate(({ variables, id }) => {
    document.body.classList.add(id === "dark" ? "vscode-dark" : "vscode-light");
    for (const [name, value] of Object.entries(variables)) document.body.style.setProperty(name, value);
  }, { variables: theme.variables, id: themeId });
  return { page, problems };
}

const settle = async (page) => {
  await page.waitForFunction(() => [...document.querySelectorAll(".myst-mermaid-diagram, .myst-vega-diagram, .myst-plantuml-diagram")]
    .every((d) => d.hasAttribute("data-render-state")), undefined, { timeout: 60_000 });
  await page.waitForTimeout(2500);
};

/** One row per figure, found by the word of its source. */
const rows = (page) => page.evaluate((words) => words.map((word) => {
  const source = [...document.querySelectorAll("details[class$='-source']")].find((d) => d.textContent.includes(word));
  if (!source) return { word, missing: true };
  const figure = source.parentElement;
  const diagram = figure.querySelector(":scope > [class$='-diagram']");
  const summary = source.querySelector("summary");
  return {
    word, state: diagram.getAttribute("data-render-state") || "pending", summary: summary.textContent.trim(),
    display: getComputedStyle(source).display, summaryBox: Math.round(summary.getBoundingClientRect().height), open: source.open,
  };
}), figures.map((f) => f.word));

async function clickOpens(page) {
  const out = [];
  const panels = page.locator("details[class$='-source']");
  for (let i = 0; i < await panels.count(); i += 1) {
    const panel = panels.nth(i);
    if (!await panel.isVisible()) continue;
    const word = (await panel.textContent()).match(/w(?:mermaid|plant|lite|vega|noted)[a-z]+/u)[0];
    await panel.locator("summary").click();
    const open = await panel.evaluate((d) => d.open);
    const codeVisible = await panel.locator("pre").isVisible();
    await panel.locator("summary").click();
    out.push({ word, openAfterClick: open, codeVisible, openAfterSecondClick: await panel.evaluate((d) => d.open) });
  }
  return out;
}

async function find(page) {
  await page.keyboard.press("Control+f");
  const input = page.locator("[data-sphinx-preview-find] input[data-find-input], [data-sphinx-preview-find] input").first();
  await input.waitFor({ state: "visible" });
  const out = [];
  for (const word of [...figures.map((f) => f.word), "figures"]) {
    await input.fill("");
    await input.fill(word);
    await page.waitForTimeout(700);
    const count = await page.evaluate(() => [...document.querySelectorAll("[data-sphinx-preview-find] *")]
      .filter((e) => e.children.length === 0 && /\d+ of \d+|No results|No match/iu.test(e.textContent)).map((e) => e.textContent.trim()).join(" | "));
    const openPanels = await page.evaluate(() => [...document.querySelectorAll("details[class$='-source']")].filter((d) => d.open).length);
    const matchesIn = await page.evaluate(() => [...(CSS.highlights || [])].flatMap(([, highlight]) => [...highlight].map((range) => {
      const owner = range.startContainer.parentElement;
      const part = owner.closest("details[class$='-source'], [class$='-diagram']");
      return part ? part.className : owner.tagName.toLowerCase();
    })));
    out.push({ word, count, matchesIn: [...new Set(matchesIn)].sort(), openPanels });
  }
  await page.keyboard.press("Escape");
  return out;
}

async function exportFile(page, name) {
  await page.evaluate(() => { window.__posted.length = 0; });
  await page.locator("[data-sphinx-preview-export]").first().evaluate((button) => button.click());
  await page.waitForFunction(() => window.__posted.some((m) => m.type === "previewExportHtml"), undefined, { timeout: 30_000 });
  const message = await page.evaluate(() => window.__posted.find((m) => m.type === "previewExportHtml"));
  const target = path.join(root, `${name}.export.html`);
  const files = createNodeFileSystem();
  const answers = [];
  const manager = {
    host: {
      files, logger: createMemoryLogger(), workspace: { folders: () => [{ path: workspace }] },
      ui: { confirm: async () => true, pickSaveFile: async () => target, showInformation: async () => undefined, showError: async (m) => { throw new Error(m); } },
    },
    activePathOf: () => documentPath,
  };
  manager.requests = new HostRequestController(manager);
  const controller = new HtmlExportController(manager);
  const handlers = new Map();
  controller.register({ on: (type, handler) => handlers.set(type, handler) });
  await handlers.get("previewExportHtml")(message, {
    documentUri: message.documentId, document: { id: message.documentId, path: documentPath }, configuration: { maxContentWidth: 900 },
    panel: { bundleRoot: path.join(worktree, "out", "bundle") }, webview: { html: "", nonce: "", resources: new Map() },
    postToPage: async (m) => { answers.push(m); return true; },
  });
  const answer = answers.find((m) => m.type === "previewExportHtmlResult");
  return { target, ok: answer?.ok, userGesture: message.userGesture };
}

/** The page from its top to a little under its last paragraph. */
async function clipped(page, file) {
  const box = await page.getByText("The text after the figures.").boundingBox();
  await page.screenshot({ path: file, fullPage: true, clip: { x: 0, y: 0, width: 900, height: Math.ceil(box.y + box.height + 28) } });
}

async function editMode(page) {
  await page.locator("[data-sphinx-preview-edit-toggle]").first().evaluate((button) => button.click());
  await page.waitForFunction(() => document.documentElement.getAttribute("data-sphinx-preview-edit-mode") === "on");
  const out = [];
  for (const word of ["wmermaidfail", "wplantrefused", "wnotedfail"]) {
    const panel = page.locator("details[class$='-source']", { hasText: word });
    const visible = await panel.isVisible();
    await page.evaluate(() => { window.__posted.length = 0; });
    await panel.locator("summary").click();
    await page.waitForTimeout(500);
    const opens = await page.evaluate(() => window.__posted.filter((m) => m.type === "previewEditOpen"));
    const open = await panel.evaluate((d) => d.open);
    let editor = null;
    if (opens.length === 1) {
      const lines = MARKDOWN.split("\n");
      const originalText = lines.slice(opens[0].line - 1, opens[0].endLine).join("\n");
      await page.evaluate((data) => window.dispatchEvent(new MessageEvent("message", { data })),
        { ...opens[0], type: "previewEditSource", originalText });
      await page.waitForTimeout(700);
      editor = await page.evaluate((w) => {
        const box = [...document.querySelectorAll("textarea")].find((t) => t.value.includes(w));
        return box ? { visible: box.getBoundingClientRect().height > 0, firstLine: box.value.split("\n")[0] } : null;
      }, word);
      await page.keyboard.press("Escape");
      await page.waitForTimeout(700);
    }
    out.push({ word, visible, previewEditOpen: opens.map((m) => [m.line, m.endLine]), disclosureOpen: open, editor });
  }
  return out;
}

(async () => {
  const browser = await chromium.launch({ args: ["--allow-file-access-from-files"] });
  const noJs = await browser.newContext({ javaScriptEnabled: false, viewport: { width: 900, height: 1000 } });
  const report = { mode, figures: figures.map((f) => [f.word, f.want]) };
  try {
    if (mode === "assert") {
      for (const [name, engine] of [["builtin", "builtin"], ["jar", "jar"]]) {
        const pagePath = await buildPage(name, engine, true);
        const { page, problems } = await openPage(browser, pagePath, "light");
        await settle(page);
        const result = report[name] = { preview: await rows(page) };
        result.clicks = await clickOpens(page);
        result.find = await find(page);
        const exported = await exportFile(page, name);
        result.export = { ok: exported.ok, userGesture: exported.userGesture, file: path.basename(exported.target), scripts: (fs.readFileSync(exported.target, "utf8").match(/<script/giu) || []).length };
        const reader = await noJs.newPage();
        await reader.goto(pathToFileURL(exported.target).href);
        result.export.rows = await rows(reader);
        result.export.clicks = await clickOpens(reader);
        await reader.close();
        if (engine === "builtin") result.editMode = await editMode(page);
        result.pageErrors = problems;
        await page.close();
      }
      // Pending: the same document with no diagram runtime, so no figure gets a render state.
      const pending = await openPage(browser, await buildPage("pending", "builtin", false), "light");
      await pending.page.waitForTimeout(1500);
      report.pending = { preview: await rows(pending.page), find: await find(pending.page) };
      await pending.page.close();
    } else if (mode === "syntax") {
      const { page, problems } = await openPage(browser, await buildPage("syntax", "builtin", true), "light");
      await settle(page);
      report.syntax = { preview: await rows(page) };
      report.syntax.pictures = await page.evaluate(() => [...document.querySelectorAll(".myst-plantuml-diagram")].map((d) => {
        const src = d.querySelector("img")?.getAttribute("src");
        const svg = src ? decodeURIComponent(src.slice(src.indexOf(",") + 1)) : "";
        return { state: d.getAttribute("data-render-state"), picture: Boolean(src), says: [...new DOMParser().parseFromString(svg || "<svg/>", "image/svg+xml").querySelectorAll("text")].map((e) => e.textContent).join(" ").slice(0, 260), message: d.querySelector("p")?.textContent?.slice(0, 200) };
      }));
      await clipped(page, path.join(root, "syntax-light.png"));
      report.syntax.pageErrors = problems;
      const exported = await exportFile(page, "syntax");
      const reader = await noJs.newPage();
      await reader.goto(pathToFileURL(exported.target).href);
      report.syntax.exported = await rows(reader);
      await reader.close();
      await page.close();
    } else {
      const pagePath = await buildPage("shots", "builtin", true);
      for (const themeId of ["light", "dark"]) {
        const { page } = await openPage(browser, pagePath, themeId);
        await settle(page);
        report[themeId] = { preview: await rows(page) };
        const height = await page.evaluate(() => document.documentElement.scrollHeight);
        await page.setViewportSize({ width: 900, height: Math.min(height + 20, 3000) });
        await page.waitForTimeout(1500);
        await clipped(page, path.join(root, `preview-${themeId}.png`));
        const exported = await exportFile(page, themeId);
        const reader = await noJs.newPage();
        await reader.goto(pathToFileURL(exported.target).href);
        report[themeId].export = await rows(reader);
        await clipped(reader, path.join(root, `export-${themeId}.png`));
        await reader.close();
        await page.close();
      }
    }
  } finally {
    await browser.close();
    fs.writeFileSync(path.join(root, "report.json"), JSON.stringify(report, null, 1));
  }
  for (const [key, value] of Object.entries(report)) {
    console.log(`== ${key}`);
    if (Array.isArray(value)) { console.log(JSON.stringify(value)); continue; }
    if (typeof value !== "object") { console.log(String(value)); continue; }
    for (const [section, data] of Object.entries(value)) {
      if (section === "export" && data.rows) {
        console.log(`-- export ${JSON.stringify({ ...data, rows: undefined, clicks: undefined })}`);
        data.rows.forEach((r) => console.log(`export row ${JSON.stringify(r)}`));
        data.clicks.forEach((r) => console.log(`export click ${JSON.stringify(r)}`));
      } else if (Array.isArray(data)) {
        console.log(`-- ${section}`);
        data.forEach((r) => console.log(JSON.stringify(r)));
      }
    }
  }
})().catch((error) => { console.error(error); process.exit(1); });

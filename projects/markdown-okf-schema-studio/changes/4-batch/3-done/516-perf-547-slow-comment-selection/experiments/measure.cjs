// Drives the rendered preview pages in headless Chromium and records a performance trace per scenario.
// The host side of the comments is the product's CommentsController on the real disk (no VS Code).
// usage: node measure.cjs <worktree> <tag> <resultName> [--reps 5] [--throttle 1] [--variants a,b] [--scenarios x,y]
"use strict";
const fs = require("node:fs");
const path = require("node:path");
const { pathToFileURL } = require("node:url");
const { execFile } = require("node:child_process");

const here = __dirname;
const [worktreeArg, tag, resultName, ...rest] = process.argv.slice(2);
const worktree = path.resolve(worktreeArg);
const option = (name, fallback) => { const i = rest.indexOf(`--${name}`); return i < 0 ? fallback : rest[i + 1]; };
const REPS = Number(option("reps", 5));
const THROTTLE = Number(option("throttle", 1));
const OFFSET = Number(option("offset", 0));
const { chromium } = require(path.join(worktree, "node_modules", "playwright-core"));
const lib = (p) => require(path.join(worktree, "out", "src", p));
const { CommentsController, createCommentsState } = lib("session/features/comments");
const { createNodeFileSystem } = lib("node-services/nodeFileSystem");

const VARIANTS = {
  full: { doc: "full" },
  nothreads: { doc: "nothreads" },
  small: { doc: "small" },
  nosvg: { doc: "nosvg" },
  notables: { doc: "notables" },
  flat: { doc: "flat" },
  xl4: { doc: "xl4" },
  inlinesvg: { doc: "inlinesvg" },
  "full-nohas": { doc: "full", asset: "nohas" },
  "full-nohas3": { doc: "full", asset: "nohas3" },
  "xl4-nohas": { doc: "xl4", asset: "nohas" },
  "xl4-nohas3": { doc: "xl4", asset: "nohas3" },
  "small-nohas": { doc: "small", asset: "nohas" },
  "full-noselchange": { doc: "full", block: ["selectionchange"] },
  "full-nohover": { doc: "full", block: ["mousemove", "mouseover", "mouseout"] },
  "xl4-noselchange": { doc: "xl4", block: ["selectionchange"] },
  "xl4-nohover": { doc: "xl4", block: ["mousemove", "mouseover", "mouseout"] },
  "full-noclearright": { doc: "full", asset: "noclearright" },
  "full-noheadclear": { doc: "full", asset: "noheadclear" },
  "full-edit": { doc: "full", edit: true },
  "full-edit-nohas": { doc: "full", asset: "nohas", edit: true },
  "small-edit": { doc: "small", edit: true },
  "xl4-edit": { doc: "xl4", edit: true },
  "full-instr": { doc: "full", asset: "instr" },
  "xl4-instr": { doc: "xl4", asset: "instr" },
  "small-instr": { doc: "small", asset: "instr" },
};
const names = option("variants", Object.keys(VARIANTS).join(",")).split(",");
const wanted = option("scenarios", "drag-text,drag-table,release,drag-scroll,hover,extend-cell,extend-large,keyboard,create,repost").split(",");
const pages = JSON.parse(fs.readFileSync(path.join(here, "pages", tag, "pages.json"), "utf8")).pages;

const GROUPS = {
  style: /^(UpdateLayoutTree|RecalculateStyles|ParseAuthorStyleSheet|InvalidateLayout|Document::recalcStyle|Document::updateStyle)/,
  layout: /^Layout$/,
  paint: /^(PrePaint|Paint|Layerize|UpdateLayer|UpdateLayerTree|Commit|CompositeLayers|RasterTask|PaintImage)$/,
  hittest: /^HitTest$/,
  script: /^(FunctionCall|EventDispatch|EvaluateScript|TimerFire|FireAnimationFrame|MinorGC|MajorGC|V8\.|v8)/,
};

function analyse(buffer) {
  const events = JSON.parse(buffer.toString("utf8")).traceEvents;
  const mains = events.filter((e) => e.name === "thread_name" && e.args?.name === "CrRendererMain").map((e) => `${e.pid}:${e.tid}`);
  const perThread = new Map(mains.map((k) => [k, []]));
  const open = new Map();
  for (const e of events) {
    const list = perThread.get(`${e.pid}:${e.tid}`);
    if (!list) continue;
    if (e.ph === "X") list.push({ name: e.name, ts: e.ts, dur: e.dur || 0, args: e.args });
    else if (e.ph === "B") { const s = open.get(e.tid) || []; s.push(e); open.set(e.tid, s); }
    else if (e.ph === "E") { const s = open.get(e.tid) || []; const b = s.pop(); if (b) list.push({ name: b.name, ts: b.ts, dur: e.ts - b.ts, args: { ...b.args, ...e.args } }); }
  }
  const list = [...perThread.values()].sort((a, b) => b.length - a.length)[0] || [];
  list.sort((a, b) => a.ts - b.ts || b.dur - a.dur);
  const stack = [], roots = [];
  for (const e of list) {
    while (stack.length && e.ts >= stack[stack.length - 1].ts + stack[stack.length - 1].dur) stack.pop();
    e.self = e.dur;
    if (stack.length) stack[stack.length - 1].self -= e.dur; else roots.push(e);
    stack.push(e);
  }
  const out = { busy: 0, maxTask: 0, style: 0, layout: 0, paint: 0, hittest: 0, script: 0, other: 0, styleElements: 0, styleCount: 0, styleMaxElements: 0, layoutCount: 0, events: {}, top: {} };
  for (const r of roots) { out.busy += r.dur / 1000; out.maxTask = Math.max(out.maxTask, r.dur / 1000); }
  for (const e of list) out.top[e.name] = (out.top[e.name] || 0) + Math.max(0, e.self) / 1000;
  out.top = Object.fromEntries(Object.entries(out.top).sort((a, b) => b[1] - a[1]).slice(0, 14).map(([k, v]) => [k, Math.round(v * 10) / 10]));
  for (const e of list) {
    const group = Object.keys(GROUPS).find((g) => GROUPS[g].test(e.name)) || "other";
    out[group] += Math.max(0, e.self) / 1000;
    if (e.name === "UpdateLayoutTree") {
      const n = e.args?.elementCount ?? e.args?.endData?.elementCount ?? 0;
      out.styleElements += n; out.styleCount += 1; out.styleMaxElements = Math.max(out.styleMaxElements, n);
    }
    if (e.name === "Layout") out.layoutCount += 1;
    if (e.name === "EventDispatch") {
      const type = e.args?.data?.type || "?";
      const t = out.events[type] || (out.events[type] = { count: 0, total: 0, max: 0 });
      t.count += 1; t.total += e.dur / 1000; t.max = Math.max(t.max, e.dur / 1000);
    }
  }
  return out;
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function openPage(browser, variant, runDir) {
  const spec = VARIANTS[variant];
  const asset = spec.asset || "orig";
  const built = pages.find((p) => p.doc === spec.doc && p.assetName === asset);
  const sourceDir = path.join(here, "bundle", spec.doc);
  fs.rmSync(runDir, { recursive: true, force: true });
  fs.mkdirSync(runDir, { recursive: true });
  for (const f of ["report.md", "report.comments.json"]) fs.copyFileSync(path.join(sourceDir, f), path.join(runDir, f));
  const documentPath = path.join(runDir, "report.md");
  const documentId = built.documentId; // the page was built for the generated bundle's identity
  const context = await browser.newContext({ viewport: { width: 1200, height: 900 }, deviceScaleFactor: 1 });
  const page = await context.newPage();
  const errors = [];
  page.on("pageerror", (e) => errors.push(String(e)));
  page.on("console", (m) => { if (m.type() === "error") errors.push(m.text()); });

  // Host: the real comments controller over the real file system, on the run's copy of the sidecar.
  const files = createNodeFileSystem();
  const hostLog = [];
  const timed = (name, fn) => async (...args) => { const s = performance.now(); try { return await fn(...args); } finally { hostLog.push([name, performance.now() - s]); } };
  const timedFiles = {};
  for (const name of ["stat", "readFile", "writeFile", "rename", "delete", "isSymbolicLink"]) timedFiles[name] = timed(name, files[name].bind(files));
  const text = fs.readFileSync(documentPath, "utf8");
  const posted = [];
  const host = {
    files: timedFiles,
    logger: { error: (...a) => errors.push(a.join(" ")), warn: () => {}, info: () => {} },
    ui: { showWarning: async (w) => { errors.push(w); } },
    documents: { idOf: (p) => pathToFileURL(p).toString(), get: () => ({ path: documentPath, isDirty: false, revision: 1, getText: () => text }) },
    settings: { section: () => ({ get: (_k, fallback) => fallback }) },
    // Stand-in for the VS Code git extension's getConfig("user.name"): one git process, value discarded.
    vcs: { userName: timed("gitUserName", () => new Promise((r) => execFile("git", ["config", "--get", "user.name"], { cwd: runDir }, () => r("Reader")))) },
    paths: { userName: () => "Reader" },
    watcher: { watch: () => ({ onDidCreate: () => ({ dispose() {} }), onDidChange: () => ({ dispose() {} }), onDidDelete: () => ({ dispose() {} }), dispose() {} }) },
  };
  const documentsGet = host.documents.get;
  host.documents.get = (id) => (id === pathToFileURL(documentPath).toString() ? documentsGet() : undefined);
  const manager = { host, sessions: () => new Set() };
  const controller = new CommentsController(manager);
  const preview = {
    disposed: false, documentUri: pathToFileURL(documentPath).toString(),
    stage: { activeDocumentPath: documentPath, activeDocumentIdentity: documentId, activeDocumentRevision: 1, requestId: 1 },
    comments: createCommentsState(), probe: { commentPosts: 0 },
    postToPage: async (message) => {
      hostLog.push(["post:" + message.type, performance.now()]);
      posted.push(message);
      await page.evaluate((m) => window.postMessage(m, "*"), message);
    },
  };
  const routes = new Map();
  controller.register({ on: (type, handler) => routes.set(type, handler) });
  const creations = [];
  await page.exposeFunction("__toHost", async (message) => {
    const handler = routes.get(message.type);
    if (!handler) return;
    const start = performance.now(), from = hostLog.length;
    await handler(message, preview);
    const log = hostLog.slice(from);
    const at = (n) => { const e = log.find((x) => x[0] === n); return e ? e[1] - start : null; };
    const steps = {};
    for (const [name, ms] of log) if (!name.startsWith("post:")) steps[name] = (steps[name] || 0) + ms;
    creations.push({ total: performance.now() - start, toComments: at("post:previewComments"), toResult: at("post:previewCommentResult"), steps });
  });
  await context.addInitScript((blocked) => {
    const add = EventTarget.prototype.addEventListener;
    EventTarget.prototype.addEventListener = function (type, ...a) {
      if (blocked.includes(type) && (this === document || this === window)) return undefined;
      return add.call(this, type, ...a);
    };
    let state;
    window.acquireVsCodeApi = () => ({
      postMessage: (m) => { if (String(m.type).startsWith("previewComment")) window.__toHost(JSON.parse(JSON.stringify(m))); },
      getState: () => state, setState: (s) => { state = s; },
    });
  }, spec.block || []);
  await page.goto(pathToFileURL(built.file).toString(), { waitUntil: "load" });
  await page.evaluate(async () => { await Promise.all([...document.images].map((i) => i.decode().catch(() => {}))); });
  await sleep(600);
  await controller["post"](preview);
  await sleep(600);
  if (spec.edit) {
    await page.evaluate(() => document.querySelector("[data-sphinx-preview-edit-toggle]").click());
    await sleep(600);
    const on = await page.evaluate(() => document.querySelector("[data-sphinx-preview-edit-toggle]").getAttribute("data-edit-mode"));
    if (on !== "on") errors.push("edit mode not on: " + on);
  }
  const facts = await page.evaluate(() => ({
    elements: document.getElementsByTagName("*").length,
    dataLine: document.querySelectorAll("[data-line]").length,
    mapped: document.querySelectorAll("[data-sphinx-source-file][data-sphinx-source-line]").length,
    tables: document.querySelectorAll("#sphinx-myst-preview-content table").length,
    rows: [...document.querySelectorAll("#sphinx-myst-preview-content table")].filter((t) => !t.closest("[data-okf-properties]")).reduce((n, t) => n + t.rows.length, 0),
    images: [...document.images].filter((i) => i.naturalWidth > 0).length,
    marks: document.querySelectorAll("mark[data-okf-comment-thread]").length,
    orphans: document.querySelectorAll("[data-okf-comment-orphan]").length,
    badges: document.querySelectorAll("[data-okf-comment-badge]").length,
    height: document.documentElement.scrollHeight,
    styled: getComputedStyle(document.querySelector("#sphinx-myst-preview-content table") || document.body).borderCollapse,
  }));
  const cdp = await context.newCDPSession(page);
  if (THROTTLE > 1) await cdp.send("Emulation.setCPUThrottlingRate", { rate: THROTTLE });
  return { context, page, facts, errors, posted, creations, preview, controller };
}

/** Client points for a text drag (consecutive list items / paragraphs) or a table drag. */
async function target(page, kind, skip = 0) {
  return page.evaluate(({ kind, skip }) => {
    const content = document.getElementById("sphinx-myst-preview-content");
    const point = (el, atEnd) => {
      const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
      let node, found;
      while ((node = walker.nextNode())) if (node.data.trim()) { found = node; if (!atEnd) break; }
      const range = document.createRange();
      const at = atEnd ? Math.max(0, found.data.length - 2) : 1;
      range.setStart(found, at); range.setEnd(found, at + 1);
      const r = range.getBoundingClientRect();
      return { x: r.left + 1, y: r.top + r.height / 2 };
    };
    let first, last;
    if (kind === "table") {
      const tables = [...content.querySelectorAll("table")].filter((t) => !t.closest("[data-okf-properties]"));
      if (!tables.length) return null;
      const table = tables[Math.min(2, tables.length - 1)];
      window.scrollTo(0, table.getBoundingClientRect().top + scrollY - 160);
      first = table.rows[1].cells[0]; last = table.rows[table.rows.length - 1].cells[table.rows[0].cells.length - 1];
    } else {
      const all = [...content.querySelectorAll("li, p")].filter((e) => !e.closest("table, [data-okf-properties]") && e.textContent.trim().length > 20);
      let best;
      for (let i = Math.min(skip, all.length - 1); i < all.length; i += 1) {
        const top = all[i].getBoundingClientRect().top;
        let j = i;
        while (j + 1 < all.length && all[j + 1].getBoundingClientRect().bottom - top < 520) j += 1;
        const span = all[j].getBoundingClientRect().bottom - top;
        if (!best || span > best.span) best = { i, j, span };
        if (span > 200) break;
      }
      window.scrollTo(0, all[best.i].getBoundingClientRect().top + scrollY - 160);
      first = all[best.i]; last = all[best.j];
    }
    return { from: point(first, false), to: point(last, true) };
  }, { kind, skip });
}

const selectionInfo = (page) => page.evaluate(() => ({ length: String(getSelection()).length, button: !!document.querySelector("[data-okf-comment-create]") }));
const clearSelection = async (page) => { await page.evaluate(() => { getSelection().removeAllRanges(); }); await sleep(150); };

async function traced(browser, page, steps, action) {
  await browser.startTracing(page, { categories: ["devtools.timeline", "disabled-by-default-devtools.timeline", "toplevel", "blink", "v8.execute"] });
  let extra, buffer;
  try { extra = await action(); } finally { buffer = await browser.stopTracing(); }
  return { steps, ...analyse(buffer), ...(extra || {}) };
}

const pace = () => sleep(THROTTLE > 1 ? 90 : 30);

async function drag(browser, page, t, steps) {
  await sleep(250);
  await page.mouse.move(t.from.x, t.from.y);
  await page.mouse.down();
  await pace();
  return traced(browser, page, steps, async () => {
    const wall = performance.now();
    let input = 0;
    for (let k = 1; k <= steps; k += 1) {
      const s = performance.now();
      await page.mouse.move(t.from.x + ((t.to.x - t.from.x) * k) / steps, t.from.y + ((t.to.y - t.from.y) * k) / steps);
      input += performance.now() - s;
      await pace();
    }
    await sleep(150);
    return { inputRoundTrip: input / steps, wall: performance.now() - wall, selection: await selectionInfo(page) };
  });
}

async function scenarios(browser, run) {
  const { page } = run;
  const out = {};
  const want = (n) => wanted.includes(n);
  const text = await target(page, "text", 12);
  if (want("drag-text") && text) {
    out["drag-text"] = await drag(browser, page, text, 40);
    await page.mouse.up(); await clearSelection(page);
  }
  const table = await target(page, "table");
  if (table && (want("drag-table") || want("release"))) {
    const result = await drag(browser, page, table, 40);
    if (want("drag-table")) out["drag-table"] = result;
    if (want("release")) {
      out.release = await traced(browser, page, 1, async () => { await page.mouse.up(); await sleep(300); return { selection: await selectionInfo(page) }; });
    } else await page.mouse.up();
    await clearSelection(page);
  }
  if (want("drag-scroll")) {
    await page.evaluate(() => window.scrollTo(0, 250)); await sleep(250);
    await page.mouse.move(300, 300); await page.mouse.down(); await page.mouse.move(320, 700); await pace();
    out["drag-scroll"] = await traced(browser, page, 30, async () => {
      for (let k = 0; k < 30; k += 1) {
        await page.mouse.wheel(0, 160); await pace();
        await page.mouse.move(320 + (k % 5) * 60, 700 + (k % 3) * 12); await pace();
      }
      await sleep(150);
      return { selection: await selectionInfo(page), scrollY: await page.evaluate(() => scrollY) };
    });
    await page.mouse.up(); await clearSelection(page);
  }
  if (want("hover") && (table || text)) {
    const t = await target(page, table ? "table" : "text", 12);
    await sleep(250);
    out.hover = await traced(browser, page, 40, async () => {
      for (let k = 1; k <= 40; k += 1) {
        await page.mouse.move(t.from.x + ((t.to.x - t.from.x) * k) / 40, t.from.y + ((t.to.y - t.from.y) * k) / 40);
        await pace();
      }
      await sleep(150);
    });
  }
  // Selection changes with the pointer up: the path where the selectionchange handler does its full work.
  for (const [name, large] of [["extend-cell", false], ["extend-large", true]]) {
    if (!want(name)) continue;
    const ok = await page.evaluate((large) => {
      const content = document.getElementById("sphinx-myst-preview-content");
      const blocks = [...content.querySelectorAll("td[data-line], th[data-line], tr[data-line] td, li, p")].filter((e) => !e.closest("[data-okf-properties]") && e.textContent.trim().length > 30);
      const from = blocks[large ? 0 : Math.floor(blocks.length / 2)];
      const to = large ? blocks[Math.floor(blocks.length * 0.9)] : from;
      const firstText = (el) => { const w = document.createTreeWalker(el, NodeFilter.SHOW_TEXT); let n; while ((n = w.nextNode())) if (n.data.trim().length > 2) return n; return null; };
      const a = firstText(from), b = firstText(to);
      if (!a || !b) return false;
      to.scrollIntoView({ block: "center" });
      getSelection().setBaseAndExtent(a, 0, b, 2);
      return true;
    }, large);
    if (!ok) continue;
    await sleep(300);
    out[name] = await traced(browser, page, 30, async () => {
      for (let k = 0; k < 30; k += 1) { await page.evaluate(() => getSelection().modify("extend", "forward", "word")); await pace(); }
      await sleep(150);
      return { selection: await selectionInfo(page) };
    });
    await clearSelection(page);
  }
  if (want("keyboard") && text) {
    const t = await target(page, "text", 12);
    await sleep(200);
    await page.mouse.move(t.from.x, t.from.y); await page.mouse.down(); await page.mouse.move(t.from.x + 60, t.from.y, { steps: 3 }); await page.mouse.up();
    await sleep(250);
    const before = await selectionInfo(page);
    out.keyboard = await traced(browser, page, 30, async () => {
      for (let k = 0; k < 30; k += 1) { await page.keyboard.press("Shift+ArrowRight"); await pace(); }
      await sleep(150);
      return { before, selection: await selectionInfo(page) };
    });
    await clearSelection(page);
  }
  if (want("scroll-selected")) {
    // A large selection is already made (pointer up), then the wheel scrolls: every scroll re-reads it.
    await page.evaluate(() => {
      const content = document.getElementById("sphinx-myst-preview-content");
      const blocks = [...content.querySelectorAll("li, p, td")].filter((e) => !e.closest("[data-okf-properties]") && e.textContent.trim().length > 30);
      const firstText = (el) => { const w = document.createTreeWalker(el, NodeFilter.SHOW_TEXT); let n; while ((n = w.nextNode())) if (n.data.trim().length > 2) return n; return null; };
      window.scrollTo(0, 400);
      getSelection().setBaseAndExtent(firstText(blocks[0]), 0, firstText(blocks[Math.floor(blocks.length * 0.9)]), 2);
    });
    await page.mouse.move(600, 450); await sleep(400);
    out["scroll-selected"] = await traced(browser, page, 30, async () => {
      for (let k = 0; k < 30; k += 1) { await page.mouse.wheel(0, k < 15 ? 160 : -160); await pace(); await pace(); }
      await sleep(150);
      return { selection: await selectionInfo(page) };
    });
    await clearSelection(page);
  }
  if (want("tripleclick") && table) {
    const t = await target(page, "table");
    await sleep(250);
    out.tripleclick = await traced(browser, page, 1, async () => {
      await page.mouse.click(t.from.x + 3, t.from.y, { clickCount: 3 });
      await sleep(300);
      return { selection: await selectionInfo(page) };
    });
    await clearSelection(page);
  }
  if (want("create")) {
    const samples = [];
    for (let n = 0; n < 3; n += 1) {
      const t = await page.evaluate((n) => {
        const content = document.getElementById("sphinx-myst-preview-content");
        const host = [...content.querySelectorAll("td")].filter((c) => !c.closest("[data-okf-properties]") && !c.querySelector("mark") && c.textContent.trim().length > 40);
        const els = host.length ? host : [...content.querySelectorAll("li, p")].filter((c) => !c.querySelector("mark") && c.textContent.trim().length > 40);
        const el = els[Math.floor((els.length * (n + 1)) / 5)];
        if (!el) return null;
        el.scrollIntoView({ block: "center" });
        const w = document.createTreeWalker(el, NodeFilter.SHOW_TEXT); let node; while ((node = w.nextNode()) && node.data.trim().length < 20);
        const r = document.createRange(); r.setStart(node, 1); r.setEnd(node, 2); const a = r.getBoundingClientRect(); r.setStart(node, 11); r.setEnd(node, 12); const b = r.getBoundingClientRect();
        return { from: { x: a.left, y: a.top + a.height / 2 }, to: { x: b.left, y: b.top + b.height / 2 } };
      }, n);
      if (!t) break;
      await sleep(200);
      await page.mouse.move(t.from.x, t.from.y); await page.mouse.down(); await page.mouse.move(t.to.x, t.to.y, { steps: 4 }); await page.mouse.up();
      await sleep(250);
      if (!(await page.$("[data-okf-comment-create]"))) { samples.noButton = (await selectionInfo(page)).length; break; }
      const open = await traced(browser, page, 1, async () => { await page.click("[data-okf-comment-create]"); await sleep(250); });
      await page.fill("[data-okf-comment-compose-input]", "Lorem ipsum review comment " + n);
      await page.evaluate(() => {
        window.__latency = undefined;
        const before = document.querySelectorAll("mark[data-okf-comment-thread], [data-okf-comment-badge]").length;
        let start;
        document.querySelector("[data-okf-comment-compose-save]").addEventListener("pointerdown", () => { start = performance.now(); }, { once: true });
        const seen = new MutationObserver(() => {
          if (document.querySelector("[data-okf-comment-compose]")) return;
          if (document.querySelectorAll("mark[data-okf-comment-thread], [data-okf-comment-badge]").length <= before) return;
          seen.disconnect();
          const done = performance.now();
          requestAnimationFrame(() => setTimeout(() => { window.__latency = { toDom: done - start, toFrame: performance.now() - start }; }, 0));
        });
        seen.observe(document.body, { childList: true, subtree: true });
      });
      await sleep(200);
      const from = run.creations.length;
      const save = await traced(browser, page, 1, async () => {
        await page.click("[data-okf-comment-compose-save]");
        await page.waitForFunction(() => window.__latency, null, { timeout: 20000 });
        await sleep(300);
      });
      samples.push({ open, save, latency: await page.evaluate(() => window.__latency), host: run.creations[from], marks: await page.evaluate(() => document.querySelectorAll("mark[data-okf-comment-thread]").length) });
    }
    if (samples.noButton !== undefined) out.createNoButton = { steps: 1, events: {}, busy: 0, selection: { length: samples.noButton } };
    out.create = samples;
  }
  if (want("repost")) {
    await clearSelection(page);
    const last = [...run.posted].reverse().find((m) => m.type === "previewComments");
    if (last) {
      await page.evaluate(() => { window.__comments = []; window.scrollTo(0, 2000); });
      await sleep(300);
      out.repost = await traced(browser, page, 10, async () => {
        for (let k = 0; k < 10; k += 1) { await page.evaluate((m) => window.postMessage(m, "*"), last); await sleep(THROTTLE > 1 ? 400 : 150); }
        return { split: await page.evaluate(() => window.__comments), threads: last.threads.length };
      });
    }
  }
  return out;
}

(async () => {
  const browser = await chromium.launch({ headless: true }); // headless shell, as test/visual uses
  const results = { tag, throttle: THROTTLE, reps: REPS, chromium: browser.version(), started: new Date().toISOString(), runs: [] };
  const file = path.join(here, "results", `${resultName}.json`);
  fs.mkdirSync(path.dirname(file), { recursive: true });
  try {
    for (let rep = 0; rep < REPS; rep += 1) {
      // Variants interleaved, rotated each repetition, so drifting machine load spreads over all of them.
      const order = names.map((_, i) => names[(i + (rep + OFFSET) * 3) % names.length]);
      for (const variant of order) {
        const run = await openPage(browser, variant, path.join(here, "runs", resultName, variant));
        try {
          const out = await scenarios(browser, run);
          results.runs.push({ rep, variant, facts: run.facts, errors: run.errors.slice(0, 5), scenarios: out });
        } catch (error) {
          results.runs.push({ rep, variant, facts: run.facts, errors: [...run.errors.slice(0, 5), String(error.stack || error)] });
          console.error(variant, rep, String(error));
        } finally { await run.context.close(); }
        fs.writeFileSync(file, JSON.stringify(results));
        console.log(rep, variant, new Date().toISOString());
      }
    }
  } finally { await browser.close(); }
  results.finished = new Date().toISOString();
  fs.writeFileSync(file, JSON.stringify(results));
})().catch((error) => { console.error(error); process.exit(1); });

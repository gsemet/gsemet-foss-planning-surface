// Verifier probe of CR-517, independent of the change's own tests.
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

const [baseJs, headJs] = process.argv.slice(2).map((file) => fs.readFileSync(file, "utf8"));
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

const setup = () => {
  const log = [];
  const comments = window.CT.installCommentThreads(document, window,
    { reply: () => undefined, resolve: () => undefined, remove: () => undefined },
    (event, detail) => log.push(event + ": " + detail));
  const dump = (node) => node.nodeType === 3 ? node.nodeValue : node.nodeType !== 1 ? "#" + node.nodeType
    : [node.tagName, [...node.attributes].map((a) => [a.name, a.value]).sort((a, b) => a[0].localeCompare(b[0])),
      [...node.childNodes].map(dump), "value" in node && node.tagName === "TEXTAREA" ? node.value : undefined];
  const geometry = () => {
    const parts = [];
    document.querySelectorAll("[data-line], [data-sphinx-source-line]").forEach((element, index) => {
      const r = element.getBoundingClientRect();
      const tops = new Set();
      const walker = document.createTreeWalker(element, NodeFilter.SHOW_TEXT);
      for (let node = walker.nextNode(); node; node = walker.nextNode()) {
        if (!node.nodeValue.trim()) continue;
        const range = document.createRange();
        range.selectNodeContents(node);
        // The vertical middle of each line box: stable across inline boxes of different heights.
        for (const box of range.getClientRects()) if (box.width > 0) tops.add(Math.round(box.top + window.scrollY));
      }
      const f = (v) => Math.round(v * 100) / 100;
      parts.push([index, f(r.top + window.scrollY), f(r.height), [...tops].sort((a, b) => a - b).join(",")].join("|"));
    });
    return parts;
  };
  const pristine = [...document.querySelectorAll("[data-line]")].map((element) => element.cloneNode(true));
  window.__v = {
    log,
    step(action) {
      if (action.patch !== undefined) {
        // As a content patch does: one block is brought anew, comment elements next to it are dropped, apply().
        const blocks = [...document.querySelectorAll("[data-line]")];
        const old = blocks[action.patch % blocks.length];
        const index = blocks.indexOf(old);
        const detached = blocks.length !== pristine.length;
        while (old.nextElementSibling?.matches("[data-okf-comment-badge]")) old.nextElementSibling.remove();
        old.replaceWith(pristine[index].cloneNode(true));
        comments.apply();
        return { patched: !detached };
      }
      const before = geometry();
      let moved;
      if (action.hide !== undefined) {
        if (action.hide) document.documentElement.setAttribute("data-sphinx-preview-comments", "off");
        else document.documentElement.removeAttribute("data-sphinx-preview-comments");
        comments.visibilityChanged();
        return {};
      }
      if (action.open !== undefined) {
        const opened = comments.openThread(action.open);
        const input = document.querySelector("[data-okf-comment-reply-input]");
        if (input) input.value = "draft " + action.open;
        if (action.ask) document.querySelector("[data-okf-comment-delete]")?.click();
        return { opened };
      }
      if (action.apply) { comments.apply(); return {}; }
      moved = comments.setThreads(action.threads);
      const after = geometry();
      const changed = after.filter((row, i) => row !== before[i]);
      return { moved, changed: changed.length + Math.abs(after.length - before.length), sample: changed.slice(0, 3),
        was: before.filter((row, i) => row !== after[i]).slice(0, 3) };
    },
    dump: () => JSON.stringify(dump(document.documentElement)),
    candidates: () => [...document.querySelectorAll("[data-line]")].map((element) => {
      const texts = [];
      const walker = document.createTreeWalker(element, NodeFilter.SHOW_TEXT);
      for (let node = walker.nextNode(); node; node = walker.nextNode()) if (node.nodeValue.trim().length > 1) texts.push(node.nodeValue);
      return { line: Number(element.getAttribute("data-line")), tag: element.tagName, texts, all: element.textContent };
    }),
  };
};

let seed = Number(process.env.SEED || 20261127);
const random = (below) => { seed = (seed * 48271) % 2147483647; return seed % below; };

function makePool(candidates, size) {
  const pool = [];
  const focus = Array.from({ length: 14 }, () => candidates[random(candidates.length)]);
  for (let i = 0; i < size; i += 1) {
    const block = random(3) ? focus[random(focus.length)] : candidates[random(candidates.length)];
    const source = random(4) === 0 || !block.texts.length ? block.all : block.texts[random(block.texts.length)];
    const from = random(Math.max(1, source.length - 2));
    let quote = source.slice(from, from + 2 + random(random(3) ? 14 : 60));
    const kind = random(20);
    let line = block.line;
    if (kind === 0) quote = "";
    else if (kind === 1) quote = "nowhere to be found " + i;
    else if (kind === 2) line = 99999;
    else if (kind === 3) quote = quote.replace(/\s+/g, "  ");
    const thread = {
      id: "t" + i, anchor: { line, endLine: line, quote, prefix: "", suffix: "" }, resolved: random(5) === 0,
      createdAt: "2026-11-27T10:00:00Z",
      comments: [{ id: "c" + i, author: "Ada", createdAt: "2026-11-27T10:00:00Z", body: "Body " + i }],
    };
    const verdict = random(10);
    if (verdict < 4) thread.orphaned = false; else if (verdict === 4) thread.orphaned = true;
    pool.push(thread);
  }
  return pool;
}

(async () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "verifier517-diff-"));
  const browser = await chromium.launch();
  const totals = { lists: 0, mismatches: 0, geometryMoved: 0, answeredTrue: 0, answeredFalse: 0, missed: 0, trueWithoutMove: 0,
    popoverLists: 0, hiddenLists: 0, applies: 0, maxMarks: 0, maxBadges: 0, maxOrphans: 0 };
  const misses = [];
  try {
    console.log("chromium", browser.version(), "runs per page", RUNS, "steps", STEPS, "seed", seed);
    for (const doc of docs.filter((d) => (process.env.DOCS || "rich,readme,contributing").split(",").includes(d.name))) {
      for (const width of [420, 900]) {
        const url = await render(doc, root, width);
        const here = { lists: 0, mismatches: 0, missed: 0, geometryMoved: 0 };
        for (let run = 0; run < (doc.name === "rich" ? RUNS * 3 : RUNS); run += 1) {
          const pages = [];
          for (const source of [baseJs, headJs]) {
            const page = await browser.newPage({ viewport: { width, height: 800 }, bypassCSP: true });
            await page.goto(url);
            await page.evaluate(source + ";window.CT = CT;");
            await page.evaluate(`(${setup.toString()})()`);
            await page.evaluate(() => document.fonts.ready);
            pages.push(page);
          }
          const [base, head] = pages;
          const pool = makePool(await head.evaluate(() => window.__v.candidates()), 60);
          let list = [], hidden = false, popover = false;
          for (let step = 0; step < STEPS; step += 1) {
            const change = list.length < 5 ? 0 : random(17);
            const at = random(list.length || 1);
            const candidate = pool[random(pool.length)];
            let action;
            if (change <= 2) { if (!list.some((t) => t.id === candidate.id)) list.splice(change === 0 ? list.length : at, 0, candidate); }
            else if (change === 3 || change === 4) list.splice(at, 1);
            else if (change === 5) list = list.map((t, i) => i === at ? { ...t, resolved: !t.resolved } : t);
            else if (change === 6) list = list.map((t, i) => i === at ? { ...t, comments: [...t.comments, { id: "r" + step, author: "Bo", createdAt: "", body: "Reply" }] } : t);
            else if (change === 7) list = list.map((t, i) => i === at ? { ...candidate, id: t.id } : t);
            else if (change === 8) list = [...list.slice(at), ...list.slice(0, at)];
            else if (change === 9) { hidden = !hidden; action = { hide: hidden }; }
            else if (change === 10 || change === 11) action = { open: list[at].id, ask: change === 11 };
            else if (change === 12) { if (random(3) === 0) action = { apply: true }; else if (random(6) === 0) list = []; }
            else if (change >= 14) action = { patch: random(100000) };
            // change 13 and what falls through: the same list again, or the edited list.
            action ??= { threads: list };
            const results = [await base.evaluate((a) => window.__v.step(a), action), await head.evaluate((a) => window.__v.step(a), action)];
            if (action.open !== undefined) popover = results[1].opened;
            if (action.apply) totals.applies += 1;
            if (action.patch !== undefined) totals.patches = (totals.patches || 0) + 1;
            const [a, b] = [await base.evaluate(() => window.__v.dump() + JSON.stringify(window.__v.log)),
              await head.evaluate(() => window.__v.dump() + JSON.stringify(window.__v.log))];
            if (a !== b) {
              totals.mismatches += 1; here.mismatches += 1;
              if (totals.mismatches <= 5) {
                let i = 0; while (a[i] === b[i]) i += 1;
                console.log("MISMATCH", doc.name, width, run, step, JSON.stringify(action).slice(0, 300), "\n base", a.slice(i - 150, i + 150), "\n head", b.slice(i - 150, i + 150));
              }
              break;
            }
            if (action.threads) {
              const r = results[1];
              totals.lists += 1; here.lists += 1;
              if (hidden) totals.hiddenLists += 1;
              if (popover && await head.evaluate(() => !!document.querySelector("[data-okf-comment-popover]"))) totals.popoverLists += 1;
              if (r.moved) totals.answeredTrue += 1; else totals.answeredFalse += 1;
              if (r.changed) { totals.geometryMoved += 1; here.geometryMoved += 1; }
              if (r.moved && !r.changed) totals.trueWithoutMove += 1;
              if (!r.moved && r.changed) {
                totals.missed += 1; here.missed += 1;
                if (misses.length < 8) misses.push({ doc: doc.name, width, run, step, hidden, changed: r.changed, was: r.was, now: r.sample });
              }
              const counts = await head.evaluate(() => ["thread", "badge", "orphan"].map((k) => document.querySelectorAll(`[data-okf-comment-${k}]`).length));
              totals.maxMarks = Math.max(totals.maxMarks, counts[0]); totals.maxBadges = Math.max(totals.maxBadges, counts[1]); totals.maxOrphans = Math.max(totals.maxOrphans, counts[2]);
            }
          }
          for (const page of pages) await page.close();
        }
        console.log(doc.name, width, JSON.stringify(here));
      }
    }
  } finally {
    await browser.close();
    fs.rmSync(root, { recursive: true, force: true, maxRetries: 5 });
  }
  console.log("totals", JSON.stringify(totals));
  for (const miss of misses) console.log("missed move", JSON.stringify(miss));
})().catch((error) => { console.error(error); process.exit(1); });

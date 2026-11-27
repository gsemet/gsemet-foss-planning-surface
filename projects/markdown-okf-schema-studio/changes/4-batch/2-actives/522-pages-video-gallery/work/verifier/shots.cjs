// Verifier's pictures at the head: the built videos.html (posters, nothing playing) and the README
// sections that hold the five GIFs, rendered from README.md with markdown-it so that each GIF stays an
// image (GitHub's own rendering is not used: nothing is sent to an outside service).
// Usage: node shots.cjs <worktree> <evidence folder>
const http = require("node:http");
const fs = require("node:fs");
const path = require("node:path");
const [repoArgument, out] = process.argv.slice(2);
const repo = path.resolve(repoArgument);
const { chromium } = require(path.join(repo, "node_modules", "playwright-core"));
const MarkdownIt = require(path.join(repo, "node_modules", "markdown-it"));
const site = path.join(repo, "out", "site");
const TYPES = { ".html": "text/html; charset=utf-8", ".css": "text/css", ".js": "text/javascript", ".png": "image/png", ".gif": "image/gif", ".svg": "image/svg+xml", ".webm": "video/webm", ".mp4": "video/mp4" };
const readme = `<!doctype html><meta charset="utf-8"><title>README</title><style>
body{margin:0;background:#fff;color:#1f2328;font:16px/1.5 "Segoe UI",sans-serif}
main{width:880px;margin:0 auto;padding:24px}img{max-width:100%}
h1,h2{border-bottom:1px solid #d1d9e0;padding-bottom:.3em}
pre{background:#f6f8fa;padding:12px;overflow:auto;font:13.6px/1.45 Consolas,monospace}code{font-family:Consolas,monospace;font-size:.9em}
table{border-collapse:collapse}td,th{border:1px solid #d1d9e0;padding:6px 13px}a{color:#0969da}</style>
<main>${new MarkdownIt({ html: true }).render(fs.readFileSync(path.join(repo, "README.md"), "utf8"))}</main>`;

const server = http.createServer((request, response) => {
  const pathname = decodeURIComponent(new URL(request.url, "http://x").pathname);
  if (pathname === "/readme/") {
    response.writeHead(200, { "content-type": TYPES[".html"] }).end(readme);
    return;
  }
  // /readme/<path> reads the repository's docs/ and images/ only; everything else is the built site.
  const [root, rest] = pathname.startsWith("/readme/") ? [repo, pathname.slice(8)] : [site, pathname.slice(1)];
  const file = path.join(root, path.normalize(rest));
  const allowed = root === site || /^(docs|images)\//.test(rest);
  if (!allowed || !file.startsWith(root + path.sep) || !fs.existsSync(file) || !fs.statSync(file).isFile()) {
    response.writeHead(404).end();
    return;
  }
  response.writeHead(200, { "content-type": TYPES[path.extname(file)] ?? "application/octet-stream", "content-length": fs.statSync(file).size });
  fs.createReadStream(file).pipe(response);
});

// Section, picture name, how long to wait so that the section's GIFs have moved on from frame 0.
const SECTIONS = [
  ["readme-raw-markdown", "Highest respect for the raw Markdown"],
  ["readme-edit-myst", "Edit MyST visually"],
  ["readme-diff", "See what changed since the last commit"],
  ["readme-radio", "Decide in the page: choices in your plans"],
];

(async () => {
  await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
  const base = `http://127.0.0.1:${server.address().port}`;
  const browser = await chromium.launch();
  try {
    const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
    const requests = [];
    const failed = [];
    page.on("request", (r) => requests.push(new URL(r.url()).pathname));
    page.on("response", (r) => { if (r.status() >= 400) failed.push(`${r.status()} ${new URL(r.url()).pathname}`); });
    await page.goto(`${base}/videos.html`, { waitUntil: "networkidle" });
    await page.waitForTimeout(2500);
    await page.screenshot({ path: path.join(out, "videos-page-top.png") });
    await page.screenshot({ path: path.join(out, "videos-page.png"), fullPage: true });
    const state = await page.evaluate(() => [...document.querySelectorAll("video")].map((v) => v.paused && v.readyState === 0));
    console.log(`videos-page-top.png, videos-page.png: ${state.length} videos, ${state.filter(Boolean).length} paused and unloaded at capture; video requests ${requests.filter((p) => /\.(webm|mp4)$/.test(p)).length}; failed ${failed.join(", ") || "none"}`);
    for (const [name, title] of SECTIONS) {
      failed.length = 0;
      await page.goto(`${base}/readme/`, { waitUntil: "load" });
      await page.waitForTimeout(7000);
      const found = await page.evaluate((wanted) => {
        const headings = [...document.querySelectorAll("h2, h3")];
        const start = headings.find((h) => h.textContent.trim() === wanted);
        const next = headings[headings.indexOf(start) + 1];
        const main = document.querySelector("main").getBoundingClientRect();
        const y = start.getBoundingClientRect().top + window.scrollY - 12;
        const end = next.getBoundingClientRect().top + window.scrollY - 8;
        const images = [...document.querySelectorAll("img")].filter((i) => { const t = i.getBoundingClientRect().top + window.scrollY; return t > y && t < end; })
          .map((i) => `${i.getAttribute("src").split("/").pop()} ${i.complete && i.naturalWidth > 0 ? `${i.naturalWidth}x${i.naturalHeight}` : "BROKEN"}`);
        return { clip: { x: main.left, y, width: main.width, height: end - y }, images };
      }, title);
      await page.screenshot({ path: path.join(out, `${name}.png`), fullPage: true, clip: found.clip, animations: "allow" });
      console.log(`${name}.png "${title}" ${Math.round(found.clip.width)}x${Math.round(found.clip.height)}: ${found.images.join(", ")}; failed ${failed.join(", ") || "none"}`);
    }
  } finally {
    await browser.close();
    server.closeAllConnections();
    server.close();
  }
})().catch((error) => { console.error(error); process.exit(1); });

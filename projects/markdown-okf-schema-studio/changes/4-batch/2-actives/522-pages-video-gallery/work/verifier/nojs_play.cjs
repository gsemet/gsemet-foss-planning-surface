// With scripts disabled, does the browser's own play button start a card of the built videos.html?
// Usage: node nojs_play.cjs <worktree>
const http = require("node:http");
const fs = require("node:fs");
const path = require("node:path");
const [repo] = process.argv.slice(2);
const { chromium } = require(path.join(repo, "node_modules", "playwright-core"));
const site = path.join(repo, "out", "site");
const TYPES = { ".html": "text/html; charset=utf-8", ".png": "image/png", ".svg": "image/svg+xml", ".webm": "video/webm", ".mp4": "video/mp4" };
let log = [];
const server = http.createServer((request, response) => {
  const pathname = decodeURIComponent(new URL(request.url, "http://x").pathname);
  log.push(pathname);
  const file = path.join(site, path.normalize(pathname));
  if (!file.startsWith(site + path.sep) || !fs.existsSync(file) || !fs.statSync(file).isFile()) return void response.writeHead(404).end();
  const size = fs.statSync(file).size;
  const range = /^bytes=(\d+)-(\d*)$/.exec(request.headers.range ?? "");
  const headers = { "content-type": TYPES[path.extname(file)] ?? "application/octet-stream", "accept-ranges": "bytes" };
  if (!range) { response.writeHead(200, { ...headers, "content-length": size }); return void fs.createReadStream(file).pipe(response); }
  const start = Number(range[1]);
  const end = range[2] ? Number(range[2]) : size - 1;
  response.writeHead(206, { ...headers, "content-range": `bytes ${start}-${end}/${size}`, "content-length": end - start + 1 });
  fs.createReadStream(file, { start, end }).pipe(response);
});
server.listen(0, "127.0.0.1", async () => {
  let failures = 0;
  for (const [label, launch] of [["chromium", {}], ["chrome", { channel: "chrome" }]]) {
    const browser = await chromium.launch(launch);
    const page = await (await browser.newContext({ viewport: { width: 1280, height: 900 }, javaScriptEnabled: false })).newPage();
    log = [];
    await page.goto(`http://127.0.0.1:${server.address().port}/videos.html`, { waitUntil: "networkidle" });
    const video = page.locator("figure#table-anchors video");
    await video.scrollIntoViewIfNeeded();
    await page.waitForTimeout(300);
    const box = await video.boundingBox();
    const videos = () => [...new Set(log.filter((p) => /\.(webm|mp4)$/.test(p)))];
    await page.mouse.click(box.x + box.width / 2, box.y + box.height / 2);
    await page.waitForTimeout(1200);
    const afterPicture = videos();
    await page.mouse.click(box.x + 24, box.y + box.height - 48);
    await page.waitForTimeout(1500);
    const state = await video.evaluate((v) => ({ paused: v.paused, time: Number(v.currentTime.toFixed(2)) }));
    const ok = afterPicture.length === 0 && videos().length === 1 && !state.paused && state.time > 0;
    if (!ok) failures += 1;
    console.log(`${ok ? "ok  " : "FAIL"} ${label} ${browser.version()} scripts disabled: after picture click requests ${JSON.stringify(afterPicture)}; after play button requests ${JSON.stringify(videos())} paused=${state.paused} t=${state.time}`);
    await browser.close();
  }
  console.log(`failures: ${failures}`);
  server.close();
  process.exitCode = failures ? 1 : 0;
});

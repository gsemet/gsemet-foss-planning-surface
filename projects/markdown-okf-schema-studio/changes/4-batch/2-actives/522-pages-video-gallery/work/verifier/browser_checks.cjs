// Verifier's own checks of the built out/site in real browsers, served on 127.0.0.1.
// Usage: node browser_checks.cjs <worktree>
const http = require("node:http");
const fs = require("node:fs");
const path = require("node:path");
const [repo] = process.argv.slice(2);
const { chromium } = require(path.join(repo, "node_modules", "playwright-core"));
const site = path.join(repo, "out", "site");
const TYPES = { ".html": "text/html; charset=utf-8", ".css": "text/css", ".js": "text/javascript", ".png": "image/png", ".gif": "image/gif", ".svg": "image/svg+xml", ".webm": "video/webm", ".mp4": "video/mp4", ".json": "application/json" };

let log = [];
const server = http.createServer((request, response) => {
  const pathname = decodeURIComponent(new URL(request.url, "http://x").pathname);
  log.push(pathname);
  const file = path.join(site, path.normalize(pathname));
  if (!file.startsWith(site + path.sep) || !fs.existsSync(file) || !fs.statSync(file).isFile()) {
    response.writeHead(404).end();
    return;
  }
  const size = fs.statSync(file).size;
  const range = /^bytes=(\d+)-(\d*)$/.exec(request.headers.range ?? "");
  const headers = { "content-type": TYPES[path.extname(file)] ?? "application/octet-stream", "accept-ranges": "bytes" };
  if (range) {
    const start = Number(range[1]);
    const end = range[2] ? Number(range[2]) : size - 1;
    response.writeHead(206, { ...headers, "content-range": `bytes ${start}-${end}/${size}`, "content-length": end - start + 1 });
    fs.createReadStream(file, { start, end }).pipe(response);
    return;
  }
  response.writeHead(200, { ...headers, "content-length": size });
  fs.createReadStream(file).pipe(response);
});

let failures = 0;
const check = (ok, message) => { console.log(`${ok ? "ok  " : "FAIL"} ${message}`); if (!ok) failures += 1; };
const isVideo = (p) => /\.(webm|mp4)$/.test(p);
const videoRequests = () => [...new Set(log.filter(isVideo))];
const sleep = (page, ms) => page.waitForTimeout(ms);

async function open(browser, base, options = {}) {
  const context = await browser.newContext({ viewport: { width: 1280, height: 900 }, ...options });
  const page = await context.newPage();
  const seen = [];
  const errors = [];
  const bad = [];
  page.on("request", (r) => seen.push(new URL(r.url()).pathname));
  page.on("pageerror", (e) => errors.push(e.message));
  page.on("response", (r) => { if (r.status() >= 400) bad.push(`${r.status()} ${new URL(r.url()).pathname}`); });
  log = [];
  await page.goto(`${base}/videos.html`, { waitUntil: "networkidle" });
  await sleep(page, 600);
  return { context, page, seen, errors, bad };
}

const state = (video) => video.evaluate((v) => ({ paused: v.paused, time: v.currentTime, ready: v.readyState, events: v.dataset.events ?? "" }));
const record = (video) => video.evaluate((v) => { for (const n of ["play", "pause"]) v.addEventListener(n, () => { v.dataset.events = `${v.dataset.events ?? ""} ${n}`.trim(); }); });
async function middle(page, video) {
  await video.scrollIntoViewIfNeeded();
  await sleep(page, 150);
  const box = await video.boundingBox();
  return { x: box.x + box.width / 2, y: box.y + box.height / 2, box };
}

async function run(label, launch, base) {
  let browser;
  try {
    browser = await chromium.launch(launch);
  } catch (error) {
    console.log(`== ${label}: cannot launch: ${error.message.split("\n")[0]}`);
    return;
  }
  try {
    console.log(`== ${label} ${browser.version()}`);
    // (2a) load, then scroll through the whole page: nothing of any video is requested, nothing plays.
    {
      const { context, page, seen, errors, bad } = await open(browser, base);
      const height = await page.evaluate(() => document.documentElement.scrollHeight);
      for (let y = 0; y <= height; y += 300) { await page.mouse.wheel(0, 300); await sleep(page, 80); }
      await sleep(page, 5000);
      const videos = await page.evaluate(() => [...document.querySelectorAll("video")].map((v) => ({ paused: v.paused, ready: v.readyState, time: v.currentTime, preload: v.preload, controls: v.controls, autoplay: v.autoplay, poster: v.getAttribute("poster") })));
      check(videos.length === 18, `18 video elements in the loaded page (${videos.length})`);
      check(videos.every((v) => v.paused && v.ready === 0 && v.time === 0), "every video paused, readyState 0, time 0, after load, a full scroll and 5 s");
      check(videos.every((v) => v.preload === "none" && v.controls && !v.autoplay && v.poster), "DOM: preload=none, controls, no autoplay, poster on each");
      check(videoRequests().length === 0 && !seen.some(isVideo), `no .webm/.mp4 request on load: server log ${JSON.stringify(videoRequests())}, page requests ${seen.filter(isVideo).length}`);
      const posters = [...new Set(log.filter((p) => p.endsWith("/poster.png")))];
      check(posters.length === 18, `the 18 posters were requested (${posters.length})`);
      check(bad.length === 0 && errors.length === 0, `no failed response ${JSON.stringify(bad)}, no page error ${JSON.stringify(errors)}`);
      console.log(`     canPlayType mp4/h264: ${await page.evaluate(() => document.createElement("video").canPlayType('video/mp4; codecs="avc1.64001F"') || "(none)")}`);
      await context.close();
    }
    // (2b) each card, on a fresh page: real mouse clicks in the middle of the picture.
    const probe = await open(browser, base);
    const ids = await probe.page.evaluate(() => [...document.querySelectorAll(".video-gallery figure")].map((f) => f.id));
    await probe.context.close();
    for (const id of ids) {
      const { context, page, errors } = await open(browser, base);
      const video = page.locator(`figure#${id} video`);
      const src = "/" + (await video.locator("source").getAttribute("src"));
      const before = videoRequests().length;
      await record(video);
      let at = await middle(page, video);
      const others = await page.evaluate(() => document.querySelectorAll("video").length);
      await page.mouse.click(at.x, at.y);
      await page.waitForFunction((i) => { const v = document.querySelector(`figure[id="${i}"] video`); return v.currentTime > 0.2 || v.error || v.networkState === 3; }, id, { timeout: 8000 }).catch(() => undefined);
      await sleep(page, 900);
      const one = await state(video);
      const asked = videoRequests();
      const playingOthers = await page.evaluate((i) => [...document.querySelectorAll("video")].filter((v) => v.closest("figure").id !== i && (!v.paused || v.readyState !== 0)).length, id);
      await page.mouse.click(at.x, at.y);
      await sleep(page, 1100);
      const two = await state(video);
      await page.mouse.click(at.x, at.y);
      await sleep(page, 1100);
      const three = await state(video);
      const ok = before === 0 && one.paused === false && one.time > 0 && one.events === "play"
        && asked.length === 1 && asked[0] === src && playingOthers === 0 && others === 18
        && two.paused === true && two.events === "play pause"
        && three.paused === false && three.events === "play pause play" && errors.length === 0;
      check(ok, `${id}: requests before click ${before}; click1 paused=${one.paused} t=${one.time.toFixed(2)} events="${one.events}" requested ${asked.map((a) => a.split("/").pop()).join(",") || "none"}; others touched ${playingOthers}; click2 paused=${two.paused} "${two.events}"; click3 paused=${three.paused} "${three.events}"; errors ${errors.length}`);
      await context.close();
    }
    // Space bar on a focused, unloaded video.
    for (const id of ["short-demo-01", "table-anchors"]) {
      const { context, page, errors } = await open(browser, base);
      const video = page.locator(`figure#${id} video`);
      await record(video);
      await video.focus();
      await page.keyboard.press("Space");
      await sleep(page, 1500);
      const one = await state(video);
      await page.keyboard.press("Space");
      await sleep(page, 800);
      const two = await state(video);
      check(!one.paused && one.time > 0 && one.events === "play" && two.paused && two.events === "play pause" && errors.length === 0, `space bar on ${id}: first paused=${one.paused} t=${one.time.toFixed(2)} "${one.events}"; second paused=${two.paused} "${two.events}"; errors ${errors.length}`);
      await context.close();
    }
    // The native play button of an unloaded video (bottom left of the controls).
    {
      const { context, page, errors } = await open(browser, base);
      const video = page.locator("figure#table-anchors video");
      await record(video);
      const { box } = await middle(page, video);
      let used = null;
      for (const dy of [48, 40, 56, 32, 24]) {
        await page.mouse.click(box.x + 24, box.y + box.height - dy);
        await sleep(page, 1200);
        if ((await state(video)).events) { used = dy; break; }
      }
      const one = await state(video);
      check(!one.paused && one.events === "play" && errors.length === 0, `native play button before load (x+24, bottom-${used}): paused=${one.paused} "${one.events}"`);
      await context.close();
    }
    // Known gap of the PR: pausing while the file is still loading.
    {
      const { context, page, errors } = await open(browser, base);
      await page.route("**/table-anchors.webm", () => undefined);
      const video = page.locator("figure#table-anchors video");
      await record(video);
      const at = await middle(page, video);
      await page.mouse.click(at.x, at.y);
      await sleep(page, 1200);
      const one = await state(video);
      await video.focus();
      await page.keyboard.press("Space");
      await sleep(page, 1200);
      const two = await state(video);
      console.log(`     pause while loading: after click "${one.events}" ready=${one.ready}; after space paused=${two.paused} "${two.events}"; page errors ${JSON.stringify(errors)}`);
      check(two.paused && errors.some((m) => /interrupted by a call to pause/.test(m)), "known gap reproduced: unhandled play() rejection");
      await context.close();
    }
    // CORE-098 known issue: scripts disabled.
    {
      const { context, page } = await open(browser, base, { javaScriptEnabled: false });
      const video = page.locator("figure#table-anchors video");
      const at = await middle(page, video);
      await page.mouse.click(at.x, at.y);
      await sleep(page, 1200);
      console.log(`     scripts disabled: after a click on the picture, video requests ${JSON.stringify(videoRequests())}`);
      check(videoRequests().length === 0, "without the script a click on the picture requests nothing");
      await context.close();
    }
    // The home page (the README): the five clips are looping, autoplaying videos.
    {
      const { context, page, errors, bad } = await open(browser, base);
      await page.goto(`${base}/index.html`, { waitUntil: "load" });
      await sleep(page, 2500);
      const home = await page.evaluate(() => [...document.querySelectorAll("video")].map((v) => ({ src: v.currentSrc.split("/").pop(), autoplay: v.autoplay, loop: v.loop, muted: v.muted, paused: v.paused, time: v.currentTime })));
      for (const v of home) console.log(`     index.html video ${v.src} autoplay=${v.autoplay} loop=${v.loop} muted=${v.muted} paused=${v.paused} t=${v.time.toFixed(1)}`);
      const five = ["table-anchors", "slash-menu-grid", "figure-editor", "diff-side-by-side", "radio-buttons"].map((c) => `${c}.webm`);
      check(JSON.stringify(home.map((v) => v.src)) === JSON.stringify(five) && home.every((v) => v.autoplay && v.loop && v.muted), "index.html: the five README clips are autoplay, loop, muted videos, in README order");
      for (const name of five) {
        const v = page.locator(`video:has(source[src$="${name}"])`);
        await v.scrollIntoViewIfNeeded();
        await sleep(page, 1200);
        const s = await state(v);
        check(!s.paused && s.time > 0, `index.html ${name} plays once in view: paused=${s.paused} t=${s.time.toFixed(1)}`);
      }
      const links = await page.evaluate(() => [...document.querySelectorAll("a")].filter((a) => a.textContent.trim() === "Videos").map((a) => a.getAttribute("href")));
      console.log(`     index.html links named Videos: ${links.join(" ")}`);
      check(errors.length === 0, `index.html: no page error ${JSON.stringify(errors)}; failed responses ${JSON.stringify(bad)}`);
      await context.close();
    }
  } finally {
    await browser.close();
  }
}

(async () => {
  await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
  const base = `http://127.0.0.1:${server.address().port}`;
  try {
    await run("Playwright Chromium", {}, base);
    await run("installed Google Chrome (headless)", { channel: "chrome" }, base);
    await run("installed Microsoft Edge (headless)", { channel: "msedge" }, base);
  } finally {
    server.closeAllConnections();
    server.close();
  }
  console.log(`\nfailures: ${failures}`);
  process.exit(failures ? 1 : 0);
})().catch((error) => { console.error(error); process.exit(1); });

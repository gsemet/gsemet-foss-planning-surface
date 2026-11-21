// Probe: two CDP connections to one page. A (the stress main page) emulates 1400x900. B (a scenario's own
// connection, like paste-url) emulates 1200x800 then disconnects. Does a real click through A still reach an
// out-of-process iframe afterwards? Usage: node emulation-probe.cjs <playwright-core dir> <variant>
const http = require("node:http");
const path = require("node:path");
const { spawn } = require("node:child_process");
const { chromium } = require(path.resolve(process.argv[2]));
const variant = process.argv[3] ?? "diff";
const frameHtml = `<body style="margin:0"><button id=b style="width:200px;height:60px">x</button><script>window.n=0;addEventListener("pointerdown",()=>window.n++,true)</script>`;
const mk = (html, port) => new Promise((r) => { const s = http.createServer((q, s2) => { s2.setHeader("content-type", "text/html"); s2.end(html); }); s.listen(port, "127.0.0.1", () => r(s)); });
(async () => {
  await mk(frameHtml, 8781);
  await mk(`<body style="margin:0"><script>window.m=0;addEventListener("pointerdown",()=>window.m++,true)</script><div style="height:100px"></div><iframe src="http://localhost:8781/" style="position:absolute;left:700px;top:60px;width:600px;height:300px;border:0"></iframe>`, 8780);
  const exe = require("node:fs").readdirSync(process.env.LOCALAPPDATA + "/ms-playwright").filter((d) => d.startsWith("chromium-")).sort()[0];
  const bin = path.join(process.env.LOCALAPPDATA, "ms-playwright", exe, "chrome-win64", "chrome.exe");
  const proc = spawn(bin, ["--remote-debugging-port=9333", "--user-data-dir=" + path.join(require("node:os").tmpdir(), "emu-probe-" + Date.now()), "--site-per-process", "--window-size=1500,1000", "--no-first-run", "http://127.0.0.1:8780/"], { stdio: "ignore" });
  await new Promise((r) => setTimeout(r, 4000));
  const A = await chromium.connectOverCDP("http://127.0.0.1:9333");
  const pa = A.contexts()[0].pages().find((p) => p.url().includes("8780"));
  await pa.setViewportSize({ width: 1400, height: 900 });
  const frameOf = () => pa.frames().find((f) => f.url().includes("8781"));
  const clicks = async (label) => {
    const before = await frameOf().evaluate(() => window.n);
    const mBefore = await pa.evaluate(() => window.m);
    await pa.mouse.click(1000, 150);
    await new Promise((r) => setTimeout(r, 500));
    const after = await frameOf().evaluate(() => window.n);
    const mAfter = await pa.evaluate(() => window.m);
    console.log(label, JSON.stringify({ inner: await pa.evaluate(() => [innerWidth, innerHeight]), frameClicks: after - before, mainClicks: mAfter - mBefore }));
  };
  await clicks("A alone (1400x900)");
  const B = await chromium.connectOverCDP("http://127.0.0.1:9333");
  const pb = B.contexts()[0].pages().find((p) => p.url().includes("8780"));
  if (variant === "diff") await pb.setViewportSize({ width: 1200, height: 800 });
  else if (variant === "same") await pb.setViewportSize({ width: 1400, height: 900 });
  await clicks("A while B emulates");
  await B.close();
  await new Promise((r) => setTimeout(r, 1000));
  await clicks("A after B closed");
  await clicks("A again");
  await A.close();
  proc.kill();
  process.exit(0);
})().catch((e) => { console.error(e); process.exit(1); });

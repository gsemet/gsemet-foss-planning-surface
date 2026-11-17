// usage: node spike.mjs <variant> '<settings-json>' <devPath...>   (env AGENTS=0 for a normal window)
import { spawn, spawnSync } from "node:child_process";
import fs from "node:fs"; import net from "node:net"; import path from "node:path";
import { createRequire } from "node:module";
import { setTimeout as delay } from "node:timers/promises";
const repo = "/Users/az02065/Projects/DevTools/markdown-okf-schema-studio";
const { chromium } = createRequire(path.join(repo, "package.json"))("playwright-core");
const S = path.dirname(new URL(import.meta.url).pathname);
const [variant, settingsJson, ...devPaths] = process.argv.slice(2);
const out = path.join(S, "runs", variant); fs.rmSync(out, { recursive: true, force: true }); fs.mkdirSync(out, { recursive: true });
const root = fs.mkdtempSync(path.join(fs.realpathSync("/tmp"), "ags-"));
const d = (n) => { const p = path.join(root, n); fs.mkdirSync(p, { recursive: true }); return p; };
const userData = d("data"), agentsData = d("agents-data");
const settings = { "update.mode": "none", "extensions.autoUpdate": false, "telemetry.telemetryLevel": "off", "workbench.startupEditor": "none", "security.workspace.trust.enabled": false, ...JSON.parse(settingsJson || "{}") };
for (const ud of [userData, agentsData]) { fs.mkdirSync(path.join(ud, "User"), { recursive: true }); fs.writeFileSync(path.join(ud, "User", "settings.json"), JSON.stringify(settings, null, 2)); }
if (process.env.INSTALL_VSIX) for (const dir of [path.join(root, "ext"), path.join(root, "agents-ext")]) {
  const r = spawnSync("/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code", ["--user-data-dir", userData, "--extensions-dir", dir, "--install-extension", process.env.INSTALL_VSIX, "--force"], { encoding: "utf8", env: { ...process.env, VSCODE_CLI: undefined } });
  fs.appendFileSync(path.join(out, "install.log"), dir + "\n" + r.stdout + r.stderr + "\n");
}
const port = await new Promise((r) => { const s = net.createServer(); s.listen(0, "127.0.0.1", () => { const p = s.address().port; s.close(() => r(p)); }); });
const target = path.join(S, "ws", "sample.md");
const argv = [`--user-data-dir=${userData}`, `--extensions-dir=${d("ext")}`, `--shared-data-dir=${d("shared")}`, `--agent-plugins-dir=${d("plugins")}`,
  `--agents-user-data-dir=${agentsData}`, `--agents-extensions-dir=${d("agents-ext")}`,
  ...devPaths.map((p) => `--extensionDevelopmentPath=${p}`),
  `--remote-debugging-port=${port}`, "--remote-debugging-address=127.0.0.1", "--skip-welcome", "--skip-release-notes", "--disable-telemetry", "--new-window",
  ...(process.env.AGENTS === "0" ? [path.join(S, "ws")] : ["--agents"])];
fs.writeFileSync(path.join(out, "argv.json"), JSON.stringify({ root, argv }, null, 2));
const log = fs.openSync(path.join(out, "vscode.log"), "a");
const child = spawn("/Applications/Visual Studio Code.app/Contents/MacOS/Code", argv, { detached: true, stdio: ["ignore", log, log],
  env: { ...process.env, PROBE_OUT: out, PROBE_TARGET: target, VSCODE_CLI: undefined, ELECTRON_RUN_AS_NODE: undefined } });
child.unref();
fs.writeFileSync(path.join(out, "pid"), String(child.pid));
let browser;
for (let i = 0; i < 120 && !browser; i++) { try { browser = await chromium.connectOverCDP(`http://127.0.0.1:${port}`); } catch { await delay(500); } }
await delay(Number(process.env.WAIT ?? 20000));
const pages = browser.contexts().flatMap((c) => c.pages());
fs.writeFileSync(path.join(out, "pages.json"), JSON.stringify(await Promise.all(pages.map(async (p) => ({ url: p.url(), title: await p.title().catch(() => "") }))), null, 2));
let i = 0; for (const p of pages) { if (/workbench|sessions|agents/i.test(p.url())) await p.screenshot({ path: path.join(out, `shot-${i++}.png`) }).catch(() => {}); }
fs.writeFileSync(path.join(out, "session.json"), JSON.stringify({ port, pid: child.pid, root }));
console.log(JSON.stringify({ out, port, pid: child.pid, root }));
if (process.env.KILL === "1") { await browser.close().catch(() => {}); try { process.kill(child.pid); } catch {} await delay(2000); }
process.exit(0);

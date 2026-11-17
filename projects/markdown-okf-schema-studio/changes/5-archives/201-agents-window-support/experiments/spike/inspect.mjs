// node inspect.mjs <port> [js-expression evaluated with `doc` = webview document]
import { createRequire } from "node:module";
const { chromium } = createRequire("/Users/az02065/Projects/DevTools/markdown-okf-schema-studio/package.json")("playwright-core");
const port = process.argv[2];
const targets = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json();
const expr = process.argv[3] ?? `({
  title: doc.title,
  buttons: [...doc.querySelectorAll("button")].map((x) => ({ l: x.getAttribute("aria-label") || x.title || x.textContent.trim().slice(0, 30), d: x.disabled || x.getAttribute("aria-disabled") === "true" })).slice(0, 12),
  readOnly: (doc.body.innerText.match(/(read[- ]only|no workspace)[^\\n]{0,160}/i) || [null])[0],
  textStart: doc.body.innerText.slice(0, 80),
})`;
for (const t of targets.filter((t) => t.type === "iframe")) {
  const ws = new WebSocket(t.webSocketDebuggerUrl);
  await new Promise((r) => ws.addEventListener("open", r));
  const res = await new Promise((r) => {
    ws.addEventListener("message", (m) => { const d = JSON.parse(m.data); if (d.id === 1) r(d); });
    ws.send(JSON.stringify({ id: 1, method: "Runtime.evaluate", params: { expression: `(() => { const doc = document.querySelector("#active-frame")?.contentDocument; if (!doc) return "no active-frame"; return JSON.stringify(${expr}); })()`, returnByValue: true, awaitPromise: true } }));
  });
  console.log(res.result?.result?.value ?? JSON.stringify(res));
  ws.close();
}
process.exit(0);

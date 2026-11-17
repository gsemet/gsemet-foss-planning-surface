// STAB-07 probe: GitHub alerts must render identically with LF and CRLF line endings.
import * as path from "node:path";
import { createRequire } from "node:module";
const require = createRequire(import.meta.url);
const out = path.resolve(process.env.OUT ?? "out/src");
const { renderMyst } = require(`${out}/render/mystRenderer.js`);
const crlf = "> [!NOTE]\r\n> Remember this.\r\n\r\nText\r\n";
const lf = crlf.replaceAll("\r\n", "\n");
const [a, b] = [await renderMyst(lf), await renderMyst(crlf)];
console.log(JSON.stringify({
  probe: "crlf-alerts", lfAdmonition: /admonition/.test(a.html), crlfAdmonition: /admonition/.test(b.html),
}));

// Closes a leftover trial window gracefully over CDP: node closecdp.js <port>
const { chromium } = require("C:/Users/gaeta/Projets/markdown-okf-schema-studio.worktrees/batch-07-CR-445/node_modules/playwright-core");
(async () => { const b = await chromium.connectOverCDP(`http://127.0.0.1:${process.argv[2]}`); const s = await b.newBrowserCDPSession(); await s.send("Browser.close").catch(() => {}); console.log("closed"); })().catch((e) => console.log("nothing to close: " + String(e).slice(0, 80)));

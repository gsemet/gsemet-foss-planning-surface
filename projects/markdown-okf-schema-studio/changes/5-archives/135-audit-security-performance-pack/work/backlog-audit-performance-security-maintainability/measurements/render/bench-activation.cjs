require("./vscode-stub.cjs");
if (global.gc) global.gc();
const h0 = process.memoryUsage().heapUsed, r0 = process.memoryUsage().rss;
const t = performance.now();
let m; try { m = require(process.argv[2]); } catch (e) { console.log("require failed", e.message); process.exit(1); }
const d = performance.now() - t;
if (global.gc) global.gc();
console.log(JSON.stringify({ file: process.argv[2].split("/").pop(), requireMs: +d.toFixed(1), heapDeltaMB: +((process.memoryUsage().heapUsed - h0) / 1048576).toFixed(1), rssDeltaMB: +((process.memoryUsage().rss - r0) / 1048576).toFixed(1), exports: Object.keys(m) }));

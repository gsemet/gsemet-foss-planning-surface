// Wraps churn.js's ev() to report where undisposed subscriptions were created (N=3,R=1).
const Module = require("node:module");
const live = new Map();
globalThis.__trackSub = (d) => { const st = new Error().stack.split("\n").filter((l) => l.includes("out/src")).slice(0, 2).map((l) => l.trim()).join(" <- "); live.set(d, st); return d; };
globalThis.__untrack = (d) => live.delete(d);
process.on("exit", () => { const c = {}; for (const s of live.values()) c[s] = (c[s] ?? 0) + 1; console.log(c); console.log("applied log:", globalThis.__store?.applied?.length); });
require("./churn.js");

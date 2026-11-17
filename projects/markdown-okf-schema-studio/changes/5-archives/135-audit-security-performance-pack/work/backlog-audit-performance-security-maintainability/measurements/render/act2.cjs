require("./vscode-stub.cjs");
const m = require(process.argv[2]);
const t = performance.now();
Promise.resolve().then(() => m.activate({ subscriptions: [], extensionUri: { fsPath: "/x", scheme: "file" }, extensionPath: "/x", globalState: { get() {}, update() {}, keys: () => [] }, workspaceState: { get() {}, update() {}, keys: () => [] } })).then(() => console.log("activate ms", (performance.now() - t).toFixed(1)), (e) => console.log("activate threw", String(e).slice(0, 100), (performance.now() - t).toFixed(1))).finally(() => process.exit(0));

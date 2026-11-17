const path = require("node:path");
const O = path.join(__dirname, "out/src");
exports.O = O;
exports.pipeline = require(O + "/core/render/renderPipeline.js");
exports.mystEngine = require(O + "/core/render/mystEngine.js");
exports.mystRenderer = require(O + "/core/render/mystRenderer.js");
exports.san = require(O + "/core/security/html-sanitizer.js");
exports.mapping = require(O + "/core/mapping/sourceMapping.js");
exports.anch = require(O + "/core/comments/anchoring.js");
const { ResourcePolicy } = require(O + "/core/security/resource-policy.js");
exports.ResourcePolicy = ResourcePolicy;
const root = "/tmp/bench-ws";
exports.root = root;
exports.mkDoc = (text, v = 1) => ({ uri: { scheme: "file", fsPath: root + "/doc.md" }, languageId: "markdown", version: v, getText: () => text });
exports.opts = (text, id = 1) => ({ document: exports.mkDoc(text, id), workspaceRoot: root, requestId: id, isWorkspaceTrusted: () => true, plantUmlEngine: "builtin" });
exports.sanCtx = () => ({ outputRoot: root, policy: new ResourcePolicy([]), nonce: "n", sourceMapping: { sourceFile: root + "/doc.md", documentId: "d" },
  resolveResource: () => undefined, resolveNavigation: () => ({ kind: "blocked" }) });
exports.median = (a) => [...a].sort((x, y) => x - y)[a.length >> 1];
exports.t = async (fn) => { const s = performance.now(); const r = await fn(); return [performance.now() - s, r]; };

const Module = require("node:module");
const mk = () => new Proxy(function () {}, { get: (t, k) => k === Symbol.toPrimitive ? () => "" : k === "then" ? undefined : mk(), apply: () => mk(), construct: () => mk() });
const stub = mk();
const orig = Module._load;
Module._load = function (req, ...a) { return req === "vscode" ? stub : orig.call(this, req, ...a); };

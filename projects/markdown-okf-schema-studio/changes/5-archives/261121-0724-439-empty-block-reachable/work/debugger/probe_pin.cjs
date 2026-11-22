const { isPageToHostMessage } = require(process.argv[2] + "/out/src/core/protocol/pageToHost.js");
const base = { documentId: "file:///x.md", revision: 1, requestId: 1, editId: "e1", line: 3, endLine: 3, originalText: "First.\n", editedText: "" };
const t = (n, m) => console.log(n.padEnd(48), isPageToHostMessage(m));
t("autosave + pinViewportTop (test as written)", { type: "previewEditSave", ...base, pinViewportTop: 200, final: false });
t("autosave without pin", { type: "previewEditSave", ...base, final: false });
t("final+deleteWhenEmpty + pinViewportTop only", { type: "previewEditSave", ...base, pinViewportTop: 200, final: true, deleteWhenEmpty: true });
t("final+deleteWhenEmpty + pinLine+pinViewportTop", { type: "previewEditSave", ...base, pinLine: 3, pinViewportTop: 200, final: true, deleteWhenEmpty: true });
t("final+deleteWhenEmpty, no pin", { type: "previewEditSave", ...base, final: true, deleteWhenEmpty: true });
t("previewBlocksDelete + pinViewportTop", { type: "previewBlocksDelete", documentId: base.documentId, revision: 1, requestId: 1, line: 3, endLine: 3, pinViewportTop: 200 });

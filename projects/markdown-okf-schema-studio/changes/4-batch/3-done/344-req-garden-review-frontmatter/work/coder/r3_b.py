import re, sys
sys.path.insert(0, sys.argv[0].rsplit("/", 1)[0])
from r3_mark import read, write

f = "test/integration/previewEditing.test.ts"
text, crlf = read(f)
assert not crlf
FIRST_THEME = '    for (const theme of ["white", "dark"] as const) {\n      const frame = await previewFrame(page);\n'
KEYS = ["page", "document", "directory", "evidence", "implementationPath", "testPath", "expectedOutsidePath", "stemTarget", "cleanup"]
steps = []


def extract(name, markers, start, end, doc, params="", ret=None, edits=()):
    global text
    i = text.index(start)
    j = text.index(end, i)
    body = text[i:j]
    text = text[:i] + "@@STEP:%s@@\n" % name + text[j:]
    for a, b in edits:
        assert a in body, (name, a[:40])
        body = body.replace(a, b)
    body = "\n".join(l[2:] if l.startswith("  ") else l for l in body.split("\n"))
    used = [k for k in KEYS if re.search(r"\b%s\b" % k, body)]
    steps.append(dict(name=name, markers=markers, body=body.rstrip("\n"), used=used, doc=doc, params=params, ret=ret))


SP = "    const schemaPreview = getActivePreviewForTests();\n"
extract("stepFrontmatterTable", ["StRS-MDOKFSTUDIO-FMSCHEMA-001", "SwRS-MDOKFSTUDIO-FMSCHEMA-001"],
        SP, FIRST_THEME, "The properties table renders from the schema: fields, link statuses and excerpts, evidence line badges.",
        ret="schemaPreview")
extract("stepLinkTooltips", ["SwRS-MDOKFSTUDIO-FMSCHEMA-067", "SwRS-MDOKFSTUDIO-FMSCHEMA-084"],
        FIRST_THEME, "    // The user edits and saves the linked target in the editor",
        "A link tooltip shows the target description and excerpt; the violation of the closed schema counts in the badge and shows as an error row.")
extract("stepDescriptionColumn", ["SwRS-MDOKFSTUDIO-FMSCHEMA-014", "SwRS-MDOKFSTUDIO-LIFE-169"],
        '    assert.match(\n      getActivePreviewForTests()?.html ?? "",\n      /<thead>',
        '    await setViewport(page, { width: 2400, height: 1100 });\n    const longDescription',
        "The Description column collapses, the choice survives a refresh, in wide and narrow layouts.")
extract("stepLinksOpen", ["StRS-MDOKFSTUDIO-FMSCHEMA-014", "SwRS-MDOKFSTUDIO-FMSCHEMA-073", "SwRS-MDOKFSTUDIO-FMSCHEMA-063"],
        "    const refreshedFrame = await previewFrame(page);\n    await refreshedFrame.locator('[data-okf-field=\"related\"] a[data-sphinx-preview-navigation",
        "    const invalidLinkContext = currentContext(document);",
        "Each frontmatter link opens its target at its fragment or marker line; the line badge follows the file.")
extract("stepLinkRepair", ["SwRS-MDOKFSTUDIO-FMSCHEMA-073", "SwRS-MDOKFSTUDIO-FMSCHEMA-063"],
        "    const invalidLinkContext = currentContext(document);", "    const initial = currentContext(document);\n",
        "An invalid link value shows its code, a repaired one resolves; an ambiguous stem and an escaped symlink are refused at click time.",
        edits=[('duplicateRoot = fs.mkdtempSync(path.join("/tmp", "studio-duplicate-root-"));',
                'const duplicateRoot = fs.mkdtempSync(path.join("/tmp", "studio-duplicate-root-"));\n    cleanup.duplicateRoot = duplicateRoot;'),
               ('symlinkOutsideRoot = fs.mkdtempSync(path.join("/tmp", "studio-symlink-outside-"));',
                'const symlinkOutsideRoot = fs.mkdtempSync(path.join("/tmp", "studio-symlink-outside-"));\n    cleanup.symlinkOutsideRoot = symlinkOutsideRoot;')])
# the edits above are applied before the dedent: indentation is fixed by the dedent
extract("stepAnchorMode", ["SwRS-MDOKFSTUDIO-TOOLBAR-120"],
        '    sendPreviewMessageForTests({\n      type: "previewAnchorModeChanged",\n      ...initial,\n      anchorToEditor: false,',
        '    sendPreviewMessageForTests({\n      type: "previewFrontmatterSave",\n      ...initial,\n      editId: "integration-status-save"',
        "The Anchor button switches whether the preview follows the editor.",
        params=", initial: ReturnType<typeof currentContext>")
extract("stepFrontmatterSaves", ["SwRS-MDOKFSTUDIO-BLOCK-058", "SwRS-MDOKFSTUDIO-FMEDIT-024", "SwRS-MDOKFSTUDIO-FMEDIT-043"],
        '    sendPreviewMessageForTests({\n      type: "previewFrontmatterSave",\n      ...initial,\n      editId: "integration-status-save"',
        "    const current = currentContext(document);\n    const beforeRejectedEdits",
        "Frontmatter saves of an enum, a boolean, an added, removed and renamed field change only their lines; a required field is not removed.",
        params=", initial: ReturnType<typeof currentContext>")
extract("stepFrontmatterRefusals", ["SwRS-MDOKFSTUDIO-FMEDIT-016"],
        "    const current = currentContext(document);\n    const beforeRejectedEdits", "    const bodyEditContext = currentContext(document);",
        "The host refuses a value that breaks the enum, the stale revision, the array item or the object property, and writes the valid ones.",
        params=", initial: ReturnType<typeof currentContext>")
extract("stepBodyEdits", ["StRS-MDOKFSTUDIO-BLOCK-003", "SwRS-MDOKFSTUDIO-BLOCK-014", "SwRS-MDOKFSTUDIO-BLOCK-216"],
        "    const bodyEditContext = currentContext(document);", "    const tableContext = currentContext(document);",
        "A body block is edited, autosaved and saved; a save whose original text no longer matches is refused.")
extract("stepTableAndInsert", ["SwRS-MDOKFSTUDIO-BLOCK-094", "SwRS-MDOKFSTUDIO-BLOCK-053"],
        "    const tableContext = currentContext(document);", "    // Edit lock and save-triggered renders",
        "A table is edited cell by cell, a new block is inserted with clean blank lines, and a cancelled insertion is removed.")
extract("stepEditLock", ["SwRS-MDOKFSTUDIO-BLOCK-191"],
        "    // Edit lock and save-triggered renders", "    // The copy button of a code block",
        "An open block edit holds the render until it ends.")
steps[0]["body"] += "\n\n  return schemaPreview;"
calls = {
    "stepFrontmatterTable": "    const schemaPreview = await stepFrontmatterTable(ctx);\n",
    "stepLinkTooltips": "    await stepLinkTooltips(ctx);\n",
    "stepDescriptionColumn": "    await stepDescriptionColumn(ctx);\n",
    "stepLinksOpen": "    await stepLinksOpen(ctx);\n",
    "stepLinkRepair": "    await stepLinkRepair(ctx);\n",
    "stepAnchorMode": "    const initial = currentContext(document);\n    await stepAnchorMode(ctx, initial);\n",
    "stepFrontmatterSaves": "    await stepFrontmatterSaves(ctx, initial);\n",
    "stepFrontmatterRefusals": "    await stepFrontmatterRefusals(ctx, initial);\n    await stepSchemaOrderAndBadge(ctx);\n",
    "stepBodyEdits": "    await stepBodyEdits(ctx);\n",
    "stepTableAndInsert": "    await stepTableAndInsert(ctx);\n",
    "stepEditLock": "    await stepEditLock(ctx);\n",
}
for k, v in calls.items():
    text = text.replace("@@STEP:%s@@\n" % k, v)
assert "@@STEP" not in text
text = text.replace("  let duplicateRoot: string | undefined;\n  let symlinkOutsideRoot: string | undefined;\n",
                    "  const cleanup: { duplicateRoot?: string; symlinkOutsideRoot?: string } = {};\n")
text = text.replace("    if (duplicateRoot) fs.rmSync(duplicateRoot, { recursive: true, force: true });\n    if (symlinkOutsideRoot) fs.rmSync(symlinkOutsideRoot, { recursive: true, force: true });\n",
                    "    if (cleanup.duplicateRoot) fs.rmSync(cleanup.duplicateRoot, { recursive: true, force: true });\n    if (cleanup.symlinkOutsideRoot) fs.rmSync(cleanup.symlinkOutsideRoot, { recursive: true, force: true });\n")
anchor = "    await vscode.window.showTextDocument(document, vscode.ViewColumn.One);\n    await vscode.commands.executeCommand(COMMAND_ID);\n"
assert text.count(anchor) == 1
text = text.replace(anchor, anchor + "    const ctx: EditingContext = {\n      page, document, directory, evidence, implementationPath, testPath, expectedOutsidePath, stemTarget, cleanup,\n    };\n")
out = ["""interface EditingContext {
  page: Page;
  document: vscode.TextDocument;
  directory: string;
  evidence: RealWindowEvidence;
  implementationPath: string;
  testPath: string;
  expectedOutsidePath: string;
  stemTarget: string;
  cleanup: { duplicateRoot?: string; symlinkOutsideRoot?: string };
}
"""]
for s in steps:
    mk = "\n".join("// @tests_req " + m for m in s["markers"])
    d = "/** " + s["doc"] + " */\n"
    ret = "Promise<NonNullable<ReturnType<typeof getActivePreviewForTests>>>" if s["ret"] else "Promise<void>"
    destruct = "  const { %s } = ctx;\n" % ", ".join(s["used"]) if s["used"] else ""
    out.append(f"{d}{mk}\nasync function {s['name']}(ctx: EditingContext{s['params']}): {ret} {{\n{destruct}{s['body']}\n}}\n")
steps_text = "\n".join(out)
marker = "// @tests_req StRS-MDOKFSTUDIO-FMSCHEMA-001\n// @tests_req StRS-MDOKFSTUDIO-FMSCHEMA-014\n"
i = text.index(marker)
j = text.index("export async function run()")
text = text[:i] + steps_text + "\n" + text[j:]
write(f, text, crlf)

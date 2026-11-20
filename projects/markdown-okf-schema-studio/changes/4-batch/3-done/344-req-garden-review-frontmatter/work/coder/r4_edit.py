import sys

path = sys.argv[1]
with open(path, "rb") as handle:
    text = handle.read().decode("utf-8")

old_a = (
    '  const requestBefore = currentContext(document).requestId;\n'
    '  assert.equal(await vscode.workspace.applyEdit(replaceDocument(document, brokenText)), true);\n'
    '  try {\n'
    '    await waitFor("the count field to carry its schema violation", () =>\n'
    '      /<tr class="[^"]*\x08okf-error\x08[^"]*" data-okf-field="count"/u.test(getActivePreviewForTests()?.html ?? ""));\n'
    '    await waitForCurrentPreview(document, requestBefore);\n'
)
new_a = (
    '  // The outside edit targets the active, settled preview, as in stepSchemaProblem.\n'
    '  await vscode.window.showTextDocument(document, vscode.ViewColumn.One);\n'
    '  await waitForCurrentPreview(document);\n'
    '  const requestBefore = currentContext(document).requestId;\n'
    '  assert.equal(await vscode.workspace.applyEdit(replaceDocument(document, brokenText)), true);\n'
    '  try {\n'
    '    await withPreviewEvidence(document, () => waitForCurrentPreview(document, requestBefore));\n'
    '    await withPreviewEvidence(document, () => waitFor("the count field to carry its schema violation", () =>\n'
    '      countRowHasError(getActivePreviewForTests()?.html ?? "") === true));\n'
)
old_b = (
    '    await waitFor("the count field to be valid again", () =>\n'
    '      !/<tr class="[^"]*\x08okf-error\x08[^"]*" data-okf-field="count"/u.test(getActivePreviewForTests()?.html ?? ""));\n'
    '    await waitForCurrentPreview(document);\n'
    '  }\n'
    '}\n'
)
new_b = (
    '    await withPreviewEvidence(document, () => waitFor("the count field to be valid again", () =>\n'
    '      countRowHasError(getActivePreviewForTests()?.html ?? "") === false));\n'
    '    await withPreviewEvidence(document, () => waitForCurrentPreview(document));\n'
    '  }\n'
    '}\n'
    '\n'
    '/** The opening tag of the `count` row of the properties table, whatever its attribute order. */\n'
    'function countRowTag(html: string): string | undefined {\n'
    '  return html.match(/<tr\\b[^>]*\\bdata-okf-field="count"[^>]*>/u)?.[0];\n'
    '}\n'
    '\n'
    '/** Whether the `count` row carries the error class; undefined when the html has no `count` row. */\n'
    'function countRowHasError(html: string): boolean | undefined {\n'
    '  const tag = countRowTag(html);\n'
    '  return tag === undefined ? undefined : /\\bclass="[^"]*\\bokf-error\\b/u.test(tag);\n'
    '}\n'
    '\n'
    '/** Runs a wait; on failure, rethrows it with the active preview\'s phase, versions and `count` row tag. */\n'
    'async function withPreviewEvidence(document: vscode.TextDocument, wait: () => Promise<void>): Promise<void> {\n'
    '  try {\n'
    '    await wait();\n'
    '  } catch (error) {\n'
    '    const preview = getActivePreviewForTests();\n'
    '    const evidence = preview\n'
    '      ? `phase=${preview.phase} documentVersion=${String(preview.documentVersion)} document.version=${document.version}`\n'
    '        + ` requestId=${String(preview.requestId)} sameDocument=${String(preview.documentUri === document.uri.toString())}`\n'
    '        + ` countRow=${countRowTag(preview.html) ?? "no count row"}`\n'
    '      : "no active preview";\n'
    '    throw new Error(`${error instanceof Error ? error.message : String(error)} [${evidence}]`);\n'
    '  }\n'
    '}\n'
)
for old, new in ((old_a, new_a), (old_b, new_b)):
    if text.count(old) != 1:
        sys.exit("anchor not found once")
    text = text.replace(old, new)
if "\x08" in text:
    sys.exit("backspace left")
with open(path, "wb") as handle:
    handle.write(text.encode("utf-8"))
print("ok")

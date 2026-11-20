import sys
sys.path.insert(0, "C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/4-batch/2-actives/344-req-garden-review-frontmatter/work/coder")
from r3_mark import *
TODO = '''/**
 * StRS review-annotations REVIEW-012: the TODO action of the edition palette wraps each line of the
 * block in a TODO comment, one undo restores the lines, and the committed source holds the comment.
 */
// @tests_req StRS-MDOKFSTUDIO-REVIEW-012
// @tests_req SwRS-MDOKFSTUDIO-REVIEW-160
export async function scenarioTodoToggle(page: Page, evidence: Evidence): Promise<void> {
  await withSmokeDocument("realinput-todo", async (document) => {
    await openSidePreview(document);
    await waitForRender(document);
    await setEditMode(page, true);
    const area = "[data-sphinx-preview-block-editor] textarea";
    const value = (): Promise<string> => withCurrentFrame(page, (frame) => frame.locator(area).inputValue());
    const original = "First paragraph line one\ncontinues on line two.";
    const wrapped = "<!-- TODO: First paragraph line one -->\n<!-- TODO: continues on line two. -->";
    await withCurrentFrame(page, (frame) => frame.locator("p", { hasText: "First paragraph" }).click());
    await waitForEditor(page, area);
    await press(page, MOD + "+a");
    await withCurrentFrame(page, (frame) => frame.locator("[data-edit-action='todo']").click());
    await waitFor("the TODO comment around each line", async () => await value() === wrapped);
    await press(page, MOD + "+z");
    await waitFor("one undo to restore the lines", async () => await value() === original);
    await press(page, MOD + "+a");
    await withCurrentFrame(page, (frame) => frame.locator("[data-edit-action='todo']").click());
    await waitFor("the TODO comment again", async () => await value() === wrapped);
    await press(page, MOD + "+Enter");
    await waitFor("the source to hold the TODO comment around the lines", () =>
      bufferText(document) === SMOKE.replace(original, wrapped));
    await captureAfter(evidence, page, "review-annotations/r05-todo-toggle",
      "Edit mode on; the TODO action wrapped both lines of the paragraph, one Cmd/Ctrl+Z restored them, "
      + "and the committed source holds the two TODO comments.");
    await leaveEditModeOff();
  });
}

'''
f = "test/integration/realInput/blockKeys.ts"
replace(f, "export async function scenarioCtrlEnterCommit(", TODO + "export async function scenarioCtrlEnterCommit(")
replace(f, "// @tests_req SwRS-MDOKFSTUDIO-REVIEW-152\nexport async function scenarioHiddenReviewMarks",
 "// @tests_req StRS-MDOKFSTUDIO-REVIEW-012\n// @tests_req SwRS-MDOKFSTUDIO-REVIEW-152\nexport async function scenarioHiddenReviewMarks")
replace("test/integration/realInput/run.ts", "scenarioParagraphBlurCommit, scenarioReviewComments,", "scenarioParagraphBlurCommit, scenarioReviewComments, scenarioTodoToggle,")
replace("test/integration/realInput/run.ts", "    await scenarioHiddenReviewMarks(page);\n", "    await scenarioHiddenReviewMarks(page);\n    await scenarioTodoToggle(page, evidence);\n")
# realWindowGaps
g = "test/integration/realWindowGaps.ts"
replace(g, "// @tests_req SwRS-MDOKFSTUDIO-REVIEW-006\n// @tests_req SwRS-MDOKFSTUDIO-REVIEW-008\n// @tests_req SwRS-MDOKFSTUDIO-REVIEW-009\n/**\n * CR 147",
 "// @tests_req StRS-MDOKFSTUDIO-REVIEW-018\n// @tests_req SwRS-MDOKFSTUDIO-REVIEW-006\n// @tests_req SwRS-MDOKFSTUDIO-REVIEW-008\n// @tests_req SwRS-MDOKFSTUDIO-REVIEW-009\n/**\n * CR 147")
# frontmatter scenarios
ff = "test/integration/realInput/frontmatterFields.ts"
add(ff, {
 "export async function scenarioListEditorClickAndKeys": ["S:FMEDIT-001", "FMSCHEMA-043"],
 "export async function scenarioCustomKeyAndOpenNewField": ["S:FMEDIT-005"],
 "export async function scenarioAddFieldPositionAndEscape": ["S:FMEDIT-005", "FMEDIT-019"],
})
te = "test/integration/realInput/textEditing.ts"
add(te, {
 "export async function scenarioFrontmatterValueMinimalPatch": ["S:FMEDIT-008"],
 "export async function scenarioFrontmatterStructuralMinimalPatch": ["S:FMEDIT-008"],
 "export async function scenarioEnterCommitsTextField": ["S:FMEDIT-001"],
})
add("test/integration/realInput/flushBeforeNavigate.ts", {"export async function scenarioFlushFrontmatterKeptAsTyped": ["S:FMEDIT-008"]})
for ln in ["SwRS-MDOKFSTUDIO-FMEDIT-019","SwRS-MDOKFSTUDIO-FMSCHEMA-039","SwRS-MDOKFSTUDIO-FMSCHEMA-043","SwRS-MDOKFSTUDIO-FMSCHEMA-063","StRS-MDOKFSTUDIO-FMEDIT-001","StRS-MDOKFSTUDIO-FMEDIT-005","StRS-MDOKFSTUDIO-FMEDIT-008","StRS-MDOKFSTUDIO-FMSCHEMA-001","StRS-MDOKFSTUDIO-FMSCHEMA-014"]:
    replace("test/integration/realInput/markers.ts", "// @tests_req %s\n" % ln, "")

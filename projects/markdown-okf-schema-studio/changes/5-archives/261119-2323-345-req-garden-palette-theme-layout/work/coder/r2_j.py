import sys; sys.path.insert(0, "C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/4-batch/2-actives/345-req-garden-palette-theme-layout/work/coder")
from r2lib import *
S = "test/page/modules/slashMenu.test.ts"
for i, a in [("PALETTE-256",'test("P11: the menu follows the caret on scroll'),("PALETTE-256",'test("P11: the menu keeps the same left edge'),("PALETTE-256",'test("P11 r2: scrolling inside the menu'),
  ("PALETTE-240",'test("P11 r2: in MyST the MyST entry ranks'),("PALETTE-240",'test("P11 r2: the best match being only fuzzy')]:
    mark_before(S, a, [i], kind="tests", above_doc=False)

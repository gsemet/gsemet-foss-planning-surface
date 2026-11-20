import sys; sys.path.insert(0, "C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/4-batch/2-actives/345-req-garden-palette-theme-layout/work/coder")
from r2lib import *
P = "test/page/modules/editActions.test.ts"
hdr = ["PALETTE-%03d" % n for n in (39,43,45,48,49,50,52,53,54,58,69,72,83,89,92,109,114,115,123,124,125,126,127,130,132,133,135,136,137,138,147,148,149,150)]
drop_lines(P, hdr, lines_at=range(1, 53))
M = [
 ("PALETTE-039", 'test("a selection cutting into a marker run'),
 ("PALETTE-043", 'for (const [arg, input, expected] of headingCases)'),
 ("PALETTE-050", 'for (const [input, expected] of ruleCases)'),
 ("PALETTE-054", 'for (const [arg, input, expected] of fenceCases)'),
 ("PALETTE-058", 'test("T34: color wraps the selection in the exact span'),
 ("PALETTE-069", 'test("T34: colorCode replaces the code under the caret'),
 ("PALETTE-072", 'test("emoji inserts at the caret'),
 ("PALETTE-083", 'test("shortcutFor uses Cmd on macOS and Ctrl elsewhere for B and I'),
 ("PALETTE-089", 'test("link is a strict action for blocks and cells'),
 ("PALETTE-089", 'test("linkDraft prefills'),
 ("PALETTE-092", 'for (const [input, text, url, expected] of linkCases)'),
 ("PALETTE-092", 'test("linkEdit escapes brackets'),
 ("PALETTE-092", 'test("linkEdit never breaks the target'),
 ("PALETTE-109", 'test("T31: image inserts ![name](path)'),
 ("PALETTE-114", 'test("thread inserts an empty comment thread'),
 ("PALETTE-115", 'test("T25: alert on an empty line'),
 ("PALETTE-124", 'test("T26: details inserts'),
 ("PALETTE-125", 'test("T26: footnote takes the next free number'),
 ("PALETTE-127", 'test("T28: admonition wraps the touched lines'),
 ("PALETTE-127", 'test("T28: custom admonition'),
 ("PALETTE-127", 'test("T30: dropdown inserts'),
 ("PALETTE-132", 'test("T28: deflist'),
 ("PALETTE-133", 'test("T28: math inline'),
 ("PALETTE-136", 'test("T28: label inserts'),
 ("PALETTE-147", 'test("T30: ref inserts'),
 ("PALETTE-148", 'test("T30: doc inserts'),
 ("PALETTE-149", 'test("T30: cite inserts'),
 ("PALETTE-150", 'test("T31: figure inserts the directive'),
 ("PALETTE-276", 'for (const [input, expected] of strikeCases)'),
 ("PALETTE-276", 'test("T26: kbd wraps'),
 ("PALETTE-276", 'test("T28: sub and sup wrap'),
 ("PALETTE-276", 'test("T30: roleKbd wraps'),
 ("PALETTE-277", 'for (const [input, expected] of quoteCases)'),
 ("PALETTE-277", 'test("T25: checkbox puts'),
 ("PALETTE-277", 'test("P11: Bulleted list on an empty line'),
 ("PALETTE-277", 'test("P11: Numbered list numbers'),
]
for i, a in M:
    mark_before(P, a, [i], kind="tests", above_doc=False)

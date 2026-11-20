import sys
sys.path.insert(0,r"C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/4-batch/2-actives/345-req-garden-palette-theme-layout/work/coder")
from fm import *
def edit(id,pairs):
    b=getbody(id)
    for a,c in pairs:
        assert b.count(a)==1,(id,a[:50])
        b=b.replace(a,c)
    setbody(id,b)
edit(full("LAYOUT-011"),[
("so that the first element keeps exactly 40 px.\n","so that the first element keeps exactly 40 px. The extension SHALL measure the clearance again after layout changes (a window resize, a change of size or content of the column, the toolbar or a leading properties table, a root attribute, a web font load, the window load, the toolbar collapsed or expanded, a change of the width mode) and publish the toolbar bottom edge plus 8 px as --sphinx-preview-toolbar-bottom while the toolbar shares horizontal space with the text column (0 otherwise).\n"),
("### Known issues\n","""### Scenario (nominal): The clearance follows layout changes
- GIVEN a leading properties table whose Description toggle moves under the toolbar after the last measurement
- WHEN the window load event fires
- THEN the inset is measured again and published (192 px in the tested layout)

- GIVEN the properties section is replaced by a new one
- WHEN the next update runs
- THEN the new section is observed for size changes

- GIVEN a 360 px pane in edit mode with the toolbar collapsed to its first row and a paragraph, then a table, as first element
- WHEN the page is rendered
- THEN the paragraph and the table start exactly 40 px (within 4 px) below the top; and with a settled page, a click on the collapse chevron makes the toolbar-collapse callback measure the first-element clearance again

- GIVEN a page whose first element sits 40 px below the top, and a width mode change that makes the column narrower
- WHEN the Width button is clicked
- THEN the first-element clearance is measured again, so the first element keeps its 40 px gap below the toolbar at the new width; a width mode change that leaves the column width and the toolbar position unchanged still measures again (the change callback calls the update unconditionally) and the published values stay the same

### Scenario (boundary): Toolbar bottom edge for the sticky palette
| Input | Outcome |
| --- | --- |
| 460 px column and a toolbar from 200 to 450 px ending at 84 px | --sphinx-preview-toolbar-bottom is 92px |
| 600 px column from 100 px and a toolbar from 800 px | The toolbar bottom is 0px |

### Known issues
"""),
("- Method: test/visual/capture_comment_checks.py (first-block editor and Start writing button)","""- Method: test/page/modules/firstClearance.test.ts (the layout-change re-measure): a late load or font settlement measures again; the leading properties table is observed itself, also after it is replaced; P4 the toolbar's bottom edge is published for the sticky palette only where it overlaps the column; a change inside a burst of skipped updates is measured by one trailing update. Burst limit: more than 200 updates within one second are skipped and the last change is measured in one trailing timer, so exactly one timer is pending after a burst (a protection added after a continuous-integration regression; after a change the layout is also measured on every animation frame until it has been unchanged for 60 frames, limit 300 frames, which no test checks).
- Method: test/visual/capture_comment_checks.py and test/visual/scenarioAssertions.ts (collapsing the toolbar): visual scenarios v55 and v56 (collapsed toolbar at 360 px); the callback wiring in the page runtime is checked by inspection (the callback list is complete). test/page/diagReq.layout.requirements.test.ts: `a width mode change measures the first-element clearance again, even when nothing moved`.
- Method: test/visual/capture_comment_checks.py (first-block editor and Start writing button)"""),
])
# LAYOUT-001
edit(full("LAYOUT-001"),[
("""### Scenario (nominal): Narrow table and long words
- GIVEN a service-level table wider than a 460 px pane in the dark theme (visual scenario v01), and text blocks, links and table cells holding long words or bare URLs
- WHEN the preview is rendered
- THEN the table scrolls inside its own wrapper to its far-right column without widening the page, and the text blocks, links and table cells carry overflow-wrap anywhere so that long words and URLs wrap
""","""### Scenario (nominal): Long words and URLs wrap
- GIVEN text blocks, links and table cells holding long words or bare URLs
- WHEN the preview is rendered
- THEN the text blocks, links and table cells carry overflow-wrap anywhere so that long words and URLs wrap and the page does not widen (a table wider than the pane scrolls inside its own box, see SwRS-MDOKFSTUDIO-LAYOUT-032)
"""),
("""### Scenario (boundary): Machine geometry checks
| Input | Outcome |
| --- | --- |
| The geometry checks function run on a page without any content | Four results are reported in the order overlay-covers-text, overlay-clipped, identifier-split, status-two-lines, each not applicable and passing |
| Identifier-split check on a cell whose single text node wraps over two lines | That text node fails and its text is named in the detail |
| Identifier-split check on a cell whose text nodes share one line | Passes |
| Identifier-split check on list items on separate lines | Passes |

""",""),
("- Known issue: The machine geometry checks are test tooling with no user-visible effect, and they are undocumented outside their unit test; the overlay checks serve other scopes' visual scenarios.\n",""),
("- Method: test/visual/scenarioDefinitions1.ts and test/visual/capture_layout_checks.py (width modes at 460 px, narrow table and long words, GFM gallery): visual scenarios v01, v66","- Method: test/visual/scenarioDefinitions1.ts and test/visual/capture_layout_checks.py (width modes at 460 px, long words, GFM gallery): visual scenarios v01, v66"),
("- Method: test/core/preview/previewStyles.test.ts (narrow table and long words)","- Method: test/core/preview/previewStyles.test.ts (long words)"),
("- Method: test/page/geometryChecks.test.ts (machine geometry checks): four ids, not applicable without a DOM, identifier-split cases, nested text node counted once.\n","- Note: the four machine geometry checks of test/page/geometryChecks.test.ts are test infrastructure with no user-visible effect and are not a requirement.\n"),
("and the geometry check ids and order are exact with every check passing when it is not applicable.","."),
])
# LAYOUT-022
edit(full("LAYOUT-022"),[
("""### Scenario (nominal): Wide table in Margin
- GIVEN Margin width mode, a column of 700 px and a table 900 px wide
- WHEN the preview is rendered
- THEN no element is marked data-sphinx-preview-wide and the table scrolls inside the column

""",""),
])

import sys
sys.path.insert(0, sys.argv[1])
from merge import *

def add_scen(i, scen, note):
    p = swrs_path(i)
    t = read(p)
    body, tail = split_links(t)
    pos = None
    for h in ("### Known issues", "### Related requirements", "### Verification notes"):
        k = body.find("\n" + h + "\n")
        if k >= 0 and (pos is None or k < pos):
            pos = k + 1
    body = body[:pos] + scen.strip("\n") + "\n\n" + body[pos:]
    body = body.rstrip("\n") + "\n" + note + "\n\n"
    write(p, body + tail)

add_scen("REVIEW-133", """### Scenario (boundary): An HTML comment inside a tab item keeps its own source lines

- GIVEN a tab item that holds a paragraph and the comment `<!-- review: inner -->` on line 5
- WHEN the document is rendered
- THEN the comment wrapper carries data-line 5 and data-end-line 5, the tab panel stays one block, and the paragraph beside the comment carries no source line
""", "- Method: test/core/render/cardsTabs.test.ts, unit test `a comment and a thread in a tab item keep their own source line range` (An HTML comment inside a tab item keeps its own source lines).")
add_scen("REVIEW-167", """### Scenario (boundary): A thread inside a tab item keeps its own source lines

- GIVEN a tab item that holds an inline thread comment from line 7 to line 12
- WHEN the document is rendered
- THEN the thread wrapper carries data-line 7 and data-end-line 12, so that the reply and the delete of the thread name those lines, and the tab panel stays one block
""", "- Method: test/core/render/cardsTabs.test.ts, unit test `a comment and a thread in a tab item keep their own source line range` (A thread inside a tab item keeps its own source lines).")

from st import *
A="StRS-MDOKFSTUDIO-TOOLBAR-001"
set_title(A,"The toolbar groups its controls, collapses and remembers its collapsed state")
set_description(A,"When a reader opens a preview, the Studio SHALL show its controls in four clearly grouped rows that never overlap each other, and let the reader collapse them to the first row, keeping the collapsed choice for the workspace, in Restricted Mode and for standalone files too.")
set_need(A,"As a reader, I find the preview controls in four clear rows. I fold the toolbar down to its first row to free the top of the pane and unfold it again, and a collapsed toolbar stays collapsed when I reopen a preview of the same workspace, in Restricted Mode and for a standalone file too. The toolbar and its tooltips move softly (not at all when my system asks for reduced motion), and a newly opened collapsed toolbar shows briefly that it can expand. My other view choices (zoom, width, table of contents, incoming-change marks, comments) are kept by the rule of the previews that come back after a reload.")
t=rd(A)
old1="- A view preference only changes how the preview looks, never the document, so every preview accepts it, whatever the trust.\n- A value that is not valid for its preference is refused; a stored value that is not valid falls back to the default of that preference alone.\n- The meaning of zoom and width is described in the theme-zoom and layout-width scopes.\n"
new1="- Only the collapsed toolbar is remembered here. The other view choices (zoom, width mode, table of contents, incoming-change marks, comments) are kept and read back by the rule of StRS-MDOKFSTUDIO-LIFE-014, whatever the trust of the workspace; the meaning of zoom and width is described in the theme-zoom and layout-width scopes.\n"
assert old1 in t
wr(A,t.replace(old1,new1))
add(A,"depends_on",["SwRS-MDOKFSTUDIO-LIFE-169","SwRS-MDOKFSTUDIO-LIFE-170"])
set_main_paths(A,"""#### Path 1: Collapse the toolbar and find it collapsed

1. A preview page is built
   - SwRS-MDOKFSTUDIO-TOOLBAR-001: the toolbar is drawn as four rows of titled buttons, inside the pane and without overlap
2. The toolbar is expanded
   - SwRS-MDOKFSTUDIO-TOOLBAR-007: the reader presses the collapse button and the rows of navigation and view are hidden
   - Option SwRS-MDOKFSTUDIO-TOOLBAR-007 (boundary): when collapsed, the hidden rows are out of the Tab order
3. The toolbar is collapsed
   - SwRS-MDOKFSTUDIO-TOOLBAR-007: the collapsed choice is kept for the workspace and a new page starts from it
   - Option SwRS-MDOKFSTUDIO-LIFE-169 (refusal): a message with a value that is not a boolean is dropped without an answer
   - Option SwRS-MDOKFSTUDIO-LIFE-170 (boundary): a stored value that is not valid is skipped and the next source is used
4. A new preview of the workspace opens collapsed
   - SwRS-MDOKFSTUDIO-TOOLBAR-130: the rows unroll once and roll up again, and a load hint shows that the toolbar can expand, without changing the saved choice
5. The toolbar is collapsed and shows that it can expand
""")
for s in ("LIFE-169","LIFE-170","TRUST-001"):
    print(s, drop("SwRS-MDOKFSTUDIO-"+s,"derives_from",["StRS-MDOKFSTUDIO-TOOLBAR-001"]), get_list("SwRS-MDOKFSTUDIO-"+s,"derives_from"))

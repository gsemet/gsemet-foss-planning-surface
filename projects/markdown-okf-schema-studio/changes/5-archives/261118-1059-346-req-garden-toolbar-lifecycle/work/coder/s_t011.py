from st import *
A="StRS-MDOKFSTUDIO-TOOLBAR-011"
set_description(A,"When a reader clicks a link in the preview, the Studio SHALL open its target, or refuse it with a reason, show in the tooltip of a link that comes into view the file it leads to or the reason it cannot be followed, and never open from a link in the page a file outside the workspace roots.")
set_need(A,"As a reader, I click a link and land on the right document, line, heading or web page. When a link cannot be followed I am told why. I rest the pointer on a link and read where it goes before I click, and a small warning icon next to a link tells me that its target is missing or blocked. A link in the page cannot take me to a file outside my workspace.")
t=rd(A)
old="- A link to a missing or blocked target keeps its text and colour; a small warning icon follows it and its tooltip names the problem.\n"
assert old in t
wr(A,t.replace(old,old+"- The setting that allows frontmatter links to files outside the workspace belongs to the frontmatter links use case (StRS-MDOKFSTUDIO-FMSCHEMA-014); links in the page never use it.\n"))

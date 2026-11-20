from st import *
A="StRS-MDOKFSTUDIO-LIFE-021"
t=rd(A)
old="- A setting that is not set reads as its default; a stored value of the wrong type is normalized.\n"
assert old in t
wr(A,t.replace(old,old+"- The groups come in a fixed order (Preview, Editing, Frontmatter, Comments, PlantUML), and a setting keeps the same place from one release to the next, so that the reader finds it where they found it before.\n- Every setting carries a description that says what it changes and what its default is, so the reader does not have to read the documentation to set it.\n"))
set_main_paths(A,"""#### Path 1: Find and set a Studio setting

1. The reader opens the settings editor
   - SwRS-MDOKFSTUDIO-LIFE-156: the Studio settings are listed in the groups Preview, Editing, Frontmatter, Comments and PlantUML, in that order
2. The Studio settings are listed in their groups
   - SwRS-MDOKFSTUDIO-LIFE-156: each setting shows its default and a description
   - Option SwRS-MDOKFSTUDIO-LIFE-156 (boundary): a setting with nothing stored reads as its default
3. Each setting shows its default and its description
""")

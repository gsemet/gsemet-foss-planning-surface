from st import *
A="StRS-MDOKFSTUDIO-TOOLBAR-006"
set_need(A,"As a reader, I open a table of contents next to a long document when I want an overview. I close it when I want the room, and the preview remembers my choice. In the table of contents I see where I am, I fold the sections I do not need, and I click a heading to go there without leaving the document. I read the document and the table of contents side by side, and neither hides part of the other.")
for s in ("LIFE-169","LIFE-170"):
    print(drop("SwRS-MDOKFSTUDIO-"+s,"derives_from",[A]))

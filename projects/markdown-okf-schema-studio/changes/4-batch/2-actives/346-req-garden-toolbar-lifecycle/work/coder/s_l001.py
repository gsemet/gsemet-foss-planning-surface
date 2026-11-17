from st import *
A="StRS-MDOKFSTUDIO-LIFE-001"
set_main_paths(A,"""#### Path 1: Open a side preview

1. A saved Markdown file is the active editor
   - SwRS-MDOKFSTUDIO-LIFE-003: the reader runs Open Preview to Side and a preview opens beside the editor, or is revealed if one is open
   - Option SwRS-MDOKFSTUDIO-LIFE-003 (refusal): a file that is not a saved .md file opens no preview and shows a message
2. A side preview is open beside the editor
   - SwRS-MDOKFSTUDIO-LIFE-151: the preview locks its editor group, so the files the reader opens next are shown in another group
   - Option SwRS-MDOKFSTUDIO-LIFE-149 (nominal): the built-in Markdown preview, its commands and its settings stay as they were, beside the Studio preview
   - Option SwRS-MDOKFSTUDIO-LIFE-038 (nominal): several previews can be open, each with its own state and only the newest following the active editor
3. The side preview is open and the editor group is locked

#### Path 2: Open as a tab

1. A saved Markdown file is the active editor
   - SwRS-MDOKFSTUDIO-LIFE-018: the reader opens it through Open With and the file shows in a tab that keeps showing it
   - Option SwRS-MDOKFSTUDIO-LIFE-018 (refusal): a document that is not a saved Markdown file is not opened
2. The file is shown in a Studio tab
""")

from st import *
A="StRS-MDOKFSTUDIO-LIFE-022"
t=rd(A)
t=t.replace("### Preserved stakeholder intent\n\n## User Need\n\n","### Preserved stakeholder intent\n\n")
i=t.index("### Rationale and constraints")
t=t[:i]
t+="""### Rationale and constraints

- Closing a preview panel or a document stops the preview's render queue, pending render stages, file watchers, subscriptions and Problems entries, so that no late result reaches the panel.
- What another live preview still uses is kept: its watcher and the Problems entries of a file it shows.
- Removing a workspace folder keeps the panel open and shows the file with restricted reads, and the reading state is kept; adding a folder that holds the file back gives the preview its full reads again.
- Deactivating the extension disposes the previews' work and leaves the panels to VS Code, which restores them later.
- No file is ever changed by closing.

### Main paths

#### Path 1: Close a preview

1. A preview is open, rendering or idle
   - SwRS-MDOKFSTUDIO-LIFE-143: the reader closes the panel or the document, and the preview stops its render queue, watchers and Problems entries
   - Option SwRS-MDOKFSTUDIO-LIFE-143 (boundary): another live preview of the same root or file keeps its watcher and its Problems entries
2. The preview has left nothing behind

#### Path 2: Remove the folder of a preview

1. A preview shows a file of a workspace folder
   - SwRS-MDOKFSTUDIO-LIFE-143: the reader removes the folder, the preview's work is disposed and the same panel shows the file again with restricted reads
   - Option SwRS-MDOKFSTUDIO-LIFE-143 (boundary): a removed folder with no document to show disposes the preview and its panel
2. The preview shows its file with restricted reads
   - SwRS-MDOKFSTUDIO-LIFE-143: a folder that holds the file is added back and the preview gets full reads again on the same panel
3. The preview has full reads again

"""
wr(A,t)
set_list("SwRS-MDOKFSTUDIO-LIFE-143","derives_from",[A])
# LIFE-014 narrowing
B="StRS-MDOKFSTUDIO-LIFE-014"
set_title(B,"Previews come back after a reload, and each document keeps its reading place and view choices")
set_description(B,"When VS Code restores its window or a reader returns to a document, the Studio SHALL bring the previews back on their documents at the reading state they had, give each document its own reading place and view choices, and keep the view choices the reader made for the workspace, leaving every file as it was.")
set_need(B,"As a reader, I reload the window and my previews come back on the same documents, at the same place, with their open sections. I return to a document and find it at its own place, with its own Description choice. The view choices I made (zoom, width, table of contents and the others) are found again when I reopen a preview of the same workspace.")
t=rd(B)
old="- Deactivating the extension leaves the panels to VS Code, which restores them later.\n"
assert old in t
t=t.replace(old,"- A view choice only changes how the preview looks, never the document, so every preview accepts it, whatever the trust.\n- A value that is not valid for its choice is refused, and a stored value that is not valid falls back to the default of that choice alone.\n- The collapsed toolbar is one of these choices; the meaning of zoom and width is described in the theme-zoom and layout-width scopes.\n")
wr(B,t)
print(get_list("SwRS-MDOKFSTUDIO-LIFE-143","derives_from"))

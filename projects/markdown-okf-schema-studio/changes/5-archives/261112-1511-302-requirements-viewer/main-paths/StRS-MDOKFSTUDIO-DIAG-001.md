### Main paths

#### Path 1: Insert a diagram, break it, fix it

1. Edit mode is on with the GFM palette
   - SwRS-MDOKFSTUDIO-DIAG-017: the writer clicks Mermaid in the palette
   - Option SwRS-MDOKFSTUDIO-DIAG-017 (refusal): the Strict or MyST palette offers no Mermaid
2. A starter fence is in the document
   - SwRS-MDOKFSTUDIO-DIAG-001: the page renders the fence
   - Option SwRS-MDOKFSTUDIO-DIAG-001 (boundary): an empty fence is left blank
3. The diagram is drawn as a picture
   - SwRS-MDOKFSTUDIO-DIAG-127: a click on the picture opens its source
   - Option SwRS-MDOKFSTUDIO-DIAG-009: text typed elsewhere keeps the drawing
4. The source editor is open
   - SwRS-MDOKFSTUDIO-DIAG-015: an invalid line is saved
5. A parser message shows, the source stays
   - SwRS-MDOKFSTUDIO-DIAG-001: the writer fixes the source
6. The diagram is drawn again in the theme colours

#### Path 2: Switch the theme

1. The diagram is drawn as a picture
   - SwRS-MDOKFSTUDIO-DIAG-005: the reader changes the theme
   - Option SwRS-MDOKFSTUDIO-DIAG-005 (boundary): the colours stay the same, nothing is redrawn
2. The diagram is redrawn in the new theme, labels kept

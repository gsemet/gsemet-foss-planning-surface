# Mermaid flowchart labels sit at the top of their boxes in a real VS Code export

Found on 2026-11-11 (release 1.7.0 check, fixture 87-export-html, Cream): in the file written by
Export to HTML in real VS Code, the labels of the flowchart boxes sit at the top of the boxes
instead of their middle.

CR 299 (PR #369) could not reproduce it in the visual campaign: there the labels are centred in
both the preview and the export, and the export embeds the same SVG as the preview. The cause is
likely font metrics in the real webview or in the browser that opens the file.

Expected: compare the preview and the export of the same diagram in real VS Code (and the
exported file opened in a browser); centre the labels wherever they are off.

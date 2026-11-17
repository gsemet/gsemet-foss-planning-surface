# Mermaid node and edge labels are clipped in the real VS Code webview

Source: demo video track B (real VS Code 1.143 window, clean profile), 2026-10-28.

In the webview, flowchart labels lose their last characters: "under 10 mi", "Swap with a spar",
"Call the control roc". The same diagram renders whole in the headless harness, so the cause is
likely font metrics at measure time (font not yet loaded, or a different font in the webview).
Evidence: /private/tmp/claude-502/cr170-b/out/demo-b-contact-sheet.png (tile 6). Needs a real-input
check that asserts label boxes are not narrower than their text.

## Decision (user, 2026-10-28)

Not a 1.0.0 blocker; stays P2.

## Also seen in the README

The real-window README picture `myst-diagrams-and-figure` (PR #184, from heavy run 40762299560)
shows clipped labels ("Nc", "Hold and inspe"). Regenerate that picture once fixed.

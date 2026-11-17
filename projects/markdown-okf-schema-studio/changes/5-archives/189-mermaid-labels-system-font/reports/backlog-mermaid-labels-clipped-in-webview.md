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

## Status after CR 178 (2026-10-29, PR #191 kept as a draft, out of the 1.0.1 stack)

- `htmlLabels: false` (SVG text) showed whole labels in the real window (heavy run 40784166335,
  README picture at `ef81a610`); the owner rejected it for now — see P3 `mermaid-svg-text-labels`.
- Waiting for `document.fonts.ready` before the first render does NOT fix it: real-window picture from
  heavy run 40787817885 still shows "Yes|", "Nc", "Hold and inspe" (byte-identical to main's README
  picture). Screenshot: `/private/tmp/claude-502/cr178-driver/after-fonts-wait-only.png`.
- The clipping appears only in the shown image: the SVG is displayed as a data-URI `<img>`, which
  cannot use the page's `@font-face` fonts, so text measured in the page is drawn wider in the image.
- Candidates: pin an explicit font family and size in Mermaid's theme variables (a font the `<img>`
  context also has); render the SVG inline instead of as an `<img>`; or SVG text (P3 item).
- Test gap: the real-input label-fit check measures in the page, not the shown image, so it passes
  while labels are cut. A real guard must measure the image (pixels, or the image box vs text).
- PR #191 (`change-requests/178-mermaid-labels-clipped`, head `ca12066f`) holds reusable groundwork:
  the fonts wait, its unit test, the HTML-label real-input check, visual-harness probe node.

## Fixed by CR 189 (PR #191, head f32c9534) — close when #191 merges

Real cause: the page CSP (nonce-only `style-src`) blocks the `<style>` Mermaid injects in its temporary
measuring SVG, so labels were measured at the body font/size but drawn at 16px in the data-URI image
(the repo has no `@font-face`). Fix: Mermaid measures inside a nonce-styled `div.myst-mermaid-measure`;
measure element and Mermaid config share one pinned system font stack at 16px; HTML labels kept.

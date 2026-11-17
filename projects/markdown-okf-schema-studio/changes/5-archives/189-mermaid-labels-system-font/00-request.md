# 189 — Mermaid labels clipped in the webview: same font in page and image

Type: fix · Priority: P2 · Owner decision 2026-10-29 (via the Chief of Staff), after CR 178 showed that
waiting for fonts does not fix it. Backlog intent and CR 178 findings: `reports/backlog-intent.md`.
Previous round reviews: `../178-mermaid-labels-clipped/reviews/`.

Branch: reuse `change-requests/178-mermaid-labels-clipped` (draft PR #191, worktree wt-178, head
ca12066f) — it holds the groundwork (fonts wait, unit test, HTML-label real-input check, visual probe).

Constraint (owner): keep Mermaid's HTML labels. `htmlLabels: false` is not allowed.

Diagnosis so far: the diagram is shown as a data-URI `<img>`; an SVG inside `<img>` cannot use the
page's `@font-face` fonts, so text measured in the page is drawn wider in the image.

Order of attempts:
1. Pin a font that exists in BOTH contexts (a system font stack, no `@font-face` font) via Mermaid
   `themeVariables.fontFamily` / config `fontFamily`, so measure and draw use the same metrics.
2. If not enough: render the SVG inline instead of as an `<img>`, with the same sanitisation as
   today. First find and record (reports/img-security-reason.md) why the `<img>` was chosen: code
   comments, requirements (DIAG-*, TRUST-*, security), git log.

Proof (all required):
- real-window picture from a heavy run shows "Yes", "No", "Hold and inspect" whole;
- fix the test gap: the label-fit check measures what the IMAGE draws (e.g. render the SVG data URI
  into a canvas / compare text box vs node inside the image document), not the page;
- regenerate `images/readme/myst-diagrams-and-figure.png` from that heavy run (only that picture);
- CHANGELOG and DIAG SwRS text describe the real fix.

If proven: #191 goes back to ready (title/body rewritten) and joins the stack below the 1.0.1 PR.
If not proven after round 3: no partial fix; #191 stays draft; the backlog item stays open.

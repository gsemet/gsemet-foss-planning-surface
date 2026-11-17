# Known issues K1, K3 (P1, decided 2026-10-22)

Found by the P9 visual campaign (scenarios tagged `knownIssue`); not fixed in PR #11.
When a fix lands, remove `knownIssue` from its scenarios (v17/v18 keep it until K2 is fixed too).

- **K1 overflow.** A long unbroken word and a long bare URL (autolink) are wider than the pane: the
  word overflows its paragraph, the link makes the whole page scroll horizontally (1093 px at 900,
  1058 px at 460). Scenarios rendering-core/v17, v18 (fixture 35-cjk-rtl). Likely fix:
  `overflow-wrap: anywhere` on paragraphs/links.
- **K3 Mermaid error duplication.** An invalid Mermaid diagram gets one more "Unable to render
  Mermaid diagram" line on every re-render (each theme switch adds one; 55 after the toolbar checks).
  Scenarios diagrams/v08, v09 (fixture 40-mermaid-error). Fix: replace the previous error element
  in `mermaidPreview.ts`.

Note from P9 B4: `knownIssue` masks a whole scenario; consider per-assertion `knownIssue`.

K4 (Caution colour) split out on 2026-10-22 → `requests/022-caution-alert-style` (archives/022 once landed).

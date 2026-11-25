# Answers

Source CR: `vega-charts-readable-legends-hover-detai`. Its Q4, Q8, Q11, Q12 and Q13 apply here. The
first specification, of which sections 2, 3 and 5 are this CR's, is kept at `work/first-spec.md`.
The candidate renderings, the hover mock the Fable critic judged and the probe are in the source
CR's `work/exploration/`.

1. live-Q1 (2026-11-25, the owner, relayed by the Chief of Staff): **A hover detail on charts by default, for Vega-Lite, in a small themed box.** The owner asked in the source CR whether a hover detail could be the default on charts. The Chief of Staff gave it a CR of its own when splitting the change (source Q11).
2. live-Q2 (2026-11-25, Chief of Staff): **Routine points are the Griller's; a behaviour choice that truly needs the owner goes to the Chief of Staff.**
3. live-Q3 (2026-11-25, decided by the Griller from the code, source Q4): **The chart becomes a live Vega view in the preview, because an image gets no hover.**
   - Today `drawChart` runs the view with `renderer: "none"` and `view.toSVG()`, and `vegaPreview.ts` shows an `<img>` (data URL).
   - The preview now mounts `new View(..., { renderer: "svg", loader, expr: expressionInterpreter, tooltip })`, with the same loader and interpreter. DIAG-122 (allowed data only, `href` refused) and DIAG-124 (no eval) keep their behaviour.
   - The view mounts into a child `div.myst-vega-view`, never into `div.myst-vega-diagram`: `View.initialize` clears its element and sets a role and an aria-label, which would overwrite the diagram's.
   - `drawChart`, the SVG-string path, stays for the unit tests.
4. live-Q4 (2026-11-25, Chief of Staff on the spec critic, source Q12): **The hover default goes to Vega-Lite only.**
   - Vega-Lite compiles with `config.mark.tooltip: true`. A spec's own `tooltip` encoding, or `"tooltip": null`, wins.
   - A full Vega spec never gets it: no config can add one, and Studio rewrites no spec.
   - A unit test proves that a full Vega mark with no tooltip encode has a null tooltip.
5. live-Q5 (2026-11-25, the owner's wish and the Fable critic's verdict, source Q8): **The hover detail is a themed box of Studio's own, never the native `title` tooltip.**
   - The native tooltip comes late, in the OS style at a small fixed size, and ignores theme and zoom.
   - The box is a new `src/page/modules/chartTooltip.ts`, given to the view as its `tooltip` handler.
   - One shared element sits on `document.body`, outside the content, so the export and the morph never see it.
   - It shows key and value rows, built with `textContent`: muted key, bold value.
   - It takes the page's background, colours and font, at the legend label size.
   - Border: 1 px, stronger in dark (the critic found it faint there). Radius 4 px and a light shadow, as in the judged mock.
   - It is offset from the pointer and flips at the viewport edge, so it does not cover the neighbouring mark (a critic finding).
   - It hides on a null value, on scroll, on a content update and when its chart is redrawn.
   - It is placed with CSSOM only: no `style` attribute, no new dependency.
6. live-Q6 (2026-11-25, Chief of Staff, source Q12, first spec open question 1): **Vega's own pointer interactions run in the live view; its input widgets do not.**
   - Selections, hover encodings, zoom and pan from a spec's signals work.
   - `config.events.bind: "none"` turns input bindings off, and `href` stays refused.
   - The Limits line of `docs/user/charts.md` says "input bindings and links are not available".
7. live-Q7 (2026-11-25, Chief of Staff, source Q12, first spec open question 2): **No canvas fallback.** If the SVG renderer violates the page's CSP, the Driver stops and reports to the Chief of Staff instead of shipping. A canvas would export an empty chart, since the export clones the DOM.
8. live-Q8 (2026-11-25, Chief of Staff, source Q12): **The export keeps a static picture.**
   - The export clones the page content, so a chart is exported as its drawn inline SVG, with no hover box and no script.
   - Gradient references are rewritten to local `#id`; the export test uses a gradient chart.
   - `whenDiagramsSettled` (DIAG-128) still waits for every chart.
9. live-Q9 (2026-11-25, decided by the Griller, first spec section 2): **The drawing cache keeps detached live views.**
   - It holds at most 16 views by key and finalizes a view evicted while detached.
   - A view is reused only when its host is detached, after a keyed morph replaced the block. Two identical charts on one page each get their own view.
   - The key carries the body font size from the source CR's sizes, so a change of font size or zoom redraws the chart.
   - A late result for a key no longer shown is cached and not shown, as today (PERF-07, DIAG-009).
10. live-Q10 (2026-11-25, Chief of Staff, source Q12): **Proof in a real window and on the real page.**
    - The real-window integration test opens a chart document and proves a live `svg`, a hover box and no CSP violation.
    - The zoom, edit-click and find tests run on a page that bundles the page runtime with `vegaPreview.js`.
    - The Chromium CSP test proves that the box shows on a Vega-Lite bar, and not on a full Vega mark with no tooltip.
11. live-Q11 (2026-11-25, Chief of Staff, source Q12): **The legend swatch stroke width of the source CR stays.** If the new screenshots show bloated filled swatches, it is dropped and the PR says so.
12. live-Q12 (2026-11-25, Chief of Staff, source Q13): **This CR updates the clip scenarios that select `img.myst-vega-image`, since it is the one that replaces the image with the live view.** That means theme-switch, plus CR-493 and CR-500 as merged by then.
13. live-Q13 (2026-11-25, decided by the Griller, first spec section 7): **Requirements, docs and screenshots.**
    - Requirements:
      - DIAG-123 gets the live themed view and its hover part;
      - DIAG-128: export as the drawn inline SVG with no hover;
      - DIAG-009: reuse of detached views only;
      - StRS-MDOKFSTUDIO-DIAG-015, path 1 step 3: "a themed live SVG with hover detail", an editorial change since the StRS is proposed.
    - The markers move with the code into the split modules.
    - `docs/user/charts.md` says how to turn the hover off (`"tooltip": null`) and that a full Vega spec shows only its own tooltips. The writing skill gets the same lines if it covers charts.
    - Screenshots: the hover box in Cream and in dark.
    - Then `just requirements-update` and a dated log entry.

Grilled enough (2026-11-25): by the Griller, from the source CR's grill, its Fable critic and spec critic, and the Chief of Staff's split decisions; no owner question left.
Destination: running batch batch-09, after vega-charts-readable-legends-hover-detai and the clips. Critic: yes (the source CR's Fable critic on the hover mock, and its spec critic).

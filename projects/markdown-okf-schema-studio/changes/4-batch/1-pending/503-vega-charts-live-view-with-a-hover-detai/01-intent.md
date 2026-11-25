# Vega charts: live view with a hover detail

The owner wants a hover detail on charts by default. Today a Vega-Lite or Vega chart is shown in
the preview as an image, which receives no mouse event, so no hover detail can show.

This change draws each chart in the preview as a live Vega SVG view. Hovering a Vega-Lite mark
shows a small box in the page's own colours, with the mark's fields as key and value rows. A full
Vega spec shows the tooltips it defines itself; Studio adds none to it.

The HTML export keeps a static picture: the drawn SVG, with no hover box and no script. Chart data
loading and the page's security rules (no eval, no network, no inline style) are unchanged.

This CR is the second half of "Vega charts: readable legends, hover detail, no Chart source", which
the Chief of Staff split after the spec critic. It comes after that CR in the stack.

# Decisions (owner, 2026-11-03)

- One CR with [unnecessary-table-margin-breakage](../unnecessary-table-margin-breakage/01-intent.md):
  it applies variant D of the prototype (token columns never wrap and size to their widest cell;
  prose columns need about 20ch; the table stays in the column when the minimums fit, otherwise it
  breaks out to its natural width capped by the page). Auto width mode only.
- The case of this item is covered: a cell holding content that cannot shrink (a code block, an
  admonition with a code block, a long unbroken line) makes the table break out.

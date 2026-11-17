# A refused block open leaves an empty, stuck frame

User decision (2026-10-25): P2.

Current behaviour (SwRS-MDOKFSTUDIO-BLOCK-216, BLOCK-039, TABLE-034, BLOCK-134, BLOCK-160, Known
issue): the status line of a block editor ("Loading Markdown source…", or the refusal reason) is
attached to the frame only when the source arrives. After a refused open the writer sees an empty
frame with no reason, no Done/Cancel, no Escape; the Refresh button stays disabled and a click on
another block opens nothing, until a render patches the page or edit mode is turned off. The table
cell editor shows the reason but is stuck the same way. A block move refused after a key press
shows no reason (only an arrow click marks the bar pending).

## Expected

- The status line is in the frame from the start: "Loading…", then the refusal reason.
- After a refusal the writer can leave: the frame closes after showing the reason, or keeps at
  least Cancel and Escape; other blocks can be opened again.
- A refused keyboard move shows its reason.
- Page tests; update the listed SwRS in the same change.

Requirement ids older than the baseline merge map to their current tile in `.agents/changes/archives/059-requirements-okfreq/reduction/mapping.csv`.

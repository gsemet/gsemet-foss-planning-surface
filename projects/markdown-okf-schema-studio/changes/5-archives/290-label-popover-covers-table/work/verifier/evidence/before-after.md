# CR 290 before / after (pane 290 px, edit mode, Rename label popover open on `table-label`)

Source: https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/d4a9ba6698edff18035c36d77079923c9e6227cf/
Downloaded here (curl exit 0 each, 580x1600 PNG at 2x): v46-before-light.png, v46-after-light.png, v46-before-dark.png, v46-after-dark.png

- v46-before-light.png: the popover sits right under the anchor icon, over the table header (Name / Value) and the `alpha` row; only `beta` and `gamma` rows are visible. It is 322 px wide and runs off the right edge of the 290 px pane.
- v46-after-light.png: the popover sits above the icon, over the end of the paragraph before the table (accepted trade); the full table (Name, Value header, alpha, beta, gamma) is visible and uncovered; the popover fits inside the pane with an 8 px margin on both sides.
- v46-before-dark.png: same as before-light in the dark theme (header and `alpha` hidden, popover overflows right).
- v46-after-dark.png: same as after-light in the dark theme (popover above the icon, table fully visible, inside the pane).

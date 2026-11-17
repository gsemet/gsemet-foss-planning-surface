# Edition Palette

When the edition mode is enabled, add a new floating palette bellow the existing one.

It will receive edition options. Make it extentable. beautifu, simple, user friendly
keep harmony with the existing floating panel

Every non-supported edition in the code should result in new feature added to the code.

## Additional buttons in  Preview and editor floating panel

- back
- next (to navigate back to the page after a click on a link)
- zoom in/out
- switch left/right margin on/off

split on 2 lines

## Select box: edition mode

- strict markdown
- GitHub Flavored Markdown (GFM)
- MyST Markdown (incl. GFM)

This select allow to show button configuration

## Placement

On top of the block under edition

On table cell edition, there is an existing one
we need to determine if we merge or shift the existing one to let room for the new one

## Strict markdown buttons

- title (show dropdown to select level h1-h5)
- italic
- bold
- strikethrough
- code -> create triple backtick block + display dropdown for list of programming languages
- link (Ctrl + K shortcut). The potential highlighted text becomes the link text and caret placed
  at link location place.
- blockquote
- horizontal rule
- table -> like word, a submenu to select number of line and columns by simply showing a grid preview
  (one-click selection, max 9x9, on hover highlight the corresponding grid cells)
- images (open a file picker to select an image, default on the current md folder)
- emoji picker
- html color picker (self-actived when a color code is detected)
- TODO indicator (icon + text on hover). self activate on ctrl+/
  (catch the vscode shortcut code code line comment)

## GitHub Flavored Markdown (GFM) buttons

keep the existing buttons and add the following for GFM:

- admonition (GFM only) -> print the block definition `>` + show at cursor place dropdown
  for selecting admonition type (note, tip, warning, etc.)
- checkbox
- html table (a second button to convert a md table to html-in-md table, add new table)

propose others

(myst-markdown)=
## MySt Markdown

Inspect the book/ folder for syntax and configuration and find all supported features.
propose me a curated list of the important MyST Markdown features.

At minimal:

- admonition (all types + custom)
- footnotes
- definition lists
- math (LaTeX)
- subscript and superscript
- figures, image with caption
- anchors edition (show icon where anchor is placed, on click, allow edition

## Custom editor

- Figure (size, caption, legend,... propose other idea) -> "edit" button on an existing figure or a dedicated button in the floating edit bar
- color picker (allow to select text and background color) -> floating button
- emoji picker (allow to insert emojis at the cursor position) -> floating button
- URL (on a selection then Ctrl+k/cmd+k or the floating button, display a little panel with 2 fields, text (prefilled with selection) and link, default focus on the first empty field)

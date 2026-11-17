when mouse hover a table, little accent on the table raw.

by default, the odds and even rows has slightly different backrgound colors.

highlight is more marked

table heading even more.

## Prototypes

Three options, each in the Cream, White and Dark themes. All use the existing theme tokens through
`color-mix`, so they also follow a VS Code theme. The third body row is shown as hovered.
To try the real hover, open [table-row-hover.html](prototypes/table-row-hover.html) in a browser.

Today the page has no odd and even row colours and no row hover: the three options add both. Even
rows are the same in all of them: the text colour at 3%.

### A. Quiet

The neutral text colour only: hover at 8%, heading at 14%. Nothing new on the page, but the hover
is faint in Dark.

![Option A in the three themes](prototypes/option-a.png)

### B. Accent tint

The theme accent tints the hovered row at 12% and the heading at 24%. The clearest of the three, and
the table takes the colour of the theme.

![Option B in the three themes](prototypes/option-b.png)

### C. Accent edge

Neutral rows (hover at 6%, heading at 10%). The accent is only a 3 px bar on the hovered row and a
2 px line under the heading. The most discreet, but the bar sits where the row handles appear in
edit mode.

![Option C in the three themes](prototypes/option-c.png)

## Choice

Which option do we build?

- ( ) A. Quiet
- (x) B. Accent tint (recommended)
- ( ) C. Accent edge

## To check when building

- The frontmatter properties table (`.okf-properties`) sizes and styles itself: decide whether it
  gets the same hover.
- Edit mode: the hover must stay below the row and column handles, the cell selection and the
  change bars.
- The heading colour replaces `--studio-textBlockQuote-background` in
  `src/core/preview/styles/contentBlockStyles.ts`.




# show: resolve concept names given without the .md extension

issue: https://github.com/gsemet/okf-schema/issues/56

## Intent (from the ticket, not grilled yet)

`okf-schema show` answers "Concept not found" for a name without `.md`, the form the Getting
Started and knowledge-graph tutorials use. `new` and `backlinks` accept that form. The ticket
suggests trying `<name>.md`, or fixing the tutorials if the extension is required.

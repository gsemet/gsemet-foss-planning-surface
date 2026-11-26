# Field row with a validation error has no red style in a bundle

In a bundle with a schema, a frontmatter field with a validation error (for example `status: publshed` against an enum) shows only a small uncoloured badge. The row `tr[data-okf-field].okf-error` carries the class `okf-error` in the DOM but has no visible style: only `.okf-info-row.okf-error th` is styled (src/core/preview/styles/propertiesStyles.ts). Expected: the field row is visibly red, as the information rows are. Found while filming the bundle frontmatter clip (CR-499). Confirm first that this is a gap and not intended.

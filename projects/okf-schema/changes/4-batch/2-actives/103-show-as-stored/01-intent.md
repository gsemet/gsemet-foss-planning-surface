# show: print the stored file, without the trust line

issue: https://github.com/gsemet/okf-schema/issues/58

## Intent (grilled 2026-11-25, see 02-answers.md)

`okf-schema show` re-serializes the frontmatter (style and comments are lost), invents an empty
block for a file without frontmatter or with invalid YAML, and prints `trust:` inside the
document.

`show` must print the stored file as it is, without validating it, and no longer print `trust:`
or `stale: true`. The result of the API `show_bundle` gains the exact stored text.

A new command, `okf-schema trust`, prints those lines instead, and is documented (added
2026-11-25, answers 9 to 12). It stacks on `trust-actor-forms`, which makes the tier right.

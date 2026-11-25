# show: stray trust line and reformatted frontmatter

issue: https://github.com/gsemet/okf-schema/issues/58

## Intent (from the ticket, not grilled yet)

`okf-schema show` appends `trust: unverified` after the closing `---`, where it reads as body
text, and re-serializes the frontmatter in another style than the stored file. The ticket expects
the document printed as stored, with any trust status clearly separated (labelled header, stderr
line or `--trust` option).

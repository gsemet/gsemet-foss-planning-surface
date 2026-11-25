# index: keeps broken links in root summaries, validate misses them

issue: https://github.com/gsemet/okf-schema/issues/57

## Intent (from the ticket, not grilled yet)

`okf-schema index` keeps an existing root-index summary verbatim, including relative links that
resolve only from the subdirectory, and `okf-schema validate` does not check links in
`index.md` files. The ticket asks for at least one of: regenerate or rebase the summary's links,
or report W2 for broken links in `index.md`.

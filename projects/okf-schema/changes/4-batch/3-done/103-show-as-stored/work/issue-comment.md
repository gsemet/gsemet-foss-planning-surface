Thanks for the report. This is accepted, and we reproduced it. It is broader than described: `show` also drops YAML comments, and for a file whose frontmatter is missing or is not valid YAML it prints an empty `{}` block.

- `okf-schema show` will print the stored file as it is, with nothing added.
- It will no longer print the `trust:` and `stale: true` lines, and no `--trust` option replaces them. The trust tier will then appear in no command; `list` still marks stale concepts with `[STALE]`.
- `show` will not validate the file: a damaged file is printed as it is. Use `okf-schema validate` to check it.
- In the Python API, the result of `show_bundle` gains a field with the exact stored text; its current fields do not change.

Planned as a fix release. No date yet; the pull request will be linked here.

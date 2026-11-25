Thanks for the report. This is accepted.

- `okf-schema show` will accept a concept name with or without `.md`: the exact path when it is a file, otherwise `<name>.md`.
- `show` on a directory with no matching concept will report "Concept not found" (exit code 2) instead of a Python traceback.
- `show` will refuse a path that leaves the bundle, including a symlink that points outside it (an OKF bundle is self-contained).
- The Python API `show_bundle` will raise `FileNotFoundError` in these cases.

Not part of this change: applying the outside-symlink rule to the other commands (a separate change), the `trust:` line and frontmatter formatting of `show` (#58), and "did you mean" suggestions.

No date yet; the pull request will be linked here.

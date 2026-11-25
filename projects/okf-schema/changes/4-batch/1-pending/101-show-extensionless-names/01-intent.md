# show: resolve concept names given without the .md extension

issue: https://github.com/gsemet/okf-schema/issues/56

## Intent (grilled on 2026-11-25; the decisions are in `02-answers.md`)

`okf-schema show` accepts a concept name with or without `.md`, the form the tutorials use. It
opens only what is inside the bundle, symlinks included, and fails with a plain "not found"
error instead of a traceback. The other commands' symlink handling is a separate item
(`bundle-outside-symlinks`); the output's format is issue 58.

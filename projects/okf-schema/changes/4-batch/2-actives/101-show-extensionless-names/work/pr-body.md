## Description

`okf-schema show --path <bundle> api/health-check`, the form the Getting Started and
knowledge-graph tutorials use, answered "Concept not found". Showing a directory ended in a
Python traceback, and a `../` path or a symbolic link could make `show` read a file outside the
bundle.

With this change, `show` and the Python API `show_bundle`:

- take a concept name with or without `.md`: the exact file first, else the name with `.md`
  added; a directory is never shown;
- read a name from the bundle root, with or without a leading `/`, from any terminal folder, and
  still accept an absolute disk path inside the bundle;
- judge containment on the real path, symbolic links followed, and refuse a path that leaves the
  bundle without reading it (**UNVERIFIED:** for symbolic links, see Known gaps);
- report every refusal as an `Error:` line with exit code 2 (`FileNotFoundError` in the API),
  never a traceback.

Behaviour to know: a script that relied on `show` reading a file outside the bundle, or through a
symbolic link that leaves it, now gets an error. On Windows a name starting with `\` keeps its
Windows meaning (a path from the root of the drive). Git Bash rewrites a leading `/` before
okf-schema receives it; write the name without it, or set `MSYS_NO_PATHCONV=1`. The command
reference documents these limits.

The requirements gain `SwRS-OKFSCHEMA-CORE-010` ("Stay inside the bundle", proposed, applied to
`show` only), and `SwRS-OKFSCHEMA-CORE-005` gains the name resolution scenarios and depends on
it. The command reference and the packaged `okf-schema` agent skill are updated. Unaffected:
scaffold guidance and examples (neither runs `show`), the tutorials (their commands already use
the extensionless form), the feature coverage map (its `show` entry does not change), CI,
`justfile` and packaging.

## Type of Change

- [x] Bug fix
- [ ] New feature
- [ ] Breaking change
- [x] Documentation update
- [ ] Refactoring

## Checklist

- [ ] I have run `just preflight` and all checks pass
- [x] I have added tests that prove my fix is effective or my feature works
- [x] I have updated the documentation accordingly
- [ ] My changes generate no new warnings

## Autonomous decisions

- The real path is computed with `os.path.realpath` rather than `Path.resolve()`: on Python 3.12
  and older, `Path.resolve()` raises `RuntimeError` on a link loop, which would turn "Concept not
  found" into a traceback. A test covers the loop.
- The placeholders in the requirement texts are written as `PATH`, `BUNDLE` and plain words
  instead of angle brackets, which the prose check reports as unfilled.

## Known gaps

- `just preflight` does not pass on the Windows machine used for development: 8 tests that this change does not edit fail because the machine refuses to create symbolic links (WinError 1314). The three requirement checks pass there; the examples, report and documentation steps pass when run on their own.
- **UNVERIFIED:** the symbolic link refusals and the installed-package inspection check. Their new tests were skipped on that machine; they need a run where symbolic links are permitted and a non-Windows run.
- `validate`, `list`, `index`, `backlinks` and `lint` still follow symbolic links whose target is outside the bundle; this change covers `show` only.

## Related Issues

Fixes #56

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
  bundle without reading it;
- report every refusal as an `Error:` line with exit code 2 (`FileNotFoundError` in the API),
  never a traceback.

Behaviour to know: a script that relied on `show` reading a file outside the bundle, or through a
symbolic link that leaves it, now gets an error. On Windows a name starting with `\` keeps its
Windows meaning (a path from the root of the drive). Git Bash rewrites a leading `/` before
okf-schema receives it; write the name without it, or set `MSYS_NO_PATHCONV=1`. On a
case-insensitive file system such as macOS, an absolute path whose bundle part is spelled in
another letter case than the real path of `--path` is not recognized as inside the bundle and is
reported as not found, although such a path was read before. The command reference documents these
limits.

The requirements gain `SwRS-OKFSCHEMA-CORE-010` ("Stay inside the bundle", proposed, applied to
`show` only), and `SwRS-OKFSCHEMA-CORE-005` gains the name resolution scenarios and depends on
it. The command reference and the packaged `okf-schema` agent skill are updated. Unaffected:
scaffold guidance and examples (neither runs `show`), the tutorials (their commands already use
the extensionless form), the feature coverage map (its `show` entry does not change), CI,
`justfile` and packaging.

## Deliverables

What `okf-schema show --path <bundle> NAME` answers, before at `2f09cef` and after at `41fcd6d`
(Windows 11, Python 3.12.10). `leak.md` is a symbolic link in the bundle to a file outside it.

| `NAME` | Before (`2f09cef`) | After (`41fcd6d`) |
|--------|--------------------|-------------------|
| `api/health-check`, `/api/health-check` | not found, exit 2 | concept shown, exit 0 |
| `/etc/passwd` | not found at the drive root, exit 2 | not found inside the bundle, exit 2 |
| `api` (a directory), `.` | `PermissionError` traceback, exit 1 | `Concept not found`, exit 2 |
| `../../secret.md`, an absolute outside path, `leak.md` | outside file printed, exit 0 | `Concept path is outside the bundle`, exit 2 |
| `../../secret`, `../../missing`, `leak` | not found, exit 2 | outside the bundle, exit 2 |
| `\api\health-check` | not found at the drive root, exit 2 | outside the bundle, exit 2 |
| a name with `.md`, an absolute inside path, `api/../api/health-check.md` | shown | shown (unchanged) |

When a file `bundle.md` sits beside a bundle folder named `bundle`, `.` is refused as outside the
bundle instead of not found.

## Type of Change

- [x] Bug fix
- [ ] New feature
- [ ] Breaking change
- [x] Documentation update
- [ ] Refactoring

## Checklist

- [x] I have run `just preflight` and all checks pass
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

- `validate`, `list`, `index`, `backlinks` and `lint` still follow symbolic links whose target is outside the bundle; this change covers `show` only.
- The requirements change log entry records a verification run made on a host that refused symbolic links; it does not mention the later full run at the same commit, which passed. It was left because changing it would move the verified commit.

## Test plan

- [x] New or changed tests: with the sources at `2f09cef`, 22 of the 37 selected `show` tests fail;
  at `41fcd6d`, all 37 pass
- [x] Local gates at `41fcd6d`: `just preflight` passes (1129 tests passed, 12 skipped: the
  installed-package acceptance tests, which do not run on Windows)
- [x] Evidence: before at `2f09cef`, after at `41fcd6d`
- [x] Review: approved at `41fcd6d`
- [x] Verified at `41fcd6d`
- [x] CI green at `41fcd6d`: Python 3.10 to 3.13, macOS and Windows jobs pass (the release tagging
  job is skipped outside the default branch); the symbolic link tests run on every job, and the
  installed-package inspection test passes on the non-Windows ones

## Related Issues

Fixes #56

## Internal references

- CR-101 show-extensionless-names.
- Text outputs kept with the change request, under `work/verifier/evidence/`: `before-show.txt`,
  `after-show.txt`, `before-tests.txt`, `after-tests.txt`, `after-scenario-powershell.txt`,
  `after-scenario-git-bash.txt`, `after-probe-names.txt`, `after-other-commands.txt`, and
  `before-after.md`, which lists the pairs and how to reproduce them.

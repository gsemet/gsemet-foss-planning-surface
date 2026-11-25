## Description

`okf-schema show` rewrote a concept before printing it: flow mappings and lists became block
style, dates were rewritten, YAML comments were lost, and a `trust:` line was inserted between
the frontmatter and the body. `show` now prints the concept file byte for byte as it is stored,
and a new `okf-schema trust` command prints the trust tier and staleness.

```text
                     show <concept>                                  trust <concept>
before   rewritten frontmatter, "trust: <tier>",         no such command
         "stale: true" when stale, body
after    the stored file, nothing added, not validated    "trust: <tier>"
                                                          "stale: true" when stale
```

Choices made:

- `show` writes bytes: a file without frontmatter, with invalid YAML or not valid UTF-8 is
  printed as it is, with exit code 0 and nothing on stderr.
- `trust` reads one concept, writes nothing, and answers a file that is not valid UTF-8 with one
  `Error: Concept file is not valid UTF-8: <path>` line and exit code 2.
- The Python function `show_bundle` keeps its fields and gains `raw`, the exact stored text.

**Compatibility:** a script that read the `trust:` or `stale: true` lines of `show` no longer
finds them; `okf-schema trust` prints the same two lines.

This pull request builds on the trust tier fix of #69.

## Type of Change

- [ ] Bug fix
- [x] New feature
- [ ] Breaking change
- [x] Documentation update
- [ ] Refactoring

## Checklist

- [ ] I have run `just preflight` and all checks pass
- [x] I have added tests that prove my fix is effective or my feature works
- [x] I have updated the documentation accordingly
- [ ] My changes generate no new warnings

## Related Issues

Fixes #58

## Blast radius

Grade: 2. The output of an existing command changes and a command is added; a plain revert
restores the previous output. No stored file or data format changes.

## Autonomous decisions

- The requirement scenarios of `trust` write `TIER` and `PATH` instead of angle-bracket
  placeholders, because the requirement prose check reads `<...>` as an unfilled placeholder.
- `show` writes in a loop until every byte is out, because a single write on an unbuffered
  standard output can take only part of the file and still end with exit code 0.

## Known gaps

- The installed-package acceptance tests skip on Windows. Their two `show` test functions were run
  on Windows through a local harness against a wheel built from an earlier state of this change,
  before the output loop was added.
- On a non-blocking standard output that is full, `show` retries without pause. This case is not
  tested.
- One acceptance sentence of the bundle containment requirement still says that "the concept is
  shown as before", although it now also covers `trust`. Only its trigger sentence was widened.
- The docstrings of the previous concept name change still say version 0.18.2, while the release
  holding it is planned as 0.19.0.
- `trust` on an unquoted impossible date such as `stale_after: 2020-02-30` ends in a traceback
  (exit code 1), although the command line reference says an unparseable value gives no stale line.
  The cause is in the frontmatter parser, predates this change (`list` fails too) and is left
  unchanged here.

<details>
<summary>Details</summary>

## Changes

- Concept name resolution and bundle containment are shared by `show`, `trust` and `show_bundle`;
  the resolution rules and error messages are unchanged.
- `show` writes the stored bytes to binary standard output.
- New `trust` command.
- `ConceptDetail.raw` added to the Python API.
- Requirements, command line reference, feature and evidence map, standalone agent skill and tests
  updated.
- Unaffected: the new project scaffold and the examples use neither `show` output nor the trust
  tier command; CI, `justfile` and packaging ship the command in the existing console script;
  `CHANGELOG.md` is generated at release; the README shows neither command.

## Human decisions

- `show` prints the stored file and nothing else: no rebuilt frontmatter, no validation.
- `show` no longer prints the trust tier or staleness.
- The Python API gains a `raw` field; its current fields do not change.
- A dedicated command prints the two lines `show` used to add, for one concept, with no listing of
  a whole bundle, and ships in the same pull request.
- The change is a feature, for release 0.19.0.
- On a file that is not valid UTF-8, `show` prints the bytes, `show_bundle` keeps failing, and
  `trust` writes one error line and exits 2.
- The wrong trust tier of some actor forms is fixed separately, before this change.

## Impacts

Command line users get the stored file from `show` and use `trust` for the tier and staleness. No
visual change.

## Test plan

- [ ] New or changed tests (they fail on the previous code)
- [ ] Local gates
- [ ] Evidence
- [ ] Review
- [ ] Verified
- [ ] CI green

## Internal references

- CR-103 show-as-stored.
- Work files: `work/coder/r1.md`, `evidence/scenario-run.txt`, `evidence/acceptance-windows.txt`.

</details>

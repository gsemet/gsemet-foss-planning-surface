## New Features
- New `okf-schema trust --path BUNDLE CONCEPT_PATH` command: it prints the trust tier of a concept (`unverified`, `machine-confirmed` or `human-reviewed`) and `stale: true` once `stale_after` is reached, and writes no file. See the [trust command reference](https://github.com/gsemet/okf-schema/blob/v0.19.0/docs/source/reference/cli.md#okf-schema-trust).
- The Python API result of `show_bundle` now has `raw`, the exact stored text of the concept file. See the [show reference](https://github.com/gsemet/okf-schema/blob/v0.19.0/docs/source/reference/cli.md#okf-schema-show).

## Breaking Changes
- `okf-schema show` now prints the concept file byte for byte, in any encoding, with nothing added: comments, quoting and line endings are kept, and the `trust:` and `stale:` lines are gone. Scripts that read those lines must call `okf-schema trust` with the same `--path` and concept. See the [show reference](https://github.com/gsemet/okf-schema/blob/v0.19.0/docs/source/reference/cli.md#okf-schema-show).
- `okf-schema show` no longer parses the file: invalid YAML or a file that is not valid UTF-8 is printed with exit code 0. Use `okf-schema validate` to check a file.
- Validation now reports broken links in `index.md` and `log.md` as W2, so `validate --strict` can start failing; `okfkb validate` and `okfreq validate` report them too. Run `okf-schema index` or fix the links by hand. See [W2](https://github.com/gsemet/okf-schema/blob/v0.19.0/docs/source/reference/validation-codes.md#w2-broken-cross-link).

## Bug Fixes
- `okf-schema show` finds a concept with or without `.md` or a leading `/`, from any terminal folder, and accepts an absolute path inside the bundle. See [how a concept name is read](https://github.com/gsemet/okf-schema/blob/v0.19.0/docs/source/reference/cli.md#okf-schema-show).
- `okf-schema show` and `show_bundle` refuse paths and symbolic links that leave the bundle, and a directory gives a plain error instead of a traceback.
- `okf-schema index` no longer copies into a parent index a link that only works from the subdirectory. Run it again to repair damaged summaries; summaries you wrote are kept. See the [index reference](https://github.com/gsemet/okf-schema/blob/v0.19.0/docs/source/reference/cli.md#okf-schema-index).
- A new subdirectory summary comes from the introduction of its `index.md`, never from a list entry or a heading, with its links adjusted for the parent index. An introduction already copied is not refreshed: delete the entry line and run `index` again.
- Valid links with an anchor or percent-encoding are no longer reported as broken or counted as broken by `stats`.
- The trust tier now counts every OKF 0.2 actor form: an agent such as `reference_agent/gemini-2.5-pro` reads as `machine-confirmed`. Any non-empty actor other than `human:<id>` counts as machine, including unrecognized ones. See [W10](https://github.com/gsemet/okf-schema/blob/v0.19.0/docs/source/reference/validation-codes.md#w10-unrecognized-actor-string-in-verifiedby).
- W10 now warns only about actors in no recognized form, lists the accepted forms and names the faulty entry.

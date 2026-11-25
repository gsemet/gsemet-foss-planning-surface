# Matrix probe r2, CR-102 (batch-01)

Head: 4b38782b9f0ac3b06d4f0fc104d7a997d0cf2a6c

Result: VERIFIED for the Windows cells run on this machine. Linux and macOS cells: not run here.
The `windows-latest` CI runner: not run here either (to be read from CI later).

Scope: the specification's two host matrices (link rewriting, section 1.2; percent-decoded
existence check, section 5, with `stats`). No previous matrix note, nothing carried. The head is
committed, not pushed. `git status --porcelain` printed nothing after the probe.

Paths: `<W>` is the CR's worktree, `<S>` is `<CR folder>/work/scratch/matrix-r2` (a `git init`
scratch project, removed at the end). Every command ran from `<W>`.

Host (`uv run --no-sync -- python -c "..."`): `Windows-11-10.0.26200-SP0`, Python `3.13.18`,
`okf_schema.__file__` = `<W>/src/okf_schema/__init__.py`.

## Cells

| Cell | Windows (this machine) | Linux | macOS |
| --- | --- | --- | --- |
| Link rewriting uses `/` (check 3) | VERIFIED (C1, C2) | not run here | not run here |
| `caf%C3%A9.md` found, no W2 (check 16) | VERIFIED, not skipped (C3, C4) | not run here | not run here |
| `stats` does not count it (check 22) | VERIFIED, not skipped (C5, C6) | not run here | not run here |

## Tests (C1, C3, C5), SHA 4b38782

Command:

    uv run --no-sync -- pytest -v -rs -o addopts="" -p no:cacheprovider \
      tests/test_api.py::test_index_bundle_rewrites_introduction_links \
      tests/test_api.py::test_index_bundle_rewrites_links_relative_to_a_nested_parent \
      tests/test_api.py::test_index_bundle_decodes_paths_to_detect_damage \
      tests/test_validator.py::test_validate_bundle_w2_decodes_percent_encoded_paths \
      tests/test_api.py::test_stats_bundle_counts_broken_links_like_w2 \
      tests/test_api.py::test_stats_bundle_counts_broken_links \
      tests/test_edge_cases.py \
      -k "rewrites or decodes or stats_bundle_counts_broken or external_links_only"

`-o addopts=""` drops the coverage options, which would fail a subset run. Output:

    platform win32 -- Python 3.13.18, pytest-9.1.1
    collected 54 items / 40 deselected / 14 selected
    test_index_bundle_rewrites_introduction_links[relative_and_parent_links] PASSED
    test_index_bundle_rewrites_introduction_links[anchor_only_link] PASSED
    test_index_bundle_rewrites_introduction_links[percent_encoded_link] PASSED
    test_index_bundle_rewrites_introduction_links[external_and_bundle_rooted_links] PASSED
    test_index_bundle_rewrites_introduction_links[image_link] PASSED
    test_index_bundle_rewrites_links_relative_to_a_nested_parent PASSED
    test_index_bundle_decodes_paths_to_detect_damage[file_only_in_the_subdirectory] PASSED
    test_index_bundle_decodes_paths_to_detect_damage[file_at_the_parent] PASSED
    test_validate_bundle_w2_decodes_percent_encoded_paths[concept] PASSED
    test_validate_bundle_w2_decodes_percent_encoded_paths[index] PASSED
    test_validate_bundle_w2_decodes_percent_encoded_paths[log] PASSED
    test_stats_bundle_counts_broken_links_like_w2 PASSED
    test_stats_bundle_counts_broken_links PASSED
    test_link_edge_cases_external_links_only PASSED
    ====================== 14 passed, 40 deselected in 0.87s ======================

No skip: 14 selected, 14 passed. The only skips found in `tests/` by a search for skip and xfail
markers are in `conftest.py` (`installed_product`, acceptance tests on Windows) and
`test_file_links.py` (symlinks); none of the selected tests uses them.

## Real CLI flow: bundle

    git init -q <S>
    uv run --no-sync -- okf-schema new --path <S>/kb/bundle --name <n> --type concept --title <n>
      for <n> in: README, api/health-check, api/guide, "api/my file", api/café, a/x, a/b/c
    uv run --no-sync -- okf-schema index --path <S>/kb/bundle
      -> 0 updated, 4 created, 0 unchanged, 0 skipped

Then, as an author would, one introduction line added before the list of two generated indexes:

- `api/index.md`: `[g](guide.md#s), [u](../README.md), [t](#top), [f](my%20file.md), [c](caf%C3%A9.md#x).`
- `a/b/index.md`: `See [c](c.md), [up](../x.md), [r](../../README.md) and [top](#top).`

## C2, link rewriting through the CLI, SHA 4b38782

    uv run --no-sync -- okf-schema index --path <S>/kb/bundle   (run A)
      -> 2 updated, 0 created, 2 unchanged, 0 skipped
    uv run --no-sync -- okf-schema index --path <S>/kb/bundle   (run B)
      -> 0 updated, 0 created, 4 unchanged, 0 skipped
    cat <S>/kb/bundle/index.md
      - [api](./api/) — [g](api/guide.md#s), [u](README.md), [t](api/index.md#top), [f](api/my%20file.md), [c](api/caf%C3%A9.md#x).
    cat <S>/kb/bundle/a/index.md
      - [b](./b/) — See [c](b/c.md), [up](x.md), [r](../README.md) and [top](b/index.md#top).
    grep -rn --include=index.md -F '\' <S>/kb/bundle
      -> no output, exit 1 (no backslash in any index.md)
    uv run --no-sync -- okf-schema validate --strict --path <S>/kb/bundle
      -> 14 warnings, all W1 or W3 (the `new` template has an empty description and no
         `generated.at`), no W2; "Validation failed: 0 error(s), 14 warning(s) (strict mode)", exit 1

## C4, percent-decoded check through the CLI, SHA 4b38782

Added: in `api/guide.md` `[a](my%20file.md) [b](caf%C3%A9.md#x) [c](missing%20x.md)`; a second
introduction line in `api/index.md` `Gone: [m](missing%20x.md).`; in the root `log.md`
`- Links [a](api/my%20file.md) [b](api/caf%C3%A9.md#x) [m](missing%20x.md)` under a date heading.
(A first try put `log.md` in `api/`: that is E6, a log belongs at the root, so it was moved.)

    uv run --no-sync -- okf-schema validate --path <S>/kb/bundle
      W2 lines, exactly three (the rest is W1 and W3), exit 0:
      [W2] Broken cross-link 'missing%20x.md' in '<S>/kb/bundle/api/guide.md'
      [W2] Broken cross-link 'missing%20x.md' in '<S>/kb/bundle/api/index.md'
      [W2] Broken cross-link 'missing%20x.md' in '<S>/kb/bundle/log.md'

No W2 names `my%20file.md` or `caf%C3%A9.md`, in the concept, the index files or the log.

Existence test of a damaged summary (check 16, section 2), root `api` line set to
`- [api](./api/) — [c](caf%C3%A9.md#x)`:

    café.md only in api/:  okf-schema index  -> 1 updated; line recomputed:
      - [api](./api/) — [g](api/guide.md#s), [u](README.md), [t](api/index.md#top), [f](api/my%20file.md), [c](api/caf%C3%A9.md#x). Gone:...
    café.md also at the root (okf-schema new --name café), line set again:
      okf-schema index  -> line kept: - [api](./api/) — [c](caf%C3%A9.md#x)
      okf-schema index  -> 0 updated, 0 created, 4 unchanged, 0 skipped
    okf-schema validate  -> W2 only for 'missing%20x.md' (api/index.md, log.md); none for the root index

## C6, `stats` through the CLI, SHA 4b38782

    uv run --no-sync -- okf-schema stats --path <S>/kb/bundle
      with [a](my%20file.md) [b](caf%C3%A9.md#x) [c](missing%20x.md) in api/guide.md:
        3 links (1 broken)
        Health: 90% — 1 broken link
      after removing [c](missing%20x.md):
        2 links
        Health: 100% — all clear

## Not run

- Linux (`ubuntu-latest`) and macOS (`macos-latest`) cells, and the `windows-latest` runner: not
  run here. `.github/workflows/ci.yml` runs `just preflight` (which runs `pytest -n 4`) in the
  `preflight` and `cross-platform` jobs; read those results once the head is pushed.
- No gate, no verdict command, no before/after, no PR description check (matrix probe).

# index: no broken links in subdirectory summaries, W2 in index.md

issue: https://github.com/gsemet/okf-schema/issues/57

Code described: `origin/main` 2f09cef (okf-schema 0.18.1). Decisions: `02-answers.md`
(index-links-Q1 to Q7).

## Goal

`okf-schema index` must stop writing broken links into the index that lists a subdirectory,
repair the summaries it already damaged, and keep the generic sentence fresh. `okf-schema validate`
must report broken links in every `index.md` as W2, like it does for concepts, and must stop
treating `page.md#part` or `#top` as broken.

Today, with `api/index.md` holding only a list and no summary for `api` yet,
`okf-schema index` writes in the root:

```markdown
- [api](./api/) — [Health Check](health-check.md)  [API Endpoint]
```

After the change it writes:

```markdown
- [api](./api/) — Auto-generated index for concepts in `api`.
```

or, if `api/index.md` has an introduction before its first list, that introduction with its
relative links rewritten to work from the root.

### Where the summary is written

`index_bundle` writes an `index.md` in every directory, and each one lists its direct
subdirectories as `- [<dir>](./<dir>/) — <summary>`. The bug and the fix are the same at every
level. In this specification, the **parent index** is the `index.md` holding the entry (the bundle
root in the issue, `a/index.md` for an entry `./b/` of `a/`), and the **subdirectory index** is
`<dir>/index.md`. "Valid from the root" in the answers means valid from the parent index's folder.

## Current code (origin/main)

- `src/okf_schema/api.py`
  - `index_bundle` (line 411): walks `sorted(dirs_with_md)`, so the root is processed before its
    subdirectories; for each `index.md` it parses the existing file with
    `_parse_existing_index` and calls `_generate_index_content`.
  - `_get_subdir_description` (line 966): schema `x-okf-summary`, else schema `description`
    (cut to 120 characters), else the **first non-heading line** of the subdirectory index, a
    list marker `- `/`* ` stripped, cut to 117 characters + `...`, else
    ``Auto-generated index for concepts in `<dir>`.`` (written in three places).
  - `_parse_existing_index` (line 1025): collects `descriptions` (link target -> summary) from
    every `- [text](target) — summary` line, and strips a trailing `[...]` (the type tag), which
    is why a copied `[API Endpoint]` disappears on the next run.
  - `_generate_index_content` (line 1068): for a subdirectory entry, a single-type schema summary
    wins; otherwise `preserved.get(subdir_rel, _get_subdir_description(...))` (lines 1167, 1169),
    so any text already in the parent index is kept forever.
- `src/okf_schema/_internal/utils.py`
  - `resolve_link` (line 38): external targets (`://`, `mailto:`) give `None`; `/x` resolves from
    the bundle root; anything else from the source's folder. Anchors are not removed.
  - `find_broken_links` (line 81): used only by W2; reports every internal target whose resolved
    path does not exist, so `a.md#part` and `#top` are reported.
- `src/okf_schema/validator.py`
  - `validate_concept` (W2 at line 851): `find_broken_links(body, path, bundle_root)`, message
    `Broken cross-link '{target}' in '{path}'`.
  - `validate_index` (line 863): only E3. `validate_bundle` calls it for every `index.md`.
  - `okfreq` runs this same `validate_bundle` on its tiers folder (`_okf_findings`,
    `src/okf_schema/okfreq/core.py:2810`); W2 is not in `_OKF_IGNORED_CODES`
    (`{"W3", "W4", "W7"}`), so `okfreq validate` reports the new index W2 too. `okfkb update`
    reaches `index_bundle` through `update_bundle`, so it gets the index fix too.

## What changes

### 1. Subdirectory summary source (index-links-Q1)

Order, for each `./<dir>/` entry of a parent index (only point c is new; a and b stay as today):

a. Schema summary first, unchanged: when all concepts of `<dir>` share one type with a schema,
   its `x-okf-summary`, else its `description` (120-character cut as today). It replaces any
   existing text, as today.
b. Otherwise, a summary already written in the parent index is preserved, **except** the two
   cases of sections 2 and 3, which go to point c.
c. Otherwise the **introduction** of the subdirectory index, rewritten (section 1.2), else the
   generic text ``Auto-generated index for concepts in `<dir>`.``.

Never a list entry, never a heading.

#### 1.1 The introduction

Rewrite the non-schema fallback of `_get_subdir_description` (and give the generic text one
constant or helper instead of three literals):

- Read the subdirectory index body (frontmatter removed with `extract_frontmatter`, as today;
  an `OSError`/`UnicodeDecodeError` still gives the generic text).
- Scan its lines from the top, and stop at the first line that starts a list: after stripping,
  it starts with `- `, `* `, `+ `, or digits followed by `. ` or `) `.
- Before that line, skip blank lines, heading lines (starting with `#`) and HTML comment lines
  (starting with `<!--`). The rest is the introduction text. Which part of it is taken, and how
  it fits on one line, is open question 1; the proposed rule: the first paragraph (consecutive
  non-blank, non-heading lines), joined with single spaces.
- No text before the first list (or no list and no text) gives the generic text.

#### 1.2 Links rewritten from the parent index

In the introduction, every link matched by `MARKDOWN_LINK_RE` (`[t](x)` and `![t](x)`) is
rewritten so it works from the parent index's folder:

- External targets (`://` or `mailto:`, the test `resolve_link` uses) and `/`-prefixed targets (bundle-rooted) are
  kept as written.
- A target with a path part: split at the first `#` and rewrite the path part **textually,
  without resolving it**: `posixpath.normpath("<dir>/" + path)`, where `<dir>` is the subdirectory
  index's folder relative to the parent index's folder, in `/` form (for a nested level, the same
  join with that relative folder), plus the `#...` part unchanged. Do not use `resolve_link` or
  `Path.resolve()` here: they follow symlinks, so a link through a symlink would be rewritten to
  the symlink's target, possibly outside the bundle (see the inbox item `bundle-outside-symlinks`).
  Only existence checks (section 2, W2) resolve paths. Example: in `api/index.md`,
  `[guide](guide.md#setup)` becomes `[guide](api/guide.md#setup)` in the root;
  `[up](../README.md)` becomes `[up](README.md)` (`normpath("api/../README.md")`).
- An anchor-only target `#x` (it points at the subdirectory index itself) becomes
  `<dir>/index.md#x`.
- The link text is not changed. A link already broken from the subdirectory is rewritten the same
  way and stays broken; W2 reports it (section 4).
- Output never contains `\`, whatever the host (see the host matrix).

#### 1.3 Length cut

Today the line is cut at 120 characters (117 + `...`), which can cut a link in two (the answers
record this as a fact for the specification). How the cut works now is open question 2; the
proposed rule: keep the 120-character limit, but never cut inside a `[...](...)` link: when the
cut would fall inside one, cut before that link (trailing whitespace removed) and append `...`.

### 2. Damaged summaries already written (index-links-Q2)

In `_generate_index_content`, a preserved summary of a `./<dir>/` entry is **not** preserved,
and goes to point c, when it has the bug's signature:

- after stripping, it starts with a Markdown link `[text](target)` (or `![...](...)`);
- `target` is relative: not external, not `/`-prefixed, not anchor-only;
- its path part (before `#`) does **not** exist resolved from the parent index's folder;
- and it **does** exist resolved from `<dir>/`.

This applies only to an entry that exists: `_get_immediate_subdirs_with_content` lists a
subdirectory only when it or a descendant holds a Markdown file (`has_markdown_files`). A
subdirectory holding only YAML schemas gets no entry at all, and its old line is dropped, as today.

Any other preserved summary is left untouched (including one that starts with a link broken
from both places, or valid from the parent; those keep their text and W2 reports the broken ones).
The issue's `- [_schema](./_schema/) — [_base.schema.yaml](_base.schema.yaml)` has the signature
(the file exists in `_schema/`, not at the root) and is recomputed when `_schema/` holds a Markdown
file (for example its own `index.md`); with only YAML schemas the line is dropped, as above.

### 3. Generic text recomputed (index-links-Q5)

A preserved summary equal to the exact generic text of that entry
(``Auto-generated index for concepts in `<dir>`.``) is not treated as authored: it goes to point c
on every run, so an introduction added later to the subdirectory index reaches the parent index.
Any other text, even close to it, is preserved.

Consequence to keep: the root is processed before its subdirectories, so on a first run of a fresh
bundle the root gets the generic text (subdirectory index not yet written); the next run picks up
an introduction if one was authored. A bundle whose subdirectory indexes hold only lists is stable
from the second run (a second run reports every index `unchanged`).

### 4. W2 in every index.md (index-links-Q3)

`validate_index` (`src/okf_schema/validator.py`) also runs
`find_broken_links(body, path, bundle_root)` on the body of every `index.md` (root and nested;
root frontmatter excluded, as `extract_frontmatter` already splits it) and adds, per broken target,
`report.add_warning("W2", f"Broken cross-link '{target}' in '{path}'", path)`: same code, message
and severity as for concepts. `validate --strict` then fails on it, as for any warning. Update its
docstring (checks E3 and W2). `okfreq validate` and `okfkb validate` report it too, through the
same `validate_bundle`.

### 5. Anchors ignored when a link is checked (index-links-Q4)

In `find_broken_links` (`src/okf_schema/_internal/utils.py`): split each target at the first `#`;
an empty path part (`#top`) is a link to the document itself and is never broken; otherwise only
the path part is resolved and checked. The reported target stays the target as written (with its
anchor). The anchor itself is not verified. This applies to concepts and index files alike
(W2 is the only user of `find_broken_links`). `resolve_link` and its other callers (graph,
backlinks, stats, superseded-link rewriting) are not changed. Update the docstring and add a
doctest for `a.md#part`.

### 6. Fixture carrying the bug

`tests/fixtures/bundle/valid/index.md` holds the bug's signature itself:
`- [subdir](./subdir/) — [Concept A](concept-a.md)` (`concept-a.md` is in `subdir/`). With
section 4 it would raise W2 and break `test_validate_bundle_valid_valid_bundle_is_conformant`
(`tests/test_validator.py:778`, asserts no warning). Replace that line with the output of the fixed
`index`: ``- [subdir](./subdir/) — Auto-generated index for concepts in `subdir`.``
(`subdir/index.md` is only a list). `test_index_bundle_returns_index_updates` runs `index_bundle`
in place on this fixture; with the fixed line it leaves it unchanged. A scan of every other
`index.md` under `tests/fixtures/`, `examples/`, `requirements/`, `src/okf_schema/data/`,
`skills/` found no other broken link and no anchor link; `docs/source/index.md` (Sphinx, not a
bundle) is out of scope.

## Surfaces (product maintenance guideline)

- **Runtime:** `src/okf_schema/api.py` (sections 1 to 3, `index_bundle` docstring: the summary
  order, repair of damaged summaries and generic text), `src/okf_schema/validator.py` (section 4),
  `src/okf_schema/_internal/utils.py` (section 5). CLI help of `index` in `src/okf_schema/cli.py`
  (around line 798): one sentence on where subdirectory summaries come from, if the help describes
  it.
- **Human docs:**
  - `docs/source/reference/cli.md`, `## okf-schema index`: the summary order of section 1, links
    rewritten from the parent index, damaged summaries and the generic text recomputed, other
    summaries preserved; a before/after of the issue's case; the limit that an introduction once
    copied into a parent index is kept as authored and not refreshed when the subdirectory
    introduction changes.
  - `docs/source/reference/validation-codes.md`: `### W2` covers concept bodies and every
    `index.md`, and ignores `#...` anchors (the anchor is not verified); in "Validation Scope",
    "Reserved files" lists W2 for `index.md`; a compatibility note: bundles with broken links in an
    index get new W2, so `--strict` can start failing until `okf-schema index` or a manual fix.
- **Agent skills:** `skills/okf-schema/SKILL.md`: the `index` row (line 136) says where
  subdirectory summaries come from and that damaged ones are repaired; the W2 row (line 359) adds
  `index.md` and the anchor rule. No new reference file.
- **Same batch, CR-101** (`4-batch/1-pending/101-show-extensionless-names`) edits
  `skills/okf-schema/SKILL.md` line 135 (next to this CR's line 136),
  `docs/source/reference/cli.md` and `requirements/tiers/log.md`. Whichever CR lands second
  rebases on the other and keeps both SKILL.md rows, both `cli.md` changes and both log entries.
- **Scaffold guidance (`src/okf_schema/data/`):** unaffected; it ships no index-generation or W2
  wording (the Driver checks with a grep for `W2` and `okf-schema index` and states the result).
- **Requirements** (`requirements/`, following both requirements guidelines):
  - `SwRS-OKFSCHEMA-CORE-004`: add scenario `S3` "Write subdirectory summaries valid from the
    parent index" (GIVEN a subdirectory index with or without an introduction, and a parent entry
    that is missing, generic or damaged; WHEN index runs; THEN the summary is the introduction with
    rewritten links or the generic text, and other authored summaries are kept). Add it to
    `scenarios:` and the body; IDs, UUID and other authored fields unchanged.
  - `SwRS-OKFSCHEMA-CORE-001`: add scenario `S4` "Report broken links in index files" (GIVEN an
    `index.md` with a broken relative link and a concept with `a.md#part` to an existing file;
    WHEN validate runs; THEN W2 names the index link and not the anchored one).
  - Mark the new tests `@tests_req SwRS-OKFSCHEMA-CORE-004#S3` and
    `@tests_req SwRS-OKFSCHEMA-CORE-001#S4`. `implemented_in_files` is generated
    (`requirements/config.yml` lists it in `generated_fields`): never edit it by hand. Put
    `# @implements_req SwRS-OKFSCHEMA-CORE-001` above `find_broken_links` in
    `src/okf_schema/_internal/utils.py`, so the regeneration adds that file to CORE-001. The
    rewritten summary helpers stay in `src/okf_schema/api.py`, which already carries the CORE-004
    marker on `index_bundle`; a helper placed in another file gets
    `# @implements_req SwRS-OKFSCHEMA-CORE-004` above it. Append an entry to `requirements/tiers/log.md`
    (IDs, reason: issue 57, verification). Run `okfreq lint requirements`.
  - Acceptance paths are unchanged; the existing `@accepts_req StRS-OKFSCHEMA-CORE-002#S2` test
    must still pass.
- **Examples:** unaffected: no example bundle has a broken or anchored link in an index, and none
  depends on the old copied line; `just refresh-all-examples` (run by preflight) must show no diff
  in `examples/`. If it does, review and keep it.
- **Verification:** the tests below; `docs/source/explanation/project-feature-coverage.md` has no
  row on index generation or W2: leave it, and say so in the change summary.

## Out of scope

- Concept descriptions edited after indexing are not refreshed in existing index entries
  (index-links-Q6, filed apart as `index-stale-descriptions`).
- An introduction copied into a parent index is then preserved as authored text, and is not
  refreshed when the subdirectory introduction changes later (also covered by the inbox item
  `index-stale-descriptions`).
- Verifying that an anchor exists in the target.
- Anchors in `resolve_link` for graph, backlinks, stats and superseded-link rewriting.
- Processing order of `index_bundle` (root before subdirectories) and schema summary rules.
- Concept entries of an index, and summaries without the bug's signature.
- `docs/source/index.md` (Sphinx).

## Evidence

All checks read the shipped code at the head under test; the fixture of section 6 is a
repository file read as it ships. Bundles built in `tmp_path` are prepared inputs for the broken
cases a shipped file cannot hold.

### Checks (pytest, `tests/test_api.py` unless named)

1. Issue reproduction: `api/health-check.md` (type `API Endpoint`), `api/index.md` with only its
   list, root written as in the issue; `index_bundle` writes
   ``- [api](./api/) — Auto-generated index for concepts in `api`.``; a second run reports every
   index `unchanged`.
2. Fresh bundle, no root summary yet, `api/index.md` list only (written before the first run):
   the root gets the generic text, not the list line.
3. Introduction taken: `api/index.md` = `# api`, blank, `See [guide](guide.md#setup) and
   [up](../README.md).`, blank, list; files `api/guide.md` and `README.md` exist: the root entry
   is `See [guide](api/guide.md#setup) and [up](README.md).`; `validate_bundle` gives no W2.
   Same with an anchor-only `[top](#top)` giving `api/index.md#top`.
4. Nested level: entry `./b/` in `a/index.md` from `a/b/index.md`; links are rewritten relative
   to `a/`.
5. Damaged summary repaired: root entry `[Health Check](health-check.md)` with the file in `api/`
   is recomputed; the `_schema` case of the issue too, with `_schema/` holding
   `_base.schema.yaml` and a Markdown file (`_schema/index.md`, list only), so that the entry
   exists: it gets the generic text. A second case with only the YAML file: no `_schema` entry.
6. Not damaged, kept: an authored summary without a leading link; one starting with a link valid
   from the root; one starting with a link broken from both places (kept, and W2 reports it).
7. Generic text recomputed: root holds the generic text, an introduction is then added to
   `api/index.md`: the next run writes the introduction. A text differing from the generic one by
   a character is kept.
8. Schema summary still first: existing schema tests keep passing
   (`test_index_bundle_schema_aware_root_descriptions` and neighbours).
9. Never a heading or list entry: subdirectory index with `## Section` before the list, and one
   with only a numbered list (`1. [C](c.md)`): generic text.
10. Length cut, per the answer to open question 2: a long introduction whose 117th character
    falls inside a link gives a summary with no cut link.
11. Existing tests updated, not deleted: `test_index_bundle_subdir_description_from_index_body`
    still passes (its `Intro line.` is an introduction); `test_index_bundle_subdir_description_oserror`
    and `test_index_bundle_get_subdir_description_truncates_long_desc` follow the new helper.
12. `tests/test_validator.py`: W2 for a broken link in a nested `index.md` and in the root
    `index.md` (with frontmatter); no W2 for a valid one; message format as for concepts.
13. `tests/test_validator.py`: concept with `[a](other.md#part)` (file exists) and `[t](#top)`:
    no W2; `[a](missing.md#part)`: W2 reporting `missing.md#part`. Same in an `index.md`.
14. `test_validate_bundle_valid_valid_bundle_is_conformant` passes on the shipped fixture
    `tests/fixtures/bundle/valid/` (section 6), read from the repository as it ships.
15. CLI (`tests/test_cli_core.py`): `okf-schema validate --strict --path <bundle>` exits non-zero
    on a bundle whose only problem is a broken link in an `index.md`, and its output contains
    `W2`.

### Host matrix (link rewriting, section 1.2)

- Linux (CI `preflight` job, ubuntu-latest): rewritten targets use `/`.
- macOS (CI `cross-platform`, macos-latest): rewritten targets use `/`.
- Windows (CI `cross-platform`, windows-latest, and the user's machine): rewritten targets use
  `/`, never `\` (check 3 asserts the exact string on every host).

### Scenario steps (manual, in a scratch folder, installed CLI)

1. `okf-schema new --path kb/bundle --name api/health-check --type "API Endpoint" --title "Health Check"`,
   then `okf-schema index --path kb/bundle` twice: root line is the generic text, second run all
   unchanged.
2. Write the issue's damaged root line, run `okf-schema index --path kb/bundle`: the line is back
   to the generic text; `okf-schema validate --strict --path kb/bundle` passes.
3. Put `- [api](./api/) — [Health Check](nope.md)` in the root and run `validate --strict`: W2 on
   `index.md`, non-zero exit. `index` keeps that line (no signature).
4. Add an introduction with a relative link to `api/index.md`, run `index`: the root shows it with
   the link rewritten; `validate --strict` passes.
5. `just preflight` passes; its generated diffs reviewed (no change expected under `examples/`).

## Open questions

1. **Which part of the introduction (index-links-Q1 says "the sentence written before the first
   list"):** proposed: the first paragraph before the first list, its lines joined with single
   spaces. Alternatives: only its first sentence; or every paragraph before the list, joined.
2. **The 120-character cut that can cut a link in two (fact recorded in answer 5):** proposed:
   keep 120 characters but never cut inside a link (cut before it, then `...`). Alternatives: no
   cut at all for an introduction; or drop the links' Markdown (keep their text) before cutting.

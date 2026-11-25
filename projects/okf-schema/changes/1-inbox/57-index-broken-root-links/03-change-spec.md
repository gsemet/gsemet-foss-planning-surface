# index: no broken links in subdirectory summaries, W2 in index.md

issue: https://github.com/gsemet/okf-schema/issues/57

Code described: `origin/main` 2f09cef (okf-schema 0.18.1). Decisions: `02-answers.md`
(index-links-Q1 to Q13, answers 1 to 14).

## Goal

`okf-schema index` must stop writing broken links into the index that lists a subdirectory,
repair the summaries it already damaged, keep the generic sentence fresh, and give summaries that
stay the same from one run to the next. `okf-schema validate` must report broken links in every
`index.md` as W2, like it does for concepts, and must stop treating `page.md#part`, `#top` or a
percent-encoded path to an existing file (`my%20file.md`) as broken.

Today, with `api/index.md` holding only a list and no summary for `api` yet,
`okf-schema index` writes in the root:

```markdown
- [api](./api/) — [Health Check](health-check.md)  [API Endpoint]
```

After the change it writes:

```markdown
- [api](./api/) — Auto-generated index for concepts in `api`.
```

or, if `api/index.md` has an introduction before its first list, that whole introduction on one
line, with its relative links rewritten to work from the root.

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
    every `- [text](target) — summary` line, and strips a trailing `[...]` (the type tag,
    `re.sub(r"\s+\[[^\]]+\]\s*$", "", desc)`, line 1055) on every entry, subdirectory entries
    included, which is why a copied `[API Endpoint]` disappears on the next run.
  - `_generate_index_content` (line 1068): for a subdirectory entry, a single-type schema summary
    wins; otherwise `preserved.get(subdir_rel, _get_subdir_description(...))` (lines 1167, 1169),
    so any text already in the parent index is kept forever.
- `src/okf_schema/_internal/utils.py`
  - `resolve_link` (line 38): external targets (`://`, `mailto:`) give `None`; `/x` resolves from
    the bundle root; anything else from the source's folder. Anchors are not removed.
  - `find_broken_links` (line 81): used only by W2; reports every internal target whose resolved
    path does not exist, so `a.md#part` and `#top` are reported, and so is `my%20file.md` when
    `my file.md` exists (the target is not percent-decoded).
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
c. Otherwise the **introduction** of the subdirectory index, rewritten (section 1.2) and cut
   (section 1.3), else the generic text ``Auto-generated index for concepts in `<dir>`.``
   (also when the cut leaves nothing before `...`, section 1.3).

Never a list entry, never a heading.

#### 1.1 The introduction (index-links-Q1, index-links-Q10)

Rewrite the non-schema fallback of `_get_subdir_description` (and give the generic text one
constant or helper instead of three literals):

- Read the subdirectory index body (frontmatter removed with `extract_frontmatter`, as today;
  an `OSError`/`UnicodeDecodeError` still gives the generic text).
- Scan its lines from the top, and stop at the first line that starts a list: after stripping,
  it starts with `- `, `* `, `+ `, or digits followed by `. ` or `) `.
- Before that line, skip blank lines, heading lines (starting with `#`) and HTML comment lines
  (starting with `<!--`). The rest is the introduction text, and **all** of it is taken
  (index-links-Q10): every paragraph before the first list, each line stripped, the lines joined
  with single spaces into one line. No sentence splitting: a paragraph is never cut at its first
  `.`. This is how answer 5's "the sentence written before the first list" reads.
- A subdirectory index with no list at all: its whole body, filtered the same way, is the
  introduction.
- No text before the first list (or no list and no text) gives the generic text.
- The introduction is then rewritten (section 1.2), then cut (section 1.3), in that order.

#### 1.2 Links rewritten from the parent index

In the introduction, every link matched by `MARKDOWN_LINK_RE` (`[t](x)` and `![t](x)`) is
rewritten so it works from the parent index's folder:

- External targets (`://` or `mailto:`, the test `resolve_link` uses) and `/`-prefixed targets
  (bundle-rooted) are kept as written.
- A target with a path part: split at the first `#` and rewrite the path part **textually,
  without resolving it**: `posixpath.normpath("<dir>/" + path)`, where `<dir>` is the subdirectory
  index's folder relative to the parent index's folder, in `/` form (for a nested level, the same
  join with that relative folder), plus the `#...` part unchanged. Do not use `resolve_link` or
  `Path.resolve()` here: they follow symlinks, so a link through a symlink would be rewritten to
  the symlink's target, possibly outside the bundle (see the inbox item `bundle-outside-symlinks`).
  Only existence checks (sections 2 and 5) resolve paths. Example: in `api/index.md`,
  `[guide](guide.md#setup)` becomes `[guide](api/guide.md#setup)` in the root;
  `[up](../README.md)` becomes `[up](README.md)` (`normpath("api/../README.md")`).
- An anchor-only target `#x` (it points at the subdirectory index itself) becomes
  `<dir>/index.md#x`.
- A percent-encoded path (`my%20file.md`, `caf%C3%A9.md`) is rewritten as written, still encoded
  (`api/my%20file.md`): the rewrite is textual and never decodes. Only the existence checks
  decode (section 5).
- The link text is not changed. A link already broken from the subdirectory is rewritten the same
  way and stays broken; W2 reports it (section 4).
- Output never contains `\`, whatever the host (see the host matrix).

#### 1.3 Length cut (index-links-Q12)

Today the line is cut at 120 characters (117 + `...`), which can cut a link in two (fact recorded
in answer 5). New rule, applied to the rewritten introduction:

- 120 characters or fewer: kept whole.
- Longer: the cut falls at character 117 (`text[:117]`, as today). When that position is inside a
  link, that is strictly after the start and before the end of a `MARKDOWN_LINK_RE` match (`[t](x)`
  or `![t](x)`) of the rewritten text, the cut moves to the start of that link. The kept text has
  its trailing whitespace removed, then `...` is appended. The result is never longer than 120
  characters and never holds part of a link.
- Nothing left after the cut (index-links-Q13): when the kept text is empty after its trailing
  whitespace is removed (an introduction starting with a link that covers character 117), the
  summary is the generic text ``Auto-generated index for concepts in `<dir>`.``, not `...` alone.
  Being the exact generic text, it is recomputed on every run like any generic text (section 3),
  so a shorter introduction written later reaches the parent index.
- The schema `description` cut (point a) is unchanged: schema text is not an introduction.

### 2. Damaged summaries already written (index-links-Q2)

In `_generate_index_content`, a preserved summary of a `./<dir>/` entry is **not** preserved,
and goes to point c, when it has the bug's signature:

- after stripping, it starts with a Markdown link `[text](target)` (or `![...](...)`);
- `target` is relative: not external, not `/`-prefixed, not anchor-only;
- its path part does **not** exist resolved from the parent index's folder;
- and it **does** exist resolved from `<dir>/`.

The two existence tests use the same path check as W2 (section 5: anchor removed, path
percent-decoded), so the repair and W2 agree on what "broken" and "valid" mean.

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

### 3b. Trailing `[...]` kept on subdirectory entries (index-links-Q9)

In `_parse_existing_index`, the trailing-`[...]` strip (line 1055) applies only to entries that
are not subdirectory entries. A subdirectory entry is one whose target ends with `/` (the form
`./<dir>/` that `_generate_index_content` writes); these never get a type tag, so their summary is
kept exactly as written. Concept entries keep today's behaviour: the tag is stripped on parse and
re-added from the concept's type on generation.

Effects:

- An introduction ending with a bracketed word (`Work in progress [draft]`) is copied once and
  stays identical on the next runs: the summary is stable between runs.
- Side effect, accepted with the answer: an old subdirectory line ending with `[Type]` without the
  bug's signature, for example `- [api](./api/) — Endpoints of the service  [API Endpoint]`, now
  keeps its `[API Endpoint]` (today it is dropped on the next run). A line with the signature
  (section 2) is recomputed anyway, whatever its end.

### 4. W2 in every index.md (index-links-Q3)

`validate_index` (`src/okf_schema/validator.py`) also runs
`find_broken_links(body, path, bundle_root)` on the body of every `index.md` (root and nested;
root frontmatter excluded, as `extract_frontmatter` already splits it) and adds, per broken target,
`report.add_warning("W2", f"Broken cross-link '{target}' in '{path}'", path)`: same code, message
and severity as for concepts. `validate --strict` then fails on it, as for any warning. Update its
docstring (checks E3 and W2). `okfreq validate` and `okfkb validate` report it too, through the
same `validate_bundle`.

### 5. Anchors ignored and paths decoded when a link is checked (index-links-Q4, index-links-Q11)

In `find_broken_links` (`src/okf_schema/_internal/utils.py`), for each internal target (external
ones are still skipped, with the same test as `resolve_link`):

1. Split the target at the first `#`. An empty path part (`#top`) is a link to the document itself
   and is never broken. The anchor itself is not verified.
2. Percent-decode the path part with `urllib.parse.unquote` (UTF-8, its default): `my%20file.md`
   becomes `my file.md`, `caf%C3%A9.md` becomes `café.md`.
3. Resolve the decoded path with `resolve_link` and check that it exists, as today (directories
   still accepted).

The reported target stays the target **as written** (with its encoding and its anchor): a link
really broken, such as `missing%20x.md#part`, is reported as `missing%20x.md#part`. This applies
to concepts and index files alike (W2 is the only user of `find_broken_links`). Put steps 1 and 2
in one small helper beside it (for example `_link_path_for_check(target) -> str | None`, `None`
for anchor-only) and use it also for the two existence tests of section 2. `resolve_link` and its
other callers (graph, backlinks, stats, superseded-link rewriting) are not changed. Update the
docstring of `find_broken_links` (anchors ignored, paths decoded, targets reported as written) and
add doctests for `a.md#part` and `#top`.

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

- **Runtime:** `src/okf_schema/api.py` (sections 1 to 3b, `index_bundle` docstring: the summary
  order, the whole introduction, the cut, repair of damaged summaries and generic text),
  `src/okf_schema/validator.py` (section 4), `src/okf_schema/_internal/utils.py` (section 5). CLI
  help of `index` in `src/okf_schema/cli.py` (around line 798): one sentence on where
  subdirectory summaries come from, if the help describes it.
- **Human docs:**
  - `docs/source/reference/cli.md`, `## okf-schema index`: the summary order of section 1 (the
    whole introduction before the first list, on one line), links rewritten from the parent index,
    the 120-character cut that never splits a link (the generic text when nothing is left before
    the link), damaged summaries and the generic text recomputed, other summaries preserved exactly as written (a trailing `[...]` on a
    subdirectory entry included); a before/after of the issue's case; the limit that an
    introduction once copied into a parent index is kept as authored and not refreshed when the
    subdirectory introduction changes.
  - `docs/source/reference/validation-codes.md`: `### W2` covers concept bodies and every
    `index.md`, ignores `#...` anchors (the anchor is not verified), percent-decodes the path
    before checking it (`%20`, accents), and reports a broken target as written; in "Validation
    Scope", "Reserved files" lists W2 for `index.md`; a compatibility note: bundles with broken
    links in an index get new W2, so `--strict` can start failing until `okf-schema index` or a
    manual fix.
- **Agent skills:** `skills/okf-schema/SKILL.md`: the `index` row (line 136) says where
  subdirectory summaries come from (the whole introduction, links rewritten, never a list entry)
  and that damaged ones are repaired; the W2 row (line 359) adds `index.md`, the anchor rule and
  the percent-decoding. No new reference file.
- **Same batch, CR-101** (`4-batch/1-pending/101-show-extensionless-names`) edits
  `skills/okf-schema/SKILL.md` line 135 (next to this CR's line 136),
  `docs/source/reference/cli.md` and `requirements/tiers/log.md`. Whichever CR lands second
  rebases on the other and keeps both SKILL.md rows, both `cli.md` changes and both log entries.
- **Scaffold guidance (`src/okf_schema/data/`):** unaffected; it ships no index-generation or W2
  wording (the Driver checks with a grep for `W2` and `okf-schema index` and states the result).
- **Requirements** (`requirements/`, following both requirements guidelines):
  - `SwRS-OKFSCHEMA-CORE-004`: add scenario `S3` "Write subdirectory summaries valid from the
    parent index" (GIVEN a subdirectory index with or without an introduction, and a parent entry
    that is missing, generic or damaged; WHEN index runs; THEN the summary is the whole
    introduction on one line with rewritten links, cut at 120 characters without splitting a link,
    or the generic text (also when the cut leaves nothing); other authored summaries are kept as
    written; a second run changes nothing). Add it to `scenarios:` and the body; IDs, UUID and other authored fields unchanged.
  - `SwRS-OKFSCHEMA-CORE-001`: add scenario `S4` "Report broken links in index files" (GIVEN an
    `index.md` with a broken relative link, and a concept with `a.md#part` and `my%20file.md` to
    existing files; WHEN validate runs; THEN W2 names the index link as written and neither the
    anchored nor the encoded one).
  - Mark the new tests `@tests_req SwRS-OKFSCHEMA-CORE-004#S3` and
    `@tests_req SwRS-OKFSCHEMA-CORE-001#S4`. `implemented_in_files` is generated
    (`requirements/config.yml` lists it in `generated_fields`): never edit it by hand. Put
    `# @implements_req SwRS-OKFSCHEMA-CORE-001` above `find_broken_links` in
    `src/okf_schema/_internal/utils.py`, so the regeneration adds that file to CORE-001. The
    rewritten summary helpers stay in `src/okf_schema/api.py`, which already carries the CORE-004
    marker on `index_bundle`; a helper placed in another file gets
    `# @implements_req SwRS-OKFSCHEMA-CORE-004` above it. Append an entry to
    `requirements/tiers/log.md` (IDs, reason: issue 57, decisions index-links-Q1 to Q13,
    verification). Run `okfreq lint requirements`.
  - Acceptance paths are unchanged; the existing `@accepts_req StRS-OKFSCHEMA-CORE-002#S2` test
    must still pass.
- **Examples:** unaffected: no example bundle has a broken, anchored or encoded link in an index,
  and none depends on the old copied line; `just refresh-all-examples` (run by preflight) must
  show no diff in `examples/`. If it does, review and keep it.
- **Verification:** the tests below; `docs/source/explanation/project-feature-coverage.md` has no
  row on index generation or W2: leave it, and say so in the change summary.

## Out of scope

- Concept descriptions edited after indexing are not refreshed in existing index entries
  (index-links-Q6, filed apart as `index-stale-descriptions`).
- An introduction copied into a parent index is then preserved as authored text, and is not
  refreshed when the subdirectory introduction changes later (also covered by the inbox item
  `index-stale-descriptions`).
- Verifying that an anchor exists in the target.
- Anchors and percent-decoding in `resolve_link` for graph, backlinks, stats and superseded-link
  rewriting.
- Processing order of `index_bundle` (root before subdirectories) and schema summary rules.
- Concept entries of an index (their type tag handling stays as today), and summaries without the
  bug's signature.
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
   Same with an anchor-only `[top](#top)` giving `api/index.md#top`, and with
   `[f](my%20file.md)` (file `api/my file.md`) giving `api/my%20file.md`, with no W2.
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
10. Length cut (index-links-Q12), exact strings asserted: (a) an introduction of exactly 120
    characters is kept whole; (b) one of 150 plain characters gives `text[:117]` with trailing
    whitespace removed, plus `...`; (c) in `api/index.md`, the introduction
    `"A" * 100 + " see [guide](guide.md) and more " + "B" * 40` (in the root the link becomes
    `[guide](api/guide.md)` and spans character 117) gives `"A" * 100 + " see..."`, which holds
    no `[` or `](` and is at most 120 characters; (d) a link that ends before character 117 is
    kept whole and the cut falls after it; (e) nothing left after the cut (index-links-Q13): in
    `api/index.md`, the introduction `"[" + "g" * 130 + "](guide.md) here."` (a link from
    character 0 covering character 117) gives in the root
    ``- [api](./api/) — Auto-generated index for concepts in `api`.``, never `...` alone; a second
    run reports every index `unchanged`; then the introduction is shortened to `Short intro.` and
    the next run writes `Short intro.` (the generic text was recomputed). The span test is done on
    the rewritten text.
11. Whole introduction (index-links-Q10): `api/index.md` = `# api`, blank, `First paragraph.`,
    `Second line of it.`, blank, `Another paragraph. With two sentences.`, blank, list: the root
    entry is `First paragraph. Second line of it. Another paragraph. With two sentences.`. A
    subdirectory index with no list (`# api`, blank, `Only text.`): `Only text.`.
12. Trailing `[...]` kept (index-links-Q9): `api/index.md` introduction `Work in progress [draft]`;
    the first run writes `- [api](./api/) — Work in progress [draft]`, the second run reports
    every index `unchanged` and the line still ends with `[draft]`. A root holding
    `- [api](./api/) — Endpoints of the service  [API Endpoint]` keeps that line unchanged. A
    concept entry still carries its type tag once, not twice, after two runs. Unit tests on
    `_parse_existing_index`: `- [api](./api/) — Text [X]` gives `{"./api/": "Text [X]"}`, and
    `- [c](c.md) — Text  [X]` still gives `{"c.md": "Text"}`.
13. Existing tests updated, not deleted: `test_index_bundle_subdir_description_from_index_body`
    still passes (its `Intro line.` is an introduction); `test_index_bundle_subdir_description_oserror`
    and `test_index_bundle_get_subdir_description_truncates_long_desc` follow the new helper;
    `test_index_bundle_parse_existing_index_no_h1` and
    `test_index_bundle_parse_existing_index_with_intro` still pass.
14. `tests/test_validator.py`: W2 for a broken link in a nested `index.md` and in the root
    `index.md` (with frontmatter); no W2 for a valid one; message format as for concepts.
15. `tests/test_validator.py`, anchors (index-links-Q4): concept with `[a](other.md#part)` (file
    exists) and `[t](#top)`: no W2; `[a](missing.md#part)`: W2 reporting `missing.md#part`. Same
    in an `index.md`.
16. `tests/test_validator.py`, decoding (index-links-Q11): files `my file.md` and `café.md`
    exist; a concept linking `[a](my%20file.md)` and `[b](caf%C3%A9.md#x)` gets no W2;
    `[c](missing%20x.md)` gets W2 whose message names `missing%20x.md` as written. Same in an
    `index.md`. Section 2 agrees (`tests/test_api.py`): a root entry starting with
    `[a](my%20file.md)` whose file exists only in `api/` is recomputed; one whose file exists at
    the root is kept.
17. `test_validate_bundle_valid_valid_bundle_is_conformant` passes on the shipped fixture
    `tests/fixtures/bundle/valid/` (section 6), read from the repository as it ships.
18. CLI (`tests/test_cli_core.py`): `okf-schema validate --strict --path <bundle>` exits non-zero
    on a bundle whose only problem is a broken link in an `index.md`, and its output contains
    `W2`.
19. Doctests of `find_broken_links` (`a.md#part`, `#top`) run with the suite.

### Host matrix (link rewriting, section 1.2)

- Linux (CI `preflight` job, ubuntu-latest): rewritten targets use `/`.
- macOS (CI `cross-platform`, macos-latest): rewritten targets use `/`.
- Windows (CI `cross-platform`, windows-latest, and the user's machine): rewritten targets use
  `/`, never `\` (check 3 asserts the exact string on every host).

### Host matrix (percent-decoded existence check, section 5)

- Linux (ubuntu-latest): `caf%C3%A9.md` decodes to `café.md`, found on disk: no W2 (check 16).
- macOS (macos-latest): same result (check 16).
- Windows (windows-latest and the user's machine): same result (check 16). Check 16 is not
  skipped on any host: if a runner cannot create `café.md`, it fails and the Driver reports it.

### Scenario steps (manual, in a scratch folder, installed CLI)

1. `okf-schema new --path kb/bundle --name api/health-check --type "API Endpoint" --title "Health Check"`,
   then `okf-schema index --path kb/bundle` twice: root line is the generic text, second run all
   unchanged.
2. Write the issue's damaged root line, run `okf-schema index --path kb/bundle`: the line is back
   to the generic text; `okf-schema validate --strict --path kb/bundle` passes.
3. Put `- [api](./api/) — [Health Check](nope.md)` in the root and run `validate --strict`: W2 on
   `index.md`, non-zero exit. `index` keeps that line (no signature).
4. Add a two-paragraph introduction with a relative link, ending with `[draft]`, to
   `api/index.md`, run `index`: the root shows both paragraphs on one line with the link rewritten
   and `[draft]` at the end; `validate --strict` passes; a second `index` run reports every index
   unchanged.
5. Add `[x](my%20file.md)` to a concept and create `my file.md` beside it: `validate --strict`
   passes.
6. `just preflight` passes; its generated diffs reviewed (no change expected under `examples/`).

## Open questions

None. Answers 10 to 13 (index-links-Q9 to Q12) settled the two questions of an earlier version
(extent of the introduction, 120-character cut) and the critic's findings on the trailing `[...]`
and on encoded links; answer 14 (index-links-Q13) settled what is written when nothing is left
after the cut (the generic text).

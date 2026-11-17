# Change specification: gate requirement markers

Short name: `marker-gate`. No tracker issue (verbal origin: the requirements gardening audit,
`changes/1-inbox/requirements-gardening/evidence/audit-synthesis.md`, systemic findings 1 and 8).

Read the project's `.agents/constitution.md` before starting; its rules and the project guidelines
rank above this specification.

## Goal

A requirement marker is a link from a requirement to the code or test that carries it. Today two
kinds of link go wrong without any check failing:

- an in-force SwRS can have no `@implements_req` at all (DIAG-128 went through: its code carries
  TOOLBAR-137 only);
- markers are piled in long lists on file headers, big constants or a marker-only file, so they
  point at no code point or test in particular (`editActions.test.ts:9-51`, 43 IDs;
  `test/integration/realInput/markers.ts`, 64 IDs attached to no scenario).

After this CR, `just check` (so the `static` CI jobs on Linux and Windows) refuses both. The
existing long lists are frozen in a baseline that can only shrink; the six req-garden CRs empty it.

## Decisions carried from `02-answers.md`

- marker-gate-Q1: an in-force, non-exempt SwRS with no `@implements_req` fails `just check`.
  DIAG-128 is fixed in this CR.
- marker-gate-Q2: a marker comment names at most 3 IDs. A companion file names, for each ID, the
  scenario that checks it (for example `@tests_req X — scenarioPalette`).
- marker-gate-Q3: the gate starts from a baseline of today's offenders that can only shrink (a
  ratchet); the six req-garden CRs empty it.
- marker-gate-Q4: the check lives in Studio, extending `scripts/check-marker-companions.mjs`.
  okfreq may take it over later through okf-schema's CR okfreq-gardening-skill-audit-checks (not
  this CR).
- marker-gate-Q5: rule 3 covers any tracked file with a `// Companion of:` line, not only
  `*.markers.ts`; `test/integration/realInput/markers.ts` goes on a rule-3 baseline until the
  req-garden CRs name each scenario.
- marker-gate-Q6: companion `@implements_req` lines name their code point, and a companion whose
  marker lines are all named escapes the 3-ID cap.
- marker-gate-Q7: the named scenario or code point must exist in the host file or its folder.
- Order (critic fix): `req-use-case-diagrams` lands after this CR (its `depends.json`:
  `{"after": ["req-marker-gate"]}`) and writes its companion line in the rule-3 form.
- Way: short specification, not reviewed by the owner; a spec critic runs (it changes what the
  static checks refuse).
- From the request: remove the stale `@tests_req SwRS-MDOKFSTUDIO-LAYOUT-021`.

## Marker block (the definition every sibling CR applies)

This definition goes, word for word, into `.agents/glossary/common.md` and the "Marker placement"
subsection of `requirements/guidelines/project.guidelines.md` (section 4), so the six req-garden
Drivers and `req-use-case-diagrams` point at it instead of restating it:

> **Marker block**: the requirement markers that sit together with no line of code between them.
> Several one-ID marker comments above one declaration or one test form one block, even when blank
> lines or prose comment lines (a JSDoc, an explanation) separate them; only a code line ends a
> block. A block names at most 3 distinct requirement IDs. To mark more, put each marker at the
> code or test it names: on another declaration, or inside the test body that checks it.

Technically: a line is a marker line when okfreq reads it as one (pattern below); a comment line is
a line whose trimmed text starts with `//`, `#`, `/*`, `*` or `<!--`, or ends with `*/` or `-->`;
a blank line is empty after trimming; every other line is a code line. A block is a maximal run of
marker, comment and blank lines that holds at least one marker line. Lines are split on `\n`, a
trailing `\r` ignored.

## Facts measured at main dedbdb2a (for the Driver to re-measure)

- SwRS: 465 `proposed`, 10 `draft`, 457 `superseded`, 59 `deprecated`. Among the in-force ones
  (`draft`, `proposed`, `approved`) with `annotation_exemption` not `true`, exactly one has no
  `@implements_req` in a source directory: DIAG-128 (`implemented_in_files: []`). So rule 1 needs
  no baseline once DIAG-128 is fixed.
- Marker blocks naming more than 3 IDs: 62 blocks in 61 files. Largest:
  `test/integration/realInput/markers.ts:4-67` (64), `test/page/modules/editActions.test.ts:9-51`
  (43), `src/page/modules/editPalette.ts:23-39` (17), `test/integration/previewEditing.test.ts:242-258`
  (17), `test/core/frontmatter/okfFrontmatter.test.ts:29-43` (15),
  `src/core/preview/styles/contentBlockStyles.ts:6-19` (14). One of them is a `*.markers.ts`
  companion: `src/core/render/requirementsViewer.markers.ts` (7), which escapes the cap once named
  (section 3).
- Companions today: the four `*.markers.ts` (`src/core/render/mystTightness.markers.ts`,
  `src/core/render/requirementsViewer.markers.ts`, `src/core/render/siteTheme.markers.ts`,
  `src/page/modules/plantumlBundle.markers.ts`; `@implements_req` lines only) and
  `test/integration/realInput/markers.ts` (`// Companion of: test/integration/realInput/run.ts`,
  64 `@tests_req` lines, comment lines and `export {};` only), which `check-markers` does not see
  today because of its name.
- okfreq 0.17 (`okf_schema/okfreq/core.py`, marker scan) matches
  `^\s*(?:(?:#|//|/\*|\*|<!--)\s*)?(@implements_req|@tests_req)\s+<id>` with no end anchor: text
  after the ID on the same line is ignored, one ID per line. Source dirs of every scope (from
  `requirements/config.yml`): `src`, `sphinx`, `skills`; test dirs: `test`, `sphinx/tests`.

## What changes

### 1. `scripts/check-marker-companions.mjs` (run by `just check-markers`, part of `just check`)

Restructure it so its pure functions are exported and the command runs only when the file is
executed directly (the `test/build/mystSourcePatches.test.ts` pattern: the test imports the `.mjs`
with `import(pathToFileURL(...))`), and accept a `--root <dir>` option (default: the repository
root) so the test can run it on a scratch git repository. Files are still those git tracks or
would track (`git ls-files --cached --others --exclude-standard`). The `check:markers` npm script
and `just check-markers` keep their names.

**Companion.** A companion is a tracked file under `src/` or `test/` that is named `*.markers.ts`
or holds a `// Companion of: <path>` line (marker-gate-Q5). The existing companion rules (a host
line naming an existing file, only comment lines and `export {};`, only existing requirement IDs,
at least one marker) apply to every companion; `realInput/markers.ts` already passes them.

**Rule 1, a source marker on every SwRS.** For each `requirements/tiers/swrs/**/SwRS-*.md`: parse
its YAML frontmatter (the `yaml` package already in `package.json`). When `req_lifecycle` is
`draft`, `proposed` or `approved` and `annotation_exemption` is not `true`, the SwRS ID must appear
in at least one `@implements_req` marker line of a file under the union of the scopes'
`source_dirs` read from `requirements/config.yml` (do not hard-code `src`, `sphinx`, `skills`).
Scan the files, never the generated `implemented_in_files` field: `just check` runs before
`just requirements-lint`, so the field can be stale. Message, one per SwRS:
`<requirement file>: SwRS-… is in force and not exempt but no @implements_req marks it in src/, sphinx/ or skills/ (put the marker at the code that produces the behaviour)`
(the directory list printed from the config). No baseline for this rule.

**Rule 2, at most 3 IDs per marker block.** In every tracked file under the scopes' source and
test dirs, each marker block (definition above) names at most 3 distinct IDs. A companion whose
marker lines all pass rule 3 is not held to rule 2 (marker-gate-Q6); a companion with an unnamed
line is. Message: `<file>:<first>-<last>: a marker block names <n> requirement IDs (at most 3): put each marker at the code or test it names`.

**Rule 3, companion lines name their target.** In a companion, each marker line is
`// @tests_req <ID> — <scenario>` or `// @implements_req <ID> — <code point>`: an em dash between
spaces, then a non-empty name. For `@tests_req`, the name is the scenario (test title or scenario
identifier) that checks the ID; for `@implements_req`, the function, constant, module or build
entry that implements it. The name must occur as text in the host file or in a file directly in
the host's folder (not its subfolders) (marker-gate-Q7). Messages:
`<file>:<line>: a companion marker names its scenario or code point after " — "` and
`<file>:<line>: "<name>" is found neither in <host> nor in its folder`. Update the existing
"malformed marker" regex (`^// @(implements_req|tests_req) (\S+)\s*$`) to accept the name.

**Ratchet.** New file `scripts/marker-baseline.json`, shaped like
`scripts/file-size-baseline.json`: a `description` (what it is, how to lower it), the `limit` (3)
and two maps:
- `blocks` (rule 2): each file with an over-limit block, mapped to the sum of distinct IDs over its
  over-limit blocks;
- `unnamedCompanionLines` (rule 3): each companion mapped to its number of marker lines without a
  valid name. Its only entry at the start is `test/integration/realInput/markers.ts` (64).
  `realInput/markers.ts` is therefore on both maps: as long as one of its lines is unnamed it is
  held to the cap; once all are named, its `blocks` entry turns stale and `--update` removes it.

Same semantics as `scripts/check-file-sizes.mjs`, for each map:
- a file not listed that breaks the rule fails (the rule's message);
- a listed file whose count grew fails: `<file>: <n> <what> (baseline <m>); a listed file may only shrink`;
- a listed file whose count shrank, reached 0 or is gone fails as stale, naming
  `node scripts/check-marker-companions.mjs --update`;
- `--update` lowers or removes stale entries, never raises one or adds a file.
The initial baseline is written once in this CR from the measured offenders (after the fixes of
sections 2 and 3), by a one-off run the Driver does not keep as a command option. Rule 1 has no
baseline; the four `*.markers.ts` companions are fixed in this CR (section 3), so the rule-3 map
starts with `realInput/markers.ts` only.

Output: keep the one-line success summary, extended, for example
`check-markers: 5 companion file(s), <n> in-force SwRS marked, <k> files on the marker baseline`.
Update the header comment of the script to list every rule and the marker block definition.

### 2. DIAG-128 and the stale marker

- Add `// @implements_req SwRS-MDOKFSTUDIO-DIAG-128` at the code that waits for the diagrams and
  keeps them as images: `whenDiagramsSettled` in `src/page/modules/exportSnapshot.ts` (beside the
  TOOLBAR-137 marker at line 84) and the call in the export run of the same file (around line 124);
  the Driver checks whether `embedImages` in `src/core/export/exportContent.ts` (keeps a `data:`
  diagram image as it is) also produces this behaviour and marks it if so. Each block stays at
  3 IDs or fewer. No behaviour change; the existing DIAG-128 tests stay as they are.
- Remove `// @tests_req SwRS-MDOKFSTUDIO-LAYOUT-021` at
  `test/session/diagReq.viewState.requirements.test.ts:107` (LAYOUT-021 is superseded; the same
  test already carries LIFE-169). If the CR "delete retired requirements" lands first and removes
  it, nothing to do.
- `just requirements-update`, and one dated entry in `requirements/tiers/log.md` (topic
  "Requirement markers gated": DIAG-128 gets its implementation marker, the stale LAYOUT-021
  marker removed, the new check-markers rules).

### 3. The four `*.markers.ts` companions

Rewrite each marker line to the rule-3 form, naming the code point that implements the ID. Do not
move or drop an ID.

- `mystTightness.markers.ts` (host `scripts/myst-patches.mjs`): name the patch function or
  constant of that file that implements CORE-070.
- `requirementsViewer.markers.ts` (host `test/site/requirementsViewer/write.ts`): name, per ID, the
  function of `write.ts` or of a file directly in `test/site/requirementsViewer/` that implements
  it. Once all seven lines are named, it escapes the cap.
- `siteTheme.markers.ts` (host `test/site/siteTheme.ts`): name the function or constant of the
  site look (CORE-086) in that file or `test/site/`.
- `plantumlBundle.markers.ts`: its host line names `src/page/modules/plantumlPreview.ts`, but the
  bundle build it marks (TRUST-074) is in the root `esbuild.mjs` (the build entry
  `entryPoints: ["src/page/modules/plantumlPreview.ts"]`, `outfile: "out/bundle/plantumlPreview.js"`,
  and the copy of the engine `LICENSE` to `out/bundle/plantuml/LICENSE`). Retarget its host line to
  `// Companion of: esbuild.mjs` (update its prose comment to match) and name the build entry,
  `out/bundle/plantumlPreview.js`, which occurs in `esbuild.mjs`. The file stays in
  `src/page/modules/` (okfreq reads implementation markers only in source dirs).

### 4. Rules and docs

- `requirements/guidelines/project.guidelines.md`, "During a change": a short "Marker placement"
  subsection holding the marker block definition above word for word, the three rules, the
  companion definition, the baseline and its `--update`, and that a new marker list over 3 IDs or
  a new unnamed companion line is never added to the baseline. (Not `requirements.guidelines.md`:
  `okfreq init --force` replaces it.)
- `.agents/glossary/common.md`: add "Marker block" with the definition above word for word, and
  "Companion marker file" (the companion definition of section 1).
- `CONTRIBUTING.md`, the `just check-markers` bullet: the new rules and the baseline, like the
  `just check-limits` bullet.
- `justfile`: the comment above `check-markers` names the new rules.

## Order with other CRs

- `req-use-case-diagrams` depends on this CR (`depends.json`: `{"after": ["req-marker-gate"]}`). It
  adds an `@implements_req` line to `src/core/render/requirementsViewer.markers.ts` in the rule-3
  form (`// @implements_req <ID> — <code point>`, the name found in
  `test/site/requirementsViewer/`), so it passes this gate when it lands after it.
- The six req-garden CRs empty both maps of `scripts/marker-baseline.json` and apply the marker
  block definition of `project.guidelines.md`; each runs `--update` for the entries it lowers.

## Out of scope

- Moving the existing markers out of the baseline's files, and naming the 64 scenarios of
  `realInput/markers.ts` (the req-garden CRs do it).
- A gate on SwRS with no `@tests_req`, on StRS validation tests, or on markers naming a retired
  requirement.
- Any change to okfreq or okf-schema (CR okfreq-gardening-skill-audit-checks there).
- Requirement text changes; changes to the CI workflow file (the `static` jobs already run
  `just check` through `just ci-static`).

## CI environment

The change alters what the existing `static` (ubuntu-latest) and `static-windows`
(windows-latest) jobs refuse, through `just ci-static` → `just check` → `just check-markers`.
There: a fresh checkout (no `out/`, no untracked files, so `--others` adds nothing), Node from
`.nvmrc` and `npm ci` from the lock file (`yaml` present), git available, LF line endings
(`.gitattributes`: `eol=lf`). Nothing is fetched from the network by the check. Before the push,
as `ci.guidelines.md` rule 2 asks, `just check` and `just ci-static` pass locally on Windows (Git
for Windows shell). Only the first CI run proves the Linux run (case-sensitive paths of the
baseline keys, which come from `git ls-files` and use `/` on both systems).

## Evidence

- Unit test `test/build/checkMarkers.test.ts` (runs in `just unit` through the
  `out/test/build/**` glob), each case on a scratch git repository with a minimal
  `requirements/config.yml`, a SwRS file and source files, with `--root`:
  1. an in-force non-exempt SwRS with no `@implements_req` fails with the rule 1 message; the same
     SwRS with `annotation_exemption: true`, or `superseded`, passes; a marker in `test/` only does
     not count;
  2. a block of 4 marker lines fails; 3 pass; two blocks of 3 separated by a code line pass; 4
     one-ID markers above one declaration split by a blank line or a prose comment line still
     fail;
  3. a companion line without ` — <name>`, or with a name absent from the host and its folder,
     fails; a file with a `// Companion of:` line but not named `*.markers.ts` is checked the same
     way; a companion with all lines named and 5 IDs passes; the same companion with one unnamed
     line fails rule 2 and rule 3;
  4. the ratchet, for each map: a listed file that grew fails, one that shrank fails as stale,
     `--update` lowers it and never adds a file.
  The refusal in each case is not made by the current script (constitution, section 3).
- `just check-markers` on the branch passes with the baseline, and fails when a 4-ID block is added
  to any file not on the baseline, or when an unnamed line is added to a named companion (try
  each, then revert).
- `just requirements-update` then `just requirements-lint`: DIAG-128 has a non-empty
  `implemented_in_files`; TRUST-074 keeps `src/page/modules/plantumlBundle.markers.ts` in its
  `implemented_in_files`; `okfreq trace --json` no longer lists LAYOUT-021 in `missing_ids` (or
  the marker is gone).
- `just preflight` (on Windows, the static stage).

## Open questions

None: marker-gate-Q5 to Q7 answered the previous ones.

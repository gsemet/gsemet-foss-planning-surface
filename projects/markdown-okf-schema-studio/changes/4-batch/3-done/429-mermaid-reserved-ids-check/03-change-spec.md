# CR-429 Change Specification: the requirements lint parses every use case diagram

Short name: `mermaid-check`. No tracker issue (verbal, filed by the batch-06 Foreman on 2026-11-17).

## Goal

A StRS use case diagram that Mermaid cannot parse must fail early, at `just requirements-lint`
(so also at `just check` and CI's static jobs), with a clear message: the StRS, the line in its
file, and the cause. Today such a diagram passes every check and only breaks the site build
(`test/site/requirementsViewer/useCaseDiagram.ts`, `renderUseCaseDiagrams`): in batch-06, six
PALETTE StRS sequence diagrams used `Box` as a participant id, a word Mermaid reserves, and failed
to parse (fixed in CR-345 by renaming it `Field`). The guideline also lists the words to avoid.

## Decisions carried from `02-answers.md`

1. **When:** `just requirements-lint` fails with a clear message naming the StRS, the line and
   the cause. (Owner: "Au lint des exigences".)
2. **Depth:** every use case diagram is parsed with the real Mermaid parser and every parse error
   is caught, not only reserved words. (Owner: "Analyse complète".)

## Facts established while writing this spec (read-only probes on `main`, 2026-11-20)

- The bundle holds 93 StRS with a `### Use case diagram` Mermaid fence: 66 `sequenceDiagram`,
  21 `stateDiagram-v2`, 6 `flowchart LR`. None uses `Box` any more.
- The project's Mermaid is `mermaid` 12.2.0 (`package.json` `"mermaid": "^12.2.0"`, a runtime
  dependency). Its ESM entry (`import mermaid from "mermaid"`) runs in plain Node and
  `await mermaid.parse(text)` parses without a browser: a sequence diagram with `participant Box`
  throws `Parse error on line 4: ... Expecting 'link', '+', '-', '()', 'ACTOR', got 'box'`.
- **Catch:** in plain Node every `stateDiagram-v2` fails with
  `DOMPurify.addHook is not a function` (DOMPurify, imported by Mermaid, has no `window` there, so it
  exposes no hooks). Setting no-op methods on the `dompurify` default export **before** importing
  Mermaid fixes it, because Mermaid's ESM build imports the same `dompurify` module instance:

  ```js
  import DOMPurify from "dompurify";
  DOMPurify.addHook ??= () => {};
  DOMPurify.removeHook ??= () => {};
  DOMPurify.removeAllHooks ??= () => {};
  DOMPurify.sanitize ??= (text) => text;
  const { default: mermaid } = await import("mermaid");
  ```

  With this, all 93 diagrams of the bundle parse, in about 1.7 s for the whole run, and a state
  diagram using `state` or `note` as a state id fails with Mermaid's parse error. The shim only
  matters for sanitising rendered labels; the check parses and never renders, so it does not
  weaken what is checked. `dompurify` is already installed (a dependency of `mermaid`, `^3.4.12`);
  no dependency is added to `package.json` or the lock file.
- CI's `static` (ubuntu-latest) and `static-windows` jobs run `just dev-ci` (`npm ci` and
  `uv sync`, **no Playwright Chromium**) then `just ci-static`, which runs `just check`, which ends
  with `requirements-lint`. So the check cannot use the Chromium path of `renderUseCaseDiagrams`;
  it uses Mermaid in Node as above.

## What changes

### 1. New script `scripts/check-use-case-diagrams.mjs`

An ESM Node script, the same shape as `scripts/check_main_paths.py` and
`scripts/check-marker-companions.mjs`. Usage: `node scripts/check-use-case-diagrams.mjs <bundle root>`
(the project passes `requirements`). Header comment documents the usage, the output and the
exit codes, and points to `requirements/guidelines/project.guidelines.md`, "Use case diagram of a
StRS". It carries `// @implements_req SwRS-MDOKFSTUDIO-CORE-<new>` (section 4) at the function that
checks the diagrams (`scripts/` is a source dir of the `rendering-core` scope).

Behaviour:

- Reads `<bundle root>/config.yml` with `yaml` (already a dependency, used the same way by
  `check-marker-companions.mjs`) to find the StRS folder (`tiers.StRS.folder`) and walks every
  `*.md` under `<bundle root>/tiers/<folder>/` recursively, in sorted order. The StRS id is the
  front matter's `id:`; a file with no `id` is skipped.
- Normalises line endings (`\r\n` and `\r` to `\n`) before anything, so it gives the same result on
  Windows checkouts.
- Extracts the diagram with **the same rules as `parseUseCaseDiagram`** in
  `test/site/requirementsViewer/useCaseDiagram.ts`, so the lint checks exactly what the site draws:
  only the text before `<!-- okf:links:start -->`; the section starts at a line matching
  `^###\s+Use case diagram\s*$`; it ends at the next line, outside a fence, that starts with a
  heading of level 1 to 3 or with `<!--`; the diagram is the first ```` ```mermaid ```` fence of the
  section, closed by a ```` ``` ```` line; its body is trimmed; no section, no Mermaid fence, an
  unclosed fence or an empty body is no diagram (not counted, not an error). Unlike
  `parseUseCaseDiagram`, the script also keeps the file line number of the first non-blank line of
  the fence body (to report lines).
- Applies the DOMPurify shim above, then imports Mermaid and calls `await mermaid.parse(body)` on
  each diagram, catching every throw. It checks every diagram and reports every failure (it does
  not stop at the first).
- On a failure, the file line is: when Mermaid's message matches `Parse error on line (\d+)`, the
  line of the first non-blank body line plus that number minus 1; otherwise the line of the
  ```` ```mermaid ```` opening line. It prints, on stdout:

  ```
  <path>:<line>: <StRS id>: the use case diagram does not parse (see "Use case diagram of a StRS" in requirements/guidelines/project.guidelines.md)
      <each line of Mermaid's message, indented by 4 spaces>
  ```

  `<path>` is relative to the current directory, with forward slashes on every host (for example
  `requirements/tiers/strs/palette/StRS-MDOKFSTUDIO-PALETTE-003.md`). After all files, exit 1.
- When every diagram parses: prints one line
  `use case diagrams: <n> StRS checked, all parse (Mermaid <version>)`, where `<n>` counts the StRS
  that have a diagram and `<version>` is read from Mermaid's `package.json` (`12.2.0` today); exit 0.
- When it cannot run (missing or unreadable bundle root or `config.yml`, Mermaid not installed):
  one line `check-use-case-diagrams: cannot run: <reason>` on stderr, with
  `(run \`just dev\`)` when Mermaid is missing; exit 2. A state diagram failing with a message that
  contains `DOMPurify` is reported like any failure (it would show the shim stopped working, for
  example after a Mermaid upgrade; the unit test below catches that first).

### 2. Wiring: `package.json` and `justfile`

- `package.json` `scripts`: add `"check:diagrams": "node scripts/check-use-case-diagrams.mjs requirements"`,
  next to the other `check:*` scripts.
- `justfile`, recipe `requirements-lint`: add the line `{{ npm }} run check:diagrams` after the
  `check_main_paths.py` line. Update the recipe's comment to
  `# Validate the okfreq requirements bundle: schemas, links, navigation, generated coverage, the Main paths citations and the use case diagrams.`
- `just check` already runs `requirements-lint` (last dependency); CI's static jobs run it through
  `just ci-static`. No CI workflow file changes.

### 3. Guideline `requirements/guidelines/project.guidelines.md`, "Use case diagram of a StRS"

- Add a bullet after the GitHub rendering bullet:
  "`just requirements-lint` runs `scripts/check-use-case-diagrams.mjs`, which parses every use case
  diagram with the project's Mermaid (the same extraction as the site) and fails on any parse error
  with `<path>:<line>: <StRS id>: ...` followed by Mermaid's message. Its last line is
  `use case diagrams: <n> StRS checked, all parse (Mermaid <version>)`. It parses and does not
  draw: a diagram that parses but cannot be drawn still fails only the site build."
- Add a bullet listing the ids to avoid, in this exact shape (one line per kind, words in
  backticks, comma separated) so the test of section 5 can read it:

  ```
  - Ids Mermaid reserves (a participant, node or state with one of these names does not parse;
    the check catches others too):
    - `sequenceDiagram` (any case): `box`, `end`, `alt`, `opt`, `loop`, `par`, `and`, `else`, `rect`, `critical`, `break`, `option`, `note`, `activate`, `deactivate`, `participant`, `actor`, `create`, `destroy`, `title`, `autonumber`, `over`
    - `flowchart` (lower case): `end`, `subgraph`, `graph`, `style`, `class`, `click`
    - `stateDiagram-v2`: `state`, `note`
  ```

  These words were each confirmed rejected by Mermaid 12.2.0 in the probes of this spec
  (sequence: `participant <Word>` with a capitalised word; flowchart: `A --> <word>`; state:
  `[*] --> <word>`). A word the test of section 5 finds accepted is removed from the list, not kept.
- The bullet "On the site the diagram is drawn once ..." stays as is. The bullet "The section is
  optional in this release of the rule; a later change makes it mandatory ... with a check" stays
  as is (making it mandatory is out of scope).

### 4. Requirements (okfreq)

- New SwRS created with `okfreq new` in scope `rendering-core` (the next free `CORE` number at the
  time of the change; call it CORE-NEW here), `derives_from: StRS-MDOKFSTUDIO-TRUST-014` (the StRS
  of SwRS-MDOKFSTUDIO-CORE-087, the site drawing of the same diagrams), `req_lifecycle: proposed`.
  - Title: "The requirements lint parses every use case diagram".
  - Normative: "When a maintainer runs the requirements lint, it SHALL parse the Mermaid fence of
    the Use case diagram section of every StRS with the project's Mermaid, using the same section
    and fence as the site, and SHALL fail naming the file, the line, the StRS id and Mermaid's
    message for each fence that does not parse."
  - Scenario (nominal): every diagram parses; the lint passes and prints
    `use case diagrams: <n> StRS checked, all parse (Mermaid <version>)`.
  - Scenario (boundary): a StRS with no section, a section with no Mermaid fence, or an empty fence:
    not counted and no error.
  - Scenario (refusal): one or more fences do not parse (for example a `sequenceDiagram` with
    `participant Box`, or a `stateDiagram-v2` with a state named `state`); each is reported as
    `<path>:<line>: <StRS id>: ...` with Mermaid's message, and the lint fails (exit 1).
  - Verification notes: unit tests in `test/build/checkUseCaseDiagrams.test.ts`.
- `@implements_req SwRS-MDOKFSTUDIO-CORE-NEW` in `scripts/check-use-case-diagrams.mjs`;
  `@tests_req SwRS-MDOKFSTUDIO-CORE-NEW` in each test of section 5.
- SwRS-MDOKFSTUDIO-CORE-087 is not changed (the site behaviour is unchanged). No `approved`
  requirement is touched (TRUST-014 and CORE-087 are `proposed` and not edited), so no owner
  agreement is needed.
- `just requirements-update`, its generated files committed, and a dated entry in
  `requirements/tiers/log.md` ("Use case diagrams parsed at the requirements lint": the new SwRS,
  the test file).

### 5. Tests: new `test/build/checkUseCaseDiagrams.test.ts`

Runs in `just unit` (the `test:unit` glob includes `out/test/build/**/*.test.js`). Same pattern
as `test/build/checkMarkers.test.ts`: spawn `node scripts/check-use-case-diagrams.mjs <root>` with
`process.execPath`, on scratch bundles under `os.tmpdir()` that hold a minimal `config.yml` and
StRS files (the project's folders are never written). Tests (each with `// @tests_req
SwRS-MDOKFSTUDIO-CORE-NEW`):

1. **Refusal, reserved id in a sequence diagram:** a StRS whose diagram has `participant Box` (the
   batch-06 case): exit 1; the output has `<path>:<line>: StRS-…: the use case diagram does not parse`
   with the line equal to the file line Mermaid names, and Mermaid's message (`got 'box'`).
2. **Refusal, state diagram:** a `stateDiagram-v2` with a state named `state`: exit 1, reported;
   and a valid `stateDiagram-v2` in the same bundle is **not** reported (this proves the DOMPurify
   shim works: without it every state diagram fails).
3. **Every failure reported:** two broken StRS in one bundle give two reports, and a broken fence
   with no line in Mermaid's message (for example a body with no diagram type) reports the
   ```` ```mermaid ```` line.
4. **Boundary:** no section, a section without a Mermaid fence, an empty fence, and a Mermaid fence
   after the next `###` heading: exit 0, `use case diagrams: 0 StRS checked, all parse`; a CRLF file
   with a valid diagram is counted.
5. **The shipped bundle (reads `requirements/` from the repository at the head under test, not a
   copy):** running the script on `requirements` exits 0, and its `<n>` equals the number of StRS
   files under `requirements/tiers/strs/` for which `parseUseCaseDiagram` (imported from
   `test/site/requirementsViewer/useCaseDiagram`) returns a diagram. This guards the two
   extractions from drifting apart.
6. **The shipped guideline's word list (reads `requirements/guidelines/project.guidelines.md` from
   the repository as it ships):** parses the three kind lines of the "Ids Mermaid reserves" bullet,
   builds one scratch StRS per word using it as an id in its kind (sequence: `participant <Word>`
   capitalised; flowchart: `A --> <word>`; state: `[*] --> <word>`), and asserts that the script
   reports every one of them. The list must be non-empty for each of the three kinds.

## Out of scope

- Making the Use case diagram section mandatory for every in-force StRS (the guideline keeps it
  for a later change).
- Drawing (rendering) at lint time; layout or drawing failures stay caught by the site build
  (`renderUseCaseDiagrams`, SwRS-MDOKFSTUDIO-CORE-087, unchanged).
- Checking against GitHub's newer Mermaid; only the project's Mermaid 12.2.0 is used.
- Mermaid fences elsewhere in the bundle (SwRS, other sections): only the Use case diagram of a
  StRS, as the site draws it.
- Adding Chromium to CI's static jobs, or any dependency (`dompurify` is already installed through
  `mermaid`).
- The writing skill: no rendered syntax changes, so `skills/writing-for-markdown-okf-schema-studio/`
  is not touched.
- `CHANGELOG.md`: a `test`/`build` change with no user-facing effect adds no line (release-process
  guideline, step 2); the PR template's "No user-facing change" box is ticked.

## CI and host matrix

The change adds no CI job; it adds a step to `requirements-lint`, which both static jobs run
through `just ci-static` -> `just check`.

- Environment of those jobs: `ubuntu-latest` (`static`) and `windows-latest` (`static-windows`,
  Git for Windows shell), after `just dev-ci` (`npm ci` from the lock file, so `mermaid`,
  `dompurify` and `yaml` are present; `uv sync`). Absent there and present locally: Playwright
  Chromium (not needed: the check runs in plain Node), warm `node_modules` (replaced by `npm ci`).
  No network or credential is used by the check.
- Host matrix (the check depends on the host for line endings and path separators):
  - Windows, local `just requirements-lint` and `just check`: proven before the push (output line
    `use case diagrams: 93 StRS checked, all parse (Mermaid 12.2.0)`, or the count at the time).
  - Windows CI (`static-windows`): proven by the PR's first CI run.
  - Linux CI (`static`): proven only by the PR's first CI run (no local Linux run is required).

## Evidence

- `just compile` then `just unit`: the six tests of section 5 pass.
- Fails on the previous code (constitution, section 3): on `main` without the change, a StRS with
  `participant Box` passes `just requirements-lint`; with it, the lint fails. Show it once by
  temporarily changing `Field` back to `Box` in one PALETTE StRS diagram in the worktree, running
  `just requirements-lint` (expected: exit 1 with the path, the line of the failing statement, the
  StRS id and Mermaid's `got 'box'`), then reverting the file; quote the output in the PR's Tests
  section. Do not commit the broken file.
- `just requirements-lint` on the change: last line of the new step
  `use case diagrams: <n> StRS checked, all parse (Mermaid 12.2.0)`.
- `just requirements-update` leaves no diff after its generated files are committed;
  `just check-markers` passes with the new SwRS marked in source and tests.
- `just preflight` passes (static stage on Windows; CI runs the others).
- The PR body's Tests section lists SwRS-MDOKFSTUDIO-CORE-NEW with
  `scripts/check-use-case-diagrams.mjs` and `test/build/checkUseCaseDiagrams.test.ts`.

## Files touched

- `scripts/check-use-case-diagrams.mjs` (new)
- `test/build/checkUseCaseDiagrams.test.ts` (new)
- `package.json` (`check:diagrams` script)
- `justfile` (`requirements-lint` line and comment)
- `requirements/guidelines/project.guidelines.md` ("Use case diagram of a StRS")
- `requirements/tiers/swrs/rendering-core/SwRS-MDOKFSTUDIO-CORE-NEW.md` (new, via `okfreq new`),
  the files `just requirements-update` regenerates, `requirements/tiers/log.md`

## Open questions

None. (Using a DOMPurify no-op shim in Node rather than Chromium follows from decision 2, "the real
Mermaid parser", and from CI's static jobs having no Chromium; it adds no dependency.)

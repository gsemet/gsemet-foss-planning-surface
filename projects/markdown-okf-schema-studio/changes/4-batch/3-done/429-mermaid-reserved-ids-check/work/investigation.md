# CR-429 investigation (mermaid-check)

Worktree `C:/Users/gaeta/Projets/markdown-okf-schema-studio.worktrees/batch-06-CR-429`, base
`origin/main` 82c11a47. Read only; probes ran `node --input-type=module -e` from the worktree
(Node v24.22.2, `node_modules` with `mermaid` 12.2.0, `dompurify`, `yaml` present).

## Two findings that change the spec's letter (read first)

1. **`participant Box` alone parses.** In Mermaid 12.2.0 a sequence diagram declaring
   `participant <Word>` parses for **every** word of the spec's sequence list (`box`, `end`, `alt`,
   ... `over`), alone or after another participant. It fails only when the id is **used in a
   message**: `sequenceDiagram / participant A / participant Box / A->>Box: x` fails with
   `got 'box'`; all 22 words fail in that form. The batch-06 diagrams failed the same way (message
   lines). Consequences for the Coder:
   - Test 1: the scratch diagram must use `Box` in a message line (for example
     `participant Writer`, `participant Box`, `Writer->>Box: hi`); the reported line is the
     **message line**, not the `participant` line (Mermaid says `Parse error on line 4` for that
     4-line body).
   - Test 6, sequence form: build `participant A` + `participant <Word>` + `A-><Word>: x`
     (capitalised word), not `participant <Word>` alone; otherwise every sequence word is
     "accepted", the spec's rule "a word found accepted is removed" would empty the list, and the
     non-empty assertion fails.
   - Guideline bullet wording: "a participant, node or state with one of these names does not
     parse" is not exact for sequences; say "a participant used in a message, a node or a state
     with one of these names does not parse". The word lists themselves are all confirmed rejected
     (sequence in the message form, flowchart `A --> <word>`, state `[*] --> <word>`: 0 accepted).
2. **Mermaid strips `%%` comment lines before numbering.** A body with a `%%` line before the
   error reports a line one too small (probe: comment at body line 2, error at body line 5,
   Mermaid says line 4). Blank lines inside the body are counted correctly. No StRS diagram of the
   bundle has a `%%` line today (`grep -rln "^\s*%%" requirements/tiers/strs` -> 0). Smallest fix:
   none needed by the spec; optional: map Mermaid's line to the n-th body line that is not a `%%`
   line. Mention it in the script header as a known limit if not handled.

## Files and entry points

- `test/site/requirementsViewer/useCaseDiagram.ts`: `parseUseCaseDiagram(text)` (exported) with
  `SECTION = /^###\s+Use case diagram\s*$/mu` and `FENCE = /^```mermaid[^\n]*\n([\s\S]*?)\n```[^\S\n]*$/mu`;
  the section loop toggles `fenced` on any line starting with ```` ``` ```` and breaks on
  `^(?:#{1,3}\s|<!--)` outside a fence. Note: the fence regex allows text after ```` ```mermaid ````
  (`[^\n]*`) and trailing blanks after the closing ```` ``` ````; mirror that. It does **not**
  normalise CRLF itself (`model.ts` `diagramOf` passes the body as read); the repo has
  `* text=auto eol=lf`, so checkouts are LF and test 5 compares like with like.
- Module top-level imports: `playwright-core` (`chromium`, not launched at import),
  `../../reportPaths`, `../siteTheme`, `./urls`. Already imported by unit tests in `test/site/`;
  importing from `test/build` is fine.
- **Import from test/build:** `tsconfig.json` has `rootDir: "."`, `outDir: "out"`, `module: NodeNext`,
  package.json has no `"type": "module"`, so tests compile to CommonJS under `out/test/...`. In
  `test/build/checkUseCaseDiagrams.test.ts` write
  `import { parseUseCaseDiagram } from "../site/requirementsViewer/useCaseDiagram";` (compiled
  `out/test/build/...` -> `out/test/site/requirementsViewer/useCaseDiagram.js`). Repo root from the
  compiled test: `path.resolve(__dirname, "../../..")` (as `checkMarkers.test.ts` and
  `unitGlobs.test.ts`).
- `scripts/check-marker-companions.mjs` shape to mirror: a leading `/** ... */` block (purpose,
  rules, options, exit), imports `node:*` then a blank line then `import { parse as parseYaml } from "yaml";`,
  exported pure helpers, a `main()` and the guard
  `if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) main();`.
  Note the spec's script needs top-level `await` for the shim order (`import DOMPurify` static,
  then `await import("mermaid")`); do the Mermaid import inside `main()` (async), so a test could
  import helpers without loading Mermaid, and so "Mermaid missing" can be caught (`ERR_MODULE_NOT_FOUND`)
  for the exit-2 message. A static `import DOMPurify from "dompurify"` at the top would itself
  throw if node_modules is missing: import it dynamically in the same try.
- `test/build/checkMarkers.test.ts` shape to mirror: `const script = path.resolve(__dirname, "../../..", "scripts", "<name>.mjs");`,
  `spawnSync(process.execPath, [script, root], { encoding: "utf8" })`, output `${stdout}${stderr}`,
  scratch root `fs.mkdtempSync(path.join(os.tmpdir(), "studio-<x>-"))` removed in `finally` with
  `fs.rmSync(root, { recursive: true, force: true })`; `import { test } from "node:test"`,
  `import * as assert from "node:assert/strict"`. No `git init` needed (the new script walks the
  folder, not git). Path in output is relative to the **current directory**: spawn with
  `cwd: root` and pass `.` or the bundle path, or match the path loosely; decide one and assert it.
  Test 5 must spawn with `cwd` = repo root and arg `requirements`.
- Minimal scratch `config.yml`: `tiers:\n  StRS: {folder: strs}\n` is enough for the script
  (it reads only `tiers.StRS.folder`). Real config: `tiers.StRS.folder: strs`; StRS live in
  subfolders `requirements/tiers/strs/<scope>/` (walk recursively; skip `index.md` via "no `id`").
- `justfile`: `npm := env("STUDIO_NPM", "fnm exec -- " + (if os_family() == "windows" { "npm.cmd" } else { "npm" }) + " --registry=https://registry.npmjs.org/")`
  (line 4). Recipe today (lines 168-173):

  ```
  # Validate the okfreq requirements bundle: schemas, links, navigation and generated coverage.
  requirements-lint:
      {{ okfreq }} validate requirements --check-links --project-root .
      {{ okfreq }} lint requirements --check --check-links --project-root .
      {{ okfreq }} update-coverage requirements --check
      uv run --no-sync --group requirements python scripts/check_main_paths.py requirements
  ```

  Add `    {{ npm }} run check:diagrams` as the last line; `just format` (`just --unstable --fmt`,
  first dependency of `check` and `preflight`) must leave it unchanged.
- `package.json` `scripts`: `check:*` block at lines ~405-410; add `"check:diagrams"` after
  `"check:settings"` (or with the others).
- Guideline `requirements/guidelines/project.guidelines.md`, section "Use case diagram of a StRS"
  (line 81); the GitHub-rendering bullet is lines 100-105; insert the two bullets between it and
  "On the site the diagram is drawn once ..." (line 106).

## Requirements (okfreq)

- Next free CORE number: **CORE-090** (`origin/main` and every batch-06 branch top out at CORE-089;
  `okfreq new` allocates, never write the id by hand; another batch-06 CR merging a CORE first would
  move it: re-run `okfreq new` at rebase, never renumber by hand).
- Command (from the worktree root):

  ```
  uv run --no-sync --group requirements okfreq new swrs "The requirements lint parses every use case diagram" --path requirements --project markdown-okf-schema-studio --scope rendering-core --derives-from StRS-MDOKFSTUDIO-TRUST-014 --lifecycle proposed --description "When a maintainer runs the requirements lint, it SHALL parse the Mermaid fence of the Use case diagram section of every StRS with the project's Mermaid, using the same section and fence as the site, and SHALL fail naming the file, the line, the StRS id and Mermaid's message for each fence that does not parse."
  ```

  Then fill the scenarios and Verification notes by hand in the shape of CORE-087
  (`### Scenario (nominal): ...` with GIVEN/WHEN/THEN bullets; `### Verification notes` with
  `- Method:` and `- Criteria:`). `--path requirements` vs `--path .`: check `okfreq new swrs --help`
  ("Project or requirements-bundle path"); `requirements` is the bundle.
- `requirements/tiers/log.md`: newest date first (`## 2026-11-20` exists at the top, add a
  `### Use case diagrams parsed at the requirements lint (CR-429)` entry under it with `- Added:`,
  `- Sources:`, `- Tests:` bullets as the CR-350 entry does).
- Then `just requirements-update` (fills `implemented_in_files: [scripts/check-use-case-diagrams.mjs]`,
  `tested_in_files`, links, index).

## Gates a new script or test may trip

- `check-markers` (`scripts/check-marker-companions.mjs`): rule 1 needs one `@implements_req` of
  the new SwRS in a source dir; `scripts` is a source dir (union of all scopes), so the marker in
  the `.mjs` counts. Rule 2: one `// @tests_req` per test (a block of 1), fine. Not a companion
  file. `scripts/marker-baseline.json` needs no change (nothing over the limit is added). Note the
  marker regex: the line must start (after spaces) with `//`, `#`, `/*`, `*` or `<!--` then the
  marker; a marker inside a JSDoc `*` line also counts. Do not write `@implements_req` in prose of
  the header comment for another id.
- `check-limits` (`scripts/check-file-sizes.mjs`): measures only `src/` (800 lines) and `test/`
  (1 500); `scripts/` is not measured. The new test file stays far below 1 500. No `@ts-ignore`.
- `check-exports` (`scripts/check-unused-exports.mjs`): checks only exports of `src/` modules;
  exports of the new `.mjs` and of the test are not checked. Nothing to allow-list.
- `check-boundaries`: `src/` only. Not affected.
- `unitGlobs.test.ts`: `out/test/build/**/*.test.js` is in the `test:unit` glob; fine.
- `requirements-lint` itself: `okfreq lint --check` / `update-coverage --check` fail until
  `just requirements-update` ran after markers exist.
- The unit runner adds `--import ./scripts/register-myst-patches.mjs` to the test process only;
  the spawned script runs in a plain `node`, as in CI.

## Smallest change

Exactly the spec's file list; no other file. The script is about 120 lines: config read, recursive
`*.md` walk (sorted), CRLF normalisation, extraction mirroring `parseUseCaseDiagram` plus the
first-non-blank-body-line number, the dynamic `dompurify` shim then `mermaid` import, a parse loop,
the report/exit codes. Mermaid version: read `node_modules/mermaid/package.json` via
`createRequire(import.meta.url).resolve("mermaid/package.json")` (check the `exports` map allows
it; otherwise resolve `mermaid` and walk up to its `package.json`) or `fs` on
`<repo>/node_modules/mermaid/package.json` relative to the script.

## Risks

- The two findings above (sequence word test form; `%%` line shift).
- Mermaid's message for a state diagram with `state` is `Expecting 'ID', 'EDGE_STATE', got '1'`
  (not the word): test 2 should assert the report line and "does not parse", not the word.
- A message without "Parse error on line" (for example `No diagram type detected matching given
  configuration for text: hello world`) falls back to the ```` ```mermaid ```` line: probe confirms
  that message shape for test 3.
- Mermaid keeps a global state between `parse` calls (`mermaid.parse` resets per call in 12.x;
  probe parsed 66 forms in one process with consistent results).
- Concurrent CORE number allocation in batch-06 (see above).
- Run time: one process parses the whole bundle in about 0.8-1.7 s; tests 1-6 spawn about 6-10
  processes; test 6 should put all ~30 words into **one** scratch bundle (one spawn) to keep `just
  unit` fast.

## Questions only the user can answer

None.

## Evidence plan

Kind of change: build/lint tooling with no user-facing effect; the proof is command output.
Raw logs go to `work/gates/*.log`; quoted excerpts in the PR's Tests section.

1. Unit tests: `just compile` then `just unit`. Expected: the six tests of
   `test/build/checkUseCaseDiagrams.test.ts` listed as passing in the spec reporter output
   (`ok` lines), total failures 0.
2. Fails before, passes after (constitution section 3), temporary revert, **not committed**:
   - On the change, edit `requirements/tiers/strs/palette-slash/StRS-MDOKFSTUDIO-PALETTE-007.md`:
     replace `Field` by `Box` on lines 72 (`participant Field as Text box`) and 79
     (`Page->>Field: ...`).
   - Run `just requirements-lint`. Expected (dry-run in memory, computed with the spec's rule):
     exit non-zero, and stdout containing

     ```
     requirements/tiers/strs/palette-slash/StRS-MDOKFSTUDIO-PALETTE-007.md:79: StRS-MDOKFSTUDIO-PALETTE-007: the use case diagram does not parse (see "Use case diagram of a StRS" in requirements/guidelines/project.guidelines.md)
         Parse error on line 13:
         ...ment        Page->>Box: insert or repla
         ----------------------^
         Expecting 'link', '+', '-', '()', 'ACTOR', got 'box'
     ```

     (line 79 is the message line, not the participant line 72; see finding 1).
   - "Before": with the same edit in place, run the base recipe's four lines (the three
     `okfreq` lines and `check_main_paths.py`, as in `git show origin/main:justfile`) one by one and
     record exit 0 for each: the base lint lets the broken diagram through. Then
     `node scripts/check-use-case-diagrams.mjs requirements` records exit 1 with the output above.
   - Restore with `git checkout -- requirements/tiers/strs/palette-slash/StRS-MDOKFSTUDIO-PALETTE-007.md`
     and show `git status --short` clean for that path.
3. `just requirements-lint` on the change: last line
   `use case diagrams: 93 StRS checked, all parse (Mermaid 12.2.0)` (93 on base; the count at the
   time if another CR adds diagrams), exit 0.
4. `just requirements-update` then `git status --short`: after committing its output, a second run
   leaves no diff. `just check-markers`: exit 0 and its summary line counts one more in-force SwRS
   than on base.
5. `just preflight`: passes (Windows, static stage); `just check` includes the new step.
6. CI: `static` (ubuntu) and `static-windows` jobs of the PR's first run green; their logs show the
   `use case diagrams: ...` line. Linux is shown only by CI.
7. PR Tests section: SwRS-MDOKFSTUDIO-CORE-090 (or the id `okfreq new` returns) with
   `scripts/check-use-case-diagrams.mjs` and `test/build/checkUseCaseDiagrams.test.ts`.

Cannot be shown: GitHub's newer Mermaid (out of scope); a diagram that parses but fails to draw
(still caught only by the site build, by design).

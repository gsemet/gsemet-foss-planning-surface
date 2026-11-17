# Plan: apply the requirement reduction inside PR #62

This plan is written for an orchestrator agent with no other context. Follow it step by step. Do
not skip a gate. When a gate fails twice on the same step, stop and report; do not improvise a
workaround.

## 0. Context

- **Repository:** `markdown-okf-schema-studio`. **Branch:** `changes-requests/059-requirements-batch3`
  (PR #62, not merged). **Worktree:** `/Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-059-b3`.
  Baseline head when this plan was written: `ccdd039`.
- **Goal:** reduce the requirements from **1863 SwRS and 228 StRS** (active) to **364 SwRS and 76
  StRS**, without losing a behaviour, a scenario, a Known issue or a test.
- **Inputs, in this folder** (`.agents/changes/requests/059-requirements-okfreq/reduction/` in the
  main checkout):
  - `mapping.csv`: one row per active id: `old_id,new_tile_key,action,reason`.
  - `tiles.csv`: one row per tile: `tile_key,level,scope,crosscutting,survivor_id,old_requirements,proposed_title`.
  - `tile-model.md`: what a tile is, the body template (§1), the 13 cross-cutting tiles (§2).
  - `mapping-summary.md`: counts per scope and how markers follow each action.
  - `tools/`: `build_mapping.py` and the tile specs that generated the CSVs.
- **Read before starting:** `.agents/constitution.md`, `AGENTS.md`, `CONTRIBUTING.md`,
  `requirements/guidelines/requirements.guidelines.md` (in the worktree).
- **Not in this plan:** code changes. The code simplifications are a separate follow-up PR after
  PR #62 merges (`code-simplification.md`, "Follow-up PR plan").

### Vocabulary

| Term | Meaning |
| --- | --- |
| tile | A row of `tiles.csv`: one new SwRS (one observable behaviour) or one new StRS (one use case). |
| survivor | The existing id that becomes the tile (`survivor_id`). `NEW` means it must be created. |
| member | An old id mapped to a tile in `mapping.csv` (the survivor is a member too, action `keep`). |
| main scope | rendering-core, code-blocks, gfm, myst, diagrams, frontmatter-schema, frontmatter-editing, layout-width. Already on `master`; ids are published. |
| PR scope | theme-zoom, toolbar-navigation, block-editing, palette-slash, table-editing, review-annotations, lifecycle-sync, trust-security. Only in PR #62; ids never published. |
| `okfreq` | `uv run --no-sync --group requirements okfreq`, run from the worktree root after `unset VIRTUAL_ENV`. |
| BASE | The commit recorded in step 0. Old bodies are always read from BASE: `git show BASE:<path>`. |

## 1. Decisions (resolved by the maintainer)

| # | Decision |
| --- | --- |
| D1 | About 370 SwRS (here 364): one SwRS per observable behaviour, but each palette action and each page↔host message type keeps its own SwRS. |
| D2 | PR-scope files that are absorbed are **deleted** (never published). Their id ranges are recorded as retired in `requirements/tiers/log.md` (step 8). The maintainer opens the okf-schema issue about id allocation himself; do not open it. |
| D3 | Main-scope survivors are **edited in place**. Main-scope absorbed ids are **superseded** (or archived for the 8 drop rows). No main file is deleted. |
| D4 | No code change in this PR. Markers and comment lines only. |

## 2. What okfreq can and cannot do (okf-schema 0.13.0)

| Need | okfreq | How |
| --- | --- | --- |
| Create a tile without a survivor | `okfreq new swrs …` | **Only in step 3, before any file is deleted.** `new` takes the lowest free number (`while id in existing: number += 1`), so a deletion first would hand out a retired number. After step 3, never run `okfreq new` in this PR. |
| Merge N requirements into 1 | none | Edit the survivor body. Delete the absorbed PR-scope files. In main scopes, `okfreq supersede <old> <survivor> --path . --yes` once per old id (N:1 works: `superseded_by` is one string per old file). |
| Archive a non-observable main SwRS | `okfreq archive <id> --path . --yes` | Sets `lifecycle: deprecated`. |
| Exempt retired files from markers | none: `supersede` and `archive` do not set it | `tools/set-exemption.py` (§4.2). |
| Cite a cross-cutting tile | authored `depends_on` (base schema, filename-stem link) | List the cross-cutting ids in the feature tile; `--check-links` verifies them. |
| Change title, description, `derives_from` | authored fields | Edit them. Title = first `##` heading; description = the normative sentence. |
| Generated fields (`derived_by`, `implemented_in_files`, `tested_in_files`) | `okfreq update-coverage` | Never edit by hand. |

Never hand-allocate an id. Never reuse one.

## 3. Gates

Every commit passes G1 to G6. G7 runs at the end.

| Gate | Command | Pass criterion |
| --- | --- | --- |
| G1 | `okfreq update-coverage requirements`, then `okfreq update-coverage requirements --check` | 0 files would change |
| G2 | `okfreq validate requirements --prose --check-links --project-root .` | 0 errors; prose warnings not more than at the previous commit |
| G3 | `okfreq lint requirements`, then `okfreq lint requirements --check --prose --check-links --project-root .` | Indexes up to date, 0 errors |
| G4 | `okfreq trace requirements --json > /tmp/trace.json` | `missing_ids` = 0 and `duplicates` = 0; every active non-exempt SwRS has at least one `@implements_req` and one `@tests_req` file |
| G5 | `python3 <CR>/reduction/tools/tile-audit.py --worktree . --mapping <CR>/reduction/mapping.csv --scopes <done scopes>` (§4.3) | 0 findings |
| G6 | `just check` | Green |
| G7 | `just requirements-report` and `just preflight` | Green. The real VS Code integration stage has had focus timeouts: allow up to 3 runs, and report a timeout separately from a real failure. |

`<CR>` is `/Users/az02065/Projects/DevTools/markdown-okf-schema-studio/.agents/changes/requests/059-requirements-okfreq`.

Commit messages follow Conventional Commits and end with the trailer
`Assisted-by: Claude:<model>`. Do not push until step 8 passes.

## 4. Scripts (write them in `<CR>/reduction/tools/`, not in the repository)

The orchestrator writes these three scripts in step 0 and tests them on a scratch copy of the
worktree (`git worktree add /tmp/059-dry BASE`), then removes the scratch worktree. Writers never
run them.

### 4.1 `apply-tiles.py`

```console
python3 apply-tiles.py --worktree <wt> --mapping mapping.csv --tiles tiles.csv \
  --scopes <scope>[,<scope>…] [--levels StRS|SwRS|both] [--only <tile_key>,…] [--dry-run]
```

Rows selected: `mapping.csv` rows whose **tile** lives in one of `--scopes` (column `scope` of
`tiles.csv`) and whose level is in `--levels`; with `--only`, only the rows of those tiles.
Tiles, not old ids, decide ownership, so an old id
of another scope moves with the tile that absorbs it.

For each selected row, in this order:

1. **Precondition.** The survivor file of the tile exists and is active. For `keep` rows, do
   nothing else.
2. **Markers.** In `src/`, `sphinx/`, `scripts/` and `test/` (all text files), replace every line
   `@implements_req <old>` and `@tests_req <old>` by the survivor id, keeping the comment opener
   and indentation. If the survivor id is already marked with the same tag in that file, delete
   the line instead (one marker per id per file). For `drop-implementation-detail` rows, delete
   the marker line.
3. **Files.**
   - PR scope (`fold-as-scenario`, `replace-by-crosscutting`, `merge-into`,
     `drop-implementation-detail`): `git rm` the old file.
   - Main scope, `supersede`: `okfreq supersede <old> <survivor> --path . --yes`.
   - Main scope, `drop-implementation-detail`: `okfreq archive <old> --path . --yes`.
4. **References, repo-wide and idempotent.** After the files step, for **every** row of the
   whole mapping whose old file is now deleted, superseded or deprecated (not only the selected
   rows), replace the old id by its survivor in:
   - `derives_from` and `depends_on` of every active requirement file;
   - id references inside the bodies of active requirement files (the 340 references found in
     BASE);
   - `test/visual/capture_*.py` comments that are not markers.
   Do not touch retired files, `log.md`, or the CR history files. Deduplicate a list that now
   contains the same id twice.
5. **Exemptions.** Run `set-exemption.py` (§4.2).
6. Print a summary: rows applied, files deleted, superseded, archived, marker lines renamed and
   deleted, references rewritten. Exit non-zero on any precondition failure, before writing.

`--dry-run` prints the same summary and writes nothing.

### 4.2 `set-exemption.py`

Sets `annotation_exemption: true` and an `exemption_reason` on every superseded or deprecated
requirement that is not yet exempt. It edits the frontmatter as text, so that okfreq's formatting
and key order stay as they are (precedent: commit `c19ae3e`).

```python
#!/usr/bin/env python3
"""Exempt superseded and archived requirements from traceability markers."""
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1]) / "requirements" / "tiers"
changed = 0
for path in sorted(root.glob("s*rs/*/*.md")):
    text = path.read_text(encoding="utf-8")
    head, sep, body = text.partition("\n---\n")
    life = re.search(r"^lifecycle: (\S+)$", head, re.M)
    if not life or life.group(1) not in ("superseded", "deprecated"):
        continue
    if re.search(r"^annotation_exemption: true$", head, re.M):
        continue
    by = re.search(r"^superseded_by: (\S+)$", head, re.M)
    if life.group(1) == "superseded" and by:
        reason = f"Superseded by {by.group(1)}; no marker expected."
    else:
        reason = "Archived. Not an observable behaviour; no marker expected."
    line = f'annotation_exemption: true\nexemption_reason: "{reason}"'
    if re.search(r"^annotation_exemption: false$", head, re.M):
        head = re.sub(r"^annotation_exemption: false$", line, head, count=1, flags=re.M)
    else:
        head = re.sub(r"^(tier: .*)$", lambda m: m.group(1) + "\n" + line, head, count=1, flags=re.M)
    head = re.sub(r'^exemption_reason: (?!").*\n(?:  .*\n)*', "", head, flags=re.M)
    path.write_text(head + sep + body, encoding="utf-8")
    changed += 1
print(f"exempted {changed} files")
```

Check after the first run: open three changed files and compare with
`requirements/tiers/swrs/lifecycle-sync/SwRS-MDOKFSTUDIO-LIFE-089.md`. If okfreq reflows the long
reason line in G3, accept its formatting.

### 4.3 `tile-audit.py` (gate G5) and `scenario-checklist.py` (reviewer pass)

`tile-audit.py --worktree <wt> --mapping mapping.csv --scopes <scopes>` reports, for every active
tile of the given scopes:

- title equals the first `##` heading; description equals the text under `### Normative behavior`;
- exactly one `SHALL` in the normative behaviour;
- 2 to 9 `### Scenario (nominal|refusal|boundary): …` headings, at least one nominal and one
  refusal or boundary (cross-cutting tiles: a table may replace extra scenarios);
- a `### Verification notes` section that names at least one test file per `tested_in_files`
  entry;
- every id in `depends_on` exists and is active;
- no active file (requirement, `src/`, `test/`) cites an id that is deleted, superseded or
  deprecated;
- every superseded or deprecated file has `annotation_exemption: true`;
- every `mapping.csv` row of the scopes is applied (survivor active, others retired as the action
  says);
- for each `msg-` tile: the message type named in its key appears in the scenario text.

`scenario-checklist.py --worktree <wt> --base BASE --mapping mapping.csv --scope <scope>` writes
`<CR>/reduction/review/<scope>.md`. For every tile of the scope, it lists every member, and for
each member, from `git show BASE:<path>`:

- each old `### Scenario…` title, with an empty "covered by" cell;
- each old `Known issue` line, with an empty "kept as" cell;
- the totals: old scenarios, old Known issues, new scenarios plus table rows, new Known issues.

## 5. Ownership rules for parallel work

- **Only the orchestrator commits, runs scripts and edits marker lines.**
- A **writer** is a subagent that rewrites the survivor files of a set of tiles. It owns exactly
  the survivor files listed for its stream in §7 (by `survivor_id` in `tiles.csv`). It edits the
  body and the authored fields `title`, `description`, `derives_from`, `depends_on`. It edits no
  other file: no source, no test, no other requirement, no index.
- A writer works in its own worktree branched from the current integration head, and returns
  its branch. The orchestrator integrates streams **one at a time**: rebase the stream branch on
  the integration head, run `apply-tiles.py` for the stream's scopes, run the gates, commit, then
  take the next stream. Shared files (`src/session/pageMessages.ts`, `src/core/protocol/*.ts`,
  `test/visual/scenarios.ts`, companions) are only ever changed by `apply-tiles.py` during an
  integration, so they never conflict.
- A **reviewer** is a separate subagent, never the writer of the same tiles. It reads only.

## 6. Steps

### Step 0: baseline and tools (no commit)

1. In the worktree: `git status` must be clean. Record `BASE=$(git rev-parse HEAD)` in
   `<CR>/reduction/STATE.md` (create it).
2. Record the counts in `STATE.md`: active SwRS and StRS (expect 1863 and 228), the highest
   number in `swrs/trust-security/` (expect TRUST-089) and `swrs/lifecycle-sync/` (expect
   LIFE-168), implementation and test marker links from `okfreq trace requirements --json`
   (expect 1972 and 2283), and the output of `okfreq status`.
3. Save `okfreq generate-report --output-json /tmp/059-before.json`.
4. Check the inputs: `mapping.csv` has 2091 data rows and each active id exactly once
   (`cut -d, -f1 mapping.csv | sort | uniq -d` is empty); `tiles.csv` has 364 SwRS and 76 StRS
   rows. If the active ids in the worktree differ from `mapping.csv`, stop: the mapping is stale.
5. Write and dry-run the scripts of §4 on a scratch worktree at BASE.

Gate: none (no commit). Effort: 2 h.

### Step 1: guideline (1 commit, first)

Edit `requirements/guidelines/requirements.guidelines.md`, section `## Levels`. Replace the whole
section body (from the StRS bullet to the end of the "Families of equivalent assertions" bullet)
by exactly this text:

```markdown
- **StRS** (`StRS-MDOKFSTUDIO-<TOKEN>-NNN`): a user use case observable in VS Code (what a writer,
  reviewer or maintainer can do and see), with `--user-need`. No implementation detail, no
  message names, no pixel values. A use case is broad enough to have about 3 to 8 SwRS; a scope
  has about 2 to 8 StRS.
- **SwRS** (`SwRS-MDOKFSTUDIO-<TOKEN>-NNN`): one observable behaviour of the extension (host,
  page or renderer), meaning one trigger family and one outcome rule, with `--derives-from` one or
  more StRS (any scope). The body holds all the scenarios of that behaviour, named by kind:
  `### Scenario (nominal): …`, `### Scenario (refusal): …` and `### Scenario (boundary): …`. It
  has at least one nominal and one refusal or boundary scenario and about eight at most; above
  that, it holds two behaviours and is split. Equivalent cases go in one scenario with a table
  (input, outcome), not in several scenarios or several SwRS.
- One SwRS per palette action, and one per page↔host message type of `src/core/protocol/`. A
  message SwRS states the accepted shape and what happens to a malformed or unexpected message.
  The feature SwRS that handles a message is its message SwRS when it states that shape. One
  message SwRS may cover two types that share one shape.
- Settings, commands, slash entries and toolbar buttons are named scenarios of the feature SwRS
  they belong to (accepted values, default, refusal of invalid or stale input), not SwRS of
  their own.
- A rule that every message, request, button or handler applies (a gate, the read-only refusal,
  answer correlation, one edit at a time, where a view choice is stored) is written once, as a
  cross-cutting SwRS with one table row per case. A SwRS that relies on it lists it in
  `depends_on` and cites it ("see SwRS-…") instead of repeating its scenarios.
- Known issues are notes in a `### Known issues` section (`- Known issue: …`), written as the
  code behaves. Only behaviour defects go there; documentation and test gaps go to the backlog.
- Page-wide properties checked on every visual scenario (no horizontal overflow, toolbar row
  layout per zoom, tooltip contrast, white/cream palette) are ONE SwRS each, in the scope of their
  subject (layout-width, toolbar-navigation, theme-zoom), not one per scenario.
- Families of equivalent assertions (code-blocks v05–v12, admonition galleries) map to one SwRS;
  a long scenario lock line is split into scenarios of that SwRS.
```

In the same file, section `## Creating`, add after the paragraph that starts "Never write
requirement frontmatter by hand":

```markdown
`okfreq new` takes the lowest free number. Never create a requirement in a change that also
deletes requirement files, and never create one whose number is listed as retired in
`requirements/tiers/log.md`.
```

Commit: `docs(requirements): one SwRS per observable behaviour`. Gates: G2, G3, G6.

### Step 2: StRS tiles, all scopes (1 commit)

StRS go first so that every SwRS can point its `derives_from` at a surviving StRS.

1. One writer rewrites the 76 StRS survivors (`tiles.csv`, `level` = StRS): title and
   description from `proposed_title` (adjust the wording if needed), the use case, the old facet
   StRS as constraints (`tile-model.md` §3). Input: the bodies of all members at BASE.
2. Orchestrator: `apply-tiles.py --scopes <all 16> --levels StRS`. This deletes 101 PR-scope
   StRS, supersedes 51 main StRS and rewrites `derives_from` in every SwRS repo-wide.
3. Deduplicate `@tests_req StRS-…` lines per file (done by the marker step of the script).
4. Gates G1 to G6 (G5 with the StRS checks only).

Commit: `docs(requirements): one StRS per use case`. Effort: 6 h.

### Step 3: create the three new tiles (1 commit, before any SwRS deletion)

Step 2 deleted StRS files only. No SwRS file has been deleted yet, so `okfreq new swrs` cannot
reuse a retired SwRS number.

1. Create, in this order:

   ```console
   okfreq new swrs "Each page request is answered once or ends after its timeout" --path . \
     --project markdown-okf-schema-studio --scope trust-security \
     --description "When the page sends a request to the host, the extension SHALL answer it once with the matching result or end it with a readable error after its timeout." \
     --derives-from <StRS survivor of TRUST.uc-* that holds "ignores answers not meant for it">
   okfreq new swrs "A view choice made on the page is stored for the workspace" --path . \
     --project markdown-okf-schema-studio --scope lifecycle-sync \
     --description "When the writer changes a view choice on the page, the extension SHALL validate it and store it for the workspace." \
     --derives-from <StRS survivor of the lifecycle use case on state across reloads>
   okfreq new swrs "A new page starts each view choice from the panel, stored or default value" --path . \
     --project markdown-okf-schema-studio --scope lifecycle-sync \
     --description "When a page opens, the extension SHALL start each view choice from the panel state, else the stored value, else the default." \
     --derives-from <same StRS>
   ```

   Pick the `--derives-from` ids from the StRS survivors written in step 2 (`tiles.csv`,
   `TRUST.uc-*` and `LIFE.uc-*` rows).
2. **Check:** the new ids are greater than the maxima recorded in step 0 (expect TRUST-090,
   LIFE-169, LIFE-170). If not, `git restore` and stop.
3. Write the ids into `<CR>/reduction/STATE.md` and replace `NEW` by them in a local copy of
   `tiles.csv` used by the scripts (`tiles.local.csv`). Use that copy from now on.
4. Write the three bodies (template of `tile-model.md` §1, one table row per case). Members:
   `tiles.csv` column `old_requirements`; old bodies from BASE.
5. Orchestrator: `apply-tiles.py --scopes trust-security,lifecycle-sync --levels SwRS` **limited to
   these three tiles** (add `--only TRUST.request-answer-correlation,LIFE.view-choice-store,LIFE.view-choice-start`
   to the script).
6. Gates G1 to G6.

Commit: `docs(requirements): add answer correlation and view choice tiles`. Effort: 5 h.

From here on, **never run `okfreq new`** in this PR. If a tile turns out to need a new id, stop
and report.

### Step 4: other cross-cutting tiles (2 commits, sequential)

The feature tiles of step 5 list these in `depends_on`, so they must exist in their final form
first.

- **4a. Trust gates:** `TRUST.page-message-envelope` (8 members), `TRUST.page-message-gates`
  (19), `TRUST.readonly-request-refusal` (15), `TRUST.host-message-acceptance` (3),
  `TRUST.readonly-no-edit-affordance` (11), `TRUST.readonly-keeps-viewing` (9). Commit
  `docs(requirements): write the trust gate rules once`.
- **4b. Editing and palette:** `BLOCK.edit-exclusivity` (17), `BLOCK.source-edit-outcome` (12),
  `PALETTE.popover-focus-contract` (15), `PALETTE.popover-leave-saves` (9). Commit
  `docs(requirements): write the editing rules once`.

For each: one writer, then `apply-tiles.py --only <keys>`, then the reviewer pass (step 5.5) for
those tiles, then gates G1 to G6. Effort: 12 h.

### Step 5: feature tiles per stream (parallel writers, sequential integration)

| Stream | Scopes | SwRS tiles to write | of which `msg-` | StRS (done in step 2) | Old SwRS absorbed | Agent-hours |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| S-A | block-editing, table-editing | 66 | 11 | 13 | 277 | 15 |
| S-B | palette-slash | 57 | 1 | 7 | 169 | 11 |
| S-C | review-annotations, toolbar-navigation | 70 | 13 | 12 | 261 | 14 |
| S-D | lifecycle-sync, theme-zoom, trust-security (feature tiles) | 50 | 7 | 16 | 198 | 10 |
| S-E (main) | rendering-core, code-blocks, gfm, myst | 48 | 3 | 13 | 183 | 9 |
| S-F (main) | diagrams, frontmatter-schema, frontmatter-editing, layout-width | 60 | 2 | 15 | 257 | 11 |
| | **Total** | **351** | **37** | **76** | **1345** | **70** |

351 feature tiles plus the 13 cross-cutting tiles of steps 3 and 4 make 364.

**Writer brief (same for every stream):**

- Inputs: the stream's rows of `tiles.local.csv` (non-cross-cutting SwRS tiles of its scopes), the
  member bodies at BASE, the tests listed in their `tested_in_files`, `tile-model.md` §1 and §2,
  and the guideline of step 1.
- For each tile, rewrite the survivor file: title (start from `proposed_title`), one `SHALL`
  sentence, named scenarios (each old scenario becomes a scenario, a table row, or is noted as a
  duplicate of a named one), `### Known issues` with every old Known issue note unchanged,
  `### Verification notes` naming the test of each scenario, `depends_on` for every cross-cutting
  rule it relies on, `derives_from` to the StRS survivors.
- `msg-` tiles: state the accepted shape of the message type named in the key (fields, bounds),
  and what happens to a malformed one. List `TRUST.page-message-envelope` (page to host) or
  `TRUST.host-message-acceptance` (host to page) in `depends_on`.
- Main-scope survivors (D3): the original normative sentence must remain true as one of the
  scenarios. If it cannot, stop and report the tile; do not change its meaning.
- Touch no file outside the survivor files of the stream.

**Message types without a `msg-` tile.** The writer of the named feature tile adds a scenario
that states the accepted shape (step 1 guideline: "the feature SwRS that handles a message is its
message SwRS when it states that shape"):

| Message type (direction) | Feature tile that states its shape | Stream |
| --- | --- | --- |
| previewReady (page to host) | `LIFE.live-render` | S-D |
| previewScroll, previewReveal (page to host) | `LIFE.preview-to-editor-reveal` | S-D |
| previewState (page to host) | `LIFE.reading-state-save` | S-D |
| previewRefresh (page to host) | `LIFE.refresh` | S-D |
| previewShowProblems (page to host) | `MYST.problems-view` | S-E |
| previewThemeMode (page to host) | `THEME.current-mode` | S-D |
| previewListTargets | `PALETTE.label-list` | S-B |
| previewListCitations | `PALETTE.citation-scan` | S-B |
| previewPickDocument | `PALETTE.doc-picker` | S-B |
| previewPickImage | `PALETTE.image-picker-host` | S-B |
| previewPasteImage | `PALETTE.paste-image-host` | S-B |
| previewPasteHtml | `PALETTE.paste-html-page` | S-B |
| previewEditSource (host to page) | `BLOCK.open-block-editor` | S-A |
| previewComments (host to page) | `REVIEW.threads-to-page` | S-C |
| previewPlantUmlIncludesChanged (host to page) | `DIAG.include-watch` | S-F |
| the 14 other `…Result` types (host to page) | the request's tile, plus a row in `TRUST.request-answer-correlation` | as the request |

Before writing, confirm each designation by reading the handler (`src/session/pageMessages.ts`
for page to host, `src/core/protocol/hostToPage.ts` and the page module for host to page). If the
handler belongs to another tile, use that tile and note it in `STATE.md`.

**Integration of each stream (orchestrator), in the order S-E, S-F, S-A, S-B, S-C, S-D:**

1. Rebase the stream branch on the integration head.
2. `apply-tiles.py --scopes <stream scopes> --levels SwRS`.
3. Reviewer pass (step 5.5) for each scope of the stream.
4. Gates G1 to G6.
5. Commit, one per scope: `docs(requirements): <scope> as behaviour tiles`.

The main-scope streams go first because they only supersede and archive: if anything goes wrong
there, no file has been deleted yet in the PR scopes.

### Step 5.5: reviewer pass (per scope, and for steps 3 and 4)

1. Orchestrator: `scenario-checklist.py --scope <scope>`. It writes
   `<CR>/reduction/review/<scope>.md`.
2. Reviewer: for every old scenario, fill "covered by" with the new scenario title or table row,
   or "duplicate of `<new scenario>`". For every old Known issue, fill "kept as" with the new note.
   Check every value (limits, timeouts, reason texts) word for word.
3. Pass criteria:
   - no empty "covered by" cell;
   - new Known issue notes = old Known issue notes for the scope, or each difference is
     explained in the review file (a note that was a documentation or test gap, moved to a
     named backlog item);
   - every test that carried a member's `@tests_req` at BASE still carries a marker of the tile
     (`okfreq trace` at BASE against now).
4. If the pass fails, send the review file back to the writer and repeat. After two failed
   rounds, note the scope as blocked in `STATE.md` and continue with the next stream.

### Step 6: markers and companions (1 commit)

The renames happened in each integration. This step fixes what the script cannot:

- Move file-head markers to the function or the first test (LAYOUT-007/008, THEME-025/037,
  TOOLBAR-034, BLOCK-251).
- Put each tile's `@tests_req` above the first test of that tile in each file.
- Fold companion markers back into the host where they fit: `src/page/modules/editPalette.markers.ts`
  (15 left, host reaches 781 lines), `test/page/modules/editActions.markers.ts` (43),
  `test/core/frontmatter/okfFrontmatter.markers.ts` (15), checking each host against
  `scripts/check-file-sizes.mjs`. Keep `test/integration/realInput.markers.ts`. Update the list
  of companions in the guideline.
- Gates G1 to G6. Commit: `chore(requirements): place markers next to their behaviour`.

### Step 7: backlog references (separate, main checkout)

11 backlog items in the main checkout `.agents/changes/backlog/` cite SwRS ids (list in
`mapping-summary.md`). Replace each id by its survivor from `mapping.csv`. This is a commit on
`master` in the main checkout, or a note to the maintainer if he prefers: ask in the final report,
do not push to `master`.

### Step 8: final audit (1 commit)

1. `okfreq status`, `okfreq trace requirements --json`,
   `okfreq generate-report --output-json /tmp/059-after.json`. Expected:
   - 364 SwRS and 76 StRS active;
   - implementation markers 100 %, SwRS test markers at least 99.7 %;
   - about 813 implementation and 1072 test marker links (from 1972 and 2283).
2. G5 over all 16 scopes.
3. Add an entry at the top of `requirements/tiers/log.md`:
   - counts before and after;
   - **retired id ranges**: compute them from `mapping.csv` (PR-scope rows whose action is not
     `keep`), compressed per token, for example `SwRS-MDOKFSTUDIO-BLOCK-002–010, 012, …`. State
     that these ids were never published and must never be allocated again;
   - the verification commands and their results.
4. In `<CR>`, add one line on top of `known-issues-batch3-4.txt`, `gap-report.md` and
   `reviews/*.md`: "Ids in this file predate the reduction; see `reduction/mapping.csv`."
5. Gates G1 to G7.

Commit: `docs(requirements): record the reduction and retired ids`. Then push the branch and
update the PR description (sections: what changed, counts, how to review by `tiles.csv`,
retired ids; internal references last).

## 7. Effort

| Step | Agent-hours |
| --- | ---: |
| 0 baseline and scripts | 2 |
| 1 guideline | 1 |
| 2 StRS | 6 |
| 3 new tiles | 5 |
| 4 cross-cutting | 12 |
| 5 streams (6 in parallel) | 70 |
| 5.5 reviews | 16 |
| 6 markers | 8 |
| 8 audit and preflight | 4 |
| **Total** | **about 124** |

Wall time: about 3 days with 6 writers in parallel during step 5.

## 8. Risks

| Risk | Effect | Mitigation |
| --- | --- | --- |
| A retired number is reallocated | An id comes back with another meaning | `okfreq new` only in step 3, before any SwRS deletion; retired ranges in `log.md`; the okf-schema issue (maintainer) |
| Behaviour lost in a merge | A scenario, value or Known issue disappears | Reviewer pass with the per-scenario checklist; Known issue counts equal or explained |
| A main survivor changes meaning (D3) | A published id stops meaning what it meant | Writers stop on such a tile; the original sentence stays a scenario |
| Script error on markers | Duplicate or orphan markers | Dry run in step 0; G4 and G5 on every commit |
| Rebase conflicts between streams | Lost edits | Writers touch only their survivor files; only the orchestrator touches shared files, one stream at a time |
| A message type has no clear owner tile | Gap in the one-SwRS-per-type rule | The designation table in step 5, confirmed against the handler |
| PR size | Review fatigue (1138 deleted files, 516 retired files) | One commit per scope; review by `tiles.csv`; `mapping.csv` lists every deleted id |

# 059 — requirements-okfreq (resume: inventories only)

Moved from backlog `P1/requirements-okfreq` (the tracker is `STATE.md` in this folder; the plan is in
`setup-plan.md` and `scope-briefs.md`). Started by the overnight chain the user asked for on
2026-10-23 ("then the next P1").

## Decisions for this resume

1. **Sonnet only** (the item's rule from 2026-10-22: token cost). Orchestrator, analysts and
   critics run on Sonnet. No Opus.
2. **Scope of this run: P10.1 inventories only.** Analysis that writes only inside this folder.
   No repo change and no commit (rule D33: commits wait for the PR). Out of scope:
   - P10.0 setup: it needs okfreq ≥ 0.13, and 0.12.0 is installed (`uv tool`). Upgrading is an
     install, which is the user's decision.
   - P10.2 onwards.
3. **Code base = the refactor branch** `origin/changes-requests/056-refactor-host-neutral-core`
   (PR #51, ready, not merged). It moved almost every `src/` file into `src/core`, `src/host-api`,
   `src/page`, `src/node-services`, `src/host-vscode`. Use a read-only detached worktree
   `../markdown-okf-schema-studio-wt-059` at that ref.
4. Paths in `STATE.md`, `scope-briefs.md` and `tools/*.mjs` still point to the old location
   `.agents/changes/archives/021-feature-session-007-020/p10-requirements/`. Read them as this
   folder. `tools/scope-map.mjs` computes the repo root from its own location: make it take the
   repo root as an argument (or fix the relative depth). Edits to the files of this folder are
   allowed.
5. Steps:
   1. Remap `tools/scope-map.json` to the refactored tree. Every `src/` file goes in exactly one
      scope; tests go in a scope or in "tooling". `scope-map.mjs` must report no problem.
   2. Regenerate the checklists with `extract-checklists.mjs`. Keep the checklist ids stable
      (`tools/checklist-ids.json`).
   3. Update the evidence paths of the 5 inventories already written (rendering-core,
      code-blocks, gfm, frontmatter-schema, frontmatter-editing) to the new files and symbols.
   4. Write the 11 missing inventories (myst, diagrams, layout-width, theme-zoom,
      toolbar-navigation, block-editing, palette-slash, table-editing, review-annotations,
      lifecycle-sync, trust-security) with the common brief of `scope-briefs.md`.
   5. Run one Sonnet critic per scope (16 in total), with verdict APPROVE or REVISE, and at most
      one revision per scope.
   The "Shared hosts" hint of the common brief is outdated: after the refactor, behaviours sit in
   the feature controllers and page feature modules. Search there.
6. Analysts run no builds, no tests and no VS Code. Update `STATE.md` (per-scope status table,
   next action, journal) after each step.
7. Done for this run: 16 inventories, each with a critic review at APPROVE (or REVISE with the
   remaining gaps listed), the counts in `STATE.md`, and a short summary for the user. Never merge,
   never push, never install.

## Decision added (user, 2026-10-24)

8. **okfreq is installed in the project**, not as a global `uv tool`: P10.0 adds
   `okf-schema>=0.13.0` (published on PyPI) to a dependency group of `pyproject.toml`, relocks
   `uv.lock` with `UV_NO_CONFIG=1` (public index), and every okfreq call in the justfile, the
   guideline and the agents goes through `uv run okfreq`. This install is allowed for P10.0. It
   starts after the 7 remaining inventories and the 16 critics, in a branch with a PR (rule D33).

## Decision added (user, 2026-10-24, later)

9. **One PR finishes the CR**: batch 3 (theme-zoom, toolbar-navigation, table-editing,
   block-editing), batch 4 (palette-slash with F-CODE-029, review-annotations, lifecycle-sync,
   trust-security), P10.4 markers, P10.5 gap closure and P10.6 audit all land in a single PR on
   branch `changes-requests/059-requirements-batch3`, with one commit per scope or step. P10.4 and
   P10.5 change `src/` (comments only for markers) and `test/` (new tests): from P10.4 on, running
   `just check` and the affected test suites is required, and `just preflight` before the PR
   (real VS Code runs take `WINDOW-TESTS.lock`). Fixing a Known issue stays out of scope (backlog).
   The Known issues are put to the user one by one before the merge.

## Decision added (user, 2026-10-25)

10. **Reduce the baseline inside PR #62, before merge**: target about 400 SwRS (from 1863) and
    about 90 StRS (from 230), by removing overlap and restructuring the requirement tiles, with a
    possible code simplification without feature loss. An Opus audit proposes the analysis,
    mapping, code simplifications and plan (outputs in `reduction/`); the user validates the plan,
    then a Sonnet orchestrator applies it with markers and tests following. PR #62 is not merged
    until then.

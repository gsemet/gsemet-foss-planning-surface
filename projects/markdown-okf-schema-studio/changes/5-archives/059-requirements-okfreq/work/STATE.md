driver: orchestrator L (Sonnet) · updated: 2026-10-26
status: requirements reduction DONE in PR #62: squashed to one commit, pushed, checks green, mergeable; waiting for the maintainer's review/merge · round: —
head: changes-requests/059-requirements-batch3 @ e45990d (squashed) · PR: https://github.com/gsemet/markdown-okf-schema-studio/pull/62 · run: checks green
next: maintainer reviews and merges; then update the 11 backlog items (reduction/backlog-id-updates.md) and start the code-simplification follow-up PR (reduction/code-simplification.md) · question: backlog id updates in main checkout: apply now or after merge?

> **PARKED (U36, 2026-10-22): token cost too high for now.** Moved from
> archives/021-feature-session-007-020/p10-requirements. P10.1 partial: inventories done for rendering-core,
> code-blocks, gfm, frontmatter-schema, frontmatter-editing (no critic review yet); myst, diagrams,
> layout-width, theme-zoom, toolbar-navigation interrupted (not written); batches C, D not started.
> Decided 2026-10-22: requirements BEFORE the refactoring (they lock behaviour first);
> when resumed, use Sonnet only (inventory and review), no Opus, to cut token cost.
> Order: after P1 items and P2 e2e-campaign-rest.
> Resume: re-run extract-checklists.mjs after P9 lands, then continue P10.1 with remaining scopes.

# P10 — Requirements baseline with okfreq: state

Re-entrant tracker for post-plan item P10 (U30, U31, D32, D33). A resumed session reads this file
first, then `setup-plan.md`, `scope-briefs.md` and `checklists/index.md`. Update it after every
step (status cells, "Next action", "Last commit").

- Current step: **P10.1 inventories: complete** (16 inventories, 16 critic reviews, totals 920 behaviours: 824 tested, 92 untested, 4 doc-only, 263 undocumented; every checklist row cited or n/a/moved with the target citing it, 24 process/CI/release rows are n/a)
- Last commit: none (D33: P10 commits wait until the GitHub PR exists, see "Rules")
- PR: not yet created (post-plan "PR" item runs after T1, T2, F and preflight)
- okfreq: PATH has 0.12.0; **0.13.0 or newer required** (see setup-plan.md §1)

## Next action

P10.0 setup (okfreq as project dependency `okf-schema>=0.13.0`, `uv run okfreq`, branch + PR, rule D33), then P10.2 StRS. The PARKED note above is obsolete (resumed in CR 059, finished 2026-10-24).

## Steps

| Step | What | Who | Status | Output |
| --- | --- | --- | --- | --- |
| P10.prep | Setup plan, scope map, checklists, scope briefs | analyst (Opus) | done 2026-10-22 | `setup-plan.md`, `tools/`, `checklists/`, `scope-briefs.md` |
| P10.0 | Setup: okfreq ≥ 0.13 init, config.yml, schemas, guideline (baseline + overlay), `install-skills`, AGENTS.md section, justfile recipes in check/preflight, stats report, tiers/log.md | orchestrator | todo (after PR) | `requirements/`, `.agents/skills/okfreq*`, justfile, AGENTS.md |
| P10.1 | Inventory per scope (Opus, high effort) + Sonnet "what did it miss?" against checklists | Opus ×16, Sonnet ×16 | todo (can start before PR) | `inventory/<scope>.md` (`F-<TOKEN>-NNN`), `reviews/<scope>-inventory.md` |
| P10.2 | StRS per scope (use cases, user need) | Opus | todo | `requirements/tiers/strs/<scope>/` via `okfreq new strs` |
| P10.3 | SwRS per scope (one bounded SHALL, GIVEN-WHEN-THEN, `derives_from`) + Sonnet critical review | Opus, Sonnet | todo | `requirements/tiers/swrs/<scope>/`, `reviews/<scope>-swrs.md` |
| P10.4 | Traceability markers (`@implements_req` / `@tests_req`), `update-coverage`, `validate --prose --check-links`, `lint`, `trace --json` | Sonnet implementers | todo | marker commits per scope |
| P10.5 | Gap closure: tests for untested SwRS (gates B/T/E) or gap report; undocumented behaviours flagged to the user | Sonnet + orchestrator | todo | `gap-report.md` |
| P10.6 | Completeness audit: checklist item → SwRS → impl marker → test marker; stats; no placeholder left | Sonnet (critical) | todo | `reviews/completeness.md`, `out/reports/requirements/` |
| P10.7 | Landing: commits per step, archive `archives/0NN-requirements-baseline` report | orchestrator | todo | archive report |

## Per-scope status

Cell values: `todo`, `wip`, `done`, `reviewed` (Sonnet review passed), or a count (`12 StRS`).
Checklist items: count of rows in `checklists/*.md` whose scope is this scope (keyword-guessed
`?` rows included; analysts confirm or move them).

| # | Scope | Token | Checklist items | Inventory | StRS | SwRS | Markers | Review |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- |
| 1 | rendering-core | CORE | 66/66 | done (58 behaviours: 53 tested, 4 untested, 1 doc-only, 17 undocumented) | 5 StRS | wip | todo | APPROVE after 1 revision (orchestrator fixes) |; SwRS: APPROVE (re-check)
| 2 | code-blocks | CODE | 28/28 | done (33 behaviours: 22 tested, 11 untested, 0 doc-only, 17 undocumented) | 4 StRS | wip | todo | APPROVE after repair of a corrupted file |; SwRS: APPROVE (re-check)
| 3 | gfm | GFM | 16/16 (+2 claimed) | done (37 behaviours: 34 tested, 3 untested, 0 doc-only, 12 undocumented) | 4 StRS | wip | todo | APPROVE |; SwRS: APPROVE after re-check fix
| 4 | myst | MYST | 61/61 | done (73 behaviours: 70 tested, 3 untested, 0 doc-only, 19 undocumented) | 14 StRS | wip | todo | APPROVE after 1 revision |; SwRS: APPROVE after re-check fix
| 5 | diagrams | DIAG | 30/30 (+5 claimed) | done (55 behaviours: 45 tested, 10 untested, 0 doc-only, 13 undocumented) | 14 StRS | 120 SwRS | todo | APPROVE |; SwRS: REVISE, fixed; re-check FIX-REQUIRED, fixed (PR 59) |
| 6 | frontmatter-schema | FMSCHEMA | 52/52 | done (49 behaviours: 45 tested, 4 untested, 0 doc-only, 18 undocumented) | 18 StRS | 89 SwRS | todo | APPROVE after 1 revision |; SwRS: REVISE, fixed; re-check FIX-REQUIRED, fixed (PR 59) |
| 7 | frontmatter-editing | FMEDIT | 27/27 | done (35 behaviours: 30 tested, 4 untested, 1 doc-only, 10 undocumented) | 11 StRS | 87 SwRS | todo | APPROVE after 1 revision |; SwRS: REVISE, fixed; re-check FIX-REQUIRED, fixed (PR 59) |
| 8 | layout-width | LAYOUT | 94/94 (+8 claimed) | done (28 behaviours: 27 tested, 1 untested, 0 doc-only, 6 undocumented) | 9 StRS | 41 SwRS | todo | APPROVE |; SwRS: REVISE, fixed; re-check FIX-REQUIRED, fixed (PR 59) |
| 9 | theme-zoom | THEME | 24/24 | done (33 behaviours: 27 tested, 6 untested, 0 doc-only, 14 undocumented) | todo | todo | todo | APPROVE |
| 10 | toolbar-navigation | TOOLBAR | 62/62 | done (54 behaviours: 48 tested, 6 untested, 0 doc-only, 15 undocumented) | todo | todo | todo | APPROVE after 1 revision |
| 11 | block-editing | BLOCK | 59/59 (+15 claimed) | done (77 behaviours: 71 tested, 5 untested, 1 doc-only, 11 undocumented) | todo | todo | todo | APPROVE after 1 revision |
| 12 | palette-slash | PALETTE | 168/168 (+8 claimed) | done (105 behaviours: 103 tested, 2 untested, 0 doc-only, 21 undocumented) | todo | todo | todo | APPROVE after 1 revision (orchestrator fix) |
| 13 | table-editing | TABLE | 33/33 | done (54 behaviours: 50 tested, 4 untested, 0 doc-only, 16 undocumented) | todo | todo | todo | APPROVE after 1 revision |
| 14 | review-annotations | REVIEW | 81/81 (+2 claimed) | done (70 behaviours: 67 tested, 3 untested, 0 doc-only, 19 undocumented) | todo | todo | todo | APPROVE after 1 revision |
| 15 | lifecycle-sync | LIFE | 48/48 (+10 claimed) | done (86 behaviours: 74 tested, 12 untested, 0 doc-only, 21 undocumented) | todo | todo | todo | APPROVE |
| 16 | trust-security | TRUST | 22/22 | done (73 behaviours: 58 tested, 14 untested, 1 doc-only, 34 undocumented) | todo | todo | todo | APPROVE after 1 revision |

Total checklist items: 869 (regenerated 2026-10-24 on the 056 refactor layout; see `checklists/index.md` for the per-checklist split).

## Rules

- **IDs never reused.** Requirement IDs (`StRS-MDOKFSTUDIO-<TOKEN>-NNN`,
  `SwRS-MDOKFSTUDIO-<TOKEN>-NNN`, U31) and UUIDs are allocated only by `okfreq new`; a dropped
  requirement is archived/superseded (`okfreq archive` / `okfreq supersede --yes`), never deleted or
  renumbered. Checklist ids (`C-<KIND>-NNN`, `tools/checklist-ids.json`) and inventory ids
  (`F-<TOKEN>-NNN`) follow the same rule.
- **Creation through `okfreq new` only** (`--path . --project markdown-okf-schema-studio --scope
  <scope>`); never hand-write frontmatter, never hand-edit `derived_by`, `implemented_in_files`,
  `tested_in_files` (refresh with `okfreq update-coverage requirements`).
- **Commits only after the PR exists** (D33, U33). Until then, everything stays in this ignored
  folder. After that: one Conventional Commit per step and scope, no scope in the type for
  `docs:` / `test:` / `build:` (`.github/guidelines/git-commit-allowed-scopes.md`), end with the
  attribution trailer of the session reminder.
- **Idempotent steps.** Before creating a requirement, `okfreq search "<words>" requirements` and
  the scope's inventory line (`F-…` → requirement id column) must show it does not exist yet. Mark
  each inventory line with the requirement id(s) it produced; a re-run skips filled lines.
- **Markers** sit on their own line, at line start after optional indentation and a comment
  opener (`// @implements_req SwRS-…`, `# @tests_req SwRS-…`, ` * @tests_req …` inside a block
  comment). Trailing markers after code and `/** @tests_req …` on the opening line are NOT seen by
  okfreq (verified, see setup-plan.md §7). One marker per ID per file (a second one is reported as
  a duplicate).
- **StRS test markers** only on real stakeholder validation tests (integration / real-input / visual
  e2e), per `strs_test_coverage_mode: linked-swrs-and-validation-test`.
- **No builds, tests or VS Code** from analyst agents while other agents run gates; markers-only
  commits still pass `just check` before landing.
- **Checklists are regenerated, not edited** (except the SwRS column):
  `cd ../markdown-okf-schema-studio-wt-059 && fnm exec -- node <this folder>/tools/extract-checklists.mjs .` (CR 059: argument = code root).
  Scope map check: `cd ../markdown-okf-schema-studio-wt-059 && fnm exec -- node <this folder>/tools/scope-map.mjs .`.

## Journal

- 2026-10-24 11:00 DONE step 4+5: 7 analysts (diagrams 55, layout-width 28, theme-zoom 33, toolbar-navigation 54, table-editing 54, review-annotations 70, trust-security 73 behaviours) and 16 critics; 11 REVISE verdicts (mostly rows moved to a scope that did not cite them) fixed by one revision pass each; re-check APPROVE for all (3 with small orchestrator fixes: rendering-core, palette-slash, code-blocks). Global check: all 869 checklist rows cited in an F line except 24 process/CI/release/tooling rows (n/a). Code base: main 8513346 (refactor PR #51 merged, files identical to c166165). Reviews in reviews/.

- 2026-10-24 08:40 PAUSED on coordinator order. Step 4: 4 analysts finished and saved (myst 73, palette-slash 105, lifecycle-sync 86, block-editing 77 behaviours; checklist rows all covered). 7 scopes not started. No critic started. Worktree wt-059 kept.
- 2026-10-24 CR 059 step 3: Sonnet agent updated the evidence paths of the 5 existing inventories to the 056 layout (source of truth `c166165`); no behaviour removed; added F-CODE-030, F-CORE-048, F-CORE-049; noted fixed items F-CORE-034/035 and the `WorkspaceEdit` fallback removal (F-GFM-022).
- 2026-10-24 CR 059 steps 1-2: `tools/scope-map.json` remapped to the 056 layout (612 tracked src/test/sphinx files, 16 scopes + tooling, `scope-map.mjs <repo-root>` reports OK); `tools/extract-checklists.mjs <code-root>` adapted (messages from `core/protocol`, palette from `core/palette/paletteActions.ts`, toolbar from `core/preview/previewToolbar.ts`, page controls from `src/page/**`, archives read from this repo, ids kept; control ids moved by label) and re-run: 869 rows (was 703; CHANGELOG, archives and visual scenarios grew since the first extraction), no retired id.

- 2026-10-22 P10.prep: scope map (312 tracked src/test/sphinx files → 16 scopes or tooling),
  10 checklists (703 items), setup plan, scope briefs. Found: PATH okfreq 0.12.0 lacks the flags
  the okf-schema justfile uses; marker regex ignores trailing and `/** @…` markers;
  frontmatter-editing has no exclusive source file.
- 2026-10-24 19:56 P10.0 landed: PR #55 merged (main 8f0315b). Batch 1 of P10.2+P10.3 started.

## Journal (batch 1)

- 19:58 branch changes-requests/059-requirements-batch1 created in wt-059; StRS analysts launched (4 scopes).
- 20:05 StRS done: CORE 5, CODE 4, GFM 4, MYST 14; SwRS analysts launched.
- 20:15 SwRS done: CORE 66, CODE 30, GFM 36, MYST 87; critics launched.
- 20:40 PR #56 opened, checks green, mergeable. Reviews: REVISE x4, fixed in one pass.
- 21:10 Re-check: rendering-core APPROVE, code-blocks APPROVE, gfm and myst FIX-REQUIRED (stale descriptions, glued headings) -> fixed, 2 commits, pushed, checks green, mergeable.

## Journal (batch 2)

- 21:06 branch changes-requests/059-requirements-batch2 created in wt-059 from origin/main; StRS analysts launched (diagrams, frontmatter-schema, frontmatter-editing, layout-width).
- 21:10 StRS done: DIAG 14, FMSCHEMA 18, FMEDIT 11, LAYOUT 9; SwRS analysts launched.
- 2026-10-24 User decisions on batch-1 open points: (a) CORE-021 kept as a core-pipeline behaviour, not reachable from VS Code; (b) includes in Restricted Mode: code is right, doc fix filed as backlog/P3/docs-includes-restricted-mode.
- 2026-10-24 (c, d) colour grammar + diagnostic code: fix, backlog/P3/html-colour-grammar.
- 2026-10-24 (e) currency '$' rendering: verify first, backlog/P2/currency-dollar-preview-check.
- 2026-10-24 (f) copy button keyboard path: fix, backlog/P2/copy-button-keyboard. F-CODE-028 must be specified as current behaviour (Known issue), not skipped.
- 2026-10-24 (g) checkbox refusal tooltip-only, malformed toggle leaves box busy, misleading standalone message: fix, backlog/P3/checkbox-refusal-feedback. Specify as current behaviour (Known issue).
- 21:26 SwRS done: DIAG 111, FMSCHEMA 74, FMEDIT 71, LAYOUT 35. Removed 17 accidental duplicate FMSCHEMA StRS (019-035, uncommitted); fixed <word> placeholders in 6 FMSCHEMA StRS. Gates green. Critics launched. Coordinator extra: re-read batch-1 skips (F-CODE-028, F-MYST-018 ...) for the follow-up commit.
- 21:33 Critics: all 4 REVISE (diagrams 12, fmschema 25, fmedit 14, layout 14 defects). Revision pass launched (same analysts resumed).

- 2026-10-24 22:20 Batch 2 J: gates green (655 req), 4 re-checks FIX-REQUIRED, one fix pass each (splits: DIAG-120, FMSCHEMA-088/089, FMEDIT-086/087, LAYOUT-041); follow-up: CODE-026/027/017, GFM-024/026/027 Known issues, MYST-094 (F-MYST-044), MYST-095 (F-MYST-018); 5 commits, PR 59 opened. F-CODE-029 goes to palette-slash in a later batch.
- 2026-10-24 batch 2 decisions: (1) no backlog ids in requirement text: remove the 'Backlog: P3/checkbox-refusal-feedback.' lines of GFM-024/026/027, add the rule to the guideline. (2) empty YAML schema: backlog/P3/empty-yaml-schema; messages owned by okf-schema (gsemet/okf-schema#41).
- 2026-10-24 (3) field editor in error + click on a block: cancel the field and open the block, backlog/P3/field-editor-error-then-block-click.
- 2026-10-24 (4) {doc}/{download} empty link: fix, backlog/P3/doc-download-empty-link. Target checks and {numref}: no change (stay Known issue).
- 2026-10-24 follow-up (PR 59): backlog ids removed from 7 SwRS + guideline rule; LAYOUT-042 added (first-bar-bottom); FMEDIT-035/086 + FMSCHEMA-041 cover the closed-schema flag; critic re-check 2: diagrams, frontmatter-editing fixed (DIAG-004 note, inventory row), fmschema and layout APPROVE. Deprecated DIAG-021, FMEDIT-080/081 stay in derived_by and the index by okfreq design.

## Journal (batch 3)

- 23:00 branch changes-requests/059-requirements-batch3 created in wt-059-b3 from origin/main (885eb4e); header fixed (PR 59 merged); 4 analysts launched.
- 23:50 (batch 3) analysts done: THEME 12 StRS/55 SwRS, TOOLBAR 14/133, TABLE 15/120, BLOCK 26/250. Rebased on origin/main (PR #60). Gates green (1281 requirements). NOTE: use /Users/az02065/Projects/DevTools/markdown-okf-schema-studio/.venv/bin/okfreq (worktree .venv lacks okf-schema). Critics launched. Scope extended by coordinator (decision 9): one PR for whole CR (batch 4, P10.4 markers, P10.5 tests, P10.6 audit, preflight).
- 00:20 batch 3 critics: all REVISE (THEME 18, TOOLBAR 24, TABLE 17, BLOCK 18 defects); revision pass launched (same analysts resumed). Nothing committed yet (explicit paths at commit time).
- 00:50 batch 3 re-check: THEME 1, TOOLBAR 6, TABLE 5, BLOCK 5 defects FIX-REQUIRED; last fix pass sent. Open decisions: THEME-052/053 restored (own zoom rules); TABLE-029 restored; BLOCK-227 thread guard goes to review-annotations (batch 4).
- 01:20 batch 3 DONE: 4 commits (d690dbf theme, 157f5dc toolbar, 855a0eb table, block) on wt-059-b3; counts active StRS/SwRS THEME 13/52, TOOLBAR 14/147, TABLE 15/121, BLOCK 25/241. Last fix passes (after re-check FIX-REQUIRED) NOT re-checked by a critic, only by validate/lint/coverage gates and a script (no active text cites a deprecated id). Next: batch 4 (palette-slash+F-CODE-029, review-annotations (cite DIAG-019/020; BLOCK-227 thread guard + read-only thread refusal go here), lifecycle-sync (F-LIFE-054 reading-mode click reveals source; cite TOOLBAR-120..133,147..149 for anchor/scroll/mark), trust-security (+CORE-066; cite BLOCK-121/181/224, F-TABLE-049 read-only half)). No PR yet.
- 02:10 batch 4 analysts done: PALETTE 27/270, REVIEW 18/216, LIFE 21/165, TRUST 14/78 (StRS/SwRS, before critics). Gates green. Critics launched.
- 02:50 batch 4 critics REVISE (PALETTE 21, REVIEW 14, LIFE 24, TRUST 13); revision pass sent with cross-scope ownership decisions (trust owns read-only/envelope/nonce; lifecycle owns package contract; REVIEW-165 over PALETTE-086).
- 04:10 batch 4 re-check: PALETTE 4, REVIEW 2, LIFE 8, TRUST 8 FIX-REQUIRED; last fix pass sent (trust archives CORE-020, adds fresh-nonce SwRS; lifecycle takes package contract 700-char/no-languages; LIFE-074 archived).
- 05:30 batch 4 DONE: 4 commits (2338856 palette, 45a5506 review, be1aa1d lifecycle, b5a6b04 trust+CORE-020 archived). Active StRS/SwRS: PALETTE 27/272, REVIEW 18/215, LIFE 22/155, TRUST 15/85. Last fix pass (after re-check FIX-REQUIRED) not re-checked by critic. P10.4: widened config.yml source_dirs=[src,sphinx], test_dirs=[test,sphinx/tests] for all scopes (decision); method: locator agents write scratchpad/locate/<scope>.json, script scratchpad/apply_markers.py inserts markers (no file conflicts).
- 08:30 P10.4 done: markers applied (4 commits: build config widen, src markers, test markers (+4 .markers.ts companion files for files at the size limit), requirements coverage refresh); rebased on origin/main (be74ea4/dbb26d7); just check passes (UV_PROJECT_ENVIRONMENT=main .venv, worktree .venv has old okfreq). Coverage: SwRS source 95.82% (1834/1914), tests 82.08% (1571/1914), StRS tests 1.74% (4/230), combined 80.88%; before: ~0 (no markers). Gap: 29 SwRS no impl marker, 292 no test marker. P10.5 gap closers launched (9 agents, new test files).
- 10:00 P10.5 done: 9 gap closers wrote new tests (81 files under test/, all pass, just check green); StRS validation markers applied (62.6% StRS covered); archived SwRS exempted. Coverage: source 98.82%, tests 99.73%, StRS 62.61%, combined 98.55% (before 0). gap-report.md written. Next: P10.6 audit -> reviews/completeness.md, then preflight, PR.
- 11:30 P10.6 audit (reviews/completeness.md) FIX-REQUIRED 12 defects -> one fix pass done (D1 notes 300+, D8/D9 wording, D7 tests, D2 checklist+inventory trace recorded, D3 22 exemptions, D4, D5 guideline, D12 log). Not done: D6 coarse markers (style modules, integration run()), D5b companion check script, D3 DIAG-012/013/014/031/116 browser tests. just check green. Next: just preflight, then PR.
- 13:00 preflight: ci-static + ci-visual pass; ci-integration failed twice (real-input undo timeout, reload suite timeout: window focus flakiness, frontmost app was VS Code) and passed on the third run, then ci-report and ci-gallery passed. Needs env -u ELECTRON_RUN_AS_NODE -u VSCODE_*. Next: push + PR.
- 13:30 PR https://github.com/gsemet/markdown-okf-schema-studio/pull/62 opened; waiting for checks.
- 2026-10-25 PR #62 known issues triage: (1) TRUST-071 Restricted Mode capability: verify then fix, backlog/P1/restricted-mode-capability.
- 2026-10-25 (2) LIFE-155 trust grant keeps read-only: backlog/P2/trust-grant-refresh. TRUST-088 maps to the existing P3/docs-includes-restricted-mode (doc fix, user decision of 2026-10-24).
- 2026-10-25 (3) CORE-014 empty include argument fails the render: backlog/P2/include-empty-argument.
- 2026-10-25 (4) PALETTE-181 + 10 SwRS stale after autosave: verify then fix, backlog/P1/palette-stale-after-autosave.
- 2026-10-25 (5) BLOCK-015/018/024 inline link also opens the editor: verify then fix, backlog/P2/inline-link-opens-editor.
- 2026-10-25 (6) refused open empty frame (BLOCK-216/039/134/160, TABLE-034): backlog/P2/refused-open-empty-frame.
- 2026-10-25 user: triage the remaining Known issues autonomously. Filed P2: stale-request-no-answer, block-editor-save-races, block-edit-line-endings, table-insert-splits-table, table-cell-paste-linebreak, switch-back-state-lost, watcher-ignore-absolute-path, page-security-hardening. P3: table-editor-polish, link-navigation-fixes, toolbar-band-fixes, preference-write-failure, readonly-reason-wording, comments-button-hides-threads, lifecycle-small-fixes, block-editing-small-fixes, requirements-test-quality. No item: THEME-017 (note), TRUST-019 (VS Code-supplied CSP). PR #62 open questions accepted as decided by the orchestrator (22 exemptions, *.markers.ts, scan folders).
- 2026-10-25 reduction audit (Opus): 311 SwRS / 76 StRS possible. User: ~370 variant (one SwRS per palette action and per message type). Main session: delete never-merged PR #62 files + log retired ranges; supersede main-scope ids; code simplifications in a follow-up PR; okfreq id reuse reported as gsemet/okf-schema#42. Opus reworking mapping and plan.
- 2026-10-26 main session: PR #62 squashed to one commit (e45990d), 76 StRS / 364 SwRS, checks green, mergeable. Backlog ids updated from reduction/backlog-id-updates.md; 33 backlog items point to reduction/mapping.csv. okf-schema PR gsemet/okf-schema#43 (okfreq-setup skill) green. Next: user merges #62 and #43; archive CR 059; code-simplification follow-up PR (reduction/code-simplification.md).

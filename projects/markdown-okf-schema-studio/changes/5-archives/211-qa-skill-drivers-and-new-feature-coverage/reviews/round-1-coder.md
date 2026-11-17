Coder round 1 summary: items 1-5 + pitfalls implemented. Files: SKILL.md, references/charters.md,
references/harness-pitfalls.md, references/use-cases.md (okf/ corpus refs -> docs/ & fixtures-visual),
scripts/new-features.py (new; searches merged:>=DATE and drops PRs whose merge commit is ancestor of
recorded revision; --since/--campaign/--json-file/--dry-run), scripts/coverage-map.py (Revision: `sha`,
"at commit `sha`", QA_CHANGES_ROOT, --campaign, fallback newest 04-archives/*qa-campaign*, non-ancestor
sha skipped with note), scripts/setup-workspace.sh (env-var corpora: BOOK_DIR, visual, docs,
fixtures-qa from sibling skill, synth, VAULT_DIR optional; okf-schema removed; workspace at $QA_ROOT/ws),
scripts/noop-sweep.mjs (link-only skip, --follow-links, navigate-back heuristic Meta+1/Alt+Left; exported
selectTargets/isLinkOnly helpers; --limit already applied without --from), scripts/engine.mjs
(substitute(): single ${var} field of a known numeric field with integer value -> Number).
Open points: nth failure not reproduced (clicksel/qa.mjs already Number()); navigate-back untested live;
isLinkOnly helper exported but in-page logic is a copy; bug-sheet-template.md placeholder links
../evidence/image.jpg unresolved (pre-existing).
Dry runs: new-features --campaign 210 -> 0 PRs since 2026-10-31 (empty table); --since 2026-10-20 -> 132 PRs.
coverage-map --campaign 210 -> "Baseline: b9118506 ... (--campaign)". setup-workspace -> 192 md files, vault skipped.

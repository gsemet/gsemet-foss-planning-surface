# CR 211 report

Commit c1399a18075664f9beff5453cc8c8bc421e7cc17 (parent b9118506), branch
change-requests/211-qa-skill-drivers-and-new-feature-coverage, not pushed (Foreman delivers).
41 files under .agents/skills/markdown-studio-exploratory-qa-claude/ (10 modified, 31 new: 29 campaign-210
scenarios/synth, scripts/new-features.py, assets/synth/admon.md).

Rounds: R1 Coder+Inspector (CHANGES REQUESTED, 11 findings); R2 Coder + 2 follow-up Coders (item 7, #228 false
positive, owner replay fixes a/b) + Inspector (CHANGES REQUESTED, sweep way back); R3 Coder + Inspector (APPROVE).
Items 1-7 and owner replay fixes done. Gates: bash -n, py_compile, node --check, scenario JSON parse, relative
links: OK. `just check` not run: it does not cover .agents/skills (format=just --fmt, compile, unit, contracts...).
Dry runs: coverage-map --campaign 210 -> Baseline b9118506; new-features --campaign 210 -> 0 rows (#228,#230-#236
already in b9118506); setup-workspace (QA_ROOT scratch, no VAULT_DIR) -> 193 md files, deleted afterwards.
Open: noop-sweep goBack()/abort never run live; Inspector R3 non-blocking minor: one failed doc-id read aborts the
sweep (suggest re-read after 250 ms).

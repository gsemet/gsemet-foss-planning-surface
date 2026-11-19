# Conflicts: CR-382 rebased onto CR-381 head 105ad668

- docs/how-to/use-cases-direct.md, docs/how-to/use-cases-foreman.md (Factory mode paragraph): kept CR-382's restyled wording, replaced `../README.md#factory-mode` with `https://github.com/gsemet/chantier#factory-mode` (CR-381's intent).
- skills/chantier/scripts/cli/tests/test_docs_site.py: kept both functions: CR-381's `test_skill_and_references_links_resolve` (moved here; one copy only) and CR-382's `test_the_docs_style_guide_is_wired_in_and_stays_out_of_the_rules`; imports merged (`SKILL`, `repo_file_of`, `linked`). File is CRLF; blank lines normalised to CRLF so ruff format passes.
- Second commit f5d25780 (GitHub URL link): dropped by git, patch already upstream.
- No BOM added.

Fast gate: `UV_PYTHON=3.13 just check` in the worktree, result: pass (exit 0) after the CRLF fix. That fix is an uncommitted working-tree change to test_docs_site.py (line endings of blank lines); the Driver must commit it.

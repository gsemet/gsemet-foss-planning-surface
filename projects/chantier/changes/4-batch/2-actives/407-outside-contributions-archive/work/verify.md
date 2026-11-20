# Verify CR-407

Head: 68c5a68d34472a6295a6b3ce7dad92a14582dadb

All claims judged at 68c5a68.

1. validate on prepared trees (scratch project, `chantier validate`, one archive folder each, removed after).
   - 261120-1015-outside-42-fix-typo: `no error, no gap (1 CRs)`, exit 0.
   - 261120-1015-outside-fix-typo, outside-42-fix-typo, 261120-outside-42-fix-typo, 261120-1015-outside-42-Fix_Typo, 261120-1015-outside-42-: each `1 error(s), 0 gap(s) in 1 CRs` and one line `error 5-archives/<name>: not an outside archive's name (<YYMMDD-HHMM>-outside-<number>-<slug>) -> rename it`, exit 3.
   - 261120-1015-412-outside-contributions-archive, 264-edit-outside-trusted-workspace: `no error, no gap (1 CRs)`, exit 0.
2. `pytest tests/test_validate.py`: 55 passed (new parametrized test and the unchanged format-only test). `pytest test_startup_manifest.py test_plugin_files.py test_code_targets.py`: 82 passed.
3. Help: `chantier validate` text in `chantier --help` line 111: "outside archives' names, summary.json's format" (validate --help itself shows only the usage, as before).
4. Card and docs: diff read against spec 3.2 and 5: Entry points row, "An outside PR" paragraph (writer first, read-only forge read, three write-nothing cases, two files with delivery.md shape, summary lint/set, sync now, reply line), docs/planning-folder.md (tree line + validate paragraph), docs/planning-modes.md, concepts.md all match.
5. Real read: `gh pr view 380 --repo gsemet/chantier --json number,title,url,author,state,mergedAt,files,body` returns keys author, body, files, mergedAt, number, state (MERGED), title, url; mergedAt 2026-11-20T14:55:52Z.
6. PR description (pr-body.md): consistent with the diff (7 files); Known gaps hold GitLab unproved, card untested, `just test` time unmeasured; no images. Review box: log note "r1 approved at 9841318, committed as 68c5a68" matches. "Verified at"/"CI green at" boxes are the Driver's to fill.

VERIFIED

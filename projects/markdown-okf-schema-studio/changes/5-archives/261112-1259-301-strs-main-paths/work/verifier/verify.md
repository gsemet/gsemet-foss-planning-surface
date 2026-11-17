# Verify CR-301 at 040e40a1a61f09d83817fd795f97a7ea071cab15

- Check run: "main paths: 78 StRS checked, 536 SwRS citations, all valid", exit 0.
- Mutations of a cited ID in DIAG-001 (reverted with git checkout):
  - DIAG-999: ":116: ... does not exist"
  - DIAG-071 (superseded): "is superseded, not active" (+ does not derive from)
  - DIAG-023 (active, other StRS): "does not derive from StRS-MDOKFSTUDIO-DIAG-001"
- Count: 78 with a section + TRUST-012, TRUST-014 (no section, listed in log.md with reasons) = 80.
- 16 approved StRS: approved_by gaetan@xeberon.net, approved_at and verified.at 2026-11-12T12:30:00+01:00.
- just requirements-lint: passes (indexes, projections, coverage unchanged, check_main_paths valid).
- just release-tests: 178 passed.
- just requirements-update: no diff (git status clean).
- Read TOOLBAR-002, TABLE-001, DIAG-001 paths against SwRS (TOOLBAR-004/006, TABLE-025/119 and others): faithful.
- Not run: just preflight, real-input (excluded by brief).

VERIFIED

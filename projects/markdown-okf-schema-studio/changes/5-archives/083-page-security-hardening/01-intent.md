# Harden the preview page: sanitizer allow-list and message origin

Triage (2026-10-25, autonomous, user asked to triage without technical questions): P2.

Current behaviour is specified as-is with "Known issue" in the SwRS listed below (PR #62 baseline).
The fix updates those SwRS in the same change.

SwRS TRUST-048, TRUST-060, TRUST-045.

- The sanitizer is a deny-list: `base`, non-stylesheet `link` and unknown attributes pass (the CSP
  limits the damage).
- The page does not check the origin of window message events (src/page/hostTransport.ts).
- An ignored linked stylesheet stays in the page although the diagnostic says it is ignored.
- Expected: allow-list sanitizer, origin check, remove ignored link elements; security tests.
  TRUST-019 (VS Code-supplied CSP wildcard) is not ours and stays a note.

Requirement ids older than the baseline merge map to their current tile in `.agents/changes/archives/059-requirements-okfreq/reduction/mapping.csv`.

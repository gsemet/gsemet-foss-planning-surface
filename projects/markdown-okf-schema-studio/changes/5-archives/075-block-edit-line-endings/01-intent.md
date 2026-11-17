# Block edits and insertions with CRLF or lone-CR line endings

Triage (2026-10-25, autonomous, user asked to triage without technical questions): P2.

Current behaviour is specified as-is with "Known issue" in the SwRS listed below (PR #62 baseline).
The fix updates those SwRS in the same change.

SwRS BLOCK-060 (deduced, verify first), BLOCK-094, BLOCK-101.

- Verify first: a multi-line block saved in a CRLF document may come back with LF inside (mixed
  line endings), which matters on Windows.
- The insertion planner finds line ends by LF only: in a lone-CR document an insertion lands at the
  end or is refused as stale.
- Expected: edits and insertions keep the document's line ending; unit tests for LF, CRLF, CR.

Requirement ids older than the baseline merge map to their current tile in `.agents/changes/archives/059-requirements-okfreq/reduction/mapping.csv`.

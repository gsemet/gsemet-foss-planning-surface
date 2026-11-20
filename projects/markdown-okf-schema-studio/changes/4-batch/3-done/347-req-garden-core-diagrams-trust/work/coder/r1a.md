# CR-347 Round 1, pass A (coder): done

Scope: spec section 1 (four new StRS) and the reparenting of sections 1 and 4. Sections 2, 3, 5-9 untouched (open, later passes).

## Checklist
- New StRS DIAG-015 (charts and drawings), CORE-006 (writing skill), CORE-007 (release), CORE-008 (published site): done. Created with `okfreq new strs ... --lifecycle proposed`; Normative behavior, Preserved stakeholder intent (the User need), Rationale and constraints, Main paths written. Main paths cite only SwRS they derive. Use case diagrams: open (pass for section 8).
- Moved: DIAG-121..127 to DIAG-015; CORE-073/074 to CORE-006; CORE-075/076/078 to CORE-007; CORE-069, 080..086 to CORE-008: done (old parent replaced in derives_from).
- Dropped: TRUST-052 (CORE-001), REVIEW-017 (DIAG-001, DIAG-006), REVIEW-038 (same), DIAG-001 SwRS (DIAG-006), TRUST-074/075 (DIAG-006), TRUST-065/090 (DIAG-009), LIFE-026 (TRUST-001), CORE-041 (TRUST-006), BLOCK-238, FMEDIT-054, GFM-027 (TRUST-009), LIFE-062 (TRUST-004; it keeps LIFE-007): done.
- Not droppable, parent kept (note for the log): TRUST-086 (only TRUST-009) and DIAG-050 (only DIAG-009). Both already had depends_on TRUST-052; no edit needed. TRUST-052 keeps TRUST-009.
- REVIEW-017/038 `relates_to` the diagram SwRS: open (only if the exclusion of diagrams is a scenario of theirs; their bodies belong to the review scope CR, not checked).
- Approved StRS CORE-001, DIAG-001, DIAG-006: no text change; none of their Main paths cites a moved SwRS (no stop needed). approved_by/at untouched.

## Notes
- Files created by okfreq came with CRLF; I converted the four new StRS to LF to match the repo.
- Main path of CORE-008 cites CORE-084 and CORE-083 as options; CORE-085 (social cards) and CORE-086 (cream look) are not in a path (they are not steps of the path).
- Moving SwRS out of TRUST-014 (CORE-069, 080..086) leaves TRUST-014 with TRUST-074/075 as the spec intends.
- The notes from r1.md about TRUST-006 merge, DIAG-061, and CORE-002 remain for later passes.

## Gates
- `just requirements-update`: pass (2 indexes updated; only pre-existing W2 broken-cross-link warnings).
- `just requirements-lint`: pass (1130 requirements, 0 errors, 27 warnings; main paths: 83 StRS, 559 citations, all valid).
- `just check-markers`: pass (451 in-force SwRS marked, 50 baseline files).

## Hand-over
Pass B: merges and splits (section 3); pass C: StRS text, diagrams (also for the four new StRS), W002, log entry. Scripts: work/scratch/reparent.py and bodies.py (already applied; do not rerun).

# Garden the requirements of rendering-core, diagrams, trust-security

From the requirements gardening audit, CR requirements-gardening (projects/markdown-okf-schema-studio/changes, evidence/audit-synthesis.md): the findings and the proposed old-to-new mappings are in evidence/audit-core-diagrams-trust.md.

Goal: a human reviewer understands these use cases by reading their StRS; each SwRS is one observable behaviour, traced by markers on the code that does it and on the tests that check its scenarios.

- Fix the StRS text that contradicts its SwRS or the code; an approved StRS changes only with the owner's recorded re-approval.
- Add the missing StRS and split the umbrella StRS named in the report.
- Reparent: shared rules are cited with depends_on, not derived; each SwRS derives from the use case it serves.
- Merge and split SwRS per the report's mapping, with okfreq supersede / archive. Owner decision (2026-11-17): published requirements are never deleted.
- Move markers onto the code and the tests they name; mark the real tests cited in the verification notes; fix markers on the wrong test.
- Give every StRS a validation test on a real scenario (not the companion list); add tests for the scenarios no test checks.
- Candidates draft -> proposed are changed only on the owner's word.
- Write each StRS's use-case diagram (rule of CR req-use-case-diagrams).

Depends on: req-use-case-diagrams, req-marker-gate.

# Verify CR-429

Head: c749c3b5d5ebcb0397902d8230a19534c6e83e29

Verdict: VERIFIED

All claims judged at c749c3b5d5ebcb0397902d8230a19534c6e83e29, in the CR's worktree.

1. The check rejects a reserved id and names file, line, StRS and word. Temporary edit (not committed) of
   `requirements/tiers/strs/palette-slash/StRS-MDOKFSTUDIO-PALETTE-007.md`, `Field` to `Box` on lines 72 and 79.
   Command: `just requirements-lint`. Exit 1. Output:
   ```
   requirements/tiers/strs/palette-slash/StRS-MDOKFSTUDIO-PALETTE-007.md:79: StRS-MDOKFSTUDIO-PALETTE-007: the use case diagram does not parse (see "Use case diagram of a StRS" in requirements/guidelines/project.guidelines.md)
       Parse error on line 13:
       ...ment        Page->>Box: insert or repla
       ----------------------^
       Expecting 'link', '+', '-', '()', 'ACTOR', got 'box'
   error: recipe `requirements-lint` failed on line 174 with exit code 1
   ```
2. Before (base lets it through). `git diff origin/main...HEAD -- justfile` shows the only recipe change is the added
   `{{ npm }} run check:diagrams` line. With the same edit in place, the four base lines (validate, lint, update-coverage
   --check, check_main_paths.py) ran before it in the run above and passed ("0 indexes would change", "0 files would change",
   "main paths: 92 StRS checked ... all valid"); only the new line failed.
3. Restore. `git checkout -- <that file>`; `git status --short` empty; `git rev-parse HEAD` = c749c3b5d5ebcb0397902d8230a19534c6e83e29.
4. Clean tree passes: `just requirements-lint` tail: `use case diagrams: 93 StRS checked, all parse (Mermaid 12.2.0)`.
5. Unit tests: `just unit` fail 0, pass 4066; the seven new tests listed ok (refusal Box, refusal state, every failure reported,
   boundary/CRLF, shipped bundle count, every guideline id rejected, comment/directive line mapping).
6. Guideline: `git diff origin/main...HEAD -- requirements/guidelines/project.guidelines.md` adds the check description and the
   lists of reserved ids for sequenceDiagram, flowchart, stateDiagram-v2.
7. Cited, not rerun: gate log work/gates/20261120-104044.log first line `gate CR-429 ... head c749c3b5...` (just preflight pass);
   work/gates/prepush-check.log (just check pass). CI at c749c3b: `gh pr checks 434`: checks, report, static, static-windows,
   visual pass; integration, stress, others skipping.
8. PR body (posted body equals pr-body.md, diffed): Summary, Deliverables (npm script, script, message format, last line),
   Changes (script, package.json, justfile, guideline, SwRS-CORE-090 + StRS-TRUST-014 + log/index, test file) match the 9-file
   diff stat. Autonomous decisions: the Box-as-participant-declaration behaviour is covered by the test "refusal: ... used in a message"
   and the comment-line mapping by its own test. Review box: log note "r1 approved ... committed as c749c3b5" proves it.
   Observations, not failures: Test plan boxes "New or changed tests", "Requirements" and "CI green" are unchecked although
   proved above; Known gaps "None" is consistent (no UNVERIFIED claim). The mid-body claim that 12.2.0 parses a reserved participant
   declaration was not rerun separately (the Box edit declared it and the error came on the message line 79, consistent with it).

## Description pass at c749c3b5d5ebcb0397902d8230a19534c6e83e29

Posted body (`gh pr view 434 --json body`) equals pr-body.md (diff: only the trailing newline). Sections of the template present (Summary, Deliverables with a Mermaid diagram and output, Changes, Impacts, Blast radius, Test plan, Known gaps). Changes match the 9-file diff stat. Test plan boxes now checked and match the proof above: unit 4066 pass at c749c3b, preflight and check pass, review note "r1 approved ... committed as c749c3b5", `gh pr checks 434` static, static-windows, visual, report, checks pass. No role names, no images, no internal references. Known gaps "None": no UNVERIFIED claim. VERIFIED.

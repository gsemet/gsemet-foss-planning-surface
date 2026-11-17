# Verify CR-165 at a5a4e48 (PR 106)

Verdict: VERIFIED.

Note: no verifier.md card exists in skills/chantier/references; verified against the spec and the PR body Deliverables.

| Claim | Proof |
|---|---|
| Retro at each pause and release, `4-batch/retro.md`, one line per problem with fix, offered as numbered inbox items before close | Diff of foreman.md, status-layout.md (Completion "Retro", For you line), chief-of-staff.md, concepts.md, docs, read against spec section 1. Cards only, no test (agent behaviour, per spec). |
| CoS cost split: steering (in spend/budget in direct mode), grill and specifications (outside), whole session with compaction count | evidence/pytest-a5a4e48.txt (42 passed, incl. the turn-rule unit test); scenario checks run_scenario.py ~720-745, 897, 1010-1058 (add up, no `Chief of Staff (steering)` line, `2 compactions since the batch opened`, earlier-batch turns excluded); gate log 459/459 on github and gitlab. |
| Unknown, never 0 (Copilot, no transcript, untimed calls) | scenario lines 2996-3011 (`unknown: not measured on this host`), "not placed" check; gate log. |
| status and STATUS.md say who steers and the shape; no steering = unknown; STATUS.json null | status.py diff (`steering_word`, `shape_word`, `batch_markdown`, `foreman` default removed); scenario 955-977, 1153. |
| `just check` | Re-run at a5a4e48: 42 passed, release-notes ok. |
| `just scenario` | evidence/scenario-gate-a5a4e48.log: github 459/459, gitlab 459/459. |

Deviations, disclosed in the PR body or commit: shape also has `series`, default shape `parallel` (a5a4e48); the direct-mode "steering outside the budget" line prints only when spent outside the claim window; untimed calls are in neither share and are reported. None contradicts a Deliverable.

Not proven by execution: the macOS/Windows legs of CI (reported green by the caller, not re-observed); retro behaviour of the cards (read only).

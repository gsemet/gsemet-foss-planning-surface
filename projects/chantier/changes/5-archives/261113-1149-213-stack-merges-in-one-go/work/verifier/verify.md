# Verify CR-213 at 548e0f7
- just check at head: 58 passed, release-notes ok.
- forge_stack.py read: create/show, five checks, GitHub-only refusal, exit 2/4 as spec.
- Gate log 20261113-105001: github 649/649, gitlab 637/637; transcript steps seen: create refused (no PR), create once bottom-to-top, second create exit 4, show draft/order/release/closed/missing/foreign, GitLab "GitHub only", insertion order.
- 12 roles x 2 hosts: description ends "Prompt starts with: `chantier ...`", refusal names the line and a new start.
- SVG/texts: batch-modes, cr-lifecycle(+simple) changed in step; new text lines short enough for their boxes (no overflow by width estimate).

## Description pass (PR 156 body at 548e0f7)
- Head, 5 CI checks green, counts (58, 649/649, 637/637) match earlier evidence.
- FAIL: agent roles appear outside Internal references: Summary 'the stack driver left every PR'; Changes 'driver.md, foreman.md, chief-of-staff.md' and 'Foreman' wording. Reword (e.g. 'stack batches left...', 'cards for stack creation, batch start and routing').
- GitHub reviewDecision is empty; 'Review approved' rests on the chantier review record.
- Re-check of the reworded body at 548e0f7: no role word outside Internal references; other claims unchanged. VERIFIED.

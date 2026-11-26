# Simplify the role cards and the agents' prompts

The cards and the agent prompts have become very complicated. Plan how to simplify them: each role should boot on a short card, rules should live in one place, and rules that only record a past incident should leave the cards.

Measured at 0.15.1 (bytes; lines):
- chief-of-staff.md 206 KB (2310 lines): "While it runs" 67 KB, "Backlog and grill" 40 KB, "Steering a batch yourself" 19 KB, "Starting a batch" 17 KB.
- driver.md 135 KB (1611 lines): Stack driver 31 KB, Release driver 11 KB, CR driver re-takes 9 KB.
- hosts/claude-code.md 109 KB (962 lines): "Allow rules" 26 KB (the same "Risk accepted" paragraph repeated on 14 rebase rows), "Tools" 20 KB; 103 lines say "unproved", 70 mention a "Trial", 39 name a batch.
- foreman.md 85 KB, concepts.md 74 KB, foreman-stack.md 17 KB, status-layout.md 17 KB, pr-template.md 17 KB.
- The 15 agent wrappers are small (1 KB each) and almost identical; the 4 SKILL.md are 4 KB each, with one 2 KB paragraph ($CHANTIER, dev/plugin mode) copied in each.
- Total references: 808 KB, about 200 K tokens; a Griller's boot reads session-start (13 KB) + sync + titles + its card (11 KB), then points at chief-of-staff.md "Backlog and grill" (40 KB) and hosts/claude-code.md (109 KB) "with its card".
- Verbatim repeated long sentences across cards: 41, about 20 KB redundant (worker cards repeat the same 5 boilerplate rules); the real bloat is size per card and incident history, not copy-paste.

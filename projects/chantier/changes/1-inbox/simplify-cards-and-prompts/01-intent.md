# Simplify the role cards and the agents' prompts

The owner finds the cards (`skills/chantier/references/*.md`) and the agent prompts very complicated. Intent: specify a plan that makes every role boot on a short, readable card, with each rule in one place and no incident history in the text a role reads, without losing a rule that protects the user (never merge, rebase only, no fallback, the user's boundaries).

Measured first (see `intake/request.md`): the cards total 808 KB; `chief-of-staff.md` is 206 KB, `driver.md` 135 KB, `hosts/claude-code.md` 109 KB, `foreman.md` 85 KB, `concepts.md` 74 KB. The wrappers (1 KB each) are not the problem. Verbatim duplication is small (about 20 KB); the weight is the size of each card and the incident and trial history written into the rules.

Grill: what "simple" means, what leaves the cards, how a card is cut, how the change is proved safe, in how many CRs.

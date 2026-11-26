# Simplify the role cards and the agents' prompts

The owner finds the cards (`skills/chantier/references/*.md`) and the agent prompts very complicated. Intent: specify a plan that makes every role boot on a short, readable card, with each rule in one place and no incident history in the text a role reads, without losing a rule that protects the user (never merge, rebase only, no fallback, the user's boundaries).

Measured first (see `intake/request.md`): the cards total 808 KB; `chief-of-staff.md` is 206 KB, `driver.md` 135 KB, `hosts/claude-code.md` 109 KB, `foreman.md` 85 KB, `concepts.md` 74 KB. The wrappers (1 KB each) are not the problem. Verbatim duplication is small (about 20 KB); the weight is the size of each card and the incident and trial history written into the rules.

Grill: what "simple" means, what leaves the cards, how a card is cut, how the change is proved safe, in how many CRs.

## The owner's framing (2026-11-24, in the grill)

The cards grew from dozens of runs and retros that each added small corrections; they are far too heavy and detailed and cost a lot at every role's start. They should rely on Opus 5.5 and Sonnet 5.5 inferring from a vital minimum. Wanted: a complete rewrite of the card mechanism, the smallest possible cards, no behaviour lost, progressive disclosure to the fullest (the model may stumble on a command and run `--help`; the watcher and server print state lines that remind the model where it stands; the board lets agents message each other and avoids wakes). A total overhaul is accepted if every role's boot gets much lighter; simpler role cards would also let outside people bring their own roles.

Fixed: the roles (not their cards), the working with the server (improvable), the Foreman orchestrating with the tools it is given. The goal is mainly to improve those tools and each role's progressive disclosure.

A Fable study (work/study-fable.md) is commissioned before the grill goes on; the first four questions (measure, history, split, rules in code) were withdrawn by the owner pending that study.

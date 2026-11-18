# Answers

## 2026-11-13: audit cases proposed

The Chief of Staff proposed nine more cases (release delays the pause; `close` refused within 5
minutes of a session write; `order confirm` refused while other CRs are open; `open` refused for a
missing specification; a subagent's Write of some Markdown names refused; an action refused to a
peer session; the round limit; Remote Control limits; no price for a model). The owner has not
picked yet.

## 2026-11-13: case 5, Markdown file names

Owner, 2026-11-13, on case 5: « c'es tpas un probleme du classifier de Claude => oui il faut
utiliser des prefix devant, ca resoud tout. » The refusal of a subagent's Write of some Markdown
file names is not the auto-mode classifier. The rule: every file a subagent writes has a prefix
(a number, as `04-report.md`); that solves it.

## Settled by the Chief of Staff (spec-writer's questions, 2026-11-18, the user asks no questions)
- The code is the target: a running direct batch queues `order add` (CR-171), and the factory mode (CR-370) builds on it. The docs and the SVG are corrected to match, texts and SVG together.
- The table also gets the audit cases (b) `close` refused within 5 minutes of a session write, (c) `order confirm` refused while other CRs are open, (d) `open` refused for a missing specification, (f) the round limit, (h) no price for a model. (a) folds into row B; (e) and (g) stay in the host references.


# Cognitive load budget for role cards and agent texts

Priority P2. To study: a cognitive load budget, checked each time a role card (or another text an
agent reads to do its work) is changed. To grill with the owner after batch-09 of
markdown-okf-schema-studio ends. Filed on 2026-11-26 from that project's Chief of Staff session, on
the owner's word.

The owner, verbatim: "Est-ce que tu crois qu'il serait possible de mettre en place dans le projet
chantier, pour lui, des sortes de vérifications de la charge cognitive à chaque fois qu'on essaye de
changer une carte? En gros, j'aimerais qu'on ait une sorte de budget cognitif, donc ce serait un CR à
étudier en P2 appelé Cognitive Load, par exemple, ou Cognitive Checks, qui permettrait de rajouter
une sorte de budget. Lorsque je veux modifier une carte du Chief of Staff, etc., vérifierait si le
budget cognitif n'est pas dépassé. On a déjà un budget en termes de caractères sur les cartes, et on
voit bien que ça a posé pas mal de problèmes. Mais un budget cognitif, ce serait intéressant à
évaluer. Donc on grillera ça après le batch en cours."

Seen at filing (checkout at 266b784f):

- The size budget today: `skills/chantier/scripts/cli/tests/test_brief_bytes.py` caps the bytes of
  each role's brief (for example chief-of-staff 24 400, foreman 22 200).
- `skills/chantier/references/` holds short role cards (chief-of-staff.md 6 040 bytes) and 296 topic
  files (355 528 bytes in all).
- Dense sentences with several nested conditions exist under that budget, for example the mismatched
  ask rule in `help merge-series-stack` (part 2).

Leads to examine in the grill (proposals of the filing session, nothing decided):

- Deterministic measures run as a test, per role and per moment: rules (must, never, only), conditions
  and exceptions per sentence, sentence length, nested parentheses, topics to follow to act, terms
  used before they are defined, rules stated twice.
- A budget as a ratchet (a change may not raise a figure without the owner's yes), first in report-only
  mode.
- Behaviour as the reference: quiz or scenario compliance before and after a card change (`evals/kit`),
  on demand because of its cost; an LLM judge only as advice.
- Calibration against rule breaks actually reported as anomalies, so that the figures are not met by
  rewriting that helps no reader, as can happen with a byte cap.

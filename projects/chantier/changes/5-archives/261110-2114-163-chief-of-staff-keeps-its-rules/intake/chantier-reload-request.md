# "chantier reload": reload chantier's rules, by hand or after a compaction

## The user's words (2026-11-10, batch-09)

"Ah si je dit « chantier reload » ou « /chantier reload » (en text ou en skill), je veux que ce
soit pour recharger les règles de chantier. Typiquement après un compact. Ou alors tu es capable
de détecter que tu as été compact et recharger par toi même le skill ?"

## What happened

- After a `/compact`, the user ran `/chantier:chantier` with no argument to reload the rules.
- The skill has no "reload" entry point. The Chief of Staff guessed what was meant: it read the
  cards again, did not repeat the introduction, and gave a status.
- After a compaction the session sees the summary marker ("This session is being continued from
  a previous conversation…"). Nothing makes it reload the cards on its own. The summary even
  says to go on directly, so in practice it does not reload.

## The request

1. **A reload entry point.** "chantier reload", in plain text or as `/chantier:chantier reload`,
   means:
   - read the skill and its cards again (and `foreman.md` and the host's reference while steering
     a direct batch);
   - no introduction;
   - nothing touched in the batch;
   - a short line saying the rules are reloaded, then the current status if a batch runs.
2. **A reload after compaction, with no word from the user.** It must not depend on the model
   noticing the compaction.
   - A lead to study: the plugin already ships a hooks module (`hooks/register.tsx`).
   - That module can hook `session.compact` (trigger `manual` or `auto`).
   - It can tell the summarizer to keep "reload chantier's cards", or add the reload after the
     summary.
   - On Copilot, find the host's own way, or document the limit.

## Related

- The P2 CR `chief-of-staff-keeps-its-rules` asks for rules that hold through compaction. This
  item may join it, or come first as its simplest piece: the user decides.

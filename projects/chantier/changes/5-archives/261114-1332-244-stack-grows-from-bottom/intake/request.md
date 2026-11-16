The native stack is made as soon as its bottom CRs are ready and grows on top as each further CR becomes ready, instead of only once every CR of the batch has a PR.

The user (2026-11-14): "je veux la stack complète comme prévue"; asked what the tools lack for a night to end in a stack.

What happened (batch-17): `forge-stack create` refuses while any open CR of the stack has no PR (forge_stack.py `_plan`), and the stack driver's card starts it only when every open CR is ready or blocked. At 07:41 five CRs were ready (221, 237, 232, 233, 234) and no stack could exist, because CR-225 to CR-228 had no PR yet.

Wanted:
- the stack driver makes the native stack as soon as the run of ready CRs from the default branch up is ready;
- each CR that becomes ready later is added on top with `forge-stack rebuild` (it exists for insertions);
- the five checks hold for the stack as it stands, not the whole batch; the stack-ready ask says which CRs are still to come;
- the user may merge the bottom while the top goes on.
Near CR-234 (forge-stack-followups), which touches `rebuild`.
## After the critic's review (Fable, 2026-11-14)

- Name the three places to change: the refusal in `commands/forge_stack.py` (`_plan`, lines 67-73, "no PR recorded"), check 2 of `show` (line 217), and the stack's order: `chain()` sorts by `order` (`commands/facts.py:33-36`), so a "ready run from the bottom" exists only if the lowest-order CRs finish first; under `after`, the order must follow readiness, or one slow CR blocks the stack again.
- Lands after CR-233 (merge-any-time), whose spec keeps "a stack driver takes the stack when its open CRs are all ready or blocked" (lines 88-97): this item amends those paragraphs.
- Goes with start-on-unready-dependency.
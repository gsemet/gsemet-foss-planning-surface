A CR that depends on another starts only once that dependency is ready, and the cards say so.

The user (2026-11-14), on the proposal to start a CR on an unready dependency: "je ne suis pas d'accord, la dépendance est faite pile pour empêcher de commencer avant que l'autre soit prêt". Decision: the rails are right; no CR starts on a dependency that is not ready.

What remains: the card contradicts the rails. `concepts.md` (~line 101) says a stack starts "every CR at once, on the default branch or on its last open dependency", while `rails.py` (lines ~132 and 225-236) refuses a CR until its dependency is ready (in stack and series, `ready` meets it). Rewrite the card's sentence to say what the rails do: in a stack every CR with no open dependency starts at once; one with a dependency starts once that dependency is ready, on its branch. Check foreman.md and driver.md for the same wording.

A cards-only change; small.
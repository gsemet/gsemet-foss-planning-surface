# Conflicts: CR-210 restack onto CR-209 head e28788a

- evals/SCORECARD.md, after J24: the base added J25 (CI claim), the CR added J26 (main checkout fast-forward). Kept both rows, J25 then J26.
- chief-of-staff.md, Foreman-mode differences list: the base added "A note that carries work to a Driver", the CR added "The main checkout after a merge". Kept both bullets.
- concepts.md rule 8: base reworded the wait ("except the one bounded wait before a second CI look"); the CR added the main-checkout sentence (steering session only, `merge --ff-only --no-overwrite-ignore`, only when clean). Kept both.
- foreman.md, merge paragraph: the base rewrote the release PR and fix merge rule (grant, default-branch base); the CR added "then the fast-forward (Your means)" after `order merged`. Kept the base's rule and added the CR's clause.

Fast gate: `just check` passed (58 tests).

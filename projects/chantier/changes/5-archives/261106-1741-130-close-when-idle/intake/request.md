# A batch closes only when nothing runs

The user: "Il faut une CR pour que un batch ne puisse pas se clôturer si une CR ou autre driver
(change, qa, release) est encore actif. Un batch PEU être clos quand tout est fini, sur approbation.
Mais pas possible de clore si un driver ou même un foreman est encore actif. Il faut pouvoir
garantir que les coûts soient pertinents"

Found in the code, at c25a837:

- `commands.py`, `land`: refuses on recorded state only: a `working` CR, a queued one, a ready or
  blocked one, an open order, a stack agent. It runs with no word from the user.
- `commands.py`, `close`: only checks that the batch's folder holds no sub-folder. It looks at no
  CR status, no order and no Foreman.
- `commands.py`, `order` and `_apply_order`: nothing reads the batch's status.
  `chief-of-staff.md`, Starting a batch, says new work joins with `order add` until `close`.
- `commands.py`, `_cost_rows`: the spend stops at `landed`, and `status.py` calls it final there.
- `state.py`: `LIVE` is the recorded `working`; the CLI has no proof that an agent really stopped.

Seen on batch-06: `order add` was accepted 27 s after `land`. CR-129 then ran on a landed batch, and
neither its spend nor the Foreman's after landing is in the $49.38.

To grill: what proves that a Driver or a Foreman is no longer active; whether `order add` on a
landed batch reopens it or is refused; whether the final cost is taken at `land` or at `close`.

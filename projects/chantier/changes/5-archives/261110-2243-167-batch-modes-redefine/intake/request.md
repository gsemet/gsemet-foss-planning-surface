Redefine the batch modes: series, parallel, stack

The user's request (2026-11-10, in French), translated. It came after batch-09 (opened as a
stack) started its three CRs at once, which the user read as "not in series": the user calls it a
specification problem.

- **Series:** the PRs have a precise order, and the Chief of Staff guides the user through the
  merges. They may depend on one another; those not at the bottom must be drafts. On request,
  the Chief of Staff can switch everything to a stack at once.
- **Parallel:** everything happens at the same time and, unless told otherwise, the first to
  arrive wins. Rebase as soon as one is merged.
- **Stack:** parallel, but with a stack driver.
- Show it with an SVG in the README, other than the batch lifecycle one, and clear explanations
  in the README and the docs.
- To be handled later (not grilled now).

Original words:

> Alors c'est un problème de spécification: met en P1 de redéfinir les mode série, parallel,
> stack.
>
> Série: les PR ont un autre precis, et tu guides l'utilisateur pour les merges. Elles peuvent
> dépendre les unes des autres, celles qui ne sont pas tout en bas doivent être en draft. Sur
> demande tu peux tout passer en stack d'un coup.
>
> Parallel: tout se passe en meme temps et said indication inverse c'est le premier arrivé qui
> gagne. Il faut rebase des qu'un est mergé
>
> Stack: parallel Mais avec un stack driver.
>
> Il faut bien montrer ça avec un svg dans le readme, autre que batch lifecycle, et des
> explications claire dans le readme et la doc. On traitera ça plus tard

Context for the grill (the Chief of Staff's notes, not the user's words):

- Today `open` makes a stack by default and `--parallel` independent CRs; there is no series
  mode. The cards say a batch runs its CRs in parallel unless the plan says why not
  (`chief-of-staff.md`, "Backlog and grill"; `foreman.md`).
- Related: `diagrams-modes-griller` (P1) also edits the README and the docs SVGs; the new SVG
  here is a separate one. `docs/batch-pace.svg` exists and may be what this replaces or extends.
- To settle in the grill: "un autre precis" read as "un ordre précis"; "said indication
  inverse" read as "sauf indication inverse"; what "tout passer en stack d'un coup" means for a
  series batch.

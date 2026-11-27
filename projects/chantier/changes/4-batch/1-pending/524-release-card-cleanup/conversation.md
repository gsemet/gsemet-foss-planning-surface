# Excerpts of the conversation with the Chief of Staff, batch-32

The owner's lines are verbatim, in French, as typed. The Chief of Staff's lines are short summaries,
marked as such, not quotes. The release Driver anonymises any capture it renders from this file
(`docs/release-process.md`).

## The cleanup

**Owner:** « c'est quoi ces 240 sujets ? je nme comprend pas, un model comme toi peut deja faire
tout seul plein de chose. poourquoi sur compliquer? il faut garder en instruction les elements les
plus important, deplacer en CLI tout ce qui est mecanique et qui n a pas besoin de garder dans le
context. Il faut faire un grand menage. Lance une revue Fable qui determinera un plan. Objectif:
des cartes claires, efficace, des tools dans des CLI organisé logiquement, exploitant au maximum le
progressive disclousre du modele. »

*Chief of Staff (summary):* a review produced a plan; its five decisions were asked one at a time.
The owner chose steps 1 to 3 now, with a new version; steps 4 to 7 wait.

## The batch

**Owner:** « ouvre un batch et lance ces 7 CR »

**Owner:** « fait un batch stack et rajoute la CR du TUI qui elargie les colonnes je ne sais pas
ou elle est »

## The live view

**Owner:** « tu peux prendre l une ou l autre des bordure existante. Attention pour le
redimensionnement dynamique c est sur les colonne principale PAS dans la colonne centrale »

## The go

*Chief of Staff (summary):* the plan of ten change requests, with their waits, the card count before
and after the batch, and the choices made for the owner.

**Owner:** « A. Ajouter et démarrer (recommandé) »

*Chief of Staff (summary):* ten change requests joined batch-32; the Foreman started the first two,
the inventory's last reading and the wider columns of `live`.

## Drivers handing over

**Owner:** « c'est quoi cette histoire ? je croyais avoir fixer ca avec autocompact ? »

*Chief of Staff (summary):* a Driver's card makes it hand over before the host compacts it; the
request to change that limit is still in the backlog.

## First pull request

*Chief of Staff (summary):* the wider columns of `live` are the first change request ready to merge.

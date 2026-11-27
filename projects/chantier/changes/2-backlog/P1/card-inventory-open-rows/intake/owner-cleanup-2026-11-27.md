## The owner's words (2026-11-27), verbatim, to the Chief of Staff

1. « je reste surpris par le nombre de carte. ca fait bcp 330 »
2. « non je veux supprimer ce qui sert a rien. le but du rework etait de deplacer des instructions dans des tools CLI »
3. « c'est quoi ces 240 sujets ? je nme comprend pas, un model comme toi peut deja faire tout seul plein de chose. poourquoi sur compliquer? il faut garder en instruction les elements les plus important, deplacer en CLI tout ce qui est mecanique et qui n a pas besoin de garder dans le context. Il faut faire un grand menage. Lance une revue Fable qui determinera un plan.

   Objectif: des cartes claires, efficace, des tools dans des CLI organisé logiquement, exploitant au maximum le progressive disclousre du modele. »

4. Added later the same day, while the review ran: « deja tous ces cartes p1 p2 ... c'est beaucoup trop. il faut mettre dans une carte un theme. et surtout avec un nombre de carte important il faut orgnaiser le progressive disclosure efficacement, retirer tout ce qui pourra etre inferer directement par le modele, par exemple par le retour de la CLI. »

5. Added next: « aussi, les cartes sous C:\Users\gaeta\Projets\chantier\skills\chantier\references\topics doivent etre agnostique du harnais (claude code ou copilot,..) sauf situation exceptionnelle. Pareil pour la forge, on sait que c est sur git, ca peut etre git ou gitlab, certain concept ont des noms differents (MR, PR, utilise PR les modeles savent faire l adaptation). certains concepts peuvent ne pas etre utilisable directement. il faut que les cartes soient assez abstraite pour laisser le modele fait l adaptation tout seul, et fournir des CLI intelligement construit pour ne pas surcharger la charge cognitive dans le contexte. »

## What is asked

A big cleanup, planned by a review run on Fable:

- keep as instructions only the most important elements; the model already does much on its own;
- move into the CLI everything mechanical that need not stay in the context;
- delete what serves nothing;
- one page per theme, with no `-p1`, `-p2` parts;
- organise progressive disclosure efficiently, as the number of pages is large;
- remove everything the model can infer by itself, for example from what the CLI returns;
- topic cards agnostic of the host (Claude Code, Copilot), save exceptions;
- the same for the forge, with one word, PR, the model adapting it; a concept a forge cannot use directly is still written abstractly;
- cards abstract enough for the model to adapt by itself, and CLIs built so that they add little to its context.

Goal: clear and effective cards, tools in logically organised CLIs, making the most of the model's progressive disclosure.

The review's plan: `work/fable-review-plan.md`. It is a proposal: nothing is deleted or started without the owner's word.

## Measured by the Chief of Staff on main at 4d12a5b (2026-11-27)

- `skills/chantier/references`: 330 files, about 613 KB: 296 topic pages (353 KB) for 240 topics in `topics.json`, 29 files at the root (187 KB), 3 host files and 2 forge files.
- 105 topic pages are `-pN` parts of 50 subjects; `help` prints a topic's parts one after the other. A per-page byte budget of the rewrite's specifications made a long text split (`507-sc21-cards-foreman`, "at most 1,500 bytes").
- `help --for`: 183 of the 240 topics list the Chief of Staff, 74 the Foreman.
- Text search for what points at each topic: 8 named by the CLI's source, 107 only by a card or skill, 93 only by another topic, 32 by nothing found (a search, so a reference may be missed; "not named" does not mean useless).

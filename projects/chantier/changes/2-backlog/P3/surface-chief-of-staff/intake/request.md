# A surface-level Chief of Staff orchestrates per-project orchestrators

The user's idea (2026-11-21), to study, no CR to build yet: "Et si le chief of staff était au niveau de la surface (donc multi projet) et le foreman au niveau du projet, que gagnerait on que perdrait ton."

The user's answer after the Fable study (2026-11-21): "Je suis d'accord sur le risque de saturation. Mais je pense qu'il faut faire une session par grill c'est plus facile pour moi. Donc le chief of staff ne ferait que l'orchestration des orchestrateur de projets. Garde cette idée de côtée en P3 pour l'instant ne perd pas d'info". Read: one session per grill; the surface-level Chief of Staff only orchestrates the projects' orchestrators. Parked in P3, nothing lost.

## The Fable study, as given to the user (French)

# Chief of Staff au niveau de la surface, Foreman au niveau du projet : étude Fable (2026-11-21)

Étude en lecture seule. Rien n'a été mesuré : les tailles et les coûts sont des estimations tirées des cartes et du code.

## Recommandation
Ne pas faire tout de suite un Chief of Staff (CoS) unique pour toute la surface. D'abord la **variante B** : garder un CoS par projet, et ajouter une vue et un réveil communs à tous les projets. Mesurer, puis décider d'un « CoS de surface léger » (**variante A**). Le CoS unique complet ne paie que si les projets sont nombreux mais calmes, si tu pilotes surtout depuis le téléphone, et si le contexte tient sans compactions fréquentes. Avec deux projets actifs en parallèle (chantier et Studio), séparer les projets vaut plus que la session économisée.

## Ce que tu gagnerais
- Un seul endroit où parler, au lieu d'une session par projet (la surface en compte 4).
- Des priorités arbitrées entre projets, ce que personne ne fait aujourd'hui.
- Une seule session à ouvrir sur le téléphone.
- Les accords pour le board et le watcher, demandés une seule fois.
- Un peu moins de coût fixe : un seul jeu de cartes chargé (gain modeste).

## Ce que tu perdrais
- **Contexte et compactions, le risque principal.** Une seule session CoS a déjà connu 50 compactions en 45 h. Avec N projets, il y aurait N backlogs, N grills et N flux d'événements dans la même fenêtre, et un risque de mélanger les projets après un résumé.
- **Coût par tour.** Un événement du projet A paie aussi le contexte du projet B.
- **Un projet bloque les autres.** Un grill long occupe la seule session. Sous Remote Control, le mode par défaut est direct : il faudrait imposer le mode Foreman.
- **Règles par projet.** Le CoS devrait tenir N `AGENTS.md` (langue, release, permissions) sans les croiser.
- **Siège et watcher, aujourd'hui par projet.** Il faudrait N sièges et N watchers dans une seule session, et un nouveau cas à définir pour passer un seul projet à une autre session.

## Ce qu'il faudrait changer
| Zone | Taille |
|---|---|
| Les cartes du CoS (« ton projet » partout, projet courant explicite, rechargement après compaction) | Grand |
| La carte du Foreman | Petit |
| Le siège, `status` et `watch` dans le CLI | Moyen |
| Le board (l'accueil de surface existe déjà) | Petit |
| Docs, schémas, scénario, evals | Moyen |

Ce qui ne bouge pas : le Foreman, les Drivers, les workers, les dossiers de planning, les journaux, le serveur, le hub et le writer.

## Variantes
- **A. CoS de surface léger** : il trie entre les projets et fait les rapports ; le grill et le go restent dans un CoS ou un Griller par projet.
- **B. Le modèle actuel, plus une vue** : un `status` de surface et un réveil « le projet X t'attend ». Taille petite à moyenne, sans risque pour la séparation des projets.
- **C. CoS unique, Foreman obligatoire** : l'idée étudiée telle quelle ; c'est le grand chantier.

## À mesurer d'abord, sur une semaine
1. Le nombre de sessions CoS ouvertes par jour, et combien de fois tu changes de session pour une simple question de priorité.
2. Les tokens par tour et les compactions d'un CoS, multipliés par le nombre de projets.
3. Un essai d'un jour sans batch : une session qui tient deux projets.
4. Sous Remote Control : est-ce qu'un Foreman se démarre bien pour un autre projet ?

Si le point 1 est faible, B suffit. Si les points 2 et 3 tiennent sans mélange, A devient raisonnable, et C seulement après.

# CR board mod

rajoute un mod dans chantier si possible déclanché quand `/chantier` est apprlé pour démarer un chantier sur un projet.

**But :** voir l'état des change requests sans quitter la conversation, dans un panneau à côté du chat.

**Comportement**
- `/chantier` ouvre le panneau « CR board », et le ferme s'il est déjà ouvert.
- Le panneau affiche les CR connues  : actives, backlog, landed, trashed

* utilise les json

- Il se met à jour tout seul quand le fichier change.
- Les liens relatifs deviennent cliquables : spec, `STATE.md`, rapports./ ...
- Depuis un worktree, il retrouve le fichier dans le checkout principal.
- S'il n'y a pas de fichier, il l'indique en une ligne.

**Limites**
- Lecture seule : il affiche l'état et ne pilote rien.
- Il ne génère pas le tableau, c'est le rôle de `just orchestrator`.
- La vérification ne tourne que panneau ouvert, toutes les 15 secondes, et le fichier n'est relu que s'il a changé.

Grill moi beaucoup sur le design de ce mod pour donner une "visualisation" intégrée a Claude cod quand on utilise chantier

Regarde le board que j'avais fait sur le predecesseur de chantier. il faut que tu fasse mieux !

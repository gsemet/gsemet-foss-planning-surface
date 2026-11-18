# Switch a batch from Foreman mode to direct mode, even with CRs in flight

The user's request (2026-11-18), as given:

Projet chantier (C:\Users\gaeta\Projets\chantier). Ajoute la bascule d'un batch du mode Foreman au mode direct, même quand des CR sont en cours. Une PR, en brouillon jusqu'à ce que la CI soit verte ; je fusionne moi-même par rebase.

Pourquoi : aujourd'hui un batch ouvert avec un Foreman ne peut jamais passer en direct (skills/chantier/references/chief-of-staff.md, « A batch keeps the steering it was opened with... a Foreman batch never becomes direct », vers la ligne 777, et la fin de « Switching to Foreman mode », vers la ligne 1564). Cas réel : le Foreman du batch-06 de Studio s'est arrêté (limite d'usage atteinte, battement de cœur vieux de 9 h) avec 5 CR en cours et 4 PR ouvertes. Le Chief of Staff ne peut ni reprendre la main en direct, ni clôturer sans abandonner tout le travail.

Ce qui est voulu, sur le modèle de « Switching to Foreman mode » (le sens inverse, qui existe déjà) :

1. Déclencheur : la parole de l'utilisateur seulement (« passe le batch en direct »), sur un batch en cours ou en pause, Foreman vivant ou non.
2. Arrêt de l'ancien pilote :
   - Foreman vivant : le Chief of Staff lui envoie un ordre de passation. Le Foreman ne lance plus de Driver, arrête chacun de ses Drivers en cours (arrêt de l'hôte), après un `$CHANTIER note <cr> "switch to direct mode: Driver stopped; the Chief of Staff restarts it"`, puis répond qu'il a fini et s'arrête.
   - Foreman qui ne répond pas (prouvé par `foreman get` + un ping sans réponse, ou la parole de l'utilisateur) : le Chief of Staff demande à l'utilisateur d'arrêter la session du Foreman (ou l'arrête lui-même avec son accord), et traite ses Drivers comme « stoppés de l'extérieur ».
   - Dans les deux cas, jamais deux Drivers sur une même CR : aucun Driver n'est relancé tant que l'ancien n'est pas arrêté.
3. Prise de la main : le Chief of Staff réclame l'époque suivante (`foreman set <son id> --epoch <n+1>`, `foreman transcript`), et le CLI passe `steering` du batch de `foreman` à `direct`. Il faut une commande pour ça (par exemple `order steering direct --epoch <n+1>` ou une option de `foreman set`), qui l'enregistre dans le record du batch et dans son journal. L'ancienne époque devient périmée (exit 3).
4. Reprise : chaque CR en cours est relancée par le chemin de redémarrage existant (`agents set <cr> - --epoch <n>`, `handoff`, `take <cr> --note "resume: switch to direct mode" --epoch <n>`, nouveau Driver, `agents set <cr> <id> --epoch <n>`). Les CR en file restent en file. Les PR, branches et worktrees existants sont gardés.
5. Coût et clôture : les appels de l'ancien Foreman et de ses Drivers restent comptés (Foreman remplacé = jamais bloquant à `close`, comme aujourd'hui) ; `cost`, `status` et le board affichent bien « direct » après la bascule.

À mettre à jour :
- chief-of-staff.md : la règle ligne ~777, une section « Switching to direct mode » à côté de « Switching to Foreman mode », la ligne du tableau « Entry points » si besoin ;
- foreman.md : ce que fait le Foreman quand il reçoit l'ordre de passation ;
- routing.md si un nouveau message est ajouté ;
- le CLI (commands/orders.py, seat.py ou foreman, opening_record / record du batch) et ses tests ;
- le board et `status` si l'affichage du pilote en dépend ;
- le changelog / les notes de version selon les règles du dépôt.

Règles : celles du dépôt chantier (AGENTS.md, guide de commit, modèle de PR), tests et checks verts avant de dire que c'est fini.

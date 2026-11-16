# Interview: improve skill boot

Short name: `improve-skill-boot`

Date: 2026-11-16.

This record preserves every numbered question, its choices and recommendation,
and the user's answer. Questions are reproduced in French; explanatory context
is summarized in English. Later answers take precedence where noted.

## Round 1: destination and startup contract

### Q1: Où conserver cette demande et les réponses de l'entretien ?

Context: the requested directory was absent and was in the code repository,
whereas the current session used an external planning surface.

- A. Dans le chemin exact demandé (recommended).
- B. Dans la surface de planification.

Recommendation: A, respect the explicitly requested destination.

Answer:
> A. Dans le chemin exact demandé (recommandé)

### Q2: Quels points d'entrée doit couvrir cette amélioration ?

Context: distinguish the observed Copilot case from a cross-host or cross-role
startup contract.

- A. Le Chief of Staff sur tous les hôtes (recommended).
- B. Le Chief of Staff sous Copilot SDK uniquement.
- C. Tous les rôles et tous les hôtes.

Recommendation: A, address the affected entry point without expanding to every
role.

Answer:
> C. Tous les rôles et tous les hôtes

### Q3: Quelle stratégie de lecture souhaites-tu au démarrage ?

Context: loading full references consumed context before there was work to do;
essential rules must nevertheless remain available.

- A. Un socle court obligatoire, puis des références à la demande (recommended).
- B. Tout lire, mais mieux découper.
- C. Deux niveaux au choix de l'utilisateur.

Recommendation: A, reduce required material rather than just improving transport.

Answer:
> A. Un socle court obligatoire, puis des références à la demande (recommandé)

### Q4: Le démarrage doit-il conserver ses effets automatiques actuels ?

Context: taking the seat, launching the board and joining autosync are actions,
not merely checks.

- A. Oui, conserver ces actions et mieux qualifier leurs résultats (recommended).
- B. Vérifier seulement, puis demander avant toute activation.
- C. Prendre le siège et rejoindre l'autosync, mais lancer le board sur demande.

Recommendation: A, preserve behavior while improving evidence reporting.

Answer:
> B. Vérifier seulement, puis demander avant toute activation

Resolution: this broad rule was refined by Q17 and superseded where applicable
by Q19, Q20, Q21 and Q23. Do not retain a blanket confirmation requirement.

## Round 2: permissions, references and host evidence

### Q5: Qui doit demander l'autorisation d'activer les services ?

Context: avoid making subordinate agents repeat permissions already granted to
their parent.

- A. La session interactive demande un accord groupé ; les agents héritent des
  autorisations nécessaires (recommended).
- B. Chaque session demande son propre accord groupé.
- C. Chaque activation exige un accord distinct.

Recommendation: A, keep effects explicit without interrupting every agent.
Inheritance does not grant extra merge or publication permissions.

Answer:
> A. La session interactive demande un accord groupé ; les agents héritent des autorisations nécessaires (recommandé)

Resolution: permission inheritance remains bounded by role. Q17 and subsequent
answers distinguish mandatory CLI preparation, seat acquisition, board launch
and autosync instead of treating them as one uniform activation bundle.

### Q6: Comment garantir que les lectures différées ne soient pas oubliées ?

Context: a short startup needs reliable reference loading before later actions.

- A. Une table "action -> lectures obligatoires" (recommended).
- B. Le jugement de l'agent suffit.
- C. Une vérification par la CLI.

Recommendation: A, an explicit contract without equating a reading declaration
with comprehension.

Answer:
> A. Une table “action → lectures obligatoires” (recommandé)

An indispensable inaccessible reference blocks the action that requires it.

### Q7: Comment départager les règles génériques et les capacités réelles de l'hôte ?

Context: tool availability, documented behavior and tested workflows are different
levels of evidence, particularly for Foreman versus direct mode.

- A. Un contrat commun, avec une fiche de capacités et de preuves par hôte
  (recommended).
- B. Des procédures de démarrage entièrement séparées par hôte.
- C. Un mode conservateur tant que le parcours n'est pas éprouvé.

Recommendation: A, reduce contradictions without overstating tool availability.

Answer:
> A. Un contrat commun, avec une fiche de capacités et de preuves par hôte (recommandé)

### Q8: Veux-tu arrêter l'entretien ici ?

Recommendation: no; success criteria, blocking errors and reporting were open.

Answer:
> non

## Round 3: blocking behavior, measurement and reporting

### Q9: Une vérification en échec doit-elle bloquer toute la session ou seulement les actions concernées ?

Context: failed GitHub authentication need not prevent backlog discussion,
whereas unresolved location or seat ownership may prevent planning writes.

- A. Bloquer uniquement les actions concernées, en les nommant (recommended).
- B. Tout bloquer au premier échec.
- C. Traiter les échecs comme des avertissements jusqu'à l'action.

Recommendation: A; distinguish failed, unavailable and unperformed checks.

Answer:
> A. Bloquer uniquement les actions concernées, en les nommant (recommandé)

Resolution: CLI failure is the explicit startup-blocking exception confirmed
in Q17, Q19 and Q23.

### Q10: Quel critère d'allègement souhaites-tu imposer au socle obligatoire ?

Context: token counts depend on the model and existing context; mandatory
documentation volume is more reproducible. Project rules remain applicable.

- A. Un plafond de 12 Kio de documentation Chantier par rôle au démarrage
  (recommended).
- B. Une réduction d'au moins 50 % par rapport à une mesure de référence.
- C. Aucun seuil chiffré.

Recommendation: A, a measurable target rather than an already demonstrated
performance claim.

Answer:
> A. Un plafond de 12 Kio de documentation Chantier par rôle au démarrage (recommandé)

The scope includes common and host references, and excludes project rules and
check output.

### Q11: Quel compte rendu veux-tu à la fin de l'initialisation ?

Context: separate product introduction from operational state and evidence.

- A. Un bilan court, avec introduction détaillée sur demande (recommended).
- B. Conserver l'introduction complète au premier démarrage.
- C. N'afficher que les anomalies et les demandes d'autorisation.

Recommendation: A, show verified state, pending permissions and untested claims;
do not improvise remaining-capacity estimates.

Answer:
> A. Un bilan court, avec introduction détaillée sur demande (recommandé)

### Q12: Veux-tu arrêter l'entretien ici ?

Recommendation: no; permission handling across reloads and role changes remained.

Answer:
> non

## Round 4: permission lifetime and side effects

### Q13: Combien de temps un accord d'activation reste-t-il valable ?

Context: reloading a skill should not restart services or repeat permissions,
but an old grant must not silently cover a different project or wider scope.

- A. Pour cette session, ce projet et les activations explicitement autorisées
  (recommended).
- B. Pour une seule invocation du skill.
- C. Persistant entre les sessions du projet.

Recommendation: A; permissions are withdrawable, and withdrawal does not
automatically stop another session's shared service.

Answer:
> A. Pour cette session, ce projet et les activations explicitement autorisées (recommandé)

### Q14: L'accord groupé doit-il permettre d'accepter seulement certaines activations ?

Context: allow the seat and autosync while refusing the board, without ambiguous
dependencies or repeated prompts.

- A. Oui, chaque activation reste sélectionnable dans une seule demande
  (recommended).
- B. Non, le groupe est indivisible.
- C. Oui, puis redemander séparément les activations refusées lorsqu'elles
  deviennent utiles.

Recommendation: A; disclose dependencies and do not work around refusals.

Answer:
> quelles activations parlent on? donne des exampels

Resolution: unanswered at this point; examples were supplied before Q17.

### Q15: Les vérifications avant accord doivent-elles être strictement sans effet de bord ?

Context: a command called a check may still create state, install dependencies
or indirectly activate a service.

- A. Oui, aucune écriture ni installation avant accord (recommended).
- B. Autoriser les caches et installations locales, mais aucune écriture dans
  les dépôts ni activation de service.
- C. Autoriser les fichiers techniques ignorés par Git.

Recommendation: A, judge actual effects rather than command names.

Answer:
> A. Oui, aucune écriture ni installation avant accord (recommandé)

Resolution: Q19 explicitly permits automatic official CLI preparation as an
exception. Q20 permits taking a free seat after explicit CoS invocation.
Ordinary checks remain read-only.

### Q16: Veux-tu arrêter l'entretien ici ?

Recommendation: yes, proceed to a summary if the choices were settled.

Answer:
> non

## Round 5: concrete activation examples

The clarification distinguished:

- Seat acquisition: writing state naming the project's CoS.
- Board launch: a persistent server, an open port and possible LAN exposure;
  the current board also joins autosync.
- Autosync participation: a persistent participant in a group that may commit
  and push surface changes while enabled.
- CLI preparation: dependency installation and cache creation when needed.
- Ordinary rule, seat and capability reads: not activations.

The startup grant does not replace the user's batch go or release/merge
permissions. Hidden dependencies must be disclosed.

### Q17: Pour ces actions de démarrage, veux-tu pouvoir donner un accord partiel ?

- A. Oui, un formulaire avec des actions sélectionnables et leurs dépendances
  (recommended).
- B. Non, un accord pour l'ensemble présenté.
- C. Une confirmation séparée par action.

Recommendation: A, precise consent without multiple interruptions.

Answer:
> Le CLI est obligatoire, il faut fail s'il ne marche pas. l'autosync doit etre une option opt-in. La prise du siege Chief of Staff est en effet une question a poser si ce n'est pas clair, si une autre session est active dessus. Lancer le board oui c'est une demande a faire.

Resolution: replace the undifferentiated activation model with separate rules
for CLI, seat, board and autosync.

### Q18: Veux-tu arrêter l'entretien ici ?

Recommendation: yes, if the clarification resolved the remaining point.

Answer:
> non

## Round 6: CLI preparation, seat acquisition and board independence

### Q19: Si la CLI nécessite une installation ou une réparation, que doit faire le démarrage ?

Context: a mandatory CLI does not by itself establish permission to install it.

- A. Échouer avec le diagnostic, sans installer ni réparer (recommended).
- B. Demander l'autorisation de la préparer.
- C. Autoriser sa préparation automatique.

Recommendation: A, follow the explicit-failure requirement without implicit
repair.

Answer:
> C. Autoriser sa préparation automatique

Resolution: explicit exception to Q15, bounded by Q23.

### Q20: Un siège libre doit-il être pris automatiquement après une invocation explicite du Chief of Staff ?

Context: distinguish an unoccupied seat from another occupant whose liveness
the host cannot establish.

- A. Oui si le siège est libre ou déjà à cette session ; demander sinon
  (recommended).
- B. Toujours demander avant de prendre un siège libre.
- C. Prendre aussi le siège d'une session prouvée arrêtée.

Recommendation: A, no redundant question and no silent replacement.

Answer:
> A. Oui si le siège est libre ou déjà à cette session ; demander sinon (recommandé)

### Q21: Le board doit-il pouvoir fonctionner sans rejoindre l'autosync ?

Context: board startup currently can join autosync, which conflicts with
independent autosync opt-in.

- A. Oui, board et autosync indépendants (recommended).
- B. Non, proposer le board avec autosync comme un ensemble explicitement accepté.

Recommendation: A; neither session nor board joins implicitly, and other
participants are not stopped.

Answer:
> A. Oui, board et autosync indépendants (recommandé)

### Q22: Veux-tu arrêter l'entretien ici ?

Recommendation: no, check the consistency of the revised choices.

Answer:
> non

## Round 7: preparation limits and manual synchronization

### Q23: Jusqu'où va la préparation automatique de la CLI ?

Context: preparation must not silently replace the selected source or version.

- A. Uniquement la procédure officielle de la version et de la source
  sélectionnées (recommended).
- B. Autoriser aussi des tentatives de réparation.
- C. Autoriser une mise à jour automatique de Chantier.

Recommendation: A; prepare required dependencies by the official procedure,
then fail explicitly without substitution or improvised repair.

Answer:
> A. Uniquement la procédure officielle de la version et de la source sélectionnées (recommandé)

### Q24: Sans opt-in à l'autosync, l'agent peut-il synchroniser manuellement la surface à sa place ?

Context: clarify whether opt-in governs the persistent participant or all
surface synchronization. Git operations for an authorized code batch are
separate.

- A. Non, aucune synchronisation de remplacement automatique (recommended).
- B. Oui, suivre les règles existantes de synchronisation manuelle.
- C. Demander au cas par cas avant chaque synchronisation manuelle.

Recommendation: A, avoid substituting manual synchronization for a refused
participant.

Answer:
> B. Oui, suivre les règles existantes de synchronisation manuelle

Resolution: the user deliberately limited opt-in to persistent autosync
participation. Existing project rules govern manual surface synchronization;
do not replace this answer with the interviewer's recommendation.

### Q25: Veux-tu arrêter l'entretien ici ?

Recommendation: yes, present the summary and persistence choices.

Answer:
> oui

## Summary and persistence handoff

The summary presented the final decisions and explicitly identified the
superseded blanket activation rule. No unresolved decision was identified.
Performance and host capabilities remain to be demonstrated, not assumed.

### Q26: Quelle suite souhaites-tu pour cette synthèse ?

- A. Sauvegarder l'entretien complet et la proposition dans le dossier demandé
  (recommended).
- B. Sauvegarder uniquement un document de synthèse dans ce dossier.
- C. Garder uniquement la synthèse dans cette conversation.
- D. Sauvegarder la spécification puis engager le workflow d'implémentation.

Recommendation: A, matching the original request without implementing.

Answer:
> A. Sauvegarder l'entretien complet et la proposition dans le dossier demandé (recommandé)

This authorizes interview/proposal persistence only, not implementation.

## Subsequent lifecycle decisions

- 2026-11-16: the user selected P1: "je l'ai mis en P1".
- 2026-11-16: the user requested realization from the external surface:
  "chantier reload. faisons la CR improve-skill-boot en mode directe."
  This supersedes the earlier persistence-only authorization, not the
  functional interview decisions.
- 2026-11-16: after restoring GitHub access, the user requested continuation:
  "reprennons le CR demandé".
- 2026-11-16: the user confirmed the existing specification should be reused:
  "tu refais la spec ? Elle n'est pas deja dans
  /Users/az02065/Projects/DevTools/gsemet-foss-planning-surface/projects/chantier/changes/2-backlog/P1/improve-skill-boot/03-specification.md ?"
- 2026-11-16: the user authorized naming alignment:
  "ah tu peux realigner les noms dans les CR importés".

The original Q1 through Q26 above remain authoritative, including their explicit
supersession notes. Any new interview question continues at
improve-skill-boot-Q27. Autosync remains stopped.

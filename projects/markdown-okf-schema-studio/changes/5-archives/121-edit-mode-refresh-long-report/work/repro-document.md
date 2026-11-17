# Coût en tokens du pattern orchestrateur, driver et sous-agents : analyse de la semaine

Analyse du 2026-10-26, sur toutes les sessions Claude Code actives du 19 au 26 octobre 2026.
Elle remplace la version courte écrite plus tôt, dont plusieurs estimations se révèlent fausses
une fois mesurées (voir la section « Ce que les mesures corrigent »).

## 1. Résumé

- **Coût total de la semaine au tarif API : 1 374 $,** pour 668 agents, dont 657 sous-agents.
- **Pas de tokens d'entrée hors cache :** 100 % de l'entrée passe par le cache de prompts. Le coût
  se répartit ainsi : lectures du cache 49 %, écritures du cache 35 % (29 % à 5 minutes, 6 % à
  1 heure), sortie 16 %.
- **Trois postes expliquent l'essentiel du gaspillage mesurable :**
  1. **Les reconstructions complètes du cache après une attente de plus de 5 minutes : 234 $
     (17 %).** Ce sont surtout l'orchestrateur, le driver et le coder qui attendent la CI, un test
     long ou un sous-agent. Pour l'orchestrateur de la nuit, c'est 62 % de son coût propre.
  2. **Les contextes longs relus à chaque tour.** Les tours faits à plus de 200 k tokens de contexte
     coûtent 546 $ (40 %). L'orchestrateur de la nuit a tourné avec 263 k tokens de contexte moyen
     pendant 285 tours.
  3. **Les fichiers lus par le shell (`cat`, `sed -n`, `grep`) dans les sous-agents,** puis traînés
     dans le contexte jusqu'à la fin : environ 180 $ de lectures du cache (± 15 %).
- **Le pattern orchestrateur → coder → relecteur coûte, à taille égale, autant que le pattern
  driver par CR :** environ 1,0 $ par 100 lignes modifiées dans les deux cas, en médiane, hors
  orchestration. La différence se joue dans le **surcoût d'orchestration**, qui va de 2 % à 32 %
  du sous-arbre selon la façon dont l'orchestrateur attend.

**Recommandation :** garder l'orchestrateur LLM, mais le faire tourner « court et réactif » :
- peu de tours ;
- un contexte borné, avec une relève dès qu'il dépasse 100 k tokens ;
- aucune attente faite par le LLM : un script attend, puis l'agent repart d'un résumé ;
- des sorties d'outils résumées par script.

Gain estimé, à qualité égale : **30 à 40 % du coût total.** Le détail est au § 6, et chaque
chiffre y est relié à une mesure.

## 2. Méthode

**La source :** toutes les transcriptions `~/.claude/projects/**/*.jsonl` (sessions principales et
sous-agents), filtrées sur les messages horodatés entre le 2026-10-19 et le 2026-10-26 inclus.
Il y a 870 fichiers, dont 668 actifs dans la fenêtre. Les fichiers `.meta.json` donnent pour
chaque sous-agent sa description, son modèle, son parent et sa profondeur.

**Le comptage :**
- les messages assistant sont dédupliqués par `message.id` (un message est écrit en plusieurs
  lignes quand il est streamé) ;
- pour chaque message, on garde `input_tokens`, `cache_read_input_tokens`,
  `cache_creation.ephemeral_5m/1h_input_tokens` et `output_tokens` ;
- les messages `<synthetic>` sont exclus.

**Le prix :** tarifs Anthropic première partie en $/MTok, pris dans la référence de l'API.

| Modèle | Entrée | Écriture 5 min (1,25×) | Écriture 1 h (2×) | Lecture du cache | Sortie |
|---|---|---|---|---|---|
| Opus 5.5 | 4,00 | 5,00 | 8,00 | 0,20 | 20,00 |
| Sonnet 5.5 | 2,00 | 2,50 | 4,00 | 0,20 | 10,00 |
| Haiku 5.5 | 0,10 | 0,125 | 0,20 | 0,01 | 0,50 |

Le coût est calculé au tarif API, même si ces sessions passaient par un abonnement : c'est la
question posée.

**La classification :**
- **Le rôle** vient de la description du sous-agent (orchestrateur, driver, coder ou rédacteur,
  relecteur ou critique ou audit, analyste ou inventaire, autre), plus la session principale.
- **Le chantier** vient de la description du sous-agent et de celle de ses ancêtres.
- **Le coût par CR** groupe les agents dont la description contient « CR NNN ». Il est rapproché de
  la PR GitHub (lignes ajoutées et supprimées) par le nom de branche, ou par le `report.md`
  archivé pour les anciennes CR.

**L'attribution du contexte :** chaque résultat d'outil de `n` tokens reçu au tour `i` d'un agent
de `N` tours est relu `N − i` fois.
- La taille en tokens est estimée à 3,2 caractères par token. Une image compte pour 1 600 tokens.
- Ce modèle explique **86 %** des lectures de cache mesurées pour les sous-agents (496 $ estimés
  pour 576 $ mesurés). Les parts sont donc fiables à ± 15 % près ; les montants en dollars sont
  remis à l'échelle sur la mesure.
- Il ne s'applique pas à la session principale, car les compactions y remettent le contexte à zéro.

**Les reconstructions du cache :** on compte les tours, hors premier tour, où l'écriture dépasse
60 % du contexte (avec un contexte de plus de 20 k tokens). C'est une signature claire d'un cache
expiré. Elles sont croisées avec le délai écoulé depuis le tour précédent.

**Les limites :**
- La classification par description est heuristique : environ 2 % du coût reste en « autre ».
- La taille des PR mesure mal la difficulté. Une CR de test en vraie fenêtre ou de cause racine
  coûte plus cher par ligne.
- Les sessions d'autres machines ne sont pas comptées.

## 3. Où va l'argent

### 3.1 Par rôle

| Rôle | Agents | Coût | Part | Tours | Lectures du cache | Écritures 5 min | Écritures 1 h | Sortie |
|---|---|---|---|---|---|---|---|---|
| Coder / rédacteur | 236 | 564,9 $ | 41,1 % | 11 559 | 1 474 M | 55,7 M | 0 | 6,31 M |
| Session principale (humain) | 11 | 218,2 $ | 15,9 % | 2 703 | 475 M | 0 | 10,6 M | 1,93 M |
| Relecteur / critique / audit | 248 | 212,1 $ | 15,4 % | 5 050 | 522 M | 23,9 M | 0 | 3,12 M |
| Analyste / inventaire | 44 | 185,2 $ | 13,5 % | 2 706 | 539 M | 18,5 M | 0 | 2,88 M |
| Orchestrateur | 24 | 99,6 $ | 7,2 % | 1 027 | 188 M | 21,0 M | 0 | 0,70 M |
| Driver | 50 | 67,5 $ | 4,9 % | 1 555 | 99 M | 10,6 M | 0 | 0,36 M |
| Autre | 55 | 25,7 $ | 1,9 % | 797 | 56 M | 3,4 M | 0 | 0,42 M |

Les sous-agents Opus représentent **369 $ (27 %),** pour 109 agents. Ce sont surtout les coders de la
période « driver par CR » (CR 041 à 051, étapes S de la CR 056) et le driver de la CR 056.

### 3.2 Par chantier

| Chantier | Coût | Agents |
|---|---|---|
| Base de requirements (CR 059 et 060 : rédacteurs, analystes, critiques, réduction) | 665,8 $ (48 %) | 363 |
| Pipeline de CR, du backlog à la PR (piles de nuit, CR 023 à 104) | 248,3 $ (18 %) | 197 |
| Session principale | 218,2 $ (16 %) | 11 |
| Refactor CR 056, étapes S1 à S8 (driver Opus) | 152,3 $ (11 %) | 27 |
| Plan de corrections deep-UX (T#, P#) | 67,2 $ (5 %) | 48 |
| Divers | ≈ 22 $ (2 %) | 22 |

### 3.3 Par poste de facturation

| Poste | Coût | Part |
|---|---|---|
| Lectures du cache | 671 $ | 49 % |
| Écritures du cache à 5 min | 402 $ | 29 % |
| Écritures du cache à 1 h (session principale) | 85 $ | 6 % |
| Sortie | 216 $ | 16 % |
| Entrée hors cache | ≈ 0 $ | 0 % |

Le cache marche déjà : il n'y a presque aucune entrée payée au plein tarif. Le levier n'est donc
pas « activer le cache ». Il est de **réduire le nombre de tours multiplié par la taille du
contexte,** et d'**éviter que le cache expire.**

### 3.4 Par taille de contexte au moment du tour

| Contexte | Tours | Coût approximatif |
|---|---|---|
| < 50 k | 3 089 | 94 $ |
| 50 à 100 k | 8 478 | 275 $ |
| 100 à 200 k | 8 300 | 426 $ |
| 200 à 400 k | 5 020 | 471 $ |
| > 400 k | 463 | 75 $ |

Les 5 483 tours faits au-delà de 200 k tokens, soit 21 % des tours, coûtent 546 $, soit 40 %.

## 4. Les constats, mesurés

### 4.1 Le cache expire pendant les attentes (234 $, 17 %)

| Rôle | Écritures totales | Démarrage à froid | Incrémentales | Reconstructions | Coût des reconstructions |
|---|---|---|---|---|---|
| Coder / rédacteur | 178 $ | 14 $ | 86 $ | 147 | 78 $ |
| Session principale | 85 $ | 4 $ | 35 $ | 31 | 45 $ |
| Relecteur | 70 $ | 12 $ | 46 $ | 30 | 11 $ |
| Orchestrateur | 54 $ | 2 $ | 5 $ | 83 | **48 $** |
| Analyste | 48 $ | 3 $ | 26 $ | 25 | 20 $ |
| Driver | 41 $ | 4 $ | 7 $ | 93 | **31 $** |

**Le délai avant reconstruction confirme la cause :**
- 124 des 147 reconstructions des coders surviennent 5 à 15 minutes après le tour précédent, le
  temps d'un `just preflight` ou d'une suite en vraie fenêtre.
- Celles des orchestrateurs et des drivers surviennent 5 à 60 minutes après, le temps d'une CI ou
  d'un sous-agent.
- Celles de la session principale surviennent après plus d'une heure, quand l'utilisateur est absent.

**Le cas de l'orchestrateur de la nuit (« Orchestrator P1+P2 stacked PRs ») :**
- 285 tours, 263 k tokens de contexte moyen, 453 k au maximum, 12,9 h de durée ;
- coût propre de 40,03 $, dont **24,7 $ de reconstructions (62 %),** 12,9 $ de lectures et 1,5 $ de
  sortie. 32,5 $ ont été dépensés avec un contexte de plus de 200 k.

À l'opposé, « Orchestrator night run » a piloté 43 agents (44,9 $ de sous-arbre) en 14 tours, avec
57 k de contexte moyen, pour **0,76 $ de coût propre.** C'est la preuve que le même rôle peut
coûter 50 fois moins cher selon la façon dont il attend et pilote.

### 4.2 Le surcoût d'orchestration varie de 2 % à 32 %

| Orchestrateur ou driver | Coût propre | Sous-arbre | Surcoût | Tours | Contexte max | Durée |
|---|---|---|---|---|---|---|
| Orchestrator P1+P2 stacked PRs (Sonnet) | 40,03 $ | 123,43 $ | 32 % | 285 | 453 k | 12,9 h |
| Orchestrator L : réduction PR #62 (Sonnet) | 25,11 $ | 109,59 $ | 23 % | 231 | 494 k | 3,5 h |
| Driver CR 056 S1..S8 (Opus) | 20,39 $ | 152,33 $ | 13 % | 96 | 211 k | 8,6 h |
| Orchestrator K : requirements batch 3 (Sonnet) | 16,84 $ | 245,97 $ | 7 % | 139 | 417 k | 11,1 h |
| Orchestrator night run (Sonnet) | 0,76 $ | 44,87 $ | **1,7 %** | 14 | 81 k | 7,1 h |
| Orchestrator D : CR 056 (Opus) | 0,73 $ | 153,06 $ | **0,5 %** | 10 | 57 k | 8,6 h |

Les orchestrateurs bon marché délèguent des lots entiers et dorment jusqu'à la notification. Les
chers font eux-mêmes du `git`, des `gh`, des polls et des lectures, et gardent tout dans leur
contexte. Exemple : l'orchestrateur P1+P2 a fait 208 appels Bash, dont 35 lectures de fichiers par
le shell, 34 commandes git et 18 polls.

### 4.3 Coût par CR à taille égale

| Pattern | CR | Coût médian | Lignes médianes | $ / 100 lignes (médiane) | Total | Lignes totales |
|---|---|---|---|---|---|---|
| Driver par CR (CR 023 à 060) | 29 | 5,70 $ | 551 | **1,06 $** | 237,4 $ | 22 414 |
| Pile de nuit, orchestrateur → coder → relecteur (CR 062 à 103) | 40 | 1,24 $ | 104 | **1,02 $** | 83,4 $ | 7 793 |

Ces chiffres excluent le refactor CR 056 (101 869 lignes) et ne comptent pas le surcoût de
l'orchestrateur. Si on l'ajoute, la pile de nuit monte à environ 2,2 $ par CR, dont 0,93 $
d'orchestration pour 43 CR.

À taille égale, le coût par ligne est le même : **le pattern n'est pas en cause, c'est la façon de
l'opérer.**
- **Le driver par CR coûte un peu moins de 1 $ par CR en médiane,** mais il ajoute une couche de
  contexte et d'attente par CR.
- **Les CR qui touchent le vrai VS Code coûtent 2 à 6 $ par 100 lignes :** 041 (1,91), 044 (2,18),
  047 (2,14) et 048 (5,77). Ce sont les tests en vraie fenêtre, la recherche de flakes et les
  attentes longues.
- **La poignée de tableau (CR 084) a coûté 21,33 $,** pour 1 396 lignes et 3 tours de reprise, à
  cause de deux changements de spécification en cours de route : ajout des `{list-table}`, puis
  poignées à l'extérieur du tableau.

### 4.4 Ce que contient le contexte des sous-agents

Sur 576 $ de lectures du cache des sous-agents :

| Contenu | Part (modèle, ± 15 %) | Montant remis à l'échelle |
|---|---|---|
| Prompt de base : prompt système, outils, brief (≈ 34 k tokens en médiane au 1er tour) | 30 % | ≈ 171 $ |
| Résultats d'outils | 49 % | ≈ 283 $ |
| Texte produit par le modèle | 21 % | ≈ 122 $ |

**Le détail des résultats d'outils** (sur les 283 $) :

| Source | Part | Montant | Appels | Taille moyenne |
|---|---|---|---|---|
| Bash, lecture de fichiers (`cat`, `sed -n`, `grep`, `ls`, `find`) | 63,6 % | ≈ 180 $ | 11 000 | 1,5 k tokens |
| Bash, autres commandes | 14,5 % | ≈ 41 $ | 4 770 | 1,1 k |
| Read (hors `src/` et règles) | 6,1 % | ≈ 17 $ | 283 | 5,7 k |
| Read `src/` | 3,3 % | ≈ 9 $ | 56 | 7,0 k |
| okfreq | 3,2 % | ≈ 9 $ | 1 427 | 1,0 k |
| git | 3,0 % | ≈ 8 $ | 1 043 | 1,4 k |
| Images | 0,7 % | ≈ 2 $ | 255 | — |
| Polls CI | 0,1 % | < 1 $ | 498 | 0,1 k |

**Les démarrages à froid ne pèsent que 40 $ (3 %)** pour 657 sous-agents. En revanche, le prompt de
base de 34 k tokens est relu à chaque tour : multiplié par le nombre de tours, il pèse 30 %. Le
levier est donc le **nombre de tours,** pas le nombre de sous-agents.

**Les tours et l'appel d'outils par tour** sont presque séquentiels : environ un appel par tour.

| Rôle | Tours médians | Tours p90 | Contexte médian par tour | Croissance du contexte (dernier / premier) |
|---|---|---|---|---|
| Coder / rédacteur | 32 | 110 | 112 k | 3,4× |
| Analyste | 52 | 94 | 177 k | 6,4× |
| Relecteur | 13 | 49 | 81 k | 2,2× |
| Driver | 26 | 67 | 65 k | 1,9× |
| Orchestrateur | 16 | 39 | 154 k | 2,3× |
| Session principale | 63 | 272 | 170 k | 2,1× |

Les coders font 10 921 appels Bash pour 11 559 tours ; ils regroupent rarement leurs appels.

### 4.5 La base de requirements : écrire puis réduire

Ce chantier a coûté **666 $ (48 % de la semaine)** : 217 $ de rédacteurs, 185 $ d'analystes,
158 $ de critiques et audits, 90 $ d'orchestrateurs. Il a d'abord produit environ 1 000
requirements, avant que l'audit de réduction n'en retienne 440 (76 StRS et 364 SwRS). La réduction
seule, l'orchestrateur L, coûte 109,6 $ de sous-arbre. C'est un coût de première mise en place, qui
ne se répète pas. **Il montre qu'une granularité fixée avant la génération évite de payer deux
fois.**

### 4.6 La session principale (218 $, 16 %)

- Opus 5.5 avec cache à 1 h, 2 703 tours, 170 k tokens de contexte médian, 500 k au maximum.
- 29 reconstructions après plus d'une heure d'absence de l'utilisateur, pour 41 $, avec un contexte
  moyen de 214 k au moment de la reprise.
- Le cache à 1 h y coûte 85 $ d'écritures, mais il évite les reconstructions pour les absences
  de 5 à 60 minutes.

### 4.7 La qualité : ce que la pile de nuit a laissé passer

La pile de nuit, la moins chère par CR, a laissé passer **deux régressions** que seul le test en
vraie fenêtre voyait :
1. #87 bloquait les messages de VS Code vers la page d'aperçu.
2. #82 a cassé un test sans que la CI normale le voie.

Les trouver a coûté une bisection par 5 exécutions de la CI « heavy » et une reprise de
l'orchestrateur. Toute économie doit garder ce filet, au minimum le job « heavy » sur le haut de
chaque pile.

## 5. Ce que les mesures corrigent dans la version courte

| J'avais écrit | La mesure dit |
|---|---|
| Les démarrages à froid des sous-agents coûtent beaucoup | **Faux :** 40 $, 3 %. C'est le prompt de base relu à chaque tour qui pèse (30 % des lectures du cache des sous-agents). |
| Regrouper les petites CR économise 20 à 30 % | **Non démontré :** le coût par ligne est le même pour les petites et les grosses CR. Le gain viendrait surtout de moins d'attentes, pas de moins de démarrages. |
| Le cache de prompts : 40 à 60 % sur les entrées | **Déjà acquis :** 100 % de l'entrée passe par le cache. Le vrai problème est son **expiration** pendant les attentes (17 % du total). |
| Haiku pour les relectures : 10 à 15 % | **À mesurer avant :** les relectures coûtent 15 %, mais elles ont attrapé des erreurs. Risque sur la précision, donc à n'utiliser que pour des contrôles mécaniques, ou mieux, à remplacer par des scripts. |

## 6. Recommandations, classées par gain mesuré et sans perte de précision

Chaque levier garde les mêmes agents et les mêmes relectures. Il change la façon d'attendre, de lire
et de piloter, pas qui juge.

| # | Levier | Base mesurée | Gain estimé | Risque pour la précision |
|---|---|---|---|---|
| 1 | **Aucune attente faite par le LLM.** Un script lance la CI ou le test long, attend, et rend la main avec un résumé de 10 à 30 lignes. L'agent qui attend est soit relancé neuf depuis `STATE.md`, soit maintenu au chaud. Dans un harnais API (Agent SDK), passer le cache à 1 h ou envoyer un keep-alive `max_tokens: 0` toutes les 4 min 30 pour les agents qui attendent. | Reconstructions des sous-agents : 189 $. Écritures 5 min totales : 402 $. | **120 à 170 $ (9 à 12 %)** | Nul : même travail, cache gardé |
| 2 | **Un orchestrateur court et borné.** Il délègue des lots, dort jusqu'aux notifications et ne fait ni git, ni gh, ni lecture lui-même (ces commandes passent par des scripts à sortie résumée). Il passe la main au-delà de 100 k tokens. | Orchestrateurs et drivers : 167 $ propres. Le modèle « night run » coûte 1,7 % de surcoût, contre 32 % pour l'orchestrateur P1+P2. | **80 à 120 $ (6 à 9 %)** | Faible : les décisions restent au LLM, avec un état complet dans les fichiers |
| 3 | **Des lectures ciblées dans les sous-agents.** `grep -n` avec contexte, `sed -n a,b`, des résumés de logs, et des sorties de vérifications tronquées par script à l'erreur utile. Regrouper les lectures en parallèle dans un même tour. | Lectures par le shell : ≈ 180 $. Autres sorties Bash : ≈ 41 $. Croissance du contexte 3,4× chez les coders. | **70 à 110 $ (5 à 8 %)** | Faible si le script garde la sortie complète sur disque, que l'agent peut ouvrir |
| 4 | **Moins de tours, avec des appels groupés.** Une consigne de parallélisme, et des scripts « tout-en-un » pour la routine : vérifications, commit, PR, pile. | Le prompt de base relu à chaque tour pèse ≈ 171 $ ; environ un appel par tour aujourd'hui. | **40 à 80 $ (3 à 6 %)** | Nul |
| 5 | **Une spécification figée avant de coder les fonctionnalités.** Pour la CR 084, les deux changements de spécification ont coûté environ 3 reprises. Pour les requirements, la granularité doit être fixée avant la génération. | CR 084 : 21,33 $. Réduction des requirements : 109,6 $ de sous-arbre. | Ponctuel, de 10 à 100 $ par chantier | Positif : moins de reprises |
| 6 | **Une session principale légère.** Elle délègue les lectures longues, compacte ou repart d'un résumé avant une longue absence, et garde Opus pour le jugement. | 218 $ ; 41 $ de reconstructions après plus d'une heure. | **25 à 45 $ (2 à 3 %)** | Nul |
| 7 | **Le bon modèle par rôle.** Sonnet pour les coders et les orchestrateurs. Opus seulement pour la cause racine et la bisection, et pour la session humaine. Haiku uniquement pour des contrôles mécaniques, déjà mieux faits par script. | Sous-agents Opus : 369 $ (27 %). À taille égale, la pile de nuit (Sonnet) coûte autant par ligne que l'ère Opus et driver. | À mesurer : jusqu'à 30 % du coût des coders Opus | **Moyen :** valider sur 10 CR avant de généraliser |

**Total des leviers 1 à 4 et 6, sans toucher aux modèles : environ 335 à 525 $ sur 1 374 $, soit
24 à 38 %.** Ces leviers se recouvrent partiellement : moins de tours, c'est aussi moins
d'expirations. Je retiens donc **30 à 40 %** comme fourchette prudente avec le levier 7, et 25 à
30 % sans lui.

## 7. Garder la flexibilité de l'orchestrateur

- **Le LLM garde :** le triage, la découpe, les choix produit, la cause racine, les écarts au plan
  (une CR sortie de la pile, une correction ajoutée en haut), le code et la relecture.
- **Les scripts prennent :** la création de la CR et du worktree, l'assemblage du brief, les
  vérifications à sortie résumée, le commit et le contrôle du corps de PR, `gh stack` (sans jamais
  renommer une branche ouverte), l'attente et le résumé de la CI (`ci-triage`), le job « heavy » sur
  le haut de la pile, et l'archivage.
- **Chaque étape de script peut être sautée ou refaite par l'orchestrateur** (`--from`, `--skip`). Un
  échec de script rend la main avec son résumé ; il ne corrige jamais rien en silence.
- **Pour les travaux non standard** (recherche, fonctionnalité, bisection), l'orchestrateur pilote
  librement, avec seulement les règles 1 à 3 : pas d'attente LLM, contexte borné, sorties résumées.

## 8. Plan de mise en place et mesure

1. **Garder ce script d'analyse comme outil.** Il est copié dans `.agents/changes/cost-analysis/`
   (`analyze.py`, `roles.py`, `deep.py`, `rebuild.py`). Le déplacer dans `scripts/` pour le versionner. Il
   suffit pour suivre chaque semaine le coût par rôle, par CR et par 100 lignes, et le taux de
   reconstructions.
2. **Écrire les scripts d'attente et de résumé** (`ci-triage`, `cr-gates`, `cr-wait`), puis mettre
   la règle « aucune attente LLM » et la relève à 100 k dans le guideline
   change-requests-lifecycle.
3. **Relancer une pile de 10 CR et comparer à la référence de cette semaine,** sur ces indicateurs :

   | Indicateur | Référence | Objectif |
   |---|---|---|
   | Surcoût d'orchestration | 32 % | < 5 % |
   | Coût des reconstructions | 17 % du total | < 5 % |
   | Coût par 100 lignes | 1,02 $ | stable ou en baisse |
   | Régressions vues par le job « heavy » | 2 | 0 |

4. **Seulement ensuite, tester le levier 7** (le modèle par rôle) sur un échantillon, avec le même
   filet de tests.

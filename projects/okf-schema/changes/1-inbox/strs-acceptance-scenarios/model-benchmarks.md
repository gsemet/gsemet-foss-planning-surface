---
title: "Benchmark de 5 modèles LLM sur une implémentation complète (okf-schema)"
description: >-
  Comparaison honnête de 5 modèles de code sur une même spécification multi-surfaces de 1 260
  lignes, évalués sur le temps, le coût en tokens et la précision réelle (tests de mutation).
status: published
date: 2026-11-25
---

# Benchmark de 5 modèles LLM sur une implémentation complète

Cinq modèles de code ont implémenté **la même spécification de changement** de bout en bout sur le
dépôt open-source [`okf-schema`](https://github.com/gsemet/okf-schema) (outil Python `okfreq` de
traçabilité d'exigences). Ce rapport compare leurs livrables sur trois axes — **temps**, **coût en
tokens** et **précision par rapport à la spécification** — en privilégiant la qualité mesurée
(tests de mutation, exécution réelle) plutôt que le volume de code ou de documentation produit.

[TOC]

## Résumé exécutif

::::{grid} 1 1 3 3
:::{grid-item-card} Meilleur équilibre
**Claude Sonnet 5.5** ([PR #63](https://github.com/gsemet/okf-schema/pull/63))
^^^
Le plus rapide (~29 min actif, 42 min avec CI), **0 écart notable** à la spec, 8/8 mutations
tuées et CI verte sur les 6 environnements.
+++
Temps 9,5/10 · Coût 5,5/10 (~16 $) · Précision 9/10
:::
:::{grid-item-card} Surprise qualitative
**DeepSeek V4.1 Flash** ([PR #64](https://github.com/gsemet/okf-schema/pull/64))
^^^
10/10 mutations tuées et très peu d'interventions humaines, mais au prix d'une approche par force
brute : **3 h** de run et **4× plus de tokens** que les autres.
+++
Temps 2,5/10 · Coût 4/10 (214 M in) · Précision 8,5/10
:::
:::{grid-item-card} Leçon transversale
**Couverture ≠ Robustesse**
^^^
La couverture (>95 %) et une CI verte ne suffisent pas : Gemini 4 Neon passe la CI du premier
coup avec la meilleure doc (8/10) et 3× moins de tokens, mais ne tue que **5/10 mutations**.
+++
Tests de mutation et dédoublonnage doc restent clés
:::
::::

## Ce qui a été benchmarké

### Le sujet : une évolution multi-surfaces de `okfreq`

`okf-schema` fournit des schémas JSON et des outils CLI (`okfreq`, `okfkb`) pour gérer des bases
d'exigences en Markdown avec frontmatter YAML. La spécification soumise aux 5 modèles
([`03-change-spec.md`](03-change-spec.md), ~1 260 lignes, 9 règles normatives, matrice de
vérification D1–D7) demandait d'ajouter un nouveau mode de couverture des exigences parties
prenantes (*StRS*) :

- **Scénarios déclarés :** un champ frontmatter `scenarios:` listant les chemins principaux d'un
  StRS (`S1`, `S2`…) et les transitions d'un SwRS, avec des titres alignés dans le corps.
- **Deux verbes de traçabilité :** un nouveau marqueur `@accepts_req <StRS>#S<n>` pour les tests
  d'acceptation sur le produit assemblé, distinct de `@tests_req <ID>#S<n>` pour les tests
  unitaires ou d'intégration, produisant **deux compteurs indépendants** (*tested* et *accepted*).
- **Diagnostics et dérogations :** deux avertissements actionnables (`W003` et `W004`) et un
  mécanisme de dérogation justifiée (*waiver*) avec motif non vide obligatoire.
- **Rétrocompatibilité stricte :** format de rapport v2, mais **sortie inchangée** dans les deux
  modes historiques (`linked-swrs` et `linked-swrs-and-validation-test`).
- **6 surfaces touchées par chaque PR (~112 à 115 fichiers) :** moteur Python et CLI, schémas JSON,
  documentation humaine (Diátaxis), skills d'agents, exemples exécutables et migration des propres
  exigences du dépôt avec 12 tests d'acceptation sur le wheel installé.

### Protocole d'évaluation

Plutôt que d'évaluer au volume de code ou de tests, chaque PR a été contrôlée selon la même
grille :

1. **Conformité CLI en boîte noire :** exécution de la matrice de la spec (modes historiques vs
   nouveau mode, `okfreq new`, `validate`, `trace`, `update-coverage`, `report`) dans des projets
   temporaires isolés.
2. **Test de mutation :** injection manuelle, un par un, de **8 à 10 défauts comportementaux** dans
   le moteur (ex. `@tests_req` compté comme accepté, `W004` supprimé, motif de dérogation vide
   accepté, `retire` ignorant `@accepts_req`, anciens modes altérés) afin de mesurer si la suite de
   tests de la PR détecte réellement les régressions.
3. **Revue qualitative des tests et de la documentation :** distinction entre tests comportementaux,
   doublons, tests tautologiques ou couplés au texte ; vérification par exécution des exemples
   documentés ; mesure de la redondance documentaire.
4. **Métriques de session :** durée active, appels LLM, volume de tokens (entrée, cache, sortie) et
   coût extraits directement des journaux d'exécution.

:::{important} Biais méthodologiques à garder en tête
1. **Évolution de la spec en cours de route :** Fusion (GPT-6.1 Terra, `#60`) a tourné avant
   l'ajout de 5 clarifications tardives (`U1`–`U5`) dans la spec et a reçu deux retouches manuelles
   après coup. MAI-Code-2 (`#62`), Sonnet 5.5 (`#63`), DeepSeek V4.1 Flash (`#64`) et Gemini 4
   Neon (`#65`) ont travaillé en un seul tir sur la spec mise à jour.
2. **Tarification :** les coûts de MAI-Code-2 et DeepSeek V4.1 Flash sont estimés à partir de tarifs
   de repli (DeepSeek V4.1 Flash étant facturé 0 $ sur l'environnement d'essai). C'est pourquoi le
   **volume brut de tokens** et le **nombre d'appels LLM** figurent dans le tableau ci-dessous.
3. **Tests de mutation :** chaque revue indépendante a choisi ses 8 à 10 mutations pertinentes pour
   le code inspecté ; le ratio tué/total est un indicateur fort de robustesse, pas un score
   normalisé au pourcent près.
:::

## Comparaison synthétique

| Modèle (PR) | Temps (/10) | Coût & tokens (/10) | Précision (/10) | Mutations tuées | Tests / Couv. | Doc (/10) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Claude Sonnet 5.5**                                                          | **9,5** · ~29 min actif (42 min total) | **5,5** · ~16 $ · 57 M in / 530 k out · 498 appels | **9,0** · 0 écart notable | 8 / 8 | 1 116 · 95,61 % | 6,5 |
| **DeepSeek V4.1 Flash**                                                          | **2,5** · ~3h03 continu | **4,0** · 0 $ fact. (~10,5 $ est.) · **214 M in / 2,1 M out** · 2 105 appels | **8,5** · écarts mineurs | 10 / 10 | 1 141 · 95,60 % | 6,0 |
| **Gemini 4 Neon**                                                              | **7,5** · ~49 min actif (55 min total) | **7,5** · ~9,47 $ · **19 M in** / 194 k out · 170 appels | **7,0** · trous de tests cas limites | 5 / 10 | 1 040 · 95,17 % | **8,0** |
| **Fusion (GPT-6.1 Terra)**                                                 | **5,0** · ~1h43 actif (14 msg) | **8,0** · ~4,85 $ · 59 M in / 172 k out · 426 appels | **6,5** · trous CLI/skills | 7 / 9 | 1 086 · 95,57 % | 6,0 |
| **MAI-Code-2**                                                          | **7,0** · ~54 min–1h11 | **9,0** · ~2,9 $ est. · 49 M in / 97 k out · 259 appels | **5,5** · couv. < 95 %, écarts | 6 / 9 | 1 040 · 94,96 % | 6,0 |

### Notes par axe

```vega-lite
data:
  values:
    - {model: "Sonnet 5.5 (#63)", axe: "Temps", note: 9.5}
    - {model: "Sonnet 5.5 (#63)", axe: "Coût en tokens", note: 5.5}
    - {model: "Sonnet 5.5 (#63)", axe: "Précision / spec", note: 9.0}
    - {model: "DeepSeek V4.1 Flash (#64)", axe: "Temps", note: 2.5}
    - {model: "DeepSeek V4.1 Flash (#64)", axe: "Coût en tokens", note: 4.0}
    - {model: "DeepSeek V4.1 Flash (#64)", axe: "Précision / spec", note: 8.5}
    - {model: "Gemini 4 Neon (#65)", axe: "Temps", note: 7.5}
    - {model: "Gemini 4 Neon (#65)", axe: "Coût en tokens", note: 7.5}
    - {model: "Gemini 4 Neon (#65)", axe: "Précision / spec", note: 7.0}
    - {model: "GPT-6.1 Terra (#60)", axe: "Temps", note: 5.0}
    - {model: "GPT-6.1 Terra (#60)", axe: "Coût en tokens", note: 8.0}
    - {model: "GPT-6.1 Terra (#60)", axe: "Précision / spec", note: 6.5}
    - {model: "MAI-Code-2 (#62)", axe: "Temps", note: 7.0}
    - {model: "MAI-Code-2 (#62)", axe: "Coût en tokens", note: 9.0}
    - {model: "MAI-Code-2 (#62)", axe: "Précision / spec", note: 5.5}
mark: bar
encoding:
  y:
    field: model
    type: nominal
    sort: ["Sonnet 5.5 (#63)", "DeepSeek V4.1 Flash (#64)", "Gemini 4 Neon (#65)", "GPT-6.1 Terra (#60)", "MAI-Code-2 (#62)"]
    title: null
  x:
    field: note
    type: quantitative
    scale: {domain: [0, 10]}
    title: "Note (/10)"
  yOffset: {field: axe}
  color: {field: axe, type: nominal, title: "Axe"}
config:
  axis: {labelFontSize: 14, titleFontSize: 15, labelLimit: 260}
  legend: {labelFontSize: 14, titleFontSize: 15}
```

### Volume, coûts et temps

::::{grid} 1 1 3 3
:::{grid-item-card} Volume de tokens
```vega-lite
width: container
data:
  values:
    - {model: "Gemini 4 Neon", tokens_m: 19.3, calls: 170}
    - {model: "MAI-Code-2", tokens_m: 48.9, calls: 259}
    - {model: "Sonnet 5.5", tokens_m: 57.4, calls: 498}
    - {model: "GPT-6.1 Terra", tokens_m: 58.6, calls: 426}
    - {model: "DeepSeek V4.1", tokens_m: 214.2, calls: 2105}
mark: bar
encoding:
  y: {field: model, type: nominal, sort: x, title: null}
  x: {field: tokens_m, type: quantitative, title: "Entrée (M tokens, cache inclus)"}
  tooltip:
    - {field: model, type: nominal}
    - {field: tokens_m, type: quantitative, title: "Tokens entrée (M)"}
    - {field: calls, type: quantitative, title: "Appels LLM"}
config:
  axis: {labelFontSize: 14, titleFontSize: 15, labelLimit: 220}
  legend: {labelFontSize: 14, titleFontSize: 15}
```
+++
Gemini 4 Neon : 3× moins que Sonnet, 11× moins que DeepSeek
:::
:::{grid-item-card} Coûts (USD)
```vega-lite
width: container
data:
  values:
    - {model: "MAI-Code-2", usd: 2.9, source: "Estimé"}
    - {model: "GPT-6.1 Terra", usd: 4.85, source: "Facturé"}
    - {model: "Gemini 4 Neon", usd: 9.47, source: "Facturé"}
    - {model: "DeepSeek V4.1", usd: 10.46, source: "Estimé (0 $ facturé)"}
    - {model: "Sonnet 5.5", usd: 16.02, source: "Facturé"}
mark: bar
encoding:
  y: {field: model, type: nominal, sort: x, title: null}
  x: {field: usd, type: quantitative, title: "Coût (USD)"}
  color: {field: source, type: nominal, title: null, legend: {orient: bottom, columns: 1}}
  tooltip:
    - {field: model, type: nominal}
    - {field: usd, type: quantitative, title: "USD"}
    - {field: source, type: nominal, title: "Source"}
config:
  axis: {labelFontSize: 14, titleFontSize: 15, labelLimit: 220}
  legend: {labelFontSize: 14, titleFontSize: 15, labelLimit: 240}
```
+++
Tarif de repli pour MAI-Code-2 et DeepSeek
:::
:::{grid-item-card} Temps actif (minutes)
```vega-lite
width: container
data:
  values:
    - {model: "Sonnet 5.5", min: 29, note: "42 min avec CI"}
    - {model: "Gemini 4 Neon", min: 49, note: "55 min avec CI"}
    - {model: "MAI-Code-2", min: 54, note: "1h11 session totale"}
    - {model: "GPT-6.1 Terra", min: 103, note: "1h43 actif, 14 msg"}
    - {model: "DeepSeek V4.1", min: 173, note: "2h53 actif (3h03 brut)"}
mark: bar
encoding:
  y: {field: model, type: nominal, sort: x, title: null}
  x: {field: min, type: quantitative, title: "Durée active (min)"}
  tooltip:
    - {field: model, type: nominal}
    - {field: min, type: quantitative, title: "Minutes actives"}
    - {field: note, type: nominal, title: "Détail"}
config:
  axis: {labelFontSize: 14, titleFontSize: 15, labelLimit: 220}
  legend: {labelFontSize: 14, titleFontSize: 15}
```
+++
Temps de travail agent hors attentes humaines
:::
::::

## Analyse détaillée par modèle

::::{tab-set}
:::{tab-item} Sonnet 5.5 (#63)
**Verdict : meilleur livrable global** — Temps **9,5/10** · Coût **5,5/10** · Précision **9,0/10**

- **Points forts :** exécution la plus rapide grâce au parallélisme des sous-agents (~29 min de
  travail effectif, 42 min CI comprise, zéro attente humaine) ; **8/8 mutations tuées** ; aucun
  écart notable par rapport à la spec (anciens modes préservés, erreurs `validate` affichées en
  mode texte) ; CI verte sur les 6 jobs (Python 3.10–3.13, macOS, Windows).
- **Points faibles :** coût intermédiaire (~16 $, dont 78 % dans les 8 sous-agents) ; quelques
  doublons entre tests bibliothèque et CLI ; documentation redondante (mêmes règles répétées dans
  5 à 6 pages).
:::
:::{tab-item} DeepSeek V4.1 Flash (#64)
**Verdict : très solide, mais très lent et très verbeux** — Temps **2,5/10** · Coût **4,0/10** ·
Précision **8,5/10**

- **Points forts :** surprise qualitative du benchmark ; **10/10 mutations tuées** ; seulement 5
  interventions utilisateur ; seul modèle à relayer le test d'acceptation rapide dans la suite
  propre d'`okf-schema` (`tests/test_acceptance_export.py`).
- **Points faibles :** compense par la force brute (~3 h en continu, 2 105 appels LLM, 34
  compactions, 214 M tokens en entrée et 2,1 M en sortie) ; diff très lourd (+7 696 lignes) ;
  petits défauts (placeholder `<main path title>` compté comme scénario déclaré, un assert vide,
  correctifs Windows encore en cours lors de l'audit) ; doc très redondante (819 lignes sur deux
  pages).
:::
:::{tab-item} Gemini 4 Neon (#65)
**Verdict : très sobre, doc au top et CI verte du premier coup, mais tests trop légers sur les cas
limites** — Temps **7,5/10** · Coût **7,5/10** · Précision **7,0/10**

- **Points forts :** champion absolu de la sobriété en tokens (**19,3 M in** dont 94 % de cache,
  194 k out, 170 appels — 3× moins que Sonnet 5.5 et 11× moins que DeepSeek) pour ~9,47 $ et
  ~49 min de travail actif (55 min avec CI) ; un seul commit propre et **CI verte dès le premier
  push** sur les 6 plateformes (Python 3.10–3.13, macOS, Windows) ; cœur du moteur conforme aux
  règles 1–9 (anciens modes préservés) ; **meilleure documentation du benchmark (8,0/10)**,
  claire et exacte.
- **Points faibles :** seulement **5/10 mutations tuées** — les tests unitaires couvrent mal les
  cas négatifs (motif de *waiver* ou d'exemption composé d'espaces, StRS déprécié, nettoyage de
  `accepted_in_files` en ancien mode) ; 4 petits oublis de spec (textes `--help` CLI non mis à
  jour sauf `trace`, placeholders non remplis provoquant un `W002` dans `examples/okfreq-examples`
  suite à un `.replace()` obsolète dans le `justfile`, contrôle de cohérence des titres absent de
  `test_project_contract.py`).
:::
:::{tab-item} GPT-6.1 Terra (#60)
**Verdict : économe mais incomplet et plus laborieux** — Temps **5,0/10** · Coût **8,0/10** ·
Précision **6,5/10**

- **Points forts :** bon rapport coût/volume (~4,85 $ sur 426 appels) ; cœur du moteur conforme ;
  anciens modes respectés sur `okfreq new` ; exemples documentés vérifiés par les tests.
- **Points faibles :** session la plus chaotique (14 messages utilisateur, relances « recommence »
  et push oublié) ; **1 mutation survit** (motif de *waiver* composé d'espaces accepté) et 1 autre
  n'est détectée que par un test sur le dépôt lui-même ; `trace` altère la sortie des anciens
  modes ; CLI et skills non couverts par les tests.
:::
:::{tab-item} MAI-Code-2 (#62)
**Verdict : champion de la sobriété, mais trop juste en rigueur** — Temps **7,0/10** · Coût
**9,0/10** · Précision **5,5/10**

- **Points forts :** le plus sobre en appels (259) et en tokens (48,9 M in / 97 k out, ~2,9 $
  estimé) ; livré en un seul commit propre ; anciens modes conformes sur `okfreq new`.
- **Points faibles :** **3 mutations sur 9 survivent** (`retire`, préremplissage `okfreq new`,
  helper de motif de *waiver* vide) ; couverture à **94,96 %** (sous le seuil de 95 %) ; écart de
  nommage (`tested`/`accepted` au lieu de `tests`/`accepts`) ; documentation tronquée sur
  `okfreq-cli.md` et affirmation inexacte (« schema-driven » pour un texte codé en dur) ;
  `CHANGELOG.md` modifié hors périmètre.
:::
::::

## Enseignements et recommandation

:::{tip} Décision recommandée : merger **Claude Sonnet 5.5** (`gsemet/okf-schema#63`)
C'est le meilleur compromis entre fiabilité prouvée (8/8 mutations tuées, 0 écart de spec, CI
verte), vitesse d'exécution (~29 min actif) et coût maîtrisé (~16 $).
:::

Quatre enseignements ressortent de cet exercice sur une tâche longue et multi-surfaces :

1. **Ne pas confondre volume, couverture et qualité :** les 5 modèles produisent 10 à 20 % de
   tests faibles (extraits de prose, doublons) et dupliquent les mêmes règles dans plusieurs
   fichiers de documentation (même Gemini 4 Neon, pourtant le meilleur en doc à 8/10). Le test de
   mutation a été décisif : Gemini 4 Neon dépasse 95 % de couverture et passe la CI du premier
   coup, mais ne tue que 5/10 mutations sur les cas limites.
2. **Le parallélisme bien orchestré fait la différence sur le délai :** Sonnet 5.5 boucle les 6
   surfaces en ~29 min de travail effectif (42 min avec CI), soit 2 à 4× plus vite que les autres
   runs, sans sacrifier la précision.
3. **Les modèles « gratuits » ou bon marché peuvent compenser par le volume :** DeepSeek V4.1 Flash
   atteint un excellent niveau fonctionnel mais consomme ~4× plus de tokens et 3 h de temps mur, ce
   qui pèse sur la latence et la taille du diff à relire.
4. **Post-traitement humain indispensable sur la documentation :** quelle que soit la PR retenue,
   un passage court de dédoublonnage (une seule source de vérité dans la référence, liens depuis les
   autres pages) et de nettoyage des tests d'extraits de prose reste nécessaire avant ou juste après
   le merge.

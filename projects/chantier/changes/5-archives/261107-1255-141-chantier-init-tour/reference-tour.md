# Reference tour (approved by the user, 2026-11-07)

The simulation of `init` run on the chantier repository itself, chat mode, as the user approved
it ("C'est parfait"). It is in the user's language, French; the tour always talks the user's
language. It is the target for tone, structure, depth and length, not a text to copy: every
path, gate, example CR and improvement comes from the project at hand.

---

### chantier, en une phrase

Tu donnes tes demandes à un seul interlocuteur, et une équipe d'agents les réalise : chaque
changement devient une pull request. Trois choses restent à toi : quoi faire, quand lancer, quoi
merger.

### L'histoire d'une demande

Suivons un vrai manque de ce dépôt : `just tag` lit la version dans ta copie locale au lieu de
`origin/main`.

1. **Tu la dis au Chief of Staff**, le chef de cabinet : il t'écoute et ne code jamais. « Dépose
   ceci » : elle devient une **Change Request (CR)**, un dossier dans `.agents/changes/1-inbox/`.
2. **Il te grille** : quelques questions, chacune avec sa réponse recommandée (« refuser une
   copie en retard, ou lire `origin/main` ? »). Tes réponses donnent la **spécification** : ce
   que la CR change, et rien de plus.
3. **Tu la priorises** (« mets-la en P1 ») : elle passe dans `2-backlog/P1/`.
4. **Tu dis « lance les P1 »**. Il montre le plan et attend ton go. Ensuite, il ouvre un
   **batch**, c'est-à-dire les CR lancées ensemble (`batch-08`). Puis il démarre le **Foreman**,
   le contremaître : une autre session qui répartit le travail sans poser une seule brique.
5. **Un Driver**, le chef d'équipe, prend la CR dans un **slot** libre. Il crée la branche
   `chantier/batch-08/140-just-tag-origin-main` et sa copie de travail à côté du dépôt. Puis il
   enchaîne les **rounds** : le **Coder** écrit, l'**Inspector** relit sans avoir écrit, trois
   fois au plus.
6. Le Driver lance ensuite le **long gate** (`just scenario`), pousse le code, ouvre la PR et lit
   la CI. Le **Verifier**, qui n'a rien écrit, prouve sur le code poussé que la spécification
   est tenue. La CR est **ready**.
7. **Tu relis et tu merges** : chantier ne merge jamais tes PR. Tu dis « j'ai mergé #80 », et le
   dossier part dans `4-archives/`.

```text
toi ⇄ Chief of Staff ──ordres──▶ Foreman ──▶ Driver (un par CR) ──▶ Coder · Inspector · Verifier
         ▲                         │ questions        │ fin de CR
         └────── rapports ◀────────┴◀─────────────────┘
```

```text
1-inbox ─priorité─▶ 2-backlog/P1…P4 ─lancement─▶ 3-requests/batch-08 ─ton merge─▶ 4-archives
   └───────────────────── abandon ─────────────────────────────────────────────▶ 5-trash
```

```text
Coder → Inspector ✗ → Coder → Inspector ✓ → long gate → PR → CI → Verifier → ready → ton merge
```

### Ce que tu verras

```text
.agents/changes/3-requests/batch-08/140-just-tag-origin-main/
├── intake/request.md    ta demande, telle quelle
├── 01-intent.md         résumée et analysée
├── 02-answers.md        tes réponses
├── 03-change-spec.md    la spécification
└── work/                notes, journaux des gates, texte de la PR
```

« status ? » :

| CR | État | PR | Dépense |
|---|---|---|---|
| CR-140 just tag | working, round 2 sur 3 | — | $… |
| CR-141 … | ready | #81 | $… |

### L'argent et tes décisions

- **Budget :** un plafond en dollars pour le Foreman et son équipe. Une fois atteint, aucun
  Driver ne démarre plus.
- **Slots :** combien de CR tournent en même temps (4 par défaut).
- **Rounds :** combien de reprises par CR (3 par défaut).
- **Ce que toi seul fais :** prioriser, dire go, merger, publier une release, relever une limite.
- « Combien ça a coûté ? » donne le détail mesuré.

### Pour bien démarrer ici

- **Le harnais est clair :** `just check` (fast gate), `just scenario` (long gate), `main`
  protégée, merge par rebase. Rien à ajouter à `AGENTS.md` pour commencer.
- **`.gitignore` :** `.agents/` n'est ni suivi ni ignoré. Ajoute toi-même la ligne
  `.agents/changes/` : ta copie de `main` reste propre, et les CR restent sur ta machine.
- **CR proposée :** `just tag` lit la version depuis `origin/main`. Je la dépose en inbox ?

**Phrases à dire :** « dépose ceci : … », « mets-la en P1 », « lance les P1 », « status ? »,
« drop CR-140 », « j'ai mergé #80 », « combien ça a coûté ? ».

**Glossaire :**
- **Stack :** les PR d'un batch empilées l'une sur l'autre.
- **Fast gate :** la vérification rapide après chaque round.
- **Long gate :** la suite complète, une fois avant la PR.
- **Investigator :** cartographie le code avant le premier round.
- **Debugger :** trouve pourquoi un check est rouge.
- **Conflict resolver :** fait le rebase et résout les conflits.
- **Release CR :** publie ce qui est mergé, selon la procédure du projet.
- **Grant :** ce que tu autorises pour une release sans qu'on te le redemande.
- **STATUS.md :** l'état du batch, que le CLI tient à jour.
- **close :** clôt un batch terminé, sur ton oui.

# Answers

## 2026-11-10, while batch-09 ran

- The user, on triage while steering: "Ah si tu peux trier mais pas démarrer".
- Then: "En mode direct ou autre tu peux trier (soit directement soit à la demande d'un griller), réorganiser le backlog, ajouter supprimer merger etc tout ce que tu peux faire avec des fichiers. C'est toucher au batch que tu peux pas".
- So, in either steering mode, while a batch runs:
  - **Allowed:** any work on the backlog's files:
    - triage, directly or on a Griller's request;
    - reorganise the backlog;
    - file, add, drop and merge items.
  - **Not allowed:** touching the running batch. For example, a CR does not join it and nothing is started.
  - The card's line forbidding triage while steering is stricter than this and must change.
  - Grilling and writing specifications are not named here: the grill of this CR settles them.
- The Chief of Staff had saved these rules in its own host memory. The user: "Je ne veux pas que tu te bases sur ta mémoire je veux encoder ce qu'il faut dans chantier pour les AUTRES utilisateurs. Laisse ta mémoire en dehors".
  - **The fix lives in chantier itself:** the cards, the skill and the CLI, so that it works for every user and on every host.
  - It must not rely on an agent's private memory or on this user's setup.
  - The memory entries were removed.
- The user then asked for "chantier reload": "Ah si je dit « chantier reload » ou « /chantier reload » (en text ou en skill), je veux que ce soit pour recharger les règles de chantier. Typiquement après un compact. Ou alors tu es capable de détecter que tu as été compact et recharger par toi même le skill ?"
  - It was filed as `chantier-reload`.
  - Asked whether to merge it into this CR, the user said: "Oui fusionne".
  - Its request is kept whole in `intake/chantier-reload-request.md`:
    - a reload entry point, in plain text or through the skill;
    - an automatic reload after a compaction that does not rely on the model noticing it. A lead to study: the plugin's hooks module and its `session.compact` event.

## Grill of 2026-11-10, batch-09 paused

1. **Grill and spec-writer while steering.**
   - The question: are grilling a CR with the user and starting the spec-writer allowed while the session steers a running batch?
   - The user: "Pas de grille, spec writer oui".
   - The steering session does not grill while its batch runs.
   - It may start the spec-writer on a CR already grilled, for example by a Griller, on the user's word.
   - Combined with the earlier answer, while a batch runs:
     - **allowed:** all work on the backlog's files (file, triage, reorganise, merge, drop) and starting the spec-writer;
     - **not allowed:** grilling, and touching the batch.
2. **How the rules survive a compaction.**
   - The user chose "Rechargement auto (Recommandé)".
   - **Automatic reload:** on Claude Code, the plugin's hooks module reloads the cards at every compaction, manual or automatic.
   - **Manual reload:** "chantier reload", in plain text or through the skill, does the same.
   - **No new CLI gate:** the CLI keeps refusing only what touches the batch, as it does today.
   - The CLI gate asked for in `intake/no-grill-while-steering-request.md` is replaced by the reload.
3. **When the Chief of Staff does not know where the user is.**
   - Where the user is means a phone on Remote Control, the desktop app or a terminal.
   - The user chose "Tout proposer, avec la condition", against the recommendation to assume the phone.
   - The Chief of Staff offers every option that fits, and each option says where it can be done from, for example "from the machine" or "from the phone".
   - The checklist by environment gives that condition and its reason for each option.
   - **Refined later in the same grill.**
     - The user asked: "Tu sais pas si je suis en remote ou en local ?"
     - The Chief of Staff answered with what it had seen. In the Claude desktop app, the host signals at times that the user works over Remote Control: on this day it said so at each turn's end. A terminal or Copilot gives no such signal.
     - The user chose "Signal d'abord (Recommandé)".
     - When the host says where the user is, the Chief of Staff offers only what the user can do from there.
     - When the host says nothing, it offers every option, each with its condition.
4. **Copilot.**
   - The user chose "Claude Code seulement", against the recommendation to look for a Copilot way first.
   - This CR covers Claude Code only: the automatic reload and "chantier reload".
   - Copilot is left to another CR.
   - After the restatement, the user added: "Arrange toi organiser l'information pour quand je le ferait sur copilot il y aura la place pour ses spécificités".
     - The common part goes in the shared cards, the same on every host:
       - the rules on what the steering session may do;
       - what a reload reads and does;
       - the general rule for offering options.
     - What depends on the host goes in the host's reference (`hosts/claude-code.md`, `hosts/copilot.md`):
       - how the automatic reload is triggered;
       - which surfaces exist and how the host signals where the user is;
       - each option's condition there.
     - `hosts/copilot.md` gets the same sections, marked "not done yet" with the reason, so the later Copilot CR fills them without reorganising anything.

## Grilled enough (2026-11-10)

- After the full restatement, the user: "Ok pour moi".
- The CR is grilled enough. It stays in P2.
- The user's go for the spec-writer: "Lance le reste".

## The specification's open questions (2026-11-10)

- The user, before they were asked: "Plus de question. Livre le max".
- The Chief of Staff took the specification's recommended answers, which the specification already writes:
  1. **Demo while the batch runs:** no demo. The demo goes through the batch's own stack, which counts as touching the batch.
  2. **Griller:** the reload, manual and automatic, also covers a Griller session.
- The user may still change either answer when reviewing the PR.
5. **Saying that the rules were reloaded.**
   - The user chose "Une ligne (Recommandé)".
   - After an automatic reload, the next answer starts with one line saying chantier's rules were reloaded.
6. **Splitting the CR.**
   - The user chose "Couper en deux (Recommandé)".
   - `add-several-while-paused` becomes its own CR again, in P1, with its grill (`intake/add-several-while-paused-*`).
   - This CR keeps three topics, in P2:
     - what the steering session may do;
     - the reload, automatic and manual;
     - the options by environment.

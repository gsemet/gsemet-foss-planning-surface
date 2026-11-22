import json, re, sys
WEB = "C:/Users/gaeta/Projets/chantier.worktrees/batch-30-CR-439/skills/chantier/scripts/cli/src/chantier/clients/web/js/"
R = "https://github.com/gsemet/chantier"
D = R + "/blob/main/docs/"

# id, group, doc, (en name, line, body), (fr name, line, body)
T = []
def add(i, g, doc, en, fr):
    T.append((i, g, doc, en, fr))

add("change_request", "concepts", R + "#change-requests-lifecycle",
 ("Change request", "One level over your tracker's issues: a folder that describes what you want.",
  """A Change Request (CR) sits one level over the issues of your tracker. Small requests that do not belong in the tracker, an idea, a bug, a report, are accepted and prioritised here without entering it. The tracker keeps the strategic, long-term plan; the planning folder is the tactical, short-term one, closest to the work site.

A CR is a folder, and its content varies, from one line of text to several HTML prototypes. The agents read it and find the request's intent.

CRs are fungible in the plan: they can be split, merged or dropped."""),
 ("Change request", "Un niveau au-dessus des tickets de votre tracker : un dossier qui décrit ce que vous voulez.",
  """Une Change Request (CR) se place un niveau au-dessus des tickets de votre tracker. Les petites demandes qui n'ont pas leur place dans le tracker, une idée, un bug, un rapport, sont acceptées et priorisées ici sans y entrer. Le tracker garde la vision stratégique à long terme ; le dossier de planification est le plan tactique à court terme, au plus près du chantier.

Une CR est un dossier, et son contenu varie, d'une seule ligne de texte à plusieurs prototypes HTML. Les agents le lisent et en déduisent l'intention de la demande.

Les CR sont fongibles dans le plan : on peut les découper, les fusionner ou les abandonner."""))

add("grill", "concepts", D + "use-cases.md#turn-ideas-into-ready-work",
 ("Grill and specification", "The questions a change needs, asked one by one, then written down as a specification.",
  """The Chief of Staff, or a Griller, asks the questions a change needs. Each answer is recorded in the CR.

When you say "grilled enough", you choose where the CR goes: the next batch (3-ready, the default) or the running batch, offered only while a batch is open.

Then the spec-writer writes the Change Specification in the background. On an impactful CR, the spec critic checks it afterwards and never edits it.

Nothing starts without your go."""),
 ("Grill et spécification", "Les questions qu'un changement demande, posées une à une, puis consignées dans une spécification.",
  """Le Chief of Staff, ou un Griller, pose les questions dont un changement a besoin. Chaque réponse est consignée dans la CR.

Quand vous dites « grilled enough », vous choisissez où va la CR : le prochain batch (3-ready, par défaut) ou le batch en cours, proposé seulement quand un batch est ouvert.

Ensuite le spec-writer écrit la Change Specification en arrière-plan. Sur une CR à fort impact, le spec critic la vérifie après coup et ne la modifie jamais.

Rien ne démarre sans votre feu vert."""))

add("planning_folder", "concepts", D + "planning-folder.md",
 ("Planning folder", "Where chantier writes everything, as plain Markdown and JSON.",
  """The planning folder is the only place chantier writes. Everything in it is Markdown and JSON, readable by you and by the agents.

A CR moves through its stages as folders:

- the inbox, where ideas land
- the backlog, P1 to P4
- 3-ready, the next batch
- 4-batch, with pending, active and done CRs
- then the archives

It is .agents/changes/ in your project, or the project's folder of an external planning surface."""),
 ("Dossier de planification", "L'endroit où chantier écrit tout, en Markdown et JSON simples.",
  """Le dossier de planification est le seul endroit où chantier écrit. Tout y est en Markdown et en JSON, lisible par vous et par les agents.

Une CR traverse ses étapes sous forme de dossiers :

- l'inbox, où arrivent les idées
- le backlog, de P1 à P4
- 3-ready, le prochain batch
- 4-batch, avec les CR en attente, actives et terminées
- puis les archives

C'est .agents/changes/ dans votre projet, ou le dossier du projet dans une surface de planification externe."""))

add("batch", "concepts", D + "use-cases.md#the-life-of-a-batch",
 ("Batch and slots", "A set of CRs built together, up to ready-to-merge pull requests.",
  """chantier is not continuous delivery, where one intent is one PR and one release. It is n CRs, m PRs (normally close to n), p batches, and one release.

You plan a set of CRs ahead, for instance by grilling during the day, and chantier builds the batch on its own, up to ready-to-merge PRs.

Slots are the CRs that run side by side. A CR added while the batch runs is queued and taken when a slot frees.

A batch is running, paused or closed. A batch closes on your yes, and you merge the pull requests yourself."""),
 ("Batch et slots", "Un ensemble de CR construites ensemble, jusqu'à des pull requests prêtes à fusionner.",
  """chantier n'est pas de la livraison continue, où une intention donne une PR et une release. C'est n CR, m PR (normalement proche de n), p batchs, et une release.

Vous planifiez un ensemble de CR à l'avance, par exemple en grillant pendant la journée, et chantier construit le batch seul, jusqu'à des PR prêtes à fusionner.

Les slots sont les CR qui tournent côte à côte. Une CR ajoutée pendant que le batch tourne est mise en file et prise quand un slot se libère.

Un batch est en cours, en pause ou clos. Il se clôt sur votre accord, et vous fusionnez les pull requests vous-même."""))

add("cr_lifecycle", "concepts", R + "#detailed-lifecycle",
 ("A CR's life", "From planning to archive: study, implementation, QA and release.",
  """A CR is carried through planning, study, implementation, QA, deployment and finally archive.

- Planning is mainly with the Chief of Staff.
- The central implementation loop delegates to Drivers, with strict reviews.
- A QA loop lets a validation agent act like a user, to check what the integration and end-to-end tests do not.
- The release runs with supervised auto-merge, and can monitor the deployment, to production, to package registries or to documentation pages.

Each step has an agent that acts, and several files, mostly Markdown, are added to the CR's folder along the way."""),
 ("La vie d'une CR", "De la planification à l'archive : étude, implémentation, QA et release.",
  """Une CR est portée à travers la planification, l'étude, l'implémentation, la QA, le déploiement et enfin l'archive.

- La planification se fait surtout avec le Chief of Staff.
- La boucle d'implémentation centrale délègue à des Drivers, avec des revues strictes.
- Une boucle de QA laisse un agent de validation agir comme un utilisateur, pour vérifier ce que l'intégration et les tests de bout en bout ne couvrent pas.
- La release se fait avec une fusion automatique supervisée, et peut surveiller le déploiement, en production, sur les registres de paquets ou sur les pages de documentation.

Chaque étape a un agent qui agit, et plusieurs fichiers, surtout en Markdown, s'ajoutent au dossier de la CR en chemin."""))

add("planning_modes", "concepts", D + "planning-modes.md",
 ("Planning modes", "Plan inside your project, or in a repository of its own.",
  """Chantier plans in one of two places.

- In-project, the default, with nothing to declare: .agents/changes/ in your project.
- External: a git repository of its own, the planning surface, with one folder per project. Your project's repository gets only the code and, if you want, each CR's cleaned archive in its PR.

The Chief of Staff, the Foreman and the Griller run on the default branch: your project's main checkout in-project, the surface's checkout in external mode. Only the code gets worktrees, one per CR, in your project.

In a planning surface, the surface server commits and pushes the plan."""),
 ("Modes de planification", "Planifier dans votre projet, ou dans un dépôt à part.",
  """Chantier planifie à l'un de deux endroits.

- Dans le projet, par défaut, sans rien à déclarer : .agents/changes/ dans votre projet.
- Externe : un dépôt git à part, la surface de planification, avec un dossier par projet. Le dépôt de votre projet ne reçoit que le code et, si vous le voulez, l'archive nettoyée de chaque CR dans sa PR.

Le Chief of Staff, le Foreman et le Griller travaillent sur la branche par défaut : le checkout principal de votre projet en mode projet, celui de la surface en mode externe. Seul le code a des worktrees, un par CR, dans votre projet.

Dans une surface de planification, le serveur de la surface commit et pousse le plan."""))

add("steering", "concepts", D + "use-cases.md#choose-your-configuration",
 ("Direct or Foreman", "Who steers the batch: the Chief of Staff itself, or a nested Foreman session.",
  """In direct mode the Chief of Staff steers the batch itself. In Foreman mode a nested Foreman session steers it.

The mode follows where you are: Foreman at the desktop, direct from the phone under Remote Control, or in a terminal or VS Code. Saying foreman or direct forces one.

In both modes a CR added while the batch runs is queued and taken when a slot frees.

Direct mode is simpler to use remotely. In Foreman mode the Chief of Staff stays free to grill while the Foreman runs the batch. In direct mode it holds no grill while a batch runs: open a Griller session instead."""),
 ("Direct ou Foreman", "Qui pilote le batch : le Chief of Staff lui-même, ou une session Foreman imbriquée.",
  """En mode direct, le Chief of Staff pilote le batch lui-même. En mode Foreman, une session Foreman imbriquée le pilote.

Le mode suit l'endroit où vous êtes : Foreman au poste de travail, direct depuis le téléphone sous Remote Control, ou dans un terminal ou VS Code. Dire foreman ou direct en force un.

Dans les deux modes, une CR ajoutée pendant que le batch tourne est mise en file et prise quand un slot se libère.

Le mode direct est plus simple à distance. En mode Foreman, le Chief of Staff reste libre de grill pendant que le Foreman mène le batch. En mode direct, il ne grille pas tant qu'un batch tourne : ouvrez plutôt une session Griller."""))

add("batch_modes", "concepts", R + "#batch-modes",
 ("Batch modes", "Parallel, series or stack: how a batch's pull requests relate.",
  """A batch has one of three modes. They say how the PRs relate, and who merges what, when. You merge, never chantier.

- Parallel, the default: every CR starts from the default branch at once. You merge in the order PRs become ready; after each merge the others are rebased.
- Series: the CRs have the order you gave. The next one starts once the previous is handed back, and its PR is a draft until the previous merges.
- Stack: parallel, with a stack driver that makes one native stack of PRs on the forge.

A CR that depends on another (depends.json) waits for it in every mode. A running batch can switch mode on request."""),
 ("Modes de batch", "Parallèle, série ou pile : comment les pull requests d'un batch se relient.",
  """Un batch a l'un de trois modes. Ils disent comment les PR se relient, et qui fusionne quoi, quand. Vous fusionnez, jamais chantier.

- Parallèle, par défaut : chaque CR part de la branche par défaut en même temps. Vous fusionnez dans l'ordre où les PR deviennent prêtes ; après chaque fusion, les autres sont rebasées.
- Série : les CR ont l'ordre que vous avez donné. La suivante démarre quand la précédente est rendue, et sa PR reste en brouillon jusqu'à la fusion de la précédente.
- Pile : du parallèle, avec un stack driver qui fait une pile native de PR sur la forge.

Une CR qui dépend d'une autre (depends.json) l'attend dans tous les modes. Un batch en cours peut changer de mode sur demande."""))

add("project_rules", "concepts", D + "agents-and-models.md",
 ("Your project's rules", "Your changes must land without chantier: your own files are the only configuration.",
  """Your changes must be able to land without chantier. chantier is there to industrialise, not to replace your rules.

Your AGENTS.md, and an optional chantier.yaml, are the only configuration. The chantier.yaml sets the agent and model of each role, and the skills it needs. It can be the project's, and its planning surface's.

Everything chantier writes is Markdown and JSON in the planning folder.

You can use your own agent for a role, or add a review step after the Inspector: say it, and the role runs it from the next batch."""),
 ("Les règles de votre projet", "Vos changements doivent pouvoir arriver sans chantier : vos propres fichiers sont la seule configuration.",
  """Vos changements doivent pouvoir arriver sans chantier. chantier est là pour industrialiser, pas pour remplacer vos règles.

Votre AGENTS.md, et un chantier.yaml facultatif, sont la seule configuration. Le chantier.yaml fixe l'agent et le modèle de chaque rôle, et les skills dont il a besoin. Il peut être celui du projet, et celui de sa surface de planification.

Tout ce que chantier écrit est en Markdown et en JSON dans le dossier de planification.

Vous pouvez utiliser votre propre agent pour un rôle, ou ajouter une étape de revue après l'Inspector : dites-le, et le rôle l'exécute dès le prochain batch."""))

add("gates", "concepts", D + "gates.md",
 ("Gates", "The fast gate and the long gate you declare in your AGENTS.md.",
  """A gate is a command that decides whether work is good enough to go on. You declare two in your AGENTS.md.

- The fast gate runs often, for example in a Coder's round.
- The long gate runs at the pushed head of a CR, by a Verifier, before the CR is handed back.

At init, the Chief of Staff checks the long gate, and proposes the exact lines to write in your AGENTS.md. It writes them on your yes.

You can change them later: say, for instance, that your long gate is npm test."""),
 ("Gates", "La gate rapide et la gate longue que vous déclarez dans votre AGENTS.md.",
  """Une gate est une commande qui décide si le travail est assez bon pour continuer. Vous en déclarez deux dans votre AGENTS.md.

- La gate rapide tourne souvent, par exemple dans le tour d'un Coder.
- La gate longue tourne sur la tête poussée d'une CR, par un Verifier, avant que la CR soit rendue.

À l'init, le Chief of Staff vérifie la gate longue et propose les lignes exactes à écrire dans votre AGENTS.md. Il les écrit sur votre accord.

Vous pouvez les changer plus tard : dites par exemple que votre gate longue est npm test."""))

add("costs", "concepts", D + "costs.md",
 ("Costs and limits", "What a batch costs, and the limits that cap it.",
  """A batch has a budget. Steering and the Drivers are most of what it spends; coding itself is a small share.

The Chief of Staff's own session is priced apart, on its own lines, and never in the budget.

To measure your own, ask "what did it cost?" or run chantier cost. It gives the spend by role, by CR, and what explains each figure.

Two limits are set on this board's Configuration page, in its Limits tab: the slots of a new batch (batch.slots), and how many CRs are specified at once (specifying.parallel)."""),
 ("Coûts et limites", "Ce que coûte un batch, et les limites qui le bornent.",
  """Un batch a un budget. Le pilotage et les Drivers en sont l'essentiel ; le code lui-même en est une petite part.

La session du Chief of Staff est comptée à part, sur ses propres lignes, et jamais dans le budget.

Pour mesurer les vôtres, demandez « what did it cost? » ou lancez chantier cost. Il donne la dépense par rôle, par CR, et ce qui explique chaque chiffre.

Deux limites se règlent sur la page Configuration de ce board, dans son onglet Limits : les slots d'un nouveau batch (batch.slots), et le nombre de CR spécifiées à la fois (specifying.parallel)."""))

add("boards", "concepts", D + "boards.md",
 ("Boards", "Three ways to watch a batch: this web board, a pane in Claude Code, a terminal view.",
  """The same record is shown three ways.

- This web board: live batches, what waits for you, the backlog and the merged CRs. It can run on your phone too, where you can triage the backlog. It is one client of the server's published API, which a script can use as well.
- A read-only pane in Claude Code, opened with /chantier-board or by loading the Chief of Staff.
- chantier live, a read-only view of a running board in your terminal.

The boards show the state; the steering session acts on it."""),
 ("Boards", "Trois façons de suivre un batch : ce board web, un volet dans Claude Code, une vue en terminal.",
  """Le même état est montré de trois façons.

- Ce board web : les batchs en direct, ce qui vous attend, le backlog et les CR fusionnées. Il peut tourner aussi sur votre téléphone, où vous pouvez trier le backlog. C'est un client de l'API publiée du serveur, qu'un script peut utiliser aussi.
- Un volet en lecture seule dans Claude Code, ouvert avec /chantier-board ou en chargeant le Chief of Staff.
- chantier live, une vue en lecture seule d'un board en marche, dans votre terminal.

Les boards montrent l'état ; la session de pilotage agit dessus."""))

# roles
add("chief_of_staff", "roles", D + "use-cases.md",
 ("Chief of Staff", "The one person you talk to, in your own session.",
  """You talk to the Chief of Staff, in your own session. It holds the seat: the one session that opens and runs batches in the repository.

It keeps the backlog, and asks the questions a change needs. Nothing starts without your go, and you merge the pull requests.

It opens a batch on your word, and in direct mode it steers the batch itself, starting the Drivers.

Its session is priced apart from the batch's budget."""),
 ("Chief of Staff", "La seule personne à qui vous parlez, dans votre propre session.",
  """Vous parlez au Chief of Staff, dans votre propre session. Il tient le siège : l'unique session qui ouvre et mène les batchs dans le dépôt.

Il tient le backlog, et pose les questions dont un changement a besoin. Rien ne démarre sans votre feu vert, et vous fusionnez les pull requests.

Il ouvre un batch sur votre parole, et en mode direct il pilote le batch lui-même, en lançant les Drivers.

Sa session est comptée à part du budget du batch."""))

add("griller", "roles", D + "use-cases.md#a-chief-of-staff-and-grillers-in-remote",
 ("Griller", "An optional session that grills beside the Chief of Staff.",
  """A Griller is an optional session of yours, started with /chantier:griller. It refines the inbox and the backlog while the Chief of Staff runs batches.

It never opens a batch. The Chief of Staff picks up what it files.

It matters most in direct mode, where the Chief of Staff, busy steering, holds no grill while a batch runs."""),
 ("Griller", "Une session facultative qui grille à côté du Chief of Staff.",
  """Un Griller est une session facultative à vous, lancée avec /chantier:griller. Il affine l'inbox et le backlog pendant que le Chief of Staff mène les batchs.

Il n'ouvre jamais de batch. Le Chief of Staff reprend ce qu'il dépose.

Il compte surtout en mode direct, où le Chief of Staff, occupé à piloter, ne grille pas tant qu'un batch tourne."""))

add("foreman", "roles", D + "use-cases-foreman.md",
 ("Foreman", "A nested session that steers a batch, so the Chief of Staff stays free.",
  """In Foreman mode, a nested Foreman session steers each batch. It starts the Drivers and follows the batch.

Your Chief of Staff stays free for a natural, dynamic conversation while the batch runs, so you can grill future topics with it.

The Foreman is the default at the desktop. From the phone, a terminal or VS Code, direct mode is used instead, unless you ask for foreman."""),
 ("Foreman", "Une session imbriquée qui pilote un batch, pour que le Chief of Staff reste libre.",
  """En mode Foreman, une session Foreman imbriquée pilote chaque batch. Elle lance les Drivers et suit le batch.

Votre Chief of Staff reste libre pour une conversation naturelle et dynamique pendant que le batch tourne : vous pouvez grill les sujets à venir avec lui.

Le Foreman est le choix par défaut au poste de travail. Depuis le téléphone, un terminal ou VS Code, le mode direct est utilisé, sauf si vous demandez foreman."""))

add("driver", "roles", D + "agents-and-models.md",
 ("Driver", "Runs one CR in its own worktree, up to a pull request handed back ready.",
  """A Driver, or CR driver, takes one CR to completion. It works in the CR's own git worktree, in your project.

It delegates to short workers: the Investigator, Coder, Inspector, Verifier and Debugger, any of which can be your own agent. Its reviews are strict.

It ends when the pull request is handed back ready to merge. The Foreman, or the Chief of Staff in direct mode, starts the Drivers."""),
 ("Driver", "Mène une CR dans son propre worktree, jusqu'à une pull request rendue prête.",
  """Un Driver, ou CR driver, mène une CR jusqu'au bout. Il travaille dans le worktree git propre à la CR, dans votre projet.

Il délègue à des workers courts : l'Investigator, le Coder, l'Inspector, le Verifier et le Debugger, dont chacun peut être votre propre agent. Ses revues sont strictes.

Il termine quand la pull request est rendue prête à fusionner. Le Foreman, ou le Chief of Staff en mode direct, lance les Drivers."""))

add("spec_writer", "roles", D + "use-cases.md#turn-ideas-into-ready-work",
 ("Spec-writer and spec critic", "One writes the Change Specification, the other checks it.",
  """The spec-writer writes the Change Specification in the background, once you say a CR is grilled enough.

On an impactful CR, the spec critic checks the specification afterwards. It never edits it.

Both are agents of the Chief of Staff or the Griller: you are not asked to wait for them, and the batch's Drivers start from the specification they leave."""),
 ("Spec-writer et spec critic", "L'un écrit la Change Specification, l'autre la vérifie.",
  """Le spec-writer écrit la Change Specification en arrière-plan, dès que vous dites qu'une CR est grilled enough.

Sur une CR à fort impact, le spec critic vérifie ensuite la spécification. Il ne la modifie jamais.

Tous deux sont des agents du Chief of Staff ou du Griller : on ne vous demande pas de les attendre, et les Drivers du batch partent de la spécification qu'ils laissent."""))

add("investigator", "roles", D + "agents-and-models.md",
 ("Investigator", "Optional: maps unfamiliar code before the first round.",
  """The Investigator is optional. When the code is unfamiliar, it maps it before round 1.

It is one of the short workers the CR driver runs. Like the others, it can be your own agent.

It reads and maps; it does not change the code."""),
 ("Investigator", "Facultatif : cartographie un code inconnu avant le premier tour.",
  """L'Investigator est facultatif. Quand le code est inconnu, il le cartographie avant le tour 1.

C'est l'un des workers courts que lance le CR driver. Comme les autres, il peut être votre propre agent.

Il lit et cartographie ; il ne modifie pas le code."""))

add("coder", "roles", D + "agents-and-models.md",
 ("Coder", "Writes the code of a round and runs the fast gate.",
  """The Coder writes the code of a round of a CR, in the CR's worktree, and runs your fast gate.

It is a short worker the CR driver starts. You can name your own agent for it, for instance a language specialist: say "use my rust-coder as the coder".

If a Coder runs into trouble, a new one can start on the role's escalation model."""),
 ("Coder", "Écrit le code d'un tour et lance la gate rapide.",
  """Le Coder écrit le code d'un tour d'une CR, dans le worktree de la CR, et lance votre gate rapide.

C'est un worker court que démarre le CR driver. Vous pouvez désigner votre propre agent, par exemple un spécialiste du langage : dites « use my rust-coder as the coder ».

Si un Coder rencontre un problème, un nouveau peut repartir sur le modèle d'escalation du rôle."""))

add("inspector", "roles", D + "agents-and-models.md",
 ("Inspector", "Reviews each round, reading the diff before the commit.",
  """The Inspector reviews each round, and reads the diff before the commit.

Your own extra review steps run after it: say "add a security review with sec-reviewer" and the Driver runs it after the Inspector.

Like the other workers, the Inspector can be your own agent."""),
 ("Inspector", "Relit chaque tour, en lisant le diff avant le commit.",
  """L'Inspector relit chaque tour, et lit le diff avant le commit.

Vos propres étapes de revue supplémentaires passent après lui : dites « add a security review with sec-reviewer » et le Driver l'exécute après l'Inspector.

Comme les autres workers, l'Inspector peut être votre propre agent."""))

add("verifier", "roles", D + "gates.md",
 ("Verifier", "Runs the long gate at the pushed head before a CR is handed back.",
  """The Verifier runs your long gate at the pushed head of a CR, before the CR is handed back. A CR is not ready until the Verifier says it is verified.

The Verifier's cost is a large part of a parallel batch, since each rebase can ask for a new verification.

It can be your own agent."""),
 ("Verifier", "Lance la gate longue sur la tête poussée avant qu'une CR soit rendue.",
  """Le Verifier lance votre gate longue sur la tête poussée d'une CR, avant que la CR soit rendue. Une CR n'est pas prête tant que le Verifier ne la déclare pas vérifiée.

Le coût des Verifiers pèse lourd dans un batch parallèle, puisque chaque rebase peut demander une nouvelle vérification.

Il peut être votre propre agent."""))

add("debugger", "roles", D + "agents-and-models.md",
 ("Debugger", "A short worker that finds why something fails.",
  """The Debugger is a short worker the CR driver runs, and it can be your own agent.

It is one of the three roles that carry an escalation: the model a new agent of that role starts on after a named trouble. The other two are the Coder and the conflict resolver. The escalation model is Opus by default, and is set per role in the configuration.

Its default model is the same as the Verifier's."""),
 ("Debugger", "Un worker court qui trouve pourquoi quelque chose échoue.",
  """Le Debugger est un worker court que lance le CR driver, et il peut être votre propre agent.

C'est l'un des trois rôles qui portent une escalation : le modèle sur lequel démarre un nouvel agent de ce rôle après un problème nommé. Les deux autres sont le Coder et le conflict resolver. Le modèle d'escalation est Opus par défaut, et se règle par rôle dans la configuration.

Son modèle par défaut est le même que celui du Verifier."""))

add("conflict_resolver", "roles", None,
 ("Conflict resolver", "Settles the conflicts of a rebase.",
  """The conflict resolver is a worker that settles a rebase's conflicts. The CR driver and the stack driver can both run it.

After each merge, in parallel mode, every PR still open is rebased onto the default branch, conflict or not. That is where this worker is called, so it adds to the cost of a parallel batch."""),
 ("Conflict resolver", "Règle les conflits d'un rebase.",
  """Le conflict resolver est un worker qui règle les conflits d'un rebase. Le CR driver et le stack driver peuvent tous deux le lancer.

Après chaque fusion, en mode parallèle, chaque PR encore ouverte est rebasée sur la branche par défaut, avec ou sans conflit. C'est là que ce worker est appelé, et il pèse donc sur le coût d'un batch parallèle."""))

add("stack_driver", "roles", R + "#batch-modes",
 ("Stack driver", "In stack mode, builds the native stack on the forge and restacks it.",
  """In stack mode, the stack driver is responsible for the PR stacks. As soon as two PRs are handed back ready, it makes one native stack on the forge, and the CRs started afterwards are built on it. This is for GitHub, with the gh stack extension.

When a change is inserted into a stack ready to merge, it sends the PRs above back to draft, restacks, and verifies the stack before they turn ready again."""),
 ("Stack driver", "En mode pile, construit la pile native sur la forge et la restack.",
  """En mode pile, le stack driver est responsable des piles de PR. Dès que deux PR sont rendues prêtes, il fait une pile native sur la forge, et les CR lancées ensuite se construisent dessus. C'est pour GitHub, avec l'extension gh stack.

Quand un changement est inséré dans une pile prête à fusionner, il renvoie en brouillon les PR au-dessus, restack, et vérifie la pile avant qu'elles redeviennent prêtes."""))

add("release_driver", "roles", R + "#releases",
 ("Release driver", "Runs a release CR by your project's own procedure.",
  """A release is a CR like the others. The Release driver runs it by your project's own release procedure, from your "release" to the archive.

You approve each irreversible action, or say "auto".

A procedure ranges from a simple package publish to a long one, with a release, its notes, a pipeline to follow and an announcement. It stays written and maintained in your project, and a retro improves it."""),
 ("Release driver", "Mène une CR de release selon la procédure propre à votre projet.",
  """Une release est une CR comme les autres. Le Release driver la mène selon la procédure de release propre à votre projet, de votre « release » jusqu'à l'archive.

Vous approuvez chaque action irréversible, ou vous dites « auto ».

Une procédure va d'une simple publication de paquet à une longue, avec une release, ses notes, un pipeline à suivre et une annonce. Elle reste écrite et maintenue dans votre projet, et une rétro l'améliore."""))


def body(s):
    s = s.replace("\n", "\\n")
    if "'" in s and '"' not in s:
        return '"' + s + '"'
    return "'" + s.replace("'", "\\'") + "'"

ids = []
for i, g, doc, en, fr in T:
    ids.append((i, g, doc))
    assert len(en[2].split()) <= 150, (i, len(en[2].split()))
    assert len(fr[2].split()) <= 175, (i, 'fr', len(fr[2].split()))

def write(path, head, intro, concepts, roles, close, more, idx):
    lines = [head, "export default {"]
    lines.append(f"  'help.intro': {body(intro)},")
    lines.append(f"  'help.concepts': {body(concepts)},")
    lines.append(f"  'help.roles': {body(roles)},")
    lines.append(f"  'help.close': {body(close)},")
    lines.append(f"  'help.read_more': {body(more)},")
    for t in T:
        d = t[3 + idx]
        for k, v in zip(("name", "line", "body"), d):
            lines.append(f"  'help.{t[0]}.{k}': {body(v)},")
    lines.append("};")
    open(WEB + path, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")

write("i18n/en-help.js",
 "// English words of the Help page: its intro and headings, then each topic's name, one-line summary and\n// body (plain text, paragraphs split by a blank line, a list as lines starting with `- `).\n// Merged into en.js.",
 "chantier in a few cards: its concepts and the roles of its agents. Click a card for more.",
 "Concepts", "Roles", "Close", "Read more", 0)
write("i18n/fr-help.js",
 "// Mots français de la page Aide : son intro et ses titres, puis, par sujet, son nom, sa phrase et son\n// texte (texte simple, paragraphes séparés par une ligne vide, une liste en lignes commençant par `- `).\n// Fusionné dans fr.js.",
 "chantier en quelques cartes : ses concepts et les rôles de ses agents. Cliquez une carte pour en savoir plus.",
 "Concepts", "Rôles", "Fermer", "En savoir plus (page en anglais)", 1)

tl = ["// The Help page's topics, in display order: each its id (the address's `h=`), its group and the page of",
      "// chantier's documentation it links (null: none). Data only: every word is in i18n/en-help.js and",
      "// fr-help.js, as `help.<id>.name`, `.line` and `.body`.",
      "", "export const TOPICS = ["]
for i, g, doc in ids:
    d = "null" if doc is None else "'" + doc + "'"
    tl.append(f"  {{ id: '{i}', group: '{g}', doc: {d} }},")
tl += ["];", "", "export const topicIds = () => TOPICS.map((t) => t.id);", ""]
open(WEB + "views/help-topics.js", "w", encoding="utf-8", newline="\n").write("\n".join(tl))
print(len(T))

# Boot mode by surface, and README rework

When: after the v0.9.0 release (user, 2026-11-12).

## The user's request, verbatim (French)

> Met une CR après la release:
> /chantier:chief-of-staff: en local déclenche le mode foreman, en remote déclenche le mode direct.
> Puis il y a 2 alias : foreman ou direct pour forcer l'un ou l'autre. Ça impacte le readme, la doc,...
>
> Dans how chantier works:
> - dire que tout commence par une nouvelle session et un appel d'un skill unique de boot /chantier:chief-of-staff ( donc avec ou sans argument)
>
> Dans planing modes:
> - "chantier plans ...": commencer par "Chantier work on Change Request, a folder with markdown files, describing what you want. This starts by an 'intent', written manually, extracted from Jira or GitHub/GitLab issue ... and the Chief of Staff will help you turn it into a Change Specification. Chantier plans in two ...."
>
> Dans batch modes:
> - démarrer par expliquer pourquoi: Chantier is meant to work a bunch of Changes and ensure they are delivered in coordination. Most of the time you plan ahead a set of CR and build a Batch. For instance, you grill the day and have Chantier implements the whole batch in autonomy the night, up to a ready-to-merge PR/MR stack.
>
> A batch has one of three....
>
> ---
>
> Dans la partie Release il manque un peu de soulignage que le processus de release peut être plus ou moins complexe, d'une simple de publication de package sur pypi ou nodejs à une procédure plus complexe. Le Release Driver et le Chief of Staff vont s'arranger pour suivre votre process.
>
> Il faut donner l'exemple d'un projet publiant sur github pages, et sur un marketplace: la procédure peut créer la release, la release notes, mette en revue pour validation, puis suivre l'exécution de la pipeline de release, puis attendre la publication sur le marketplace (10 min sur vscode), publié la release notes et publier le thread Twitter d'annonce. A la fin il fait une rétro pour améliorer la procédure qui dans tous les cas reste écrite et maintenu dans votre projet.
>
> Enlève la partie repo layout et la partie "what is chantier" à déplacer dans CONTRIBUTING.md

## Summary (English)

1. **Mode by surface.** `/chantier:chief-of-staff` with no argument starts Foreman mode in a local
   session and direct mode under Remote Control. Two arguments force one: `foreman` or `direct`.
   Update the README, the docs and the cards to match.
2. **README, "How chantier works":** everything starts with a new session and one boot skill,
   `/chantier:chief-of-staff`, with or without an argument.
3. **README, "Planning modes":** open with: "Chantier works on Change Requests, a folder of
   Markdown files describing what you want. It starts from an intent, written by hand or taken
   from a Jira, GitHub or GitLab issue, and the Chief of Staff helps you turn it into a Change
   Specification. Chantier plans in two …"
4. **README, "Batch modes":** open with why: "Chantier is meant to work a set of changes and
   deliver them in coordination. Most of the time you plan a set of CRs ahead and build a batch:
   for instance you grill during the day and chantier implements the whole batch on its own
   overnight, up to a ready-to-merge PR/MR stack. A batch has one of three …"
5. **README, "Release":** stress that a release procedure ranges from a simple package publish
   (PyPI, npm) to a long procedure, and that the Release Driver and the Chief of Staff follow the
   project's own. Give the example of a project publishing to GitHub Pages and a marketplace:
   create the release and its notes, put them up for review, follow the release pipeline, wait
   for the marketplace to publish (about 10 min on the VS Code marketplace), publish the release
   notes and the announcement thread on X/Twitter, then a retro that improves the procedure,
   which stays written and maintained in the project.
6. **README:** remove "Repository layout" and "What is chantier?"; move them to CONTRIBUTING.md.
   (This reverses the readme-reorg decision, CR-195, that kept "What is chantier?" in the README.)

## Addition (user, 2026-11-12): the board mod

> je vais t'envoyer des screenshots du mod que tu pourras mettre dans la CR sur le README, tu en
> profiteras pour ameliorer la doc sur comment fonctionne le mod et ce que c'est et comment le
> declencher. tu utiliseras cette capture pour illustrer. Met une section dans le README qui
> contient 1 screenshot et le pointeur vers la page plus riche

7. **README, a new board-mod section:** one screenshot (`screenshots/board-mod-batch.png`: the "CR
   board" pane, batch-01 with 3 CRs working and 2 queued) and a link to a richer docs page.
8. **Docs, the board mod page:** what the mod is, how it works, and how to open it
   (`/chantier-board`), illustrated with the screenshots in `intake/screenshots/`. The user sends
   more screenshots; each one goes in that folder.

Screenshots so far:

- `board-mod-batch.png`: dark theme, batch-01 just opened, 3 CRs working round 1/3, 2 queued, no PR
  or cost yet.
- `board-mod-batch-prs-light.png` (user: "nouvelle capture avec les couts et PR et theme clair"):
  light theme, batch-01 at $0.57 of $20, 3 CRs in CI with their PRs (#1 to #3) and costs.
- `board-mod-waiting-light.png` (user: "une autre screenshot"): light theme, "3 waiting for you",
  1 unread ask, 2 CRs ready (Notify) in "Waiting for you", 1 in CI, 2 queued, slots 1/3.
- `board-mod-merged-light.png` (user: "une autre screenshot a garder"): light theme, 3 live,
  "1 waiting for you" while the table says "Nothing waits for you" (the unread ask counts in the
  header), slots 3/3, CR-101 in CI round 2, CR-104 round 2, CR-105 round 1, and "Merged (2 of 2)"
  open with CR-102 and CR-103.

- `direct-mode-session.png`: the whole desktop window of a direct-mode session: the Chief of Staff's
  transcript (hand-backs, a merge, an Auto-fix event it leaves to the CR's Driver), its plan, the
  Background tasks pane with the 3 Drivers and a Verifier run straight from this session, and the
  CR board pane. The user: "une autre ou on voit bien le mode direct ou les drivers sont
  directement piloté par la session en cours en mode "direct". Pendant l execution, le Chief of
  Staff refusera de griller des nouvelle requete avec vous et vous invitera passer par une autre
  session "Griller"".

- `board-mod-batch-done.png` (user: "screenshot apres que le batch soit fini"): 0 live, batch-01 at
  $9.22 of $20, "Merged (5 of 5)" with each CR's PR and cost ($0.96 to $3.32).

- `status-report-done.png` (user: "sortie detaillee sur "status" ou "/chantier:status""): the
  Chief of Staff's answer to "status" once the batch is done: the CR table (result, PR, rounds,
  cost), the notes, the cost by role with the orchestration share, the spend outside the batch and
  the cost notes. It illustrates what "status" or `/chantier:status` gives.

9. **README, "Batch modes" (direct):** illustrate direct mode with `direct-mode-session.png`: the
   Drivers run straight from the current session. Say that while the batch runs, the Chief of
   Staff in direct mode declines to grill new requests and points the user to a separate Griller
   session (`/chantier:griller`).

Notes for the docs page (Chief of Staff): the header's "waiting for you" counts the unread asks
too, not only the table's rows; the batch cost stayed at $0.57 across the last three screenshots
while the CRs moved on, then showed $9.22 once the batch was done: the batch's cost is priced
when the steering session refreshes it, not live (to explain on the docs page).

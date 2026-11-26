# What chantier does with a ticket, from first reading to release

Encode what chantier has to do with a ticket, from the first analysis to the release.

The user's words (French, 2026-11-27, to a Griller session): "rajoute en P2 une nouvelle idee: il faudrait que l'on encode les choses a faire avec un ticket :

* apres une premiere phase d'analyse il faut dire que l'on a compris en le reformulant et en donnant suctinctivement
* la PR doit contenir la reference avec le verbe "Closes #123" (pour github out gitlab, ou l'equivalent pour d'autre systeme de ticket)
* apres implementation, déclarer ou le ticket a été implementé (le ou les PR)
* au moment de la release, apres que la release soit faite, le release driver doit trouver les tickets livrés et les annotés avec un "Released in version xxx" avec le lien.

C'est toi le chief of staff qui doit faire ces actions. avant tu dois montrer le message que tu veux envoyer verbatim à l'utilisateur et lui demander s'il est d'accord."

Read:

- After a first analysis, post on the ticket what was understood, rephrased, briefly (the sentence stops before naming what is given briefly).
- The PR carries the reference with a closing verb: "Closes #123" on GitHub or GitLab, the equivalent on another ticket system.
- After implementation, declare on the ticket where it was implemented: the PR or PRs.
- After a release is made, the Release driver finds the tickets it delivered and annotates them "Released in version xxx", with the link.
- The Chief of Staff does these actions; before posting, it shows the message verbatim to the user and asks for their agreement.

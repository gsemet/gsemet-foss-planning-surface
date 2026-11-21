Short name: `fp-cache`

# Answers
1. fp-cache-Q1 (2026-11-21): **Scope.** Not answered: "Recharge les instruction il tenmanque le context obligatoire je ne comprend pas" (the series lacked the CR's name in a context line and was written in jargon). Asked again as fp-cache-Q3.
2. fp-cache-Q2 (2026-11-21): **Proof.** Not answered: "Je ne sais pas". Asked again as fp-cache-Q4.
3. fp-cache-Q3 (2026-11-21): **What to fix.** Other: "C'est maintenant le serveur d'état qui doit lire les texte, plus la board. La board ne lit que l'api. Le server d'état peut s'enregistrer sur les update de inode ou ping toutes les 5s si pas possible". The surface server reads the planning files; the web board reads only the published API. The server learns of changes from the file system's change notifications; where those are not available, it checks every 5 s.
4. fp-cache-Q4 (2026-11-21): **Proof.** A. An automatic test plus a before/after measure in the PR.

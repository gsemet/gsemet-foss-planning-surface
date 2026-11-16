# Answers

## 2026-11-13, to the Chief of Staff

- "Ce n'est pas la première fois. Quand le chief of staff se lance il faut qu'il fasse une
  vérification des permissions sur GitHub (le cas échéant sur GitLab quand le projet est sur
  GitLab)."
- Restated: at its start, the Chief of Staff checks the forge permissions the batch needs, on
  GitHub, or on GitLab for a GitLab project.

## 2026-11-13, a missing right: warn or block?

- Warn, never block: the Chief of Staff alerts the user that the permissions may stop the
  batch from running unattended, and gives advice on what to allow.
- On Claude Code, the alert says in detail that the auto mode classifier refuses some force
  pushes, and that these come with rebases (a Driver after a rebase, the stack driver's
  restack).
- The rule is general, for every host, since we do not know whether other coding agents have
  the same problem: a CR's branches must be force-pushable at all times. The general rule
  belongs in the cards that all hosts read.
- How to do it on Claude Code (the allow rules, and the forms that match what the agents
  actually run) goes in the host's own file, `hosts/claude-code.md`.

## 2026-11-13, restatement accepted

- "ok pour l'alerte, à mettre en P1 après": the restatement is accepted; P1, for the batch after
  batch-15.

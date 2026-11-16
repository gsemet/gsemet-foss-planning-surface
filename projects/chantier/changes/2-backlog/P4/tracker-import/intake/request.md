Upstream tickets come into the inbox by a setting in `chantier.yaml`, per tracker.

The user (2026-11-13): "il faudra une config pour dire quoi faire sur les tickets upstream: github/gitlab c'est souvent synchroniser tous les ouverts on/off, mais sur jira il faudra une petite jql pour selectionner les tickets a mettre en inbox."

- GitHub and GitLab: one switch, "every open issue goes to the inbox", on or off (maybe a label filter).
- Jira: a JQL query that selects the tickets to put in the inbox.
- A ticket already filed (same link) is not filed twice; a ticket closed upstream is reported, not dropped silently.

Open points for the grill:
- Who runs the import: the Chief of Staff with the tools the session has (Jira's access method is not fixed, as the ticket card says), or the agentless launch of the planning surface (`gh`/`glab` only, no Jira credentials in the CLI).
- When: on request, at session start, or in the surface's sync.

## The ticket's parent, read only (decided 2026-11-13)

chantier is tactical; Jira and GitHub or GitLab issues are strategic and outside it. The user:
"ça reste dans l'optique Chantier = tactique, jira/github issues = stratégiques/extérieurs".
So chantier owns no objective and gives none a lifecycle (no "we rebuild Jira"):

- At import, the CR's intake records its ticket's parent as the tracker gives it (title and
  link): the Jira epic (or initiative), the GitHub parent issue (sub-issues) or milestone, the
  GitLab epic or milestone. Read from the tracker, never edited by chantier.
- Nothing shows it in this CR: the user (2026-11-13) "garde juste les infos dans l'intake du
  CR, on les affichera plus tard". Grouping by parent on the board is a later item.
- Without a tracker there is no objective: priorities P1 to P3 stay the only order.

# A playbook and a finer configuration of chantier

The user: "En inbox tu rajouteras une CR que l'on fera plus tard: playbook et configuration fine de
chantier (ajd: autodetection depuis AGENTS.md), pour des configurations un peu plus avancée ou pour
amener des drivers il faudra une manière que le chief of staff trouve sans ambiguïté les skills et
agents interessant. Pareil les modèles à utiliser pour le dev ajd c'est hardcodé mais si les gens
veulent utiliser un autre, sans devoir déclarer des agent custom. Et aussi si certains tools ou
skill sont nécessaire par exemple si je dois passer par un skill pour me connecter à Jira ,…"

Three needs:

- The Chief of Staff finds the skills and agents worth using with no ambiguity, a user's own
  Drivers included.
- A project picks the models a role runs, with no custom agent: they are in each agent's frontmatter
  today.
- A project declares the tools or skills a role needs, e.g. a skill to reach Jira.

To grill: `AGENTS.md` says the user's `AGENTS.md` is the only configuration and the plugin needs no
setup; a playbook has to keep that, or change it on the user's word. Whether a host lets a start
override an agent's model decides how the second need is met.

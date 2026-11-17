Short name: `uc-diagrams`

# Answers

## 2026-11-17, owner

Questions asked in the Chief of Staff session with a recommendation each; the owner answered "Ok pour tout", then "Tu peux lancer tout ce que tu m'as dis, avec le foreman réutilisé et finissant sur une stack de PR". Every recommendation is taken:

1. uc-diagrams-Q1: **Diagram kind.** Chosen per StRS by what explains it best: a sequence diagram by default (writer, preview, VS Code, file), an actors diagram when several roles take part, a state diagram for a mode (edit on/off).
2. uc-diagrams-Q2: **Site rendering.** Pre-rendered to SVG at site build time, not in the reader's browser: light page, works without JavaScript, rendering checked by a test.
3. uc-diagrams-Q3: **Theme.** The SVG follows the site's light or dark mode: two variants rendered at build time.
4. uc-diagrams-Q4: **Mandatory or not.** The section stays optional in this CR; it becomes mandatory for every in-force StRS, with a check, once the six req-garden CRs are done (not in this CR).
5. **Way:** launched without the owner reviewing the specification ("lance tout"): a short specification the owner does not review. Spec critic: yes, it changes what the published site shows.

## 2026-11-17, owner (open questions of the specification; critic: 3 points, 2 fixed without the owner, 1 question)

6. uc-diagrams-Q5: **Dark variant.** A. Cream variant only (recommended). The theme stays a parameter of the renderer. Corrects uc-diagrams-Q3, which rested on the Chief of Staff's wrong belief that the site has a dark mode (CORE-086 forbids it).
7. uc-diagrams-Q6: **A diagram that fails to render.** A. The site build fails with the StRS id and Mermaid's message.
8. uc-diagrams-Q7: **No SwRS IDs in a diagram.** A. Yes, one sentence in the guideline: the diagram speaks of actors.
9. uc-diagrams-Q8: **Clipped labels.** A. Accept the risk; check one flowchart and one state diagram on the CI-built site before merge; the label decision stays with backlog mermaid-svg-text-labels.

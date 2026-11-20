Short name: `diff-view`

# Answers

## Series 1, 2026-11-20

Questions asked (diff-view-Q1 to Q4: direction, scroll sync from a diff, "Open Preview to Side"
from the replace preview, Studio's title button on a diff), not answered one by one: the owner
answered with a decision instead.

1. **Decision: set aside in P3, merged into `open-at-line-marker`**, 2026-11-20. Owner's words:
   "ok on laisse tomber en P3 avec un gros caveat, que ca implique de remplacer l'editeur de text
   pour les md et ca risque de poser des pbl. a tester en meme temps que la CR sur l'ouverture a
   la ligne. merge d'ailleur les 2 demandes dans le meme CR. met aussi tous tes resultat
   d'analyse dans le dossier". So: one CR with open-at-line-marker; the big caveat is that
   open-at-line's design makes Studio replace the text editor for `.md` files, which may break
   today's good behaviour in the diff views (every diff is VS Code's text diff today, see
   `work/01-findings.md`); the diff views are tested with that CR. All analysis results are kept
   in the CR's folder.

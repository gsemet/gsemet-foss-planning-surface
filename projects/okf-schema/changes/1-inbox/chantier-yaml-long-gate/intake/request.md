# chore: declare the long gate in chantier.yaml

Commit the root chantier.yaml that declares the long gate, written uncommitted in the main checkout on 2026-11-25 on the user's yes:

long_gate:
  commands:
    preflight: just preflight

Until this change merges, a pull request that adds or changes the root chantier.yaml stops the fast-forward of the main checkout after a merge.
# Intent: the Verifier checks the PR's description

2026-11-10, the user:

> il suffit juste que le verifier verifie que la description du PR soit propre et surtout
> coherente avec ce que livre le contenu de la PR

- The Verifier also checks the posted PR description. It must be:
  - clean: it renders properly on the forge;
  - consistent with what the PR's content delivers.
- The trigger: PR #93's posted description had lost all its line breaks, and nobody checked the
  description after its last edit.
- How the Verifier does it is left to the Driver and the Verifier. Not detailed here.

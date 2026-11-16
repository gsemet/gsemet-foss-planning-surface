Short name: `release-0-10`

# Answers

1. Q: Which version? — User, 2026-11-15: "0.10": v0.10.0, minor (new behaviour since v0.9.0, nothing breaking a user's setup).
2. Q: Steered by whom? — User, 2026-11-15: "en mode direct": the Chief of Staff steers, no Foreman.
3. Q: Which batch? — docs/release-process.md wants the release in the batch whose work it ships; the user closed batch-18 first ("Clôture. Puis tu fera la release"), so the release runs alone in its own batch (`--release 1`), from an up-to-date `main` (c1a60f6 or later). Its visuals come from batch-18's real run, read from its archive (`5-archives/batches/batch-18.json` and `.md`) and from `report.md` and `conversation.md` the Chief of Staff writes in this CR's folder.
4. Q: Which work do the notes cover? — Everything since v0.9.0 on `main`: every `feat:` and `fix:` commit exactly once (docs/release-process.md).
5. Q: The eval campaigns CONTRIBUTING.md asks for before a release? — User, 2026-11-15, on release-Q1 (A: the three campaigns, B: real-foreman stack only, C: none): "On a déjà fait les evals". The runs of 2026-11-15 (real-foreman run 2, stack, Foreman; real-direct run 3, parallel, direct; reports in `evals/results/`) are this release's runs; no `full` campaign and no new run. The claims file `evals/results/claims-v0.10.0.md` names those reports; each claim they did not bring (the post-eval fixes merged after them among them) is `scenario only` or `not exercised` and listed in the notes' "For contributors" bullet. The PR says that `full` did not run.
6. Q: A docs SVG diagram in the notes? — User, 2026-11-15, release-Q2: "A. Non": none.
7. Q: The grant? — Default: each irreversible step of the procedure waits for the user's approval; the user merges the version PR.

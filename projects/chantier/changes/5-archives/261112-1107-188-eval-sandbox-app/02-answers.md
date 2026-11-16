<!-- Copied from reproducible-evals/02-answers.md by the Chief of Staff, 2026-11-12: the grill's answers rule both CRs; the source stays there. -->

# Answers (grill, 2026-11-12)

- Q1 sandbox repository: https://github.com/gsemet/chantier-eval-sandbox, created by the user,
  public, `main` unprotected today. "Fais-en ce que tu veux."
- Q2 the frozen project: a Python project with uv, with CI. A web application served by a Python
  backend; the HTML written directly. No Node: only uv and hand-written HTML. The CI must be
  fast; the coding in each CR must be real without being too long.
- The application must exist before any eval, and every eval starts from a known SHA-1.
- Order of work: first a CR that builds this project in a clear, clean, working state. Then the
  evals change to start from the project.
- A scripted procedure force-pushes the sandbox back to its initial state: the evals merge PRs
  and even make releases on it, so the reset also cleans up the releases.
- A new campaign, **full**: 2 batches, 4 slots. The first batch has 9 CRs and ends with a
  release; the second has 3 CRs and also ends with a release.
- The quicker campaigns (real-foreman, real-direct) are one batch of 5 CRs, in stack, parallel
  or series mode, with no release ("sans release").
- The full campaign is complete: no human steps in. The operator plays the user (merges, gos,
  approvals); nothing waits on the real user.
- The release CR is the batch's last CR (first batch: 8 CRs + the release = 9; second: 2 + the
  release = 3), depending on all the others so it runs at the end.
- During the coding of the first batch, a tenth CR is injected (`order add`): it lands between
  the 8 others and the release. Not possible in direct mode, so full runs with a Foreman.
- The sandbox's `main` is not protected, so the reset can force-push. The force push lives in a
  clearly defined script (a named, reviewed kit command), never an ad-hoc command, so the
  classifier allows it.
- Merged PRs may stay on the sandbox. Every PR title carries the eval's run number, date and
  campaign type, so each run's PRs are told apart.
- Quick campaigns' mode: chosen at launch (`--mode stack|parallel|series`), the same 5 CRs in
  every mode, so the modes compare (the Chief of Staff's default; the user did not object).
- Grilled enough (user, 2026-11-12): "fais 1 puis 2": `eval-sandbox-app` first, then this CR.
  At the end, a review subagent on the fable model checks that every criterion of the evals is
  met and that the campaigns will work.
- Q3 and Q4 (which CRs, a hidden-test judge): left to the Chief of Staff ("fais-en ce que tu
  veux").

## Spec-writer's open questions (2026-11-12)

- Q5 `just check` rebuilds the sandbox's initial commit and compares it with `sandbox.json`: "Oui, un test" (one structure test, the same SHA-1 proved on Linux, macOS and Windows).
- Q6 the sandbox's release keeps the maintainer's approval of the notes: "Garder l'approbation" (in `full`, the operator gives it).

- Go (2026-11-12): "Go, budget 30 $": both CRs to 3-ready, one batch, series, direct mode, eval-sandbox-app first, the plugin's agents, 3 rounds per CR.

- Relayed by the parent Chief of Staff session (2026-11-12), the user's words: "Fait en autonomie maintenant plus de question": the batch runs to its two PRs without more questions; open points decided by the Chief of Staff and noted in the CR; the PRs stay unmerged for the user; no force push on chantier.

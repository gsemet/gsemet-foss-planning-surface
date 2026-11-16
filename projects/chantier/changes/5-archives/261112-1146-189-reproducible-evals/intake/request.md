Reproducible eval campaigns (user, 2026-11-12, chosen before release v0.9.0).

The real campaigns (real-foreman, real-direct) take fresh inbox items on this repository and its main of the day: two runs never measure the same thing, and their PRs are gone the next day. Only the variable under test (the plugin) should change from one run to the next.

Proposal the user agreed to (option A, before v0.9.0):
1. A frozen project: a dedicated GitHub repository (sandbox) holding a realistic fixture with real GitHub Actions CI, reset by the kit to a fixed tag before each run (main reset, open PRs closed, branches deleted). Real `gh`, real CI, same start every time.
2. Frozen CRs: a small set of already-specified CRs in the eval kit (request, answers, specification), no grill to replay; real-foreman and real-direct take the same set, so the two modes compare; copilot takes one of them.
3. A judge of the result: hidden tests per CR (like `evals/kit/contracts/`), run on each PR's head, so the audit says whether the work is right, not only whether the rails held.
4. The report names the chantier version, the base tag and the models: two reports compare line by line, costs included.
5. Dogfooding on this repository stays normal work, not an eval.
claude-planted is unchanged (fixture + local forge, already reproducible).

Then real-direct runs on the sandbox (never run yet; CR-187 changes its path), then the release v0.9.0 (release-v0-9-0 in the inbox).
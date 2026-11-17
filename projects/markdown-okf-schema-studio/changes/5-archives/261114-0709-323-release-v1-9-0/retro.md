# Retro: release v1.9.0

| What cost time | Root cause | Process fix (proposed CR) |
| --- | --- | --- |
| Open VSX step red on the version push; one recovery dispatch and a red run on `main` | The release job runs as a reusable workflow from `ci.yml`, so the Open VSX OIDC token names `ci.yml`; the trusted publisher is registered for `release.yml` only. CR-322 proved the publish only by a dispatch of `release.yml`, never by the `workflow_call` path | Owner registers `ci.yml` as a second Open VSX trusted publisher, or a CR makes the publish path match the registration; and CR-322-style changes prove the `workflow_call` path before a release |
| Two heavy runs needed a re-run (toc step on `main`, real-input on the branch) | Intermittent real-window integration steps | A CR to track and harden these two integration steps (flake log across runs) |
| Open VSX API answered 404 for about 2.5 minutes after a green publish | Registry indexing delay | None: the guideline's 10 to 15 minute watch covers it |

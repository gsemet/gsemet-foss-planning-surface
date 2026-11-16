# Intent

Each CR passes its own gates, but those miss what two CRs break together and any check skipped on
a PR. chantier imposes no release gate: the project's procedure rules. So the Chief of Staff, when
it prepares a release, asks the project to plan a long check on the exact head of the default
branch, before the version commit, if its procedure has none. This is point 6 of the field report
in `.agents/changes/1-inbox/lessons-from-studio-run/`.

This CR is also a real-tools eval of chantier on its own repository: the PR is opened on GitHub,
with real CI, and is never merged.

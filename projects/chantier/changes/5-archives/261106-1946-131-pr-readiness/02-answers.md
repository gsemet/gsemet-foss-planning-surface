# Answers

- 2026-11-06: `pr-readiness` and `stack-pr-base` are one CR.
- 2026-11-06: a Driver opens its PR as a draft, unless the project's rules say otherwise. The PR turns
  ready at hand-back if its base is the default branch; otherwise it stays a draft until the PR
  under it merges, and the stack driver turns it ready.
- Earlier, from the request: draft is an example; the project's rules rank first (a label, for
  instance). Assume nothing, read them. Works on GitHub and GitLab.

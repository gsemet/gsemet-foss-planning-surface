---
title: Grill answers, tracker issues and draft pull requests
date: 2026-11-10
---

# Grill answers

Owner's answers, 2026-11-10.

| Question | Answer |
| --- | --- |
| Approval of issue comments | The Chief of Staff drafts every issue comment (grill done, PR opened) and posts it after the owner approves its text. At release, one approval covers the whole list of "Released in <release notes>" comments. |
| Where the issue is recorded | An `issue:` line in the `01-intent.md` front matter, carried into `03-change-spec.md` and the PR body (`Fixes #N` here). |
| Draft PRs in a stack | Each PR turns ready on its own, as soon as it is mergeable itself (CI green at its head, review done), without waiting for the rest of the stack. |
| Chantier | In this CR: the generic rules also go into the Chantier repository (`/Users/az02065/Projects/DevTools/chantier`), as their own PR there. The project-specific rules (GitHub, `gh`, `Fixes #N`) stay in this project. |
| CI on drafts | Already checked: `ci.yml` runs on draft PRs (no draft filter), so no workflow change is needed. |

## Scope consequences

- Two repositories, two PRs: this project (process guideline, project guidelines, `AGENTS.md`) and
  Chantier (its generic process docs, agents or skill text that cover the grill, the PR and the
  release). The Chantier checkout is 14 commits behind its `origin/main`: start from `origin/main`.
- Process and guidelines only; no product code, no requirements change.

## Chantier issue

Opened 2026-11-10 after the owner approved the text: https://github.com/gsemet/chantier/issues/101. A dependent PR outside a stack stays a draft (owner).

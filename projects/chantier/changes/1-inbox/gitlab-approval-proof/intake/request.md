# Prove CR-409's GitLab approval read on a real GitLab project

Priority P3, later. From CR-409 (typed waits, batch-29), at its Driver's request, 2026-11-20.

CR-409 reads a merge request's approval state on GitLab (through `glab`, its GraphQL answer) for the typed waits. It is proved only against a fake `glab` (`fake_glab`) in the scenario: there is no GitLab account to prove it with. Prove the GitLab approval read on a real GitLab project: a merge request waiting for an approval, then approved, and check that the typed wait reads both states as it does on GitHub. Needs a GitLab account and project from the user.

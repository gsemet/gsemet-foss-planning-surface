Short name: `release`

# Answers

## 2026-11-26: the user asks for the release

Said after merging pull requests 70 and 73: "J'ai mergé. Fait une release".

- Version and scope are not asked: the project's procedure computes the version
  (`just bump-version`), and the release holds what is merged on `main` since `v0.18.1`.
- The user merges the version pull request. No irreversible step is approved in advance.

Spec critic: no. The specification applies the project's written procedure unchanged and decides
nothing new; the user reviews and merges the version pull request.

## 2026-11-26: the release notes are written without Copilot

The user: "Il faudra que tu fasse la release notes toi même je n' ai plus de crédit copilot".

- The release notes are written by the release work itself, not by `gh copilot`.
- The CI-started **Release** run will fail at note generation; the notes reach the GitHub release
  by the documented dispatch with `release_notes` ("Recovery and Release Notes"). That dispatch
  publishes: it still waits for the user's approval.

## Release announcement on the tickets

Standing instruction of 2026-11-25: "Oui, poster. poste les liens quand tu les as, et quanbd la
release sera faite tu postes des commentaires pour annoncer la dispo". Once the release is
published, the availability comment goes on issues 56, 57 and 58 with no further question. This
is the steering session's step, not the Release driver's.

## Why

A CR's PR is open and mergeable as soon as it exists, whatever its CI, its evidence or its base. PR 55
and PR 57, both green, were merged into another CR's branch: the forge said nothing against it.

## What

- **Ready to merge**, defined once in `concepts.md`: the CR is handed back `ready` and its base is the
  default branch. Any other CR's PR is a draft.
- **CR Driver:** opens its PR as a draft, turns it ready just before `handback ready` when its base is
  the default branch, and otherwise leaves the draft and says what it waits for in the hand-back. A
  send-back turns the PR back to a draft first.
- **Stack driver:** opens no PR, and keeps each PR it moves true to the definition.
- **Project rules first, no fallback:** a project's own way of showing it is followed as written; a
  forge that refuses a draft stops that step.
- **Report:** 🔵 to review is a ready PR only.

GitHub and GitLab commands are named alike. The CLI gains no forge command.

## Beyond the specification

- A release PR is opened ready and left as it is: it sits in the Drivers' shared section, and the
  Foreman merges it, which a forge refuses on a draft. This keeps its behaviour on `main`.
- `evals/kit/forge.py` and `audit.py` serve `pr ready` and the draft flag: the eval's fake forge refuses
  unknown calls, so a Driver following the new card would have stopped there.

## Checks

`just check` and `just scenario` pass. The scenario's fakes needed no change.

## Evidence at e997676

- `gh pr checks 69`: `just check` on Linux, macOS and Windows and `just scenario` on Linux, all pass; the long gate passed locally on Windows too.
- Each forge call is named on both forges: `driver.md` lines 35-36 (open), 44 and 99 (draft), 61 and 98 (ready).
- `git diff --stat origin/main...HEAD -- skills/chantier/scripts` is empty: the CLI is unchanged.
- `evals/kit/forge.py` on a throwaway state: `pr create --draft` gives `isDraft: true`, `pr ready` false, `pr ready --undo` true.

The change is card text and a fake forge: there is no screenshot to compare.
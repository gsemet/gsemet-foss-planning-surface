## Summary

The v0.8.0 release showed four rough edges in the release procedure. `just tag` tagged whatever sat at the head of `origin/main`, even a commit pushed after the release merge. CONTRIBUTING gave an incomplete `gh release create` command. The agent running the release asked for a go on a release PR the user had already merged. The private-data scan missed a UUID glued to a word with `_` (such as `local_<uuid>`). This PR fixes the four.

## Deliverables

- **`just tag` refuses a wrong head.** After fetching, it compares the subject of `origin/main`'s head with `release: v<local version>` and stops, with no tag and no push, when they differ:

  ```text
  just tag: origin/main is "<subject>", expected "release: v<version>"
  ```

  The check is a `check-tag` subcommand of `scripts/version.py`, so it is the same on Linux, macOS and Windows, and reads the version with the code `just version-show` uses. The recipe takes no argument.
- **CONTRIBUTING, "Release"**: step 4 says `just tag` refuses unless origin/main's head is the `release: vX.Y.Z` commit; step 5 writes `gh release create vX.Y.Z --title vX.Y.Z --verify-tag --notes-file ...`, so `gh` refuses instead of creating a tag the forge lacks.
- **Release procedure card**: a release PR the user already merged needs no release go; the agent running the release sees the merge on the forge and goes on. The tag push, the published release and the announcement keep their `release go`.
- **UUID scan**: the `uuid` pattern is bounded by hexadecimal digits instead of `\b`, so `local_<uuid>` is caught by `--scan` and `--check`.

- **Shown by hand** (throwaway clone of a local bare repository, `just tag` run from PowerShell; the same lines also run in Git Bash):

  ```text
  match    (origin/main head "release: v0.8.0"):  * [new tag] v0.8.0 -> v0.8.0   exit 0, tag on origin/main, local and remote
  mismatch (one commit after it):  just tag: origin/main is "feat: later commit", expected "release: v0.8.0"   exit 1, no tag local or remote
  ```

  `release_notes.py --scan` on a file holding `local_00000000-1111-2222-3333-444444444444` prints `a.txt:1: uuid` and exits 1; on a file without a UUID it exits 0.

## Blast radius

Grade: 1. Release tooling, one card paragraph and a regex; a plain `git revert` restores the previous behaviour.

## Autonomous decisions

- The tag check lives in `scripts/version.py` (a `check-tag` subcommand) rather than in shell, for portability across the justfile's shells.
- The specification's open question (does the user's merge also stand for the tag push) was taken as no: only the merge needs no go.

<details>
<summary>Details</summary>

## Changes

- `justfile`: `tag` runs `version.py check-tag` between the fetch and the tag.
- `scripts/version.py`: `check-tag`.
- `scripts/release_notes.py`: the `uuid` pattern.
- `CONTRIBUTING.md`: release steps 4 and 5.
- `skills/chantier/references/driver.md`: one bullet in the release section.
- `skills/chantier/scripts/cli/tests/test_structure.py`: a test that `scan_text` reports a `uuid` hit for `name_<uuid>`.

## Human decisions

- All four fixes go in one PR.
- `just tag` refuses when the head does not match; no expected-SHA argument.
- The agent running the release verifies the user's merge on the forge and goes on without asking; the user's merge is the go.

## Impacts

No visual change. Releasers see a refusal message from `just tag` on a mismatched head.

## Test plan

- [x] New or changed tests (they fail on the previous code): the UUID test
- [x] Local gates: `just check`; `just scenario`
- [x] Evidence: `just tag` in a throwaway clone (match, mismatch), `release_notes.py --scan` on files with and without a UUID
- [x] Review
- [x] CI green

## Internal references

CR-164 release-retro-v0-8-0

</details>

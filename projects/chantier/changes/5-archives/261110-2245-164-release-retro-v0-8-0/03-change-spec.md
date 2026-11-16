# Release retro v0.8.0: a safe `just tag`, the full release command, no go for the user's merge, the UUID scan

## Goal

Four fixes from the v0.8.0 release retro, in one PR:

1. `just tag` refuses unless the subject of origin/main's head is `release: v<the local version>`.
2. CONTRIBUTING writes the full `gh release create` command, with `--title vX.Y.Z` and
   `--verify-tag`.
3. The Release driver asks no release go for a merge the user already did: it sees the merge on
   the forge and goes on.
4. `scripts/release_notes.py --scan` catches a UUID right after `_` (such as `local_<uuid>`),
   with a structure test.

This CR merges five retro P1s (`just-tag-checks-head`, `release-create-full-command`,
`release-user-merge-no-go`, `release-verify-merge-commit`, `scan-uuid-after-underscore`); their
requests are in `intake/`. `release-verify-merge-commit` is covered by item 1: no separate step.

## What changes

### 1. `just tag` checks origin/main's head (`justfile`, and a script if needed)

Today the recipe fetches `origin main`, then tags `origin/main` with the version read from the
local checkout (`uv run --script scripts/version.py show`) and pushes the tag. It checks nothing:
a commit pushed to main after the release merge would get the tag.

New behaviour:

- After `git fetch origin main` and before `git tag`, read the subject of origin/main's head
  (`git log -1 --format=%s origin/main`) and the local version.
- If the subject is not exactly `release: v<version>`, refuse: print one line that names both
  (for example `just tag: origin/main is "<subject>", expected "release: v<version>"`), exit
  non-zero, create no tag and push nothing.
- Otherwise tag `origin/main` and push the tag, as today.
- No expected-SHA argument: the recipe keeps no parameter.

The recipe must run on Linux, macOS and Windows (the justfile's `windows-shell` is PowerShell),
so the comparison should not depend on one shell's syntax. Putting it in a Python script run by
`uv run --script` (for example a subcommand of `scripts/version.py`, or a small function there)
is one portable way; the Driver chooses. The version must stay read by the same code as
`just version-show`.

The subject `release: vX.Y.Z` is the one `just release` commits; a rebase merge keeps it, so the
check holds after the version PR is merged by rebase.

### 2. CONTRIBUTING's release steps (`CONTRIBUTING.md`, section "Release")

- Step 4 (`just tag`): say that it refuses unless origin/main's head is the `release: vX.Y.Z`
  commit of the local version, so a commit pushed after the merge never gets the tag. Add no
  `gh pr view --json mergeCommit` step: the check above covers it.
- Step 5: write the full command, title included:

  ```bash
  gh release create vX.Y.Z --title vX.Y.Z --verify-tag --notes-file <tmp>/release-notes.md <each file that --prepare listed>
  ```

  `--verify-tag` makes `gh` refuse when the tag `just tag` pushed is not on the forge, instead of
  creating one.

### 3. The Release driver and a merge the user already did (`skills/chantier/references/driver.md`)

In the "Release driver" section, the bullets on irreversible actions and on the release PR
(today: a release PR is the Foreman's to merge, `handback blocked merge: <pr link>`). Add, in the
card's style, that a release PR the user has already merged needs no release go: the Driver
sees the merge on the forge (`gh pr view <pr>`, or the forge's equivalent the host card names)
and goes on to the procedure's next step without asking; the user's merge is the go.

- Only the merge is concerned: every other irreversible action (the pushed tag, the published
  release, the announcement) keeps its `release go`, as the card says today.
- No CLI change: `release go` (`rails.release_go`) and `release_merged` stay as they are. The CLI
  knows no role; this is the card's judgement.
- The agent files (`agents/release-driver.md`,
  `com.github.copilot/agents/chantier-release-driver.agent.md`) name no procedure and do not
  change.

### 4. The UUID scan (`scripts/release_notes.py`)

The `uuid` entry of `FIXED` is bounded by `\b`, and `_` is a word character, so `local_<uuid>`
is missed. Bound it by hexadecimal digits instead:

```python
("uuid", re.compile(r"(?<![0-9a-fA-F])[0-9a-fA-F]{8}-(?:[0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}(?![0-9a-fA-F])")),
```

`FIXED` serves both `--scan` and `--check` (`release-notes.md` and `tweet.md`): both catch it.

Structure test, in `skills/chantier/scripts/cli/tests/test_structure.py`: load
`scripts/release_notes.py` the way `_version_script()` loads `scripts/version.py`
(`importlib.util.spec_from_file_location`), then assert that `scan_text` with `FIXED` reports a
`uuid` hit for a line holding `name_<uuid>` (a made-up UUID such as
`00000000-1111-2222-3333-444444444444`). One short test; it needs no git and no network.

## Out of scope

- An expected-SHA argument to `just tag`.
- A `gh pr view --json mergeCommit` step in CONTRIBUTING.
- Any CLI change (`rails.py`, `commands.py`), any change to `release go` or to the grant.
- `docs/release-process.md` and `release-template.md`: unchanged.
- Other private-data patterns of the scan.

## Evidence

- `just check` passes on Linux, macOS and Windows, with the new UUID test.
- `just scenario` passes (`driver.md` is a card).
- `just tag`, shown by hand in the PR (commands and output), in a throwaway clone or a branch
  whose remote is a local bare repository, never on the real origin:
  - origin/main's head subject is `release: v<version>`: the tag is created on origin/main and
    pushed;
  - origin/main has one more commit after it: refused, with the message naming both, and no
    tag exists locally or on the remote;
  - on Windows (PowerShell) and on one POSIX shell.
- `uv run --script scripts/release_notes.py --scan <file>` on a file holding `local_<uuid>`
  exits 1 and prints a `uuid` line; on a file without one it exits 0.
- The diff of `driver.md` and `CONTRIBUTING.md` shows the points above, nothing else.

## Open questions

1. Item 3 says the Driver "goes on to the next step without asking". This specification keeps
   the release go of every other irreversible action (the next step is usually the tag push,
   which still asks unless the grant covers it). Is that the intent, or should the user's merge
   also stand for the tag?

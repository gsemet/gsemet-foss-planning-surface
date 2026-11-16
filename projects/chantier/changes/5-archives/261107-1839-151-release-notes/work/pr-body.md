## Summary

A chantier release used to publish auto-generated notes. Users saw a list of commits, with no
screenshots, no usage examples and no announcement text. This PR makes each release ship
reviewed release notes with visual evidence, usage examples and links to the docs, plus a
three-post announcement thread with one image. The notes are reviewed in the version PR and
published exactly as written.

## Deliverables

The release folder, committed with the version:

```text
docs/release-notes/YYYY-MM-DD-vX.Y.Z/
├── release-notes.md   GitHub release notes, images linked by bare file name
├── tweet.md           announcement thread: ## 1/, ## 2/, ## 3/, one Image: line
└── *.png              images of the notes and of the thread
```

`scripts/release_notes.py` has three modes:

| Mode | What it does |
| --- | --- |
| `--check` | Validates the folder (from 0.8.0 on), scans for private data. Run by `just check`. |
| `--prepare vX.Y.Z` | Validates, copies the images, rewrites their links to the release assets, prints the asset paths. |
| `--scan FILE...` | Lists home paths, emails, UUIDs and the local git identity found in files. |

## Changes

- `docs/release-process.md`: chantier's own release guideline (folder, notes structure, visuals, anonymisation, thread).
- `scripts/release_notes.py` and `justfile`: the check (`just check` now runs `release-notes`) and the staging of `docs/release-notes` in `just release`.
- `CONTRIBUTING.md`: the Release section publishes with `gh release create --notes-file` and the images attached; `--generate-notes` is gone.
- `skills/chantier/references/release-template.md`: a generic default for projects with no procedure of their own; linked from `driver.md` and `chief-of-staff.md`.
- `README.md`: layout lines.

## Impacts

No visual change. The first release to use this is 0.8.0; before that, `just check` prints `release-notes: none needed before 0.8.0`.

## Blast radius

Grade: 2. From 0.8.0 on, a release fails `just check` without valid notes. A `git revert` restores the previous release steps; nothing in the CLI changes.

## Test plan

- [x] New or changed tests: no behaviour change in the CLI; the script's refusals are shown by the dry run below
- [x] Local gates: `just check` passes (at 0.7.0 it prints `release-notes: none needed before 0.8.0`); `just scenario` passes
- [x] Evidence: dry run in a throwaway worktree (not pushed, removed), below
- [x] Review
- [x] CI green

Dry run (version set to 0.8.0 in the throwaway worktree):

```text
$ just check            (no notes folder)
release-notes: Expected one docs/release-notes/YYYY-MM-DD-v0.8.0/release-notes.md, found 0   exit=1
$ just check            (sample folder: title naming 0.8, one PNG, valid tweet.md)
release-notes: docs/release-notes/2026-11-07-v0.8.0/release-notes.md ok                       exit=0
$ release_notes.py --check, one defect at a time
image in a subfolder     Image next to the notes expected, found: sub/shot.png                   exit=1
image at an https URL    Image next to the notes expected, found: https://example.com/shot.png   exit=1
missing ## 3/            tweet.md must hold ## 1/, ## 2/ and ## 3/ in order, found ['1/', '2/']  exit=1
two Image: lines         tweet.md must hold exactly one Image: line, in post 1                   exit=1
post 3, no install link  Post 3 of tweet.md must link https://github.com/gsemet/chantier#install exit=1
home path in tweet.md    Private data in the release text: tweet.md:5: home path                 exit=1
email in the notes       Private data in the release text: release-notes.md:5: email             exit=1
UUID in the notes        Private data in the release text: release-notes.md:5: uuid              exit=1
$ release_notes.py --prepare v0.8.0 --output <tmp>/n.md --assets <tmp>/a
<tmp>/a/shot.png                                                                               exit=0
n.md: <img src="https://github.com/gsemet/chantier/releases/download/v0.8.0/shot.png" width="600">
$ release_notes.py --scan scan-bad.md   (git user name, home path, UUID)
scan-bad.md:1: git user name / scan-bad.md:2: home path / scan-bad.md:3: uuid                  exit=1
$ release_notes.py --scan scan-ok.md                                                           exit=0
```

Also: `generate-notes` no longer appears in `CONTRIBUTING.md`, which names `notes-file` and `release-process`; `release-template` is linked from `driver.md` and `chief-of-staff.md`; `git diff --stat origin/main` lists no file under the CLI, `agents/`, `com.github.copilot/agents/`, `.github/` or `scenario/`.

## Autonomous decisions

- The email pattern lets `@example.com` and `@example.org` through, because `user@example.com` is the anonymisation replacement.
- `--prepare` also validates `tweet.md` and copies the thread's image into the assets folder.

## Internal references

CR-151 release-notes

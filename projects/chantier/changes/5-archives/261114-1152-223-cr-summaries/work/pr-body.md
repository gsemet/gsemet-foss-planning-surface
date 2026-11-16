## Summary

The agents write Markdown, and the board's server stays deterministic and reads JSON. This adds a condensed `summary.json` to each change request's folder: its title, a one-line summary of its state, where the request came from (GitHub, GitLab or Jira issue, or verbal), labels and a group. A checksum of the covered Markdown files tells when a summary is late. A summary is a judgment, so an agent writes it; the CLI lists the gaps, stores what it is given and records the checksums. This PR is the CLI and the cards only: it draws nothing on the board.

## Deliverables

New command `chantier summary` with four actions:

```text
summary lint [<folder> ...]                         # lists gaps, exit 2 if any; writes nothing
summary set <folder> [--title T] [--summary S | --unchanged] [--tracker K]
summary label <folders> (--add L[,L] | --remove L[,L])
summary group <folders> (--name G | --clear)
```

| Module | Responsibility |
| --- | --- |
| `summaries/sources.py` | covered files, normalised SHA-256, diff |
| `summaries/origin.py` | the `issue:` line to `{kind, ref, url}` |
| `summaries/store.py` | read and write `summary.json` |
| `summaries/gaps.py` | unreadable, no summary, late; the walk |
| `summaries/view.py` | `summary_view(folder)` for the board's server |
| `commands/summary.py` | parsers, handlers, output lines |

Choices: the default `lint` walk leaves `5-archives` and `6-trash` out (a named archive folder is still checked); no frontmatter and no Markdown is ever changed; `STATUS` files are unchanged by a `summary.json`.

## Blast radius

Grade: **1**. A new command, new modules and card text; one small change makes the backlog `files` count in `STATUS.json` skip `summary.json`. `git revert` restores the previous behaviour.

## Autonomous decisions

- The `STATUS.json` backlog `files` count skips `summary.json`, so the STATUS files stay identical with or without it, as the specification requires.

## Known gaps

- Only the GitHub forge's scenario was run on this machine; the GitLab scenario and the Linux and macOS runs wait for CI.
- The scenario's byte comparison of CR-level STATUS files is weak: those files are not regenerated in the copy.
- `summary lint` on a copy of the repository's planning folder gave `39 gap(s) in 39 CRs` in 0.99 s (archives left out of the default walk), judged at the pre-restack head.

<details>
<summary>Details</summary>

## Changes

- `summary.json` records (`CrSummary`, `Origin`) in `core/records.py`; atomic JSON write.
- `commands/summary.py` and the `summaries/` package; the walk in `lifecycle/stages.py`.
- Cards: `concepts.md`, `chief-of-staff.md`, `griller.md`, `spec-writer.md`; `docs/planning-folder.md`.
- Scenario section 21 and extra checks in section 20.

## Human decisions

- The default `summary lint` walk leaves the archives out (a named archive folder is still checked); a separate pass, on the user's order, summarises the archives later.

## Impacts

No visual change. Agents that edit a CR's Markdown run `summary lint` and close its gaps.

## Test plan

- [x] New or changed tests: scenario section 21 (33 checks), passing at the pre-restack head
- [x] Local gates at the pre-restack head: `just check` and `just scenario` pass (long gate); mypy --strict also run for linux, darwin and win32 by the author
- [ ] Evidence: none, no visual change
- [x] Review: approved at the pre-restack head (the review covered this diff before it was committed as the pre-restack head)
- [ ] Verified at `955e7d6` (restack onto main; pending)
- [ ] CI green at `955e7d6` (restack onto main; pending)

## Internal references

- CR-223 cr-summaries; builds on the CLI restructure and root `pyproject.toml` of the base PRs.

</details>

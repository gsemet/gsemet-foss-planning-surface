## Description

The version PR for chantier v0.11.0: `release: v0.11.0` made by `just release minor` (0.10.0 to 0.11.0), the release folder `docs/release-notes/2026-11-17-v0.11.0/` with its three anonymised images, and the claims file `evals/results/claims-v0.11.0.md`. It sits on top of the stack (#258: PRs 251, 252, 249, 254, 257), so it shows the commits of those PRs too; merge it after them. It changes no code or card.

Every `feat:` and `fix:` commit since v0.10.0 appears once in the notes: the model per role and host (`faa4719`, `944f93c`, `2faa446`, `a92113f`) and the Configuration page (`4fc8ba8`) in the first two highlights, the PRs page (`edf4642`) and its merge signal (`849ac8c`) in the third, `066c34d` and `cc56e3c` in Smaller changes, `942e14d`, `51a3c8e` and `d15df0b` in All fixes. Not a row: `9eaef4a` is a `wip:` commit (the short startup core); it changes how every role starts, and the campaigns are what bring it to the test.

## Known gaps

- No campaign has run for v0.11.0: the real-direct run on a stack and the real-foreman run on a parallel batch are pending; they run at the desk before the merge, and the claims file and the notes get their results then. `full` and `copilot` are not run for this release.
- Every claim of the claims file is `not exercised`, campaign pending.

## Test plan

- [x] `just release minor` ran `just check` at `624f2d2`: passed (369 tests, `scripts/release_notes.py --check` ok).
- [x] Local Windows `just scenario` at `624f2d2`: passed.

---

<h1 align="center">chantier 0.11</h1>

<p align="center"><b>Choose each role's agent and model on Claude Code and Copilot, edit them from the board, and watch your batch's PRs live</b></p>

<p align="center"><sub>18 changes since 0.10.0 · Claude Code and GitHub Copilot · MIT</sub></p>

<p align="center">
<a href="https://github.com/gsemet/chantier#install">Install</a> ·
<a href="https://github.com/gsemet/chantier/blob/v0.11.0/docs/tutorial-claude-code.md">Tutorial</a> ·
<a href="https://github.com/gsemet/chantier/blob/v0.11.0/docs/use-cases.md">Use cases</a> ·
<a href="https://github.com/gsemet/chantier/compare/v0.10.0...v0.11.0">Full changes</a>
</p>

---

## 🎛 Pick the model of each role, per host

Each role now has a model on each host, and you choose it. chantier reads its configuration in four
layers, from weakest to strongest: its own shipped defaults, your planning surface's `chantier.yaml`,
the project's file in that surface, and the code repository's `chantier.yaml`. A layer carries only
what it changes, and `default` takes a value back to the layer below. A role with a model and no agent
of yours starts the plugin's agent on that model; on Copilot, where a named agent cannot take a
chosen model yet, it starts a generic agent with the role's contract in its prompt. Copilot's model
names come from GitHub's own tables, with each model's plans, and a name that matches several models
is refused with the identifiers it matches.

```yaml
hosts:
  claude:
    roles:
      inspector:
        model: opus
  copilot:
    roles:
      coder:
        model: gpt-6.1-terra
```

Say "run the inspector on Opus" to the Chief of Staff and it writes the lines. A running batch keeps
the team it started with; the change applies to the next one.

See [your own agents and models](https://github.com/gsemet/chantier/blob/v0.11.0/docs/agents-and-models.md).

## 🖥 Edit them from the board

The board has a Configuration page: for each host, one row per role, with the agent and the model in
the project's file in your planning surface, the value in effect and the layer it comes from, and how
the role starts. Every change is judged first, then written by Save, keeping the file's comments and
its other keys. When the code repository's own file overrides a value, the row says so.

| Configuration, per host and role |
| --- |
| ![The Configuration page: Copilot's roles with their agents and models, and the Copilot models with their plans](https://github.com/gsemet/chantier/blob/624f2d220eccbb00287cf9a756ea3bfbd3f0f99b/docs/release-notes/2026-11-17-v0.11.0/board-config.png?raw=true) |

See [the web board](https://github.com/gsemet/chantier/blob/v0.11.0/docs/web-board.md).

## 🔀 A live PRs page, and a merge it tells you about

The new PRs page reads your batch's PRs from the forge with your own `gh` or `glab`, read-only: one row
per change in merge order, with the PR's state, whether it conflicts and its checks, refreshed every
ten seconds while a PR is not done. "Ready to merge" needs the record and the forge to agree. When the
page sees a PR merged that the record does not hold, it leaves one line in a local file, and
`chantier status` prints it, so the Chief of Staff records the merge at its next look.

| The PRs page |
| --- |
| ![The PRs page: five PRs of a batch, merged, open, conflicting, draft and being checked by the forge](https://github.com/gsemet/chantier/blob/624f2d220eccbb00287cf9a756ea3bfbd3f0f99b/docs/release-notes/2026-11-17-v0.11.0/board-prs.png?raw=true) |

See [the web board](https://github.com/gsemet/chantier/blob/v0.11.0/docs/web-board.md).

## 🛠 Smaller changes

- **The board shows your planning surface.** The project picker's first entry is the surface, by name
  and path, and each project's line shows its folder and its repository.

  | The project picker |
  | --- |
  | ![The project picker: the planning surface, then three projects with their folder and repository](https://github.com/gsemet/chantier/blob/624f2d220eccbb00287cf9a756ea3bfbd3f0f99b/docs/release-notes/2026-11-17-v0.11.0/board-picker.png?raw=true) |

- **A roomier Triage.** The cards are at most 320 px wide, the backlog is a
  grid, hovering shows no scroll bar, and the side panel closes when you change view.
- **A model check for Copilot.** The Copilot evaluation checks that each role runs on its chosen model.

<details><summary><b>🐞 All fixes</b></summary>

- **The board.** Every Triage card has the same width at every window size, and the project count of
  the picker button wraps so its number stays readable.
- **The configuration page.** It writes the project file with LF, also when the file had CRLF.

</details>

<details><summary><b>🛠 For contributors</b></summary>

- **Not exercised by an eval.** No campaign has run for this release yet; the two chosen, a
  real-direct run on a stack and a real-foreman run on a parallel batch, run before the merge, and these
  notes are updated from their reports. `full` and the Copilot campaign are not run for this release.
  None of the release's changes has been brought to an eval's test:
  - the Copilot roles running on their chosen model and the model check, the Copilot model catalog;
  - the four layers of configuration with the shipped model defaults, and a role started on its
    configured model, with a generic agent where the host cannot;
  - the board's Configuration, PRs and Triage pages, the planning surface in the selector, the picker's
    count and the LF of the project file;
  - the local signal of a merge the PRs page sees, which `status` prints.
- This release also carries the short startup core: every role reads a short contract at start and
  defers its full card until an action names it. No campaign has brought it to the test yet.
- The release's claims file is `evals/results/claims-v0.11.0.md`: one row per change, its rail and
  its result.
- Known: direct mode on Copilot has not been run in a real campaign, and neither has GitLab.

</details>

---

## Announcement thread (a draft: you post it yourself, no agent does)

# Announcement thread for 0.11.0

## 1/

Until now, every chantier role ran the model its agent file said, and checking your PRs meant
switching to the forge. Now each role has a model per host that you set in a file, or from a page of
the board, and a PRs page shows the batch's PRs as the forge sees them.

chantier 0.11 also tells the Chief of Staff when the page sees a merge it has not recorded. Its
evals have not run yet: the notes say which changes no run has seen.

Image: https://github.com/gsemet/chantier/blob/624f2d220eccbb00287cf9a756ea3bfbd3f0f99b/docs/release-notes/2026-11-17-v0.11.0/board-prs.png?raw=true

## 2/

What changed, with captures from the board:
https://github.com/gsemet/chantier/releases/tag/v0.11.0

## 3/

chantier is a free Claude Code and GitHub Copilot plugin, MIT licensed. Install it, or update it
from its marketplace:
https://github.com/gsemet/chantier#install



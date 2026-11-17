# Change Specification: Release v0.8.0

## 1. What

Release chantier 0.8.0 from `main` (head 648289c at filing), by the project's own procedure:
[CONTRIBUTING.md](https://github.com/gsemet/chantier/blob/main/CONTRIBUTING.md) "Release" for the mechanics and
[docs/release-process.md](https://github.com/gsemet/chantier/blob/main/docs/release-process.md) for the notes, the announcement
thread and their images. This is the first release under that process: `just check` refuses a
missing or invalid `docs/release-notes/YYYY-MM-DD-v0.8.0/` folder.

## 2. Scope

The 13 non-merge commits of `v0.7.0..main`, among them: direct mode (a batch steered by the Chief of
Staff), `chantier init`, the spec-writer agent, the CR board's slots, a batch paused then closed on
the user's word, the default PR template, the batch-lifecycle and use-case docs, and the visual
release notes themselves. Every `feat:` and `fix:` commit appears exactly once in the notes.

## 3. Deliverables

- The version PR (`release: v0.8.0`, from `just release minor`), which also holds
  `docs/release-notes/<date>-v0.8.0/`: `release-notes.md`, `tweet.md` and the PNG captures.
- Captures from batch-08 only (board, `STATUS.md`, `report.md`, `conversation.md`, CLI output), each
  anonymised and scanned (`release_notes.py --scan`) before rendering with headless Chrome, and read
  by the Driver before committing. No docs SVG diagram.
- After the merge: the tag `v0.8.0` (`just tag`) and the GitHub release published with
  `release_notes.py --prepare v0.8.0`, `gh release create --notes-file`, images attached.

## 4. What the user reviews

The version PR: the notes, the thread and every image. Each irreversible action (merge, tag,
publish) waits for the user's approval (default grant). Only the user posts the thread.

## 5. Evidence

1. `just check` passes on the version PR, including `release_notes.py --check` on 0.8.0.
2. The tag `v0.8.0` points at the merged version commit on `main`.
3. The GitHub release v0.8.0 shows the notes with its images loaded from release assets.

Open questions: None.

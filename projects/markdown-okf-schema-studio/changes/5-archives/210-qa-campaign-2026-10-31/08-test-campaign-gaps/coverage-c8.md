# Coverage note — charter C8 (replay of the previous Highs)

Exercised: UX-01, UX-03, UX-04, UX-12, UX-16, UX-17, UX-25, UX-35, UX-38, each by a `q scenario` in `scenarios/ux-NN-*.json`.

Substitutions and limits:
- UX-16 and UX-17 ran on `synth/frontmatter-edge.md` (title field), because the OKF `SwRS-CORE-001.md` fixture is not in the workspace. UX-16 asserts one changed line only; the folded `description` and sequence re-indentation were not separately checked because the buffer diff shows exactly one line.
- UX-25 was replayed by opening a non-Markdown file with Quick Open (new fixtures `synth/ux25-nonmd-link.md`, `synth/ux25-export.py`), not by clicking the properties link (no `projectRoot` set up).
- UX-03 ran in the Open With editor with Cmd+Z once; successive Cmd+Z presses were not tried.
- UX-04 scenario types the item text without the `- ` marker, since Enter now continues the list.
- UX-12 asserts one changed line on the wide table only; aligned/compact tables are covered by other charters.

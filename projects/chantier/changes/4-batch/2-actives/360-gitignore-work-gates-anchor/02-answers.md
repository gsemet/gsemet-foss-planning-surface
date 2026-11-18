# Answers

- The user (2026-11-18): "Oui, spécifie les P1", after the standing word of the day "plus de question" (no more questions): no grill; the behaviour choices below are the Chief of Staff's.

## Settled by the Chief of Staff

- **The fix.** The planning folder's `.gitignore` entry becomes `**/work/gates/`; the scenario's check asserts the new text.
- **The sweep.** Every other entry of the shipped planning-folder `.gitignore` with a slash in the middle and no leading `**/` is checked the same way and fixed in the same CR when it has the same bug.
- **Existing planning folders.** Whatever writes or refreshes that `.gitignore` (`init`, or the step that adds missing entries) brings the new line to an existing folder; the old line may stay (it is harmless).
- Spec critic: no, a one-line ignore pattern and its test, with no role behaviour behind it.

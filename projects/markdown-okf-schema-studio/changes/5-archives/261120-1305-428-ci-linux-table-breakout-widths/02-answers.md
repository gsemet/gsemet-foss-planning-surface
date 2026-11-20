Short name: `linux-breakout`

# Answers (owner, 2026-11-20, Chief of Staff grill)

- Where: run the tableBreakout width tests in the existing Linux visual CI job (Chromium present), not a new xvfb job. (owner chose: 'Travail visuel')
- If Linux widths differ from Windows by more than 1 px, or any of the 12 owner verdicts changes: stop and ask the owner with the widths. (owner chose: 'S arrêter et demander')

- Open question 1 (where the Linux widths are recorded): keep them printed on every run through t.diagnostic in the committed test, so every visual log carries them; plus the Windows/Linux table in the PR body. Decided by the Chief of Staff under the owner's standing autonomy grant.

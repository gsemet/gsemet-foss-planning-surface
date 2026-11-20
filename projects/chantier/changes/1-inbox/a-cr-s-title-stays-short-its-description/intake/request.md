# A CR's title stays short; its description goes below

The user, 2026-11-20, on the refreshed board: seven inbox items written by a Griller (split off from planning-server) had no `#` heading and no `summary.json`, so the board's Title column showed their whole one-paragraph request (330 to 770 characters). "Le titre des CR est immense, ça va pas du tout. Y a-t-il un linter de ces fichiers pour forcer l'agent à mettre un titre court et une description plus longue ?" Nothing checks it today: `summary lint` checks a title exists, not its length; `validate` neither. The seven were fixed by hand with a short `# Title` heading.

Wanted:
- `validate` (and `summary lint`) refuse a CR whose title (summary title, else the request's heading, else its first line) is longer than a short limit (about 70 characters), and an intake request with no `#` heading, naming the file and the fix.
- `chantier file` never files a CR without a short title: it takes or asks for one, the request text going below it as the description.
- The Griller's, spec-writer's and Chief of Staff's cards say it: a short title, the description under it.
- The board never shows more than one line of title (truncated with the full text on hover) as a safety net.
